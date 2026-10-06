# Lab 8 - Healing: the recorded walkthrough

*Recorded with Claude Code 2.1.281, with a healing model configured, from the lab's instructions. Results are shortened; your agent's answers will differ in wording.*

*The rehearsal had a healing model configured in `.env` (`HEAL_MODEL`, `HEAL_BASE_URL`, `HEAL_API_KEY`).*

## Step 1 - Let the layout drift

**The participant runs** `uv run --no-sync python -m shop preset drift_and_bug`:

```
applied preset drift_and_bug in space default
```

## Step 2 - Run the suite as it is

**The participant runs** `uv run robotcode robot --exclude broken`:

```
------------------------------------------------------------------------------
Tests.Ui.Product Detail :: A product's detail page, /products/{id}... | PASS |
6 tests, 6 passed, 0 failed
==============================================================================
Tests.Ui.Search :: Product search on the home page and the products page (s...
==============================================================================
WEB-004_AC-1 Home Page Hero Shows Search Input :: The first screen... | PASS |
------------------------------------------------------------------------------
WEB-004_AC-3 Enter Shows Matching Results :: Searching "headphones... | PASS |
------------------------------------------------------------------------------
WEB-004_AC-3 Search Button Shows Matching Results :: Searching "he... | PASS |
------------------------------------------------------------------------------
... (18 more lines)
```

**The participant runs** `uv run robotcode results show --failed`:

```
# Show — results/output.xml

- ❌ **FAIL** Tests.Ui.Catalogue.WEB-002_AC-1 Card Prices Are The Product Prices (`tests/ui/catalogue.robot:26`) _(12:10:00 · 10.50 s)_
  > TimeoutError: locator.waitFor: Timeout 10000ms exceeded.
- ❌ **FAIL** Tests.Ui.Catalogue.WEB-002_AC-7 Audio Filter Shows Only Audio (`tests/ui/catalogue.robot:51`) _(12:10:12 · 12.29 s)_
  > TimeoutError: locator.waitFor: Timeout 10000ms exceeded.
- ❌ **FAIL** Tests.Ui.Checkout.WEB-006_AC-1 Order Total Adds Up (`tests/ui/checkout.robot:17`) _(12:10:27 · 10.43 s)_
  > TimeoutError: locator.evaluate: Timeout 10000ms exceeded.
- ❌ **FAIL** Tests.Ui.Checkout.WEB-006_AC-7 Successful Order (`tests/ui/checkout.robot:27`) _(12:10:38 · 10.36 s)_
  > TimeoutError: locator.fill: Timeout 10000ms exceeded.

## Statistics
... (10 more lines)
```

## Step 3 - Run it again with healing

**The participant runs** `git status --short -- tests resources > /tmp/before-heal.txt; uv run robotcode -p heal robot --exclude broken`:

```
------------------------------------------------------------------------------
Tests.Ui.Product Detail :: A product's detail page, /products/{id}... | PASS |
6 tests, 6 passed, 0 failed
==============================================================================
Tests.Ui.Search :: Product search on the home page and the products page (s...
==============================================================================
WEB-004_AC-1 Home Page Hero Shows Search Input :: The first screen... | PASS |
------------------------------------------------------------------------------
WEB-004_AC-3 Enter Shows Matching Results :: Searching "headphones... | PASS |
------------------------------------------------------------------------------
WEB-004_AC-3 Search Button Shows Matching Results :: Searching "he... | PASS |
------------------------------------------------------------------------------
... (28 more lines)
```

## Step 4 - Triage every heal

*In the lab you triage the heals yourself. The rehearsal has the agent draft a triage, so that the walkthrough shows the questions to ask.*

**Prompt:**

> Read results/heal/events.jsonl, which the healing run wrote, and triage every heal in it: accept, reject or investigate, with one sentence of reason each. Judge whether the new locator finds the element the step meant, and whether it uses the stable contract of docs/conventions.md or something that will drift again. Then list the tests that still failed with healing on, and say for each whether its locator healed and why it still fails. Do not change any file.

*The agent runs `ls -la results/heal/ && wc -l results/heal/events.jsonl && cat docs/conventions.md`*

```
total 180
drwxr-xr-x  4 user user  4096 Sep 25 12:13 .
drwxr-xr-x 12 user user  4096 Sep 25 12:11 ..
drwxr-xr-x  2 user user  4096 Sep 25 12:13 diffs
-rw-r--r--  1 user user 61667 Sep 25 12:13 events.jsonl
-rw-r--r--  1 user user 80533 Sep 25 12:13 heal_report.html
drwxr-xr-x  3 user user  4096 Sep 25 12:13 healed_files
-rw-r--r--  1 user user 16384 Sep 25 12:13 history.sqlite
-rw-r--r--  1 user user   411 Sep 25 12:13 summary.json
5 results/heal/events.jsonl
# Test conventions

... (72 more lines)
```

*The agent reads `<repo>/docs/agent-environment.md`*

