"""Check the lab contract (spec: workshop/labs) and that main holds no answers (spec: workshop/solutions).

    uv run --no-sync python tools/check_labs.py [--root DIR] [--solutions REF] [--pending-transcripts]
                                                [--show-patterns]

Checks every lab folder under labs/: its files, the header table every INSTRUCTIONS.md
opens with, the time budget against the timetable, the sections, links and glossary
anchors, and that participant-facing text gives no answer away. Links to the site's
transcripts, reference pages and answer sheet are checked against the solutions branch,
where that material lives. Every tracked file on main is scanned for answers. Exits with
status 1 on any finding. --pending-transcripts accepts links to transcripts that have not
been recorded yet, and to reference pages not written yet; --show-patterns prints the answer patterns.
"""
from __future__ import annotations

import argparse
import base64
import re
import subprocess
import sys
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# folder -> (module, minutes, preset). Minutes are the lab share of each module in the
# master document's timetable; Lab 0 fills its whole 30-minute module.
LABS = {
    "lab-00-arrival": ("0", 30, "clean"),
    "lab-02-context": ("2", 25, "clean"),
    "lab-03-skills": ("3", 25, "clean"),
    "lab-04-robotcode": ("4", 25, "clean"),
    "lab-05-prompt-to-green": ("5", 30, "clean"),
    "lab-06-mcp": ("6", 25, "clean"),
    "lab-07-hooks-toolbelt": ("7", 20, "buggy"),
    "lab-08-healing": ("8", 12, "drift_and_bug"),
    "lab-09-ci": ("9", 15, "clean"),
}
# The bonus labs: self-paced after the day, so an estimated time instead of a timetable share.
BONUS = {
    "bonus-1-library": ("Bonus 1", 120, "clean"),
    "bonus-2-tool": ("Bonus 2", 60, "clean"),
}
HEADER_ROWS = ("Module", "Time", "Shop preset", "You need", "You start from")
SECTIONS = ("## Steps", "## Stretch", "## Compare with the reference", "## If your agent fails")

# Where relative links may point: what the documentation site renders from main.
LINK_ROOTS = ("labs/", "docs/", "SETUP.md", "GLOSSARY.md")
# The site, and its paths that the build takes from the solutions branch (spec: workshop/docs-site).
SITE = "https://manykarim.github.io/ai-engineering-robotframework"
FROM_SOLUTIONS = ("transcripts", "solutions", "docs/facilitator/suite-outcomes")
SOLUTIONS = "origin/solutions"

# Answers that must not appear: in participant-facing text (spec: Labs do not give the answers away), and
# for scope "all" in any file on main (spec: No answers on main). The patterns are stored base64-encoded,
# so that this file is not itself where an agent finds the answers; --show-patterns prints them. To add one:
#     python -c "import base64, sys; print(base64.b64encode(sys.argv[1].encode()).decode())" '<regex>'
_ENCODED = [
    ("XGIoQlVHfExPQ0FUT1IpX1tBLVpfXSs=", 0, "a feature flag", "all"),
    ("TUlTU0lOR19CVVRUT058V1JPTkdfUFJJQ0V8QlJPS0VOX0xJTktTfFNMT1dfUkVTUE9OU0V8Q0hFQ0tPVVRfVE9UQUw=", 0,
     "a planted bug", "all"),
    ("b21pdHM/ICh0aGUgKT90YXh8d2l0aG91dCB0YXh8MVwuMTV8XGIxNSA/JQ==", re.I, "the checkout or price defect", "all"),
    ("cHJvZHVjdHM/IDUgYW5kIDEwfDMsIDYsIDl8NCwgOCBhbmQgMTI=", re.I, "which products a defect hits", "all"),
    ("cm9sZT1saW5rXFtuYW1lPSJSZXNldCJcXXxpbmxpbmUgbG9jYXRvciBpcyBpbg==", re.I, "where the inline locator is", "all"),
    ("V0VCLTAwMl9BQy0xMA==", 0, "the test with the inline locator", "participant"),  # every test listing has it
    ("NCBzdGFycyAoYW5kfCYpIHVw", re.I, "the cause of the Module 5 broken test", "all"),
    ("Jz84OTlcLjAnPyg/ITApfHVuZm9ybWF0dGVkfGFzIG51bWJlcnM/IGZyb20gdGhlIEFQSQ==", re.I,
     "the cause of the Module 4 broken test", "all"),
]
GIVEAWAYS = [(re.compile(base64.b64decode(b).decode(), f), what, scope) for b, f, what, scope in _ENCODED]
PARTICIPANT_FILES = ("labs/**/*.md", "GLOSSARY.md", "docs/environments.md", "docs/robotcode.md",
                     "docs/building-with-agents.md")
