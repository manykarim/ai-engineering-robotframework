# Lab 7 - Hooks and the toolbelt: the recorded walkthrough

*Recorded with Claude Code 2.1.296, from the lab's instructions. Results are shortened; your agent's answers will differ in wording.*

## Step 1 - Read Hooks

*The participant reads `docs/hooks.md`. No agent is involved.*

## Step 2 - Wire the hooks

*Lab 4 recorded the plugin in `.claude/settings.json`, so the hooks section is merged into it.*

**The participant runs** `uv run --no-sync python -c "import json,pathlib; p=pathlib.Path('.claude/settings.json'); s=json.loads(p.read_text()) if p.exists() else {}; s['hooks']=json.loads(pathlib.Path('hooks/claude-code.settings.json').read_text())['hooks']; p.write_text(json.dumps(s, indent=2)+chr(10))" && cat .claude/settings.json`:

```
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
... (45 more lines)
```

## Step 3 - Try them

**Prompt:**

> Do these four steps in order, and after each one report exactly what happened. Do not work around anything that is blocked or rejected; just report it and continue with the next step.
> 1. In tests/ui/checkout.robot, add the line "    Click    css=button.buy" as the last step of the test "WEB-006_AC-7 Successful Order".
> 2. In tests/ui/checkout.robot, in the test "WEB-006_AC-7 Successful Order", change the step "Place Order" to "Place Ordr".
> 3. In tests/api/smoke.robot, in the test "Health Reports Ok", change the expected status value ok to okay.
> 4. Run the shell command: git commit -am "hook check"

*The agent reads `<repo>\tests\ui\checkout.robot`*

*The agent reads `<repo>\tests\api\smoke.robot`*

**Agent:**

Step 1:

*The agent edits `<repo>\tests\ui\checkout.robot`*

```
PreToolUse:Edit hook error: [uv run --no-sync --project "$CLAUDE_PROJECT_DIR" python "$CLAUDE_PROJECT_DIR/hooks/no_inline_locators.py"]: Rejected: this edit adds the locator literal 'css=button.buy' t
```

**Agent:**

Step 2:

*The agent edits `<repo>\tests\ui\checkout.robot`*

```
The file <repo>\tests\ui\checkout.robot has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Agent:**

Step 3:

*The agent edits `<repo>\tests\api\smoke.robot`*

```
The file <repo>\tests\api\smoke.robot has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Agent:**

Step 4:

*The agent uses `PowerShell` with `{"command": "git commit -am \"hook check\"", "description": "Commit all tracked changes"}`*

```
PreToolUse:PowerShell hook error: [uv run --no-sync --project "$CLAUDE_PROJECT_DIR" python "$CLAUDE_PROJECT_DIR/hooks/green_before_commit.py"]: Commit blocked: The latest suite run has 1 failed test(s
```

**Agent:**

The hooks blocked steps 1 and 4. Steps 2 and 3 went through, but the tests then flagged each of them as a failure. As you asked, I didn't work around or undo anything.

**1. Add `Click    css=button.buy` to "WEB-006_AC-7 Successful Order": rejected.**
The `no_inline_locators.py` hook refused the edit before it was made, so the file was not changed. It said the edit adds the locator `css=button.buy` to a test file, which breaks convention 2 of `docs/conventions.md` ("Locators live in resources"). The locator belongs in a keyword under `resources/`.

**2. Change `Place Order` to `Place Ordr`: applied, then flagged by two hooks.**
The edit was saved in `tests/ui/checkout.robot:30`. Afterwards:
- `run_affected_tests.py` ran `tests/ui/checkout.robot`: 3 passed, 1 failed. "WEB-006_AC-7 Successful Order" failed with `No keyword with name 'Place Ordr' found. Did you mean: checkout.Place Order`.
- `static_check.py` (`robotcode analyze code`) found 1 error: `tests/ui/checkout.robot:30:5: KeywordNotFound: No keyword with name 'Place Ordr' found.`

**3. Change the expected status from `ok` to `okay` in "Health Reports Ok": applied, then flagged.**
The edit was saved in `tests/api/smoke.robot:14`. Afterwards `run_affected_tests.py` ran `tests/api/smoke.robot`: 1 passed, 1 failed. "Health Reports Ok" failed with `ok != okay`.

**4. `git commit -am "hook check"`: blocked.**
The `green_before_commit.py` hook stopped the command before it ran, so nothing was committed. Its message was: `Commit blocked: The latest suite run has 1 failed test(s): Health Reports Ok. Fix them before you commit.` It named only the smoke test, probably because that was the most recent run. The checkout failure from step 2 is still there too.

The working tree still holds both broken edits, plus your earlier change to `.claude/settings.json`. To get back to green, revert steps 2 and 3.

**The participant runs** `git checkout -- tests/ui/checkout.robot tests/api/smoke.robot && git status --short`:

```
M .claude/settings.json
```

## Step 4 - Write a hook of your own

**Prompt:**

> Read docs/hooks.md and hooks/hookio.py. Write a hook in hooks/, on top of hookio.py and in the style of the hooks next to it, that does this: No shortcut to green: refuse an edit that adds the `broken` tag, `Skip`, `Run Keyword And Ignore Error` or `Pass Execution` to a test. It must also run as a plain command. Wire it into this agent's own hook file, next to the hooks already there. Test it with a JSON input like the one this agent sends, once with an action it should let through and once with one it should catch, and show me both results.

*The agent reads `<repo>\docs\hooks.md`*