*The agent runs `cat results/heal/summary.json; echo; python3 -c "
import json
for i,l in enumerate(open('results/heal/events.jsonl')):
    d=json.loads(l)
    print('=== line',i, type(d).__name__, list(d.keys()) if isinstance(d,dict) else len(d))
"`*

```
Exit code 1
{
  "transactions": 5,
  "healed": 5,
  "unhealed": 0,
  "suppressed": 0,
  "by_failure_class": {
    "locator-drift": 5
  },
  "affected_files": [
    "<repo>/resources/legacy.resource"
  ],
... (8 more lines)
```

*The agent runs `uv run --no-sync python -c "
import json
for i,l in enumerate(open('results/heal/events.jsonl')):
    d=json.loads(l)
    def walk(o,p='',depth=0):
        if isinstance(o,dict):
            for k,v in o.items():
                walk(v,p+'.'+k,depth+1)
        elif isinstance(o,list):
            print(p,'[list len',len(o),']')
            for j,v in enumerate(o[:3]):
                walk(v,p+f'[{j}]',depth+1)
        else:
            s=repr(o)
            print(p,'=',s[:300]+('...' if len(s)>300 else ''))
    print('=== line',i)
    walk(d)
"`*

```
=== line 0
.event_id = 'heal-1'
.timestamp = '2026-09-25T10:11:55.625965Z'
.test_name = 'WEB-002_AC-1 Card Prices Are The Product Prices'
.suite_name = 'Tests.Ui.Catalogue'
.source = '<repo>/resources/legacy.resource'
.lineno = 15
.keyword.name = 'Get Element'
.keyword.args [list len 1 ]
.keyword.args[0] = 'section:has(h2:text-is("All products")):not(:has(section)) >> .product-grid'
.keyword.owner_library = 'Browser'
.keyword.assign [list len 1 ]
... (319 more lines)
```

*The agent runs `uv run --no-sync python -c "
import json
for i,l in enumerate(open('results/heal/events.jsonl')):
    d=json.loads(l)
    print('=== ',d['event_id'], d['test_name'])
    print(d['context']['evidence']['dom-excerpt']['excerpt'])
    print('--- attempts detail')
    for a in d['outcome']['attempts']:
        print(a['detail'])
"`*

```
<persisted-output>
Output too large (42.7KB). Full output saved to: ~/.claude/projects/-tmp-claude-1000--mnt-c-workspace-ai-engineering-robotframework-6fe17ce9-00bd-4179-bc22-dbf725b60a81-scratchpad-rehearsal-

Preview (first 2KB):
===  heal-1 WEB-002_AC-1 Card Prices Are The Product Prices
<body class="site">
<a>Skip to main content</a>
<header class="site-header">
<a>
<span class="brand-mark">

</span>
... (82 more lines)
```

*The agent reads `~/.claude/projects/-tmp-claude-1000--mnt-c-workspace-ai-engineering-robotframework-6fe17ce9-00bd-4179-bc22-dbf725b60a81-scratchpad-rehearsal-repo/4dc550e3-4737-445c-9fc3-12be7a5eeac3/tool-results/bwt0zv1dy.txt`*

*The agent runs `cat -n resources/legacy.resource; echo ----; ls -R results/heal/diffs results/heal/healed_files | head -30; echo ----; ls -la results/; git status --short resources/legacy.resource`*

```
     1	*** Settings ***
     2	Documentation       Legacy locators, kept deliberately; see docs/conventions.md.
     3	...
     4	...                 These keywords find elements by id, class or data-test hook instead of
     5	...                 the shop's stable contract. Each such locator names exactly one element.
     6	
     7	Library             Browser
     8	Resource            catalogue.resource
     9	Resource            checkout.resource
    10	
    11	
    12	*** Keywords ***
... (58 more lines)
```

*The agent loads the skill `robotcode:robotcode`*

*The agent runs `cat ~/.claude/plugins/cache/robotframework-agent-plugins/robotcode/7c753f8adca1/skills/robotcode/references/results.md | head -150`*

```
# Interpreting test results — the `robotcode results` subcommands

`robotcode results` inspects a finished Robot Framework run — the `output.xml` / `output.json` it wrote — from the terminal. It reads the file **server-side** and returns only the slice you ask for: h

Reach for it whenever a run has finished and the question is "did it pass, what failed, why, or what changed?" — five subcommands (`summary`, `show`, `log`, `stats`, `diff`) cover those, detailed belo

> **Note**: RobotCode auto-detects non-interactive use and disables paging/colors automatically — no extra flags needed. (If a wrapper ever forces a pager, `--no-pager --no-color` before the subcomman

## Contents

1. The shared option surface across all five subcommands
2. `summary` — the headline
... (137 more lines)
```

*The agent runs `uv run --no-sync robotcode results summary --failed -o results/output.xml 2>&1 | tail -40`*

```
# Summary — results/output.xml

- _Status:_ ❌ **FAIL**
- _Total:_ 30
- _Passed:_ 28
- _Failed:_ 2
- _Skipped:_ 0
- _Started:_ 2026-09-25 12:11:00
- _Ended:_ 2026-09-25 12:13:08
- _Elapsed:_ 2 min 7.7 s
- _Messages:_ 7 FAIL

... (6 more lines)
```

