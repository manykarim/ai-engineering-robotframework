# Lab 3 - Skills: the recorded walkthrough

*Recorded with Claude Code 2.1.281, from the lab's instructions. Results are shortened; your agent's answers will differ in wording.*

## Step 1 - Install the Robot Framework Agent Skills

**The participant runs** `uvx rf-agentskills@0.6.0 install --agent claude-code --scope project --project . --what skills`:

```
 installed Claude Code  
┏━━━━━━━━┳━━━━━━━━━━━━━┓
┃ op     ┃ destination ┃
┡━━━━━━━━╇━━━━━━━━━━━━━┩
│ files  │ 92 written  │
│ merges │ 0 performed │
└────────┴─────────────┘
  → Claude Code will pick up skills, agents, and hooks on next session start.
```

## Step 2 - See what you got

**Prompt:**

> Which skills do you have for Robot Framework, and what is each one for? One line each.

**Agent:**

I have 12 Robot Framework skills:

**Writing tests and keywords**
- **testcase-builder**: writes test cases from requirements or scenarios, including tags, setup/teardown and templates.
- **keyword-builder**: writes user keywords with arguments, documentation and tags, following the project's existing style.
- **resource-architect**: plans how resource files, variable files and shared keywords are laid out across a suite.

**Finding and understanding keywords**
- **libdoc-search**: searches library and resource documentation for keywords that fit a use case.
- **libdoc-explain**: explains a specific keyword, its arguments and how to use it, from its libdoc.

**Web UI**
- **browser**: tests with Browser Library (Playwright), which waits automatically and handles iframes, Shadow DOM and multiple tabs.
- **selenium**: tests with SeleniumLibrary (WebDriver), covering forms, windows, frames and JavaScript execution.

**API**
- **requests**: REST tests with RequestsLibrary, covering sessions, authentication, uploads and response checks.
- **restinstance**: REST tests with RESTinstance, which has built-in assertions, JSON Schema and OpenAPI validation.

**Other platforms**
- **appium**: mobile tests with AppiumLibrary for native, hybrid and mobile-browser apps on iOS and Android.
- **platynui**: native desktop UI tests with PlatynUI, finding elements by XPath on Windows and Linux.

**Results**
- **results**: reads `output.xml` and reports pass/fail counts, tag stats, errors and timings, and merges runs with rebot.

Since the demo shop has a web UI and an API, the web UI and API skills are the ones that matter here. Which of the two libraries in each pair to use depends on what the repo pins.

## Step 3 - Rerun Lab 2's prompt

**Prompt:**

> Write a Robot Framework test for criterion WEB-002_AC-5 of this repository and save it as results/lab-03/with-skills.robot. Do not run it, and do not change any other file.

*The agent runs `cat docs/agent-environment.md docs/conventions.md && grep -rn "WEB-002" openspec/specs/shop/ | head -30 && ls results results/* 2>/dev/null; git ls-files | head -100`*

```
# Environment

- Install: `uv sync --locked`, then `uv run --no-sync rfbrowser install chromium`.
- Check the environment: `uv run --no-sync python setup-check/check.py`.
- Run the suite: `uv run robotcode robot`. Plain `robot` ignores `robot.toml` and cannot find the shop.
- Run one test: `uv run robotcode robot -t "<test name>"`.
- `-p shared` selects the shared instance: `uv run robotcode -p shared robot`. Without it, the local shop.
- Logs and reports go to `results/`, which git ignores.
# Test conventions

How the tests in this repository are written. The shipped suite follows these rules, and so should every test you or
an agent add. They are specified in `openspec/specs/workshop/test-conventions/spec.md`.
... (202 more lines)
```

*The agent runs `git ls-files | sed -n '100,400p' | grep -v "^openspec/changes\|^\.github\|^\.agents" ; cat openspec/specs/shop/catalogue/spec.md; cat openspec/specs/shop/interpretation-rules/spec.md`*

```
openspec/config.yaml
openspec/specs/.gitkeep
openspec/specs/shop/authentication/spec.md
openspec/specs/shop/cart/spec.md
openspec/specs/shop/catalogue/spec.md
openspec/specs/shop/checkout/spec.md
openspec/specs/shop/interpretation-rules/spec.md
openspec/specs/shop/product-detail/spec.md
openspec/specs/shop/search/spec.md
openspec/specs/workshop/agent-context/spec.md
openspec/specs/workshop/baseline-suite/spec.md
openspec/specs/workshop/setup-check/spec.md
... (189 more lines)
```

*The agent runs `cat labs/lab-03-skills/INSTRUCTIONS.md labs/lab-03-skills/checklist.md; echo ----; cat tests/ui/catalogue.robot; echo ----; cat resources/catalogue.resource; echo ----; cat resources/shop.resource; echo ----; cat robot.toml`*

```
# Lab 3 - Skills

Install ready-made Robot Framework [skills](../../GLOSSARY.md#skill), then write one of your own that enforces a
convention of this repository, and check that it loads when it should, and only then.

| | |
|---|---|
| Module | 3 - Agent Skills |
| Time | 25 minutes |
| Shop preset | `clean` |
| You need | Lab 0 done. Your `AGENTS.md` from Lab 2 helps, but this lab works without it |
| You start from | `main`, plus your work from Lab 2 if you have it |
... (330 more lines)
```

