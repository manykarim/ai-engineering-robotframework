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

**Prompt:**

> No test covers the price range filter yet. Explore it with the RobotCode REPL and a visible browser (HEADLESS set to False): open the products page through resources/shop.resource, set the range to $100-$300, apply the filters, and tell me which keywords and locators would work for a test. Don't write a test file.

**Agent:**

I'll start with the environment and conventions docs the repo asks me to read first.

*The agent reads `<repo>/docs/agent-environment.md`*

*The agent reads `<repo>/docs/conventions.md`*

*The agent loads the skill `robotcode:robotcode`*

*The agent reads `~/.claude/plugins/cache/robotframework-agent-plugins/robotcode/7c753f8adca1/skills/robotcode/references/repl.md`*

*The agent reads `<repo>/resources/shop.resource`*

**Agent:**

The skill reference file needs permission I don't have, so I'll work from the skill summary. Next I'll look at the existing catalogue keywords, the spec for the price filter, and the config.

*The agent reads `<repo>/resources/catalogue.resource`*

*The agent runs `ls resources openspec/specs/shop && cat robot.toml && grep -rn -i "price" openspec/specs/shop --include=*.md | head -60`*

```
openspec/specs/shop:
authentication
cart
catalogue
checkout
interpretation-rules
product-detail
search

resources:
api.resource
catalogue.resource
... (68 more lines)
```

**Agent:**

The spec is WEB-002_AC-8. I'll read the catalogue spec and interpretation rules, check the shop is up, and check that the REPL is available.

*The agent runs `sed -n 1,95p openspec/specs/shop/catalogue/spec.md && echo ---- && uv run --no-sync python -m shop status; echo ---- && uv run --no-sync robotcode repl --help | head -40`*

*The agent reads `<repo>/openspec/specs/shop/interpretation-rules/spec.md`*

```
# shop/catalogue Specification

## Purpose
Describes the products page, `/products`, as a shopper experiences it: the product grid, its filters, the collection previews and the highlights.

## Requirements

### Requirement: Full product grid (WEB-002_AC-1)
When a shopper opens `/products` and the page finishes loading, the page SHALL display all 12 seeded products in a grid. Each product card SHALL show the product's name, its image, its price - the pro

#### Scenario: Opening the products page
- **WHEN** a shopper opens `/products`
... (128 more lines)
```

**Agent:**

The shop is running locally (v0.3.0). Before starting the REPL I'll check the rest of its options and whether this WSL session has a display for a visible browser.

*The agent runs `uv run --no-sync robotcode repl --help | sed -n 40,200p; echo "DISPLAY=$DISPLAY WAYLAND=$WAYLAND_DISPLAY"`*

```
                                  imported. See `robot --pythonpath` option.
  -k, --show-keywords             Executed keywords will be shown in the
                                  output.
  -i, --inspect                   Activate inspection mode. This forces a
                                  prompt to appear after the REPL script is
                                  executed.
  -d, --outputdir DIR             Where to create output files. See `robot
                                  --outputdir` option.
  -o, --output FILE               XML output file. See `robot --output`
                                  option.
  -r, --report FILE               HTML output file. See `robot --report`
                                  option.
... (41 more lines)
```

*The agent runs `S=<scratch> mkdir -p $S && : > $S/cmds.txt && : > $S/out.log && echo ok`*

```
ok
```

*The agent runs `S=<scratch> cd <repo> && tail -n +1 -f $S/cmds.txt | uv run --no-sync robotcode repl --plain --no-history -k -v HEADLESS:False -d $S/results > $S/out.log 2>&1`*

```
Command running in background with ID: b3gi419pd. Output is being written to: <scratch>
Session cwd remains <repo>; directory changes made by the backgrounded command d
```

*The agent runs `S=<scratch> timeout 30 bash -c "until [ -s $S/out.log ]; do sleep 0.5; done"; cat $S/out.log`*

```
(Bash completed with no output)
```

**Agent:**

The REPL printed nothing yet (the plain prompt may be buffered). I'll send the first statements: import the shop resource and check that `${SHOP_URL}` resolved from the project config.

*The agent runs `S=<scratch> printf '%s\n' 'Import Resource    ${EXECDIR}/resources/shop.resource' 'Log To Console    URL=${SHOP_URL} HEADLESS=${HEADLESS}' >> $S/cmds.txt; timeout 40 bash -c "until grep -q 'URL=' $S/out.log; do sleep 0.5; done"; cat $S/out.log`*