*The agent runs `uv run --no-sync robotcode results log --failed -o results/output.xml 2>&1 | head -200`*

```
# Log

### Test: Tests.Ui.Catalogue.WEB-002_AC-1 Card Prices Are The Product Prices (`tests/ui/catalogue.robot:26`) ❌ **FAIL** _(12:11:06 · 49.99 s)_

> Cascade Water Bottle should cost $79.00.: $90.85 != $79.00

- **[SETUP]** **shop.Start Shop Test** ✅ **PASS** _(12:11:06 · 48 ms)_
  - **IF**
    - **IF** `"${SHOP_SPACE}"` ⏸ **NOT RUN** _(12:11:06 · 1 ms)_
      - `&{headers}` = **BuiltIn.Create Dictionary** `X-Workshop-Space=${SHOP_SPACE}` ⏸ **NOT RUN** _(12:11:06 · 0 ms)_
      - **Browser.New Context** `baseURL=${SHOP_URL}` `extraHTTPHeaders=${headers}` ⏸ **NOT RUN** _(12:11:06 · 0 ms)_
    - **ELSE** ✅ **PASS** _(12:11:06 · 6 ms)_
... (188 more lines)
```

**Agent:**

Status: both remaining failures are identified (the card price and the order total). I'm now checking the calling tests, the stable keywords and the spec criteria to judge each heal.

*The agent runs `cat -n tests/ui/checkout.robot; echo -----; cat -n resources/checkout.resource; echo -----; diff resources/legacy.resource results/heal/healed_files/resources/legacy.resource`*

```
     1	*** Settings ***
     2	Documentation       Checkout, /checkout (spec: shop/checkout).
     3	...                 Every test starts with Aurora Neural Headphones in its own cart.
     4	
     5	Resource            resources/shop.resource
     6	Resource            resources/checkout.resource
     7	Resource            resources/legacy.resource
     8	
     9	Suite Setup         Open Shop Browser
    10	Suite Teardown      Close Browser
    11	Test Setup          Start Checkout Test
    12	
... (163 more lines)
```

*The agent runs `cat -n tests/ui/catalogue.robot; echo -----; cat -n resources/catalogue.resource; echo ----; git diff --stat; git diff tests/ui/catalogue.robot resources/catalogue.resource`*

```
     1	*** Settings ***
     2	Documentation       The products page, /products (spec: shop/catalogue).
     3	
     4	Resource            resources/shop.resource
     5	Resource            resources/api.resource
     6	Resource            resources/catalogue.resource
     7	Resource            resources/legacy.resource
     8	
     9	Suite Setup         Run Keywords    Open Shop Browser    AND    Open Shop API
    10	Suite Teardown      Close Browser
    11	Test Setup          Start Shop Test
    12	
... (280 more lines)
```

*The agent runs `ls openspec/specs/shop/; grep -rn -B2 -A12 "WEB-002_AC-1\b" openspec/specs/shop/ | head -60; echo ======; grep -rn -B2 -A14 "WEB-006_AC-1\b" openspec/specs/shop/ | head -60`*

```
authentication
cart
catalogue
checkout
interpretation-rules
product-detail
search
openspec/specs/shop/catalogue/spec.md-6-## Requirements
openspec/specs/shop/catalogue/spec.md-7-
openspec/specs/shop/catalogue/spec.md:8:### Requirement: Full product grid (WEB-002_AC-1)
openspec/specs/shop/catalogue/spec.md-9-When a shopper opens `/products` and the page finishes loading, the page SHALL display all 12 seeded products in a grid. Each product card SHALL show the produc
openspec/specs/shop/catalogue/spec.md-10-
... (28 more lines)
```

*The agent runs `timeout 60 uv run --no-sync python -m shop status 2>&1 | head -40`*

```
shop     http://localhost:9090  (version 0.3.0)
space    default
presets  stage4, drift_and_bug
```

*The agent runs `uv run --no-sync robotcode results show -o results/output.xml 2>&1 | head -50; uv run --no-sync robotcode results log -o results/output.xml -t "WEB-002_AC-7*" --max-depth 3 2>&1 | grep -v "JavaScript executed\|States are\|Attribute is" | head -60`*

