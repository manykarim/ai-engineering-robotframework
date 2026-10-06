# Lab 4 - RobotCode: the recorded walkthrough

*Recorded with Claude Code 2.1.281, from the lab's instructions. Results are shortened; your agent's answers will differ in wording.*

## Step 1 - Install the RobotCode plugin

**The participant runs** `claude plugin marketplace add --scope project robotcodedev/robotframework-agent-plugins`:

```
Cloning repository (timeout: 120s): https://github.com/robotcodedev/robotframework-agent-plugins.git
Clone complete, validating marketplace…
Cleaning up old marketplace cache…
✔ Successfully added marketplace: robotframework-agent-plugins (declared in project settings)
```

**The participant runs** `claude plugin install --scope project robotcode@robotframework-agent-plugins`:

```
Installing plugin "robotcode@robotframework-agent-plugins"...✔ Successfully installed plugin: robotcode@robotframework-agent-plugins (scope: project)
```

**The participant runs** `claude plugin list`:

```

  ❯ robotcode@robotframework-agent-plugins
    Version: 7c753f8adca1
    Scope: project
    Status: ✔ enabled

  ❯ rust-analyzer-lsp@claude-plugins-official
    Version: 1.0.0
    Scope: user
    Status: ✔ enabled
```

## Step 2 - Tie it to your context

**The participant runs** `printf '\nUse RobotCode through uv (`uv run robotcode ...`) to discover tests and keywords, read library docs, debug\nfailing tests and read results.\n' >> AGENTS.md && tail -3 AGENTS.md`:

```

Use RobotCode through uv (`uv run robotcode ...`) to discover tests and keywords, read library docs, debug
failing tests and read results.
```

## Step 3 - A discovery question

**Prompt:**

> Which tests of this repository carry the tag ui, and in which files are they? Ask the project; don't grep.

*The agent reads `<repo>/docs/agent-environment.md`*

*The agent loads the skill `robotcode:robotcode`*

*The agent runs `uv run --no-sync robotcode discover tests -i ui`*

```
# Tests

- **Tests.Ui.Catalogue.WEB-002_AC-1 Every Card Offers Add To Cart** (`tests/ui/catalogue.robot:17`)
- **Tests.Ui.Catalogue.WEB-002_AC-1 Card Prices Are The Product Prices** (`tests/ui/catalogue.robot:26`)
- **Tests.Ui.Catalogue.WEB-002_AC-2 Categories Filter Group** (`tests/ui/catalogue.robot:39`)
- **Tests.Ui.Catalogue.WEB-002_AC-4 Rating Filter** (`tests/ui/catalogue.robot:46`)
- **Tests.Ui.Catalogue.WEB-002_AC-7 Audio Filter Shows Only Audio** (`tests/ui/catalogue.robot:52`)
- **Tests.Ui.Catalogue.WEB-002_AC-10 Reset Filters** (`tests/ui/catalogue.robot:64`)
- **Tests.Ui.Catalogue.WEB-002_AC-12 Handpicked Highlights** (`tests/ui/catalogue.robot:76`)
- **Tests.Ui.Checkout.WEB-006_AC-1 Order Total Adds Up** (`tests/ui/checkout.robot:17`)
- **Tests.Ui.Checkout.WEB-006_AC-7 Successful Order** (`tests/ui/checkout.robot:27`)
- **Tests.Ui.Checkout.WEB-006_AC-11 Validation Errors Next To Fields** (`tests/ui/checkout.robot:35`)
... (7 more lines)
```

**Agent:**

I asked RobotCode with `uv run --no-sync robotcode discover tests -i ui`. It found **11 tests** tagged `ui`, all in two files under `tests/ui/`.

**`tests/ui/catalogue.robot`** (suite `Tests.Ui.Catalogue`), 7 tests:
- `WEB-002_AC-1 Every Card Offers Add To Cart` (line 17)
- `WEB-002_AC-1 Card Prices Are The Product Prices` (line 26)
- `WEB-002_AC-2 Categories Filter Group` (line 39)
- `WEB-002_AC-4 Rating Filter` (line 46)
- `WEB-002_AC-7 Audio Filter Shows Only Audio` (line 52)
- `WEB-002_AC-10 Reset Filters` (line 64)
- `WEB-002_AC-12 Handpicked Highlights` (line 76)

**`tests/ui/checkout.robot`** (suite `Tests.Ui.Checkout`), 4 tests:
- `WEB-006_AC-1 Order Total Adds Up` (line 17)
- `WEB-006_AC-7 Successful Order` (line 27)
- `WEB-006_AC-11 Validation Errors Next To Fields` (line 35)
- `WEB-006_AC-12 Cart Cleared After Order` (line 50)

This used the default settings in `robot.toml`, with no profile. Nothing was run.

## Step 4 - A library question

**Prompt:**

> Which keyword of the installed Browser library reads the state of a checkbox, and what are its arguments?

*The agent runs `uv run --no-sync robotcode libdoc Browser show "Get Checkbox State"`*

```
### Get Checkbox State

#### Arguments

* `selector` (type: `str`)
* `assertion_operator` (type: `AssertionOperator | None`, default: `None`)
* `assertion_expected` (type: `bool | str`, default: `Unchecked`)
* `message` (type: `str | None`, default: `None`)

#### Returns

* `bool`
... (31 more lines)
```

**Agent:**

The keyword is **`Get Checkbox State`**. I looked it up with `uv run --no-sync robotcode libdoc Browser show "Get Checkbox State"`, so this is the documentation of the Browser version installed here. It returns a `bool`: `True` if the box is checked, `False` if not.