STORY_DIR = "labs/lab-05-prompt-to-green/stories/"  # copied verbatim; not ours to police
# What the scan of main leaves out: the suite the labs work on, the shop's specifications (correct behaviour,
# also as archived deltas), the stories copied from the shop's repository, and lock files full of version numbers.
EXEMPT = re.compile(r"^(tests/|resources/|labs/lab-05-prompt-to-green/stories/)|(^|/)specs/shop/|(^|/)[^/]*\.lock$"
                    r"|(^|/)package-lock\.json$")

LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")


def slug(heading: str) -> str:
    """GitHub's and Docusaurus' anchor for a heading."""
    text = re.sub(r"[`*_]", "", heading.strip().lower())
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def anchors(path: Path) -> set[str]:
    return {slug(m.group(1)) for m in re.finditer(r"^#{1,6} (.+)$", path.read_text(encoding="utf-8"), re.M)}


def header_table(text: str) -> dict[str, str]:
    rows = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0] and not set(cells[0]) <= {"-", ":"}:
            rows[cells[0]] = cells[1]
    return rows


def check_lab(root: Path, folder: str, spec: tuple[str, int, str]) -> list[str]:
    module, minutes, preset = spec
    lab = root / "labs" / folder
    problems = [f"{folder}: missing {name}" for name in ("INSTRUCTIONS.md", "checklist.md") if not (lab / name).is_file()]
    if problems:
        return problems
    text = (lab / "INSTRUCTIONS.md").read_text(encoding="utf-8")
    before_steps = text.split("## Steps")[0]
    table = header_table(before_steps)
    for row in HEADER_ROWS:
        if not table.get(row):
            problems.append(f"{folder}: the header table has no '{row}' row before the steps")
    if table.get("Module") and not table["Module"].startswith(f"{module} "):
        problems.append(f"{folder}: Module should start with '{module} ', is '{table['Module']}'")
    if folder in BONUS:
        if table.get("Time") and not (f"{minutes} minutes" in table["Time"] and "self-paced" in table["Time"]):
            problems.append(f"{folder}: Time should hold '{minutes} minutes' and 'self-paced', is '{table['Time']}'")
    elif table.get("Time") and table["Time"] != f"{minutes} minutes":
        problems.append(f"{folder}: Time should be '{minutes} minutes' (the timetable), is '{table['Time']}'")
    if table.get("Shop preset") and f"`{preset}`" not in table["Shop preset"]:
        problems.append(f"{folder}: Shop preset should be `{preset}`, is '{table['Shop preset']}'")
    for section in SECTIONS:
        if not re.search(rf"^{re.escape(section)}\s*$", text, re.M):
            problems.append(f"{folder}: no '{section}' section")
    if not re.search(r"^1\. ", text.split("## Steps")[-1], re.M):
        problems.append(f"{folder}: the steps are not numbered")
    fails = text.split("## If your agent fails")[-1]
    if f"{SITE}/transcripts/{folder})" not in fails:
        problems.append(f"{folder}: 'If your agent fails' does not link {SITE}/transcripts/{folder}")
    reference = text.split("## Compare with the reference")[-1].split("\n## ")[0]
    if f"{SITE}/solutions/{folder})" not in reference:
        problems.append(f"{folder}: 'Compare with the reference' does not link {SITE}/solutions/{folder}")
    checklist = (lab / "checklist.md").read_text(encoding="utf-8")
    if len(re.findall(r"^- \[ \] ", checklist, re.M)) < 2:
        problems.append(f"{folder}: checklist.md has fewer than two '- [ ]' items")
    return problems


@cache
def on_solutions(root: Path, ref: str, path: str) -> str | None:
    """A file's text on the solutions branch, or None."""
    done = subprocess.run(["git", "-C", str(root), "show", f"{ref}:{path}"], capture_output=True, text=True)
    return done.stdout if done.returncode == 0 else None


@cache
def has_ref(root: Path, ref: str) -> bool:
    return subprocess.run(["git", "-C", str(root), "rev-parse", "--verify", "--quiet", ref],
                          capture_output=True).returncode == 0


def check_site_link(root: Path, rel: str, target: str, ref: str, pending: bool) -> list[str]:
    """A link to a page of the site: the Markdown file it renders must exist where the build takes it from."""
    page, _, anchor = target[len(SITE) + 1:].partition("#")
    page = page.rstrip("/")
    candidates = [f"{page}.md", f"{page}/README.md"]
    if page.startswith(FROM_SOLUTIONS):
        if not has_ref(root, ref):
            return [f"{rel}: cannot check '{target}': {ref} is missing (git fetch origin solutions)"]
        text = next((t for c in candidates if (t := on_solutions(root, ref, c)) is not None), None)
        where = f"the solutions branch ({ref})"
    else:
        found = next((root / c for c in candidates if (root / c).is_file()), None)
        text = found.read_text(encoding="utf-8") if found else None
        where = "main"
    if text is None:
        pending_page = page.startswith(("transcripts/", "solutions/"))
        return [] if pending and pending_page else [f"{rel}: link '{target}' has no page on {where}"]
    if anchor and anchor not in {slug(m.group(1)) for m in re.finditer(r"^#{1,6} (.+)$", text, re.M)}:
        return [f"{rel}: link '{target}' has no heading '#{anchor}' on {where}"]
    return []