```
KEYWORD BuiltIn.Import Resource  ${EXECDIR}/resources/shop.resource
KEYWORD BuiltIn.Log To Console  URL=${SHOP_URL} HEADLESS=${HEADLESS}
URL=http://localhost:9090 HEADLESS=True
```

*The agent runs `S=<scratch> printf '%s\n' 'Set Global Variable    ${HEADLESS}    ${False}' 'Open Shop Browser' 'Start Shop Test' 'Import Resource    ${EXECDIR}/resources/catalogue.resource' 'Go To Catalogue' 'Log To Console    STEP1 done HEADLESS=${HEADLESS}' >> $S/cmds.txt; timeout 90 bash -c "until grep -q 'STEP1 done' $S/out.log; do sleep 0.5; done"; tail -n +4 $S/out.log`*

```
KEYWORD BuiltIn.Set Global Variable  ${HEADLESS}  ${False}
  [ INFO ] ${HEADLESS} = False
KEYWORD shop.Open Shop Browser  
  KEYWORD Browser.New Browser  chromium  headless=${HEADLESS}
    [ INFO ] {"browser": "chromium", "headless": false, "chromiumSandbox": false, "devtools": false, "handleSIGHUP": true, "handleSIGINT": true, "handleSIGTERM": true, "slowMo": 0.0, "timeout": 30000.
    [ FAIL ] FileNotFoundError: [Errno 2] No such file or directory: '<scratch>
KEYWORD shop.Start Shop Test  
<repo>/.venv/lib/python3.12/site-packages/robot/result/modeldeprecation.py:24: U
  warnings.warn(
<repo>/.venv/lib/python3.12/site-packages/robot/result/modeldeprecation.py:24: U
  warnings.warn(
<repo>/.venv/lib/python3.12/site-packages/robot/result/modeldeprecation.py:24: U
... (38 more lines)
```

*The agent uses `ToolSearch` with `{"query": "select:TaskStop", "max_results": 1}`*

*The agent uses `TaskStop` with `{"task_id": "b3gi419pd"}`*

```
{"message":"Successfully stopped task: b3gi419pd (S=<scratch> cd <scratch>
```

*The agent runs `S=<scratch> pkill -f "robotcode repl --plain" ; pkill -f "tail -n +1 -f $S/cmds.txt"; mkdir -p $S/results && : > $S/cmds.txt && : > $S/out.log && pgrep -fa "robotcode repl" || echo "no repl left"`*

```
Exit code 144
```

**Agent:**

That `pkill` pattern also matched the shell running it (exit 144), so I'll check what's left and reset the files separately.

*The agent runs `pgrep -fa "robotcode repl|cmds.txt|playwright" | grep -v pgrep || echo "none running"`*

```
2162248 <repo>/.venv/lib/python3.12/site-packages/Browser/wrapper/node_modules/playwright-core/.local-browsers/chromium_headless_shell-1243/chrome-headless-shel
2162250 <repo>/.venv/lib/python3.12/site-packages/Browser/wrapper/node_modules/playwright-core/.local-browsers/chromium_headless_shell-1243/chrome-headless-shel
2162251 <repo>/.venv/lib/python3.12/site-packages/Browser/wrapper/node_modules/playwright-core/.local-browsers/chromium_headless_shell-1243/chrome-headless-shel
2162264 <repo>/.venv/lib/python3.12/site-packages/Browser/wrapper/node_modules/playwright-core/.local-browsers/chromium_headless_shell-1243/chrome-headless-shel
2162268 <repo>/.venv/lib/python3.12/site-packages/Browser/wrapper/node_modules/playwright-core/.local-browsers/chromium_headless_shell-1243/chrome-headless-shel
2162680 <repo>/.venv/lib/python3.12/site-packages/Browser/wrapper/node_modules/playwright-core/.local-browsers/chromium_headless_shell-1243/chrome-headless-shel
2164041 <repo>/.venv/lib/python3.12/site-packages/Browser/wrapper/node_modules/playwright-core/.local-browsers/chromium_headless_shell-1243/chrome-headless-shel
2164043 <repo>/.venv/lib/python3.12/site-packages/Browser/wrapper/node_modules/playwright-core/.local-browsers/chromium_headless_shell-1243/chrome-headless-shel
2164044 <repo>/.venv/lib/python3.12/site-packages/Browser/wrapper/node_modules/playwright-core/.local-browsers/chromium_headless_shell-1243/chrome-headless-shel
2164060 <repo>/.venv/lib/python3.12/site-packages/Browser/wrapper/node_modules/playwright-core/.local-browsers/chromium_headless_shell-1243/chrome-headless-shel
2164062 <repo>/.venv/lib/python3.12/site-packages/Browser/wrapper/node_modules/playwright-core/.local-browsers/chromium_headless_shell-1243/chrome-headless-shel
2164357 <repo>/.venv/lib/python3.12/site-packages/Browser/wrapper/node_modules/playwright-core/.local-browsers/chromium_headless_shell-1243/chrome-headless-shel
... (12 more lines)
```

