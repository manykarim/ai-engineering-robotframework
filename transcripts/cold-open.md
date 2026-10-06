# Cold open: the recorded backup

*Recorded with Claude Code 2.1.281, with a healing model configured, from the lab's instructions. Results are shortened; your agent's answers will differ in wording.*

## Before the session

**The participant runs** `git status --short && echo 'clean working tree'`:

```
clean working tree
```

**The participant runs** `uv run --no-sync python setup-check/check.py | grep -E 'Healing|checks:'`:

```
  PASS  M8  Healing endpoint       HEAL_MODEL, HEAL_BASE_URL and HEAL_API_KEY are set
18 checks: 17 passed, 1 warnings, 0 failed, 0 skipped
```

## 1 - A criterion, handed to an agent

**Prompt:**

> Write a Robot Framework test for criterion WEB-004_AC-2 of this repository, following docs/conventions.md. Put the test in tests/ui/cold_open.robot and any keyword it needs in resources/, then run the test.

**Agent:**

I'll start by reading the conventions and locating the criterion.

*The agent runs `ls -la && cat docs/conventions.md && git ls-files | head -200`*

```
total 360
drwxr-xr-x 20 user user   4096 Sep 25 12:22 .
drwxr-xr-x  4 user user   4096 Sep 25 12:22 ..
drwxr-xr-x  3 user user   4096 Sep 25 12:21 .agents
drwxr-xr-x  4 user user   4096 Sep 25 12:21 .claude
-rw-r--r--  1 user user    203 Sep 25 12:22 .env
-rw-r--r--  1 user user    474 Sep 25 12:21 .env.example
drwxr-xr-x  7 user user   4096 Sep 25 12:22 .git
drwxr-xr-x  4 user user   4096 Sep 25 12:21 .github
-rw-r--r--  1 user user    523 Sep 25 12:21 .gitignore
-rw-r--r--  1 user user      5 Sep 25 12:21 .python-version
drwxr-xr-x  4 user user   4096 Sep 25 12:21 .venv
... (278 more lines)
```

*The agent runs `grep -rn "WEB-004" --include="*" -I . 2>/dev/null | grep -v "^./.venv" | head -50`*

```
GLOSSARY.md:173:A requirement as a product owner writes it, with acceptance criteria such as `WEB-004_AC-3`. Tests name the criterion
openspec/specs/workshop/baseline-suite/spec.md:9:The suite SHALL verify WEB-002_AC-1 with two separate tests - one for each card's add-to-cart control, one for each card's price - and SHALL verify WEB
openspec/specs/workshop/baseline-suite/spec.md:13:- **THEN** two names start with `WEB-002_AC-1`, one with `WEB-006_AC-1`, and none with an ID of WEB-003, WEB-004, WEB-005, WEB-007 or API-005
openspec/specs/shop/search/spec.md:8:### Requirement: Search form on the home page (WEB-004_AC-1)
openspec/specs/shop/search/spec.md:15:### Requirement: Search form on the products page (WEB-004_AC-2)
openspec/specs/shop/search/spec.md:22:### Requirement: Search submission shows results (WEB-004_AC-3)
openspec/specs/shop/search/spec.md:29:### Requirement: Autocomplete suggestions (WEB-004_AC-5)
openspec/specs/shop/search/spec.md:36:### Requirement: Clear search results (WEB-004_AC-6)
openspec/specs/shop/search/spec.md:43:### Requirement: Empty state for no results (WEB-004_AC-7)
openspec/specs/shop/search/spec.md:50:### Requirement: Results are product cards (WEB-004_AC-8)
openspec/specs/shop/search/spec.md:57:### Requirement: Search via the API (WEB-004_AC-9)
openspec/changes/workshop-labs/tasks.md:7:- [x] 1.3 Copy the five story files (WEB-003, WEB-004, WEB-005, WEB-007, API-005) from demo-webshop at the pinned `v0.3.0` into `labs/lab-05-prompt-to-green/s
... (38 more lines)
```

*The agent runs `cat openspec/specs/shop/search/spec.md && echo ---- && cat openspec/specs/shop/interpretation-rules/spec.md && echo ---- && cat labs/lab-05-prompt-to-green/stories/WEB-004_search_products.md`*

```
# shop/search Specification