```
# Show — results/output.xml

- ✅ **PASS** Tests.Api.Smoke.Health Reports Ok (`tests/api/smoke.robot:12`) _(12:11:00 · 5 ms)_
- ✅ **PASS** Tests.Api.Smoke.Catalogue Lists Twelve Products (`tests/api/smoke.robot:16`) _(12:11:00 · 8 ms)_
- ✅ **PASS** Tests.Ui.Cart.WEB-005_AC-2 Cart Badge Counts Added Items (`tests/ui/cart.robot:17`) _(12:11:01 · 538 ms)_
- ✅ **PASS** Tests.Ui.Cart.WEB-005_AC-2 Cart Badge Shows In Mobile Menu (`tests/ui/cart.robot:26`) _(12:11:02 · 319 ms)_
- ✅ **PASS** Tests.Ui.Cart.WEB-005_AC-3 Cart Page Lists Name Quantity And Prices (`tests/ui/cart.robot:35`) _(12:11:02 · 1.32 s)_
- ✅ **PASS** Tests.Ui.Cart.WEB-005_AC-4 Cart Summary Shows Subtotal Shipping Tax And Total (`tests/ui/cart.robot:41`) _(12:11:03 · 1.49 s)_
- ✅ **PASS** Tests.Ui.Cart.WEB-005_AC-9 Adding Product Again Increments Quantity (`tests/ui/cart.robot:54`) _(12:11:05 · 561 ms)_
- ✅ **PASS** Tests.Ui.Catalogue.WEB-002_AC-1 Every Card Offers Add To Cart (`tests/ui/catalogue.robot:17`) _(12:11:05 · 213 ms)_
- ❌ **FAIL** Tests.Ui.Catalogue.WEB-002_AC-1 Card Prices Are The Product Prices (`tests/ui/catalogue.robot:26`) _(12:11:06 · 49.99 s)_
  > Cascade Water Bottle should cost $79.00.: $90.85 != $79.00
... (93 more lines)
```

*The agent runs `uv run --no-sync robotcode results log -o results/output.xml -t "WEB-002_AC-7*" 2>&1 | grep -n -A8 "legacy.Get Product Grid"; uv run --no-sync robotcode results log -o results/output.xml -t "WEB-006_AC-1*" 2>&1 | grep -v "JavaScript executed\|States are\|Attribute is" | grep -n -A25 "legacy.Get Order Total"`*

