# Lab 6 - MCP: the recorded walkthrough

*Recorded with Claude Code 2.1.281, from the lab's instructions. Results are shortened; your agent's answers will differ in wording.*

## Step 1 - Connect the server

**The participant runs** `cp mcp/claude-code.mcp.json .mcp.json && cat .mcp.json`:

```
{
  "mcpServers": {
    "robotframework": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "--no-sync",
        "rf-mcp"
      ],
      "env": {
        "PYTHONPATH": "."
... (4 more lines)
```

## Step 2 - Check the connection

*Interactively, Claude Code asks you to approve the project's server; the rehearsal passes the file explicitly instead.*

**The participant runs** `claude mcp list 2>&1 | grep robotframework`:

```
robotframework: uv run --no-sync rf-mcp - ⏸ Pending approval (run `claude` to approve)
```

## Step 3 - Rebuild one test stepwise

**Prompt:**

> Using the robotframework MCP server, build a test for WEB-004_AC-3 step by step. First import the variable file shop/variables.py and the resource file resources/shop.resource, and open the shop with Open Shop Browser and Start Shop Test. Then do one step at a time, and look at the page after each step before you choose the next. Use roles, labels and visible text for locators. When every step works, save the test as tests/ui/search_stepwise.robot, with its locators in keywords under resources/.

*The agent runs `cat docs/agent-environment.md docs/conventions.md && grep -rn "WEB-004" openspec/specs/shop/ | head -30 && ls resources tests tests/ui shop`*

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
... (108 more lines)
```

*The agent runs `cat openspec/specs/shop/search/spec.md && cat openspec/specs/shop/interpretation-rules/spec.md && cat resources/shop.resource resources/search.resource tests/ui/search.robot && cat shop/variables.py && cat robot.toml`*

```
# shop/search Specification

## Purpose
Describes product search as a shopper and an API consumer experience it: the search forms, suggestions while typing, results, clearing, the empty state, and the search API.

## Requirements

### Requirement: Search form on the home page (WEB-004_AC-1)
The home page, `/`, SHALL show a search form or input in its hero section, with a placeholder or label indicating its purpose.

#### Scenario: Home page search
- **WHEN** a shopper opens `/`
... (392 more lines)
```

*The agent runs `grep -rln "search_stepwise\|stepwise" --exclude-dir=.git --exclude-dir=.venv --exclude-dir=node_modules . 2>/dev/null | head -20; cat resources/catalogue.resource | head -60; cat resources/api.resource | head -60; cat .mcp.json; git diff --stat`*

```
openspec/changes/workshop-labs/design.md
openspec/changes/workshop-labs/tasks.md
docs/WWWW_Workshop_Master_Preparation.md
docs/facilitator/run-sheet.md
labs/lab-06-mcp/checklist.md
labs/lab-06-mcp/INSTRUCTIONS.md
*** Settings ***
Documentation       The products page, /products, through the shop's stable contract:
...                 roles, accessible names, visible text and labels.

Library             Browser
Library             Collections
... (108 more lines)
```

*The agent runs `ls labs/lab-06-mcp/ 2>/dev/null; git status --short labs | head; cat labs/lab-06-mcp/checklist.md 2>/dev/null | head -80`*

```
INSTRUCTIONS.md
checklist.md
# Lab 6 - Done when

