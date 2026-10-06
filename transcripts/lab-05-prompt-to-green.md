# Lab 5 - Prompt to green: the recorded walkthrough

*Recorded with Claude Code 2.1.281, without an MCP server, from the lab's instructions. Results are shortened; your agent's answers will differ in wording.*

## Step 2 - Propose

**Prompt:**

> /opsx:propose Automate WEB-004_AC-1, WEB-004_AC-3, WEB-004_AC-6 and WEB-004_AC-7 from labs/lab-05-prompt-to-green/stories/WEB-004_search_products.md as Robot Framework UI tests. The expected behaviour is in openspec/specs/shop/search.

*The agent runs `openspec list --json; echo "---"; openspec context --json`*

*The agent reads `<repo>/labs/lab-05-prompt-to-green/stories/WEB-004_search_products.md`*

```
{
  "changes": [
    {
      "name": "workshop-labs",
      "completedTasks": 25,
      "totalTasks": 37,
      "lastModified": "2026-09-24T19:46:53.373Z",
      "status": "in-progress"
    },
    {
      "name": "ci-and-site",
      "completedTasks": 0,
... (20 more lines)
```

*The agent runs `cat openspec/config.yaml 2>/dev/null || cat openspec/config.yml; echo "---"; ls -R openspec | head -100; echo "---"; ls openspec/specs/shop/search; ls docs`*

```
schema: spec-driven
githubCopilot:
  cloudAgent: false

# Shown to every agent that creates an OpenSpec artifact in this repository.
context: |
  This is the participant repository of the workshop "Agentic Engineering with
  Robot Framework". The system under test is the demo shop, which runs from a
  published image (shop/compose.yaml); its source is not in this repository.

  Specs live in three namespaces:
  - shop/*      What the demo shop does, as a shopper or an API consumer experiences
... (130 more lines)
```

*The agent reads `<repo>/openspec/specs/shop/search/spec.md`*

*The agent reads `<repo>/docs/conventions.md`*

*The agent reads `<repo>/docs/agent-environment.md`*

*The agent runs `ls -R openspec/specs openspec/changes/archive/2026-09-25-add-cart-ui-tests openspec/changes/archive/2026-09-25-add-product-detail-ui-tests; ls -R resources tests labs/lab-05-prompt-to-green`*

```
openspec/changes/archive/2026-09-25-add-cart-ui-tests:
design.md
proposal.md
specs
tasks.md

openspec/changes/archive/2026-09-25-add-cart-ui-tests/specs:
suite

openspec/changes/archive/2026-09-25-add-cart-ui-tests/specs/suite:
cart

... (122 more lines)
```

*The agent runs `for f in openspec/changes/archive/2026-09-25-add-product-detail-ui-tests/*.md openspec/changes/archive/2026-09-25-add-product-detail-ui-tests/specs/suite/product-detail/spec.md openspec/specs/suite/product-detail/spec.md; do echo "=== $f"; cat "$f"; done`*

```
<persisted-output>
Output too large (41.7KB). Full output saved to: ~/.claude/projects/-tmp-claude-1000--mnt-c-workspace-ai-engineering-robotframework-6fe17ce9-00bd-4179-bc22-dbf725b60a81-scratchpad-rehearsal-

Preview (first 2KB):
=== openspec/changes/archive/2026-09-25-add-product-detail-ui-tests/design.md
# Design

## Context

See `proposal.md` for the motivation and `specs/suite/product-detail/spec.md` for what each test checks. The facts
below come from the local shop at version `0.3.0`: its served HTML for `/products/1`, `/products/9999`,
`/products/abc` and `/products`, its `/static/app.js`, and `GET /api/products/1`. The space was in its reset state:
... (18 more lines)
```

*The agent runs `for f in openspec/changes/archive/2026-09-25-add-cart-ui-tests/*.md openspec/specs/suite/cart/spec.md; do echo "=== $f"; cat "$f"; done`*

```
<persisted-output>
Output too large (35.6KB). Full output saved to: ~/.claude/projects/-tmp-claude-1000--mnt-c-workspace-ai-engineering-robotframework-6fe17ce9-00bd-4179-bc22-dbf725b60a81-scratchpad-rehearsal-

Preview (first 2KB):
=== openspec/changes/archive/2026-09-25-add-cart-ui-tests/design.md
# Design

## Context

See `proposal.md` for the motivation and `specs/suite/cart/spec.md` for what each test checks. The facts below come
from the local shop at version `0.3.0`, with the space in its reset state (`clean` and `stage1` both hold). They were
read from:
... (22 more lines)
```

*The agent reads `~/.claude/projects/-tmp-claude-1000--mnt-c-workspace-ai-engineering-robotframework-6fe17ce9-00bd-4179-bc22-dbf725b60a81-scratchpad-rehearsal-repo/6e039e5c-afd4-4924-9827-186807b90739/tool-results/bit51d5go.txt`*

*The agent reads `~/.claude/projects/-tmp-claude-1000--mnt-c-workspace-ai-engineering-robotframework-6fe17ce9-00bd-4179-bc22-dbf725b60a81-scratchpad-rehearsal-repo/6e039e5c-afd4-4924-9827-186807b90739/tool-results/b262qxgep.txt`*

*The agent runs `cat labs/lab-05-prompt-to-green/INSTRUCTIONS.md labs/lab-05-prompt-to-green/checklist.md; echo ===; cat openspec/specs/shop/interpretation-rules/spec.md`*

```
# Lab 5 - Prompt to green

Turn a user story into a green, convention-following test suite, the way you would with a junior engineer: agree on a
plan first, review it with a colleague, then let the work happen, run it, and refine. The vehicle is
[OpenSpec](../../GLOSSARY.md#openspec): a propose step that writes the plan down before any code exists. You finish
by debugging a broken test in conversation, without looking at the live page.

| | |
|---|---|
| Module | 5 - Natural Prompt Automation & Debugging |
| Time | 30 minutes |
| Shop preset | `clean` |
... (182 more lines)
```

*The agent runs `cat resources/shop.resource resources/catalogue.resource; echo ===DIFF; git diff resources/catalogue.resource resources/api.resource tests/ui/catalogue.robot AGENTS.md`*

```
*** Settings ***
Documentation       The browser and the shop's pages.
...
...                 One browser per suite and one context per test, so every test starts
...                 with its own cookies and an empty cart. When ${SHOP_SPACE} is set,
...                 every request the context sends - pages, assets and API calls - carries
...                 that workshop space.

Library             Browser


*** Variables ***
... (262 more lines)
```

*The agent runs `cat tests/ui/catalogue.robot tests/ui/product_detail.robot; cat robot.toml; ls; ls hooks`*

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

... (196 more lines)
```

*The agent runs `cat resources/legacy.resource resources/product_detail.resource; grep -rni "search" resources tests openspec/specs/workshop openspec/specs/suite | head -40`*

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
... (183 more lines)
```

*The agent runs `uv run --no-sync python -m shop status 2>&1 | head -30`*

```
shop     http://localhost:9090  (version 0.3.0)
space    default
presets  clean, stage1
```

*The agent runs `cd /tmp && curl -s http://localhost:9090/ -o /tmp/home.html -w "%{http_code}\n"; curl -s http://localhost:9090/products -o /tmp/products.html -w "%{http_code}\n"; wc -c /tmp/home.html /tmp/products.html; grep -o '<script[^>]*>' /tmp/home.html; grep -o '<link[^>]*>' /tmp/home.html`*

```
200
200
 47922 /tmp/home.html
 55735 /tmp/products.html
103657 total
<script src="/static/app.js?v=ee3c3f9e45a296f9" defer>
<script type="application/ld+json">
<link rel="stylesheet" href="/assets/styles.bcca56d0f15fa943.css" />
Shell cwd was reset to <repo>
```

*The agent runs `cd /tmp && python3 - <<'EOF'
import re
for name in ["home","products"]:
    html=open(f"/tmp/{name}.html").read()
    print("=====",name)
    # find search-related fragments
    for m in re.finditer(r'(?i)search', html):
        pass
    idxs=[m.start() for m in re.finditer(r'(?i)<form|search|results|clear', html)]
    # print regions around forms and search
    shown=set()
    for i in idxs:
        s=max(0,i-300)//200*200
        if s in shown: continue
        shown.add(s)
    # simpler: print all lines containing search/form/results/clear with context
    lines=html.splitlines()
    for n,l in enumerate(lines):
        if re.search(r'(?i)search|<form|results|clear|No products|hero', l):
            print(n, l.strip()[:300])
EOF`*

```
===== home
242 <section class="hero">
243 <div class="hero__content">
244 <span class="hero__badge">Spring '25 Collection</span>
245 <h1 class="hero__title">Upgrade your workspace with AI-first essentials</h1>
246 <p class="hero__subtitle">
250 <form class="hero__search" role="search">
251 <label class="form-field" aria-label="Search products">
259 <input type="search" name="query" placeholder="Search headphones, notebooks, wearables..."
260 autocomplete="off" data-test="search-input" />
264 <div class="search-suggest" hidden>
265 <ul class="search-suggest__list" role="listbox" id="search-suggestions">
... (42 more lines)
```

**Agent:**

Reading the shop's home page markup and `app.js` to see how search, clearing and the empty state behave.

*The agent runs `sed -n 236,315p /tmp/home.html`*

```
  <main id="main-content" class="site-main">
    





<section class="hero">
  <div class="hero__content">
    <span class="hero__badge">Spring '25 Collection</span>
    <h1 class="hero__title">Upgrade your workspace with AI-first essentials</h1>
    <p class="hero__subtitle">
... (68 more lines)
```

*The agent runs `curl -s "http://localhost:9090/static/app.js?v=ee3c3f9e45a296f9" -o /tmp/app.js; wc -l /tmp/app.js; grep -n -i "search\|suggest\|clear\|No products\|empty" /tmp/app.js | head -80`*

```
1452 /tmp/app.js
14:  const SEARCH_RESULTS_ENDPOINT = "/search/results";
15:  const SEARCH_SUGGEST_ENDPOINT = "/api/search/suggest";
36:  const SEARCH_FORM_SELECTOR = 'form[role="search"]';
37:  const SEARCH_INPUT_SELECTOR = 'input[name="query"]';
38:  const SEARCH_REGION_SELECTOR = '[role="region"][aria-label="Search results"]';
136:  function clearAuth() {
168:    clearTimeout(flashTimer);
276:  // Search: the results come from the server fragment (task 9.2)
279:  function getSearchRegion() {
280:    const region = document.querySelector(SEARCH_REGION_SELECTOR);
282:    const clearButton = region.querySelector("button[aria-controls]");
... (52 more lines)
```

*The agent runs `sed -n 270,380p /tmp/app.js; echo ......; sed -n 1170,1345p /tmp/app.js`*

```
      const num = Number(value) || 0;
      return `$${num.toFixed(2)}`;
    }
  }

  // ---------------------------------------------------------------------
  // Search: the results come from the server fragment (task 9.2)
  // ---------------------------------------------------------------------

  function getSearchRegion() {
    const region = document.querySelector(SEARCH_REGION_SELECTOR);
    if (!region) return null;
... (276 more lines)
```

*The agent runs `for q in headphones xyz123 aurora; do echo "===== $q"; curl -s "http://localhost:9090/search/results?query=$q" -w "\nHTTP %{http_code}\n"; done; echo "===== suggest"; curl -s "http://localhost:9090/api/search/suggest?query=xyz123" -w "\nHTTP %{http_code}\n"; curl -s "http://localhost:9090/api/search/?query=headphones" -w "\nHTTP %{http_code}\n" | head -c 1500`*

```
===== headphones










<article class="product-card"
... (188 more lines)
```

*The agent runs `grep -rn -i "stage[1-4]\|drift" docs openspec/specs/workshop GLOSSARY.md README.md 2>/dev/null | head -30`*

```
docs/facilitator/suite-outcomes.toml:2:# Derived from the test inventory (baseline-suite design D1) and the shop's drift
docs/facilitator/suite-outcomes.toml:6:# Reasons: "broken" (fails on purpose), "drift:<kind>" (its locator kind drifts
docs/facilitator/suite-outcomes.toml:32:[presets.stage2]
docs/facilitator/suite-outcomes.toml:35:"WEB-002_AC-1 Card Prices Are The Product Prices" = ["drift:class"]
docs/facilitator/suite-outcomes.toml:36:"WEB-002_AC-7 Audio Filter Shows Only Audio" = ["drift:class"]
docs/facilitator/suite-outcomes.toml:37:"WEB-006_AC-7 Successful Order" = ["drift:id"]
docs/facilitator/suite-outcomes.toml:39:[presets.stage3]
docs/facilitator/suite-outcomes.toml:42:"WEB-006_AC-1 Order Total Adds Up" = ["drift:data-test"]
docs/facilitator/suite-outcomes.toml:43:"WEB-006_AC-7 Successful Order" = ["drift:id"]
docs/facilitator/suite-outcomes.toml:45:[presets.stage4]
docs/facilitator/suite-outcomes.toml:48:"WEB-002_AC-1 Card Prices Are The Product Prices" = ["drift:class"]
docs/facilitator/suite-outcomes.toml:49:"WEB-002_AC-7 Audio Filter Shows Only Audio" = ["drift:class"]
... (18 more lines)
```