**Agent:**

No REPL of mine is left. The headless Chromium processes belong to other environments, so I'm leaving them alone. Restarting with the output directory in place:

*The agent runs `S=<scratch> mkdir -p $S/results && : > $S/cmds.txt && : > $S/out.log && ls $S`*

```
cmds.txt
out.log
results
```

*The agent runs `S=<scratch> cd <repo> && tail -n +1 -f $S/cmds.txt | uv run --no-sync robotcode repl --plain --no-history -k -d $S/results > $S/out.log 2>&1`*

```
Command running in background with ID: bo9448nbx. Output is being written to: <scratch>
Session cwd remains <repo>; directory changes made by the backgrounded command d
```

*The agent runs `S=<scratch> printf '%s\n' 'Import Resource    ${EXECDIR}/resources/shop.resource' 'Import Resource    ${EXECDIR}/resources/catalogue.resource' 'Set Global Variable    ${HEADLESS}    ${False}' 'Open Shop Browser' 'Start Shop Test' 'Go To Catalogue' 'Log To Console    STEP1 done HEADLESS=${HEADLESS}' >> $S/cmds.txt; timeout 90 bash -c "until grep -q 'STEP1 done' $S/out.log; do sleep 0.5; done"; grep -v -e 'warnings.warn' -e 'UserWarning' $S/out.log | grep -E 'KEYWORD|FAIL|STEP1|headless'`*

```
KEYWORD BuiltIn.Import Resource  ${EXECDIR}/resources/shop.resource
KEYWORD BuiltIn.Import Resource  ${EXECDIR}/resources/catalogue.resource
KEYWORD BuiltIn.Set Global Variable  ${HEADLESS}  ${False}
KEYWORD shop.Open Shop Browser  
  KEYWORD Browser.New Browser  chromium  headless=${HEADLESS}
    [ INFO ] {"browser": "chromium", "headless": false, "chromiumSandbox": false, "devtools": false, "handleSIGHUP": true, "handleSIGINT": true, "handleSIGTERM": true, "slowMo": 0.0, "timeout": 30000.
    [ INFO ] Successfully created browser with options: {"browser":"chromium","headless":false,"chromiumSandbox":false,"devtools":false,"handleSIGHUP":true,"handleSIGINT":true,"handleSIGTERM":true,"sl
KEYWORD shop.Start Shop Test  
  KEYWORD None.  
    KEYWORD None."${SHOP_SPACE}"  
      KEYWORD BuiltIn.Create Dictionary  X-Workshop-Space=${SHOP_SPACE}
      KEYWORD Browser.New Context  baseURL=${SHOP_URL}  extraHTTPHeaders=${headers}
... (9 more lines)
```

*The agent runs `S=<scratch> printf '%s\n' '${html}=    Get Property    ${FILTERS} >> role=group[name="Price range"]    outerHTML' 'Log To Console    HTML>>${html}<<END' '${n}=    Get Grid Card Count' '${vals}=    Get Price Range Values' 'Log To Console    STEP2 cards=${n} values=${vals}' >> $S/cmds.txt; timeout 60 bash -c "until grep -q 'STEP2 cards' $S/out.log; do sleep 0.5; done"; sed -n '/HTML>>/,/<<END/p' $S/out.log; grep -E 'STEP2|FAIL' $S/out.log`*

