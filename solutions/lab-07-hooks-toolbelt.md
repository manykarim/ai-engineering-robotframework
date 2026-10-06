# Lab 7 - Hooks and the toolbelt: the reference

[Lab 7](../labs/lab-07-hooks-toolbelt/INSTRUCTIONS.md) wires three hooks into your agent, moves the suite's one
inline locator into a keyword, and has your agent draft an issue for a defect it finds under `buggy`.
[Transcript](../transcripts/lab-07-hooks-toolbelt.md).

## The reference

The hook wiring for Claude Code, merged into `.claude/settings.json` beside the plugin of Lab 4. For Codex and
GitHub Copilot, `hooks/README.md` names the file each needs.

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
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "uv run --no-sync --project \"$CLAUDE_PROJECT_DIR\" python \"$CLAUDE_PROJECT_DIR/hooks/no_inline_locators.py\""
          }
        ]
      },
      {
        "matcher": "Bash",
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
        "matcher": "Write|Edit|MultiEdit",
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

The inline locator, moved into a keyword:

```diff
--- a/resources/catalogue.resource
+++ b/resources/catalogue.resource
@@ -63,6 +63,11 @@ Apply Filters
     Click    ${FILTERS} >> role=button[name="Apply filters"]
     Wait For Elements State    ${GRID}    visible
 
+Reset Filters
+    [Documentation]    Follows the filter sidebar's "Reset" link.
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

- **Each hook runs at its moment:** the locator check before an edit lands, the affected tests after it, the green
  check before a `git commit`.
- **The commands use `$CLAUDE_PROJECT_DIR`,** so they work from any working directory.
- **The test now calls a keyword,** and `hooks/no_inline_locators.py tests/` reports nothing. The rehearsal's agent
  rewrote the locator as `a:has-text("Reset")`. Moving `role=link[name="Reset"]` unchanged would have been just as
  good: both use the link's visible text.

## What to debrief

- **The planted defects under `buggy`,** which three failing tests point at:
  - products 5 and 10 have no "Add to cart" button;
  - products 3, 6, 9 and 12 show 1.15 times their price;
  - the displayed order total omits tax.

  A fourth, broken card links on products 4, 8 and 12, is checked by no shipped test. Participants who automated
  WEB-003 in Lab 5 find it with their own test.
- **The issue.** The rehearsal drafted one for the missing buttons, found through `WEB-002_AC-1 Every Card Offers Add
  To Cart`: steps, expected, actual, and the evidence from the run's log.

## Compare yours

```bash
git fetch upstream solutions
REF=$(git log -1 --format=%H --grep '^lab-07-hooks-toolbelt' upstream/solutions)
git diff "$REF" -- .claude/settings.json tests/ui/catalogue.robot resources/catalogue.resource
```

The lines marked `-` are the reference's, the lines marked `+` yours. No `upstream` remote yet? [Add it first](README.md#compare-your-files-with-the-reference).