*The agent runs `cat results/lab-02/after.robot; echo ----; cat results/lab-02/before.robot; echo ----; cat hooks/no_inline_locators.py | head -80; echo ----; grep -n "AC-4\|AC-5\|broken" docs/facilitator/suite-outcomes.md | head -20`*

```
*** Settings ***
Documentation       The products page, /products (spec: shop/catalogue).

Resource            resources/shop.resource
Resource            resources/catalogue.resource

Suite Setup         Open Shop Browser
Suite Teardown      Close Browser
Test Setup          Start Shop Test

Test Tags           WEB-002    ui

... (116 more lines)
```

*The agent loads the skill `testcase-builder`*

**Agent:**

The testcase-builder skill loaded. Next I'll use its script to generate the test block, reusing the existing catalogue keywords.

*The agent runs `echo '{"style":"keyword-driven","tests":[{"name":"WEB-002_AC-5 Availability Filter","documentation":"An availability filter offers a \"Show in-stock only\" checkbox, unchecked by default.","steps":[{"keyword":"Go To Catalogue"},{"keyword":"Checkbox Should Be Unchecked","args":["Show in-stock only"]}]}]}' | python3 .claude/rf-agentskills-files/scripts/testcase_builder.py`*

```
Exit code 1
pyenv: version `3.12' is not installed (set by <repo>/.python-version)
```

*The agent runs `echo '{"style":"keyword-driven","tests":[{"name":"WEB-002_AC-5 Availability Filter","documentation":"An availability filter offers a \"Show in-stock only\" checkbox, unchecked by default.","steps":[{"keyword":"Go To Catalogue"},{"keyword":"Checkbox Should Be Unchecked","args":["Show in-stock only"]}]}]}' | uv run --no-sync python .claude/rf-agentskills-files/scripts/testcase_builder.py`*

```
{
  "artifact": "WEB-002_AC-5 Availability Filter\n    [Documentation]    An availability filter offers a \"Show in-stock only\" checkbox, unchecked by default.\n    Go To Catalogue\n    Checkbox Should
  "full_suite": false,
  "warnings": [],
  "suggestions": []
}
```

*The agent writes `<repo>/results/lab-03/with-skills.robot`*

```
File created successfully at: <repo>/results/lab-03/with-skills.robot (file stat
```

*The agent runs `uv run --no-sync python hooks/no_inline_locators.py results/lab-03/with-skills.robot; echo "exit=$?"; git status --short`*

```
exit=0
 M AGENTS.md
?? .claude/rf-agentskills-files/
?? .claude/skills/appium/
?? .claude/skills/keyword-builder/
?? .claude/skills/libdoc-explain/
?? .claude/skills/libdoc-search/
?? .claude/skills/platynui/
?? .claude/skills/requests/
?? .claude/skills/resource-architect/
?? .claude/skills/restinstance/
?? .claude/skills/selenium/
... (4 more lines)
```

**Agent:**

I saved the test for WEB-002_AC-5 as `results/lab-03/with-skills.robot`. As you asked, I didn't run it and changed no other file; `git status` looks the same as when I started.

```robotframework
*** Test Cases ***
WEB-002_AC-5 Availability Filter
    [Documentation]    An availability filter offers a "Show in-stock only" checkbox, unchecked by default.
    Go To Catalogue
    Checkbox Should Be Unchecked    Show in-stock only
```

- **Spec:** WEB-002_AC-5 in `openspec/specs/shop/catalogue/spec.md` says the products page shows a "Show in-stock only" checkbox that is unchecked by default. The test opens `/products` and checks exactly that.
- **Conventions:** The test name starts with the criterion ID and carries the tags `WEB-002` and `ui`. It uses only existing keywords from `resources/catalogue.resource`, so there are no locators in the test file; the repo's `hooks/no_inline_locators.py` check found none. Each test gets its own browser context through `Start Shop Test`, and nothing applies a preset.
- **Label match:** `Checkbox Should Be Unchecked` finds the checkbox by its label, ignoring case and matching part of the text, as the interpretation rules allow for a form field.

**For your Lab 3 comparison:**
- **Did a skill show up?** Yes. `testcase-builder` loaded, and I used its builder script to generate the test block.
- **Did the keywords change?** No. The chosen keywords (`Go To Catalogue`, `Checkbox Should Be Unchecked`) and the settings are the same as in `results/lab-02/after.robot`. The only difference is the documentation line, which now also says "unchecked by default".
- **Why so little changed:** The installed skills describe library usage in general. What decided this test was the repository's own context: `AGENTS.md`, `docs/conventions.md` and the existing resources.

The builder script failed under plain `python3` because the pinned Python 3.12 isn't installed for pyenv. It worked with `uv run --no-sync python`, and I installed nothing.

**The participant runs** `diff results/lab-02/after.robot results/lab-03/with-skills.robot`:

```
16c16
<     [Documentation]    An availability filter offers an unchecked "Show in-stock only" checkbox.
---
>     [Documentation]    An availability filter offers a "Show in-stock only" checkbox, unchecked by default.
```

## Step 5 - Copy the template

**The participant runs** `cp -r skills/template .claude/skills/locators-in-resources && ls .claude/skills/locators-in-resources`:

```
SKILL.md
scripts
```

## Step 6 - Make it yours

*In the lab you edit `SKILL.md` yourself. For the reference solution, the rehearsal lets the agent do it with the same instructions. Claude Code asks before it writes into `.claude/`; the rehearsal approved that up front.*

**Prompt:**

> Turn .claude/skills/locators-in-resources/SKILL.md into a skill for convention 2 of docs/conventions.md, "Locators live in resources": set name to the folder's name, locators-in-resources; rewrite description to say what the skill checks and when to use it; replace the rule, the reason and the examples with those of convention 2; delete the template's comment. Leave the scripts folder alone.

*The agent runs `cat .claude/skills/locators-in-resources/SKILL.md && echo ---- && ls -R .claude/skills/locators-in-resources && echo ---- && cat docs/conventions.md`*

```
---
name: criterion-id-first
description: Checks that Robot Framework test names in this repository start with the story criterion they verify (<STORY>_<AC>, for example WEB-006_AC-1) or carry the smoke tag. Use when writing, ren
---

# Criterion ID first

<!--
  This is the template for Lab 3. It is a complete, working skill for convention 1 of docs/conventions.md.
  To make your own skill:
    1. Copy this folder into your agent's skill folder and rename it: .claude/skills/<name>/ (Claude Code),
       .agents/skills/<name>/ (Codex) or .github/skills/<name>/ (GitHub Copilot).
... (126 more lines)
```

*The agent runs `cat .claude/skills/locators-in-resources/scripts/check.py && echo ---- && cat openspec/specs/workshop/test-conventions/spec.md && echo ---- && git status --short .claude/skills/locators-in-resources && ls .claude/skills && grep -rl "locators-in-resources\|Lab 3" --include=*.md . 2>/dev/null | grep -v node_modules | head -20`*

```
"""Report test cases whose name does not start with <STORY>_<AC> and that carry no smoke tag.

    uv run --no-sync python scripts/check.py tests/ [more files or folders]

The helper script of the Lab 3 skill template. It parses the files with Robot Framework's own
parser, so it sees the test names and tags exactly as Robot Framework does. Exits with 1 when a
test breaks the rule.
"""
from __future__ import annotations

import re
import sys
... (136 more lines)
```

*The agent runs `cat labs/lab-03-skills/INSTRUCTIONS.md labs/lab-03-skills/checklist.md && echo ---- && grep -n -i "exception\|locator" docs/facilitator/suite-outcomes.md openspec/changes/archive/2026-09-24-baseline-suite/design.md | head -40`*

```
# Lab 3 - Skills

Install ready-made Robot Framework [skills](../../GLOSSARY.md#skill), then write one of your own that enforces a
convention of this repository, and check that it loads when it should, and only then.

| | |
|---|---|
| Module | 3 - Agent Skills |
| Time | 25 minutes |
| Shop preset | `clean` |
| You need | Lab 0 done. Your `AGENTS.md` from Lab 2 helps, but this lab works without it |
| You start from | `main`, plus your work from Lab 2 if you have it |
... (112 more lines)
```

*The agent runs `ls resources tests tests/* && sed -n 1,60p resources/catalogue.resource && echo ---- && sed -n 1,50p tests/ui/checkout.robot 2>/dev/null; cat skills/template/SKILL.md | diff - <(git show HEAD:skills/template/SKILL.md) && echo template-unchanged`*

```
resources:
api.resource
catalogue.resource
checkout.resource
legacy.resource
shop.resource

tests:
api
ui

tests/api:
... (118 more lines)
```

*The agent writes `<repo>/.claude/skills/locators-in-resources/SKILL.md`*

```
The file <repo>/.claude/skills/locators-in-resources/SKILL.md has been updated s
```

**Agent:**

The skill file is written. Now I'll check that the keywords and criterion in the examples really exist, and that `scripts/` is untouched.

*The agent runs `grep -rn "WEB-002_AC-5" openspec/specs/shop | head -3; grep -n "^Go To Catalogue\|^Check Category\|^Fill Checkout Form$" resources/*.resource; diff -r skills/template/scripts .claude/skills/locators-in-resources/scripts && echo scripts-identical; head -4 .claude/skills/locators-in-resources/SKILL.md | uv run --no-sync python -c "import sys,yaml;print(yaml.safe_load(sys.stdin.read().split('---')[1]))" 2>&1 | head -3`*

```
openspec/specs/shop/catalogue/spec.md:36:### Requirement: Availability filter (WEB-002_AC-5)
resources/checkout.resource:30:Fill Checkout Form
resources/catalogue.resource:22:Go To Catalogue
resources/catalogue.resource:58:Check Category
scripts-identical
{'name': 'locators-in-resources', 'description': 'Checks that Robot Framework test files in this repository contain keyword calls only, and that every locator (role=, text=, CSS or XPath selectors, >>
```

**Agent:**

WEB-002_AC-5 is the availability filter, so the criterion ID in my example is wrong. I'll look up the category filter's criterion.

*The agent runs `grep -n "^### Requirement" openspec/specs/shop/catalogue/spec.md; git show HEAD:tests/ui/catalogue.robot | grep -n "^WEB-\|Check Category" `*

```
8:### Requirement: Full product grid (WEB-002_AC-1)
15:### Requirement: Category filter group (WEB-002_AC-2)
22:### Requirement: Price range filter (WEB-002_AC-3)
29:### Requirement: Rating filter (WEB-002_AC-4)
36:### Requirement: Availability filter (WEB-002_AC-5)
43:### Requirement: Apply filters (WEB-002_AC-6)
50:### Requirement: Category filter application (WEB-002_AC-7)
57:### Requirement: Price range filter application (WEB-002_AC-8)
64:### Requirement: Combined filters (WEB-002_AC-9)
71:### Requirement: Reset filters (WEB-002_AC-10)
78:### Requirement: Collections to explore (WEB-002_AC-11)
85:### Requirement: Handpicked highlights (WEB-002_AC-12)
... (10 more lines)
```

*The agent runs `sed -i 's/^WEB-002_AC-5 Audio Filter Shows Only Audio$/WEB-002_AC-7 Audio Filter Shows Only Audio/' .claude/skills/locators-in-resources/SKILL.md && grep -n "AC-" .claude/skills/locators-in-resources/SKILL.md`*

```
14:WEB-002_AC-7 Audio Filter Shows Only Audio
```

**Agent:**

I rewrote `.claude/skills/locators-in-resources/SKILL.md` for convention 2, "Locators live in resources". The loaded skill list now shows it under its new name and description.

- **`name`** is now `locators-in-resources`, the same as the folder.
- **`description`** says what it checks: test files contain only keyword calls, and every locator (`role=`, `text=`, CSS or XPath selectors, `>>` chains) sits in a keyword under `resources/`. It says to use the skill when writing, changing or reviewing tests in `.robot` files, deciding where a locator or keyword belongs, or checking tests against the conventions of this repository. That last phrase is the wording of step 7's trigger prompt in Lab 3. Nothing in it touches shop commands like `reset`, so step 8's prompt shouldn't load it.
- **Rule, reason and examples** now come from convention 2. The rule's example is `WEB-002_AC-7 Audio Filter Shows Only Audio` calling `Go To Catalogue` and `Check Category`, which are real keywords in `resources/catalogue.resource`. I first put WEB-002_AC-5 on that test, but that criterion is the availability filter, so I changed it to AC-7. The examples table has two lines that follow the rule and four that break it. I kept the Reset-filters test out of the examples: the facilitator notes keep it as the one inline locator the skill is meant to find.
- **The template's comment** is gone.
- **`scripts/`** is unchanged; it's still identical to `skills/template/scripts`.

I also rewrote the template's "How to apply it" section. The rewrite explains how to tell a locator from data, and how to fix a finding. I took out the instruction to run `scripts/check.py`, because that script still checks convention 1, the criterion ID. An agent that ran it would report test names instead of locators. Pointing the skill back at the script is the lab's stretch goal, once `check.py` checks locators.

## Step 7 - Check that it triggers

**Prompt:**

> Review tests/ui/catalogue.robot against the conventions of this repository.

*The agent loads the skill `locators-in-resources`*

*The agent reads `<repo>/tests/ui/catalogue.robot`*

*The agent reads `<repo>/docs/conventions.md`*

*The agent reads `<repo>/resources/catalogue.resource`*

*The agent reads `<repo>/docs/agent-environment.md`*

*The agent runs `git diff -- tests/ui/catalogue.robot resources/catalogue.resource AGENTS.md`*

```
diff --git a/AGENTS.md b/AGENTS.md
index 350d077..f705e46 100644
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -1,22 +1,34 @@
 # AGENTS.md
 
-Participant repository of the workshop "Agentic Engineering with Robot Framework".
-The system under test is the demo shop, which runs from a published image.
+Participant repository of the workshop "Agentic Engineering with Robot Framework": a Robot Framework suite that
+tests the demo shop.
 
... (88 more lines)
```

*The agent reads `<repo>/resources/legacy.resource`*

*The agent reads `<repo>/resources/shop.resource`*

*The agent runs `grep -rn --include=*.robot -i "broken" tests/ ; echo ---; ls openspec/specs/shop openspec/specs/workshop; echo ---; grep -rln -i "broken" openspec/specs docs labs 2>/dev/null | head -30`*

```
tests/ui/catalogue.robot:48:    [Tags]    broken
---
openspec/specs/shop:
authentication
cart
catalogue
checkout
interpretation-rules
product-detail
search

openspec/specs/workshop:
... (27 more lines)
```

*The agent reads `<repo>/openspec/specs/workshop/test-conventions/spec.md`*

*The agent runs `cat openspec/specs/workshop/baseline-suite/spec.md; echo ======; grep -rn -i -E "exception|Reset\"|role=link|AC-12|AC-4|broken" docs/facilitator/suite-outcomes.md docs/facilitator/suite-outcomes.toml labs/lab-04-robotcode/INSTRUCTIONS.md labs/lab-07-hooks-toolbelt/INSTRUCTIONS.md labs/lab-08-healing/INSTRUCTIONS.md labs/lab-03*/INSTRUCTIONS.md 2>/dev/null | head -60`*

```
# workshop/baseline-suite Specification

## Purpose
Defines the test suite that ships with the participant repository: what it verifies, and how it behaves under every workshop preset, so that each module's demonstration - failures on purpose, drift, p

## Requirements

### Requirement: Coverage of the criteria the presets break
The suite SHALL verify WEB-002_AC-1 with two separate tests - one for each card's add-to-cart control, one for each card's price - and SHALL verify WEB-006_AC-1, together with further WEB-002 and WEB-

#### Scenario: Listing the tests
- **WHEN** the suite's test names are listed
... (137 more lines)
```

**Agent:**

Reading done. The test and its resources are loaded, and I'm now checking the assertions against the shop spec and running a static analysis.

*The agent runs `cat openspec/specs/shop/catalogue/spec.md; echo =====; cat resources/api.resource`*

```
# shop/catalogue Specification

## Purpose
Describes the products page, `/products`, as a shopper experiences it: the product grid, its filters, the collection previews and the highlights.

## Requirements

### Requirement: Full product grid (WEB-002_AC-1)
When a shopper opens `/products` and the page finishes loading, the page SHALL display all 12 seeded products in a grid. Each product card SHALL show the product's name, its image, its price - the pro

#### Scenario: Opening the products page
- **WHEN** a shopper opens `/products`
... (111 more lines)
```

*The agent runs `uv run robotcode analyze code tests/ui/catalogue.robot resources/catalogue.resource 2>&1 | tail -30`*

```
Files: 2, Errors: 0, Warnings: 0, Infos: 0, Hints: 0 (in 0.06s)
```

*The agent runs `curl -s -m 5 http://localhost:9090/api/products/ | python3 -c "import json,sys; d=json.load(sys.stdin)['items']; print([(p['name'], p['price'], type(p['price']).__name__) for p in d])" 2>&1 | head -5; grep -rn -i "\"price\"\|price.*string\|price.*number" openspec/specs/shop | head`*

```
pyenv: version `3.12' is not installed (set by <repo>/.python-version)
openspec/specs/shop/cart/spec.md:150:With items in the cart, every entry of the `items` array returned by `GET /api/cart/` SHALL contain `product_id` (integer), `name` (string), `quantity` (integer), 
```

*The agent runs `curl -s -m 5 http://localhost:9090/api/products/ | uv run --no-sync python -c "import json,sys; d=json.load(sys.stdin)['items']; print([(p['name'], p['price'], type(p['price']).__name__) for p in d])" 2>&1 | head -5`*

```
[('Atlas Standing Desk', 799.0, 'float'), ('Aurora Neural Headphones', 249.99, 'float'), ('Cascade Water Bottle', 79.0, 'float'), ('Echo Conference Speaker', 219.0, 'float'), ('Focus Loop Timer', 59.0
```

*The agent runs `uv run robotcode robot -t "WEB-002_AC-12 Handpicked Highlights" -t "WEB-002_AC-10 Reset Filters" tests/ui/catalogue.robot 2>&1 | tail -15`*

```
==============================================================================
Catalogue :: The products page, /products (spec: shop/catalogue).             
==============================================================================
WEB-002_AC-10 Reset Filters :: "Reset" clears every filter and bri... | PASS |
------------------------------------------------------------------------------
WEB-002_AC-12 Handpicked Highlights :: "Handpicked highlights" sho... | PASS |
------------------------------------------------------------------------------
Catalogue :: The products page, /products (spec: shop/catalogue).     | PASS |
2 tests, 2 passed, 0 failed
==============================================================================
Output:  <repo>/results/output.xml
Log:     <repo>/results/log.html
... (1 more lines)
```

**Agent:**

I found one convention violation in `tests/ui/catalogue.robot`. Everything else follows `docs/conventions.md`. Static analysis (`robotcode analyze code`) reports 0 errors and 0 warnings. I also ran `WEB-002_AC-10` and `WEB-002_AC-12` against the local shop and both passed.

## Must fix

**`tests/ui/catalogue.robot:69`: a locator is written directly in the test (§2 "Locators live in resources")**
```robotframework
Click    role=link[name="Reset"]
```
Every other line in the file calls a keyword and passes it data. This line passes a selector to Browser's `Click` itself. The fix is to add a keyword next to `Apply Filters` in `resources/catalogue.resource`:
```robotframework
Reset Filters
    Click    role=link[name="Reset"]
    Wait For Elements State    ${GRID}    visible
```
Then line 69 becomes `Reset Filters`. The locator itself is fine under §3, because it uses a role and an accessible name.

This is the one inline locator that the `workshop/baseline-suite` spec plants on purpose. Fixing it in your working copy is what the exercise expects. Don't carry the fix back into the participant template.

## Checked and fine

- **Criterion IDs (§1):** all 7 test names start with `WEB-002_AC-n`, and each one matches a requirement in `openspec/specs/shop/catalogue`. The two AC-1 tests share their prefix correctly.
- **Assertions against the spec:** 12 cards, 9 categories, a price range of $39.50–$899.00, and the top 3 by price with the highest first all match the spec. The rewritten AC-12 test now checks names, order and formatted prices. The API returns prices as numbers, so the `sorted(... key=price)` sort is numeric, not alphabetical.
- **Tags (§7):** `Test Tags  WEB-002  ui` covers every test. Removing `broken` from AC-12 is right, because the test now passes, as Lab 4 intends. Only `WEB-002_AC-4` still has the tag. It is the other test broken on purpose, and its expectation differs from the spec deliberately for Module 5, so I left it alone.
- **Isolation (§6):** `Start Shop Test` opens a fresh context for each test. The API is only read, and no preset or reset is applied.
- **Legacy keywords:** `Get Card Prices` (line 32) and `Get Grid Cards` (line 57) come from `resources/legacy.resource`. That is the documented exception, and these tests are meant to break when the shop's layout changes, so they are not a finding.
- **New keyword `Get Highlight Names`:** it is in the right resource (not the legacy one), has documentation, and builds on `${HIGHLIGHTS} >> role=link`.

## Optional

- **Python in test bodies (lines 29 and 79):** both lines use `Evaluate` with inline Python. The conventions don't forbid it, but moving it into a keyword would make the test read more like behaviour, for example `Get Most Expensive Products From API    3` in `resources/api.resource`.
- **Outcome matrix:** `docs/facilitator/suite-outcomes.toml` still records AC-12 as `broken` under every preset. After the Lab 4 fix, `tools/verify_outcomes.py` would therefore report a mismatch. That is expected in a participant's copy, but worth knowing if you use the matrix during the rehearsal.

Want me to make the `Reset Filters` change?

## Step 8 - Check that it stays quiet

**Prompt:**

> What does `uv run --no-sync python -m shop reset` do? Answer in two sentences.

*The agent runs `ls shop/ && grep -rn "reset" shop/*.py | head -40`*

```
__init__.py
__main__.py
__pycache__
compose.yaml
config.py
preflight.py
variables.py
shop/__main__.py:3:    status          version, space, and the presets that hold in the space
shop/__main__.py:4:    presets         the preset names the shop offers
shop/__main__.py:5:    preset NAME     apply a preset in the current space
shop/__main__.py:6:    reset           reset the current space: its flags, cart and runtime orders
shop/__main__.py:10:planted-bug flags, and ``presets`` prints no descriptions: the shop's own
... (29 more lines)
```

*The agent reads `<repo>/shop/__main__.py`*

**Agent:**

It sends `POST /api/workshop/reset` to the shop for your current space (set by `SHOP_SPACE`), which clears that space's flag settings, cart items and runtime orders, then prints how many of each it removed. On the shared instance it refuses to run and sends nothing if no space is set, so it can't wipe the baseline everyone shares (`shop/__main__.py:72-90`).

## Stretch - Give the skill teeth

**Prompt:**

> Change .claude/skills/locators-in-resources/scripts/check.py so that it reports every argument in a test file under tests/ that looks like a locator (for example css=, xpath=, id=, text=, role=, or a CSS selector), instead of checking test names. Then update SKILL.md so that it tells the agent to run it. Run it once over tests/.

*The agent runs `ls -la .claude/skills/locators-in-resources/ .claude/skills/locators-in-resources/* && cat .claude/skills/locators-in-resources/SKILL.md && echo ---- && cat .claude/skills/locators-in-resources/scripts/check.py && echo ---- && cat docs/agent-environment.md && echo ---- && cat docs/conventions.md`*

```
-rw-r--r-- 1 user user 2812 Sep 24 22:24 .claude/skills/locators-in-resources/SKILL.md

.claude/skills/locators-in-resources/:
total 16
drwxr-xr-x  3 user user 4096 Sep 24 22:24 .
drwxr-xr-x 21 user user 4096 Sep 24 22:22 ..
-rw-r--r--  1 user user 2812 Sep 24 22:24 SKILL.md
drwxr-xr-x  2 user user 4096 Sep 24 22:22 scripts

.claude/skills/locators-in-resources/scripts:
total 12
drwxr-xr-x 2 user user 4096 Sep 24 22:22 .
... (189 more lines)
```

*The agent runs `find tests -type f | sort && echo ---- && git diff && echo ---- && cat tests/ui/*.robot | head -400`*

```
tests/api/AGENTS.md
tests/api/smoke.robot
tests/ui/catalogue.robot
tests/ui/checkout.robot
----
diff --git a/AGENTS.md b/AGENTS.md
index 350d077..f705e46 100644
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -1,22 +1,34 @@
 # AGENTS.md
 
... (248 more lines)
```

*The agent runs `cat tests/api/smoke.robot tests/api/AGENTS.md && ls resources && for f in resources/*.resource; do echo "== $f"; sed -n '/\*\*\* Variables/,/\*\*\* /p' $f; done; cat robot.toml; cat pyproject.toml | head -40; git log --oneline -3 -- .claude/skills/locators-in-resources; git status --short .claude/skills/locators-in-resources`*

```
*** Settings ***
Documentation       API smoke tests: the shop answers, and the catalogue is complete.

Resource            resources/api.resource

Suite Setup         Open Shop API

Test Tags           smoke    api


*** Test Cases ***
Health Reports Ok
... (115 more lines)
```

*The agent runs `grep -rn --exclude-dir=.git --exclude-dir=.venv --exclude-dir=node_modules -l "locators-in-resources\|skill template\|scripts/check.py" . 2>/dev/null | head -30`*

```
README.md
openspec/changes/workshop-labs/tasks.md
openspec/changes/workshop-labs/design.md
labs/lab-03-skills/INSTRUCTIONS.md
openspec/changes/workshop-labs/specs/workshop/lab-assets/spec.md
.claude/skills/locators-in-resources/SKILL.md
.claude/skills/locators-in-resources/scripts/check.py
skills/template/SKILL.md
skills/template/scripts/check.py
```

*The agent runs `cat labs/lab-03-skills/INSTRUCTIONS.md && echo ---- && cat skills/template/SKILL.md && echo ---- && grep -n -i -B2 -A8 "check.py\|skill template\|locators-in-resources" openspec/changes/workshop-labs/specs/workshop/lab-assets/spec.md openspec/changes/workshop-labs/design.md | head -120`*

```
# Lab 3 - Skills

Install ready-made Robot Framework [skills](../../GLOSSARY.md#skill), then write one of your own that enforces a
convention of this repository, and check that it loads when it should, and only then.

| | |
|---|---|
| Module | 3 - Agent Skills |
| Time | 25 minutes |
| Shop preset | `clean` |
| You need | Lab 0 done. Your `AGENTS.md` from Lab 2 helps, but this lab works without it |
| You start from | `main`, plus your work from Lab 2 if you have it |
... (149 more lines)
```

*The agent runs `ls hooks && cat hooks/no_inline_locators.py && cat hooks/_*.py 2>/dev/null | head -80`*

```
README.md
__pycache__
claude-code.settings.json
codex.hooks.json
copilot.hooks.json
green_before_commit.py
hookio.py
no_inline_locators.py
run_affected_tests.py
"""Reject locator literals in test files: convention 2, "Locators live in resources".

As a hook (before an edit): refuses an edit that writes a locator literal into a .robot file
... (82 more lines)
```

*The agent runs `uv run --no-sync python - <<'EOF'
from robot.api import get_model, get_resource_model
from robot.api.parsing import ModelVisitor, Token
import robot.parsing.model.visitor as v, inspect
print(inspect.getsource(v)[:3000])
m = get_model("tests/ui/catalogue.robot")
class V(ModelVisitor):
    def visit_Statement(self, node):
        args = node.get_values(Token.ARGUMENT)
        if args: print(type(node).__name__, node.lineno, node.get_value(Token.KEYWORD) or node.get_value(Token.NAME), args[:3])
V().visit(m)
r = get_resource_model("resources/catalogue.resource")
for s in r.sections:
    for n in s.body:
        print(type(n).__name__, getattr(n, "name", None), getattr(n, "value", None))
EOF`*

```
#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016-     Robot Framework Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
... (137 more lines)
```

**Agent:**

Now the script:

*The agent writes `<repo>/.claude/skills/locators-in-resources/scripts/check.py`*

```
The file <repo>/.claude/skills/locators-in-resources/scripts/check.py has been u
```

**Agent:**

Next I'll test it against a scratch file of known locators and known data before running it on `tests/`:

*The agent runs `mkdir -p <scratch> && cat > <scratch> <<'EOF'
*** Settings ***
Documentation       role=button in docs is not a locator, nor #this.
Resource            resources/catalogue.resource
Resource            resources/checkout.resource
Suite Setup         Click    css=.banner
Test Tags           role=weird-tag


*** Variables ***
${EMAIL FIELD}      [name="email"]
${NAME}             Aurora Neural Headphones


*** Test Cases ***
Locators
    Click    role=button[name="Apply filters"]
    Fill Text    form[action="/checkout"] >> role=textbox[name="Email"]    test@example.com
    ${count}=    Get Element Count    ${GRID} >> article
    ${count}=    Get Element Count    ${grid}
    Click    xpath=//button
    Click    //button[@type="submit"]
    Click    (//a)[2]
    Click    \#email
    Click    .product-grid
    Click    [disabled]
    Click    a[href="/cart"]
    Click    button:has-text("Add to cart")
    Click    div.card
    Click    ul > li
    Click    id=email
    Click    text=Reset
    Get Text    selector=#email
    Fill Text    ${EMAIL FIELD}    x
    Fill Text    ${CHECKOUT FORM} >> role=textbox[name="Email"]    x
    VAR    ${loc}    data-testid=cart
    FOR    ${l}    IN    css=a    role=link
        Click    ${l}
    END
    [Teardown]    Click    ${CART LINK}

Data
    Check Category    Audio
    Fill Checkout Form    test@example.com    Test User    123 Test Street, City
    Get Url    $=    /checkout
    Should Be Equal    ${a}    ${b}    msg=The field "x" should show.
    ${n}=    Get Regexp Matches    ${m}    \\bORD-[0-9A-F]{8}\\b
    Should Be Equal    ${range}    ${{ ["39.50", "899.00"] }}
    Evaluate    sorted($catalogue, key=lambda p: p["price"], reverse=True)[:3]
    Evaluate    {p["name"]: p["price"] for p in $c}
    Set To Dictionary    ${before}    ${label}=${messages}
    Format Price    ${prices}[${name}]
    GET On Session    shop    /products    params=id=1
    Log    ${NAME}
    Should Be True    len($x) > 0


*** Keywords ***
Own Keyword
    [Arguments]    ${field}=[name="email"]
    Click    role=button
    RETURN    css=.x
EOF
ln -sfn "$PWD/resources" <scratch>
cd <scratch> && uv run --no-sync --project <repo> python <repo>/.claude/skills/locators-in-resources/scripts/check.py tests/; echo "exit $?"`*

```
tests/sample.robot:5: 'css=.banner' is a locator
tests/sample.robot:10: '[name="email"]' is a locator
tests/sample.robot:16: 'role=button[name="Apply filters"]' is a locator
tests/sample.robot:17: 'form[action="/checkout"] >> role=textbox[name="Email"]' is a locator
tests/sample.robot:18: '${GRID} >> article' is a locator (${GRID} from <scratch>)
tests/sample.robot:19: '${grid}' is a locator (${GRID} from <scratch>)
tests/sample.robot:20: 'xpath=//button' is a locator
tests/sample.robot:21: '//button[@type="submit"]' is a locator
tests/sample.robot:22: '(//a)[2]' is a locator
tests/sample.robot:23: '\#email' is a locator
tests/sample.robot:24: '.product-grid' is a locator
tests/sample.robot:25: '[disabled]' is a locator
... (18 more lines)
```

**Agent:**

Every locator in the scratch file was reported and none of the data was. One fix: resource paths print as absolute, so I'll resolve them relative to the working directory instead:

*The agent edits `<repo>/.claude/skills/locators-in-resources/scripts/check.py`*

```
The file <repo>/.claude/skills/locators-in-resources/scripts/check.py has been u
```

*The agent runs `cd <scratch> && uv run --no-sync --project <repo> python <repo>/.claude/skills/locators-in-resources/scripts/check.py tests/ | grep ' from '; cd <repo> && rm -rf <scratch> && echo "=== over tests/" && uv run --no-sync python .claude/skills/locators-in-resources/scripts/check.py tests/; echo "exit $?"`*

```
tests/sample.robot:18: '${GRID} >> article' is a locator (${GRID} from resources/catalogue.resource)
tests/sample.robot:19: '${grid}' is a locator (${GRID} from resources/catalogue.resource)
tests/sample.robot:33: '${EMAIL FIELD}' is a locator (${EMAIL FIELD} from tests/sample.robot)
tests/sample.robot:34: '${CHECKOUT FORM} >> role=textbox[name="Email"]' is a locator (${CHECKOUT FORM} from resources/checkout.resource)
tests/sample.robot:39: '${CART LINK}' is a locator (${CART LINK} from resources/checkout.resource)
=== over tests/
tests/ui/catalogue.robot:69: 'role=link[name="Reset"]' is a locator
exit 1
```

**Agent:**

Over `tests/` it finds one locator. Now SKILL.md:

*The agent edits `<repo>/.claude/skills/locators-in-resources/SKILL.md`*

```
The file <repo>/.claude/skills/locators-in-resources/SKILL.md has been updated s
```

*The agent runs `uv run --no-sync python hooks/no_inline_locators.py tests/; echo "hook exit $?"; uv run --no-sync ruff --version 2>/dev/null && uv run --no-sync ruff check .claude/skills/locators-in-resources/scripts/check.py; git status --short`*

```
tests/ui/catalogue.robot:69: locator literal 'role=link[name="Reset"]' in a test file
hook exit 1
 M AGENTS.md
 M resources/catalogue.resource
 M tests/ui/catalogue.robot
?? .claude/rf-agentskills-files/
?? .claude/settings.json
?? .claude/skills/appium/
?? .claude/skills/keyword-builder/
?? .claude/skills/libdoc-explain/
?? .claude/skills/libdoc-search/
?? .claude/skills/locators-in-resources/
... (9 more lines)
```

**Agent:**

I rewrote `.claude/skills/locators-in-resources/scripts/check.py` so it checks convention 2 instead of test names, and updated `SKILL.md` to tell the agent to run it. Over `tests/` it finds one locator:

```
$ uv run --no-sync python .claude/skills/locators-in-resources/scripts/check.py tests/
tests/ui/catalogue.robot:69: 'role=link[name="Reset"]' is a locator
exit 1
```

That's `Click    role=link[name="Reset"]` in `WEB-002_AC-10 Reset Filters`. The existing hook `hooks/no_inline_locators.py` reports the same single line. I haven't fixed it, since you only asked for the run.

**How the script works**
- Like the template, it reads each `.robot` file with Robot Framework's own parser. It checks every argument in tests and keywords, setups and teardowns, `FOR`/`VAR`/`RETURN`, and the file's own `*** Variables ***`, `*** Keywords ***` and `[Arguments]` defaults.
- It skips text that is never a locator: `[Documentation]`, tags and imports.
- It reports anything that starts with `css=`, `xpath=`, `id=`, `text=`, `role=`, `data-testid=` or `//`, any `>>` chain, and CSS such as `#email`, `.product-grid`, `[name="email"]`, `a[href=…]`, `button:has-text(…)`, `div.card` or `ul > li`. It also looks inside named arguments, so `selector=#email` counts.
- **An addition you didn't ask for:** it follows the file's `Resource` imports. A test that passes a resource variable holding a locator, even a bare `${GRID}`, is reported along with the resource it came from. Without this, the `${GRID}` case your `SKILL.md` describes could slip through.

**What `SKILL.md` now says:** the review bullet tells the agent to run the script from the repository root, both when reviewing and before finishing a test, and explains the output and exit codes. It also says to still read every argument, because the script only matches patterns. If it reports something that is really data, the agent should say so instead of moving it.

**Testing:** I ran it on a temporary test file with 28 kinds of locator and 13 kinds of data taken from the real suite. It reported every locator, including one inside a keyword's argument default, and none of the data. I then deleted the file.

**Limits:**
- It has to run from the repository root so it can find `resources/...`.
- A keyword's own named argument called `text=` or `id=` will be reported as a locator. For `id=`, I only report it when a letter follows, so `id=1` is left alone.
- CSS that starts with a plain tag name is only recognised for common HTML tags.

Nothing is committed, and `skills/template/` is unchanged.