```
KEYWORD BuiltIn.Log To Console  HTML>>${html}<<END
HTML>><fieldset class="filter-group">
        <legend>Price range</legend>
        
        <div class="price-filter">
          <div class="price-filter__values">
            <span>$<output for="price-min-range">39.50</output></span>
            <span>$<output for="price-max-range">899.00</output></span>
          </div>
          <div class="price-filter__sliders">
            <input type="range" id="price-min-range" aria-label="Minimum price" min="39.50" max="899.00" value="39.50" step="any">
            <input type="range" id="price-max-range" aria-label="Maximum price" min="39.50" max="899.00" value="899.00" step="any">
... (7 more lines)
```

*The agent runs `S=<scratch> printf '%s\n' 'Fill Text    ${FILTERS} >> role=slider[name="Minimum price"]    100' 'Fill Text    ${FILTERS} >> role=slider[name="Maximum price"]    300' '${vals}=    Get Price Range Values' '${hmin}=    Get Attribute    ${FILTERS} >> input[name="price_min"]    value' '${hmax}=    Get Property    ${FILTERS} >> input[name="price_max"]    value' '${smin}=    Get Property    ${FILTERS} >> role=slider[name="Minimum price"]    value' '${smax}=    Get Property    ${FILTERS} >> role=slider[name="Maximum price"]    value' 'Log To Console    STEP3 shown=${vals} sliders=${smin}/${smax} hidden=${hmin}/${hmax}' >> $S/cmds.txt; timeout 60 bash -c "until grep -q 'STEP3 shown' $S/out.log; do sleep 0.5; done"; sed -n '/STEP2 cards/,$p' $S/out.log | grep -E 'Fill Text|FAIL|STEP3|Error'`*

```
KEYWORD Browser.Fill Text  ${FILTERS} >> role=slider[name="Minimum price"]  100
KEYWORD Browser.Fill Text  ${FILTERS} >> role=slider[name="Maximum price"]  300
KEYWORD BuiltIn.Log To Console  STEP3 shown=${vals} sliders=${smin}/${smax} hidden=${hmin}/${hmax}
STEP3 shown=['100.00', '300.00'] sliders=100/300 hidden=100.00/300.00
```

*The agent runs `S=<scratch> printf '%s\n' 'Apply Filters' '${url}=    Get Url' '${n}=    Get Grid Card Count' '${names}=    Get Grid Card Names' '${prices}=    Get Texts    ${GRID} >> article >> ${CARD PRICE}' '${vals}=    Get Price Range Values' 'Log To Console    STEP4 url=${url} cards=${n} names=${names} prices=${prices} shown=${vals}' >> $S/cmds.txt; timeout 60 bash -c "until grep -q 'STEP4 url' $S/out.log; do sleep 0.5; done"; sed -n '/STEP3 shown/,$p' $S/out.log | grep -E 'Apply Filters|FAIL|STEP4|Error'`*

```
KEYWORD catalogue.Apply Filters  
KEYWORD BuiltIn.Log To Console  STEP4 url=${url} cards=${n} names=${names} prices=${prices} shown=${vals}
STEP4 url=http://localhost:9090/products?price_min=100.00&price_max=300.00 cards=6 names=['Aurora Neural Headphones', 'Echo Conference Speaker', 'Nimbus Desk Light', 'Pulse Bio Ring', 'Summit Trail Sh
```

*The agent runs `grep -n -i -E "products|Keyword|^\S" resources/api.resource | head -40; curl -s http://localhost:9090/api/products | python3 -c "import sys,json; d=json.load(sys.stdin); d=d.get('products',d) if isinstance(d,dict) else d; [print(p.get('id'), p.get('price'), p.get('name')) for p in sorted(d,key=lambda p:p['price'])]"`*

```
Exit code 1
1:*** Settings ***
2:Documentation       The shop's API, in the configured workshop space.
4:Library             Collections
5:Library             RequestsLibrary
8:*** Keywords ***
9:Open Shop API
17:Get Shop Health
22:Get Catalogue From API
23:    [Documentation]    Every product, as dictionaries, from ``GET /api/products/``.
24:    ${response}=    GET On Session    shop    /api/products/    expected_status=200
pyenv: version `3.12' is not installed (set by <repo>/.python-version)
```

*The agent runs `sed -n 8,40p resources/api.resource; curl -sL http://localhost:9090/api/products/ | uv run --no-sync python -c "import sys,json; d=json.load(sys.stdin); d=d.get('products',d) if isinstance(d,dict) else d; [print(p.get('id'), p.get('price'), p.get('name'), p.get('category')) for p in sorted(d,key=lambda p:p['price'])]"`*