*The agent reads `<repo>\hooks\hookio.py`*

*The agent searches for `hooks/**`*

```
hooks\claude-code.settings.json
hooks\README.md
hooks\codex.hooks.json
hooks\copilot.hooks.json
hooks\green_before_commit.py
hooks\hookio.py
hooks\no_inline_locators.py
hooks\run_affected_tests.py
hooks\static_check.py
hooks\__pycache__\hookio.cpython-312.pyc
```

*The agent reads `<repo>\.claude\settings.json`*

**Agent:**

Let me look at the neighbouring hooks for style.

*The agent reads `<repo>\hooks\no_inline_locators.py`*

*The agent reads `<repo>\hooks\green_before_commit.py`*

*The agent reads `<repo>\hooks\README.md`*

*The agent searches for `(?i)broken|skip|ignore error|pass execution`*

```
docs\conventions.md:74:| `broken` | the two tests that are broken on purpose, and no other |
docs\hooks.md:80:through and says so: a broken guardrail must not stop the agent.
docs\hooks.md:203:| Static check | `uv run robotcode analyze code <file>` | about 2 s | nothing | unknown keywords and variables, wrong arguments, broken imports |
docs\hooks.md:257:| No shortcut to green: refuse an edit that adds the `broken` tag, `Skip`, `Run Keyword And Ignore Error` or `Pass Execution` to a test | before an edit | refuse | an agent that make
docs\hooks.md:272:- **Open when broken.** If it cannot read its input, it lets the action through, as `hookio` does. Copilot refuses
docs\WWWW_Workshop_Master_Preparation.md:83:**Lab:** install the plugin; discovery question; libdoc lookup; step-debug a pre-broken test; REPL-explore a new flow with visible browser. Stretch: results
docs\WWWW_Workshop_Master_Preparation.md:89:**Lab:** one of three user stories to green; pair-review in breakouts (like a junior engineer's PR); debug one pre-broken test purely through conversation. 
docs\WWWW_Workshop_Master_Preparation.md:174:│   ├── ui/                    #   incl. the pre-broken tests (marked by tag: broken)
docs\WWWW_Workshop_Master_Preparation.md:244:- [ ] Build/adapt demo shop; plant the broken tests and the bugs for Lab 7; verify `drift.py` produces *healable* drift (relabels) and *unhealable* drift (
```

*The agent reads `<repo>\docs\conventions.md`*

*The agent writes `<repo>\hooks\no_shortcut_to_green.py`*

```
File created successfully at: <repo>\hooks\no_shortcut_to_green.py (file state is current in your context — no need to Read it back)
```

*The agent edits `<repo>\.claude\settings.json`*

```
Claude requested permissions to write to <repo>\.claude\settings.json, but you haven't granted it yet.
```

**Agent:**

The settings edit wasn't approved, so I'll carry on with the tests and come back to the wiring at the end. First I need a real test file to build the inputs from.

*The agent searches for `Place Order|broken`*

```
tests\ui\checkout.robot:30:    Place Order
tests\ui\checkout.robot:43:    Place Order
tests\ui\checkout.robot:53:    Place Order
```

*The agent reads `<repo>\tests\ui\checkout.robot`*

**Agent:**

Now the three checks: a plain run, an Edit that should pass, and an Edit that should be refused, each as Claude Code sends it.

*The agent runs `cd <repo>
echo "=== plain command over tests/ ==="
uv run --no-sync python hooks/no_shortcut_to_green.py tests/; echo "exit $?"

echo; echo "=== let through: Edit adds a real assertion ==="
cat > /tmp/allow.json <<'EOF'
{"session_id":"t","transcript_path":"x","cwd":"<repo>","permission_mode":"default","hook_event_name":"PreToolUse","tool_name":"Edit","tool_input":{"file_path":"<repo>\\tests\\ui\\checkout.robot","old_string":"    Length Should Be    ${numbers}    1\n","new_string":"    Length Should Be    ${numbers}    1\n    Should Start With    ${numbers}[0]    ORD-\n","replace_all":false}}
EOF
uv run --no-sync python hooks/no_shortcut_to_green.py < /tmp/allow.json; echo "exit $?"

echo; echo "=== catch: Edit wraps Place Order in Run Keyword And Ignore Error and tags the test broken ==="
cat > /tmp/deny.json <<'EOF'
{"session_id":"t","transcript_path":"x","cwd":"<repo>","permission_mode":"default","hook_event_name":"PreToolUse","tool_name":"Edit","tool_input":{"file_path":"<repo>\\tests\\ui\\checkout.robot","old_string":"    Fill Checkout Form By Field Ids    test@example.com    Test User    123 Test Street, City\n    Place Order\n","new_string":"    [Tags]    broken\n    Fill Checkout Form By Field Ids    test@example.com    Test User    123 Test Street, City\n    Run Keyword And Ignore Error    Place Order\n","replace_all":false}}
EOF
uv run --no-sync python hooks/no_shortcut_to_green.py < /tmp/deny.json; echo "exit $?"`*

```
Contains brace with quote character (expansion obfuscation)
```

**Agent:**

The shell refused the heredoc, so I'll write the two inputs as files and pipe them in.

*The agent writes `~\AppData\Local\Temp\hooktest\allow.json`*

```
Claude requested permissions to write to ~\AppData\Local\Temp\hooktest\allow.json, but you haven't granted it yet.
```

*The agent writes `~\AppData\Local\Temp\hooktest\deny.json`*