- [ ] Your agent shows the `robotframework` MCP server as connected.
- [ ] The session shows the agent running steps through the server and reading the page between them.
- [ ] Your stepwise test passes with `uv run robotcode robot tests/ui/<area>_stepwise.robot`.
- [ ] Its locators live in keywords under `resources/`.
- [ ] You can name one thing live access changed compared with your Lab 5 test, and one thing it did not.
- [ ] Only one test per criterion is left: you kept the better version and deleted the other.
- [ ] If you did the stretch goal: `uv run --no-sync python -m shop status` shows `clean` again.
```

*The agent runs `timeout 60 uv run --no-sync python -m shop status 2>&1 | tail -20`*

```
shop     http://localhost:9090  (version 0.3.0)
space    default
presets  clean, stage1
```

**Agent:**

The shop is up locally, at version 0.3.0 with a clean state. Next I'll load the robotframework MCP tools and start the stepwise session.

*The agent uses `ToolSearch` with `{"query": "select:mcp__robotframework__analyze_scenario,mcp__robotframework__execute_step,mcp__robotframework__get_session_state,mcp__robotframework__build_test`*

*The agent calls `robotframework/analyze_scenario` with `{"scenario": "WEB-004_AC-3: On the demo shop home page, a shopper enters \"headphones\" in the search input and presses Enter; a search results section lists Au`*

```
{"success":true,"scenario":{"title":"Web-004_ac-3: on the demo shop home page, a shopper enters \"headphones\" in the search input and presses enter; a search results section lists aurora neural headp
```

*The agent calls `robotframework/manage_session` with `{"action": "import_variables", "session_id": "e0305604-3453-483a-835b-a8489bcd5aff", "variable_file_path": "shop/variables.py"}`*

```
{"success":true,"session_id":"e0305604-3453-483a-835b-a8489bcd5aff","variable_file":"shop/variables.py","args":[],"variables_loaded":["SHOP_PROFILE","SHOP_SPACE","SHOP_URL"],"variables_map":{"${SHOP_P
```

*The agent calls `robotframework/manage_session` with `{"action": "import_resource", "session_id": "e0305604-3453-483a-835b-a8489bcd5aff", "resource_path": "resources/shop.resource"}`*

```
{"success":true,"session_id":"e0305604-3453-483a-835b-a8489bcd5aff","resource":"resources/shop.resource","variables_loaded":["HEADLESS"],"variable_files":[],"variables_map":{},"action":"import_resourc
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Open Shop Browser", "session_id": "e0305604-3453-483a-835b-a8489bcd5aff"}`*

```
{"success":true,"step_id":"ae9d8b48-65a8-4078-853d-0dd76c844138","keyword":"Open Shop Browser","arguments":[],"status":"pass","execution_time":0.675868,"output":"OK","assigned_variables":{},"recorded"
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Start Shop Test", "session_id": "e0305604-3453-483a-835b-a8489bcd5aff"}`*

```
{"success":true,"step_id":"92fcc686-1e28-466d-b8bd-ff9233095620","keyword":"Start Shop Test","arguments":[],"status":"pass","execution_time":0.075629,"output":"OK","assigned_variables":{},"recorded":t
```

**Agent:**

Browser and context are open. Step 1: go to the home page.

*The agent calls `robotframework/execute_step` with `{"keyword": "Go To Shop Page", "arguments": ["/"], "session_id": "e0305604-3453-483a-835b-a8489bcd5aff"}`*

```
{"success":true,"step_id":"87b07786-7d60-4774-80c2-9d03807c3ccd","keyword":"Go To Shop Page","arguments":["/"],"status":"pass","execution_time":0.11309,"output":"OK","assigned_variables":{},"recorded"
```

*The agent calls `robotframework/get_session_state` with `{"session_id": "e0305604-3453-483a-835b-a8489bcd5aff", "sections": ["page_source"], "include_reduced_dom": true, "page_source_filtered": true, "page_source_filt`*

```
{"success":true,"session_id":"e0305604-3453-483a-835b-a8489bcd5aff","sections":{"page_source":{"success":true,"session_id":"e0305604-3453-483a-835b-a8489bcd5aff","page_source_length":48253,"current_ur
```

*The agent reads `<repo>/.robotmcp_artifacts/art_7ba3c0c900d4.txt`*

**Agent:**

The home page shows a `search` landmark in `main` with a searchbox labelled "Search products" and a "Search" button. Step 2: type the query into that searchbox.

*The agent calls `robotframework/execute_step` with `{"keyword": "Fill Text", "arguments": ["role=main >> role=search >> role=searchbox[name=\"Search products\"]", "headphones"], "session_id": "e0305604-3453-483a-`*

```
{"success":true,"step_id":"87f188e3-5198-4fb8-a539-dd56968e67c2","keyword":"Fill Text","arguments":["role=main >> role=search >> role=searchbox[name=\"Search products\"]","headphones"],"status":"pass"
```

*The agent calls `robotframework/get_session_state` with `{"session_id": "e0305604-3453-483a-835b-a8489bcd5aff", "sections": ["page_source"], "include_reduced_dom": true, "page_source_filtered": true, "page_source_filt`*

```
{"success":true,"session_id":"e0305604-3453-483a-835b-a8489bcd5aff","sections":{"page_source":{"success":true,"session_id":"e0305604-3453-483a-835b-a8489bcd5aff","page_source_length":50906,"current_ur
```

*The agent runs `cd <repo>/.robotmcp_artifacts && python3 -c "import json;print(json.load(open('art_81f2c4ade883.txt'))['content'])" | sed -n '1,60p'`*

```
pyenv: version `3.12' is not installed (set by <repo>/.python-version)
```

*The agent runs `cd <repo> && uv run --no-sync python -c "import json;print(json.load(open('.robotmcp_artifacts/art_81f2c4ade883.txt'))['content'])" | sed -n '1,70p'`*

```
- document:
  - link "Skip to main content":
    - /url: "#main-content"
  - banner:
    - link "Flowline Supply":
      - /url: /
    - navigation "Primary navigation":
      - link "Home":
        - /url: /
        - img
        - text: Home
      - link "Products":
... (58 more lines)
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Press Keys", "arguments": ["role=main >> role=search >> role=searchbox[name=\"Search products\"]", "Enter"], "session_id": "e0305604-3453-483a-835b`*

```
{"success":true,"step_id":"4a5dbd6c-ecc7-4484-a489-dd2f8f5bcd62","keyword":"Press Keys","arguments":["role=main >> role=search >> role=searchbox[name=\"Search products\"]","Enter"],"status":"pass","ex
```

*The agent calls `robotframework/get_session_state` with `{"session_id": "e0305604-3453-483a-835b-a8489bcd5aff", "sections": ["page_source"], "include_reduced_dom": true, "page_source_filtered": true, "page_source_filt`*

```
{"success":true,"session_id":"e0305604-3453-483a-835b-a8489bcd5aff","sections":{"page_source":{"success":true,"session_id":"e0305604-3453-483a-835b-a8489bcd5aff","page_source_length":50681,"current_ur
```

**Agent:**

I pressed Enter and am now reading the page to see what the submit changed.

*The agent runs `uv run --no-sync python -c "import json;print(json.load(open('.robotmcp_artifacts/art_457b7d10bb47.txt'))['content'])" | sed -n '26,70p'; ls .robotmcp_artifacts | wc -l; git check-ignore -v .robotmcp_artifacts || echo "not ignored"`*

```
  - main:
    - text: Spring '25 Collection
    - heading "Upgrade your workspace with AI-first essentials" [level=1]
    - paragraph: Curated hardware, mindful accessories, and intelligent tools designed to help product teams build faster without sacrificing wellbeing.
    - search:
      - searchbox "Search products": headphones
      - button "Search"
    - paragraph:
      - text: "Trending now:"
      - link "Audio":
        - /url: /products?category=Audio
      - text: ","
... (35 more lines)
```

*The agent runs `cat labs/lab-06-mcp/INSTRUCTIONS.md`*

```
# Lab 6 - MCP

In Lab 5 your agent wrote tests without ever seeing the page. Now give it live access: the Robot Framework
[MCP server](../../GLOSSARY.md#mcp) runs one keyword at a time in a session that stays open, and lets the agent look
at the page before it decides the next step. Rebuild one of your Lab 5 tests that way, and compare.

| | |
|---|---|
| Module | 6 - Robot Framework MCP: The Live-Access Upgrade |
| Time | 25 minutes |
| Shop preset | `clean` |
| You need | Lab 5 done: one passing test of your own. If you have none, rebuild WEB-004_AC-3 instead |
... (66 more lines)
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Wait For Elements State", "arguments": ["role=main >> role=region[name=\"Search results\"]", "visible"], "session_id": "e0305604-3453-483a-835b-a84`*

```
{"success":true,"step_id":"c50bcfd2-860d-4a82-a79f-faaa510b69da","keyword":"Wait For Elements State","arguments":["role=main >> role=region[name=\"Search results\"]","visible"],"status":"pass","execut
```

**Agent:**

Step 5: find the Aurora card inside the results, by its heading's name.

*The agent calls `robotframework/execute_step` with `{"keyword": "Get Element Count", "arguments": ["role=main >> role=region[name=\"Search results\"] >> role=article >> internal:has=\"role=heading[name='Aurora Ne`*

```
{"success":true,"step_id":"372a3e8f-f0cd-4535-bcff-f2e12d77e0eb","keyword":"Get Element Count","arguments":["role=main >> role=region[name=\"Search results\"] >> role=article >> internal:has=\"role=he
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Get Element Count", "arguments": ["role=main >> role=region[name=\"Search results\"] >> article:has-text(\"Aurora Neural Headphones\")", "==", "1"]`*

```
{"success":true,"step_id":"fcec4708-2951-402a-b5ff-239cdef81f7a","keyword":"Get Element Count","arguments":["role=main >> role=region[name=\"Search results\"] >> article:has-text(\"Aurora Neural Headp
```

**Agent:**

Step 6: the card's name, taken from its heading.

*The agent calls `robotframework/execute_step` with `{"keyword": "Get Text", "arguments": ["role=main >> role=region[name=\"Search results\"] >> article:has-text(\"Aurora Neural Headphones\") >> role=heading", "*=`*

```
{"success":true,"step_id":"b815de26-7737-4a61-b9cb-956986deff5f","keyword":"Get Text","arguments":["role=main >> role=region[name=\"Search results\"] >> article:has-text(\"Aurora Neural Headphones\") 
```

**Agent:**

Step 7: the card's image, found by its alt text ("Aurora Neural Headphones product photo"), and checked for being visible and actually loaded.

*The agent calls `robotframework/execute_step` with `{"keyword": "Wait For Elements State", "arguments": ["role=main >> role=region[name=\"Search results\"] >> article:has-text(\"Aurora Neural Headphones\") >> rol`*

```
{"success":true,"step_id":"f25b7737-0bf8-4e5d-bf9e-781770213902","keyword":"Wait For Elements State","arguments":["role=main >> role=region[name=\"Search results\"] >> article:has-text(\"Aurora Neural
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Get Property", "arguments": ["role=main >> role=region[name=\"Search results\"] >> article:has-text(\"Aurora Neural Headphones\") >> role=img[name=`*

```
{"success":true,"step_id":"ed34e5f7-bc08-4461-9725-893f1f190725","keyword":"Get Property","arguments":["role=main >> role=region[name=\"Search results\"] >> article:has-text(\"Aurora Neural Headphones
```

**Agent:**

The image is visible and loaded (naturalWidth 1024). Step 8: the price. First I'll look at how the card renders it, and at the repo's existing price helpers.

*The agent runs `sed -n '60,200p' resources/catalogue.resource; sed -n '60,200p' resources/api.resource`*

```
    Check Checkbox    ${FILTERS} >> role=checkbox[name="${category}"]

Apply Filters
    Click    ${FILTERS} >> role=button[name="Apply filters"]
    Wait For Elements State    ${GRID}    visible

Get Category Checkbox Count
    ${count}=    Get Element Count    ${FILTERS} >> role=group[name="Categories"] >> role=checkbox
    RETURN    ${count}

Filter Checkboxes Should All Be Unchecked
    [Documentation]    Every checkbox of the filter sidebar is unchecked.
... (41 more lines)
```

*The agent calls `robotframework/manage_session` with `{"action": "import_resource", "session_id": "e0305604-3453-483a-835b-a8489bcd5aff", "resource_path": "resources/api.resource"}`*

*The agent calls `robotframework/manage_session` with `{"action": "import_resource", "session_id": "e0305604-3453-483a-835b-a8489bcd5aff", "resource_path": "resources/catalogue.resource"}`*

```
{"success":true,"session_id":"e0305604-3453-483a-835b-a8489bcd5aff","resource":"resources/api.resource","variables_loaded":[],"variable_files":[],"variables_map":{},"action":"import_resource"}
```

```
{"success":true,"session_id":"e0305604-3453-483a-835b-a8489bcd5aff","resource":"resources/catalogue.resource","variables_loaded":["CARD PRICE","FILTERS","GRID","HIGHLIGHTS"],"variable_files":[],"varia
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Open Shop API", "session_id": "e0305604-3453-483a-835b-a8489bcd5aff"}`*

```
{"success":true,"step_id":"b331792a-9f7b-4d36-8a9c-437de9fb57e9","keyword":"Open Shop API","arguments":[],"status":"pass","execution_time":0.003994,"output":"OK","assigned_variables":{},"recorded":tru
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Get Product From API", "arguments": ["1"], "assign_to": "product", "session_id": "e0305604-3453-483a-835b-a8489bcd5aff"}`*

```
{"success":true,"step_id":"dd1b52b7-662d-4249-bf6a-c8043ebd3dab","keyword":"Get Product From API","arguments":["1"],"status":"pass","execution_time":0.014646,"output":"{'id': 1, 'name': 'Aurora Neural
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Format Price", "arguments": ["${product}[price]"], "assign_to": "expected", "session_id": "e0305604-3453-483a-835b-a8489bcd5aff"}`*

```
{"success":true,"step_id":"4bbff87d-dad6-417c-a306-c350e80b59b9","keyword":"Format Price","arguments":["${product}[price]"],"status":"pass","execution_time":0.00265,"output":"$249.99","assigned_variab
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Get Element Count", "arguments": ["role=main >> role=region[name=\"Search results\"] >> article:has-text(\"Aurora Neural Headphones\") >> ${CARD PR`*

```
{"success":true,"step_id":"5d049280-f09d-4a2f-a7b8-18bd9fb61620","keyword":"Get Element Count","arguments":["role=main >> role=region[name=\"Search results\"] >> article:has-text(\"Aurora Neural Headp
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Get Text", "arguments": ["role=main >> role=region[name=\"Search results\"] >> article:has-text(\"Aurora Neural Headphones\") >> ${CARD PRICE}", "=`*

```
{"success":true,"step_id":"999680ca-0fdd-4e82-a22d-d35948958ee1","keyword":"Get Text","arguments":["role=main >> role=region[name=\"Search results\"] >> article:has-text(\"Aurora Neural Headphones\") 
```

*The agent calls `robotframework/build_test_suite` with `{"test_name": "WEB-004_AC-3 Enter Lists Headphones As A Card", "session_id": "e0305604-3453-483a-835b-a8489bcd5aff", "tags": ["WEB-004", "ui"], "documentation":`*

```
{"success":true,"session_id":"e0305604-3453-483a-835b-a8489bcd5aff","warnings":[{"type":"untracked_variables","count":4,"variables":["0","CARD PRICE","expected","product"],"fix":"manage_session(action
```

*The agent runs `cat .robotmcp_artifacts/art_475c5c7c71dc.txt`*

```
*** Settings ***
Documentation    Test suite generated from session e0305604-3453-483a-835b-a8489bcd5aff containing 1 test case for web automation.
Resource        resources${/}shop.resource
Resource        resources${/}api.resource
Resource        resources${/}catalogue.resource
Library         XML
Library         Browser
Variables       shop${/}variables.py
Test Tags       ui    WEB-004    automated    generated    web

*** Test Cases ***
WEB-004_AC-3 Enter Lists Headphones As A Card
... (19 more lines)
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Get Element Count", "arguments": ["role=main >> role=region[name=\"Search results\"] >> article:has-text(\"Aurora Neural Headphones\") >> role=img[`*

```
Step execution failed: Keyword execution failed: Element count for selector `role=main >> role=region[name="Search results"] >> article:has-text("Aurora Neural Headphones") >> role=img[name="Aurora Ne
Step ID: 38829996-0e35-49ec-a51e-5dadf56b316e
```

**Agent:**

No match: this Browser version matches role names exactly, so the image keeps the verified case-insensitive regex, with the name escaped. Now I'll write the resource and the test.

*The agent writes `<repo>/resources/search_stepwise.resource`*

```
File created successfully at: <repo>/resources/search_stepwise.resource (file st
```

*The agent writes `<repo>/tests/ui/search_stepwise.robot`*

```
File created successfully at: <repo>/tests/ui/search_stepwise.robot (file state 
```

**Agent:**

Files written. Next: static analysis with RobotCode, then the test run.

*The agent runs `timeout 300 uv run robotcode analyze code tests/ui/search_stepwise.robot resources/search_stepwise.resource 2>&1 | tail -20`*

```
Files: 2, Errors: 0, Warnings: 0, Infos: 0, Hints: 0 (in 0.18s)
```

*The agent runs `timeout 300 uv run robotcode robot tests/ui/search_stepwise.robot 2>&1 | tail -25`*

```
==============================================================================
Search Stepwise :: Search on the home page (spec: shop/search), built step ...
==============================================================================
WEB-004_AC-3 Enter Lists Aurora Neural Headphones As A Card :: Sea... | PASS |
------------------------------------------------------------------------------
Search Stepwise :: Search on the home page (spec: shop/search), bu... | PASS |
1 test, 1 passed, 0 failed
==============================================================================
Output:  <repo>/results/output.xml
Log:     <repo>/results/log.html
Report:  <repo>/results/report.html
```

**Agent:**

The test passes. To confirm it can also fail, I'll load the new resource into the live MCP session and give the price keyword a wrong amount.

*The agent calls `robotframework/manage_session` with `{"action": "import_resource", "session_id": "e0305604-3453-483a-835b-a8489bcd5aff", "resource_path": "resources/search_stepwise.resource"}`*

```
{"success":true,"session_id":"e0305604-3453-483a-835b-a8489bcd5aff","resource":"resources/search_stepwise.resource","variables_loaded":["RESULTS REGION","SEARCH BOX"],"variable_files":[],"variables_ma
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Result Card Should Show Price", "arguments": ["Aurora Neural Headphones", "199.99"], "session_id": "e0305604-3453-483a-835b-a8489bcd5aff", "raise_o`*

*The agent calls `robotframework/execute_step` with `{"keyword": "Search Results Should Show Card For", "arguments": ["Orbit Drone Camera"], "session_id": "e0305604-3453-483a-835b-a8489bcd5aff", "raise_on_failure"`*

```
{"success":false,"step_id":"69f904c2-c29c-4ada-8001-34fe7c725450","keyword":"Result Card Should Show Price","arguments":["Aurora Neural Headphones","199.99"],"status":"fail","execution_time":1.165224,
```

```
{"success":false,"step_id":"0334c322-9407-431d-84f2-56b91ac70e5e","keyword":"Search Results Should Show Card For","arguments":["Orbit Drone Camera"],"status":"fail","execution_time":1.145825,"error":"
```

*The agent calls `robotframework/execute_step` with `{"keyword": "Close Browser", "session_id": "e0305604-3453-483a-835b-a8489bcd5aff", "record": false}`*

```
{"success":true,"step_id":"7456d64e-b505-4e09-b878-83520820ee1c","keyword":"Close Browser","arguments":[],"status":"pass","execution_time":0.03676,"output":"OK","assigned_variables":{},"recorded":fals
```

*The agent runs `ls -la --time-style=full-iso .robotmcp_artifacts; cat .gitignore | head -30; git status --short`*

```
total 88
drwxr-xr-x  2 user user  4096 2026-09-25 11:58:20.407072166 +0200 .
drwxr-xr-x 23 user user  4096 2026-09-25 11:56:30.023495771 +0200 ..
-rw-r--r--  1 user user  7170 2026-09-25 11:56:30.026472814 +0200 art_064d89c4ddcc.txt
-rw-r--r--  1 user user  7367 2026-09-25 11:56:40.483031305 +0200 art_32a998926ae3.txt
-rw-r--r--  1 user user  2067 2026-09-25 11:56:57.625189919 +0200 art_42116940e57b.txt
-rw-r--r--  1 user user 10378 2026-09-25 11:56:57.625106561 +0200 art_457b7d10bb47.txt
-rw-r--r--  1 user user  2285 2026-09-25 11:58:20.407072166 +0200 art_475c5c7c71dc.txt
-rw-r--r--  1 user user  9578 2026-09-25 11:56:30.026720923 +0200 art_7ba3c0c900d4.txt
-rw-r--r--  1 user user 10538 2026-09-25 11:56:40.483232736 +0200 art_81f2c4ade883.txt
-rw-r--r--  1 user user  7367 2026-09-25 11:56:57.624914480 +0200 art_8aff74a4a177.txt
-rw-r--r--  1 user user  2067 2026-09-25 11:56:30.026863640 +0200 art_90a90cfb40bf.txt
... (55 more lines)
```

*The agent runs `rm -r .robotmcp_artifacts && git status --short | grep -E "robotmcp|stepwise"`*

```
?? resources/search_stepwise.resource
?? tests/ui/search_stepwise.robot
```

**Agent:**

I built the WEB-004_AC-3 test one step at a time through the robotframework MCP server and saved it as `tests/ui/search_stepwise.robot`. It passes with `uv run robotcode robot tests/ui/search_stepwise.robot`, and RobotCode's analysis reports no errors or warnings.

**How it was built.** I imported `shop/variables.py` and `resources/shop.resource`, then ran Open Shop Browser and Start Shop Test. After each step I read the page before choosing the next one:
1. Opened `/`. The page's main area has a search section with a searchbox labelled "Search products" and a "Search" button.
2. Typed "headphones" in the searchbox. A suggestion list and a "Search results" region with the Aurora card appeared right away, before anything was submitted.
3. Pressed Enter. The suggestion list closed and the results stayed.
4. Checked the "Search results" region is shown, with exactly one card for Aurora Neural Headphones, found by its visible text.
5. Checked the card's heading shows the name.
6. Checked the card's image is visible and has actually loaded, found by its alt text.
7. Checked the card shows exactly one price, and that it is $249.99, the price the shop's API gives for product 1.

**Files**
- `tests/ui/search_stepwise.robot`: calls keywords only.
- `resources/search_stepwise.resource`: new file with all the locators, in six keywords such as `Search Products With Enter` and `Result Card Should Show Price`. It reuses the price helpers in `catalogue.resource` and `api.resource`. I used new keyword names so they don't clash with `search.resource`.

To check the test can fail, I gave the keywords wrong inputs in the live session:
- A wrong price fails with "should show the price $199.99, not '$249.99'".
- "Orbit Drone Camera" fails with "not 0". That product is on the page but not in the results, so the card check only looks inside the results.

**What live access showed**
- **The shop searches as you type.** Results appear before Enter is pressed, so this test can't prove Enter itself caused them; the existing test in `tests/ui/search.robot` has the same limit. It still checks what the spec requires after a submit.
- **Label matching is exact.** I tried matching the image by the plain product name and it found nothing. In this setup a label has to match in full, so the image lookup keeps a case-insensitive pattern.
- **Not checked:** the spec says results appear "as a grid". The test checks the cards, not the layout.

**Left for you**
- There are now two tests for WEB-004_AC-3. The lab's compare step says to keep the better one and delete the other; that's your call, so I haven't deleted either.
- Nothing is committed.
- The MCP server saves page snapshots to `.robotmcp_artifacts/` in the repo, and git doesn't ignore that folder. I deleted this session's snapshots. You may want to add the folder to `.gitignore`.

## Step 4 - Run it

**The participant runs** `uv run robotcode robot tests/ui/search_stepwise.robot`:

```
==============================================================================
Search Stepwise :: Search on the home page (spec: shop/search), built step ...
==============================================================================
WEB-004_AC-3 Enter Lists Aurora Neural Headphones As A Card :: Sea... | PASS |
------------------------------------------------------------------------------
Search Stepwise :: Search on the home page (spec: shop/search), bu... | PASS |
1 test, 1 passed, 0 failed
==============================================================================
Output:  <repo>/results/output.xml
Log:     <repo>/results/log.html
Report:  <repo>/results/report.html
```

## Step 5 - Compare

**Prompt:**

> Compare the test for WEB-004_AC-3 in tests/ui/search.robot with the one in tests/ui/search_stepwise.robot, and the keywords they use. Which locators and waits differ, and which assumption of the first version did live access confirm or correct? Then keep the better version, delete the other, and run what is left.

*The agent runs `cat docs/agent-environment.md && echo ---- && cat docs/conventions.md && echo ---- && cat tests/ui/search.robot && echo ---- && cat tests/ui/search_stepwise.robot && echo ---- && cat resources/search.resource && echo ---- && cat resources/search_stepwise.resource`*

```
# Environment

- Install: `uv sync --locked`, then `uv run --no-sync rfbrowser install chromium`.
- Check the environment: `uv run --no-sync python setup-check/check.py`.
- Run the suite: `uv run robotcode robot`. Plain `robot` ignores `robot.toml` and cannot find the shop.
- Run one test: `uv run robotcode robot -t "<test name>"`.
- `-p shared` selects the shared instance: `uv run robotcode -p shared robot`. Without it, the local shop.
- Logs and reports go to `results/`, which git ignores.
----
# Test conventions

How the tests in this repository are written. The shipped suite follows these rules, and so should every test you or
... (370 more lines)
```

*The agent runs `cat resources/shop.resource && echo ---- && grep -n "CARD PRICE\|Format Price\|GRID" -A6 resources/catalogue.resource | head -60 && echo ---- && ls openspec/specs/shop/ openspec/changes/archive/*search* && grep -n "AC-3" -B2 -A12 openspec/specs/shop/search/spec.md`*

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
... (98 more lines)
```

*The agent runs `cat openspec/changes/archive/2026-09-25-add-search-ui-tests/design.md && echo ---- && grep -rln "stepwise" --exclude-dir=results --exclude-dir=.venv . 2>/dev/null | head -20; ls openspec/specs/suite/; cat robot.toml`*

```
# Design

## Context

See `proposal.md` for the motivation and `specs/suite/search/spec.md` for what each test checks. The facts below come
from the local shop at version `0.3.0`, with the space in its reset state (`clean` and `stage1` both hold). They were
read from:
- the served HTML of `/` and `/products`;
- `/static/app.js`;
- the results the shop renders for "headphones" and "xyz123";
- `GET /api/products/` and `GET /api/search/?query=headphones`.

... (337 more lines)
```

*The agent runs `cat labs/lab-06-mcp/INSTRUCTIONS.md && echo ---- && cat labs/lab-06-mcp/checklist.md && grep -n -i "stepwise" -B2 -A5 docs/facilitator/run-sheet.md openspec/changes/workshop-labs/design.md | head -80`*

```
# Lab 6 - MCP

In Lab 5 your agent wrote tests without ever seeing the page. Now give it live access: the Robot Framework
[MCP server](../../GLOSSARY.md#mcp) runs one keyword at a time in a session that stays open, and lets the agent look
at the page before it decides the next step. Rebuild one of your Lab 5 tests that way, and compare.

| | |
|---|---|
| Module | 6 - Robot Framework MCP: The Live-Access Upgrade |
| Time | 25 minutes |
| Shop preset | `clean` |
| You need | Lab 5 done: one passing test of your own. If you have none, rebuild WEB-004_AC-3 instead |
... (92 more lines)
```

*The agent runs `uv run --no-sync python -m shop status 2>&1 | tail -20`*

```
shop     http://localhost:9090  (version 0.3.0)
space    default
presets  clean, stage1
```

**Agent:**

Shop is up and clean. I'm running both AC-3 versions now before comparing them.

*The agent runs `uv run robotcode robot -d results/compare -i WEB-004 -t "WEB-004_AC-3*" tests/ui/search.robot tests/ui/search_stepwise.robot 2>&1 | tail -25`*

```
==============================================================================
Search & Search Stepwise                                                      
==============================================================================
Search & Search Stepwise.Search :: Product search on the home page and the ...
==============================================================================
WEB-004_AC-3 Enter Shows Matching Results :: Searching "headphones... | PASS |
------------------------------------------------------------------------------
WEB-004_AC-3 Search Button Shows Matching Results :: Searching "he... | PASS |
------------------------------------------------------------------------------
Search & Search Stepwise.Search :: Product search on the home page... | PASS |
2 tests, 2 passed, 0 failed
==============================================================================
... (13 more lines)
```

*The agent runs `ls transcripts/ 2>/dev/null; wc -l transcripts/lab-06-mcp.md 2>/dev/null; cat openspec/specs/suite/search/spec.md | head -80`*

```
# suite/search Specification

## Purpose
Records which search criteria of `shop/search` the suite verifies through the shop's pages, what each test checks, and which test verifies each criterion.

## Requirements

### Requirement: The home page's search input is verified (WEB-004_AC-1)
The suite SHALL verify WEB-004_AC-1 on the home page, `/`. The specification names the hero section but gives it no text, role or label. The test SHALL therefore recognise it the way a shopper does: a

#### Scenario: WEB-004_AC-1 Home Page Hero Shows Search Input
- **WHEN** the test opens `/` in a fresh browser context
... (38 more lines)
```

*The agent writes `<scratch>`*

```
Claude requested permissions to write to <scratch> but you haven't grant
```

*The agent runs `uv run robotcode robot -d ../../probe/results ../../probe/probe_search.robot 2>&1 | grep -v "^Output\|^Log\|^Report" | tail -40`*

```
[ ERROR ] Parsing '<repo>/../../probe/probe_search.robot' failed: File or direct

Try --help for usage information.
```

**Agent:**

Writing outside the repo isn't permitted, so I'll put the probe in the git-ignored `results/` folder and delete it afterwards.

*The agent writes `<repo>/results/probe/probe_search.robot`*

```
File created successfully at: <repo>/results/probe/probe_search.robot (file stat
```

*The agent runs `uv run robotcode robot -d results/probe/out results/probe/probe_search.robot 2>&1 | grep -v "^Output\|^Log:\|^Report" | tail -40`*

```
==============================================================================
Probe Search                                                                  
==============================================================================
Probe Locators                                                        
searchbox in main: 1
searchbox on page: 1
named searchbox in search landmark: 1
results region before search: 0
results region after search: page 1, in main 1
cards: 1
aurora cards: 1
heading: "Aurora Neural Headphones"
... (15 more lines)
```

**Agent:**

The probe confirms the first version's facts. Next I'm checking that nothing else uses the stepwise resource, and whether the lab checker expects a stepwise file.

*The agent runs `rm -rf results/probe && grep -rn "search_stepwise\|_stepwise" --include=*.robot --include=*.resource --include=*.py --include=*.toml . 2>/dev/null | grep -v "^./.venv" ; ls labs/ | head; grep -rln "stepwise" labs/ tools/ 2>/dev/null`*

```
tests/ui/search_stepwise.robot:7:Resource            resources/search_stepwise.resource
README.md
lab-00-arrival
lab-02-context
lab-03-skills
lab-04-robotcode
lab-05-prompt-to-green
lab-06-mcp
lab-07-hooks-toolbelt
lab-08-healing
lab-09-ci
labs/lab-06-mcp/checklist.md
... (1 more lines)
```

**Agent:**

Only the stepwise test uses `search_stepwise.resource`. I'm keeping `search.robot` and deleting the stepwise test and its resource.

*The agent runs `rm tests/ui/search_stepwise.robot resources/search_stepwise.resource && uv run robotcode robot tests/ui/search.robot 2>&1 | tail -25`*

```
==============================================================================
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
... (9 more lines)
```

**Agent:**

I kept `tests/ui/search.robot`, deleted `tests/ui/search_stepwise.robot` and `resources/search_stepwise.resource`, and ran the remaining suite: **6 tests, 6 passed**. Before deleting, I ran both AC-3 versions and both passed. Both deleted files were untracked, so git can't bring them back.

## Locators

| Element | `search.resource` (first version) | `search_stepwise.resource` |
|---|---|---|
| Search input | `role=main >> role=searchbox` | `role=main >> role=search >> role=searchbox[name="Search products"]` |
| Results section | `role=region[name=/search results/i]` | `role=main >> role=region[name="Search results"]` |
| Card, image, price | `article:has-text(name)`, `role=img[name=/name/i]`, `${CARD PRICE}` | the same three locators |
| Card heading | `role=heading`, checked with `Should Contain … ignore_case=True` | `role=heading`, checked with `*=`, which is case-sensitive |

## Waits

- **Results section:** both wait until it is visible, the same way.
- **Card:** the first version waits until the card is visible. The stepwise version uses `Get Element Count == 1`, which also retries, but it counts matches rather than checking visibility. It also requires exactly one card.
- **Heading:** the first version reads the text once, after the card is visible. The stepwise version's `*=` check retries until the timeout.
- **Image and price:** the same in both, including the image-load check (`naturalWidth > 0`).

## What live access confirmed or corrected

The first version was planned from the page's HTML and the shop's JavaScript, with a short browser check. It assumed:
- the main content holds exactly one searchbox;
- the results are in a region labelled "Search results", hidden until a search;
- "headphones" returns one card, whose heading holds the name;
- the image's alt text names the product and the image loads;
- the card shows exactly one price;
- the page does not navigate.

Live access **confirmed all of these and corrected none**. The stepwise session ended up with the same card, image and price locators. I also checked the live page myself with a throwaway script, since removed:
- one searchbox on the whole page;
- the results region absent before the search, then present once, inside the main content;
- one card, headed "Aurora Neural Headphones";
- an image with the alt text "Aurora Neural Headphones product photo" that had loaded;
- the URL still `/` after Enter.

- **What live access changed:** it pinned what the shop happens to show. The input is found by the name "Search products", inside the search form.
- **What it did not change:** neither version can tell whether Enter produced the results. The shop also searches by itself about 300 ms after typing stops, and typing alone showed results within 1 s.

## Why the first version is better

- **"Search products" comes from the shop, not the spec.** `docs/conventions.md` §4 allows an accessible name only where the spec speaks of a label. The search change's design ruled out this exact string. It is also the label on `/` only: on `/products` the label is "Search the catalogue", so the stepwise keyword can't serve the products-page test.
- **The stepwise heading check is case-sensitive.** §4 says ignore case, and the stepwise version's own card locator already does.
- **Coverage:** `openspec/specs/suite/search/spec.md` requires one AC-3 test for Enter and one for the search button. The stepwise suite has only Enter. `search.robot` has both, plus the AC-1, AC-6 and AC-7 tests.
- **Duplication:** the stepwise resource mostly copied keywords that already exist in `search.resource`.

The stepwise version did have one good idea: it finds the input inside its search form, as conventions §5 asks. I didn't carry that over, because the AC-1 test deliberately counts every searchbox in the main content.

The two AC-3 tests left in `search.robot`, one for Enter and one for the button, are not duplicates: the suite spec asks for one test per way of submitting.

## Step 6 - The cost

*`/context` is interactive; in a session it shows how much of the context the server's tools take.*