## Purpose
Describes product search as a shopper and an API consumer experience it: the search forms, suggestions while typing, results, clearing, the empty state, and the search API.

## Requirements

### Requirement: Search form on the home page (WEB-004_AC-1)
The home page, `/`, SHALL show a search form or input in its hero section, with a placeholder or label indicating its purpose.

#### Scenario: Home page search
- **WHEN** a shopper opens `/`
... (245 more lines)
```

*The agent runs `for f in resources/*.resource tests/ui/*.robot robot.toml .env.example; do echo "==== $f"; cat "$f"; done; echo "==== .env (keys only)"; sed 's/=.*/=.../' .env`*

```
==== resources/api.resource
*** Settings ***
Documentation       The shop's API, in the configured workshop space.

Library             Collections
Library             RequestsLibrary


*** Keywords ***
Open Shop API
    [Documentation]    Creates the API session. It sends ${SHOP_SPACE} when one is set.
    &{headers}=    Create Dictionary
... (485 more lines)
```

**Agent:**

Now let me check the conventions spec and whether the shop is up.

*The agent runs `cat openspec/specs/workshop/test-conventions/spec.md; echo ----; timeout 60 uv run --no-sync python -m shop status 2>&1 | head -40`*

```
# workshop/test-conventions Specification

## Purpose
Defines the conventions the shipped suite follows and that the labs, the Lab 3 skill and the Lab 7 hook rely on, so that tests written by participants and by agents read and behave like the suite they

## Requirements

### Requirement: Criterion ID first
A test that verifies a story criterion SHALL start its name with the criterion ID as `<STORY>_<AC>`. Several tests of one criterion SHALL share the prefix and differ in the rest of the name. Tests tha

#### Scenario: Tracing a failure
- **WHEN** a test named `WEB-006_AC-1 Order Total Adds Up` fails
... (47 more lines)
```

**Agent:**

The local shop is up. Let me look at how `/products` renders its search form so the locator uses the stable contract.

*The agent runs `curl -s http://localhost:9090/products | python3 -c "
import sys,re
html=sys.stdin.read()
for m in re.finditer(r'<form[^>]*>.*?</form>', html, re.S):
    s=m.group(0)
    print(re.sub(r'\s+',' ',s)[:1500]); print('----')
for m in re.finditer(r'<input[^>]*type=\"search\"[^>]*>|<[^>]*role=\"search\"[^>]*>', html):
    print(m.group(0))
"`*

```
Exit code 1
pyenv: version `3.12' is not installed (set by <repo>/.python-version)
```

*The agent runs `curl -s http://localhost:9090/products | uv run --no-sync python -c "
import sys,re
html=sys.stdin.read()
for m in re.finditer(r'<form[^>]*>.*?</form>', html, re.S):
    s=m.group(0)
    print(re.sub(r'\s+',' ',s)[:1500]); print('----')
for m in re.finditer(r'<input[^>]*type=\"search\"[^>]*>|<[^>]*role=\"search\"[^>]*>', html):
    print(m.group(0))
"`*

```
<form class="hero__search" role="search"> <label class="form-field" aria-label="Search the catalogue"> <span class="form-field__icon" aria-hidden="true"> <svg width="20" height="20" viewBox="0 0 24 24
----
<form class="filters-form" method="get"> <fieldset class="filter-group"> <legend>Categories</legend> <div class="chip-group chip-group--scroll" role="group" aria-label="Filter by category"> <label cla
----
<form class="auth-modal__form" novalidate> <label class="form-field" for="auth-email"> <span>Email</span> <input id="auth-email" name="email" type="email" placeholder="jamie@flowlinesupply.com" autoco
----
<form class="chat-widget__form" novalidate> <label class="visually-hidden" for="chat-input">Ask Flowline Supply AI assistant</label> <textarea id="chat-input" name="question" rows="2" placeholder="Ask
----
<form class="hero__search" role="search">
<input type="search" name="query" placeholder="Search the full collection..." autocomplete="off"
          data-test="search-input" />
```

*The agent runs `cat docs/facilitator/cold-open.md; echo ----; cat hooks/no_inline_locators.py | head -80; echo ----; cat .gitignore`*