```
Claude requested permissions to write to ~\AppData\Local\Temp\hooktest\deny.json, but you haven't granted it yet.
```

**Agent:**

Writing outside the repo isn't allowed either, so I'll pipe the JSON straight from PowerShell instead.

*The agent uses `PowerShell` with `{"command": "'=== plain command over tests/ ==='\nuv run --no-sync python hooks/no_shortcut_to_green.py tests/; \"exit $LASTEXITCODE\"\n''\n'=== let through: Ed`*

```
Command contains a UNC path that could trigger network requests
```

**Agent:**

The `\\` in the paths looked like a UNC path to the guard, so I'll switch the paths to forward slashes.

*The agent uses `PowerShell` with `{"command": "'=== plain command over tests/ ==='\nuv run --no-sync python hooks/no_shortcut_to_green.py tests/; \"exit $LASTEXITCODE\"\n''\n'=== let through: Ed`*

```
Command contains malformed syntax that cannot be parsed: pwsh exited with code 1: Die Befehlszeile ist zu lang.
```

**Agent:**

That was too long for one call, so I'll split it into three.

*The agent uses `PowerShell` with `{"command": "uv run --no-sync python hooks/no_shortcut_to_green.py tests/; \"exit $LASTEXITCODE\"", "description": "Run the hook as a plain command over tests/"`*

```
Command contains malformed syntax that cannot be parsed: pwsh exited with code 1: Die Befehlszeile ist zu lang.
```

**Agent:**

The PowerShell tool fails even on a one-line command ("Die Befehlszeile ist zu lang"), so this is a tool problem, not the command. I'll use Bash and keep the JSON free of `${`.

*The agent runs `uv run --no-sync python hooks/no_shortcut_to_green.py tests/; echo "exit $?"`*

```
exit 0
```

*The agent runs `echo '{"session_id":"t","transcript_path":"x","cwd":"<repo>","permission_mode":"default","hook_event_name":"PreToolUse","tool_name":"Edit","tool_input":{"file_path":"<repo>/tests/ui/checkout.robot","old_string":"    Go To Cart Page\n","new_string":"    Go To Cart Page\n    Cart Should Say It Is Empty\n","replace_all":false}}' | uv run --no-sync python hooks/no_shortcut_to_green.py; echo "exit $?"`*

```
exit 0
```

*The agent runs `echo '{"session_id":"t","transcript_path":"x","cwd":"<repo>","permission_mode":"default","hook_event_name":"PreToolUse","tool_name":"Edit","tool_input":{"file_path":"<repo>/tests/ui/checkout.robot","old_string":"    Get Order Confirmation\n    Go To Cart Page\n","new_string":"    Run Keyword And Ignore Error    Get Order Confirmation\n    Go To Cart Page\n","replace_all":false}}' | uv run --no-sync python hooks/no_shortcut_to_green.py; echo "exit $?"`*

```
Rejected: this edit adds Run Keyword And Ignore Error to tests/ui/checkout.robot, a shortcut to green. Make the test right instead: fix the keyword or the locator, or, when the shop does not do what o
exit 2
```

*The agent runs `echo '{"session_id":"t","transcript_path":"x","cwd":"<repo>","permission_mode":"default","hook_event_name":"PreToolUse","tool_name":"Edit","tool_input":{"file_path":"<repo>/tests/ui/checkout.robot","old_string":"Test Tags           WEB-006    ui\n","new_string":"Test Tags           WEB-006    ui    BROKEN\n","replace_all":false}}' | uv run --no-sync python hooks/no_shortcut_to_green.py; echo "exit $?"; echo '{"session_id":"t","transcript_path":"x","cwd":"<repo>","permission_mode":"default","hook_event_name":"PreToolUse","tool_name":"Edit","tool_input":{"file_path":"<repo>/tests/ui/checkout.robot","old_string":"    Go To Cart Page\n","new_string":"    BuiltIn.Skip If    True    flaky\n    pass_execution    done\n    Go To Cart Page\n","replace_all":false}}' | uv run --no-sync python hooks/no_shortcut_to_green.py; echo "exit $?"`*

```
Rejected: this edit adds the `broken` tag to tests/ui/checkout.robot, a shortcut to green. Make the test right instead: fix the keyword or the locator, or, when the shop does not do what openspec/spec
exit 2
Rejected: this edit adds Skip If, Pass Execution to tests/ui/checkout.robot, a shortcut to green. Make the test right instead: fix the keyword or the locator, or, when the shop does not do what opensp
exit 2
```

**Agent:**

I wrote the hook at `hooks/no_shortcut_to_green.py` and tested it. It works as a plain command and with Claude Code's JSON input. **It is not wired in yet:** my edit to `.claude/settings.json` was declined.

## The hook

It's built the same way as `no_inline_locators.py`:
- **Which files:** it only looks at `.robot` files under `tests/`.
- **Only what's new counts:** it compares the file before and after the edit, so anything already in the file doesn't block other edits to it. That matters for the two tests convention 7 says are broken on purpose.
- **What it catches:** `broken` in `[Tags]`, `Test Tags`, `Force Tags`, `Default Tags` or `Set Tags`. It also catches `Skip`, `Skip If`, `Pass Execution`, `Pass Execution If` and `Run Keyword And Ignore Error` used as a step, a setup or teardown, or an argument to another keyword. It matches names the way Robot Framework does: case, spaces and underscores don't matter, and a `BuiltIn.` prefix is fine. Documentation text and comments are ignored.
- **How it refuses:** through `hookio.deny()`, so the same script would work for Codex and Copilot too. The message tells the agent what to do instead: fix the test, or leave it failing and report it when the shop doesn't match the spec.
- **As a command:** `uv run --no-sync python hooks/no_shortcut_to_green.py tests/` lists every occurrence and exits with 1 if it finds any. It ran clean over `tests/` (exit 0).