def check_links(root: Path, path: Path, pending: bool, ref: str = SOLUTIONS) -> list[str]:
    problems = []
    rel = path.relative_to(root).as_posix()
    text = re.sub(r"^```.*?^```", "", path.read_text(encoding="utf-8"), flags=re.M | re.S)  # code shows, never links
    for target in LINK.findall(text):
        if target.startswith(SITE + "/"):
            problems += check_site_link(root, rel, target, ref, pending)
            continue
        if re.match(r"[a-z]+:", target) or target.startswith("#"):
            continue
        file_part, _, anchor = target.partition("#")
        resolved = (path.parent / file_part).resolve() if file_part else path
        try:
            repo_path = resolved.relative_to(root.resolve()).as_posix()
        except ValueError:
            problems.append(f"{rel}: link '{target}' leaves the repository")
            continue
        if not any(repo_path == r or repo_path.startswith(r) for r in LINK_ROOTS):
            problems.append(f"{rel}: link '{target}' points outside {', '.join(LINK_ROOTS)}; name it as a code path")
            continue
        if not resolved.exists():
            problems.append(f"{rel}: link '{target}' does not resolve")
            continue
        if anchor and resolved.suffix == ".md" and anchor not in anchors(resolved):
            problems.append(f"{rel}: link '{target}' has no heading '#{anchor}' in {repo_path}")
    return problems


def check_giveaways(root: Path) -> list[str]:
    problems = []
    for pattern in PARTICIPANT_FILES:
        for path in sorted(root.glob(pattern)):
            rel = path.relative_to(root).as_posix()
            if rel.startswith(STORY_DIR):
                continue
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                for regex, what, _ in GIVEAWAYS:
                    if regex.search(line):
                        problems.append(f"{rel}:{number}: gives away {what}: {line.strip()[:80]}")
    return problems


def main_files(root: Path) -> list[str]:
    """The files main tracks; outside a git checkout, every file but the usual build and tool folders."""
    done = subprocess.run(["git", "-C", str(root), "ls-files"], capture_output=True, text=True)
    if done.returncode == 0:
        return done.stdout.splitlines()
    skip = re.compile(r"(^|/)(\.git|\.venv|node_modules|results|build|\.docusaurus|__pycache__)(/|$)")
    return [p.relative_to(root).as_posix() for p in sorted(root.rglob("*"))
            if p.is_file() and not skip.search(p.relative_to(root).as_posix())]


def check_main(root: Path) -> list[str]:
    """No file on main states an answer (spec: workshop/solutions, No answers on main)."""
    problems = []
    for rel in main_files(root):
        if EXEMPT.search(rel) or not (root / rel).is_file():
            continue
        try:
            text = (root / rel).read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(text.splitlines(), 1):
            for regex, what, scope in GIVEAWAYS:
                if scope == "all" and regex.search(line):
                    problems.append(f"{rel}:{number}: states {what}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="check-labs", description=__doc__.split("\n\n")[0])
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root (default: %(default)s)")
    parser.add_argument("--solutions", default=SOLUTIONS, help="the solutions branch's ref (default: %(default)s)")
    parser.add_argument("--pending-transcripts", action="store_true",
                        help="accept links to transcripts and reference pages that have not been written yet")
    parser.add_argument("--show-patterns", action="store_true", help="print the answer patterns, decoded, and exit")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if args.show_patterns:
        for regex, what, scope in GIVEAWAYS:
            print(f"{what} ({'everywhere on main' if scope == 'all' else 'participant files'}): {regex.pattern}")
        return 0

    problems = []
    folders = {p.name for p in (root / "labs").iterdir() if p.is_dir()} if (root / "labs").is_dir() else set()
    problems += [f"labs/{name}: missing lab folder" for name in sorted((set(LABS) | set(BONUS)) - folders)]
    problems += [f"labs/{name}: not a lab of the timetable or a bonus lab"
                 for name in sorted(folders - set(LABS) - set(BONUS))]
    for folder, spec in {**LABS, **BONUS}.items():
        if folder in folders:
            problems += check_lab(root, folder, spec)
    tracked = set(main_files(root))
    for pattern in PARTICIPANT_FILES + ("docs/**/*.md", "README.md"):
        for path in sorted(set(root.glob(pattern))):
            rel = path.relative_to(root).as_posix()
            if rel in tracked and not rel.startswith(STORY_DIR):  # not the reference material a site build adds
                problems += check_links(root, path, args.pending_transcripts, args.solutions)
    problems += check_giveaways(root)
    problems += check_main(root)

    for problem in dict.fromkeys(problems):
        print(problem)
    print("the labs meet their contract" if not problems else f"{len(set(problems))} finding(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