```
# Cold open

*Facilitator material.* The first five minutes of Module 1: the destination before the theory. One prompt becomes a
green test, the shop's layout drifts and breaks the suite, and the suite heals itself. No slides.

**It may not flake.** Rehearse it until it is boring. If any step does not show its expected output, do not debug it
on stage: switch to the recorded backup, `transcripts/cold-open.md`, which you keep open in a browser tab.

## Before the session (T-15 minutes)

On your own machine, in your clone of the repository, with the local shop running:

... (143 more lines)
```

*The agent runs `cat pyproject.toml; cat tests/api/smoke.robot | head -20`*

```
[project]
name = "ai-engineering-robotframework"
version = "0.1.0"
description = "Participant repository for the workshop Agentic Engineering with Robot Framework."
readme = "README.md"
# Exactly the interpreter in .python-version: the lock targets one Python,
# and uv installs it for participants (design D1).
requires-python = "==3.12.*"
# Every direct dependency is pinned exactly and resolved into uv.lock.
# Install with `uv sync --locked`, never with pip (design D1).
dependencies = [
  "robotframework==7.5",
... (49 more lines)
```

**Agent:**

Now the keyword, in the catalogue resource next to the page it describes:

*The agent edits `<repo>/resources/catalogue.resource`*

```
The file <repo>/resources/catalogue.resource has been updated successfully.
```

*The agent edits `<repo>/resources/catalogue.resource`*

```
The file <repo>/resources/catalogue.resource has been updated successfully.
```

*The agent writes `<repo>/tests/ui/cold_open.robot`*

```
File created successfully at: <repo>/tests/ui/cold_open.robot (file state is curr
```

*The agent runs `uv run robotcode robot tests/ui/cold_open.robot 2>&1 | tail -25; echo "---- locator hook:"; uv run --no-sync python hooks/no_inline_locators.py tests/ui/cold_open.robot; echo "exit $?"`*

```
==============================================================================
Cold Open :: Search on the products page, /products (spec: shop/search).      
==============================================================================
WEB-004_AC-2 Products Page Shows Search Input :: Once the products... | PASS |
------------------------------------------------------------------------------
Cold Open :: Search on the products page, /products (spec: shop/se... | PASS |
1 test, 1 passed, 0 failed
==============================================================================
Output:  <repo>/results/output.xml
Log:     <repo>/results/log.html
Report:  <repo>/results/report.html
---- locator hook:
... (1 more lines)
```

**Agent:**

The test passes, and the Lab 7 locator hook finds no locator in the test file. Since I edited a shared resource, I'll also run the whole suite without the tests that are broken on purpose.

*The agent runs `uv run robotcode robot --exclude broken 2>&1 | grep -E "PASS|FAIL|tests?," ; git status --short`*

```
Health Reports Ok                                                     | PASS |
Catalogue Lists Twelve Products                                       | PASS |
Tests.Api.Smoke :: API smoke tests: the shop answers, and the cata... | PASS |
2 tests, 2 passed, 0 failed
Tests.Api                                                             | PASS |
2 tests, 2 passed, 0 failed
WEB-002_AC-1 Every Card Offers Add To Cart :: Every card of the gr... | PASS |
WEB-002_AC-1 Card Prices Are The Product Prices :: The price on ev... | PASS |
WEB-002_AC-2 Categories Filter Group :: A "Categories" group offer... | PASS |
WEB-002_AC-7 Audio Filter Shows Only Audio :: With only "Audio" ch... | PASS |
WEB-002_AC-10 Reset Filters :: "Reset" clears every filter and bri... | PASS |
Tests.Ui.Catalogue :: The products page, /products (spec: shop/cat... | PASS |
... (16 more lines)
```

**Agent:**

I added a test for WEB-004_AC-2 and ran it against the local shop: **1 test, 1 passed**.

**The test**, in `tests/ui/cold_open.robot`:

```robotframework
WEB-004_AC-2 Products Page Shows Search Input
    [Documentation]    Once the products page has loaded, a search input is visible on it.
    Go To Catalogue
    Search Input Should Be Visible
```

- It is named with the criterion ID first and tagged `WEB-004` and `ui`.
- It gets a fresh browser context through `Start Shop Test`, and applies no preset and no reset.
- The test file contains only keyword calls. The Lab 7 check, `hooks/no_inline_locators.py`, finds no locator in it.