## The two test runs

Both inputs are a Claude Code `PreToolUse` / `Edit` call on `tests/ui/checkout.robot`, piped to the script.

**Let through:** the edit adds `Cart Should Say It Is Empty` after `Go To Cart Page`.
```
exit 0
```

**Caught:** the edit turns `Get Order Confirmation` into `Run Keyword And Ignore Error    Get Order Confirmation`.
```
Rejected: this edit adds Run Keyword And Ignore Error to tests/ui/checkout.robot, a shortcut to green. Make the test right instead: fix the keyword or the locator, or, when the shop does not do what openspec/specs/shop/ says, leave the test failing and report it. The `broken` tag belongs to the two tests that are broken on purpose, and no other (convention 7 of docs/conventions.md).
exit 2
```

I also checked other spellings. `Test Tags ... BROKEN` was refused, and so were `BuiltIn.Skip If` and `pass_execution` (both named in the message). The file was never changed, because the hook only reads the proposed edit.

## Wiring it in

To add it, put this entry in `.claude/settings.json` under `hooks.PreToolUse`, next to the `no_inline_locators.py` entry:

```json
{
  "matcher": "Write|Edit",
  "hooks": [
    {
      "type": "command",
      "command": "uv run --no-sync --project \"$CLAUDE_PROJECT_DIR\" python \"$CLAUDE_PROJECT_DIR/hooks/no_shortcut_to_green.py\""
    }
  ]
}
```

Approve the edit and I'll make it, or paste it in yourself. Then start a new session and check `/hooks` to confirm it's active.

There is one known false positive: a cell whose value is exactly `Skip` or `Pass Execution`, used as plain text in an argument, would also be refused.

*Claude Code asks before it writes into `.claude/`, and a headless session cannot ask. The participant approves: the rehearsal added the entry the agent proposed to `.claude/settings.json`, unchanged, next to `no_inline_locators.py`.*

*A new session, so that the changed hooks are loaded.*

**Prompt:**

> In tests/ui/checkout.robot, tag the test "WEB-006_AC-7 Successful Order" as broken.

*The agent reads `<repo>\docs\conventions.md`*

*The agent reads `<repo>\tests\ui\checkout.robot`*

*The agent searches for `broken`*

```
<persisted-output>
Output too large (40.4KB). Full output saved to: ~\.claude\projects\<project>\045e819f-0fb5-48c8-bf8f-f6593fb7ee14\tool-results\toolu_01GUxS4i6RjhpZRd53ko4Jrm.txt

Preview (first 2KB):
.claude\skills\openspec-archive-change\SKILL.md:17:[Omitted long matching line]
.claude\skills\openspec-apply-change\SKILL.md:17:[Omitted long matching line]
.claude\commands\opsx\update.md:13:[Omitted long matching line]
.claude\commands\opsx\sync.md:15:[Omitted long matching line]
.claude\commands\opsx\propose.md:27:[Omitted long matching line]
.claude\commands\opsx\explore.md:17:[Omitted long matching line]
.claude\commands\opsx\archive.md:13:[Omitted long matching line]
.claude\commands\opsx\apply.md:13:[Omitted long matching line]
... (17 more lines)
```

*The agent reads `<repo>\hooks\no_shortcut_to_green.py`*

*The agent searches for `(?i)broken`*

```
No matches found
```

*The agent searches for `(?i)broken on purpose|`broken``*

```
openspec\specs\workshop\ci\spec.md-6-## Requirements
openspec\specs\workshop\ci\spec.md-7-
openspec\specs\workshop\ci\spec.md-8-### Requirement: The suite runs on every push and pull request
openspec\specs\workshop\ci\spec.md:9:A workflow SHALL run the suite on every push and every pull request, against the shop started from the image `shop/compose.yaml` pins, and SHALL upload the run's r
openspec\specs\workshop\ci\spec.md-10-
openspec\specs\workshop\ci\spec.md-11-#### Scenario: A fresh fork
openspec\specs\workshop\ci\spec.md-12-- **WHEN** a participant enables Actions on a fork of `main` and pushes a commit that changes nothing in `tests/` or `resources/`
--
openspec\specs\workshop\facilitation\spec.md-71-- how an agent drives the REPL and the debugger without waiting at a prompt;
openspec\specs\workshop\facilitation\spec.md-72-- the traps of the pinned versions a participant can meet in the labs.
openspec\specs\workshop\facilitation\spec.md-73-
openspec\specs\workshop\facilitation\spec.md:74:It SHALL be linked from Lab 4 and from the glossary's RobotCode entry, and published on the documentation site. It SHALL NOT name a planted defect, the 
... (105 more lines)
```

*The agent edits `<repo>\tests\ui\checkout.robot`*

```
PreToolUse:Edit hook error: [uv run --no-sync --project "$CLAUDE_PROJECT_DIR" python "$CLAUDE_PROJECT_DIR/hooks/no_shortcut_to_green.py"]: Rejected: this edit adds the `broken` tag to tests/ui/checkou
```

**Agent:**

I didn't tag the test. The `no_shortcut_to_green.py` hook blocked the edit, so `tests/ui/checkout.robot` is unchanged.