```
Exit code 1
*** Keywords ***
Open Shop API
    [Documentation]    Creates the API session. It sends ${SHOP_SPACE} when one is set.
    &{headers}=    Create Dictionary
    IF    "${SHOP_SPACE}"
        Set To Dictionary    ${headers}    X-Workshop-Space=${SHOP_SPACE}
    END
    Create Session    shop    ${SHOP_URL}    headers=${headers}

Get Shop Health
    [Documentation]    The body of ``GET /health``.
... (11 more lines)
```

*The agent runs `S=<scratch> printf '%s\n' 'Import Resource    ${EXECDIR}/resources/api.resource' 'Open Shop API' '@{all}=    Get Catalogue From API' '${sorted}=    Evaluate    sorted(((p["price"], p["name"]) for p in $all))' 'Log To Console    STEP5 all=${sorted}' '${expected}=    Evaluate    sorted(p["name"] for p in $all if 100 <= p["price"] <= 300)' '${names}=    Get Grid Card Names' '${actual}=    Evaluate    sorted($names)' 'Log To Console    STEP6 expected=${expected} actual=${actual} equal=${{ $expected == $actual }}' >> $S/cmds.txt; timeout 60 bash -c "until grep -q 'STEP6 expected' $S/out.log; do sleep 0.5; done"; sed -n '/STEP4 url/,$p' $S/out.log | grep -E 'FAIL|STEP5|STEP6|Error'`*

```
KEYWORD BuiltIn.Log To Console  STEP5 all=${sorted}
STEP5 all=[(39.5, 'Insight Smart Notebook'), (59.0, 'Focus Loop Timer'), (79.0, 'Cascade Water Bottle'), (129.0, 'Nimbus Desk Light'), (149.0, 'Summit Trail Shoes'), (169.0, 'Velocity Travel Backpack'
KEYWORD BuiltIn.Log To Console  STEP6 expected=${expected} actual=${actual} equal=${{ $expected == $actual }}
STEP6 expected=['Aurora Neural Headphones', 'Echo Conference Speaker', 'Nimbus Desk Light', 'Pulse Bio Ring', 'Summit Trail Shoes', 'Velocity Travel Backpack'] actual=['Aurora Neural Headphones', 'Ech
```

*The agent runs `cat tests/ui/catalogue.robot; echo ----DIFF; git diff --stat; git diff resources/catalogue.resource tests/ui/catalogue.robot | head -80`*

```
*** Settings ***
Documentation       The products page, /products (spec: shop/catalogue).

Resource            resources/shop.resource
Resource            resources/api.resource
Resource            resources/catalogue.resource
Resource            resources/legacy.resource

Suite Setup         Run Keywords    Open Shop Browser    AND    Open Shop API
Suite Teardown      Close Browser
Test Setup          Start Shop Test

... (130 more lines)
```

*The agent runs `uv run --no-sync robotcode libdoc resources/legacy.resource list 2>&1 | tail -20; grep -n -A6 -E "^Get Card Prices|^Get Grid Cards" resources/legacy.resource`*

```
Fill Checkout Form By Field Ids
Get Card Prices
Get Grid Cards
Get Order Total
Get Product Grid
18:Get Card Prices
19-    [Documentation]    The price of every grid card, in page order.
20-    ${grid}=    Get Product Grid
21-    @{prices}=    Get Texts    ${grid} >> article >> ${CARD PRICE}
22-    RETURN    ${prices}
23-
24:Get Grid Cards
... (6 more lines)
```

**Agent:**

Status: the exploration is done and the filter behaves as specified. I'm checking the last detail, which locator the legacy grid keyword uses, before I write up the recommendation.

*The agent runs `grep -n -B2 -A6 -E "^Get Product Grid" resources/legacy.resource`*

```
11-
12-*** Keywords ***
13:Get Product Grid
14-    [Documentation]    The element that holds the product cards of the grid.
15-    ${grid}=    Get Element    ${GRID} >> .product-grid
16-    RETURN    ${grid}
17-
18-Get Card Prices
19-    [Documentation]    The price of every grid card, in page order.
```

*The agent runs `S=<scratch> printf '%s\n' 'Close Browser' 'Log To Console    STEP7 closed' >> $S/cmds.txt; timeout 30 bash -c "until grep -q 'STEP7 closed' $S/out.log; do sleep 0.5; done"; sed -n '/STEP6 expected/,$p' $S/out.log | grep -E 'Close Browser|FAIL|STEP7'`*

