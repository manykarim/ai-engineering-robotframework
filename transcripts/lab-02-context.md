# Lab 2 - Context: the recorded walkthrough

*Recorded with Claude Code 2.1.281, from the lab's instructions. Results are shortened; your agent's answers will differ in wording.*

## Step 1 - The "before"

**Prompt:**

> Write a Robot Framework test for criterion WEB-002_AC-5 of this repository and save it as results/lab-02/before.robot. Do not run it, and do not change any other file.

*The agent runs `grep -rn "WEB-002" --include=* . 2>/dev/null | grep -v "^./.git/" | head -50; ls; ls results 2>/dev/null`*

```
tests/ui/catalogue.robot:13:Test Tags           WEB-002    ui
tests/ui/catalogue.robot:17:WEB-002_AC-1 Every Card Offers Add To Cart
tests/ui/catalogue.robot:26:WEB-002_AC-1 Card Prices Are The Product Prices
tests/ui/catalogue.robot:39:WEB-002_AC-2 Categories Filter Group
tests/ui/catalogue.robot:46:WEB-002_AC-4 Rating Filter
tests/ui/catalogue.robot:52:WEB-002_AC-7 Audio Filter Shows Only Audio
tests/ui/catalogue.robot:64:WEB-002_AC-10 Reset Filters
tests/ui/catalogue.robot:76:WEB-002_AC-12 Handpicked Highlights
openspec/changes/archive/2026-09-24-baseline-suite/specs/workshop/test-conventions/spec.md:50:Every test SHALL carry its story ID as a tag (for example `WEB-002`) or `smoke`, and its layer, `ui` or `a
docs/conventions.md:14:When one criterion needs several tests, they share the prefix: `WEB-002_AC-1 Every Card Offers Add To Cart` and
docs/conventions.md:15:`WEB-002_AC-1 Card Prices Are The Product Prices`. A test that verifies no criterion carries the `smoke` tag instead.
docs/conventions.md:71:| the story ID, for example `WEB-002` | every test that verifies a criterion |
... (65 more lines)
```

*The agent runs `cat openspec/specs/shop/catalogue/spec.md; echo ----; cat tests/ui/catalogue.robot; echo ----; ls -R tests resources | head -60; echo ----; ls labs; ls labs/* | head -40`*

```
# shop/catalogue Specification

## Purpose
Describes the products page, `/products`, as a shopper experiences it: the product grid, its filters, the collection previews and the highlights.

## Requirements

### Requirement: Full product grid (WEB-002_AC-1)
When a shopper opens `/products` and the page finishes loading, the page SHALL display all 12 seeded products in a grid. Each product card SHALL show the product's name, its image, its price - the pro

#### Scenario: Opening the products page
- **WHEN** a shopper opens `/products`
... (237 more lines)
```

*The agent runs `cat labs/lab-02-context/INSTRUCTIONS.md; echo ----; cat docs/conventions.md; echo ----; cat robot.toml; echo ----; ls -la results results/* `*

```
# Lab 2 - Context

Write the [context file](../../GLOSSARY.md#context-file) every agent reads, `AGENTS.md`, and see what it changes. You
need nothing but a text editor for the writing. The agent comes in before and after.

| | |
|---|---|
| Module | 2 - Context Engineering |
| Time | 25 minutes |
| Shop preset | `clean` |
| You need | Lab 0 done: the suite runs, and your agent starts in the repository |
| You start from | `main`, where `AGENTS.md` is deliberately short |
... (195 more lines)
```

*The agent runs `cat resources/catalogue.resource; echo ----; cat resources/shop.resource; echo ----; cat resources/legacy.resource; echo ----; cat openspec/specs/shop/interpretation-rules/spec.md`*

```
*** Settings ***
Documentation       The products page, /products, through the shop's stable contract:
...                 roles, accessible names, visible text and labels.

Library             Browser
Library             Collections
Library             String
Resource            shop.resource


*** Variables ***
# The innermost section headed "All products": the product grid, without the
... (232 more lines)
```

*The agent runs `ls shop; cat shop/compose.yaml; grep -rn -i "in-stock\|in stock\|instock" --exclude-dir=.git . | grep -v "^./results/" | head -30`*

```
__init__.py
__main__.py
__pycache__
compose.yaml
config.py
preflight.py
variables.py
# The demo shop, from its published image (spec: workshop/shop-access).
#
#   start       docker compose -f shop/compose.yaml up -d
#   fresh seed  docker compose -f shop/compose.yaml up -d --force-recreate
#   stop        docker compose -f shop/compose.yaml down
... (16 more lines)
```

**Agent:**

I've got the spec for WEB-002_AC-5 and the repo's conventions. Next I'll check the running shop's markup (read-only) so the checkbox locator matches the page.

*The agent runs `curl -s -m 5 http://localhost:9090/products | grep -o -i '.\{400\}in-stock.\{300\}' | head -5`*

```
(Bash completed with no output)
```

*The agent runs `curl -s -m 5 -o <scratch> -w '%{http_code} %{size_download}\n' http://localhost:9090/products; grep -o -i '.\{300\}stock.\{300\}' <scratch> | head -5`*

```
200 55735
```

*The agent runs `cd <scratch> && grep -o -i '.\{200\}\(stars\|checkbox\|availability\).\{200\}' products.html | head -8; grep -c . products.html`*

```
1487
Shell cwd was reset to <repo>
```

*The agent runs `cd <scratch> && grep -o 'src="[^"]*\.js[^"]*"' products.html | head -20`*

```
src="/static/app.js?v=ee3c3f9e45a296f9"
Shell cwd was reset to <repo>
```

*The agent runs `curl -s -m 5 'http://localhost:9090/static/app.js?v=ee3c3f9e45a296f9' -o <scratch> grep -o -i '.\{300\}\(in-stock\|in stock\|instock\|4 stars\).\{300\}' <scratch> | head -8`*

```
(Bash completed with no output)
```

*The agent runs `cd <scratch> && wc -c app.js; grep -o -i '.\{150\}\(stock\|rating\|Apply filters\).\{150\}' app.js | head -8; grep -o -i '.\{150\}\(Apply filters\|Categories\|All products\).\{150\}' products.html | head -5`*

```
48578 app.js
Shell cwd was reset to <repo>
```

**Agent:**

The server HTML doesn't contain the filter text as expected, so I'm doing one more quick check of the markup before writing the file.

*The agent runs `cd <scratch> && grep -n -i 'apply\|stock\|stars\|type="checkbox"' products.html | head -20`*

```
266:            <input type="checkbox" name="category" value="Audio" >
272:            <input type="checkbox" name="category" value="Displays" >
278:            <input type="checkbox" name="category" value="Furniture" >
284:            <input type="checkbox" name="category" value="Health" >
290:            <input type="checkbox" name="category" value="Home Office" >
296:            <input type="checkbox" name="category" value="Imaging" >
302:            <input type="checkbox" name="category" value="Outdoors" >
308:            <input type="checkbox" name="category" value="Productivity" >
314:            <input type="checkbox" name="category" value="Travel" >
345:          <input type="checkbox" name="rating" value="4" >
346:          <span>4 stars &amp; up</span>
353:          <input type="checkbox" name="availability" value="in_stock" >
... (9 more lines)
```

*The agent reads `<scratch>`*

*The agent runs `sed -n '336,361p' <scratch>`*

```
          </div>
          <input type="hidden" name="price_min" value="39.50">
          <input type="hidden" name="price_max" value="899.00">
        </div>
      </fieldset>

      <fieldset class="filter-group">
        <legend>Rating</legend>
        <label class="filter-checkbox">
          <input type="checkbox" name="rating" value="4" >
          <span>4 stars &amp; up</span>
        </label>
... (14 more lines)
```

*The agent writes `<repo>/results/lab-02/before.robot`*

```
File created successfully at: <repo>/results/lab-02/before.robot (file state is 
```

*The agent runs `rm -f <scratch> <scratch> cd <repo> && git status --short --ignored results/lab-02; git status --short`*

```
!! results/
```

**Agent:**

I saved the test to `results/lab-02/before.robot`. I didn't run it. `git status` shows no other file changed, and `results/` is ignored by git.

```robotframework
*** Test Cases ***
WEB-002_AC-5 Availability Filter
    [Documentation]    An availability filter offers an unchecked "Show in-stock only" checkbox.
    Go To Catalogue
    Checkbox Should Be Unchecked    Show in-stock only
```

- **Source:** `openspec/specs/shop/catalogue/spec.md` says the products page shows a "Show in-stock only" checkbox that starts unchecked. The test checks exactly that.
- **Style:** it follows `docs/conventions.md` and matches `WEB-002_AC-4 Rating Filter` in `tests/ui/catalogue.robot`. The name starts with the criterion ID, the tags are `WEB-002` and `ui`, and the setup and teardown are the same.
- **Locators:** the test file has none. It only calls keywords that already exist in `resources/catalogue.resource`, which finds the checkbox by its label inside the filter sidebar.
- **Label text:** I read the markup of the running shop's `/products` page without changing anything. The checkbox's label reads exactly "Show in-stock only", so looking it up by label also matches the text a shopper sees.

This matters for the lab: I read `docs/conventions.md`, the specs and the existing suite before writing, even though `AGENTS.md` doesn't point to them yet. So this "before" probably already looks like what a good `AGENTS.md` should produce, and the difference in step 7 may be smaller than the lab expects.

## Step 3 - Write AGENTS.md

*In the lab you write `AGENTS.md` yourself, in an editor. For the reference solution, the rehearsal lets the agent draft it from the same checklist.*

**Prompt:**

> Rewrite AGENTS.md following the checklist in step 3 of labs/lab-02-context/INSTRUCTIONS.md: a short section each for environment, system under test, conventions (a link to docs/conventions.md, not a copy), specifications and boundaries. Leave out secrets, anything from .env, lists of files, tests or keywords, and prose. Keep it to about 40 lines. Do not change CLAUDE.md.

*The agent reads `<repo>/labs/lab-02-context/INSTRUCTIONS.md`*

*The agent runs `git ls-files | grep -v '^labs/' | head -100 && echo --- && ls docs specs openspec 2>/dev/null`*

```
Exit code 2
.agents/skills/.openspec-target
.agents/skills/openspec-apply-change/SKILL.md
.agents/skills/openspec-archive-change/SKILL.md
.agents/skills/openspec-explore/SKILL.md
.agents/skills/openspec-propose/SKILL.md
.agents/skills/openspec-sync-specs/SKILL.md
.agents/skills/openspec-update-change/SKILL.md
.claude/commands/opsx/apply.md
.claude/commands/opsx/archive.md
.claude/commands/opsx/explore.md
.claude/commands/opsx/propose.md
... (100 more lines)
```

*The agent runs `git ls-files | grep -v '^labs/\|^\.\(agents\|claude\|github\)/\|^openspec/changes/archive' | sed -n '1,400p' | grep -v '^docs/\|^agents/\|^hooks/\|^mcp/' ; echo ---; ls labs labs/lab-02-context; echo ---; ls openspec/specs openspec/specs/*`*

```
.env.example
.gitignore
.python-version
AGENTS.md
CLAUDE.md
GLOSSARY.md
LICENSE
README.md
SETUP.md
openspec/changes/ci-and-site/.openspec.yaml
openspec/changes/ci-and-site/proposal.md
openspec/changes/workshop-labs/.openspec.yaml
... (85 more lines)
```

*The agent reads `<repo>/docs/conventions.md`*

*The agent reads `<repo>/labs/lab-02-context/checklist.md`*

*The agent reads `<repo>/robot.toml`*

*The agent reads `<repo>/openspec/specs/workshop/agent-context/spec.md`*

*The agent reads `<repo>/openspec/changes/workshop-labs/specs/workshop/agent-context/spec.md`*

*The agent runs `grep -n -i -A3 'lab.02\|lab 2\|AGENTS' tools/check_labs.py | head -80; echo ---; grep -n -i -B2 -A12 'lab 2\|AGENTS.md' openspec/changes/workshop-labs/specs/workshop/labs/spec.md openspec/changes/workshop-labs/specs/workshop/solutions/spec.md | head -120`*

```
23:    "lab-02-context": ("2", 25, "clean"),
24-    "lab-03-skills": ("3", 25, "clean"),
25-    "lab-04-robotcode": ("4", 25, "clean"),
26-    "lab-05-prompt-to-green": ("5", 30, "clean"),
---
openspec/changes/workshop-labs/specs/workshop/labs/spec.md-21-#### Scenario: Checking time budgets
openspec/changes/workshop-labs/specs/workshop/labs/spec.md-22-- **WHEN** the lab time budgets are compared with the timetable
openspec/changes/workshop-labs/specs/workshop/labs/spec.md:23:- **THEN** Lab 2 and Lab 3 have 25 minutes, Lab 4 25, Lab 5 30, Lab 6 25, Lab 7 20, Lab 8 12 and Lab 9 15, and Lab 0 fills its 30-minute m
openspec/changes/workshop-labs/specs/workshop/labs/spec.md-24-
openspec/changes/workshop-labs/specs/workshop/labs/spec.md-25-### Requirement: Done is checkable
openspec/changes/workshop-labs/specs/workshop/labs/spec.md-26-Every `checklist.md` SHALL list what "done" looks like as items a participant can check without a facilitator: a file that exists, a comma
openspec/changes/workshop-labs/specs/workshop/labs/spec.md-27-
... (23 more lines)
```

*The agent runs `ls transcripts 2>&1; sed -n '1,60p' shop/__main__.py; echo ---; cat shop/compose.yaml; echo ---; sed -n '1,80p' pyproject.toml; echo ---; grep -o '^[A-Z_]*=' .env.example`*

```
ls: cannot access 'transcripts': No such file or directory
"""The shop helper: ``uv run python -m shop <command>`` (spec: workshop/shop-access).

    status          version, space, and the presets that hold in the space
    presets         the preset names the shop offers
    preset NAME     apply a preset in the current space
    reset           reset the current space: its flags, cart and runtime orders
    wait            wait until the shop answers its health check

Every request carries the space from SHOP_SPACE. Output never names individual
planted-bug flags, and ``presets`` prints no descriptions: the shop's own
descriptions say which behaviours some presets break, which is what the
... (112 more lines)
```

**Agent:**

Checked the lab checklist, conventions, robot.toml and specs. Now I'll confirm a couple of facts before writing the file.

*The agent runs `sed -n '1,25p' openspec/specs/shop/interpretation-rules/spec.md; echo ---; grep -n '^#\|Criterion\|AC-' openspec/specs/shop/catalogue/spec.md | head -15; echo ---; uv run --no-sync robotcode --help 2>&1 | grep -n -i 'profile' | head -5`*

```
# shop/interpretation-rules Specification

## Purpose
Defines how every requirement under `shop/*` is read and checked, so that a test written from these specs passes or fails for the same reasons as the shop's own acceptance checks.

## Requirements

### Requirement: Clean state
Every requirement under `shop/*` SHALL hold in a freshly reset workshop space, in which the seeded catalogue of 12 products is unchanged and the cart is empty unless a requirement says otherwise.

#### Scenario: After a reset
- **WHEN** a participant resets their space and then checks any `shop/*` requirement
... (35 more lines)
```

*The agent writes `<repo>/AGENTS.md`*

```
The file <repo>/AGENTS.md has been updated successfully. (file state is current 
```

*The agent runs `wc -l AGENTS.md && git status --short && cat CLAUDE.md`*

```
38 AGENTS.md
 M AGENTS.md
@AGENTS.md
```

**Agent:**

I rewrote `AGENTS.md` using the step 3 checklist. It's 38 lines, and `CLAUDE.md` still contains only `@AGENTS.md`. Nothing else changed, and I haven't committed anything.

It has five sections:

- **Environment:** how to install and check the setup, how to run the whole suite and a single test (`-t "<test name>"`), that `-p shared` selects the shared instance, and that output goes to `results/`.
- **System under test:** what the shop is, how to start it locally on `localhost:9090`, that the shared instance is set up in `.env`, and that `python -m shop status` shows its state.
- **Conventions:** one line that points to `docs/conventions.md`, with none of its content copied.
- **Specifications:** `openspec/specs/shop/` has one requirement per criterion and is the reference for expected behaviour. `openspec/specs/workshop/` describes the repository, not the shop.
- **Boundaries:** never edit `resources/legacy.resource`; never apply presets or reset the shop, whether from a test or on the agent's own initiative; never read `.env`; never install tools the repository doesn't pin (no `pip`, no `rfbrowser init`); and never edit shop specs to match what the shop actually does.

Things you might want to check:

- **`-p shared` placement:** the old file said to "add `-p shared`" to `uv run robotcode robot`. But `-p` is an option of `robotcode` itself, not of `robot`, so it has to come first: `uv run robotcode -p shared robot`. That's how the new file shows it, and it matches the comment in `robot.toml`.
- **No setting names:** I left out `SHOP_URL` and `SHOP_SPACE` because you said to leave out anything from `.env`. The file only says the shared instance is configured there.
- **Two boundaries I added:** "not on your own initiative" for presets and resets, and "don't edit shop specs." Neither is in the lab's example list; remove them if they go further than you want.

I stopped at step 3. Step 4, moving one section into `docs/agent-environment.md`, isn't done.

## Step 4 - Move one section into its own file

**Prompt:**

> Move the Environment section of AGENTS.md into docs/agent-environment.md, and leave one line in AGENTS.md: "Before installing anything or running tests, read docs/agent-environment.md."

*The agent writes `<repo>/docs/agent-environment.md`*

```
File created successfully at: <repo>/docs/agent-environment.md (file state is cu
```

*The agent edits `<repo>/AGENTS.md`*

```
The file <repo>/AGENTS.md has been updated successfully. (file state is current 
```

*The agent runs `sed -n '1,8p' AGENTS.md && wc -l AGENTS.md docs/agent-environment.md && git status --short && cat CLAUDE.md`*

```
# AGENTS.md

Participant repository of the workshop "Agentic Engineering with Robot Framework": a Robot Framework suite that
tests the demo shop.

Before installing anything or running tests, read docs/agent-environment.md.

## System under test
  31 AGENTS.md
   8 docs/agent-environment.md
  39 total
 M AGENTS.md
... (2 more lines)
```

**Agent:**

I moved the Environment section into `docs/agent-environment.md`. It has an `# Environment` heading and the same six bullets, unchanged.

In `AGENTS.md`, the section (heading included) is now just your line, right under the intro: "Before installing anything or running tests, read docs/agent-environment.md." That brings `AGENTS.md` down to 31 lines. `CLAUDE.md` still contains only `@AGENTS.md`, and I haven't committed anything.

The line is plain text rather than a Markdown link, as you worded it. That's fine for agents, which read the path either way. If you'd like it clickable when viewed on GitHub, I can change it to `[docs/agent-environment.md](docs/agent-environment.md)`, matching the conventions line.

Next in the lab is step 5: start a new session and check that `/memory` lists `AGENTS.md` through `CLAUDE.md`.

**The participant runs** `wc -l AGENTS.md && cat AGENTS.md`:

```
31 AGENTS.md
# AGENTS.md

Participant repository of the workshop "Agentic Engineering with Robot Framework": a Robot Framework suite that
tests the demo shop.

Before installing anything or running tests, read docs/agent-environment.md.

## System under test

- The demo shop: a web shop with a UI and an API, run from a published image pinned in `shop/compose.yaml`.
- Local (default): `docker compose -f shop/compose.yaml up -d`, then `http://localhost:9090`.
... (20 more lines)
```

## Step 5 - Check that the agent loads it

*`/memory` is interactive; the rehearsal shows the entry point instead.*

**The participant runs** `cat CLAUDE.md`:

```
@AGENTS.md
```

## Step 6 - The "after"

**Prompt:**

> Write a Robot Framework test for criterion WEB-002_AC-5 of this repository and save it as results/lab-02/after.robot. Do not run it, and do not change any other file.

**Agent:**

I'll start with the documents the repo tells me to read first.

*The agent reads `<repo>/docs/agent-environment.md`*

*The agent reads `<repo>/docs/conventions.md`*

*The agent runs `grep -rn "WEB-002" openspec/specs/shop/ | head -50; ls results results/lab-02 2>/dev/null; git ls-files | grep -v '^\.' | head -200`*

```
openspec/specs/shop/catalogue/spec.md:8:### Requirement: Full product grid (WEB-002_AC-1)
openspec/specs/shop/catalogue/spec.md:15:### Requirement: Category filter group (WEB-002_AC-2)
openspec/specs/shop/catalogue/spec.md:22:### Requirement: Price range filter (WEB-002_AC-3)
openspec/specs/shop/catalogue/spec.md:29:### Requirement: Rating filter (WEB-002_AC-4)
openspec/specs/shop/catalogue/spec.md:36:### Requirement: Availability filter (WEB-002_AC-5)
openspec/specs/shop/catalogue/spec.md:43:### Requirement: Apply filters (WEB-002_AC-6)
openspec/specs/shop/catalogue/spec.md:50:### Requirement: Category filter application (WEB-002_AC-7)
openspec/specs/shop/catalogue/spec.md:57:### Requirement: Price range filter application (WEB-002_AC-8)
openspec/specs/shop/catalogue/spec.md:64:### Requirement: Combined filters (WEB-002_AC-9)
openspec/specs/shop/catalogue/spec.md:71:### Requirement: Reset filters (WEB-002_AC-10)
openspec/specs/shop/catalogue/spec.md:78:### Requirement: Collections to explore (WEB-002_AC-11)
openspec/specs/shop/catalogue/spec.md:85:### Requirement: Handpicked highlights (WEB-002_AC-12)
... (149 more lines)
```

*The agent reads `<repo>/openspec/specs/shop/catalogue/spec.md`*

*The agent reads `<repo>/openspec/specs/shop/interpretation-rules/spec.md`*

*The agent reads `<repo>/resources/catalogue.resource`*

*The agent reads `<repo>/tests/ui/catalogue.robot`*

*The agent reads `<repo>/results/lab-02/before.robot`*

*The agent reads `<repo>/labs/lab-02-context/INSTRUCTIONS.md`*

**Agent:**

The spec is clear: a "Show in-stock only" checkbox, unchecked by default. Next I'll check the shared resources, the run config and the locator hook, so the test only uses keywords that already exist.

*The agent reads `<repo>/resources/shop.resource`*

*The agent reads `<repo>/robot.toml`*

*The agent reads `<repo>/hooks/no_inline_locators.py`*

*The agent reads `<repo>/openspec/specs/workshop/test-conventions/spec.md`*

*The agent writes `<repo>/results/lab-02/after.robot`*

```
File created successfully at: <repo>/results/lab-02/after.robot (file state is c
```

*The agent runs `uv run --no-sync python hooks/no_inline_locators.py results/lab-02/after.robot; echo "exit=$?"; diff results/lab-02/before.robot results/lab-02/after.robot && echo identical; git status --short`*

```
exit=0
identical
 M AGENTS.md
?? docs/agent-environment.md
```

**Agent:**

I wrote the test to `results/lab-02/after.robot`. I didn't run it, and I changed no other file (`git status` shows the same two changes as before, and `results/` is ignored by git).

```robotframework
WEB-002_AC-5 Availability Filter
    [Documentation]    An availability filter offers an unchecked "Show in-stock only" checkbox.
    Go To Catalogue
    Checkbox Should Be Unchecked    Show in-stock only
```

How it follows the repo's rules:
- **Spec:** it checks what `openspec/specs/shop/catalogue/spec.md` says for WEB-002_AC-5: a "Show in-stock only" checkbox that is unchecked by default. The label is copied exactly from the spec.
- **Locators:** the test file has none. The repo's locator checker (`hooks/no_inline_locators.py`) passes on it. It reuses the existing keywords `Go To Catalogue` and `Checkbox Should Be Unchecked` from `resources/catalogue.resource`. That keyword finds the checkbox by its label inside the filter sidebar, which the spec's rules allow for a form field. The match ignores case and accepts the phrase inside a longer label.
- **Name, tags and isolation:** the name starts with `WEB-002_AC-5`, the tags are `WEB-002` and `ui`, and each test gets its own browser context through `Start Shop Test`. There are no presets or resets.

**For step 7 of the lab:** `after.robot` is identical to the existing `before.robot`. With the keyword already in the resources and the spec this clear, there was only one sensible test to write. So in this run, the new `AGENTS.md` didn't change the result; it changed what I checked before writing it.

The spec also says the checkbox is "shown", but the test doesn't check that it's visible. The only way would be a new keyword in `resources/`, and that would have meant changing another file.

## Step 7 - Compare

**The participant runs** `diff results/lab-02/before.robot results/lab-02/after.robot`:

*(no output)*

## Stretch - A nested AGENTS.md for the API tests

**Prompt:**

> Create tests/api/AGENTS.md with only what API tests need: they use resources/api.resource and its session shop, and they are tagged api. Keep it under 10 lines.

*The agent runs `ls tests tests/api 2>&1; find . -name AGENTS.md -not -path './node_modules/*' -not -path './.venv/*'; cat resources/api.resource`*

```
tests:
api
ui

tests/api:
smoke.robot
./AGENTS.md
*** Settings ***
Documentation       The shop's API, in the configured workshop space.

Library             Collections
Library             RequestsLibrary
... (20 more lines)
```

*The agent reads `<repo>/tests/api/smoke.robot`*

*The agent writes `<repo>/tests/api/AGENTS.md`*

```
File created successfully at: <repo>/tests/api/AGENTS.md (file state is current 
```

*The agent edits `<repo>/tests/api/AGENTS.md`*

```
The file <repo>/tests/api/AGENTS.md has been updated successfully. (file state i
```

**Agent:**

I created `tests/api/AGENTS.md`. It's 7 lines:

```markdown
# AGENTS.md

API tests for the demo shop.

- Import `resources/api.resource` and call `Open Shop API` in `Suite Setup`.
- Send requests through its session `shop`, which sends your space in `X-Workshop-Space`.
- Tag every test `api`, with `Test Tags` in the suite settings.
```

I based the bullets on `resources/api.resource` and `tests/api/smoke.robot`. The session is called `shop`, it's created by `Open Shop API`, and the space header is added only when a space is set. Everything else stays in the root `AGENTS.md`. I haven't committed the file.