*The agent runs `git log --all --oneline -- '*search*' | head; git branch -a; ls transcripts 2>/dev/null; ls openspec/changes/workshop-labs openspec/changes/ci-and-site`*

```
4ff478c feat(labs): suite namespace, lab folders, stories, lab checker, skills and hooks
6de5eeb chore(openspec): archive shop-specs
e28f7e3 chore(openspec): plan the participant repository in five changes
* apply-workshop-labs
  remotes/origin/HEAD -> origin/apply-workshop-labs
  remotes/origin/apply-baseline-suite
  remotes/origin/apply-shop-specs
  remotes/origin/apply-workshop-labs
  remotes/origin/archive-baseline-suite
  remotes/origin/archive-workshop-foundation
  remotes/origin/fix-tracked-bytecode
  remotes/origin/main
... (10 more lines)
```

*The agent runs `grep -rn -i "search" openspec/changes/workshop-labs openspec/specs/workshop/baseline-suite/spec.md | head -30; cat hooks/no_inline_locators.py | head -60`*

```
openspec/changes/workshop-labs/proposal.md:13:- **Module 5 becomes spec-driven.** The participant picks one story - WEB-004 search (easier), WEB-003 product detail (medium) or WEB-005 cart (harder) - 
openspec/changes/workshop-labs/design.md:78:| WEB-004 search | easier | AC-1, AC-3, AC-6, AC-7 |
openspec/changes/workshop-labs/design.md:86:The participant's change writes its delta specs to **`suite/<area>`**, named after the `shop/*` area it verifies, for example `suite/search`. Each requireme
openspec/changes/workshop-labs/design.md:116:  - the reviewer can read and search only;
openspec/specs/workshop/baseline-suite/spec.md:68:#### Scenario: Searching the test files
openspec/specs/workshop/baseline-suite/spec.md:69:- **WHEN** the test files are searched for locator literals
openspec/specs/workshop/baseline-suite/spec.md:108:- **WHEN** the suite's files are searched for `BUG_`, `LOCATOR_` and the names of the planted-bug presets
"""Reject locator literals in test files: convention 2, "Locators live in resources".

As a hook (before an edit): refuses an edit that writes a locator literal into a .robot file
under tests/. As a command, it reports every locator literal in the given files or folders:

... (55 more lines)
```

*The agent writes `/tmp/search-probe/probe.robot`*

```
Claude requested permissions to write to /tmp/search-probe/probe.robot, but you haven't granted it yet.
```

*The agent runs `ls -la <scratch> <scratch>`*

```
<scratch>
total 68380
drwx------ 50 user user    12288 Sep 25 08:15 .
drwx------  4 user user     4096 Sep 19 07:04 ..
-rwxr-xr-x  1 user user    26740 Sep 21 16:31 CONF.bak
-rwxr-xr-x  1 user user     7059 Sep 21 16:31 W2.bak
drwxr-xr-x  2 user user     4096 Sep 19 21:36 __pycache__
-rwxr-xr-x  1 user user      956 Sep 19 08:54 admin.py.bak
-rwxr-xr-x  1 user user    48290 Sep 22 09:41 app.js.fixed
-rwxr-xr-x  1 user user    48578 Sep 22 12:27 app.js.searchfix
drwxr-xr-x  3 user user     4096 Sep 24 16:59 archive-trial
drwxr-xr-x  9 user user     4096 Sep 24 12:19 archive-trial-shop
... (282 more lines)
```

*The agent runs `timeout 60 uv run --no-sync robotcode repl --help 2>&1 | head -50`*

```
Usage: robotcode repl [OPTIONS] [FILES]...

  Run Robot Framework interactively (alias `shell`).

  Starts an interactive session where you enter Robot Framework keywords and
  run them immediately. Pass FILES to execute them in the session.

Options:
  --no-history                    Don't load or save the persistent history
                                  file. In-session arrow-up recall still
                                  works, but nothing crosses session
                                  boundaries. Useful for AI-agent invocations
... (38 more lines)
```

*The agent runs `timeout 180 uv run --no-sync robotcode repl --plain --no-history -o NONE -r NONE -l NONE 2>&1 <<'EOF' | tail -80
Import Resource    ${EXECDIR}/resources/shop.resource
Import Resource    ${EXECDIR}/resources/catalogue.resource
Open Shop Browser
Start Shop Test
Go To Shop Page    /
Wait For Elements State    role=main >> role=search >> role=searchbox    visible
Get Element Count    role=main >> section:has(h1)
Get Element Count    h1
Get Element Count    role=search
Get Element Count    role=main >> section:has(h1) >> role=search >> role=searchbox
Get Element Count    role=searchbox[name=/search/i]
Get Element Count    role=searchbox[name="Search products"]
Get Attribute    role=main >> role=search >> role=searchbox    placeholder
Get Element Count    role=main >> role=search >> button:has-text("Search")
Get Element Count    role=region[name=/search results/i]
Get Text    role=main >> section >> nth=0
EOF`*

```
[ INFO ] {"browser": "chromium", "headless": true, "chromiumSandbox": false, "devtools": false, "handleSIGHUP": true, "handleSIGINT": true, "handleSIGTERM": true, "slowMo": 0.0, "timeout": 30000.0, "t
[ INFO ] Starting Browser process <repo>/.venv/lib/python3.12/site-packages/Brow
[ INFO ] Successfully created browser with options: {"browser":"chromium","headless":true,"chromiumSandbox":false,"devtools":false,"handleSIGHUP":true,"handleSIGINT":true,"handleSIGTERM":true,"slowMo"
[ INFO ] {
  "acceptDownloads": true,
  "baseURL": "http://localhost:9090",
  "bypassCSP": false,
  "forcedColors": "none",
  "ignoreHTTPSErrors": false,
  "javaScriptEnabled": true,
  "offline": false,
  "reducedMotion": "no-preference",
... (13 more lines)
```

*The agent runs `timeout 180 uv run --no-sync robotcode repl --plain --no-history -o NONE -r NONE -l NONE 2>&1 <<'EOF' | grep -E "^(P |FAIL|\[ FAIL|Error)|P:" 
Import Resource    ${EXECDIR}/resources/shop.resource
Import Resource    ${EXECDIR}/resources/catalogue.resource
Open Shop Browser
Start Shop Test
Go To Shop Page    /
Wait For Elements State    role=main >> role=search >> role=searchbox    visible
${n}=    Get Element Count    role=main >> section:has(h1)
Log To Console    P: hero section:has(h1)=${n}
${n}=    Get Element Count    h1
Log To Console    P: h1 on page=${n}
${n}=    Get Element Count    role=search
Log To Console    P: role=search on page=${n}
${n}=    Get Element Count    role=main >> section:has(h1) >> role=search >> role=searchbox
Log To Console    P: searchbox in hero=${n}
${n}=    Get Element Count    role=searchbox
Log To Console    P: searchboxes on page=${n}
${n}=    Get Element Count    role=searchbox[name=/search/i]
Log To Console    P: searchbox named /search/i=${n}
${n}=    Get Element Count    role=searchbox[name="Search products"]
Log To Console    P: searchbox named exactly Search products=${n}
${n}=    Get Element Count    role=main >> role=search >> button:has-text("Search")
Log To Console    P: search button=${n}
${n}=    Get Element Count    role=main >> role=search >> role=button
Log To Console    P: buttons in search form=${n}
${n}=    Get Element Count    role=region[name=/search results/i]
Log To Console    P: results region while hidden=${n}
${n}=    Get Element Count    role=main >> section >> nth=0 >> h1
Log To Console    P: first section holds h1=${n}
Go To Shop Page    /products
Wait For Elements State    role=main >> role=search >> role=searchbox    visible
${n}=    Get Element Count    role=search
Log To Console    P: products role=search=${n}
${n}=    Get Element Count    role=searchbox[name=/search/i]
Log To Console    P: products searchbox named /search/i=${n}
${ph}=    Get Attribute    role=main >> role=search >> role=searchbox    placeholder
Log To Console    P: products placeholder=${ph}
${n}=    Get Element Count    role=main >> section:has(h1)
Log To Console    P: products section:has(h1)=${n}
EOF`*

```
P: hero section:has(h1)=1
P: h1 on page=1
P: role=search on page=1
P: searchbox in hero=1
P: searchboxes on page=1
P: searchbox named /search/i=1
P: searchbox named exactly Search products=1
P: search button=1
P: buttons in search form=1
P: results region while hidden=0
P: first section holds h1=1
P: products role=search=1
... (3 more lines)
```

**Agent:**

The locators for the search form work on both pages. Next I'm checking the full flow in the browser: submit, results, clear, and the empty state.

*The agent runs `timeout 240 uv run --no-sync robotcode repl --plain --no-history -o NONE -r NONE -l NONE 2>&1 <<'EOF' | grep -E "P:|FAIL|Error"
Import Resource    ${EXECDIR}/resources/shop.resource
Import Resource    ${EXECDIR}/resources/catalogue.resource
VAR    ${R}    role=region[name=/search results/i]    scope=GLOBAL
VAR    ${I}    role=main >> role=search >> role=searchbox    scope=GLOBAL
VAR    ${C}    ${R} >> article:has-text("Aurora Neural Headphones")    scope=GLOBAL
VAR    ${CLR}    ${R} >> :is(button:has-text("Clear search"), button:has-text("Clear results"))    scope=GLOBAL
Open Shop Browser
Start Shop Test
Go To Shop Page    /
Fill Text    ${I}    headphones
Keyboard Key    press    Enter
Wait For Elements State    ${C}    visible
${n}=    Get Element Count    ${R} >> role=article
Log To Console    P: articles=${n}
${n}=    Get Element Count    ${C}
Log To Console    P: aurora cards=${n}
${n}=    Get Element Count    ${C} >> role=img
Log To Console    P: card role=img=${n}
${n}=    Get Element Count    ${C} >> role=img[name=/Aurora Neural Headphones/i]
Log To Console    P: card named img=${n}
Wait For Elements State    ${C} >> role=img[name=/Aurora Neural Headphones/i]    visible
${w}=    Get Property    ${C} >> role=img[name=/Aurora Neural Headphones/i]    naturalWidth
Log To Console    P: naturalWidth=${w}
${t}=    Get Text    ${C} >> role=heading
Log To Console    P: card heading=${t}
${n}=    Get Element Count    ${C} >> ${CARD PRICE}
${p}=    Get Text    ${C} >> ${CARD PRICE}
Log To Console    P: price count=${n} text=${p}
${n}=    Get Element Count    ${CLR}
${t}=    Get Text    ${CLR}
Log To Console    P: clear buttons=${n} text=${t}
${n}=    Get Element Count    ${R} >> role=heading
Log To Console    P: region headings=${n}
${n}=    Get Element Count    role=listbox
Log To Console    P: listbox visible now=${n}
Click    ${CLR}
Wait For Elements State    ${R}    hidden
${v}=    Get Property    ${I}    value
Log To Console    P: input right after clear='${v}'
${n}=    Get Element Count    role=main >> section:has(h1)
Log To Console    P: hero after clear=${n}
Sleep    1.5s
${n}=    Get Element Count    ${R}
${v}=    Get Property    ${I}    value
${l}=    Get Element Count    role=listbox
Log To Console    P: 1.5s after quick clear: region visible count=${n} input='${v}' listbox=${l}
Go To Shop Page    /
Fill Text    ${I}    headphones
Keyboard Key    press    Enter
Wait For Elements State    ${C}    visible
Sleep    1.5s
${l}=    Get Element Count    role=listbox
Log To Console    P: settled listbox visible=${l}
Click    ${CLR}
Wait For Elements State    ${R}    hidden
Sleep    1.5s
${n}=    Get Element Count    ${R}
${v}=    Get Property    ${I}    value
${l}=    Get Element Count    role=listbox
Log To Console    P: 1.5s after settled clear: region=${n} input='${v}' listbox=${l}
Go To Shop Page    /
Fill Text    ${I}    headphones
Click    role=main >> role=search >> button:has-text("Search")
Wait For Elements State    ${C}    visible
${u}=    Get Url
Log To Console    P: url after button=${u}
EOF`*

```
  "ignoreHTTPSErrors": false,
[ INFO ] {'acceptDownloads': True, 'baseURL': 'http://localhost:9090', 'bypassCSP': False, 'forcedColors': 'none', 'ignoreHTTPSErrors': False, 'javaScriptEnabled': True, 'offline': False, 'reducedMoti
P: articles=1
P: aurora cards=1
P: card role=img=1
P: card named img=1
P: naturalWidth=1024
P: card heading=Aurora Neural Headphones
P: price count=1 text=$249.99
P: clear buttons=1 text=Clear results
P: region headings=2
P: listbox visible now=0
... (6 more lines)
```

*The agent runs `timeout 240 uv run --no-sync robotcode repl --plain --no-history -o NONE -r NONE -l NONE 2>&1 <<'EOF' | grep -E "P:|FAIL|Error"
Import Resource    ${EXECDIR}/resources/shop.resource
Import Resource    ${EXECDIR}/resources/catalogue.resource
VAR    ${R}    role=region[name=/search results/i]    scope=GLOBAL
VAR    ${I}    role=main >> role=search >> role=searchbox    scope=GLOBAL
VAR    ${C}    ${R} >> article:has-text("Aurora Neural Headphones")    scope=GLOBAL
VAR    ${CLR}    ${R} >> :is(button:has-text("Clear search"), button:has-text("Clear results"))    scope=GLOBAL
Open Shop Browser
Start Shop Test
Go To Shop Page    /products
Wait For Elements State    ${GRID}    visible
Fill Text    ${I}    headphones
Keyboard Key    press    Enter
Wait For Elements State    ${C}    visible
${s}=    Get Element States    ${GRID}
Log To Console    P: grid states while results=${s}
${t}=    Get Text    ${CLR}
Log To Console    P: products clear text=${t}
Sleep    1s
Click    ${CLR}
Wait For Elements State    ${R}    hidden
Wait For Elements State    ${GRID}    visible
${v}=    Get Property    ${I}    value
Log To Console    P: products input after clear='${v}'
Go To Shop Page    /
Fill Text    ${I}    xyz123
Keyboard Key    press    Enter
Wait For Elements State    ${R}    visible
${t}=    Get Text    ${R}
Log To Console    P: empty region text=${t}
${n}=    Get Element Count    ${R} >> text=/no products/i
Log To Console    P: 'no products' in region=${n}
${n}=    Get Element Count    ${R} >> role=article
Log To Console    P: articles in empty region=${n}
Sleep    1s
${n}=    Get Element Count    text=/no results/i
Log To Console    P: 'no results' visible on page after 1s=${n}
${n}=    Get Element Count    ${R} >> text=/no results/i
Log To Console    P: 'no results' inside region=${n}
${n}=    Get Element Count    role=main >> text=/no products|no results/i
Log To Console    P: main-wide no products|no results=${n}
${n}=    Get Element Count    role=alert
Log To Console    P: alerts=${n}
${n}=    Get Element Count    role=status
Log To Console    P: status=${n}
Go To Shop Page    /
Fill Text    ${I}    xyz123
Click    role=main >> role=search >> button:has-text("Search")
Wait For Elements State    ${R} >> text=/no products/i    visible
Log To Console    P: empty state via button ok
EOF`*

```
  "ignoreHTTPSErrors": false,
[ INFO ] {'acceptDownloads': True, 'baseURL': 'http://localhost:9090', 'bypassCSP': False, 'forcedColors': 'none', 'ignoreHTTPSErrors': False, 'javaScriptEnabled': True, 'offline': False, 'reducedMoti
P: grid states while results=['attached', 'visible', 'enabled', 'defocused']
P: products clear text=Clear search
P: products input after clear=''
P: empty region text=Search results
P: 'no products' in region=1
P: articles in empty region=0
P: 'no results' visible on page after 1s=1
P: 'no results' inside region=0
P: main-wide no products|no results=2
P: alerts=0
... (2 more lines)
```

*The agent runs `timeout 180 uv run --no-sync robotcode repl --plain --no-history -o NONE -r NONE -l NONE 2>&1 <<'EOF' | grep -E "P:|FAIL|Error"
Import Resource    ${EXECDIR}/resources/shop.resource
VAR    ${R}    role=region[name=/search results/i]    scope=GLOBAL
VAR    ${I}    role=main >> role=search >> role=searchbox    scope=GLOBAL
Open Shop Browser
Start Shop Test
Go To Shop Page    /
Fill Text    ${I}    xyz123
Keyboard Key    press    Enter
Wait For Elements State    ${R} >> text=/no products/i    visible
${t}=    Get Text    ${R} >> text=/no products/i
Log To Console    P: empty-state text=${t}
${t}=    Get Property    ${R}    innerText
Log To Console    P: region innerText=${t}
${t}=    Get Text    role=status
Log To Console    P: status text='${t}'
${t}=    Get Text    text=/no results/i
Log To Console    P: suggest empty text='${t}'
${n}=    Get Element Count    role=main >> section:has(h1) >> text=/no results/i
Log To Console    P: 'no results' inside hero=${n}
EOF`*

```
  "ignoreHTTPSErrors": false,
[ INFO ] {'acceptDownloads': True, 'baseURL': 'http://localhost:9090', 'bypassCSP': False, 'forcedColors': 'none', 'ignoreHTTPSErrors': False, 'javaScriptEnabled': True, 'offline': False, 'reducedMoti
P: empty-state text=No products matched your query.
P: region innerText=Search results
P: status text=''
P: suggest empty text='No results'
P: 'no results' inside hero=1
```

*The agent runs `timeout 180 uv run --no-sync robotcode repl --plain --no-history -o NONE -r NONE -l NONE 2>&1 <<'EOF' | grep -E "P:|FAIL|Error"
Import Resource    ${EXECDIR}/resources/shop.resource
VAR    ${R}    role=region[name=/search results/i]    scope=GLOBAL
VAR    ${I}    role=main >> role=search >> role=searchbox    scope=GLOBAL
Open Shop Browser
Start Shop Test
Go To Shop Page    /
Fill Text    ${I}    xyz123
Keyboard Key    press    Enter
Wait For Elements State    ${R} >> text=/no products/i    visible
${n}=    Get Element Count    ${R}
${tag}=    Get Property    ${R}    tagName
${tc}=    Get Property    ${R}    textContent
Log To Console    P: region count=${n} tag=${tag} textContent=${tc.split()}
${n}=    Get Element Count    ${R} >> role=heading[name=/search results/i]
Log To Console    P: heading in region=${n}
${n}=    Get Element Count    role=main >> section:has(h2:has-text("Search results"))
Log To Console    P: section:has(h2 Search results)=${n}
EOF`*

```
  "ignoreHTTPSErrors": false,
[ INFO ] {'acceptDownloads': True, 'baseURL': 'http://localhost:9090', 'bypassCSP': False, 'forcedColors': 'none', 'ignoreHTTPSErrors': False, 'javaScriptEnabled': True, 'offline': False, 'reducedMoti
P: region count=1 tag=SECTION textContent=['Search', 'results', 'Clear', 'results', 'No', 'products', 'matched', 'your', 'query.']
P: heading in region=1
P: section:has(h2 Search results)=1
```

**Agent:**

All locators resolve as expected. Creating the change `add-search-ui-tests`, following the naming of the earlier cart and product-detail changes.

*The agent runs `openspec new change "add-search-ui-tests" && openspec status --change "add-search-ui-tests" --json`*

```
- Creating change 'add-search-ui-tests' with schema 'spec-driven'...
Created change 'add-search-ui-tests' at openspec/changes/add-search-ui-tests/
Schema: spec-driven
Next: openspec status --change add-search-ui-tests
{
  "changeName": "add-search-ui-tests",
  "schemaName": "spec-driven",
  "planningHome": {
    "kind": "repo",
    "root": "<repo>",
    "changesDir": "<repo>/openspec/changes",
    "defaultSchema": "spec-driven"
... (98 more lines)
```

*The agent runs `openspec instructions proposal --change "add-search-ui-tests" --json | python3 -c "import json,sys; d=json.load(sys.stdin); [print(k, '::', (json.dumps(v, indent=1) if not isinstance(v,str) else v)) for k,v in d.items() if k not in ('context',)]"`*

```
Exit code 1
pyenv: version `3.12' is not installed (set by <repo>/.python-version)
```

*The agent runs `openspec instructions proposal --change "add-search-ui-tests" --json`*

```
{
  "changeName": "add-search-ui-tests",
  "artifactId": "proposal",
  "schemaName": "spec-driven",
  "changeDir": "<repo>/openspec/changes/add-search-ui-tests",
  "planningHome": {
    "kind": "repo",
    "root": "<repo>",
    "changesDir": "<repo>/openspec/changes",
    "defaultSchema": "spec-driven"
  },
  "outputPath": "proposal.md",
... (16 more lines)
```

*The agent runs `openspec list --specs; grep -n "WEB-004\|WEB-003\|WEB-005\|Module 5" openspec/specs/workshop/baseline-suite/spec.md; git status --short -- resources tests`*

```
Specs:
  shop/authentication           requirements 10
  shop/cart                     requirements 20
  shop/catalogue                requirements 13
  shop/checkout                 requirements 11
  shop/interpretation-rules     requirements 6
  shop/product-detail           requirements 9
  shop/search                   requirements 8
  suite/cart                    requirements 4
  suite/product-detail          requirements 4
  workshop/agent-context        requirements 6
  workshop/baseline-suite       requirements 13
... (14 more lines)
```

*The agent writes `<repo>/openspec/changes/add-search-ui-tests/proposal.md`*

```
File created successfully at: <repo>/openspec/changes/add-search-ui-tests/propos
```

**Agent:**

Created proposal. Now the delta spec.

*The agent runs `openspec instructions specs --change "add-search-ui-tests" --json | grep -v '"context"' | head -60`*

```
{
  "changeName": "add-search-ui-tests",
  "artifactId": "specs",
  "schemaName": "spec-driven",
  "changeDir": "<repo>/openspec/changes/add-search-ui-tests",
  "planningHome": {
    "kind": "repo",
    "root": "<repo>",
    "changesDir": "<repo>/openspec/changes",
    "defaultSchema": "spec-driven"
  },
  "outputPath": "specs/**/*.md",
