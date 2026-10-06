# Lab 7 - Hooks and the toolbelt: the reference

[Lab 7](../labs/lab-07-hooks-toolbelt/INSTRUCTIONS.md) wires four hooks into your agent, has it write and wire a
hook of your own, moves the suite's one inline locator into a keyword, and has your agent draft an issue for a defect
it finds under `buggy`. [Transcript](../transcripts/lab-07-hooks-toolbelt.md).

## The reference

The wiring for Claude Code, merged into `.claude/settings.json` beside the plugin of Lab 4: the four hooks of
`hooks/README.md`, and the rehearsal's own hook next to the locator check. For Codex and GitHub Copilot,
`hooks/README.md` names the file each needs.

```json
{
  "extraKnownMarketplaces": {
    "robotframework-agent-plugins": {
      "source": {
        "source": "github",
        "repo": "robotcodedev/robotframework-agent-plugins"
      }
    }
  },
  "enabledPlugins": {
    "robotcode@robotframework-agent-plugins": true
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "uv run --no-sync --project \"$CLAUDE_PROJECT_DIR\" python \"$CLAUDE_PROJECT_DIR/hooks/no_inline_locators.py\""
          }
        ]
      },
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "uv run --no-sync --project \"$CLAUDE_PROJECT_DIR\" python \"$CLAUDE_PROJECT_DIR/hooks/no_shortcut_to_green.py\""
          }
        ]
      },
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          {
            "type": "command",
            "command": "uv run --no-sync --project \"$CLAUDE_PROJECT_DIR\" python \"$CLAUDE_PROJECT_DIR/hooks/green_before_commit.py\""
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "uv run --no-sync --project \"$CLAUDE_PROJECT_DIR\" python \"$CLAUDE_PROJECT_DIR/hooks/static_check.py\"",
            "timeout": 60
          }
        ]
      },
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "uv run --no-sync --project \"$CLAUDE_PROJECT_DIR\" python \"$CLAUDE_PROJECT_DIR/hooks/run_affected_tests.py\"",
            "timeout": 300
          }
        ]
      }
    ]
  }
}
```

The own hook, "No shortcut to green" from the menu in [Hooks](../docs/hooks.md#writing-your-own), as the agent wrote
it from the lab's prompt, `hooks/no_shortcut_to_green.py`:

```python
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
```

The inline locator, moved into a keyword:

```diff
--- a/resources/catalogue.resource
+++ b/resources/catalogue.resource
@@ -63,6 +63,11 @@ Apply Filters
     Click    ${FILTERS} >> role=button[name="Apply filters"]
     Wait For Elements State    ${GRID}    visible
 
+Reset Filters
+    [Documentation]    Clicks the "Reset" link, found by its visible text.
+    Click    ${FILTERS} >> a:has-text("Reset")
+    Wait For Elements State    ${GRID}    visible
+
 Get Category Checkbox Count
     ${count}=    Get Element Count    ${FILTERS} >> role=group[name="Categories"] >> role=checkbox
     RETURN    ${count}
--- a/tests/ui/catalogue.robot
+++ b/tests/ui/catalogue.robot
@@ -65,7 +65,7 @@ WEB-002_AC-10 Reset Filters
     Go To Catalogue
     Check Category    Audio
     Apply Filters
-    Click    role=link[name="Reset"]
+    Reset Filters
     Filter Checkboxes Should All Be Unchecked
     ${range}=    Get Price Range Values
     Should Be Equal    ${range}    ${{ ["39.50", "899.00"] }}
```

## Why it is a good result

- **Each hook runs at its moment:** the locator check and the own hook before an edit lands; the static check and
  the affected tests after it; the green check before a `git commit`, whether Claude Code runs it through `Bash` or
  `PowerShell`.
- **The static check is quiet on a clean file** and short on a broken one: in step 3, `Place Ordr` came back as one
  line, `KeywordNotFound` at line 30, before the affected tests had finished.
- **The own hook has one job, and a reason the agent can act on.** In the new session, asked to tag
  `WEB-006_AC-7 Successful Order` as `broken`, the agent was refused, and offered to fix the test or report the
  defect instead.
- **It counts only what an edit adds.** It compares the file before and after the edit, so the two tests that are
  broken on purpose do not block other edits to their files.
- **It is built on `hookio`,** so the same script answers Codex and Copilot too, and it runs as a plain command over
  `tests/`.
- **The commands use `$CLAUDE_PROJECT_DIR`,** so they work from any working directory.
- **The test now calls a keyword,** and `hooks/no_inline_locators.py tests/` reports nothing. The rehearsal's agent
  rewrote the locator as `a:has-text("Reset")`. Moving `role=link[name="Reset"]` unchanged would have been just as
  good: both use the link's visible text.

## What to debrief

- **Your own hook.** What did it catch, what did it let through, and would you keep it? The rehearsal's agent named
  its hook's one false positive itself: an argument whose value is exactly `Skip` or `Pass Execution` is refused too.
  A hook that is sometimes wrong in the safe direction can be fine; one that refuses good work every hour is not.
- **Claude Code guards `.claude/`.** The agent wrote the script and asked before adding its entry to
  `.claude/settings.json`. That approval is the participant's: a hook changes what the agent may do.
- **The planted defects under `buggy`,** which three failing tests point at:
  - products 5 and 10 have no "Add to cart" button;
  - products 3, 6, 9 and 12 show 1.15 times their price;
  - the displayed order total omits tax.

  A fourth, broken card links on products 4, 8 and 12, is checked by no shipped test. Participants who automated
  WEB-003 in Lab 5 find it with their own test.
- **The issue.** The rehearsal drafted one for the order total, found through `WEB-006_AC-1 Order Total Adds Up`:
  steps, the expected total from `openspec/specs/shop/checkout`, the actual summary, and the evidence from the run's
  log and the page.

## Compare yours

```bash
git fetch upstream solutions
REF=$(git log -1 --format=%H --grep '^lab-07-hooks-toolbelt' upstream/solutions)
git diff "$REF" -- .claude/settings.json hooks/ tests/ui/catalogue.robot resources/catalogue.resource
```

The lines marked `-` are the reference's, the lines marked `+` yours. No `upstream` remote yet? [Add it first](README.md#compare-your-files-with-the-reference).
