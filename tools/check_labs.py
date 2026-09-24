"""Check the lab contract (spec: workshop/labs).

    uv run --no-sync python tools/check_labs.py [--root DIR] [--pending-transcripts]

Checks every lab folder under labs/: its files, the header table every INSTRUCTIONS.md
opens with, the time budget against the timetable, the sections, relative links, glossary
anchors, and that participant-facing text gives no answer away. Exits with status 1 on any
finding. --pending-transcripts accepts links to transcripts that have not been recorded yet.
"""
from __future__ import annotations

import argparse
import re
import sys
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
HEADER_ROWS = ("Module", "Time", "Shop preset", "You need", "You start from")
SECTIONS = ("## Steps", "## Stretch", "## If your agent fails")

# Where relative links may point: what the documentation site renders.
LINK_ROOTS = ("labs/", "docs/", "transcripts/", "SETUP.md", "GLOSSARY.md")
# Transcripts that another change records; a link to them may dangle until then.
RECORDED_ELSEWHERE = {"transcripts/lab-09-ci.md": "recorded with the CI workflows (ci-and-site)"}

# Answers participant-facing text must not give away (spec: Labs do not give the answers away).
GIVEAWAYS = [
    (re.compile(r"\b(BUG|LOCATOR)_[A-Z_]+"), "a feature flag"),
    (re.compile(r"MISSING_BUTTON|WRONG_PRICE|BROKEN_LINKS|SLOW_RESPONSE|CHECKOUT_TOTAL"), "a planted bug"),
    (re.compile(r"omits? (the )?tax|without tax|1\.15|\b15 ?%", re.I), "the checkout or price defect"),
    (re.compile(r"products? 5 and 10|3, 6, 9|4, 8 and 12", re.I), "which products a defect hits"),
    (re.compile(r'role=link\[name="Reset"\]|inline locator is in|WEB-002_AC-10', re.I), "the inline locator"),
    (re.compile(r"4 stars (and|&) up", re.I), "the cause of the Module 5 broken test"),
    (re.compile(r"'?899\.0'?(?!0)|unformatted|as numbers? from the API", re.I), "the cause of the Module 4 broken test"),
]
PARTICIPANT_FILES = ("labs/**/*.md", "GLOSSARY.md", "docs/environments.md")
STORY_DIR = "labs/lab-05-prompt-to-green/stories/"  # copied verbatim; not ours to police

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
    if table.get("Time") and table["Time"] != f"{minutes} minutes":
        problems.append(f"{folder}: Time should be '{minutes} minutes' (the timetable), is '{table['Time']}'")
    if table.get("Shop preset") and f"`{preset}`" not in table["Shop preset"]:
        problems.append(f"{folder}: Shop preset should be `{preset}`, is '{table['Shop preset']}'")
    for section in SECTIONS:
        if not re.search(rf"^{re.escape(section)}\s*$", text, re.M):
            problems.append(f"{folder}: no '{section}' section")
    if not re.search(r"^1\. ", text.split("## Steps")[-1], re.M):
        problems.append(f"{folder}: the steps are not numbered")
    fails = text.split("## If your agent fails")[-1]
    if f"transcripts/{folder}.md" not in fails:
        problems.append(f"{folder}: 'If your agent fails' does not link transcripts/{folder}.md")
    checklist = (lab / "checklist.md").read_text(encoding="utf-8")
    if len(re.findall(r"^- \[ \] ", checklist, re.M)) < 2:
        problems.append(f"{folder}: checklist.md has fewer than two '- [ ]' items")
    return problems


def check_links(root: Path, path: Path, pending: bool) -> list[str]:
    problems = []
    rel = path.relative_to(root).as_posix()
    text = re.sub(r"^```.*?^```", "", path.read_text(encoding="utf-8"), flags=re.M | re.S)  # code shows, never links
    for target in LINK.findall(text):
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
            if repo_path in RECORDED_ELSEWHERE or (pending and repo_path.startswith("transcripts/")):
                continue
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
                for regex, what in GIVEAWAYS:
                    if regex.search(line):
                        problems.append(f"{rel}:{number}: gives away {what}: {line.strip()[:80]}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="check-labs", description=__doc__.split("\n\n")[0])
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root (default: %(default)s)")
    parser.add_argument("--pending-transcripts", action="store_true",
                        help="accept links to transcripts that have not been recorded yet")
    args = parser.parse_args(argv)
    root = args.root.resolve()

    problems = []
    folders = {p.name for p in (root / "labs").iterdir() if p.is_dir()} if (root / "labs").is_dir() else set()
    problems += [f"labs/{name}: missing lab folder" for name in sorted(set(LABS) - folders)]
    problems += [f"labs/{name}: not a lab of the timetable" for name in sorted(folders - set(LABS))]
    for folder, spec in LABS.items():
        if folder in folders:
            problems += check_lab(root, folder, spec)
    for pattern in PARTICIPANT_FILES + ("docs/**/*.md", "transcripts/**/*.md"):
        for path in sorted(set(root.glob(pattern))):
            if not path.relative_to(root).as_posix().startswith(STORY_DIR):
                problems += check_links(root, path, args.pending_transcripts)
    problems += check_giveaways(root)

    for problem in dict.fromkeys(problems):
        print(problem)
    print("the labs meet their contract" if not problems else f"{len(set(problems))} finding(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