... (25 more lines)
```

*The agent writes `<repo>/openspec/changes/add-search-ui-tests/specs/suite/search/spec.md`*

```
File created successfully at: <repo>/openspec/changes/add-search-ui-tests/specs/
```

*The agent runs `openspec instructions design --change "add-search-ui-tests" --json | grep -E '"(instruction|template)"'`*

```
  "instruction": "Create the design document that explains HOW to implement the change.\n\nWhen to include design.md (create only if any apply):\n- Cross-cutting change (multiple services/modules) or 
  "template": "# Design\n\n## Context\n\n<!-- Current state and constraints that shape the approach. See proposal.md for motivation - don't restate it -->\n\n## Goals / Non-Goals\n\n**Goals:**\n<!-- W
```

**Agent:**

Created the spec. Now the design, which records what the planning probe found.

*The agent writes `<repo>/openspec/changes/add-search-ui-tests/design.md`*

```
File created successfully at: <repo>/openspec/changes/add-search-ui-tests/design
```

**Agent:**

Created the design. Now the tasks.

*The agent runs `openspec instructions tasks --change "add-search-ui-tests" --json | grep -E '"(instruction|template)"'`*

```
  "instruction": "Create the task list that breaks down the implementation work.\n\nBefore writing tasks, check design.md for Open Questions. If any of them\nwould change what gets built, resolve them
  "template": "# Tasks\n\n## 1. <!-- Task Group Name -->\n\n- [ ] 1.1 <!-- Task description -->\n- [ ] 1.2 <!-- Task description -->\n\n## 2. <!-- Task Group Name -->\n\n- [ ] 2.1 <!-- Task descriptio
```

*The agent writes `<repo>/openspec/changes/add-search-ui-tests/tasks.md`*

```
File created successfully at: <repo>/openspec/changes/add-search-ui-tests/tasks.
```

*The agent runs `openspec validate add-search-ui-tests --strict; openspec status --change "add-search-ui-tests"; git status --short`*

```
Change 'add-search-ui-tests' is valid
- Loading change status...
Change: add-search-ui-tests
Schema: spec-driven
Change root: <repo>/openspec/changes/add-search-ui-tests
Progress: 4/4 artifacts complete

[x] proposal
[x] specs
[x] design
[x] tasks

