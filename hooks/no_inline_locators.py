"""Reject locator literals in test files: convention 2, "Locators live in resources".

As a hook (before an edit): refuses an edit that writes a locator literal into a .robot file
under tests/. As a command, it reports every locator literal in the given files or folders:

    uv run --no-sync python hooks/no_inline_locators.py tests/
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

from hookio import ROOT, deny, read_call

LOCATOR = re.compile(
    r"""^(?:
        (?:css|xpath|id|text|role|data-testid)=      # a selector engine prefix
      | \(?//                                        # XPath
      | \\\#[A-Za-z]                                 # #id, escaped as Robot Framework needs it
      | \.[A-Za-z][\w-]*                             # .class
      | \[[\w-]+[~|^$*]?=                           # [attribute=value]; [Tags] is a setting
      | [a-z][a-z0-9]*(?:\[|:has|:text|:nth|:visible) # button:has-text(...), a[href=...]
    )""",
    re.X,
)
CELL_SEPARATOR = re.compile(r"\s{2,}|\t|\s\|\s")
RULE = ('Convention 2 of docs/conventions.md, "Locators live in resources": test files call keywords, and every '
        "locator is written inside a keyword under resources/. Move the locator into a keyword there.")


def findings(text: str) -> list[tuple[int, str]]:
    """(line number, locator) for every locator literal in Robot Framework text."""
    found, documentation = [], False
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not line[:1].isspace() or not stripped or stripped.startswith("#"):
            documentation = False
            continue
        cells = [c for c in CELL_SEPARATOR.split(stripped) if c]
        if cells[0] == "...":
            if documentation:
                continue
            cells = cells[1:]
        else:
            documentation = cells[0].lower() == "[documentation]"
            if documentation:
                continue
        for cell in cells:
            if LOCATOR.match(cell) or " >> " in cell:
                found.append((number, cell))
    return found


def is_test_file(path: Path) -> bool:
    return path.suffix == ".robot" and path.parts[:1] == ("tests",)


def main(argv: list[str]) -> int:
    call = None if argv else read_call()
    if call is not None:
        for edit in call.edits if call.kind == "edit" else []:
            if not is_test_file(edit.path):
                continue
            # Only what the edit adds counts: a file may already hold a locator literal.
            added = Counter(cell for _, cell in findings(edit.after))
            added.subtract(Counter(cell for _, cell in findings(edit.before)))
            new = [cell for cell, count in added.items() if count > 0]
            if new:
                deny(call, f"Rejected: this edit adds the locator literal {new[0]!r} to {edit.path}. {RULE}")
        return 0

    paths = [Path(a) for a in argv] or [ROOT / "tests"]
    files = [f for p in paths for f in (sorted(p.rglob("*.robot")) if p.is_dir() else [p])]
    total = 0
    for file in files:
        for number, locator in findings(file.read_text(encoding="utf-8")):
            print(f"{file}:{number}: locator literal {locator!r} in a test file")
            total += 1
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