The hook is enforcing a rule the repo already has. Convention 7 in `docs/conventions.md` (and `openspec/specs/workshop/test-conventions/spec.md`) says only the two tests that are broken on purpose get the `broken` tag, and "WEB-006_AC-7 Successful Order" isn't one of them. Tagging it would also drop it from CI, which runs with `--exclude broken`, so any real failure would stop showing up.

I haven't tried to get around the hook. If the test is failing, the repo gives two ways forward:

- **Fix the test.** It fills the form with `Fill Checkout Form By Field Ids`, which finds fields by element id. That's fragile, and convention 3 says to avoid it. Switching to `Fill Checkout Form`, which the other checkout tests use and which finds fields by label inside the form, may be all it needs. I can do that and run the test.
- **Leave it failing and report it**, if the shop doesn't do what `openspec/specs/shop/` says, for example the order number isn't `ORD-` plus 8 hex characters.

If you still want the tag (say, to see the hook in action for the lab), you'd need to make that edit yourself or turn the hook off in `.claude/settings.json`.

**The participant runs** `git status --short`:

```
M .claude/settings.json
?? hooks/no_shortcut_to_green.py
```

## Step 5 - Let the hook check the whole suite

**The participant runs** `uv run --no-sync python hooks/no_inline_locators.py tests/; echo "exit $?"`:

```
tests\ui\catalogue.robot:68: locator literal 'role=link[name="Reset"]' in a test file
exit 1
```

**Prompt:**

> uv run --no-sync python hooks/no_inline_locators.py tests/ reports a locator literal in a test file. Move it into a keyword under resources/, following docs/conventions.md, and run the affected test.

*The agent uses `PowerShell` with `{"command": "uv run --no-sync python hooks/no_inline_locators.py tests/", "description": "Run inline locator checker on tests"}`*

```
Command contains malformed syntax that cannot be parsed: pwsh exited with code 1: Die Befehlszeile ist zu lang.
```

*The agent reads `<repo>\docs\conventions.md`*

*The agent reads `<repo>\docs\agent-environment.md`*

*The agent runs `uv run --no-sync python hooks/no_inline_locators.py tests/`*

```
Exit code 1
tests\ui\catalogue.robot:68: locator literal 'role=link[name="Reset"]' in a test file
```

*The agent reads `<repo>\tests\ui\catalogue.robot`*

*The agent searches for `Reset|Filter|^\S`*

```
resources\api.resource:1:*** Settings ***
resources\api.resource:2:Documentation       The shop's API, in the configured workshop space.
resources\api.resource:4:Library             Collections
resources\api.resource:5:Library             RequestsLibrary
resources\api.resource:8:*** Keywords ***
resources\api.resource:9:Open Shop API
resources\api.resource:17:Get Shop Health
resources\api.resource:22:Get Catalogue From API
resources\api.resource:27:Get Product From API
resources\checkout.resource:1:*** Settings ***
resources\checkout.resource:2:Documentation       The cart and checkout pages through the shop's stable contract.
resources\checkout.resource:3:...                 Form fields are always scoped to the checkout form: the sign-in dialog
... (190 more lines)
```

*The agent reads `<repo>\resources\catalogue.resource`*

*The agent searches for `AC-10`*