... (30 more lines)
```

**Agent:**

I've created the change `add-search-ui-tests` in `openspec/changes/add-search-ui-tests/`, and `openspec validate --strict` passes. It is a plan only: no test or resource file was written.

**Artifacts**
- **`proposal.md`**: why the change is needed, and its scope. It adds two new files, `tests/ui/search.robot` and `resources/search.resource`. No existing file changes, and nothing under `shop/`.
- **`specs/suite/search/spec.md`**: one requirement per criterion (WEB-004_AC-1, AC-3, AC-6 and AC-7), each naming the tests that verify it.
- **`design.md`**: facts about the shop and the choices made (D1–D8). I checked the locators in a real browser through the RobotCode REPL. Search writes nothing, so no shop state changed.
- **`tasks.md`**: 8 tasks. They re-check the locators, write the resource, write the tests, run them three times and alone, prove each check can fail, then validate.

**Six tests**

| Test | Checks |
|---|---|
| `WEB-004_AC-1 Home Page Hero Shows Search Input` | One visible search input in the hero section; its placeholder or label contains "search" |
| `WEB-004_AC-3 Enter Shows Matching Results` | "headphones" + Enter lists an Aurora Neural Headphones card with its name, a loaded image, and the price from the catalogue API |
| `WEB-004_AC-3 Search Button Shows Matching Results` | The same, submitted with the button |
| `WEB-004_AC-6 Clear Results On Home Page` | After Clear: results hidden, hero shown, input empty |
| `WEB-004_AC-6 Clear Search On Products Page` | After Clear: results hidden, product grid shown, input empty |
| `WEB-004_AC-7 Unmatched Query Shows Empty State` | "xyz123" shows a visible "no products" message inside the results, and no card |

**What the browser check found**
- **The shop also searches while you type**, 300 ms after the last keystroke, and nothing cancels that search. If a test clicks Clear as soon as results appear, the results come back about a second later. So the AC-6 tests wait 1 s before clicking (D6). The spec states no timing, so the tests don't treat the reappearing results as a bug.
- **The AC-3 tests can't show which action produced the results.** Because of that same delayed search, the results would appear even if Enter or the button did nothing. The tests still catch a submit that reloads the page or loses the results (D5).
- **There are two "no results" texts.** The shop's empty-state message is "No products matched your query." It doesn't contain the spec's example "No products found", so the test matches "no products", the spec's own words. It only looks inside the results section, because the suggestion list shows its own "No results" (D7).

**Points for the pair review**
- D2: the hero section has no role, name or quoted text, so it is found as the section that holds the page's main heading. This is the only structural locator.
- D2: the results section is found by its role and label, "Search results". Finding it by its heading text works too if the pair prefers visible text.
- D3: requiring the word "search" is my reading of "indicating its purpose". A label like "Find products" would fail, so a looser reading would only require a non-empty placeholder or label.
- D5: the button test for AC-3 adds little beyond the Enter test and could be dropped.
- The AC-3 tests read the expected price with `Get Product From API`, which exists in `resources/api.resource` only as an uncommitted edit. Task 1.2 stops if it's missing.

The artifacts are ready for review. When you are ready, run `/opsx:apply`.

## Step 3 - Pair review the plan

*In the lab, you and your partner review the plan together. The rehearsal has the agent go through the same list, so that the walkthrough shows what to look for.*

**Prompt:**

> Review the change you just proposed against the 'Plan review' list in labs/lab-05-prompt-to-green/checklist.md. Report each item as met or not met, with the evidence, and fix what is not met in the change's files. Do not start implementing.

*The agent runs `sed -n '1,14p' labs/lab-05-prompt-to-green/checklist.md; git status --short openspec/changes/add-search-ui-tests; find openspec/changes/add-search-ui-tests -type f | sort`*

```
# Lab 5 - Done when

## Plan review (step 3, with your partner)

- [ ] The change covers exactly your slice: no criterion missing, none added.
- [ ] Its specs live under `specs/suite/<area>/` in the change, not under `shop/` or `workshop/`.
- [ ] Every requirement names the criterion it verifies, as `<STORY>_<AC>`, and says what is checked.
- [ ] The tasks name one test per criterion (or more), each named `<STORY>_<AC> <behaviour>`.
- [ ] The tasks put every locator into a keyword under `resources/`, built from roles, labels or visible text.
- [ ] Quoted texts from the specification appear as they are, not paraphrased.
- [ ] Every test creates its own state (for example its own cart), and nothing applies a preset or resets the shop.
- [ ] The last task runs the new tests.
... (8 more lines)
```

**Agent:**

Re-reading the change's files from disk before reviewing, in case anything changed since I wrote them.

*The agent reads `<repo>/openspec/changes/add-search-ui-tests/specs/suite/search/spec.md`*

*The agent reads `<repo>/openspec/changes/add-search-ui-tests/tasks.md`*

*The agent reads `<repo>/openspec/changes/add-search-ui-tests/design.md`*

*The agent reads `<repo>/openspec/changes/add-search-ui-tests/proposal.md`*

*The agent runs `timeout 180 uv run --no-sync robotcode repl --plain --no-history -o NONE -r NONE -l NONE 2>&1 <<'EOF' | grep -E "P:|FAIL|Error"
Import Resource    ${EXECDIR}/resources/shop.resource
VAR    ${I}    role=main >> role=search >> role=searchbox    scope=GLOBAL
VAR    ${H}    role=main >> role=heading[level=1]    scope=GLOBAL
Open Shop Browser
Start Shop Test
Go To Shop Page    /
Wait For Elements State    ${I}    visible
${vp}=    Get Viewport Size
${n}=    Get Element Count    role=main >> role=searchbox
${hb}=    Get BoundingBox    ${H}
${ib}=    Get BoundingBox    ${I}
${n2}=    Get Element Count    ${H}
Log To Console    P: viewport=${vp} searchboxes in main=${n} h1 count=${n2}
Log To Console    P: heading box=${hb}
Log To Console    P: input box=${ib}
${sy}=    Get Scroll Position
Log To Console    P: scroll=${sy}
${n}=    Get Element Count    role=banner >> role=searchbox
Log To Console    P: searchbox in header=${n}
Go To Shop Page    /cart
${n}=    Get Element Count    role=main >> role=searchbox
Log To Console    P: /cart searchboxes in main=${n}
EOF`*

```
  "ignoreHTTPSErrors": false,