**The keyword** is in `resources/catalogue.resource`, which already covers `/products`:

```robotframework
${SEARCH FORM}      role=search

Search Input Should Be Visible
    [Documentation]    The page's search form shows a search input.
    Wait For Elements State    ${SEARCH FORM} >> role=searchbox    visible
```

- The locator uses only roles. The shop's HTML has `data-test="search-input"` and a `hero__search` class, and the conventions rule both out.
- The field is found inside its form, as convention 5 requires.
- The criterion quotes no text, so the test checks no label or placeholder.
- `Go To Catalogue` already waits for the product grid, which covers "when the page has loaded".

**Checks:**
- Because I changed a shared resource, I also ran the whole suite without the `broken` tests: **12 tests, 12 passed**. That count matches what `docs/facilitator/cold-open.md` expects in step 3.
- I did not try the test after the `stage4` layout change. Applying that preset would have changed your shop's state. The test should survive it because it uses only roles, but I haven't confirmed that.

Nothing is committed. `git status` shows the edited `resources/catalogue.resource` and the new `tests/ui/cold_open.robot`. `openspec/specs/workshop/baseline-suite` says the shipped suite must not test WEB-004, so these two changes shouldn't be kept. The cleanup in the cold-open notes (`git checkout -- resources && rm -f tests/ui/cold_open.robot`) removes both.

## 2 - A redesign overnight

**The participant runs** `uv run --no-sync python -m shop preset stage4`:

```
applied preset stage4 in space default
```

## 3 - And the suite?

**The participant runs** `uv run robotcode robot --exclude broken > /dev/null; uv run robotcode results summary | grep -E 'Total|Passed|Failed'`:

```
- _Total:_ 12
- _Passed:_ 8
- _Failed:_ 4
```

**The participant runs** `uv run robotcode results show --failed | grep FAIL | sed 's/ (`.*//'`:

```
- ❌ **FAIL** Tests.Ui.Catalogue.WEB-002_AC-1 Card Prices Are The Product Prices
- ❌ **FAIL** Tests.Ui.Catalogue.WEB-002_AC-7 Audio Filter Shows Only Audio
- ❌ **FAIL** Tests.Ui.Checkout.WEB-006_AC-1 Order Total Adds Up
- ❌ **FAIL** Tests.Ui.Checkout.WEB-006_AC-7 Successful Order
```

## 4 - The same suite, with a healing listener

**The participant runs** `uv run robotcode -p heal robot --exclude broken | grep -o 'heal: .*' | cut -c1-160`:

```
heal: 'Get Element' failed (locator-drift) and was healed: Replaced broken locator 'section:has(h2:text-is("All products")):not(:has(section)) >> .product-grid'
heal: proactively replaced known-broken locator with 'css=.catalog-content .tile-rack' (from this run)
heal: 'Get Text' failed (locator-drift) and was healed: Replaced broken locator '[data-test="checkout-total"]' with verified 'css=div.payment-totals__total'.
heal: 'Fill Text' failed (locator-drift) and was healed: Replaced broken locator 'id=checkout-email' with verified 'css=input#payment-email'.
heal: 'Fill Text' failed (locator-drift) and was healed: Replaced broken locator 'id=checkout-name' with verified 'css=input#payment-name'.
heal: 'Fill Text' failed (locator-drift) and was healed: Replaced broken locator 'id=checkout-address' with verified 'css=textarea#payment-address'.
```

**The participant runs** `uv run robotcode results summary | grep -E 'Total|Passed|Failed'`:

```
- _Total:_ 12
- _Passed:_ 12
- _Failed:_ 0
```

## 5 - Every heal is a proposal

**The participant runs** `uv run --no-sync python -c "import json; s=json.load(open('results/heal/summary.json')); print({k: s[k] for k in ('transactions', 'healed', 'unhealed')})"`:

```
{'transactions': 5, 'healed': 5, 'unhealed': 0}
```

**The participant runs** `git status --short -- tests resources`:

```
 M resources/catalogue.resource
?? tests/ui/cold_open.robot
```

## After the session

**The participant runs** `uv run --no-sync python -m shop reset`:

```
reset space default: removed 1 flag settings, 5 cart items and 3 orders
```