```
openspec\specs\shop\checkout\spec.md:76:### Requirement: Empty cart at checkout (WEB-006_AC-10)
openspec\specs\shop\checkout\spec.md-77-When a shopper with no items in the cart submits the checkout form, the error message "Your cart is empty" SHALL be displayed and no order SHALL be created.
openspec\specs\shop\checkout\spec.md-78-
openspec\specs\shop\checkout\spec.md-79-#### Scenario: Submitting without items
openspec\specs\shop\checkout\spec.md-80-- **WHEN** a shopper with an empty cart submits the checkout form with valid data
openspec\specs\shop\checkout\spec.md-81-- **THEN** "Your cart is empty" is displayed and no order is created
openspec\specs\shop\checkout\spec.md-82-
openspec\specs\shop\checkout\spec.md-83-### Requirement: Validation errors next to the fields (WEB-006_AC-11)
openspec\specs\shop\checkout\spec.md-84-When the shopper submits the checkout form with one or more invalid fields, an error message SHALL be displayed next to each invalid field, the form SHALL NOT b
--
openspec\specs\shop\cart\spec.md:9:When a shopper clicks the "Add to Cart" button on a product card on any page - the home page, the products page or a detail page - a POST request SHALL be sent to `/
openspec\specs\shop\cart\spec.md-10-
... (44 more lines)
```

*The agent loads the skill `locators-in-resources`*

**Agent:**

The checker flags `Click    role=link[name="Reset"]` at `tests/ui/catalogue.robot:68`. I'm moving it into a `Reset Filters` keyword in `resources/catalogue.resource`.

*The agent edits `<repo>\resources\catalogue.resource`*

*The agent edits `<repo>\tests\ui\catalogue.robot`*

```
The file <repo>\resources\catalogue.resource has been updated successfully.
```

```
The file <repo>\tests\ui\catalogue.robot has been updated successfully. (file state is current in your context — no need to Read it back)
```

*The agent runs `uv run --no-sync python hooks/no_inline_locators.py tests/; echo "hook=$?"; uv run --no-sync python .claude/skills/locators-in-resources/scripts/check.py tests/; echo "skill=$?"; uv run robotcode robot -t "WEB-002_AC-10 Reset Filters" 2>&1 | tail -20`*

```
hook=0
skill=0
Tests                                                                         
==============================================================================
Tests.Ui                                                                      
==============================================================================
Tests.Ui.Catalogue :: The products page, /products (spec: shop/catalogue).    
==============================================================================
WEB-002_AC-10 Reset Filters :: "Reset" clears every filter and bri... | PASS |
------------------------------------------------------------------------------
Tests.Ui.Catalogue :: The products page, /products (spec: shop/cat... | PASS |
1 test, 1 passed, 0 failed
... (10 more lines)
```

**Agent:**

I moved the locator out of the test, and the affected test now passes.

**The finding:** `tests/ui/catalogue.robot:68` had `Click    role=link[name="Reset"]` written directly in test `WEB-002_AC-10 Reset Filters`.

**The fix:**
- **`resources/catalogue.resource`:** I added a `Reset Filters` keyword. It clicks `${FILTERS} >> a:has-text("Reset")` and then waits for the product grid, the same way `Apply Filters` does.
- **The locator itself:** I changed it from matching the accessible name to matching visible text. Convention 4 says quoted UI text, here the spec's "Reset" link, should be matched by what's shown on screen. I also limited it to the filter sidebar, like the other filter keywords.
- **The test:** it now just calls `Reset Filters`.

**Checks:**
- `hooks/no_inline_locators.py tests/` and the skill's `check.py tests/` both find nothing now.
- `uv run robotcode robot -t "WEB-002_AC-10 Reset Filters"` passed (1 test, 1 passed).

The checker wouldn't run from the PowerShell tool (it failed with "command line too long"), so I ran everything through the Bash tool instead.

**The participant runs** `uv run --no-sync python hooks/no_inline_locators.py tests/; echo "exit $?"`:

```
exit 0
```

## Step 6 - Switch the shop

**The participant runs** `uv run --no-sync python -m shop preset buggy`:

```
applied preset buggy in space default
```

## Step 7 - Run the suite

**The participant runs** `uv run robotcode robot --exclude broken 2>&1 | tail -25`:

```
==============================================================================
WEB-004_AC-1 Home Page Hero Shows Search Input :: The first screen... | PASS |
------------------------------------------------------------------------------
WEB-004_AC-3 Enter Shows Matching Results :: Searching "headphones... | PASS |
------------------------------------------------------------------------------
WEB-004_AC-3 Search Button Shows Matching Results :: Searching "he... | PASS |
------------------------------------------------------------------------------
WEB-004_AC-6 Clear Results On Home Page :: On /, clearing the resu... | PASS |
------------------------------------------------------------------------------
WEB-004_AC-6 Clear Search On Products Page :: On /products, cleari... | PASS |
------------------------------------------------------------------------------
WEB-004_AC-7 Unmatched Query Shows Empty State :: Searching "xyz12... | PASS |
... (13 more lines)
```

## Step 8 - Draft an issue

**Prompt:**

> Look at the failed tests of the last run with robotcode results. Pick one failure that is a defect of the shop, not of the test. Write the steps a person would follow in the browser to see it, the expected behaviour according to openspec/specs/shop, the actual behaviour, and the evidence from the run. Save it as results/issue.md with the title as its first line. Do not file it.

*The agent reads `<repo>\docs\agent-environment.md`*

*The agent loads the skill `rf-robotcode`*

*The agent uses `PowerShell` with `{"command": "uv run robotcode --format json results summary --failed", "description": "Summarise failed tests of last run"}`*

```
Command contains malformed syntax that cannot be parsed: pwsh exited with code 1: Die Befehlszeile ist zu lang.
```

*The agent runs `uv run robotcode results summary --failed 2>&1 | head -100`*

```
# Summary — results/output.xml

- _Status:_ ❌ **FAIL**
- _Total:_ 30
- _Passed:_ 27
- _Failed:_ 3
- _Skipped:_ 0
- _Started:_ 2026-11-02 21:46:46
- _Ended:_ 2026-11-02 21:47:44
- _Elapsed:_ 57.29 s
- _Messages:_ 3 FAIL

... (8 more lines)
```

*The agent runs `git diff -- tests resources; cat tests/ui/catalogue.robot tests/ui/checkout.robot; uv run robotcode results log --failed 2>&1 | head -200`*

```
diff --git a/resources/catalogue.resource b/resources/catalogue.resource
index 6a09c9a..2784caf 100644
--- a/resources/catalogue.resource
+++ b/resources/catalogue.resource
@@ -63,6 +63,11 @@ Apply Filters
     Click    ${FILTERS} >> role=button[name="Apply filters"]
     Wait For Elements State    ${GRID}    visible
 
+Reset Filters
+    [Documentation]    Clicks the "Reset" link, found by its visible text.
+    Click    ${FILTERS} >> a:has-text("Reset")
+    Wait For Elements State    ${GRID}    visible
... (370 more lines)
```

*The agent runs `uv run robotcode results log --failed 2>&1 | sed -n '200,600p' | grep -v "Collections.Append\|^\s*- \*\*ITER" `*

```
- `@{shown}` = **legacy.Get Card Prices** ✅ **PASS** _(21:47:02 · 92 ms)_
  - `${grid}` = **legacy.Get Product Grid** ✅ **PASS** _(21:47:02 · 6 ms)_
    - `${grid}` = **Browser.Get Element** `${GRID} >> .product-grid` ✅ **PASS** _(21:47:02 · 6 ms)_
      - `[INFO] Locator found successfully.`
      - `[INFO] ${grid} = section:has(h2:text-is("All products")):not(:has(section)) >> .product-grid`
    - **RETURN** `${grid}` ✅ **PASS** _(21:47:02 · 0 ms)_
    - `[INFO] ${grid} = section:has(h2:text-is("All products")):not(:has(section)) >> .product-grid`
  - `@{prices}` = **catalogue.Get Texts** `${grid} >> article >> ${CARD PRICE}` ✅ **PASS** _(21:47:02 · 87 ms)_
    - `@{elements}` = **Browser.Get Elements** `${locator}` ✅ **PASS** _(21:47:02 · 0 ms)_
      - `[INFO] Found 12 Locators successfully.`
      - `[INFO] @{elements} = [ section:has(h2:text-is("All products")):not(:has(section)) >> .product-grid >> article >> text=/^\$[0-9,]+\.[0-9]{2}$/ >> nth=0 | section:has(h2:text-is("All products")
    - `@{texts}` = **BuiltIn.Create List** ✅ **PASS** _(21:47:02 · 0 ms)_
... (194 more lines)
```

**Agent:**

Three failures found; now checking each against the spec to decide which is a shop defect.

*The agent runs `ls openspec/specs/shop/; grep -rn -i "AC-1\b\|AC-1:\|AC-1 \|price\|add to cart\|total" openspec/specs/shop/catalogue/spec.md openspec/specs/shop/checkout/spec.md | head -60`*

```
authentication
cart
catalogue
checkout
interpretation-rules
product-detail
search
openspec/specs/shop/catalogue/spec.md:8:### Requirement: Full product grid (WEB-002_AC-1)
openspec/specs/shop/catalogue/spec.md:9:When a shopper opens `/products` and the page finishes loading, the page SHALL display all 12 seeded products in a grid. Each product card SHALL show the produc
openspec/specs/shop/catalogue/spec.md:13:- **THEN** 12 product cards are displayed, and each shows the product's name, image and price and an "Add to Cart" button
openspec/specs/shop/catalogue/spec.md:22:### Requirement: Price range filter (WEB-002_AC-3)
openspec/specs/shop/catalogue/spec.md:23:The products page SHALL display a "Price range" filter with a dual slider that has a minimum and a maximum handle. Its minimum SHALL be the lowest product pric
... (18 more lines)
```

*The agent runs `curl -s http://localhost:9090/products | grep -n -i -A25 "Cascade Water Bottle" | head -80`*

```
This Bash command contains multiple operations. The following part requires approval: curl -s http://localhost:9090/products
```

*The agent runs `cat resources/legacy.resource; grep -n "Add To Cart\|CARD\|^\${GRID\|SUMMARY\|TOTAL" resources/*.resource`*

```
*** Settings ***
Documentation       Legacy locators, kept deliberately; see docs/conventions.md.
...
...                 These keywords find elements by id, class or data-test hook instead of
...                 the shop's stable contract. Each such locator names exactly one element.

Library             Browser
Resource            catalogue.resource
Resource            checkout.resource


*** Keywords ***
... (44 more lines)
```

**Agent:**

I'll look at the live shop in a headless browser (read-only) to separate test faults from shop faults.

*The agent runs `mkdir -p results/repl /tmp/rfi && cat > /tmp/rfi/inspect.robotrepl <<'EOF'
New Browser    chromium    headless=True
New Context    baseURL=http://localhost:9090
New Page    http://localhost:9090/products
${cards}=    Get Elements    section:has(h2:text-is("All products")):not(:has(section)) >> article
FOR    ${c}    IN    @{cards}
    ${t}=    Get Property    ${c}    innerText
    Log To Console    ---\n${t}
END
${h}=    Get Property    section:has(h2:text-is("All products")):not(:has(section)) >> article:has-text("Cascade Water Bottle")    outerHTML
Log To Console    ${h}
Go To    http://localhost:9090/products/1
Click    role=button[name="Add Aurora Neural Headphones to cart"]
Sleep    1s
Go To    http://localhost:9090/checkout
${s}=    Get Property    role=complementary    outerHTML
Log To Console    ${s}
.exit
EOF
uv run robotcode repl --plain --no-history -d results/repl < /tmp/rfi/inspect.robotrepl 2>&1 | tail -150`*

```
Parser skipped input between top-level statements
```

*The agent writes `<repo>\results\repl\inspect.robotrepl`*

```
File created successfully at: <repo>\results\repl\inspect.robotrepl (file state is current in your context — no need to Read it back)
```

*The agent runs `uv run robotcode repl --plain --no-history -d results/repl < results/repl/inspect.robotrepl 2>&1 | tail -200`*

```
[ FAIL ] No keyword with name 'New Browser' found.
[ FAIL ] No keyword with name 'New Context' found.
[ FAIL ] No keyword with name 'New Page' found.
[ FAIL ] No keyword with name 'Get Property' found.
[ FAIL ] Variable '${g}' not found.
[ FAIL ] No keyword with name 'Get Property' found.
[ FAIL ] Variable '${h}' not found.
[ FAIL ] No keyword with name 'Get Property' found.
[ FAIL ] Variable '${h2}' not found.
[ FAIL ] No keyword with name 'Go To' found.
[ FAIL ] No keyword with name 'Click' found.
[ INFO ] Slept 1 second.
... (3 more lines)
```

*The agent edits `<repo>\results\repl\inspect.robotrepl`*

```
The file <repo>\results\repl\inspect.robotrepl has been updated successfully. (file state is current in your context — no need to Read it back)
```

*The agent runs `uv run robotcode repl --plain --no-history -d results/repl < results/repl/inspect.robotrepl 2>&1 | tail -200`*

```
<div class="rating" role="group" aria-label="Rated 4.2 out of 5 stars from 134 reviews">
  <span class="rating__value">4.2</span>
  <span class="rating__stars" aria-hidden="true">
    
    <svg viewBox="0 0 24 24">
      <path d="M12 2.2 14.9 8l6.4.5-4.9 4.2 1.5 6.3L12 15.8 6.1 19l1.5-6.3-4.9-4.2L9.1 8 12 2.2Z"></path>
    </svg>
    
    <svg viewBox="0 0 24 24">
      <path d="M12 2.2 14.9 8l6.4.5-4.9 4.2 1.5 6.3L12 15.8 6.1 19l1.5-6.3-4.9-4.2L9.1 8 12 2.2Z"></path>
    </svg>
    
... (188 more lines)
```

*The agent runs `ls openspec/specs/shop/interpretation-rules/ && grep -n -i "tax\|total\|complimentary\|price" openspec/specs/shop/interpretation-rules/spec.md; uv run --no-sync python -m shop status 2>&1 | grep -iv "space"`*

```
spec.md
23:- **WHEN** a requirement quotes "Tax" and the element's visible text is "Estimated tax"
shop     http://localhost:9090  (version 0.3.0)
presets  stage1, buggy
```

*The agent writes `<repo>\results\issue.md`*

```
File created successfully at: <repo>\results\issue.md (file state is current in your context — no need to Read it back)
```

**Agent:**

I wrote the issue to `results/issue.md` and did not file it. Its first line is the title: **"Checkout: order total leaves out the tax ($249.99 shown, $267.49 expected)"**.

**What failed in the last run:** 3 of 30 tests failed. I opened each page in a headless browser to check that the shop was really at fault and not the test:

| Test | What the shop does | Verdict |
|---|---|---|
| `WEB-006_AC-1 Order Total Adds Up` | Shows Subtotal $249.99, Shipping "Complimentary", Tax $17.50, but "Total due at payment" is **$249.99** | Shop defect, **the one I wrote up** |
| `WEB-002_AC-1 Card Prices Are The Product Prices` | The Cascade Water Bottle card shows $90.85 but the API price is $79.00. Pulse Bio Ring, Summit Trail Shoes and Velocity Travel Backpack also show the API price plus 15%. | Shop defect (each card has only one price on it) |
| `WEB-002_AC-1 Every Card Offers Add To Cart` | 10 "Add to cart" buttons on 12 cards. Atlas Standing Desk's button area is empty, and one other card has none either. | Shop defect |

I picked the checkout total because it is the simplest to reproduce and matters most to a shopper: `checkout/spec.md` (WEB-006_AC-1) says the total must be subtotal plus shipping plus tax. The issue has:
- **Steps:** add Aurora Neural Headphones from `/products/1`, then open `/checkout`.
- **Expected:** $267.49, with the spec text quoted.
- **Actual:** the four summary lines as the page shows them.
- **Evidence:** the failure log from `robotcode results log --failed` and the summary panel's HTML. The panel has only one total element, so the test isn't reading the wrong figure.

`shop status` says the presets `stage1, buggy` are active on the shop, which fits these being defects planted on purpose.

To look at the pages I wrote a small script, `results/repl/inspect.robotrepl`. It only reads pages and adds one item to a fresh browser cart. `results/` is ignored by git. I did not touch your uncommitted changes to `catalogue.robot` and `catalogue.resource`.

**The participant runs** `cat results/issue.md`:

```
Checkout: order total leaves out the tax ($249.99 shown, $267.49 expected)

## Environment

- Shop: http://localhost:9090, version 0.3.0 (local instance)
- Browser: Chromium (Playwright, via Robot Framework Browser), viewport 1280x720
- Found by: `tests/ui/checkout.robot` › `WEB-006_AC-1 Order Total Adds Up`, run of 2026-11-02 21:46:46

## Steps to reproduce

1. Open a fresh browser window (empty cart) and go to http://localhost:9090/products/1 (Aurora Neural Headphones).
2. Click "Add to cart". The cart link in the header shows 1.
... (59 more lines)
```

## Step 9 - File it

*Not filed during the rehearsal: it ran in a clone of the workshop's own repository, not in a fork. In your fork:* `gh issue create --repo <your-handle>/ai-engineering-robotframework --title "$(head -1 results/issue.md)" --body-file results/issue.md`

## Step 10 - Put the shop back

**The participant runs** `uv run --no-sync python -m shop reset`:

```
reset space default: removed 5 flag settings, 22 cart items and 5 orders
```

**The participant runs** `uv run robotcode robot --exclude broken 2>&1 | tail -12`:

```
Tests.Ui.Search :: Product search on the home page and the product... | PASS |
6 tests, 6 passed, 0 failed
==============================================================================
Tests.Ui                                                              | PASS |
28 tests, 28 passed, 0 failed
==============================================================================
Tests                                                                 | PASS |
30 tests, 30 passed, 0 failed
==============================================================================
Output:  <repo>\results\output.xml
Log:     <repo>\results\log.html
Report:  <repo>\results\report.html
```

**The participant runs** `uv run --no-sync python hooks/green_before_commit.py --check`:

```
The latest suite run is green and up to date: a commit may go ahead.
```