| Argument | Type | Default | Meaning |
| --- | --- | --- | --- |
| `selector` | `str` | required | The checkbox to read. |
| `assertion_operator` | `AssertionOperator \| None` | `None` | Only `==` and `!=` (and their equivalents) are allowed. If you leave it out, the keyword just returns the state and asserts nothing. |
| `assertion_expected` | `bool \| str` | `Unchecked` | The state you expect. Strings count as `True` except `FALSE`, `NO`, `OFF`, `0`, `UNCHECKED`, `NONE` and empty (case doesn't matter). So `checked` means `True` and `unchecked` means `False`. |
| `message` | `str \| None` | `None` | Replaces the default error message when the assertion fails. |

It uses strict mode, so the selector must match exactly one element.

Example from the docs:

```robotframework
Get Checkbox State    [name=can_send_email]    ==    checked
```

## Step 5 - Debug a broken test

**Prompt:**

> The test "WEB-002_AC-12 Handpicked Highlights" fails. Find out why with the RobotCode debugger: stop at the assertion that fails and look at the variables it compares. Don't guess from the failure message. Then tell me the cause before you change anything.

*The agent reads `<repo>/docs/agent-environment.md`*

*The agent loads the skill `robotcode:robotcode`*

*The agent runs `cat ~/.claude/plugins/cache/robotframework-agent-plugins/robotcode/7c753f8adca1/skills/robotcode/references/debugging.md`*

```
# Debugging a run — `robotcode robot-debug`

`robotcode robot-debug` (alias `run-debug`) is a `pdb`-style **command-line debugger** for Robot Framework. It runs a real `.robot` suite through the same runner as [`robotcode robot`](../SKILL.md) — 

Reach for the debugger when a recorded log isn't enough and you need the **live** state at the moment a test goes wrong — the real call stack, a variable's value at a specific point, or the result of 

- **[`results`](results.md)** reads a *finished* `output.xml` — no re-run. Try it **first** for "why did X fail?".
- **[REPL](repl.md)** builds state up from scratch to *explore* — no suite is running.
- **The debugger** re-runs the suite and stops it **mid-flight** to inspect the actual live state. Use it only when the recorded log doesn't answer the question.

Beyond post-mortem analysis, `robot-debug` also makes a tight **inner loop while you develop or fix a test**: run the test through it instead of a plain `robot` run, and break-on-failure (on by defaul

... (228 more lines)
```

*The agent runs `uv run --no-sync robotcode discover tests --search "WEB-002_AC-12" 2>&1 | tail -20`*

```
# Tests

- **Tests.Ui.Catalogue.`WEB-002_AC-12` Handpicked Highlights** (`tests/ui/catalogue.robot:76`)

## Statistics

- _Suites:_ 3
- _Suites with tests:_ 1
- _Tests:_ 1

_Filters: search=WEB-002_AC-12_
```

*The agent reads `<repo>/tests/ui/catalogue.robot`*

*The agent runs `uv run --no-sync python -m shop status 2>&1 | tail -20; docker ps --format '{{.Names}} {{.Status}} {{.Ports}}' 2>&1 | head`*

```
shop     http://localhost:9090  (version 0.3.0)
space    default
presets  clean, stage1
shop-shop-1 Up 13 hours (healthy) 0.0.0.0:9090->9090/tcp, :::9090->9090/tcp
```

*The agent runs `uv run --no-sync robotcode config show 2>&1 | head -60`*

```
variable-files = [
    "shop/variables.py",
]
output-dir = "results"
python-path = [
    ".",
]
paths = [
    "tests",
]
default-profiles = [
    "local",
... (29 more lines)
```

*The agent runs `command -v tmux; command -v script; command -v expect`*

```
Exit code 1
/usr/bin/tmux
/usr/bin/script
```

**Agent:**

I'll start the test under the RobotCode debugger in a tmux session so I can step through it interactively.

*The agent runs `tmux new-session -d -s rfdbg -x 250 -y 50 'uv run --no-sync robotcode robot-debug -bl "Tests.Ui.Catalogue.WEB-002_AC-12 Handpicked Highlights"; echo "=== EXITED rc=$? ==="; sleep 3600' && echo started`*

```
started
```

*The agent uses `ToolSearch` with `{"query": "select:Monitor", "max_results": 1}`*

*The agent runs `for i in $(seq 1 90); do out=$(tmux capture-pane -p -t rfdbg -S -200); if echo "$out" | grep -qE '\(rdb\)|=== EXITED'; then break; fi; sleep 1; done; tmux capture-pane -p -t rfdbg -S -200 | sed '/^$/N;/^\n$/D'`*

```
==============================================================================
Tests
==============================================================================
Tests.Ui
==============================================================================
Tests.Ui.Catalogue :: The products page, /products (spec: shop/catalogue).
==============================================================================
WEB-002_AC-12 Handpicked Highlights :: "Handpicked highlights" sho... .....F
* exception  BuiltIn.Should Be True  (tests/ui/catalogue.robot:83)  — Keyword failed: The highlights should show the three highest prices, highest first.
(rdb)
```

**Agent:**

It stopped at the failing `Should Be True` on line 83. Now I'll look at the variables it compares.

*The agent runs `send() { tmux send-keys -t rfdbg -l "$1"; tmux send-keys -t rfdbg Enter; sleep 1.5; }
tmux clear-history -t rfdbg
send '.where'
send '.list'
send '.pprint ${shown}'
send '.whatis ${shown}'
send '.pprint ${expected}'
send '.whatis ${expected}'
send '.pprint ${catalogue}'
tmux capture-pane -p -t rfdbg -S -300 | sed '/^$/N;/^\n$/D' | tail -120`*

```
  'image_url': '/static/img/aurora-headphones.jpg',
  'inventory': 25,
  'name': 'Aurora Neural Headphones',
  'price': 249.99,
  'rating': 4.8,
  'review_count': 214,
  'sku': 'AUR-NEU-001'},
 {'category': 'Health',
  'description': 'Smart hydration bottle that tracks intake, delivers pacing '
                 'reminders, and purifies water on-demand.',
  'id': 12,
  'image_url': '/static/img/cascade-bottle.jpg',
... (108 more lines)
```

*The agent runs `tmux capture-pane -p -t rfdbg -S -300 | sed '/^$/N;/^\n$/D' | grep -n -B2 -A14 -E '^\(rdb\) \.(where|list|pprint \$\{shown|whatis|pprint \$\{expected)' | head -80`*

```
8-WEB-002_AC-12 Handpicked Highlights :: "Handpicked highlights" sho... .....F
9-* exception  BuiltIn.Should Be True  (tests/ui/catalogue.robot:83)  — Keyword failed: The highlights should show the three highest prices, highest first.
10:(rdb) .where
11-> #0  BuiltIn.Should Be True               tests/ui/catalogue.robot:83
12-  #1  WEB-002_AC-12 Handpicked Highlights  tests/ui/catalogue.robot:76
13-  #2  Catalogue                            tests/ui/catalogue.robot
14-  #3  Ui                                   tests/ui
15-  #4  Tests                                tests
16:(rdb) .list
17-     78      [Tags]    broken
18-     79      @{catalogue}=    Get Catalogue From API
19-     80      ${expected}=    Evaluate    [str(p) for p in sorted((float(x["price"]) for x in $catalogue), reverse=True)[:3]]
... (25 more lines)
```

*The agent runs `send() { tmux send-keys -t rfdbg -l "$1"; tmux send-keys -t rfdbg Enter; sleep 1.5; }
tmux clear-history -t rfdbg; tmux send-keys -t rfdbg C-l; sleep 0.5
send '.kw Format Price'
send '${fmt}=    Evaluate    [__import__("robot").libraries.BuiltIn.BuiltIn().run_keyword("Format Price", p) for p in sorted((x["price"] for x in $catalogue), reverse=True)[:3]]'
send '.print ${fmt} == ${shown}'
tmux capture-pane -p -t rfdbg -S -200 | sed '/^$/N;/^\n$/D' | tail -60`*

```
  'review_count': 91,
  'sku': 'ORB-DRN-011'},
 {'category': 'Health',
  'description': 'Titanium wellness ring measuring biometrics with '
                 'personalised recovery insights, sleep coaching, and training '
                 'recommendations.',
  'id': 3,
  'image_url': '/static/img/pulse-ring.jpg',
  'inventory': 60,
  'name': 'Pulse Bio Ring',
  'price': 189.0,
  'rating': 4.7,
... (48 more lines)
```

**Agent:**

`Format Price` applied to the three highest API prices gives exactly `${shown}`. Now I'll close the debug session and check the spec wording for AC-12.

*The agent runs `tmux send-keys -t rfdbg -l '.continue'; tmux send-keys -t rfdbg Enter
for i in $(seq 1 30); do tmux capture-pane -p -t rfdbg -S -50 | grep -q '=== EXITED' && break; sleep 1; done
tmux capture-pane -p -t rfdbg -S -50 | sed '/^$/N;/^\n$/D' | tail -15; tmux kill-session -t rfdbg
cd <repo> && grep -rn -B2 -A8 'AC-12' openspec/specs/shop/ | head -40; grep -rn 'Format Price\|Get Highlight Prices' resources/*.resource | head`*

```
------------------------------------------------------------------------------
Tests.Ui.Catalogue :: The products page, /products (spec: shop/cat... | FAIL |
1 test, 0 passed, 1 failed
==============================================================================
Tests.Ui                                                              | FAIL |
1 test, 0 passed, 1 failed
==============================================================================
Tests                                                                 | FAIL |
1 test, 0 passed, 1 failed
==============================================================================
Output:  <repo>/results/output.xml
Log:     <repo>/results/log.html
... (24 more lines)
```

**Agent:**

The test is wrong, not the shop. Its expected list uses a different format from the one the page shows. I haven't changed anything.

**What the debugger showed.** I ran the test with `robotcode robot-debug -bl "Tests.Ui.Catalogue.WEB-002_AC-12 Handpicked Highlights"`. It stopped at the failing `Should Be True    $shown == $expected` (`tests/ui/catalogue.robot:83`), where:

| Variable | Value | Type |
|---|---|---|
| `${shown}` (from the page, via `Get Highlight Prices`) | `['$899.00', '$799.00', '$389.00']` | list of str |
| `${expected}` (from the API, built on line 80) | `['899.0', '799.0', '389.0']` | list of str |

Both lists hold the same three prices in the same order: 899, 799, 389. That's the Orbit Drone, the Atlas Desk and the Horizon Display, the three most expensive items in `${catalogue}`. So the shop does what the spec asks (`openspec/specs/shop/catalogue/spec.md:85`: the 3 highest-priced products, highest first).

**Cause.** Line 80 turns each price into text with Python's `str(float(...))`, which gives `'899.0'`. The page shows prices the way the shop displays them, `'$899.00'`. The comparison is between strings, so they can never match.

**Check.** At the debugger prompt, still inside the paused test, I ran `Format Price` from `resources/catalogue.resource:98` on the three highest API prices. It returned `['$899.00', '$799.00', '$389.00']`, and `${fmt} == ${shown}` came out `True`. The sibling test `WEB-002_AC-1 Card Prices Are The Product Prices` already builds its expected values this way (line 35).

**Proposed fix (not applied).** Build `${expected}` by sorting the API prices from highest to lowest, taking the top three, and running each through `Format Price`, the same way AC-1 does. Only the test changes. The shop, the spec and `legacy.resource` stay untouched.

The test is also tagged `broken`. Should I remove that tag once it passes? Tell me whether to go ahead with the fix, and about the tag.

**Prompt:**

> Fix the test so that it verifies what the criterion says, remove its broken tag, and run it.

*The agent reads `<repo>/docs/conventions.md`*

*The agent reads `<repo>/resources/catalogue.resource`*

**Agent:**

Before editing, I'll check what else refers to the `broken` tag and this test, and what the highlight links contain.

*The agent runs `grep -rn --exclude-dir={results,.git,.venv,node_modules} -i 'broken\|Handpicked\|AC-12' . 2>/dev/null | grep -v '^./openspec/specs/shop/checkout' | head -40`*

```
GLOSSARY.md:146:A repair of a broken locator at run time: a healing listener notices that an element cannot be found, finds the one
GLOSSARY.md:207:### Broken test
GLOSSARY.md:209:A test that fails on purpose, tagged `broken`, for a debugging lab. There are two.
.agents/skills/openspec-propose/SKILL.md:31:**Project check:** These steps expect a project that already uses OpenSpec. Before the first step that writes anything (`new change`, `archive`, `sync specs
.agents/skills/openspec-sync-specs/SKILL.md:19:**Project check:** These steps expect a project that already uses OpenSpec. Before the first step that writes anything (`new change`, `archive`, `sync sp
openspec/specs/shop/catalogue/spec.md:85:### Requirement: Handpicked highlights (WEB-002_AC-12)
openspec/specs/shop/catalogue/spec.md:86:The products page SHALL display a "Handpicked highlights" section showing the 3 highest-priced products, sorted by price with the highest first.
openspec/specs/shop/catalogue/spec.md:89:- **WHEN** the shopper views "Handpicked highlights"
tests/ui/checkout.robot:50:WEB-006_AC-12 Cart Cleared After Order
.agents/skills/openspec-apply-change/SKILL.md:17:**Project check:** These steps expect a project that already uses OpenSpec. Before the first step that writes anything (`new change`, `archive`, `sync 
tests/ui/catalogue.robot:48:    [Tags]    broken
tests/ui/catalogue.robot:76:WEB-002_AC-12 Handpicked Highlights
... (28 more lines)
```

*The agent runs `curl -s http://localhost:9090/products | python3 -c "
import sys,re
h=sys.stdin.read()
i=h.find('Handpicked highlights')
s=h.rfind('<section',0,i)
e=h.find('</section>',i)
print(h[s:e+10])
"`*

```
Exit code 1
pyenv: version `3.12' is not installed (set by <repo>/.python-version)
```

*The agent runs `curl -s http://localhost:9090/products | uv run --no-sync python -c "
import sys
h=sys.stdin.read()
i=h.find('Handpicked highlights')
s=h.rfind('<section',0,i)
e=h.find('</section>',i)
print(h[s:e+10])
"`*

```
<section class="catalog-hero">
  <div>
    <h1>Discover your next workflow upgrade</h1>
    <p>
      Browse thoughtfully crafted devices, accessories, and wellness tools. Everything in this catalogue is vetted by
      design leaders and product engineers in our community.
    </p>
    <form class="hero__search" role="search">
      <label class="form-field" aria-label="Search the catalogue">
        <span class="form-field__icon" aria-hidden="true">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"
            stroke-linecap="round" stroke-linejoin="round">
... (81 more lines)
```

*The agent edits `<repo>/resources/catalogue.resource`*

```
The file <repo>/resources/catalogue.resource has been updated successfully. (fil
```

*The agent edits `<repo>/tests/ui/catalogue.robot`*

```
The file <repo>/tests/ui/catalogue.robot has been updated successfully. (file st
```

**Agent:**

Now a static check of both files, then the run.

*The agent runs `uv run --no-sync robotcode analyze code tests/ui/catalogue.robot resources/catalogue.resource 2>&1 | tail -15; echo "analyze rc=$?"`*

```
Files: 2, Errors: 0, Warnings: 0, Infos: 0, Hints: 0 (in 5.31s)
analyze rc=0
```

*The agent runs `uv run --no-sync robotcode robot -bl "Tests.Ui.Catalogue.WEB-002_AC-12 Handpicked Highlights" 2>&1 | tail -20; echo "robot rc=${PIPESTATUS[0]}"`*

```
Tests                                                                         
==============================================================================
Tests.Ui                                                                      
==============================================================================
Tests.Ui.Catalogue :: The products page, /products (spec: shop/catalogue).    
==============================================================================
WEB-002_AC-12 Handpicked Highlights :: "Handpicked highlights" sho... | PASS |
------------------------------------------------------------------------------
Tests.Ui.Catalogue :: The products page, /products (spec: shop/cat... | PASS |
1 test, 1 passed, 0 failed
==============================================================================
Tests.Ui                                                              | PASS |
... (9 more lines)
```

**Agent:**

The test now passes. It checks what WEB-002_AC-12 asks for: the three most expensive products, highest price first.

**Changes**
- **`tests/ui/catalogue.robot`**, `WEB-002_AC-12 Handpicked Highlights`:
  - I removed the `broken` tag.
  - The test sorts the catalogue from the API by price and takes the top three products.
  - It checks that the section shows exactly three products, and that each one's name matches and its price matches, in order. Prices go through `Format Price` so they compare as the shop shows them (`$899.00`), the same way the AC-1 price test does. That format difference was the original failure.
  - The documentation line now follows the criterion's wording.
- **`resources/catalogue.resource`**: new keyword `Get Highlight Names`, next to `Get Highlight Prices`. It reads the name from each highlight link, so the locator stays in the resource file. `legacy.resource` is untouched.

**Checks**
- `robotcode analyze code` on both files found no errors or warnings.
- `uv run robotcode robot -bl "Tests.Ui.Catalogue.WEB-002_AC-12 Handpicked Highlights"` passed: 1 test, 1 passed. Log: `results/log.html`.

**Now out of step with the workshop docs:** three files say two tests are tagged `broken`, and now only `WEB-002_AC-4 Rating Filter` is:
- `openspec/specs/workshop/test-conventions/spec.md:51`
- `docs/conventions.md:74`
- `GLOSSARY.md:209`

Something that relies on the count, such as a lab check, could now disagree. I haven't touched these files. Should I update them, or leave them as the workshop ships them?

**The participant runs** `uv run robotcode robot --test "WEB-002_AC-12 Handpicked Highlights"`:

```
Tests.Ui.Catalogue :: The products page, /products (spec: shop/cat... | PASS |
1 test, 1 passed, 0 failed
==============================================================================
Tests.Ui                                                              | PASS |
1 test, 1 passed, 0 failed
==============================================================================
Tests                                                                 | PASS |
1 test, 1 passed, 0 failed
==============================================================================
Output:  <repo>/results/output.xml
Log:     <repo>/results/log.html
Report:  <repo>/results/report.html
```

**The participant runs** `git diff --stat`:

```
 AGENTS.md                    | 38 +++++++++++++++++++++++++-------------
 resources/catalogue.resource | 10 ++++++++++
 tests/ui/catalogue.robot     | 17 +++++++++++------
 3 files changed, 46 insertions(+), 19 deletions(-)
```

## Step 6 - Explore with the REPL

*Step 6 was recorded again on 2026-09-26 with Claude Code 2.1.283, after the suite's `HEADLESS` setting was fixed so that `-v HEADLESS:False` holds in the REPL. The other steps are from the first rehearsal.*


**Prompt:**

> No test covers the price range filter yet. Explore it with the RobotCode REPL and a visible browser (HEADLESS set to False): open the products page through resources/shop.resource, set the range to $100-$300, apply the filters, and tell me which keywords and locators would work for a test. Don't write a test file.

*The agent reads `<repo>/docs/agent-environment.md`*

*The agent reads `<repo>/docs/conventions.md`*

*The agent reads `<repo>/resources/shop.resource`*

*The agent runs `ls; cat robot.toml; ls resources tests tests/*; ls docs`*

```
AGENTS.md
CLAUDE.md
CONTRIBUTING.md
GLOSSARY.md
LICENSE
README.md
SETUP.md
agents
docs
hooks
labs
mcp
... (69 more lines)
```

*The agent reads `<repo>/docs/robotcode.md`*

*The agent reads `<repo>/resources/catalogue.resource`*

*The agent reads `<repo>/tests/ui/catalogue.robot`*

*The agent runs `git diff --stat && git diff resources/catalogue.resource tests/ui/catalogue.robot; ls openspec/specs/shop/; grep -rn -i "price range\|price-range\|min.*max" openspec/specs/shop/ | head -50`*

```
 AGENTS.md                    | 38 +++++++++++++++++++++++++-------------
 resources/catalogue.resource | 10 ++++++++++
 tests/ui/catalogue.robot     | 17 +++++++++++------
 3 files changed, 46 insertions(+), 19 deletions(-)
diff --git a/resources/catalogue.resource b/resources/catalogue.resource
index 0b9bc0b..6a09c9a 100644
--- a/resources/catalogue.resource
+++ b/resources/catalogue.resource
@@ -95,6 +95,16 @@ Get Highlight Prices
     END
     RETURN    ${prices}
 
... (59 more lines)
```

*The agent reads `<repo>/openspec/specs/shop/catalogue/spec.md`*

*The agent runs `uv run --no-sync python -m shop status 2>&1 | head -30; curl -s -o /dev/null -w "%{http_code}\n" http://localhost:9090/products`*

```
shop     http://localhost:9090  (version 0.3.0)
space    default
presets  clean, stage1
200
```

**Agent:**

I've read the conventions and the spec (WEB-002_AC-8), and the local shop is running. Next I'll open the products page in the RobotCode REPL with a visible browser.

*The agent runs `echo "DISPLAY=$DISPLAY WAYLAND=$WAYLAND_DISPLAY"; cd <repo> && uv run robotcode repl --help 2>&1 | head -40`*

```
DISPLAY=:0 WAYLAND=wayland-0
Usage: robotcode repl [OPTIONS] [FILES]...

  Run Robot Framework interactively (alias `shell`).

  Starts an interactive session where you enter Robot Framework keywords and
  run them immediately. Pass FILES to execute them in the session.

Options:
  --no-history                    Don't load or save the persistent history
                                  file. In-session arrow-up recall still
                                  works, but nothing crosses session
... (29 more lines)
```

*The agent runs `uv run robotcode libdoc Browser list "*Aria*" ; uv run robotcode libdoc Browser list "*Range*"; uv run robotcode libdoc Browser list "Fill*"; uv run robotcode libdoc Browser list "*Slider*"`*

```
Get Aria Snapshot
Fill Secret
Fill Text
```

*The agent runs `printf '%s\n' \
'Import Resource    ${EXECDIR}/resources/catalogue.resource' \
'Open Shop Browser' \
'Start Shop Test' \
'Go To Catalogue' \
'${snap}=    Get Aria Snapshot    role=complementary' \
'Log To Console    ${snap}' \
'${html}=    Get Property    role=complementary >> role=group[name="Price range"]    outerHTML' \
'Log To Console    ${html}' \
'${form}=    Get Property    role=complementary    outerHTML' \
'Log To Console    ${form}' \
'.exit' \
| timeout 120 uv run robotcode repl --plain --no-history -v HEADLESS:False 2>&1 | tail -150`*

```
[ INFO ] ${headless} = False
[ INFO ] {"browser": "chromium", "headless": false, "chromiumSandbox": false, "devtools": false, "handleSIGHUP": true, "handleSIGINT": true, "handleSIGTERM": true, "slowMo": 0.0, "timeout": 30000.0, "
[ FAIL ] FileNotFoundError: [Errno 2] No such file or directory: '<repo>/resul
[ INFO ] {
  "acceptDownloads": true,
  "baseURL": "http://localhost:9090",
  "bypassCSP": false,
  "forcedColors": "none",
  "ignoreHTTPSErrors": false,
  "javaScriptEnabled": true,
  "offline": false,
  "reducedMotion": "no-preference",
... (14 more lines)
```

**Agent:**

The REPL hit the documented trap: `results/` doesn't exist yet. It's git-ignored, so I'll create it and follow the flow exactly through `shop.resource`.

*The agent runs `git check-ignore -v results/ && mkdir -p results && printf '%s\n' \
'Import Resource    ${EXECDIR}/resources/shop.resource' \
'Open Shop Browser' \
'Start Shop Test' \
'Go To Shop Page    /products' \
'${snap}=    Get Aria Snapshot    role=complementary' \
'Log To Console    ${snap}' \
'${html}=    Get Property    role=complementary >> role=group[name="Price range"]    outerHTML' \
'Log To Console    ${html}' \
'.exit' \
| timeout 120 uv run robotcode repl --plain --no-history -v HEADLESS:False 2>&1 | grep -v '^\[ INFO \] {' | tail -150`*

```
.gitignore:11:results/	results/
[ INFO ] ${headless} = False
[ INFO ] Starting Browser process <repo>/.venv/lib/python3.12/site-packages/Br
[ INFO ] Successfully created browser with options: {"browser":"chromium","headless":false,"chromiumSandbox":false,"devtools":false,"handleSIGHUP":true,"handleSIGINT":true,"handleSIGTERM":true,"slowMo
  "acceptDownloads": true,
  "baseURL": "http://localhost:9090",
  "bypassCSP": false,
  "forcedColors": "none",
  "ignoreHTTPSErrors": false,
  "javaScriptEnabled": true,
  "offline": false,
  "reducedMotion": "no-preference",
... (122 more lines)
```

*The agent runs `cat resources/legacy.resource; uv run robotcode libdoc Browser show "Fill Text" | head -40`*

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
... (68 more lines)
```

*The agent runs `cat resources/api.resource | head -60`*

```
*** Settings ***
Documentation       The shop's API, in the configured workshop space.

Library             Collections
Library             RequestsLibrary


*** Keywords ***
Open Shop API
    [Documentation]    Creates the API session. It sends ${SHOP_SPACE} when one is set.
    &{headers}=    Create Dictionary
    IF    "${SHOP_SPACE}"
... (13 more lines)
```

**Agent:**

Now the main experiment: set both sliders with `Fill Text`, watch the displayed values and hidden fields, apply, and read the resulting grid.

*The agent runs `printf '%s\n' \
'Import Resource    ${EXECDIR}/resources/shop.resource' \
'Import Resource    ${EXECDIR}/resources/catalogue.resource' \
'Import Resource    ${EXECDIR}/resources/legacy.resource' \
'Import Resource    ${EXECDIR}/resources/api.resource' \
'Open Shop Browser' \
'Start Shop Test' \
'Go To Shop Page    /products' \
'${before}=    Get Grid Card Count' \
'Fill Text    ${FILTERS} >> role=slider[name="Minimum price"]    100' \
'Fill Text    ${FILTERS} >> role=slider[name="Maximum price"]    300' \
'${shown}=    Get Price Range Values' \
'${min_value}=    Get Property    ${FILTERS} >> role=slider[name="Minimum price"]    value' \
'${max_value}=    Get Property    ${FILTERS} >> role=slider[name="Maximum price"]    value' \
'${hidden_min}=    Get Attribute    ${FILTERS} >> input[name="price_min"]    value' \
'${hidden_hidden_max}=    Get Property    ${FILTERS} >> input[name="price_max"]    value' \
'${hidden_min_prop}=    Get Property    ${FILTERS} >> input[name="price_min"]    value' \
'${form}=    Get Property    role=complementary >> xpath=ancestor::form    outerHTML' \
'Apply Filters' \
'${url}=    Get Url' \
'${after_shown}=    Get Price Range Values' \
'${after_min}=    Get Property    ${FILTERS} >> role=slider[name="Minimum price"]    value' \
'${after_max}=    Get Property    ${FILTERS} >> role=slider[name="Maximum price"]    value' \
'${count}=    Get Grid Card Count' \
'@{names}=    Get Grid Card Names' \
'@{prices}=    Get Card Prices' \
'Open Shop API' \
'@{catalogue}=    Get Catalogue From API' \
'@{expected}=    Evaluate    sorted((p["name"], p["price"]) for p in $catalogue if 100 <= float(p["price"]) <= 300)' \
'@{all}=    Evaluate    sorted((float(p["price"]), p["name"]) for p in $catalogue)' \
'Sleep    3s' \
'.exit' \
| timeout 180 uv run robotcode repl --plain --no-history -v HEADLESS:False 2>&1 | grep -E '^\[ (FAIL|WARN) \]|\$\{|@\{|URL' | grep -v 'Starting Browser'`*

```
[ INFO ] ${headless} = False
  "baseURL": "http://localhost:9090",
[ INFO ] {'acceptDownloads': True, 'baseURL': 'http://localhost:9090', 'bypassCSP': False, 'forcedColors': 'none', 'ignoreHTTPSErrors': False, 'javaScriptEnabled': True, 'offline': False, 'reducedMoti
[ INFO ] Successfully opened URL http://localhost:9090/products
[ INFO ] ${count} = 12
[ INFO ] ${before} = 12
[ INFO ] @{elements} = [ role=complementary >> role=group[name="Price range"] >> role=status >> nth=0 | role=complementary >> role=group[name="Price range"] >> role=status >> nth=1 ]
[ INFO ] @{texts} = [ ]
[ INFO ] ${text} = 100.00
[ INFO ] ${text} = 300.00
[ INFO ] @{values} = [ 100.00 | 300.00 ]
[ INFO ] ${shown} = ['100.00', '300.00']
... (43 more lines)
```

*The agent runs `grep -n -A8 "Amount From Text" resources/checkout.resource | head -20; uv run robotcode libdoc Browser show "Click" | sed -n '1,25p'; curl -s http://localhost:9090/api/products/ | python3 -c 'import json,sys; [print(p["price"], p["name"], p.get("category")) for p in sorted(json.load(sys.stdin)["items"], key=lambda p: p["price"])]'`*

```
Exit code 1
50:    ${amount}=    Amount From Text    ${text}
51-    RETURN    ${amount}
52-
53:Amount From Text
54-    [Documentation]    The amount in a text, ``$1,234.50`` as the number 1234.5.
55-    ...                A label around it is ignored; with several amounts, the last one counts.
56-    [Arguments]    ${text}
57-    @{amounts}=    Get Regexp Matches    ${text}    \\$([0-9,]+\\.[0-9]{2})    1
58-    Should Not Be Empty    ${amounts}    msg=No amount in "${text}".
59-    ${amount}=    Evaluate    float($amounts[-1].replace(",", ""))
60-    RETURN    ${amount}
... (27 more lines)
```

*The agent runs `curl -s http://localhost:9090/api/products/ | uv run --no-sync python -c 'import json,sys; [print(p["price"], p["name"], p.get("category")) for p in sorted(json.load(sys.stdin)["items"], key=lambda p: p["price"])]'`*

```
39.5 Insight Smart Notebook Productivity
59.0 Focus Loop Timer Productivity
79.0 Cascade Water Bottle Health
129.0 Nimbus Desk Light Home Office
149.0 Summit Trail Shoes Outdoors
169.0 Velocity Travel Backpack Travel
189.0 Pulse Bio Ring Health
219.0 Echo Conference Speaker Audio
249.99 Aurora Neural Headphones Audio
389.0 Horizon Portable Display Displays
799.0 Atlas Standing Desk Furniture
899.0 Orbit Drone Camera Imaging
```

*The agent runs `printf '%s\n' \
'Import Resource    ${EXECDIR}/resources/shop.resource' \
'Import Resource    ${EXECDIR}/resources/catalogue.resource' \
'Open Shop Browser' \
'Start Shop Test' \
'Go To Shop Page    /products' \
'Fill Text    ${FILTERS} >> role=slider[name="Minimum price"]    100' \
'Fill Text    ${FILTERS} >> role=slider[name="Maximum price"]    300' \
'Apply Filters' \
'${grid}=    Get Aria Snapshot    ${GRID}' \
'Log To Console    ${grid}' \
'${main}=    Get Text    role=main >> h1' \
'${counts}=    Get Element Count    text=/[0-9]+ (products|results|items)/i' \
'${count_text}=    Get Text    text=/[0-9]+ (products|results|items)/i' \
'Take Screenshot    filename=${EXECDIR}/results/price-range-100-300' \
'Sleep    3s' \
'.exit' \
| timeout 180 uv run robotcode repl --plain --no-history -v HEADLESS:False 2>&1 | grep -vE '^\[ INFO \] (\{|Starting|Successfully created)|^  "' | sed -n '1,120p'`*

```
[ INFO ] ${headless} = False
    "width": 1280,
    "height": 720
  }
}
[ INFO ] Successfully initialized new page object and opened url: about:blank
[ INFO ] Successfully opened URL http://localhost:9090/products
[ INFO ] Fills the text '100' in the given field.
[ INFO ] Fills the text '300' in the given field.
[ INFO ] Clicks the element 'role=complementary >> role=button[name="Apply filters"]'.
[ INFO ] Waited for Element with selector section:has(h2:text-is("All products")):not(:has(section)) at state visible
[ INFO ] Aria snapshot received successfully.
... (108 more lines)
```

*The agent runs `printf '%s\n' \
'Import Resource    ${EXECDIR}/resources/shop.resource' \
'Import Resource    ${EXECDIR}/resources/catalogue.resource' \
'Import Resource    ${EXECDIR}/resources/legacy.resource' \
'Open Shop Browser' \
'Start Shop Test' \
'Go To Shop Page    /products' \
'Fill Text    ${FILTERS} >> role=slider[name="Minimum price"]    100' \
'Fill Text    ${FILTERS} >> role=slider[name="Maximum price"]    300' \
'Apply Filters' \
'${count_text}=    Get Text    ${GRID} >> p:text-matches("^[0-9]+ products?$")' \
'${prices_via_contract}=    Get Texts    ${GRID} >> article >> ${CARD PRICE}' \
'${h}=    Get Text    role=main >> h1' \
'.exit' \
| timeout 180 uv run robotcode repl --plain --no-history -v HEADLESS:False 2>&1 | grep -E '^\[ FAIL|count_text|prices_via|\$\{h\}'`*

```
[ INFO ] ${count_text} = 6 products
[ INFO ] ${prices_via_contract} = ['$249.99', '$219.00', '$129.00', '$189.00', '$149.00', '$169.00']
[ INFO ] ${h} = Discover your next workflow upgrade
```

*The agent reads `<repo>/results/price-range-100-300.png`*

**Agent:**

Everything I need is confirmed. I'll do a quick REPL check of the price-to-number conversion I'm about to suggest, so the sketch below isn't untested.

*The agent runs `printf '%s\n' \
'@{texts}=    Create List    $249.99    $219.00    $1,129.00' \
'@{amounts}=    Evaluate    [float(text.lstrip("$").replace(",", "")) for text in $texts]' \
'.exit' | timeout 60 uv run robotcode repl --plain --no-history 2>&1 | grep -E 'amounts|FAIL'`*

```
[ INFO ] @{amounts} = [ 249.99 | 219.0 | 1129.0 ]
```

**Agent:**

The $100–$300 filter works in the RobotCode REPL with a visible browser. I opened `/products` through `shop.resource` (`Open Shop Browser`, `Start Shop Test`, `Go To Shop Page /products`), set both sliders, clicked "Apply filters", and the page showed "6 products". Those are exactly the six products the API lists between $100 and $300: $249.99, $219.00, $129.00, $189.00, $149.00 and $169.00. The spec for this is `WEB-002_AC-8`. I didn't create any test file.

## Locators that work

| What | Locator | Checked |
|---|---|---|
| Minimum slider | `${FILTERS} >> role=slider[name="Minimum price"]` | yes |
| Maximum slider | `${FILTERS} >> role=slider[name="Maximum price"]` | yes |
| Values shown for the range | `${FILTERS} >> role=group[name="Price range"] >> role=status` (already used by `Get Price Range Values`) | yes: `100.00` and `300.00`, before and after applying |
| Card prices | `${GRID} >> article >> ${CARD PRICE}` | yes: returns the six prices |
| Result count (optional) | `${GRID} >> p:text-matches("^[0-9]+ products?$")` | yes: "6 products" |

`${FILTERS}`, `${GRID}` and `${CARD PRICE}` are variables already defined in `resources/catalogue.resource`.

**How to set the range: `Fill Text`.** The sliders are ordinary browser range sliders, and `Fill Text <slider> 100` sets the exact value. The page reacts properly: the displayed values change, and the form sends `?price_min=100.00&price_max=300.00`. Two alternatives I'd avoid:
- **Dragging the handles with the mouse** depends on pixel positions, and the sliders allow any value (`step="any"`), so you won't land on exactly 100.
- **Opening that URL directly** skips the "shopper sets the price range" part of the spec.

## Keywords

**Already there and usable:**
- `Go To Catalogue` is `Go To Shop Page /products` plus a wait for the product grid.
- `Apply Filters` clicks the button and waits for the new page, because Browser's `Click` waits for the page load it triggers.
- `Get Price Range Values`, `Get Grid Card Count` and `Get Grid Card Names` all work.

**Avoid `Get Card Prices`.** It's in `legacy.resource` and finds the grid by the CSS class `.product-grid`, which the conventions say not to rely on. The card-price locator above gets the same prices without that class.

**Missing, and would belong in `resources/catalogue.resource`.** This is only a sketch, not written to the repo. I ran each step of it in the REPL, but not as a keyword:

```robotframework
Set Price Range
    [Documentation]    Moves the price range handles to ``minimum`` and ``maximum``.
    [Arguments]    ${minimum}    ${maximum}
    Fill Text    ${FILTERS} >> role=slider[name="Minimum price"]    ${minimum}
    Fill Text    ${FILTERS} >> role=slider[name="Maximum price"]    ${maximum}

Get Grid Card Price Amounts
    [Documentation]    The price of every grid card as a number, in page order.
    @{texts}=    Get Texts    ${GRID} >> article >> ${CARD PRICE}
    @{amounts}=    Evaluate    [float(text.lstrip("$").replace(",", "")) for text in $texts]
    RETURN    ${amounts}
```

A test would then be `Go To Catalogue` → `Set Price Range 100 300` → `Apply Filters` → check that the list isn't empty and that every amount is between 100 and 300. That's what the spec asks: "every product in the grid is priced from $100.00 to $300.00 inclusive". Name it `WEB-002_AC-8 …`; the suite already tags every test with `WEB-002` and `ui`.

## Worth knowing
- **The bounds aren't tested.** No product costs exactly $100 or $300; the nearest ones outside are $79.00 and $389.00. A test with this range shows products outside are excluded, but not that $100 and $300 themselves are included. Covering that would need different shop data, which a test must not create through a preset.
- **One setup step:** the REPL failed at first with `FileNotFoundError … results/playwright-log.txt`, the trap listed in `docs/robotcode.md`. I created `results/`, which git ignores, and left it in place.

## Stretch - A results question

**Prompt:**

> Of the tests tagged WEB-002 in the last run, which failed and why? Use the results, not output.xml.

*The agent loads the skill `robotcode:robotcode`*

*The agent reads `<repo>/docs/agent-environment.md`*

*The agent reads `~/.claude/plugins/cache/robotframework-agent-plugins/robotcode/7c753f8adca1/skills/robotcode/references/results.md`*

*The agent runs `uv run --no-sync robotcode results --help; uv run --no-sync robotcode results show --help`*

```
Usage: robotcode results [OPTIONS] COMMAND [ARGS]...

  Inspect a finished run's `output.xml` / `output.json` — counts, failures,
  and per-test execution tree, without re-running.

  The result file is auto-discovered from the active profile's `output_dir` /
  `output` settings; override with `-o/--output PATH`. Use `-f json` (or
  `toml`) for a structured payload.

  Examples:
  ```
  robotcode results summary
... (103 more lines)
```

*The agent runs `uv run --no-sync robotcode results show -i WEB-002 --tags --message-chars 0`*

```
# Show — results/output.xml

- ✅ **PASS** Tests.Ui.Catalogue.WEB-002_AC-12 Handpicked Highlights (`tests/ui/catalogue.robot:76`) _(22:05:56 · 405 ms)_
  - _Tags:_ ui, web-002

## Statistics

- _Total:_ 1
- _Passed:_ 1
- _Failed:_ 0
- _Skipped:_ 0
- _Elapsed:_ 943 ms
... (2 more lines)
```

*The agent runs `uv run --no-sync robotcode results summary; ls -la results/`*

```
# Summary — results/output.xml

- _Status:_ ✅ **PASS**
- _Total:_ 1
- _Passed:_ 1
- _Failed:_ 0
- _Skipped:_ 0
- _Started:_ 2026-09-24 22:05:55
- _Ended:_ 2026-09-24 22:05:57
- _Elapsed:_ 1.21 s

total 584
... (9 more lines)
```

**Agent:**

The last run holds only one test, and it has the WEB-002 tag. I'm checking the other result folders in case an earlier, bigger run is the one you mean.

*The agent runs `ls -la results/lab-02 results/lab-03; uv run --no-sync robotcode discover tests -i WEB-002`*

```
results/lab-02:
total 16
drwxr-xr-x 2 user user 4096 Sep 24 21:52 .
drwxr-xr-x 5 user user 4096 Sep 24 22:05 ..
-rw-r--r-- 1 user user  554 Sep 24 21:52 after.robot
-rw-r--r-- 1 user user  554 Sep 24 21:49 before.robot

results/lab-03:
total 12
drwxr-xr-x 2 user user 4096 Sep 24 21:54 .
drwxr-xr-x 5 user user 4096 Sep 24 22:05 ..
-rw-r--r-- 1 user user  565 Sep 24 21:54 with-skills.robot
... (15 more lines)
```

**Agent:**

None of the WEB-002 tests failed in the last run, but that run was too small to tell you much.

The last run (`results/output.xml`, 2026-09-24 22:05) executed a single test:

- ✅ **PASS**: `WEB-002_AC-12 Handpicked Highlights` (`tests/ui/catalogue.robot:76`), 405 ms

The suite has seven WEB-002 tests, so the other six weren't part of that run:

- `WEB-002_AC-1 Every Card Offers Add To Cart`
- `WEB-002_AC-1 Card Prices Are The Product Prices`
- `WEB-002_AC-2 Categories Filter Group`
- `WEB-002_AC-4 Rating Filter`
- `WEB-002_AC-7 Audio Filter Shows Only Audio`
- `WEB-002_AC-10 Reset Filters`

No earlier results are kept. Each run overwrites `results/output.xml`, and `results/lab-02` and `results/lab-03` hold only `.robot` files. If you were thinking of an earlier, fuller run where something failed, its results have been overwritten.

To get a real answer for all seven, I can run them with `uv run robotcode robot -i WEB-002` and then check the results again.