[ INFO ] {'acceptDownloads': True, 'baseURL': 'http://localhost:9090', 'bypassCSP': False, 'forcedColors': 'none', 'ignoreHTTPSErrors': False, 'javaScriptEnabled': True, 'offline': False, 'reducedMoti
P: viewport={'width': 1280, 'height': 720} searchboxes in main=1 h1 count=1
P: heading box={'x': 104, 'y': 284.453125, 'width': 512, 'height': 172.78125}
P: input box={'x': 153, 'y': 580.609375, 'width': 343.9375, 'height': 43.1875}
P: scroll={'top': 0, 'left': 0, 'bottom': 720, 'right': 1280}
P: searchbox in header=0
P: /cart searchboxes in main=0
```

*The agent runs `python3 - <<'EOF' 2>/dev/null || uv run --no-sync python - <<'EOF2'
EOF
import re, pathlib
spec = pathlib.Path("openspec/specs/shop/search/spec.md").read_text()
story = pathlib.Path("labs/lab-05-prompt-to-green/stories/WEB-004_search_products.md").read_text()
norm = lambda s: re.sub(r"\s+", " ", s).lower()
for f in sorted(pathlib.Path("openspec/changes/add-search-ui-tests").rglob("*.md")):
    text = f.read_text()
    for q in sorted(set(re.findall(r'"([^"\n]+)"', text))):
        where = "spec" if norm(q) in norm(spec) else ("story" if norm(q) in norm(story) else "-")
        print(f"{f.name:10} {where:6} {q}")
EOF2`*

```
design.md  -      $249.99
design.md  -      <product name>
design.md  spec   Add to Cart
design.md  spec   Add to cart
design.md  spec   Aurora Neural Headphones
design.md  -      Aurora Neural Headphones product photo
design.md  spec   Clear results
design.md  spec   Clear search
design.md  -      Find products
design.md  story  Given search results are currently displayed
design.md  spec   No products found
design.md  -      No products matched your query.
... (55 more lines)
```

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/specs/suite/search/spec.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/specs/suite/search/spec.md 
```

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/specs/suite/search/spec.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/specs/suite/search/spec.md 
```

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/specs/suite/search/spec.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/specs/suite/search/spec.md 
```

**Agent:**

Now the design: the hero facts, the locator table, D3, D6 (including the quote), D8 and the risks.

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/design.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/design.md has been updated 
```

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/design.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/design.md has been updated 
```

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/design.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/design.md has been updated 
```

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/design.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/design.md has been updated 
```

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/design.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/design.md has been updated 
```

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/design.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/design.md has been updated 
```

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/design.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/design.md has been updated 
```

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/design.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/design.md has been updated 
```

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/design.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/design.md has been updated 
```

**Agent:**

Now the proposal and the tasks.

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/proposal.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/proposal.md has been update
```

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/proposal.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/proposal.md has been update
```

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/tasks.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/tasks.md has been updated s
```

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/tasks.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/tasks.md has been updated s
```

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/tasks.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/tasks.md has been updated s
```

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/tasks.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/tasks.md has been updated s
```

**Agent:**

Checking that no stale references remain, then re-running the quote check and validation.

*The agent runs `cd <repo>/openspec/changes/add-search-ui-tests && grep -n 'section:has(h1)\|Given search\|structural\|hero' -r . ; echo ---; cd ../../.. && uv run --no-sync python - <<'EOF'
import re, pathlib
spec = pathlib.Path("openspec/specs/shop/search/spec.md").read_text()
norm = lambda s: re.sub(r"\s+", " ", s).lower()
for f in sorted(pathlib.Path("openspec/changes/add-search-ui-tests").rglob("*.md")):
    for m in re.finditer(r"""spec(?:'s| says| calls [^"]*| asks for|ification says|ification's)[^"]{0,40}"([^"\n]+)\"""", f.read_text()):
        print(f"{f.name:10} {'ok' if norm(m.group(1)) in norm(spec) else 'NOT IN SPEC'}  {m.group(1)}")
EOF
openspec validate add-search-ui-tests --strict`*

```
proposal.md:14:  - **WEB-004_AC-1**: the home page, `/`, shows a visible search input in its hero section. The hero is the page's
proposal.md:23:    tests, one for each normal content the spec names: the hero section on `/` and the product grid on `/products`
tasks.md:70:    no `section:has(h1)` and no other locator built from the markup alone (D2);
tasks.md:89:    `Product Grid Should Be Shown` instead of the hero.
design.md:23:- **The hero.** On `/`, the form sits in the first section of `main`. It is a plain `<section>` with no role and no
design.md:55:  `article`. 300 ms after typing, the suggestions dropdown opens in the hero and shows "No results", which is outside
design.md:57:- **The normal content stays.** While results are shown, the hero on `/` and the product grid on `/products` stay
design.md:114:| Main heading (AC-1, AC-6) | `role=main >> role=heading[level=1]` | A role: the page's main heading, which opens the hero (see below). Found exactly once on `/`. |
design.md:128:**The hero is the first screen, not a container.** The spec names the hero section, but it gives it no text, no role
design.md:129:and no label. In the markup, the hero is a plain `<section>` with neither role nor name (Context). So no role, label or
design.md:130:visible text can find it as a container. The tests recognise the hero the way a shopper does: it is the part of the
design.md:133:- *`role=main >> section:has(h1)`*, the section that holds the main heading. Rejected: it rests on the markup alone,
... (28 more lines)
```

**Agent:**

Both gaps are fixed and `openspec validate add-search-ui-tests --strict` passes. The other six checklist items were already met. I changed only the four files in `openspec/changes/add-search-ui-tests/`; no test or resource was written.

**Plan review**

1. **Exactly the slice: met.** There are four requirements, one each for WEB-004_AC-1, AC-3, AC-6 and AC-7, and every test name starts with one of those IDs. The design's Non-Goals explicitly leave out AC-2, AC-5, AC-8 and AC-9, and the AC-3 requirement says the "Add to Cart" button and the detail link are not checked because they belong to AC-8.
2. **Specs under `specs/suite/<area>/`: met.** The change's only spec file is `specs/suite/search/spec.md`. Nothing is under `shop/` or `workshop/`.
3. **Every requirement names its criterion and what is checked: met.** Each requirement has the ID in its heading, for example "Search submission is verified (WEB-004_AC-3)", and starts "The suite SHALL verify WEB-004_AC-x …" followed by the checks. None names a locator, keyword or file.
4. **One test or more per criterion, named `<STORY>_<AC> <behaviour>`: met.** Task 2.1 lists six tests: AC-1 has one, AC-3 two, AC-6 two and AC-7 one, for example `WEB-004_AC-7 Unmatched Query Shows Empty State`. The dry-run check confirms the tags `WEB-004` and `ui`.
5. **Every locator in a keyword under `resources/`, built from roles, labels or visible text: was not met, now fixed.**
   - **What was wrong:** the tests call keywords only, but the hero section was found as `role=main >> section:has(h1)`. That uses only page structure (the `section` and `h1` tags), not a role, label or visible text, and the design admitted it as an exception.
   - **Why there was no simple swap:** the spec gives the hero no text, role or label, and in the page it is a plain section with neither.
   - **The fix:** the plan now treats the hero as what a shopper sees first. AC-1 checks that the page's main heading (`role=main >> role=heading[level=1]`) and the only search input in the main content (`role=main >> role=searchbox`) are both visible and fully inside the window, before any scrolling. In the AC-6 home-page test, "hero shown again" now means the main heading is visible.
   - **Checked in the browser:** in the default 1280 × 720 window, the heading sits at 284–457 px and the input at 581–624 px. The site header has no search input, and `/cart` has none in its main content.
   - **Files updated:** the spec's AC-1 and AC-6 wording, design D2, D3, D6, D8 and Risks, the proposal, and tasks 1.1, 1.3 and 2.3. Task 1.3 now also checks that the resource contains no `section:has(h1)`.
   - The one locator not written by this change is `${GRID}`, reused as shipped from `catalogue.resource`. It finds the product grid by its heading's visible text, "All products".
6. **Quoted texts appear as they are: was not met, now fixed.**
   - Design D6 attributed "Given search results are currently displayed" to the spec, but that wording is the story's. It now quotes the spec's "When search results are displayed".
   - The suite spec now quotes "Add to Cart" as the spec writes it.
   - I checked every quote the change attributes to the spec, and all are word for word in `shop/search`.
7. **Every test creates its own state; no preset or reset: met.** Each test runs in a fresh browser context and runs its own search. Search writes nothing to the shop. Tasks 1.1 and 3.2 forbid applying a preset or resetting the shop and check that none happened.
8. **The last task runs the new tests: met.** Task 3.2 runs `uv run robotcode robot tests/ui/search.robot` and then the whole suite with `--exclude broken`.

**Decision for your review:** the new hero check depends on the window size and page layout. The input ends 96 px above the bottom of the window, so a taller hero or a smaller window would fail AC-1 even though the input is still in the hero. The design records this as a risk and a review point. If you'd rather have the sturdier structural locator, the fallback is to go back to `section:has(h1)` as a deliberate exception to this checklist item.

When you're ready, run `/opsx:apply`.

## Step 4 - Apply

**Prompt:**

> /opsx:apply

**Agent:**

Using change: `add-search-ui-tests`. To apply a different change, run `/opsx:apply <other>`.

*The agent runs `openspec status --change "add-search-ui-tests" --json | head -40 && openspec instructions apply --change "add-search-ui-tests" --json`*

```
{
  "changeName": "add-search-ui-tests",
  "schemaName": "spec-driven",
  "planningHome": {
    "kind": "repo",
    "root": "<repo>",
    "changesDir": "<repo>/openspec/changes",
    "defaultSchema": "spec-driven"
  },
  "changeRoot": "<repo>/openspec/changes/add-search-ui-tests",
  "artifactPaths": {
    "proposal": {
... (101 more lines)
```

**Agent:**

I'm re-reading all four artifacts from disk in case they were edited during the pair review.

*The agent runs `cd <repo>/openspec/changes/add-search-ui-tests && cat proposal.md specs/suite/search/spec.md tasks.md && md5sum *.md specs/suite/search/spec.md`*

```
# Proposal

## Why

No test in the suite covers product search: the shipped suite leaves WEB-004 to Module 5 on purpose. This change
automates four search criteria as Robot Framework UI tests: WEB-004_AC-1, WEB-004_AC-3, WEB-004_AC-6 and
WEB-004_AC-7. Each test checks the behaviour that `openspec/specs/shop/search` specifies. The story's wording is not
the reference.

## What Changes

- A new test file for search, with one or more tests for each of the four criteria. Each test name starts with its
... (231 more lines)
```

*The agent reads `<repo>/openspec/changes/add-search-ui-tests/design.md`*

*The agent runs `cd <repo> && uv run --no-sync python -m shop status && timeout 300 uv run --no-sync robotcode repl --plain --no-history -o NONE -r NONE -l NONE 2>&1 <<'EOF' | grep -E "P:|FAIL|Error|rror:"
Import Resource    ${EXECDIR}/resources/shop.resource
Import Resource    ${EXECDIR}/resources/catalogue.resource
VAR    ${H}    role=main >> role=heading[level=1]    scope=GLOBAL
VAR    ${F}    role=main >> role=search    scope=GLOBAL
VAR    ${I}    role=main >> role=searchbox    scope=GLOBAL
VAR    ${B}    ${F} >> button:has-text("Search")    scope=GLOBAL
VAR    ${R}    role=region[name=/search results/i]    scope=GLOBAL
VAR    ${C}    ${R} >> article:has-text("Aurora Neural Headphones")    scope=GLOBAL
VAR    ${CLR}    ${R} >> :is(button:has-text("Clear search"), button:has-text("Clear results"))    scope=GLOBAL
Open Shop Browser
Start Shop Test
Go To Shop Page    /
Wait For Elements State    ${I}    visible
${a}=    Get Element Count    ${H}
${b}=    Get Element Count    ${F}
${c}=    Get Element Count    ${I}
${d}=    Get Element Count    ${B}
${e}=    Get Element Count    role=banner >> role=searchbox
Log To Console    P: home heading=${a} form=${b} input=${c} button=${d} header-input=${e}
${vp}=    Get Viewport Size
${hb}=    Get BoundingBox    ${H}
${ib}=    Get BoundingBox    ${I}
Log To Console    P: viewport=${vp} heading y=${hb}[y]..${hb}[y]+${hb}[height] input y=${ib}[y]..${ib}[y]+${ib}[height]
${n}=    Get Element Count    ${R}
${ph}=    Get Attribute    ${I}    placeholder
${nm}=    Get Element Count    role=main >> role=searchbox[name=/search/i]
Log To Console    P: hidden region=${n} placeholder=${ph} named=${nm}
Fill Text    ${I}    headphones
Press Keys    ${I}    Enter
Wait For Elements State    ${R}    visible
${a}=    Get Element Count    ${C}
${b}=    Get Element Count    ${C} >> role=img[name=/Aurora Neural Headphones/i]
${c}=    Get Element Count    ${C} >> role=heading
${d}=    Get Element Count    ${C} >> ${CARD PRICE}
${w}=    Get Property    ${C} >> role=img[name=/Aurora Neural Headphones/i]    naturalWidth
${p}=    Get Text    ${C} >> ${CARD PRICE}
Log To Console    P: enter card=${a} img=${b} heading=${c} price=${d} naturalWidth=${w} price=${p}
Sleep    1s
${n}=    Get Element Count    ${CLR}
Click    ${CLR}
Wait For Elements State    ${R}    hidden
Wait For Elements State    ${H}    visible
${v}=    Get Property    ${I}    value
Sleep    1.5s
${after}=    Get Element Count    ${R}
Log To Console    P: clear buttons=${n} input='${v}' region 1.5s later=${after}
Start Shop Test
Go To Shop Page    /
Fill Text    ${I}    headphones
Click    ${B}
Wait For Elements State    ${C}    visible
${u}=    Get Url
Log To Console    P: button url=${u}
Start Shop Test
Go To Catalogue
Fill Text    ${I}    headphones
Press Keys    ${I}    Enter
Wait For Elements State    ${C}    visible
Sleep    1s
Click    ${CLR}
Wait For Elements State    ${R}    hidden
Wait For Elements State    ${GRID}    visible
${v}=    Get Property    ${I}    value
Log To Console    P: products clear ok input='${v}'
Start Shop Test
Go To Shop Page    /
Fill Text    ${I}    xyz123
Press Keys    ${I}    Enter
Wait For Elements State    ${R} >> text=/no products/i >> nth=0    visible
${n}=    Get Element Count    ${R} >> role=article
Sleep    1s
${s}=    Get Element Count    text=/no results/i
${si}=    Get Element Count    ${R} >> text=/no results/i
Log To Console    P: empty articles=${n} 'no results' on page=${s} inside region=${si}
EOF`*

```
shop     http://localhost:9090  (version 0.3.0)
space    default
presets  clean, stage1
  "ignoreHTTPSErrors": false,
[ INFO ] {'acceptDownloads': True, 'baseURL': 'http://localhost:9090', 'bypassCSP': False, 'forcedColors': 'none', 'ignoreHTTPSErrors': False, 'javaScriptEnabled': True, 'offline': False, 'reducedMoti
[ FAIL ] Error: locator.count: Error while parsing css selector "1". Did you mean to CSS.escape it?
[ FAIL ] Variable '${d}' not found.
P: viewport={'width': 1280, 'height': 720} heading y=284.453125..284.453125+172.78125 input y=580.609375..580.609375+43.1875
P: hidden region=0 placeholder=Search headphones, notebooks, wearables... named=1
[ FAIL ] Error: locator.count: Error while parsing css selector "1". Did you mean to CSS.escape it?
[ FAIL ] Error: locator.count: Error while parsing css selector "1". Did you mean to CSS.escape it?
[ FAIL ] Error: locator.count: Error while parsing css selector "1". Did you mean to CSS.escape it?
... (17 more lines)
```

**Agent:**

The failures come from my probe script, not the locators: Robot variable names ignore case, so `${b}` and `${c}` overwrote `${B}` and `${C}`. Re-running the affected checks with distinct names.

*The agent runs `timeout 300 uv run --no-sync robotcode repl --plain --no-history -o NONE -r NONE -l NONE 2>&1 <<'EOF' | grep -E "P:|FAIL|rror:"
Import Resource    ${EXECDIR}/resources/shop.resource
Import Resource    ${EXECDIR}/resources/catalogue.resource
VAR    ${HEADING}    role=main >> role=heading[level=1]    scope=GLOBAL
VAR    ${FORM}    role=main >> role=search    scope=GLOBAL
VAR    ${INPUT}    role=main >> role=searchbox    scope=GLOBAL
VAR    ${BUTTON}    ${FORM} >> button:has-text("Search")    scope=GLOBAL
VAR    ${RESULTS}    role=region[name=/search results/i]    scope=GLOBAL
VAR    ${CARD}    ${RESULTS} >> article:has-text("Aurora Neural Headphones")    scope=GLOBAL
VAR    ${CLEAR}    ${RESULTS} >> :is(button:has-text("Clear search"), button:has-text("Clear results"))    scope=GLOBAL
Open Shop Browser
Start Shop Test
Go To Shop Page    /
Wait For Elements State    ${INPUT}    visible
${n1}=    Get Element Count    ${HEADING}
${n2}=    Get Element Count    ${FORM}
${n3}=    Get Element Count    ${INPUT}
${n4}=    Get Element Count    ${BUTTON}
${n5}=    Get Element Count    role=banner >> role=searchbox
Log To Console    P: home heading=${n1} form=${n2} input=${n3} button=${n4} header-input=${n5}
Fill Text    ${INPUT}    headphones
Press Keys    ${INPUT}    Enter
Wait For Elements State    ${RESULTS}    visible
${n1}=    Get Element Count    ${CARD}
${n2}=    Get Element Count    ${CARD} >> role=img[name=/Aurora Neural Headphones/i]
${n3}=    Get Element Count    ${CARD} >> role=heading
${n4}=    Get Element Count    ${CARD} >> ${CARD PRICE}
${w}=    Get Property    ${CARD} >> role=img[name=/Aurora Neural Headphones/i]    naturalWidth
${p}=    Get Text    ${CARD} >> ${CARD PRICE}
${t}=    Get Text    ${CARD} >> role=heading
Log To Console    P: enter card=${n1} img=${n2} heading=${n3} (${t}) price=${n4} naturalWidth=${w} price=${p}
Start Shop Test
Go To Shop Page    /
Fill Text    ${INPUT}    headphones
Click    ${BUTTON}
Wait For Elements State    ${CARD}    visible
${u}=    Get Url
Log To Console    P: button url=${u}
Start Shop Test
Go To Catalogue
${n1}=    Get Element Count    ${INPUT}
Fill Text    ${INPUT}    headphones
Press Keys    ${INPUT}    Enter
Wait For Elements State    ${CARD}    visible
Sleep    1s
${n2}=    Get Element Count    ${CLEAR}
Click    ${CLEAR}
Wait For Elements State    ${RESULTS}    hidden
Wait For Elements State    ${GRID}    visible
${v}=    Get Property    ${INPUT}    value
Log To Console    P: products inputs=${n1} clear buttons=${n2} input after='${v}'
EOF`*

```
P: home heading=1 form=1 input=1 button=1 header-input=0
P: enter card=1 img=1 heading=1 (Aurora Neural Headphones) price=1 naturalWidth=1024 price=$249.99
P: button url=http://localhost:9090/
P: products inputs=1 clear buttons=1 input after=''
```

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/tasks.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/tasks.md has been updated s
```

*The agent runs `for f in shop catalogue api; do echo "== $f"; uv run --no-sync python -m robot.libdoc resources/$f.resource list; done; echo "== variables"; sed -n '/\*\*\* Variables/,/\*\*\* Keywords/p' resources/catalogue.resource; sed -n '1,25p' resources/api.resource`*

```
== shop
Go To Shop Page
Open Shop Browser
Start Shop Test
== catalogue
Apply Filters
Check Category
Checkbox Should Be Unchecked
Filter Checkboxes Should All Be Unchecked
Format Price
Get Add To Cart Button Count
Get Card Category
... (50 more lines)
```

**Agent:**

All the reused keywords and variables exist: `Go To Shop Page`, `Go To Catalogue`, `Format Price`, `${GRID}`, `${CARD PRICE}` and `Get Product From API`.

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/tasks.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/tasks.md has been updated s
```

**Agent:**

Working on task 3 of 8 (1.3): writing `resources/search.resource`.

*The agent writes `<repo>/resources/search.resource`*

```
File created successfully at: <repo>/resources/search.resource (file state is cu
```

**Agent:**

Running the checks for task 1.3.

*The agent runs `uv run robotcode analyze code resources/search.resource; echo "exit=$?"; echo "--- forbidden patterns"; grep -nE 'id=|#[A-Za-z]|\.[a-z][a-z-]+[^a-z(]|data-|href|xpath|section:has\(h1\)' resources/search.resource | grep -vE '^\s*[0-9]+:\s*(#|\.\.\.|\[Documentation\])' ; echo "--- git"; git status --short -- resources; git diff --stat -- resources`*

```
Files: 1, Errors: 0, Warnings: 0, Infos: 0, Hints: 0 (in 0.07s)
exit=0
--- forbidden patterns
--- git
 M resources/api.resource
 M resources/catalogue.resource
?? resources/cart.resource
?? resources/product_detail.resource
?? resources/search.resource
 resources/api.resource       |  8 ++++++++
 resources/catalogue.resource | 10 ++++++++++
 2 files changed, 18 insertions(+)
```

*The agent runs `for p in 'id=' '#[A-Za-z]' 'data-' 'href' 'xpath' 'section:has' ; do printf '%-12s %s\n' "$p" "$(grep -c -- "$p" resources/search.resource)"; done; grep -nE '(^|[ >"])\.[a-zA-Z]' resources/search.resource | grep -v 'lower()' ; echo "--- UI words in shop/search spec"; for w in "search" "search results" "clear search" "clear results" "no products"; do printf '%-15s %s\n' "$w" "$(grep -ci -- "$w" openspec/specs/shop/search/spec.md)"; done`*

```
id=          0
#[A-Za-z]    0
data-        0
href         0
xpath        0
section:has  0
--- UI words in shop/search spec
search          27
search results  4
clear search    3
clear results   2
no products     2
```

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/tasks.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/tasks.md has been updated s
```

*The agent writes `<repo>/tests/ui/search.robot`*

```
File created successfully at: <repo>/tests/ui/search.robot (file state is curren
```

**Agent:**

Working on task 4 of 8 (2.1): `tests/ui/search.robot` is written. Running its checks.

*The agent runs `echo "--- inline locators"; uv run --no-sync python hooks/no_inline_locators.py tests/ui/search.robot; echo "exit=$?"; echo "--- analyze"; uv run robotcode analyze code tests/ui/search.robot; echo "--- dryrun"; uv run robotcode robot --dryrun --include WEB-004 --output NONE --report NONE --log NONE 2>&1 | grep -vE '^\s*$' | tail -25; echo "--- expected texts in spec"; for w in "headphones" "Aurora Neural Headphones" "xyz123" "/products/1"; do printf '%-26s %s\n' "$w" "$(grep -c -- "$w" openspec/specs/shop/search/spec.md)"; done`*

```
--- inline locators
exit=0
--- analyze
Files: 1, Errors: 0, Warnings: 0, Infos: 0, Hints: 0 (in 0.07s)
--- dryrun
==============================================================================
Tests.Ui.Search :: Product search on the home page and the products page (s...
==============================================================================
WEB-004_AC-1 Home Page Hero Shows Search Input :: The first screen... | PASS |
------------------------------------------------------------------------------
WEB-004_AC-3 Enter Shows Matching Results :: Searching "headphones... | PASS |
------------------------------------------------------------------------------
... (23 more lines)
```

**Agent:**

The dry run lists exactly the six tests. Confirming each one's tags.

*The agent runs `uv run robotcode --format json discover tests --include WEB-004 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
def walk(n):
    for c in n.get('children') or []:
        if c.get('type')=='test': print(c['name'], sorted(c.get('tags') or []))
        walk(c)
walk(d)" 2>/dev/null || uv run robotcode discover tests --include WEB-004 --tags 2>&1 | tail -20`*

```
- **Tests.Ui.Search.WEB-004_AC-1 Home Page Hero Shows Search Input** (`tests/ui/search.robot:16`)
  - _Tags:_ `ui`, `web-004`
- **Tests.Ui.Search.WEB-004_AC-3 Enter Shows Matching Results** (`tests/ui/search.robot:22`)
  - _Tags:_ `ui`, `web-004`
- **Tests.Ui.Search.WEB-004_AC-3 Search Button Shows Matching Results** (`tests/ui/search.robot:30`)
  - _Tags:_ `ui`, `web-004`
- **Tests.Ui.Search.WEB-004_AC-6 Clear Results On Home Page** (`tests/ui/search.robot:38`)
  - _Tags:_ `ui`, `web-004`
- **Tests.Ui.Search.WEB-004_AC-6 Clear Search On Products Page** (`tests/ui/search.robot:48`)
  - _Tags:_ `ui`, `web-004`
- **Tests.Ui.Search.WEB-004_AC-7 Unmatched Query Shows Empty State** (`tests/ui/search.robot:58`)
  - _Tags:_ `ui`, `web-004`
... (6 more lines)
```

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/tasks.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/tasks.md has been updated s
```

*The agent runs `uv run robotcode robot tests/ui/search.robot 2>&1 | grep -E '\| (PASS|FAIL) \||tests,|^Output|^Log' `*

```
WEB-004_AC-1 Home Page Hero Shows Search Input :: The first screen... | PASS |
WEB-004_AC-3 Enter Shows Matching Results :: Searching "headphones... | PASS |
WEB-004_AC-3 Search Button Shows Matching Results :: Searching "he... | PASS |
WEB-004_AC-6 Clear Results On Home Page :: On /, clearing the resu... | PASS |
WEB-004_AC-6 Clear Search On Products Page :: On /products, cleari... | PASS |
WEB-004_AC-7 Unmatched Query Shows Empty State :: Searching "xyz12... | PASS |
Search :: Product search on the home page and the products page (s... | PASS |
6 tests, 6 passed, 0 failed
Output:  <repo>/results/output.xml
Log:     <repo>/results/log.html
```

**Agent:**

Working on task 5 of 8 (2.2): the file passed 6 of 6. Now each test on its own, then three full runs in a row.

*The agent runs `for t in "WEB-004_AC-1 Home Page Hero Shows Search Input" "WEB-004_AC-3 Enter Shows Matching Results" "WEB-004_AC-3 Search Button Shows Matching Results" "WEB-004_AC-6 Clear Results On Home Page" "WEB-004_AC-6 Clear Search On Products Page" "WEB-004_AC-7 Unmatched Query Shows Empty State"; do printf 'alone: %-52s ' "$t"; uv run robotcode robot --test "$t" --output NONE --report NONE --log NONE 2>&1 | grep -E 'tests?, ' | tail -1; done; for i in 1 2 3; do printf 'run %s: ' "$i"; uv run robotcode robot tests/ui/search.robot --output NONE --report NONE --log NONE 2>&1 | grep -E 'tests?, ' | tail -1; done`*

```
alone: WEB-004_AC-1 Home Page Hero Shows Search Input       1 test, 1 passed, 0 failed
alone: WEB-004_AC-3 Enter Shows Matching Results            1 test, 1 passed, 0 failed
alone: WEB-004_AC-3 Search Button Shows Matching Results    1 test, 1 passed, 0 failed
alone: WEB-004_AC-6 Clear Results On Home Page              1 test, 1 passed, 0 failed
alone: WEB-004_AC-6 Clear Search On Products Page           1 test, 1 passed, 0 failed
alone: WEB-004_AC-7 Unmatched Query Shows Empty State       1 test, 1 passed, 0 failed
run 1: run 2: run 3:
```

**Agent:**

The three full runs printed no summary. Looking at one run's raw output.

*The agent runs `uv run robotcode robot tests/ui/search.robot --output NONE --report NONE --log NONE 2>&1 | tail -8`*

```
[ ERROR ] Parsing '<repo>/--output', '<scratch>

Try --help for usage information.
```

**Agent:**

My command was wrong: robotcode needs options before the path. Re-running the three runs with the options first.

*The agent runs `for i in 1 2 3; do printf 'run %s: ' "$i"; uv run robotcode robot --output NONE --report NONE --log NONE tests/ui/search.robot 2>&1 | grep -E 'tests?, ' | tail -1; done`*

```
run 1: 6 tests, 6 passed, 0 failed
run 2: 6 tests, 6 passed, 0 failed
run 3: 6 tests, 6 passed, 0 failed
```

**Agent:**

The file passed three runs in a row, and each test passes on its own.

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/tasks.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/tasks.md has been updated s
```

*The agent runs `git check-ignore -v results/search_mutations.robot && python3 - <<'EOF' 2>/dev/null || uv run --no-sync python - <<'EOF2'
EOF
import pathlib, re
src = pathlib.Path("tests/ui/search.robot").read_text()
blocks = re.split(r"(?m)^(?=WEB-004_)", src)
head, tests = blocks[0], blocks[1:]
out = []
for t in tests:
    name = t.splitlines()[0]
    if name.startswith("WEB-004_AC-1 "):
        t = t.replace("    Go To Home Page\n", "    Go To Shop Page    /cart\n", 1)
    elif name.startswith("WEB-004_AC-3 Enter"):
        t = t.replace("Submit Search With Enter    headphones", "Submit Search With Enter    xyz123")
    elif name.startswith("WEB-004_AC-3 Search Button"):
        t = t.replace("Get Product From API    1", "Get Product From API    2")
    elif name.startswith("WEB-004_AC-6 Clear Results"):
        t = t.replace("    Clear Search Results\n", "")
    elif name.startswith("WEB-004_AC-6 Clear Search"):
        t = t.replace("    Clear Search Results\n", "    Submit Search With Enter    headphones\n")
    elif name.startswith("WEB-004_AC-7"):
        t = t.replace("Submit Search With Enter    xyz123", "Submit Search With Enter    headphones")
    out.append(t)
pathlib.Path("results/search_mutations.robot").write_text(head + "".join(out))
EOF2
diff tests/ui/search.robot results/search_mutations.robot`*

```
.gitignore:11:results/	results/search_mutations.robot
18c18
<     Go To Home Page
---
>     Go To Shop Page    /cart
26c26
<     Submit Search With Enter    headphones
---
>     Submit Search With Enter    xyz123
32c32
<     ${product}=    Get Product From API    1
---
... (11 more lines)
```

**Agent:**

Working on task 6 of 8 (2.3): the git-ignored copy `results/search_mutations.robot` has exactly the six planned changes. Running it; every test should fail.

*The agent runs `uv run robotcode robot --output search_mutations.xml --report NONE --log NONE results/search_mutations.robot 2>&1 | grep -vE '^[=-]+$' | grep -vE '^\s*$' | head -40`*

```
Search Mutations :: Product search on the home page and the products page (...
WEB-004_AC-1 Home Page Hero Shows Search Input :: The first screen... | FAIL |
The main content should hold one search input, not 0.
WEB-004_AC-3 Enter Shows Matching Results :: Searching "headphones... | FAIL |
The search results should list a card for "Aurora Neural Headphones".
WEB-004_AC-3 Search Button Shows Matching Results :: Searching "he... | FAIL |
The card of "Aurora Neural Headphones" should show the price $39.50, not '$249.99'.
WEB-004_AC-6 Clear Results On Home Page :: On /, clearing the resu... | FAIL |
The search results section should be hidden, but it is still shown.
WEB-004_AC-6 Clear Search On Products Page :: On /products, cleari... | FAIL |
The search results section should be hidden, but it is still shown.
WEB-004_AC-7 Unmatched Query Shows Empty State :: Searching "xyz12... | FAIL |
... (4 more lines)
```

*The agent runs `rm results/search_mutations.robot results/search_mutations.xml && ls results/search_mutations* 2>&1 | head -2; git status --short -- tests resources`*

```
ls: cannot access 'results/search_mutations*': No such file or directory
 M resources/api.resource
 M resources/catalogue.resource
 M tests/ui/catalogue.robot
?? resources/cart.resource
?? resources/product_detail.resource
?? resources/search.resource
?? tests/api/AGENTS.md
?? tests/ui/cart.robot
?? tests/ui/product_detail.robot
?? tests/ui/search.robot
```

**Agent:**

Besides your earlier work, the only new files under `tests` and `resources` are `tests/ui/search.robot` and `resources/search.resource`.

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/tasks.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/tasks.md has been updated s
```

*The agent runs `openspec validate add-search-ui-tests --strict`*

```
Change 'add-search-ui-tests' is valid
```

**Agent:**

Task 7 of 8 (3.1): `openspec validate --strict` passes.

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/tasks.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/tasks.md has been updated s
```

*The agent runs `echo "=== search.robot"; uv run robotcode robot --output NONE --report NONE --log NONE tests/ui/search.robot 2>&1 | grep -E 'tests?, ' | tail -1; echo "=== whole suite, broken excluded"; uv run robotcode robot --exclude broken 2>&1 | grep -E '\| FAIL \||^[A-Z].*(should|expected|Error)|tests?, ' | tail -30; echo "=== presets after"; uv run --no-sync python -m shop status`*

```
=== search.robot
6 tests, 6 passed, 0 failed
=== whole suite, broken excluded
2 tests, 2 passed, 0 failed
2 tests, 2 passed, 0 failed
5 tests, 5 passed, 0 failed
7 tests, 7 passed, 0 failed
WEB-006_AC-11 Validation Errors Next To Fields :: Invalid fields e... | PASS |
4 tests, 4 passed, 0 failed
6 tests, 6 passed, 0 failed
6 tests, 6 passed, 0 failed
28 tests, 28 passed, 0 failed
... (5 more lines)
```

*The agent edits `<repo>/openspec/changes/add-search-ui-tests/tasks.md`*

```
The file <repo>/openspec/changes/add-search-ui-tests/tasks.md has been updated s
```

*The agent runs `openspec instructions apply --change "add-search-ui-tests" --json | grep -E '"(total|complete|remaining|state)"'`*

```
    "total": 8,
    "complete": 8,
    "remaining": 0
  "state": "all_done",
```

**Agent:**

## Implementation Complete

**Change:** add-search-ui-tests
**Schema:** spec-driven
**Progress:** 8/8 tasks complete ✓

The six search tests pass against the local shop: 6 of 6, three runs in a row, and each test alone. The whole suite, without the `broken` tests, passes 30 of 30.

### Completed This Session
- [x] **1.1 Locators confirmed in the shop.** Every locator in the design found what it should, including the heading and search input on the first screen. No row needed changing.
- [x] **1.2 Reused keywords exist.** `Go To Shop Page`, `Go To Catalogue`, `Format Price`, `${GRID}`, `${CARD PRICE}` and `Get Product From API` are all there.
- [x] **1.3 `resources/search.resource` written.** Every locator uses a role, a label or visible text, with no ids, classes, `data-` hooks, hrefs or XPath. `robotcode analyze` reports 0 errors.
- [x] **2.1 `tests/ui/search.robot` written.** It has six tests that call keywords only, and each carries `WEB-004` and `ui`. The inline-locator hook reports nothing.
- [x] **2.2 Runs are stable.** Each test passes alone, and the file passes three times in a row.
- [x] **2.3 Every check can fail.** In a throwaway copy with one planted mistake per test, all 6 tests failed, each naming the right problem. For example, the price test said "should show the price $39.50, not '$249.99'". The copy has been deleted.
- [x] **3.1 Change validated.** `openspec validate --strict` passes.
- [x] **3.2 Final run.** The six new tests pass, and the full suite without `broken` passes 30 of 30. The shop still reports `clean, stage1`.

**Files:**
- `resources/search.resource` and `tests/ui/search.robot` are the only new files.
- No existing test, keyword or spec changed.
- `openspec/changes/add-search-ui-tests/tasks.md` now has every box ticked.

**Worth knowing:**
- **The AC-6 tests wait 1 s before clicking Clear.** The shop repeats the typed search 300 ms after the last keystroke, and an earlier click lets that search bring the results back. If AC-6 ever fails on the shared instance with the results shown again after Clear, increase `${SEARCH SETTLE}` in `resources/search.resource` rather than removing it.
- **AC-1 depends on the window size.** It passes because the search input's bottom edge is at 624 px in the default 1280 × 720 window. A taller hero or a smaller window would fail it. The failure message gives the input's position and the window height.

All tasks are complete. You can archive this change with `/opsx:archive`.

## Step 5 - Run and refine

**The participant runs** `ls -t tests/ui/*.robot | head -3`:

```
tests/ui/search.robot
tests/ui/cart.robot
tests/ui/product_detail.robot
```

**The participant runs** `f=$(ls -t tests/ui/*.robot | head -1); echo $f; uv run robotcode robot $f`:

```
Search :: Product search on the home page and the products page (spec: shop...
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
... (8 more lines)
```

**The participant runs** `f=$(ls -t tests/ui/*.robot | head -1); uv run --no-sync python hooks/no_inline_locators.py $f; echo "exit $?"`:

```
exit 0
```

**Prompt:**

> If every task of the change you applied is done, archive it now: sync its delta specs into the main specs and move it to the archive, without asking me anything. If a task is not done, do not archive; say which.

*The agent runs `ls openspec/changes/ openspec/changes/add-search-ui-tests -R && cat openspec/changes/add-search-ui-tests/tasks.md && uv run --no-sync openspec list 2>/dev/null || npx --no-install openspec list 2>&1 | head -20; which openspec`*

```
openspec/changes/:
add-search-ui-tests
archive
ci-and-site
workshop-labs

openspec/changes/add-search-ui-tests:
design.md
proposal.md
specs
tasks.md

... (319 more lines)
```

*The agent loads the skill `openspec-archive-change`*

**Agent:**

Using change: add-search-ui-tests (run `/opsx:archive <other>` to pick a different one).

*The agent runs `openspec list --json | head -30; echo ---; openspec instructions archive --change add-search-ui-tests --json; echo "exit $?"; echo ---; openspec status --change add-search-ui-tests --json`*

```
{
  "changes": [
    {
      "name": "add-search-ui-tests",
      "completedTasks": 8,
      "totalTasks": 8,
      "lastModified": "2026-09-25T07:13:37.101Z",
      "status": "complete"
    },
    {
      "name": "workshop-labs",
      "completedTasks": 25,
... (132 more lines)
```

**Agent:**

Artifacts are all done and all 8 tasks are checked. Before archiving, I'll check that the deliverables actually exist and hold up, then look at the delta spec against the main specs.

*The agent runs `cat docs/agent-environment.md; echo ---; ls openspec/specs openspec/specs/suite; echo ---; cat openspec/changes/add-search-ui-tests/specs/suite/search/spec.md; echo ---; ls -la openspec/changes/add-search-ui-tests; ls tests/ui/search.robot resources/search.resource`*

```
# Environment

- Install: `uv sync --locked`, then `uv run --no-sync rfbrowser install chromium`.
- Check the environment: `uv run --no-sync python setup-check/check.py`.
- Run the suite: `uv run robotcode robot`. Plain `robot` ignores `robot.toml` and cannot find the shop.
- Run one test: `uv run robotcode robot -t "<test name>"`.
- `-p shared` selects the shared instance: `uv run robotcode -p shared robot`. Without it, the local shop.
- Logs and reports go to `results/`, which git ignores.
---
openspec/specs:
shop
suite
... (68 more lines)
```

*The agent runs `cat openspec/changes/add-search-ui-tests/.openspec.yaml; echo ---; head -20 openspec/specs/suite/cart/spec.md; echo ...; echo ---; head -8 openspec/changes/archive/2026-09-25-add-cart-ui-tests/specs/suite/cart/spec.md; echo ---; openspec validate add-search-ui-tests --strict; echo ---; uv run --no-sync python hooks/no_inline_locators.py tests/ui/search.robot; echo "hook exit $?"; echo ---; uv run robotcode analyze code tests/ui/search.robot resources/search.resource 2>&1 | tail -5`*

```
schema: spec-driven
created: 2026-09-25
---
# suite/cart Specification

## Purpose
Records which cart criteria of `shop/cart` the suite verifies through the shop's pages, what each test checks, and which test verifies each criterion.

## Requirements

### Requirement: The cart badge update is verified (WEB-005_AC-2)
The suite SHALL verify WEB-005_AC-2 with one test for each scenario in the specification: the desktop navigation and the mobile navigation. Each test SHALL start in a fresh browser context, with an em
... (27 more lines)
```

**Agent:**

The change validates under `--strict`, the no-inline-locators hook reports nothing, and static analysis finds 0 errors. Last, I'll run the six tests against the local shop to confirm the task claims.

*The agent runs `uv run --no-sync python -m shop status 2>&1 | tail -8; echo ---; uv run robotcode robot tests/ui/search.robot 2>&1 | tail -25`*

```
shop     http://localhost:9090  (version 0.3.0)
space    default
presets  clean, stage1
---
==============================================================================
Search :: Product search on the home page and the products page (spec: shop...
==============================================================================
WEB-004_AC-1 Home Page Hero Shows Search Input :: The first screen... | PASS |
------------------------------------------------------------------------------
WEB-004_AC-3 Enter Shows Matching Results :: Searching "headphones... | PASS |
------------------------------------------------------------------------------
WEB-004_AC-3 Search Button Shows Matching Results :: Searching "he... | PASS |
... (13 more lines)
```

**Agent:**

All six pass. Every task is done and confirmed, so I'm going ahead with sync and archive. First I'll fetch the specs rules the sync needs.

*The agent runs `openspec instructions specs --change add-search-ui-tests --json > <scratch> echo "exit $?"; python3 -c "import json;d=json.load(open('<scratch>'));print(list(d.keys()));print(json.dumps(d.get('rules'),indent=1))"`*

```
Exit code 1
exit 0
pyenv: version `3.12' is not installed (set by <repo>/.python-version)
```

*The agent runs `uv run --no-sync python -c "import json;d=json.load(open('<scratch>'));print(list(d.keys()));print(json.dumps(d.get('rules'),indent=1))"`*

```
['changeName', 'artifactId', 'schemaName', 'changeDir', 'planningHome', 'outputPath', 'resolvedOutputPath', 'existingOutputPaths', 'description', 'instruction', 'context', 'rules', 'template', 'depend
[
 "Requirements under shop/* describe correct behaviour only. They never name a feature flag, a locator stage, a planted bug, a locator (ids, classes, data-test hooks) or the purpose of a check. Visibl
 "Requirements under suite/* say which shop criterion the tests verify, by its <STORY>_<AC> ID, and what they check. They never name a locator, a keyword or a file. Use \"The suite SHALL verify <STORY
]
```

**Agent:**

The rules for `suite/*` specs: name the criterion ID and what the test checks, and never name a locator, keyword or file. The delta already complies. Now I'll run the sync workflow inline.

*The agent loads the skill `openspec-sync-specs`*

*The agent runs `mkdir -p openspec/specs/suite/search && uv run --no-sync python - <<'EOF'
from pathlib import Path
src = Path("openspec/changes/add-search-ui-tests/specs/suite/search/spec.md").read_text()
purpose_block, rest = src.split("## ADDED Requirements\n", 1)
purpose = purpose_block.split("## Purpose\n", 1)[1].strip()
out = f"# suite/search Specification\n\n## Purpose\n{purpose}\n\n## Requirements\n\n{rest.lstrip()}"
Path("openspec/specs/suite/search/spec.md").write_text(out)
EOF
head -12 openspec/specs/suite/search/spec.md; echo ...; grep -c '^### Requirement:' openspec/specs/suite/search/spec.md; grep -c '^#### Scenario:' openspec/specs/suite/search/spec.md; grep -n '^## ' openspec/specs/suite/search/spec.md; echo ---; diff <(sed -n '/^### Requirement/,$p' openspec/changes/add-search-ui-tests/specs/suite/search/spec.md) <(sed -n '/^### Requirement/,$p' openspec/specs/suite/search/spec.md) && echo "requirements identical to delta"; echo ---; openspec validate --specs 2>&1 | tail -5`*

```
# suite/search Specification

## Purpose
Records which search criteria of `shop/search` the suite verifies through the shop's pages, what each test checks, and which test verifies each criterion.

## Requirements

### Requirement: The home page's search input is verified (WEB-004_AC-1)
The suite SHALL verify WEB-004_AC-1 on the home page, `/`. The specification names the hero section but gives it no text, role or label. The test SHALL therefore recognise it the way a shopper does: a

#### Scenario: WEB-004_AC-1 Home Page Hero Shows Search Input
- **WHEN** the test opens `/` in a fresh browser context
... (13 more lines)
```

*The agent runs `openspec validate --specs 2>&1 | grep -i suite`*

```
✓ spec/suite/cart
✓ spec/suite/product-detail
✓ spec/suite/search
✓ spec/workshop/baseline-suite
```

*The agent runs `cd <repo>/openspec/changes && test -e archive/2026-09-25-add-search-ui-tests && echo "TARGET EXISTS" || { mv add-search-ui-tests archive/2026-09-25-add-search-ui-tests && ls -A archive/2026-09-25-add-search-ui-tests; }; echo ---; cd ../.. && openspec list`*

```
.openspec.yaml
design.md
proposal.md
specs
tasks.md
---
Changes:
  workshop-labs     25/37 tasks   14h ago
  ci-and-site       No tasks      14h ago
```

**Agent:**

The `add-search-ui-tests` change is archived and its specs are synced into the main specs.

- **Tasks:** all 8 were ticked, and I re-checked the key claims before archiving:
  - `openspec validate add-search-ui-tests --strict` passes.
  - The no-inline-locators hook reports nothing on `tests/ui/search.robot`.
  - `robotcode analyze` finds 0 errors in the test file and `resources/search.resource`.
  - `tests/ui/search.robot` passes 6 of 6 against the local shop (version 0.3.0, default space).
- **Specs:** I created a new main spec, `openspec/specs/suite/search/spec.md`. It holds the 4 requirements and 6 scenarios from the change unchanged, covering WEB-004_AC-1, AC-3, AC-6 and AC-7, and `openspec validate --specs` passes 16 of 16. Nothing under `openspec/specs/shop/` was touched.
- **Archive:** the change is now in `openspec/changes/archive/2026-09-25-add-search-ui-tests/`, with its `.openspec.yaml`.

I didn't re-run the whole suite with `--exclude broken`; task 3.2 records that as done. I also didn't apply a preset or reset the shop. Nothing is committed.

Two other changes are still active: `workshop-labs` (25 of 37 tasks done) and `ci-and-site` (no tasks yet).

## Step 6 - Debug in conversation

**Prompt:**

> The test "WEB-002_AC-4 Rating Filter" fails. Find the cause using only the files of this repository, including its specifications. Do not open a browser and do not use an MCP server. Explain the cause and your evidence before you change anything.

*The agent runs `cat docs/agent-environment.md docs/conventions.md && grep -rn "WEB-002_AC-4" --include=*.robot --include=*.resource --include=*.md . | head -50`*

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
... (80 more lines)
```

*The agent runs `cat -n tests/ui/catalogue.robot && echo ---- && cat -n resources/catalogue.resource && echo ---- && git diff -- tests/ui/catalogue.robot resources/catalogue.resource`*

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
... (239 more lines)
```

*The agent runs `cat -n openspec/specs/shop/catalogue/spec.md && echo ---- && cat -n openspec/specs/shop/interpretation-rules/spec.md`*

```
     1	# shop/catalogue Specification
     2	
     3	## Purpose
     4	Describes the products page, `/products`, as a shopper experiences it: the product grid, its filters, the collection previews and the highlights.
     5	
     6	## Requirements
     7	
     8	### Requirement: Full product grid (WEB-002_AC-1)
     9	When a shopper opens `/products` and the page finishes loading, the page SHALL display all 12 seeded products in a grid. Each product card SHALL show the product's name, its image, its price - 
    10	
    11	#### Scenario: Opening the products page
    12	- **WHEN** a shopper opens `/products`
... (150 more lines)
```

*The agent runs `sed -n 60,120p labs/lab-05-prompt-to-green/INSTRUCTIONS.md; echo ----; cat labs/lab-05-prompt-to-green/checklist.md; echo ----; sed -n 70,110p docs/facilitator/suite-outcomes.md; echo ----; sed -n 35,90p openspec/changes/archive/2026-09-24-baseline-suite/design.md`*

```
4. **Apply** (8 minutes). Let the agent build what the plan says:

   | Claude Code | Codex | GitHub Copilot |
   |---|---|---|
   | `/opsx:apply` | `$openspec-apply-change` | `/opsx-apply` |

5. **Run and refine** (4 minutes). Run your new tests yourself:

   ```bash
   uv run robotcode robot tests/ui/<your file>.robot
   ```

... (153 more lines)
```

*The agent runs `ls -la results/ 2>/dev/null | head; grep -rn "4 stars" --include=*.robot --include=*.resource --include=*.py --include=*.toml --include=*.md . | grep -v "^./openspec/changes/archive\|^./docs/facilitator\|^./transcripts" | head -20`*

```
total 888
drwxr-xr-x  5 user user   4096 Sep 24 22:51 .
drwxr-xr-x 22 user user   4096 Sep 24 22:11 ..
drwxr-xr-x  3 user user   4096 Sep 24 22:51 browser
drwxr-xr-x  2 user user   4096 Sep 24 21:52 lab-02
drwxr-xr-x  2 user user   4096 Sep 24 21:54 lab-03
-rw-r--r--  1 user user 290016 Sep 24 22:51 log.html
-rw-r--r--  1 user user 149742 Sep 24 22:51 output.xml
-rw-r--r--  1 user user 195874 Sep 24 22:51 playwright-log.txt
-rw-r--r--  1 user user 247078 Sep 24 22:51 report.html
tests/ui/catalogue.robot:50:    Checkbox Should Be Unchecked    4 stars and up
openspec/specs/shop/catalogue/spec.md:30:The products page SHALL display a rating filter with a "4 stars & up" checkbox, unchecked by default.
... (12 more lines)
```

*The agent loads the skill `robotcode:robotcode`*

**Agent:**

Checking the recorded failure from the last run in `results/`, without re-running anything.

*The agent runs `sed -n 1,80p ~/.claude/plugins/cache/robotframework-agent-plugins/robotcode/7c753f8adca1/skills/robotcode/references/results.md`*

```
# Interpreting test results — the `robotcode results` subcommands

`robotcode results` inspects a finished Robot Framework run — the `output.xml` / `output.json` it wrote — from the terminal. It reads the file **server-side** and returns only the slice you ask for: h

Reach for it whenever a run has finished and the question is "did it pass, what failed, why, or what changed?" — five subcommands (`summary`, `show`, `log`, `stats`, `diff`) cover those, detailed belo

> **Note**: RobotCode auto-detects non-interactive use and disables paging/colors automatically — no extra flags needed. (If a wrapper ever forces a pager, `--no-pager --no-color` before the subcomman

## Contents

1. The shared option surface across all five subcommands
2. `summary` — the headline
... (68 more lines)
```

*The agent runs `uv run --no-sync robotcode results log -t "WEB-002_AC-4 Rating Filter" 2>&1 | head -60`*

```
# Log

### Test: Catalogue.WEB-002_AC-4 Rating Filter (`tests/ui/catalogue.robot:46`) ❌ **FAIL** _(22:51:26 · 10.26 s)_

> TimeoutError: locator.elementHandle: Timeout 10000ms exceeded.
> Call log:
>   - waiting for locator('role=complementary').locator('role=checkbox\[name="4 stars and up"\]')

- **[SETUP]** **shop.Start Shop Test** ✅ **PASS** _(22:51:26 · 54 ms)_
  - **IF**
    - **IF** `"${SHOP_SPACE}"` ⏸ **NOT RUN** _(22:51:26 · 0 ms)_
      - `&{headers}` = **BuiltIn.Create Dictionary** `X-Workshop-Space=${SHOP_SPACE}` ⏸ **NOT RUN** _(22:51:26 · 0 ms)_
... (48 more lines)
```

*The agent runs `uv run --no-sync robotcode results show -s Catalogue 2>&1 | head -20`*

```
# Show — results/output.xml

- ✅ **PASS** Catalogue.WEB-002_AC-1 Every Card Offers Add To Cart (`tests/ui/catalogue.robot:17`) _(22:51:24 · 256 ms)_
- ✅ **PASS** Catalogue.WEB-002_AC-1 Card Prices Are The Product Prices (`tests/ui/catalogue.robot:26`) _(22:51:25 · 786 ms)_
- ✅ **PASS** Catalogue.WEB-002_AC-2 Categories Filter Group (`tests/ui/catalogue.robot:39`) _(22:51:25 · 409 ms)_
- ❌ **FAIL** Catalogue.WEB-002_AC-4 Rating Filter (`tests/ui/catalogue.robot:46`) _(22:51:26 · 10.26 s)_
  > TimeoutError: locator.elementHandle: Timeout 10000ms exceeded.
- ✅ **PASS** Catalogue.WEB-002_AC-7 Audio Filter Shows Only Audio (`tests/ui/catalogue.robot:52`) _(22:51:36 · 2.31 s)_
- ✅ **PASS** Catalogue.WEB-002_AC-10 Reset Filters (`tests/ui/catalogue.robot:64`) _(22:51:38 · 2.80 s)_
- ✅ **PASS** Catalogue.WEB-002_AC-12 Handpicked Highlights (`tests/ui/catalogue.robot:76`) _(22:51:41 · 325 ms)_

## Statistics
... (8 more lines)
```

**Agent:**

**Cause:** the test looks for the wrong label. It waits for a checkbox named **"4 stars and up"**, but the specification says the label is **"4 stars & up"**. The locator matches nothing, so the test times out. It never gets as far as checking whether the box is unchecked.

## Evidence

**1. The test's expected label** (`tests/ui/catalogue.robot:50`):
```robotframework
Checkbox Should Be Unchecked    4 stars and up
```
`Checkbox Should Be Unchecked` (`resources/catalogue.resource:78-81`) puts that text into `${FILTERS} >> role=checkbox[name="${label}"]`.

**2. The specification** (`openspec/specs/shop/catalogue/spec.md:30` and `:34`), which AGENTS.md makes the reference for expected behaviour:
> The products page SHALL display a rating filter with a "4 stars & up" checkbox, unchecked by default.

Line 47 quotes it the same way. No file under `openspec/specs/shop/` uses "and up". Playwright's name matching ignores case and accepts a longer name that contains the text, but "and" never matches "&". So this is a real mismatch, not a case or whitespace difference.

**3. The recorded failure** (last run in `results/output.xml`, read with `robotcode results log`):
```
TimeoutError: locator.elementHandle: Timeout 10000ms exceeded.
  - waiting for locator('role=complementary').locator('role=checkbox[name="4 stars and up"]')
```
The error is a 10 s timeout while looking for the element, not a wrong checkbox state. The element was never found.

**4. Everything else in the chain works.** In the same run, the other 6 catalogue tests passed. They include `WEB-002_AC-2 Categories Filter Group` and `WEB-002_AC-10 Reset Filters`, which find checkboxes through the same `${FILTERS} >> role=checkbox` path. The page, the sidebar locator and the keyword are fine; only the label is wrong.

**5. Finding a checkbox by its name is correct here.** `openspec/specs/shop/interpretation-rules/spec.md` allows accessible names "for a form field identified by its label", and a checkbox is one. The keyword needs no change, only its argument.

The repository also records this as deliberate. `openspec/changes/archive/2026-09-24-baseline-suite/design.md:80` (D4) says the test "expects the checkbox '4 stars and up', while `shop/catalogue` quotes '4 stars & up'". That's why it carries the `broken` tag.

I didn't open the failure screenshot or the live page, so the fix comes from the spec alone. Only a rerun will show whether the shop matches the spec.

## Proposed fix (not applied yet)

In `tests/ui/catalogue.robot`:
- line 50: `4 stars and up` → `4 stars & up`
- line 48: remove `[Tags]    broken`

Nothing in `resources/` needs to change. Then I'd run `uv run robotcode robot -t "WEB-002_AC-4 Rating Filter"`, which opens a headless browser against the local shop. Should I go ahead?

**Prompt:**

> Fix it, remove its broken tag, and run it.

*The agent edits `<repo>/tests/ui/catalogue.robot`*

```
The file <repo>/tests/ui/catalogue.robot has been updated successfully.
```

*The agent runs `uv run robotcode robot -t "WEB-002_AC-4 Rating Filter" 2>&1 | tail -25`*

```
==============================================================================
Tests                                                                         
==============================================================================
Tests.Ui                                                                      
==============================================================================
Tests.Ui.Catalogue :: The products page, /products (spec: shop/catalogue).    
==============================================================================
WEB-002_AC-4 Rating Filter :: A rating filter offers an unchecked ... | PASS |
------------------------------------------------------------------------------
Tests.Ui.Catalogue :: The products page, /products (spec: shop/cat... | PASS |
1 test, 1 passed, 0 failed
==============================================================================
... (9 more lines)
```

*The agent runs `uv run --no-sync robotcode discover tags --tests 2>&1 | grep -A5 -i "broken"; git diff -- tests/ui/catalogue.robot | sed -n '/AC-4/,/AC-7/p'`*

```
 WEB-002_AC-4 Rating Filter
     [Documentation]    A rating filter offers an unchecked minimum-rating checkbox.
-    [Tags]    broken
     Go To Catalogue
-    Checkbox Should Be Unchecked    4 stars and up
+    Checkbox Should Be Unchecked    4 stars & up
 
 WEB-002_AC-7 Audio Filter Shows Only Audio
```

**Agent:**

The test is fixed and now passes.

I changed two lines of `WEB-002_AC-4 Rating Filter` in `tests/ui/catalogue.robot`:
- **Label:** it now looks for `4 stars & up`, the text in `openspec/specs/shop/catalogue/spec.md`, instead of `4 stars and up`.
- **Tag:** I removed `[Tags]    broken`.

I ran `uv run robotcode robot -t "WEB-002_AC-4 Rating Filter"` against the local shop: 1 test, 1 passed, 0 failed. So the shop's checkbox is labelled as the spec says.

`robotcode discover tags` shows that no test in the suite carries `broken` any more. The other one, `WEB-002_AC-12 Handpicked Highlights`, had already lost it in your uncommitted changes.

Nothing is committed yet.

**The participant runs** `uv run robotcode robot --test "WEB-002_AC-4 Rating Filter"`:

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

## Step 7 - Archive

**The participant runs** `ls openspec/specs/suite 2>/dev/null; ls openspec/changes/archive | tail -3`:

```
search
2026-09-24-baseline-suite
2026-09-24-shop-specs
2026-09-24-workshop-foundation
```
