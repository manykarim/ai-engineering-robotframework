"""No shortcut to green: a test is made right, not made to pass.

As a hook (before an edit): refuses an edit that adds the `broken` tag, `Skip`, `Run Keyword And
Ignore Error` or `Pass Execution` to a .robot file under tests/. As a command, it reports every
one of them in the given files or folders:

    uv run --no-sync python hooks/no_shortcut_to_green.py tests/
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

from hookio import ROOT, deny, read_call

# Robot Framework matches keyword names ignoring case, spaces and underscores, with or without "BuiltIn."
SHORTCUTS = {
    "skip": "Skip",
    "skipif": "Skip If",
    "passexecution": "Pass Execution",
    "passexecutionif": "Pass Execution If",
    "runkeywordandignoreerror": "Run Keyword And Ignore Error",
}
TAG_SETTINGS = {"[tags]", "testtags", "forcetags", "defaulttags", "settags", "builtin.settags"}
DOCUMENTATION = {"[documentation]", "documentation", "metadata"}
CELL_SEPARATOR = re.compile(r"\s{2,}|\t|\s\|\s")
RULE = ("Make the test right instead: fix the keyword or the locator, or, when the shop does not do what "
        "openspec/specs/shop/ says, leave the test failing and report it. The `broken` tag belongs to the two tests "
        "that are broken on purpose, and no other (convention 7 of docs/conventions.md).")


def normalize(cell: str) -> str:
    name = cell.lower().replace(" ", "").replace("_", "")
    return name.removeprefix("builtin.")


def findings(text: str) -> list[tuple[int, str]]:
    """(line number, shortcut) for every shortcut to green in Robot Framework text."""
    found, section, previous = [], "", None
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("*"):
            section, previous = stripped.strip("* ").lower(), None
            continue
        if not stripped or stripped.startswith("#"):
            continue
        if not line[:1].isspace() and not section.startswith("setting"):
            previous = None  # a test or keyword name
            continue
        cells = [c for c in CELL_SEPARATOR.split(stripped) if c]
        comment = next((i for i, c in enumerate(cells) if c.startswith("#")), len(cells))
        cells = cells[:comment]
        if cells and cells[0] == "...":
            cells, setting = cells[1:], previous
        else:
            setting = normalize(cells[0]) if cells else None
            previous = setting
        if setting in DOCUMENTATION:
            continue
        if setting in TAG_SETTINGS:
            found += [(number, "the `broken` tag") for c in cells if normalize(c) == "broken"]
            continue
        found += [(number, SHORTCUTS[normalize(c)]) for c in cells if normalize(c) in SHORTCUTS]
    return found


def is_test_file(path: Path) -> bool:
    return path.suffix == ".robot" and path.parts[:1] == ("tests",)


def main(argv: list[str]) -> int:
    call = None if argv else read_call()
    if call is not None:
        for edit in call.edits if call.kind == "edit" else []:
            if not is_test_file(edit.path):
                continue
            # Only what the edit adds counts: the tests broken on purpose already carry their tag.
            added = Counter(shortcut for _, shortcut in findings(edit.after))
            added.subtract(Counter(shortcut for _, shortcut in findings(edit.before)))
            new = [shortcut for shortcut, count in added.items() if count > 0]
            if new:
                deny(call, f"Rejected: this edit adds {', '.join(new)} to {edit.path.as_posix()}, a shortcut to "
                           f"green. {RULE}")
        return 0

    paths = [Path(a) for a in argv] or [ROOT / "tests"]
    files = [f for p in paths for f in (sorted(p.rglob("*.robot")) if p.is_dir() else [p])]
    total = 0
    for file in files:
        for number, shortcut in findings(file.read_text(encoding="utf-8")):
            print(f"{file}:{number}: {shortcut} in a test file")
            total += 1
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