```
KEYWORD Browser.Close Browser  
KEYWORD BuiltIn.Log To Console  STEP7 closed
STEP7 closed
```

*The agent uses `TaskStop` with `{"task_id": "bo9448nbx"}`*

```
{"message":"Successfully stopped task: bo9448nbx (S=<scratch> cd <scratch>
```

**Agent:**

I opened `/products` in a visible Chromium from the RobotCode REPL, using `resources/shop.resource`. Setting the range to $100–$300 and clicking "Apply filters" works: the grid drops from 12 cards to 6, and every card is priced between $100 and $300. This is criterion **WEB-002_AC-8**. I wrote no files in the repo.

## What happened
- **Opening the page:** `Open Shop Browser`, `Start Shop Test`, then `Go To Catalogue` from `catalogue.resource`. The grid showed 12 cards and the range read `39.50` to `899.00`.
- **The sliders:** they are two `<input type="range">` elements with accessible names "Minimum price" and "Maximum price". The values shown above them are `<output>` elements, which is what the existing `Get Price Range Values` reads.
- **Setting the range:** `Fill Text` with `100` and `300` works on these sliders. The shown values changed to `100.00` / `300.00`, so the page's own handlers ran.
- **After "Apply filters":** the URL became `/products?price_min=100.00&price_max=300.00` and the range still showed `100.00` / `300.00`. The 6 cards were Aurora Neural Headphones ($249.99), Echo Conference Speaker ($219.00), Nimbus Desk Light ($129.00), Pulse Bio Ring ($189.00), Summit Trail Shoes ($149.00) and Velocity Travel Backpack ($169.00).
- **Checked against the API:** `Get Catalogue From API` filtered to 100–300 gives exactly the same 6 names.

## Keywords that already fit
| Step | Keyword |
|---|---|
| Open the page | `Go To Catalogue` |
| Apply | `Apply Filters` (clicks `${FILTERS} >> role=button[name="Apply filters"]`) |
| Check the shown range | `Get Price Range Values` returns `['100.00', '300.00']` after applying |
| Card names | `Get Grid Card Names` |

The suite setup already runs `Open Shop Browser` and `Open Shop API`, and each test starts with `Start Shop Test`.

## Two keywords to add to `resources/catalogue.resource`
Both use locators I tried in the REPL:

```robotframework
Set Price Range
    [Documentation]    Moves the price sliders to ``minimum`` and ``maximum``.
    [Arguments]    ${minimum}    ${maximum}
    Fill Text    ${FILTERS} >> role=slider[name="Minimum price"]    ${minimum}
    Fill Text    ${FILTERS} >> role=slider[name="Maximum price"]    ${maximum}

Get Grid Card Prices
    [Documentation]    The prices of the grid cards, in page order.
    @{prices}=    Get Texts    ${GRID} >> article >> ${CARD PRICE}
    RETURN    ${prices}
```

- **Don't reuse `Get Card Prices` or `Get Grid Cards`:** the suite already uses them, but they come from `legacy.resource` and find the grid through the `.product-grid` class. That's the deliberate deviation Module 8 heals. `${GRID} >> article >> ${CARD PRICE}` returned exactly one price per card (6 of 6).
- **Don't use the hidden `input[name="price_min"]` / `input[name="price_max"]` fields:** they follow the sliders, but they're implementation details. Assert through the sliders' names and the shown values.

## What to assert
The spec's scenario says "every product in the grid is priced from $100.00 to $300.00 inclusive". So the test should check that the grid isn't empty and that each price, as a number (for example `${{ float($p.lstrip("$").replace(",", "")) }}`), is between 100 and 300. Comparing names with the API also passed, but it checks more than AC-8 says.

## Caveats
- **The bounds aren't tested:** no seeded product costs exactly $100 or $300 (the nearest are $79.00 and $389.00). A pass with this data doesn't prove the bounds are inclusive.
- **Passing `-v HEADLESS:False` to `robotcode repl` didn't work:** importing `shop.resource` set it back to `True`, so I ran `Set Global Variable    ${HEADLESS}    ${False}` before `Open Shop Browser`. I didn't check whether `-v` has the same problem in a normal `robotcode robot` run.

The browser is closed and the REPL session has ended.

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
