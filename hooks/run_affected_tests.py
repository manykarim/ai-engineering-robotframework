"""Run the tests an edit affects, and tell the agent the result.

As a hook (after an edit): for a changed .robot file under tests/, runs that file; for a changed
.resource file under resources/, runs every test file that imports it, directly or through other
resources. Tests tagged broken are left out. As a command, it takes the changed files:

    uv run --no-sync python hooks/run_affected_tests.py resources/checkout.resource
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from hookio import ROOT, read_call, report

IMPORT = re.compile(r"^Resource\s{2,}(\S.*?)\s*$", re.M)
TIMEOUT = 280  # seconds; the wiring gives the hook 300


def imports(file: Path) -> set[Path]:
    """The resource files a file imports, resolved the way robot.toml's python-path does."""
    found = set()
    for name in IMPORT.findall(file.read_text(encoding="utf-8")):
        for base in (file.parent, ROOT):
            candidate = (base / name).resolve()
            if candidate.is_file():
                found.add(candidate)
                break
    return found


def affected(changed: list[Path]) -> list[Path]:
    tests = sorted((ROOT / "tests").rglob("*.robot"))
    graph = {f: imports(f) for f in tests + sorted((ROOT / "resources").rglob("*.resource"))}
    targets = {(ROOT / c).resolve() for c in changed}

    def reaches(file: Path, seen: set[Path]) -> bool:
        if file in targets:
            return True
        return any(reaches(dep, seen | {file}) for dep in graph.get(file, ()) if dep not in seen)

    return [t for t in tests if reaches(t.resolve(), set())]


def run(files: list[Path]) -> tuple[str, bool]:
    names = ", ".join(f.relative_to(ROOT).as_posix() for f in files)
    robotcode = shutil.which("robotcode", path=str(Path(sys.executable).parent)) or "robotcode"
    try:
        subprocess.run([robotcode, "robot", "--exclude", "broken", "--console", "none", *map(str, files)],
                       cwd=ROOT, capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return f"The affected tests ({names}) did not finish within {TIMEOUT} s.", True
    output = ROOT / "results" / "output.xml"
    if not output.is_file():
        return f"The affected tests ({names}) produced no results. Run them yourself: uv run robotcode robot", True
    failed, passed = [], 0
    for test in ET.parse(output).getroot().iter("test"):
        status = test.find("status")
        if status.get("status") == "FAIL":
            failed.append(f"{test.get('name')}: {(status.text or '').strip()[:200]}")
        else:
            passed += 1
    summary = f"Affected tests ({names}): {passed} passed, {len(failed)} failed."
    return (summary + "".join(f"\n- {f}" for f in failed)), bool(failed)


def main(argv: list[str]) -> int:
    call = None if argv else read_call()
    if call is None:
        changed = [Path(a) for a in argv]
    elif call.kind == "edit":
        changed = [e.path for e in call.edits]
    else:
        return 0
    changed = [c for c in changed if c.suffix in (".robot", ".resource") and c.parts[:1] in (("tests",), ("resources",))]
    files = affected(changed) if changed else []
    if not files:
        return 0
    message, problem = run(files)
    if call is None:
        print(message)
        return 1 if problem else 0
    report(call, message, problem)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