```
48:  - `${grid}` = **legacy.Get Product Grid** ✅ **PASS** _(12:11:59 · 19 ms)_
49-    - `${grid}` = **Browser.Get Element** `css=.catalog-content >> css=.tile-rack` ✅ **PASS** _(12:11:59 · 19 ms)_
50-      - `[INFO] heal: proactively replaced known-broken locator with 'css=.catalog-content >> css=.tile-rack' (from this run)`
51-      - `[INFO] Locator found successfully.`
52-      - `[INFO] ${grid} = css=.catalog-content >> css=.tile-rack`
53-    - **RETURN** `${grid}` ✅ **PASS** _(12:11:59 · 0 ms)_
54-    - `[INFO] ${grid} = css=.catalog-content >> css=.tile-rack`
55-  - `@{cards}` = **Browser.Get Elements** `${grid} >> article` ✅ **PASS** _(12:11:59 · 10 ms)_
56-    - `[INFO] Found 2 Locators successfully.`
97:- `${total}` = **legacy.Get Order Total** ✅ **PASS** _(12:12:02 · 15.06 s)_
98-  - `${text}` = **Browser.Get Text** `[data-test="checkout-total"]` ✅ **PASS** _(12:12:02 · 10.05 s)_
99-    - `[INFO] [![](file://<repo>/results/browser/screenshot/fail-screenshot-2
... (23 more lines)
```

**Agent:**

I triaged all five heals. Each new locator finds the element its step meant, which I checked against the page snapshot in each event and against the run log. None of them uses the stable contract from `docs/conventions.md`, so I'd **reject all five as fixes**. The locator drift is real and the heals were right at runtime, but the proposed replacements are CSS classes and ids, the same kind of locator that just drifted. The shop is running the `stage4, drift_and_bug` presets. I changed no files.

## Triage

| Heal | Step (`resources/legacy.resource`) | Old → healed | Verdict | Reason |
|---|---|---|---|---|
| heal-1 | `Get Product Grid` (line 15) | `${GRID} >> .product-grid` → `css=.catalog-content >> css=.tile-rack` | **Reject** | It finds the right grid (12 cards, 2 after the Audio filter), but it drops the `${GRID}` anchor on the "All products" heading, which still works, and uses two CSS classes instead; one of them, `.tile-rack`, is the class that just replaced `.product-grid`. |
| heal-2 | `Get Order Total` (line 32) | `[data-test="checkout-total"]` → `css=div.payment-totals__total` | **Reject** | It is the only total in the order summary and reads 249.99, but it swaps a `data-test` hook for a class name; the stable form finds the summary line by its visible "Total" text inside `role=complementary`, the way `Get Summary Amount` finds Subtotal, Shipping and Tax. |
| heal-3 | `Fill Checkout Form By Field Ids` (line 39) | `id=checkout-email` → `css=input#payment-email` | **Reject** | It is the checkout form's email field, not the sign-in dialog's `#account-email`, but it swaps one id for another: the ids just changed from `checkout-*` to `payment-*` and can change again, whereas `form[action="/checkout"] >> role=textbox[name="Email"]` is the contract. |
| heal-4 | same keyword (line 40) | `id=checkout-name` → `css=input#payment-name` | **Reject** | Right field, but the same id-for-id swap, where the stable locator is the "Full name" label inside the checkout form. |
| heal-5 | same keyword (line 41) | `id=checkout-address` → `css=textarea#payment-address` | **Reject** | Right field, but the same id-for-id swap, where the stable locator is the "Address" label inside the checkout form. |

Before acting on these:
- **heal-1 affects more than its event shows.** `WEB-002_AC-7 Audio Filter Shows Only Audio` also ran on it (the log says "proactively replaced known-broken locator … (from this run)"), but that test has no event of its own. The fix proposal says `blast_radius: local`, yet `Get Product Grid` has two callers. Before it found the grid, heal-1's first attempt suggested unrelated elements, such as category badges and the "Reset" link. So check the healer's suggestions before trusting them.
- **The proposed fixes can't be applied as written.** All five would write to `resources/legacy.resource`, which AGENTS.md says never to edit. The stable versions belong in the tests that call these keywords, and in the stable resource files:
  - **Checkout fields:** `Fill Checkout Form` in `checkout.resource` already fills the same three fields by label. It passed in WEB-006_AC-11 and AC-12 in this run.
  - **Product grid:** `${GRID}` alone is enough.
  - **Order total:** this needs a new keyword in `checkout.resource`.

## Tests still failing with healing on (28 passed, 2 failed)

1. **`WEB-002_AC-1 Card Prices Are The Product Prices`**
   - **Locator:** healed by heal-1, correctly. It read the 12 prices in the same order as the 12 names read through `${GRID}`.
   - **Why it still fails:** the shop has a real defect: `Cascade Water Bottle should cost $79.00.: $90.85 != $79.00`. The spec says each card shows the product's own price.
   - **Three more cards are wrong** in the page snapshot, all 15 % above the API price. The test stopped at the first mismatch, so it never reached them:
     - Pulse Bio Ring: $217.35 instead of $189.00
     - Summit Trail Shoes: $171.35 instead of $149.00
     - Velocity Travel Backpack: $194.35 instead of $169.00
2. **`WEB-006_AC-1 Order Total Adds Up`**
   - **Locator:** healed by heal-2, correctly. It read "Total due at payment $249.99".
   - **Why it still fails:** the shop has a real defect: `249.99 != 267.49`. The summary shows subtotal $249.99, shipping "Complimentary" (counted as 0) and tax $17.50, and the spec requires the total to be their sum. The shop leaves the tax out of the total.

Both failures come from the "bug" part of the `drift_and_bug` preset. Healing fixed the drift and rightly left these two tests failing. They should be reported as shop defects, not fixed by changing the tests or the spec.

## Step 5 - What stayed red

**The participant runs** `uv run robotcode results show --failed`:

```
# Show — results/output.xml

- ❌ **FAIL** Tests.Ui.Catalogue.WEB-002_AC-1 Card Prices Are The Product Prices (`tests/ui/catalogue.robot:26`) _(12:11:06 · 49.99 s)_
  > Cascade Water Bottle should cost $79.00.: $90.85 != $79.00
- ❌ **FAIL** Tests.Ui.Checkout.WEB-006_AC-1 Order Total Adds Up (`tests/ui/checkout.robot:17`) _(12:12:02 · 15.44 s)_
  > The order total should be subtotal plus shipping plus tax.: 249.99 != 267.49

## Statistics

- _Total:_ 2
- _Passed:_ 0
- _Failed:_ 2
... (6 more lines)
```

**The participant runs** `git status --short -- tests resources | diff /tmp/before-heal.txt - && echo 'no test file changed by the healing run'`:

```
no test file changed by the healing run
```

## Stretch - Repair a test with the agent

**Prompt:**

> The test "WEB-006_AC-7 Successful Order" fails under the current shop layout. Use the RobotCode debugger and the robotframework MCP server to find which locator drifted, and repair its keyword onto the stable contract of docs/conventions.md, so that it works in every layout. Explain the change, then make it.

**Agent:**

I'll start by reading the environment and conventions docs, as AGENTS.md requires.

*The agent reads `<repo>/docs/agent-environment.md`*

*The agent reads `<repo>/docs/conventions.md`*

**Agent:**

Now the RobotCode skill, since it's the source of truth for running and debugging here.

*The agent loads the skill `robotcode:robotcode`*

**Agent:**

I'll read the debugging reference, since I can't drive an interactive terminal and need the piped fallback.

*The agent reads `~/.claude/plugins/cache/robotframework-agent-plugins/robotcode/7c753f8adca1/skills/robotcode/references/debugging.md`*

*The agent runs `uv run --no-sync robotcode discover tests --search "WEB-006_AC-7" 2>&1 | tail -20; uv run --no-sync python -m shop status 2>&1 | tail -20`*

```
# Tests

- **Tests.Ui.Checkout.`WEB-006_AC-7` Successful Order** (`tests/ui/checkout.robot:27`)

## Statistics

- _Suites:_ 3
- _Suites with tests:_ 1
- _Tests:_ 1

_Filters: search=WEB-006_AC-7_

... (3 more lines)
```

**Agent:**

The shop is running locally with the `drift_and_bug` preset active. Let me read the test and see which keywords it uses.

*The agent reads `<repo>/tests/ui/checkout.robot`*

*The agent runs `ls resources/ tests/ tests/ui; cat robot.toml`*

```
resources/:
api.resource
cart.resource
catalogue.resource
checkout.resource
legacy.resource
product_detail.resource
search.resource
shop.resource

tests/:
api
... (36 more lines)
```

**Agent:**

The test calls `Fill Checkout Form By Field Ids`, which by its name looks like a legacy keyword. Let me read the three resources it imports.

*The agent reads `<repo>/resources/legacy.resource`*

*The agent reads `<repo>/resources/checkout.resource`*

*The agent reads `<repo>/resources/shop.resource`*

*The agent runs `ls openspec/specs/shop/; grep -n -B2 -A12 "AC-7" openspec/specs/shop/checkout/spec.md | head -60`*

```
authentication
cart
catalogue
checkout
interpretation-rules
product-detail
search
60-- **THEN** no error is shown for the address field
61-
62:### Requirement: Successful order (WEB-006_AC-7)
63-When every required field holds valid data, the cart contains at least one item, and the shopper submits the checkout form, an order SHALL be created and a success message SHALL be displayed. The m
64-
... (10 more lines)
```

*The agent runs `uv run --no-sync robotcode robot-debug --help 2>&1 | head -80`*

```
Usage: robotcode robot-debug [OPTIONS] [ROBOT_OPTIONS_AND_ARGS]...

  Run a real Robot Framework suite with the debugger attached (alias `run-
  debug`).

  Takes the same arguments as `robotcode robot`, but pauses at breakpoints so
  you can inspect and step through the run at a debug prompt.

Options:
  --no-history                    Don't load or save the persistent history
                                  file. In-session arrow-up recall still
                                  works, but nothing crosses session
... (58 more lines)
```

*The agent runs `printf '%s\n' \
'.where' \
'Get Element Count    id=checkout-email' \
'Get Element Count    id=checkout-name' \
'Get Element Count    id=checkout-address' \
'Get Element Count    form[action="/checkout"] >> role=textbox[name="Email"]' \
'Get Element Count    form[action="/checkout"] >> role=textbox[name="Full name"]' \
'Get Element Count    form[action="/checkout"] >> role=textbox[name="Address"]' \
'Get Attribute    form[action="/checkout"] >> role=textbox[name="Email"]    id' \
'Get Attribute    form[action="/checkout"] >> role=textbox[name="Full name"]    id' \
'Get Attribute    form[action="/checkout"] >> role=textbox[name="Address"]    id' \
'.abort' \
| timeout 300 uv run --no-sync robotcode robot-debug --plain --no-history -bl 'Tests.Ui.Checkout.WEB-006_AC-7 Successful Order' 2>&1 | tail -80`*

```
==============================================================================
Tests                                                                         
==============================================================================
Tests.Ui                                                                      
==============================================================================
Tests.Ui.Checkout :: Checkout, /checkout (spec: shop/checkout). Every test ...
==============================================================================
WEB-006_AC-7 Successful Order :: A valid order shows a confirmatio... 
* exception  Browser.Fill Text  (resources/legacy.resource:39)  — Keyword failed: TimeoutError: locator.fill: Timeout 10000ms exceeded.
Call log:
  - waiting for locator('id=checkout-email')
(rdb) > #0  Browser.Fill Text                       resources/legacy.resource:39
... (19 more lines)
```

*The agent runs `grep -rn --include=*.robot --include=*.resource --include=*.md "By Field Ids\|legacy.resource" . 2>/dev/null | grep -v "^./.claude/rf-agentskills-files\|^./.rf-agentskills" | head -30`*

```
AGENTS.md:27:- Never edit `resources/legacy.resource`.
tests/ui/checkout.robot:7:Resource            resources/legacy.resource
tests/ui/checkout.robot:29:    Fill Checkout Form By Field Ids    test@example.com    Test User    123 Test Street, City
tests/ui/catalogue.robot:7:Resource            resources/legacy.resource
openspec/specs/workshop/test-conventions/spec.md:23:Locators SHALL be built from the shop's stable contract: roles with accessible names, visible text, labels, form-field names and link targets. Ids, 
openspec/specs/workshop/test-conventions/spec.md:26:- **WHEN** a keyword for a new element is added outside the legacy resource
openspec/changes/archive/2026-09-25-add-search-ui-tests/proposal.md:31:- Nothing changes in the existing tests or keywords, in `resources/legacy.resource`, or in `openspec/specs/shop/`.
openspec/changes/archive/2026-09-25-add-cart-ui-tests/proposal.md:33:- Nothing changes in the existing tests or keywords, in `resources/legacy.resource`, or in `openspec/specs/shop/`.
openspec/changes/archive/2026-09-25-add-product-detail-ui-tests/tasks.md:54:  - `resources/legacy.resource` and `resources/catalogue.resource` are unchanged (`git diff` shows only the
docs/facilitator/suite-outcomes.md:17:Each fragile test reaches one kind of element through a legacy locator (`resources/legacy.resource`). It fails in
openspec/changes/archive/2026-09-24-baseline-suite/design.md:68:- `legacy.resource`: the id, class and `data-test` keywords, the documented deviation;
openspec/changes/archive/2026-09-24-baseline-suite/design.md:119:It states the seven conventions of `workshop/test-conventions` with one reason each, the stable-contract list from demo-webshop, and a 
... (16 more lines)
```

*The agent uses `ToolSearch` with `{"query": "select:mcp__robotframework__analyze_scenario,mcp__robotframework__execute_step,mcp__robotframework__get_session_state,mcp__robotframework__get_locato`*

*The agent calls `robotframework/analyze_scenario` with `{"scenario": "Browser Library: on the demo shop at http://localhost:9090, add Aurora Neural Headphones (product 1) to the cart from its product page, open /chec`*

```
{"success":true,"scenario":{"title":"Browser library: on the demo shop at http://localhost:9090, add aurora neural headphones (product 1) to the cart from its product page, open /checkout, fill the ch
```

**Agent:**

I'm using the robotframework MCP session to replay the repaired flow in the live shop before I edit.

*The agent calls `robotframework/execute_step` with `{"keyword": "New Browser", "arguments": ["chromium", "headless=True"], "session_id": "6b99d9a6-0b93-439c-8915-45e264b8b473"}`*

```
{"success":true,"step_id":"b58c909b-66ee-4046-85e3-1d60837ef28d","keyword":"New Browser","arguments":["chromium","headless=True"],"status":"pass","execution_time":0.721641,"output":"browser=5e229920-6
```

*The agent calls `robotframework/execute_step` with `{"keyword": "New Context", "arguments": ["baseURL=http://localhost:9090"], "session_id": "6b99d9a6-0b93-439c-8915-45e264b8b473"}`*

```
{"success":true,"step_id":"6f38200b-19bb-4464-8f7e-b7de449e1bbd","keyword":"New Context","arguments":["baseURL=http://localhost:9090"],"status":"pass","execution_time":0.022425,"output":"context=369e8
```

*The agent calls `robotframework/execute_step` with `{"keyword": "New Page", "arguments": ["http://localhost:9090/products/1"], "session_id": "6b99d9a6-0b93-439c-8915-45e264b8b473"}`*

```
{"success":true,"step_id":"1dafbb8c-587e-45d6-96e1-8bd105cbc24c","keyword":"New Page","arguments":["http://localhost:9090/products/1"],"status":"pass","execution_time":0.124336,"output":"{'page_id': '
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Click", "arguments": ["role=button[name=\"Add Aurora Neural Headphones to cart\"]"], "session_id": "6b99d9a6-0b93-439c-8915-45e264b8b473"}`*

```
{"success":true,"step_id":"52c19dfb-874c-4110-8666-ee3f21aaf3ab","keyword":"Click","arguments":["role=button[name=\"Add Aurora Neural Headphones to cart\"]"],"status":"pass","execution_time":0.772235,
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Get Text", "arguments": ["role=banner >> role=link[name=/^Cart/]", "matches", "\\d"], "session_id": "6b99d9a6-0b93-439c-8915-45e264b8b473", "timeou`*

*The agent calls `robotframework/execute_step` with `{"keyword": "Go To", "arguments": ["http://localhost:9090/checkout"], "session_id": "6b99d9a6-0b93-439c-8915-45e264b8b473"}`*

```
Step execution failed: Keyword execution failed: Text 'Cart\n1' (str) should match 'd' (str)
Step ID: 6f48d1a2-e1e0-4c9b-991c-a5cebbeff4ce
```

```
{"success":true,"step_id":"11873f94-a41f-4429-8851-481aacc21b3d","keyword":"Go To","arguments":["http://localhost:9090/checkout"],"status":"pass","execution_time":0.038025,"output":"200","assigned_var
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Fill Text", "arguments": ["form[action=\"/checkout\"] >> role=textbox[name=\"Email\"]", "test@example.com"], "session_id": "6b99d9a6-0b93-439c-8915`*

```
{"success":true,"step_id":"548fe59a-829d-4b0e-8430-2de73d65c575","keyword":"Fill Text","arguments":["form[action=\"/checkout\"] >> role=textbox[name=\"Email\"]","test@example.com"],"status":"pass","ex
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Fill Text", "arguments": ["form[action=\"/checkout\"] >> role=textbox[name=\"Full name\"]", "Test User"], "session_id": "6b99d9a6-0b93-439c-8915-45`*

```
{"success":true,"step_id":"c90446e1-cab1-48bd-826a-da6a79934c72","keyword":"Fill Text","arguments":["form[action=\"/checkout\"] >> role=textbox[name=\"Full name\"]","Test User"],"status":"pass","execu
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Fill Text", "arguments": ["form[action=\"/checkout\"] >> role=textbox[name=\"Address\"]", "123 Test Street, City"], "session_id": "6b99d9a6-0b93-43`*

```
{"success":true,"step_id":"b106c027-631c-4f0e-90a1-ec8bcda78af9","keyword":"Fill Text","arguments":["form[action=\"/checkout\"] >> role=textbox[name=\"Address\"]","123 Test Street, City"],"status":"pa
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Click", "arguments": ["form[action=\"/checkout\"] >> role=button[name=\"Place order\"]"], "session_id": "6b99d9a6-0b93-439c-8915-45e264b8b473"}`*

```
{"success":true,"step_id":"3c84b956-0a11-44cc-9dfd-b5d2508f9488","keyword":"Click","arguments":["form[action=\"/checkout\"] >> role=button[name=\"Place order\"]"],"status":"pass","execution_time":0.39
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Get Text", "arguments": ["role=main >> role=alert", "*=", "confirmed"], "session_id": "6b99d9a6-0b93-439c-8915-45e264b8b473", "assign_to": "message`*

```
{"success":true,"step_id":"64d1bb77-b97e-44a0-983d-00409d9afb88","keyword":"Get Text","arguments":["role=main >> role=alert","*=","confirmed"],"status":"pass","execution_time":0.04686,"output":"Order 
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Close Browser", "arguments": ["ALL"], "session_id": "6b99d9a6-0b93-439c-8915-45e264b8b473"}`*

```
{"success":true,"step_id":"736d891a-a5d9-468f-adf4-8530aa6a9c6c","keyword":"Close Browser","arguments":["ALL"],"status":"pass","execution_time":0.035015,"output":"OK","assigned_variables":{},"recorded
```

*The agent edits `<repo>/tests/ui/checkout.robot`*

```
The file <repo>/tests/ui/checkout.robot has been updated successfully. (file sta
```

*The agent runs `uv run --no-sync robotcode robot -bl 'Tests.Ui.Checkout.WEB-006_AC-7 Successful Order' 2>&1 | tail -12; echo "exit=$?"; uv run --no-sync robotcode analyze code tests/ui/checkout.robot 2>&1 | tail -5`*

```
Tests.Ui.Checkout :: Checkout, /checkout (spec: shop/checkout). Ev... | PASS |
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
... (2 more lines)
```

**Agent:**

`WEB-006_AC-7 Successful Order` passes again. I changed one line: the test now fills the checkout form by the fields' labels instead of their ids.

**Which locator drifted.** I ran the real test under the RobotCode debugger (`robot-debug -bl …`). It stopped in `Fill Text` at `resources/legacy.resource:39`, inside `Fill Checkout Form By Field Ids`, waiting for `id=checkout-email`. At that stop, in the live page:
- `id=checkout-email`, `id=checkout-name` and `id=checkout-address` each found 0 elements.
- The same fields found by label inside the checkout form each found exactly 1.
- In this layout the fields' ids are now `payment-email`, `payment-name` and `payment-address`.

**The shop itself behaves correctly here.** Before editing, I ran the repaired steps through the robotframework MCP server against the live shop. The order went through and the confirmation read `Order ORD-36F37ACA confirmed! …`, which matches the spec's `^ORD-[0-9A-F]{8}$`. The active `drift_and_bug` preset doesn't plant a bug in this test, so nothing needed to change in its assertion.

**The change.** In `tests/ui/checkout.robot:29`, `Fill Checkout Form By Field Ids` became `Fill Checkout Form` from `resources/checkout.resource`. That keyword already existed with the same three arguments. It finds each field by its label inside the checkout form, for example `form[action="/checkout"] >> role=textbox[name="Email"]`. Following the conventions, it finds elements by what a person sees rather than by ids, and only looks inside the checkout form, so it can't pick up the sign-in dialog's email field. Ids can be renamed, as this layout shows, but the labels stay the same, which is why it should work in every layout. I checked only the current one, because switching presets is off-limits.

**Checks.**
- The test passes on its own through `uv run robotcode robot`.
- Static analysis of the file reports no errors or warnings.
- `WEB-006_AC-11` and `WEB-006_AC-12` already use `Fill Checkout Form`, and they passed in the hook's run in this layout.

**Also worth knowing:**
- **`WEB-006_AC-1 Order Total Adds Up` fails in this layout, for a different reason.** Its `Get Order Total` keyword in `legacy.resource` waits for `[data-test="checkout-total"]`, which this layout no longer has. My edit didn't cause this and I left it alone, since you asked about AC-7. It needs the same kind of repair; I can do it next if you want.
- **`Fill Checkout Form By Field Ids` is now unused.** It stays in `legacy.resource`, which I'm not allowed to edit.
- **Nothing is committed yet.**

**The participant runs** `uv run robotcode robot --test "WEB-006_AC-7 Successful Order"`:

```
Tests.Ui.Checkout :: Checkout, /checkout (spec: shop/checkout). Ev... | PASS |
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

## Step 6 - Put the shop back

**The participant runs** `uv run --no-sync python -m shop reset`:

```
reset space default: removed 3 flag settings, 31 cart items and 10 orders
```

**The participant runs** `uv run robotcode robot --test "WEB-006_AC-7 Successful Order"`:

```
Tests.Ui.Checkout :: Checkout, /checkout (spec: shop/checkout). Ev... | PASS |
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
