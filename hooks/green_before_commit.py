"""Block a commit unless the latest suite run is green and newer than every change to the tests.

As a hook (before a shell command): lets every command through except `git commit`, which it
blocks when results/output.xml is missing, is older than the newest file under tests/ or
resources/, or holds a failed test that is not tagged broken. As a command, it prints the verdict:

    uv run --no-sync python hooks/green_before_commit.py --check
"""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET

from hookio import ROOT, deny, read_call

OUTPUT = ROOT / "results" / "output.xml"
COMMIT = re.compile(r"\bgit\s+(?:-\S+\s+(?:[^-\s]\S*\s+)?)*commit\b")
RUN = "Run the suite first: uv run robotcode robot"


def verdict() -> str | None:
    """Why a commit must wait, or None when it may go ahead."""
    if not OUTPUT.is_file():
        return f"No suite run found (results/output.xml is missing). {RUN}"
    changed = [p for folder in ("tests", "resources") for p in (ROOT / folder).rglob("*") if p.is_file()]
    newest = max(changed, key=lambda p: p.stat().st_mtime, default=None)
    if newest is not None and newest.stat().st_mtime > OUTPUT.stat().st_mtime:
        return (f"The latest suite run is older than your last change ({newest.relative_to(ROOT).as_posix()}). {RUN}")
    failed = []
    for test in ET.parse(OUTPUT).getroot().iter("test"):
        status = test.find("status")
        tags = {tag.text for tag in test.iter("tag")}
        if status is not None and status.get("status") == "FAIL" and "broken" not in tags:
            failed.append(test.get("name"))
    if failed:
        listed = "; ".join(failed[:5]) + (f"; and {len(failed) - 5} more" if len(failed) > 5 else "")
        return f"The latest suite run has {len(failed)} failed test(s): {listed}. Fix them before you commit."
    return None


def main(argv: list[str]) -> int:
    call = None if argv else read_call()
    if call is None:
        reason = verdict()
        print(reason or "The latest suite run is green and up to date: a commit may go ahead.")
        return 1 if reason else 0
    if call.kind == "shell" and COMMIT.search(call.command):
        reason = verdict()
        if reason:
            deny(call, f"Commit blocked: {reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
