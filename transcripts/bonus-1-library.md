# Bonus 1 - A library: the recorded walkthrough

*Recorded with Claude Code 2.1.289, from the lab's instructions. Results are shortened; your agent's answers will differ in wording.*

## Step 1 - Start the project next to the clone

**The participant runs** `uv init --lib demoshop-library`:

```
Initialized project `demoshop-library` at `<repo>`
```

**The participant runs** `uv add "robotframework==7.5" "robotframework-assertion-engine==5.0.1" "robotframework-pythonlibcore==4.6.0" "requests==2.34.2"
uv add --dev pytest`:

```
 ~ demoshop-library==0.1.0 (from file://<repo>)
 + iniconfig==2.3.0
 + packaging==26.3
 + pluggy==1.6.0
 + pygments==2.21.0
 + pytest==9.1.1
```

## Step 2 - Save the references

**The participant runs** `mkdir references
curl -s http://localhost:9090/openapi.json -o references/demoshop-openapi.json
curl -sL https://raw.githubusercontent.com/MarketSquare/AssertionEngine/main/README.md -o references/assertionengine-readme.md
# Keywords to imitate, and AssertionEngine's code, from the workshop's environment
cd ../ai-engineering-robotframework
uv run robotcode libdoc Browser show "Get Text" > ../demoshop-library/references/browser-get-text.md
uv run robotcode libdoc Browser show "Get Element Count" > ../demoshop-library/references/browser-get-element-count.md
uv run --no-sync python -c "import shutil, assertionengine.assertion_engine as m; shutil.copy(m.__file__, '../demoshop-library/references/assertion_engine.py')"
cd ../demoshop-library`:

*(no output)*

**The participant runs** `ls -l references | cut -c30-`:

```

8 Oct  6 19:57 assertion_engine.py
9 Oct  6 19:57 assertionengine-readme.md
4 Oct  6 19:57 browser-get-element-count.md
2 Oct  6 19:57 browser-get-text.md
7 Oct  6 19:57 demoshop-openapi.json
```

## Step 3 - Write AGENTS.md

*In the lab you write this file yourself. For the reference, the rehearsal lets the agent draft it from the lab's own list, and the transcript says so.*

**Prompt:**

> Write AGENTS.md for this project from this list, as the sections Toolstack, References, Concepts, Examples and Specification, short, and nothing else:
>
> - **Toolstack:**
>   - Python 3.12 with uv;
>   - dependencies at run time: Robot Framework 7.5, AssertionEngine, PythonLibCore and requests, pinned in
>     `pyproject.toml`;
>   - unit tests with `uv run pytest`;
>   - Robot tests in `atest/`, against the local shop at `http://localhost:9090`, run with
>     `uv run robot --outputdir results atest`;
>   - the keyword documentation is generated with
>     `uv run python -m robot.libdoc demoshop_library.DemoShopLibrary docs/DemoShopLibrary.html`;
>   - packaging with `uv build`.
> - **References:**
>   - `references/demoshop-openapi.json`, the API of the shop version under test;
>   - the User Guide's
>     [Creating test libraries](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#creating-test-libraries)
>     and [library scope](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#library-scope),
>     for Robot Framework 7.5.
> - **Concepts:**
>   - every `Get` keyword takes `assertion_operator`, `assertion_expected` and `message`, and checks with
>     AssertionEngine's `verify_assertion` (`references/assertion_engine.py`, `references/assertionengine-readme.md`);
>   - the library is built on PythonLibCore;
>   - it is imported with `url` and an optional `space`, which it sends as `X-Workshop-Space`;
>   - each library instance keeps one cart.
> - **Examples:** `references/browser-get-text.md` and `references/browser-get-element-count.md`: keyword names,
>   arguments and documentation to imitate.
> - **Specification:** OpenSpec, under `openspec/changes/`.

*The agent runs `ls -a && ls references src && cat pyproject.toml`*

```
.
..
.git
.gitignore
.python-version
.venv
README.md
pyproject.toml
references
src
uv.lock
references:
... (32 more lines)
```

*The agent writes `<repo>/AGENTS.md`*

```
File created successfully at: <repo>/AGENTS.md (file state is current in yo
```

**Agent:**

I created `AGENTS.md` in the project root with the five sections you listed: Toolstack, References, Concepts, Examples and Specification. It contains only the content you gave me.

I checked the paths it points to. The files under `references/` exist, and the four run-time dependencies are pinned in `pyproject.toml`. Three locations it names don't exist yet: `atest/`, `docs/` and `openspec/`.

**The participant runs** `cat AGENTS.md`:

```
# AGENTS.md

## Toolstack

- Python 3.12 with uv.
- Run-time dependencies: Robot Framework 7.5, AssertionEngine, PythonLibCore and requests, pinned in `pyproject.toml`.
- Unit tests: `uv run pytest`.
- Robot tests live in `atest/` and run against the local shop at `http://localhost:9090`:
  `uv run robot --outputdir results atest`.
- Keyword documentation:
  `uv run python -m robot.libdoc demoshop_library.DemoShopLibrary docs/DemoShopLibrary.html`.
- Packaging: `uv build`.
... (25 more lines)
```

## Step 4 - Set up OpenSpec

**The participant runs** `openspec init --tools claude`:

```

Learn more: https://github.com/Fission-AI/OpenSpec
Feedback:   https://github.com/Fission-AI/OpenSpec/issues

- Setting up Claude Code...
[32m✔[39m Setup complete for Claude Code
```

*In the lab you write this file yourself. For the reference, the rehearsal lets the agent draft it from the lab's own list, and the transcript says so.*

**Prompt:**

> In openspec/config.yaml, uncomment `context:` and write there, in a few lines each, the five points of AGENTS.md: toolstack, references, concepts, examples and specification. Change nothing else in the file.

*The agent reads `<repo>/openspec/config.yaml`*

*The agent edits `<repo>/openspec/config.yaml`*

```
The file <repo>/openspec/config.yaml has been updated successfully. (file s
```

*The agent runs `(python3 -c "import yaml,sys; d=yaml.safe_load(open('openspec/config.yaml')); print(sorted(d)); print(d['context'])" 2>&1 || uv run --with pyyaml python -c "import yaml; d=yaml.safe_load(open('openspec/config.yaml')); print(sorted(d)); print(d['context'])")`*

```
pyenv: version `3.12' is not installed (set by <repo>/.python-version)
['context', 'schema']
Toolstack:
- Python 3.12 with uv. Run-time dependencies: Robot Framework 7.5, AssertionEngine,
  PythonLibCore and requests, pinned in pyproject.toml.
- Unit tests: `uv run pytest`. Robot tests live in atest/ and run against the local shop
  at http://localhost:9090: `uv run robot --outputdir results atest`.
- Keyword documentation: `uv run python -m robot.libdoc demoshop_library.DemoShopLibrary docs/DemoShopLibrary.html`.
  Packaging: `uv build`.

References:
- references/demoshop-openapi.json: the API of the shop version under test.
... (18 more lines)
```

**Agent:**

I uncommented `context:` in `openspec/config.yaml` and replaced the three sample lines under it with the five points from AGENTS.md: Toolstack, References, Concepts, Examples and Specification. Each is a short labelled section. I checked the file with a YAML parser: it parses and has two keys, `schema` and `context`.

Nothing else in the file changed. One thing reads a little oddly: the `# Example:` comment above `context:` is still there. It belonged to the sample I replaced. I left it because you asked me not to change anything else, but you may want to delete that one line.

**The participant runs** `sed -n '1,30p' openspec/config.yaml`:

```
schema: spec-driven

# Project context (optional)
# This is shown to AI when creating artifacts.
# Add your tech stack, conventions, style guides, domain knowledge, etc.
# Example:
context: |
  Toolstack:
  - Python 3.12 with uv. Run-time dependencies: Robot Framework 7.5, AssertionEngine,
    PythonLibCore and requests, pinned in pyproject.toml.
  - Unit tests: `uv run pytest`. Robot tests live in atest/ and run against the local shop
    at http://localhost:9090: `uv run robot --outputdir results atest`.
... (18 more lines)
```

**Prompt:**

> Which instruction files did you load at the start of this session? Name each file with its path.

**Agent:**

Only one instruction file was loaded at the start of this session:

- `<repo>/AGENTS.md` is the project instruction file, checked into the codebase.

No `CLAUDE.md` was loaded, either at the project level or the user level. No memory index (`MEMORY.md`) was loaded either.

`AGENTS.md` mentions other files under `references/` (for example `demoshop-openapi.json`, `assertion_engine.py` and `browser-get-text.md`). Those were not loaded. They're only listed there as files to consult when needed.

## Step 5 - Propose the first slice

**Prompt:**

> /opsx:propose A Robot Framework library, `demoshop_library.DemoShopLibrary`, for the DemoShop's REST API, built on PythonLibCore, and imported with `url` and an optional `space`. A first slice of keywords: `Get Product Count`, `Get Product Price` (a product id), `Add Product To Cart` (a product id and an optional quantity), `Get Cart Item Count` and `Get Cart Total`. Every `Get` keyword takes `assertion_operator`, `assertion_expected` and `message`, and checks with AssertionEngine, so that `Get Product Price    1    ==    249.99` works as Browser's `Get Text` does. Each library instance keeps one cart. Unit tests with pytest replace the HTTP layer; Robot tests in `atest/` run every keyword against the local shop.

*The agent runs `openspec list --json; echo "---"; openspec context --json`*

```
{
  "changes": [],
  "root": {
    "path": "<repo>",
    "source": "nearest"
  }
}
---
{
  "root": {
    "path": "<repo>",
    "source": "nearest",
... (5 more lines)
```

*The agent runs `ls -la openspec openspec/* ; cat openspec/config.yaml 2>/dev/null || cat openspec/config.yml 2>/dev/null; echo "---"; find . -path ./.venv -prune -o -path ./.git -prune -o -type f -print | head -100`*

```
-rw-r--r-- 1 user user 2282 Oct  6 19:58 openspec/config.yaml

openspec:
total 20
drwxr-xr-x 4 user user 4096 Oct  6 19:58 .
drwxr-xr-x 8 user user 4096 Oct  6 19:58 ..
drwxr-xr-x 3 user user 4096 Oct  6 19:58 changes
-rw-r--r-- 1 user user 2282 Oct  6 19:58 config.yaml
drwxr-xr-x 2 user user 4096 Oct  6 19:58 specs

openspec/changes:
total 12
... (95 more lines)
```

*The agent runs `cat src/demoshop_library/__init__.py; echo "--- pyproject"; cat pyproject.toml; echo "--- README"; cat README.md; echo "--- gitignore"; cat .gitignore; cat .python-version`*

```
def hello() -> str:
    return "Hello from demoshop-library!"
--- pyproject
[project]
name = "demoshop-library"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
authors = [
    { name = "Workshop rehearsal" }
]
requires-python = ">=3.12"
... (28 more lines)
```

*The agent reads `<repo>/references/browser-get-text.md`*

*The agent reads `<repo>/references/browser-get-element-count.md`*

*The agent reads `<repo>/references/assertion_engine.py`*

*The agent reads `<repo>/references/assertionengine-readme.md`*

*The agent runs `wc -c references/demoshop-openapi.json && python3 -c "
import json
d=json.load(open('references/demoshop-openapi.json'))
print(json.dumps({k:v for k,v in d.items() if k not in ('paths','components')}, indent=1))
for p,ops in d['paths'].items():
    for m,o in ops.items():
        if isinstance(o, dict):
            print(m.upper(), p, '-', o.get('summary') or o.get('operationId'))
"`*

```
Exit code 1
8497 references/demoshop-openapi.json
pyenv: version `3.12' is not installed (set by <repo>/.python-version)
```

**Agent:**

It's small enough to read directly.

*The agent reads `<repo>/references/demoshop-openapi.json`*

*The agent runs `cd /tmp && for p in /health /api/products/ /api/products/1 /api/products/999999; do echo "=== GET $p"; curl -s -m 5 -i "http://localhost:9090$p" | head -c 3000; echo; done`*

```
=== GET /health
HTTP/1.1 200 OK
date: Tue, 06 Oct 2026 18:00:15 GMT
server: uvicorn
content-length: 33
content-type: application/json
cache-control: private, no-store

{"status":"ok","version":"0.3.0"}
=== GET /api/products/
HTTP/1.1 200 OK
date: Tue, 06 Oct 2026 18:00:15 GMT
... (25 more lines)
```

*The agent runs `cd /tmp && echo "=== products tail"; curl -s -m 5 http://localhost:9090/api/products/ | tail -c 700; echo; echo "=== products keys/count (jq?)"; which jq; curl -s -m 5 http://localhost:9090/api/products/ | grep -o '"id":[0-9]*' | wc -l; echo "=== GET /api/cart/ no session"; curl -s -m 5 -i http://localhost:9090/api/cart/; echo; echo "=== GET /api/cart/ fresh session"; curl -s -m 5 -i -H "X-Session-ID: opsx-probe-readonly-1" http://localhost:9090/api/cart/; echo; echo "=== products with space header"; curl -s -m 5 -i -H "X-Workshop-Space: opsx-probe" http://localhost:9090/api/products/ | head -c 600; echo`*

```
=== products tail
"Health","inventory":60,"rating":4.7,"review_count":321},{"id":9,"name":"Summit Trail Shoes","sku":"SUM-SHO-009","price":149.0,"description":"Trail shoes with adaptive grip pattern, live weather alert
=== products keys/count (jq?)
/usr/bin/jq
12
=== GET /api/cart/ no session
HTTP/1.1 200 OK
date: Tue, 06 Oct 2026 18:00:20 GMT
server: uvicorn
content-length: 48
content-type: application/json
cache-control: private, no-store
... (21 more lines)
```

*The agent runs `cd /tmp && S="opsx-probe-$(date +%s%N)"; H="X-Session-ID: $S"; U=http://localhost:9090
echo "=== inventory before"; curl -s $U/api/products/1 | jq -c '.product.inventory'
echo "=== add 1 x2"; curl -s -i -m 5 -H "$H" -H 'Content-Type: application/json' -d '{"product_id":1,"quantity":2}' $U/api/cart/items; echo
echo "=== add 2 x1 (default qty)"; curl -s -m 5 -H "$H" -H 'Content-Type: application/json' -d '{"product_id":2}' $U/api/cart/items; echo
echo "=== add 1 x1 again (merge?)"; curl -s -m 5 -H "$H" -H 'Content-Type: application/json' -d '{"product_id":1,"quantity":1}' $U/api/cart/items; echo
echo "=== cart"; curl -s -m 5 -H "$H" $U/api/cart/ | jq .
echo "=== qty 21"; curl -s -i -m 5 -H "$H" -H 'Content-Type: application/json' -d '{"product_id":1,"quantity":21}' $U/api/cart/items | sed -n '1p;$p'; echo
echo "=== unknown product"; curl -s -i -m 5 -H "$H" -H 'Content-Type: application/json' -d '{"product_id":999999}' $U/api/cart/items | sed -n '1p;$p'; echo
echo "=== qty 0"; curl -s -i -m 5 -H "$H" -H 'Content-Type: application/json' -d '{"product_id":1,"quantity":0}' $U/api/cart/items | sed -n '1p;$p'; echo
echo "=== clear"; curl -s -i -m 5 -X DELETE -H "$H" $U/api/cart/ | sed -n '1p;$p'; echo
echo "=== cart after clear"; curl -s -m 5 -H "$H" $U/api/cart/; echo
echo "=== inventory after"; curl -s $U/api/products/1 | jq -c '.product.inventory'`*

```
=== inventory before
25
=== add 1 x2
HTTP/1.1 200 OK
date: Tue, 06 Oct 2026 18:00:38 GMT
server: uvicorn
content-length: 174
content-type: application/json
cache-control: private, no-store

{"session":"opsx-probe-1791309638941688706","items":[{"product_id":1,"name":"Aurora Neural Headphones","quantity":2,"unit_price":249.99,"total_price":499.98}],"total":499.98}
=== add 2 x1 (default qty)
... (41 more lines)
```

**Agent:**

Probe done. The cart is cleared and inventory is unchanged at 25. Next I'll check how Robot Framework 7.5 and PythonLibCore behave, using whatever copies are installed locally.

*The agent runs `ls -a; which uv; uv --version 2>/dev/null; ls ~/.cache/uv 2>/dev/null | head; find / -path /proc -prune -o \( -name typeconverters.py -path "*robot/running/arguments*" \) -print 2>/dev/null | head; find / -path /proc -prune -o \( -type d -name robotlibcore -o -type d -name assertionengine \) -print 2>/dev/null | head`*

```
Command did not complete within its 120s timeout and was moved to the background (ID: bot6irkjt). Output is being written to: <scratch>
```

*The agent reads `<scratch>`*

*The agent uses `ToolSearch` with `{"query": "select:TaskStop", "max_results": 1}`*

*The agent uses `TaskStop` with `{"task_id": "bot6irkjt"}`*

```
{"message":"Successfully stopped task: bot6irkjt (ls -a; which uv; uv --version 2>/dev/null; ls ~/.cache/uv 2>/dev/null | head; find / -path /proc -prune -o \\( -name typeconverters.py -path \"*robot/
```

*The agent runs `ls .venv/lib/*/site-packages/ 2>/dev/null; ls -la .venv/bin | head -30`*

```
_pytest
_virtualenv.pth
_virtualenv.py
assertionengine
certifi
certifi-2026.7.22.dist-info
charset_normalizer
charset_normalizer-3.5.2.dist-info
demoshop_library-0.1.0.dist-info
demoshop_library.pth
idna
idna-3.20.dist-info
... (43 more lines)
```

**Agent:**

The project virtualenv already has everything installed. I'll run a quick experiment outside the project to see how Robot converts `assertion_expected` under different type hints.

*The agent runs `cd <scratch> && mkdir -p rf-probe && cd rf-probe && cat > Probe.py <<'EOF'
from typing import Any
from assertionengine import AssertionOperator, verify_assertion, float_str_verify_assertion, int_str_verify_assertion
from robotlibcore import DynamicCore, keyword

class Probe(DynamicCore):
    ROBOT_LIBRARY_SCOPE = "TEST"
    def __init__(self, url: str, space: str | None = None):
        self.url, self.space = url, space
        DynamicCore.__init__(self, [])

    @keyword
    def union_float_str(self, assertion_expected: float | str | None = None):
        return f"{type(assertion_expected).__name__}:{assertion_expected!r}"

    @keyword
    def any_expected(self, assertion_expected: Any = None):
        return f"{type(assertion_expected).__name__}:{assertion_expected!r}"

    @keyword(tags=("Assertion", "Getter"))
    def get_price(self, assertion_operator: AssertionOperator | None = None, assertion_expected: Any = None, message: str | None = None) -> float:
        return float_str_verify_assertion(249.99, assertion_operator, assertion_expected, "Price", message)

    @keyword
    def get_price_plain(self, assertion_operator: AssertionOperator | None = None, assertion_expected: Any = None, message: str | None = None) -> float:
        return verify_assertion(249.99, assertion_operator, assertion_expected, "Price", message)

    @keyword
    def get_count(self, assertion_operator: AssertionOperator | None = None, assertion_expected: Any = None, message: str | None = None) -> int:
        return int_str_verify_assertion(3, assertion_operator, assertion_expected, "Count", message)
EOF
cat > probe.robot <<'EOF'
*** Settings ***
Library    Probe.py    http://x

*** Test Cases ***
Conversion
    ${a}=    Union Float Str    249.99
    Log To Console    \nunion float|str "249.99" -> ${a}
    ${b}=    Union Float Str    value > 1
    Log To Console    union float|str "value > 1" -> ${b}
    ${c}=    Any Expected    249.99
    Log To Console    Any "249.99" -> ${c}
Helper Float Equal
    ${p}=    Get Price    ==    249.99
    Log To Console    \nfloat_str == 249.99 ok -> ${p}
    Get Price    >    100
    Get Price    validate    value > 100
    ${t}=    Get Price    then    value * 2
    Log To Console    then -> ${t}
Plain Verify Float Equal
    Get Price Plain    ==    249.99
Helper Float Wrong
    Get Price    ==    10    message=Custom {value} vs {expected}
Helper Contains Rejected
    Get Price    contains    9
Count Helper
    Get Count    ==    3
    Get Count    >=    1
Count Helper Wrong
    Get Count    ==    4
EOF
../demoshop-library/.venv/bin/python -m robot --output NONE --report NONE --log NONE --console verbose probe.robot 2>&1 | tail -40`*

```
/bin/bash: line 125: ../demoshop-library/.venv/bin/python: No such file or directory
Shell cwd was reset to <repo>
```

*The agent runs `cd <scratch> && ../rh/demoshop-library/.venv/bin/python -m robot --output NONE --report NONE --log NONE --console verbose probe.robot 2>&1 | tail -40`*

```
==============================================================================
Probe                                                                         
==============================================================================
Conversion                                                            
union float|str "249.99" -> str:'249.99'
union float|str "value > 1" -> str:'value > 1'
Any "249.99" -> str:'249.99'
| PASS |
------------------------------------------------------------------------------
Helper Float Equal                                                    
float_str == 249.99 ok -> 249.99
then -> 499.98
... (24 more lines)
```

*The agent runs `cd /tmp && curl -s -m 5 http://localhost:9090/ | head -c 1500; echo; echo "=== scripts"; curl -s -m 5 http://localhost:9090/ | grep -oE '(src|href)="[^"]+\.(js|mjs)[^"]*"' | head`*

```
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Flowline Supply | Shop the Future</title>
  <link rel="stylesheet" href="/assets/styles.bcca56d0f15fa943.css" />
  <script src="/static/app.js?v=ee3c3f9e45a296f9" defer></script>
  

<script type="application/ld+json">
... (41 more lines)
```

*The agent runs `cd /tmp && curl -s -m 5 "http://localhost:9090/static/app.js" > <scratch> cd <scratch> && wc -c app.js && grep -n -iE 'quantity|cart-count|cartCount|badge|X-Session|X-Workshop|session' app.js | head -40`*

```
48578 app.js
10:  const SESSION_COOKIE = "session_id";
11:  const SESSION_COOKIE_DAYS = 30;
75:  let sessionId = ensureSessionId();
102:  function ensureSessionId() {
103:    let existing = getCookie(SESSION_COOKIE);
110:      setCookie(SESSION_COOKIE, existing, SESSION_COOKIE_DAYS);
176:  // Cart badge and add to cart
179:  function getCartBadge() {
183:  function updateCartBadge(state) {
184:    const counter = getCartBadge();
187:    const quantity = items.reduce(
... (12 more lines)
```

**Agent:**

The shop's cart badge adds up item quantities (`app.js:187`), so `Get Cart Item Count` will do the same. One more check: Robot's `TEST` scope with PythonLibCore, including what a suite setup sees.

*The agent runs `cd <scratch> && cat > ScopeProbe.py <<'EOF'
import uuid
from robotlibcore import DynamicCore, keyword

class Cart:
    def __init__(self, ctx):
        self.ctx = ctx
    @keyword
    def session_of_instance(self):
        return self.ctx.session_id

class ScopeProbe(DynamicCore):
    ROBOT_LIBRARY_SCOPE = "TEST"
    def __init__(self, url: str, space: str | None = None):
        self.session_id = uuid.uuid4().hex[:8]
        DynamicCore.__init__(self, [Cart(self)])
EOF
cat > scope.robot <<'EOF'
*** Settings ***
Library    ScopeProbe.py    http://x
Library    ScopeProbe.py    http://x    space=other    AS    Other
Suite Setup    Log Session    suite setup

*** Keywords ***
Log Session
    [Arguments]    ${where}
    ${s}=    ScopeProbe.Session Of Instance
    Log To Console    \n${where}: ${s}

*** Test Cases ***
T1
    [Setup]    Log Session    t1 setup
    Log Session    t1 body
    ${o}=    Other.Session Of Instance
    Log To Console    t1 Other: ${o}
T2
    Log Session    t2 body
EOF
../rh/demoshop-library/.venv/bin/python -m robot --output NONE --report NONE --log NONE scope.robot 2>&1 | grep -E ':|PASS|FAIL' | head -20`*

```
suite setup: fe7a98ce
t1 setup: f80bc06d
t1 body: f80bc06d
t1 Other: de57215f
| PASS |
t2 body: 6712febb
| PASS |
Scope                                                                 | PASS |
Output:  NONE
Shell cwd was reset to <repo>
```

*The agent runs `openspec new change "add-demoshop-library" && openspec status --change "add-demoshop-library" --json`*

```
- Creating change 'add-demoshop-library' with schema 'spec-driven'...
Created change 'add-demoshop-library' at openspec/changes/add-demoshop-library/
Schema: spec-driven
Next: openspec status --change add-demoshop-library
{
  "changeName": "add-demoshop-library",
  "schemaName": "spec-driven",
  "planningHome": {
    "kind": "repo",
    "root": "<repo>",
    "changesDir": "<repo>/openspec/changes",
    "defaultSchema": "spec-driven"
... (98 more lines)
```

*The agent runs `openspec instructions proposal --change "add-demoshop-library" --json | jq 'del(.context)'`*

```
{
  "changeName": "add-demoshop-library",
  "artifactId": "proposal",
  "schemaName": "spec-driven",
  "changeDir": "<repo>/openspec/changes/add-demoshop-library",
  "planningHome": {
    "kind": "repo",
    "root": "<repo>",
    "changesDir": "<repo>/openspec/changes",
    "defaultSchema": "spec-driven"
  },
  "outputPath": "proposal.md",
... (15 more lines)
```

*The agent runs `openspec list --specs; openspec instructions proposal --change "add-demoshop-library" --json | jq '{rules, ctx_len: (.context|length)}'`*

```
No specs found.
{
  "rules": null,
  "ctx_len": 1428
}
```

**Agent:**

No specs exist yet, so every capability is new. Writing the proposal.

*The agent writes `<repo>/openspec/changes/add-demoshop-library/proposal.md`*

```
File created successfully at: <repo>/openspec/changes/add-demoshop-library/
```

*The agent runs `openspec status --change "add-demoshop-library" --json | jq -c '.artifacts[] | {id,status}'; openspec instructions specs --change "add-demoshop-library" --json | jq 'del(.context)'`*

```
{"id":"proposal","status":"done"}
{"id":"specs","status":"ready"}
{"id":"design","status":"ready"}
{"id":"tasks","status":"blocked"}
{
  "changeName": "add-demoshop-library",
  "artifactId": "specs",
  "schemaName": "spec-driven",
  "changeDir": "<repo>/openspec/changes/add-demoshop-library",
  "planningHome": {
    "kind": "repo",
    "root": "<repo>",
... (25 more lines)
```

**Agent:**

Now the four capability specs.

*The agent writes `<repo>/openspec/changes/add-demoshop-library/specs/library-import/spec.md`*

```
File created successfully at: <repo>/openspec/changes/add-demoshop-library/
```

*The agent writes `<repo>/openspec/changes/add-demoshop-library/specs/getter-assertions/spec.md`*

```
File created successfully at: <repo>/openspec/changes/add-demoshop-library/
```

*The agent writes `<repo>/openspec/changes/add-demoshop-library/specs/product-keywords/spec.md`*

```
File created successfully at: <repo>/openspec/changes/add-demoshop-library/
```

*The agent writes `<repo>/openspec/changes/add-demoshop-library/specs/cart-keywords/spec.md`*

```
File created successfully at: <repo>/openspec/changes/add-demoshop-library/
```

**Agent:**

Before writing the design, I'll check the exact failure messages quoted in the specs against the real AssertionEngine and Robot behaviour, in the scratch directory.

*The agent runs `cd <scratch> && cat > Msg.py <<'EOF'
from typing import Any
from assertionengine import AssertionOperator, float_str_verify_assertion, int_str_verify_assertion
from robotlibcore import DynamicCore, keyword

class Msg(DynamicCore):
    def __init__(self):
        DynamicCore.__init__(self, [])
    @keyword
    def price_of(self, product_id: int, assertion_operator: AssertionOperator | None = None, assertion_expected: float | str = 0, message: str | None = None) -> float:
        return float_str_verify_assertion(249.99, assertion_operator, assertion_expected, f"Product {product_id} price", message)
    @keyword
    def total(self, assertion_operator: AssertionOperator | None = None, assertion_expected: float | str = 0, message: str | None = None) -> float:
        return float_str_verify_assertion(float(0), assertion_operator, assertion_expected, "Cart total", message)
    @keyword
    def items(self, assertion_operator: AssertionOperator | None = None, assertion_expected: int | str = 0, message: str | None = None) -> int:
        return int_str_verify_assertion(0, assertion_operator, assertion_expected, "Cart item count", message)
EOF
cat > msg.robot <<'EOF'
*** Settings ***
Library    Msg.py

*** Test Cases ***
Price Mismatch
    Price Of    1    ==    10
Count Mismatch
    Items    >    0
Custom
    Total    ==    5    message=Total was {value}, wanted {expected}
Validate Fails
    Price Of    1    validate    value < 100
Validate Passes And Alias And Named
    Price Of    1    validate    100 < value < 300
    Price Of    1    greater than    0
    Total    assertion_operator=>=    assertion_expected=0
    Price Of    1    should be    249.99
Bad Operator
    Items    ===    12
Bad Id
    Price Of    abc
Matches Rejected
    Price Of    1    matches    249
EOF
../rh/demoshop-library/.venv/bin/python -m robot --output NONE --report NONE --log NONE msg.robot 2>&1 | grep -vE '^-+$|^=+$'`*

```
Msg                                                                           
Price Mismatch                                                        | FAIL |
Product 1 price '249.99' (float) should be '10.0' (float)
Count Mismatch                                                        | FAIL |
Cart item count '0' (int) should be greater than '0' (int)
Custom                                                                | FAIL |
Total was 0.0, wanted 5.0
Validate Fails                                                        | FAIL |
Product 1 price '249.99' (float) should validate to true with 'value < 100' (str)
Validate Passes And Alias And Named                                   | PASS |
Bad Operator                                                          | FAIL |
ValueError: Argument 'assertion_operator' got value '===' that cannot be converted to AssertionOperator or None.
... (8 more lines)
```

**Agent:**

All the quoted messages match exactly. Next, the design.

*The agent runs `openspec instructions design --change "add-demoshop-library" --json | jq '{instruction, template, rules, dependencies}'`*

```
{
  "instruction": "Create the design document that explains HOW to implement the change.\n\nWhen to include design.md (create only if any apply):\n- Cross-cutting change (multiple services/modules) or 
  "template": "# Design\n\n## Context\n\n<!-- Current state and constraints that shape the approach. See proposal.md for motivation - don't restate it -->\n\n## Goals / Non-Goals\n\n**Goals:**\n<!-- W
  "rules": null,
  "dependencies": [
    {
      "id": "proposal",
      "done": true,
      "path": "proposal.md",
      "description": "Initial proposal document outlining the change"
    }
  ]
... (1 more lines)
```

*The agent reads `<repo>/openspec/changes/add-demoshop-library/proposal.md`*

*The agent writes `<repo>/openspec/changes/add-demoshop-library/design.md`*

```
File created successfully at: <repo>/openspec/changes/add-demoshop-library/
```

*The agent runs `openspec status --change "add-demoshop-library" --json | jq -c '.artifacts[] | {id,status}'; openspec instructions tasks --change "add-demoshop-library" --json | jq '{instruction, template, rules, dependencies}'`*

```
{"id":"proposal","status":"done"}
{"id":"specs","status":"done"}
{"id":"design","status":"done"}
{"id":"tasks","status":"ready"}
{
  "instruction": "Create the task list that breaks down the implementation work.\n\nBefore writing tasks, check design.md for Open Questions. If any of them\nwould change what gets built, resolve them
  "template": "# Tasks\n\n## 1. <!-- Task Group Name -->\n\n- [ ] 1.1 <!-- Task description -->\n- [ ] 1.2 <!-- Task description -->\n\n## 2. <!-- Task Group Name -->\n\n- [ ] 2.1 <!-- Task descriptio
  "rules": null,
  "dependencies": [
    {
      "id": "specs",
      "done": true,
... (11 more lines)
```

**Agent:**

Writing the tasks. I'll also add the README to the proposal's Impact section, since one task fills in the empty README and the placeholder package description.

*The agent writes `<repo>/openspec/changes/add-demoshop-library/tasks.md`*

```
File created successfully at: <repo>/openspec/changes/add-demoshop-library/
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/proposal.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/proposal.md has been 
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/design.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/design.md has been up
```

*The agent runs `openspec validate add-demoshop-library --strict; echo "---"; openspec status --change "add-demoshop-library"; echo "---"; find openspec/changes/add-demoshop-library -type f | sort; git status --short; rm -rf ../../rf-probe`*

```
Change 'add-demoshop-library' is valid
---
- Loading change status...
Change: add-demoshop-library
Schema: spec-driven
Change root: <repo>/openspec/changes/add-demoshop-library
Progress: 4/4 artifacts complete

[x] proposal
[x] specs
[x] design
[x] tasks
... (22 more lines)
```

**Agent:**

I created the change `add-demoshop-library` in `openspec/changes/add-demoshop-library/`. It passes `openspec validate --strict`. No project code was changed.

**What I created:**
- **`proposal.md`**: why the library is needed, the five keywords, and four new capabilities. It also lists what the change touches: shop endpoints, `tests/`, `atest/`, docs and README.
- **Specs**, one per capability, with every scenario written so it can be tested:
  - `library-import`: importing with `url` and `space`, the `X-Workshop-Space` header, one cart per instance, the library scope, error reporting and libdoc.
  - `getter-assertions`: the shared `assertion_operator` / `assertion_expected` / `message` contract and the exact failure messages.
  - `product-keywords`: `Get Product Count` and `Get Product Price`.
  - `cart-keywords`: `Add Product To Cart`, `Get Cart Item Count` and `Get Cart Total`.
- **`design.md`**: nine decisions, each with the alternatives considered, plus the response shapes I saw on the local shop. The OpenAPI file gives no response schemas.
- **`tasks.md`**: 20 tasks in 8 groups, each saying how to check it is done.

I made three decisions you should review, because each changes what tests will see:
1. **Each test gets a fresh library instance (Robot's `TEST` scope), so every test starts with an empty cart.** This slice has no `Clear Cart` keyword, so if instances lived for a whole suite, each cart test would depend on the ones before it. The catch is that a cart filled in a suite setup is not visible to the tests.
2. **`Get Cart Item Count` adds up quantities**, so two of product 1 plus one of product 2 counts as 3, not 2. That is what the shop's own cart badge shows (`/static/app.js`).
3. **The `Get` keywords check with AssertionEngine's numeric helpers** (`int_str_verify_assertion` and `float_str_verify_assertion`), not by calling `verify_assertion` directly. Robot 7.5 passes `"249.99"` in as text, and a direct call then fails with `'249.99' (float) should be '249.99' (str)`. The helpers convert the expected value first and then call `verify_assertion`, so `Get Product Price    1    ==    249.99` passes.

Things I found and checked:
- **Session header:** without an `X-Session-ID` header, every caller shares the shop's `workshop-demo` cart. So the library generates its own session ID per instance and sends it with every request.
- **Assertion messages:** I tried every assertion message quoted in the specs against the installed Robot Framework, AssertionEngine and PythonLibCore in a scratch directory, which I have since deleted.
- **Probe of the shop:** I added items to a throwaway cart to see the cart's shape and the 404 and 422 responses, then cleared it. Inventory was unchanged.

**Still open:** whether the generated `docs/DemoShopLibrary.html` gets committed or ignored. Task 6.2 settles it.

The artifacts are ready for review. When you are ready, run `/opsx:apply`.

## Step 6 - Review the proposal

*The rehearsal's review: the questions of step 6, put to the agent, which changes its artifacts where an answer is no.*

**Prompt:**

> Review the change you just proposed against these questions, and change its artifacts wherever an answer is no. Then answer each question in one line.
>
> Is every keyword named and argued like the examples: `Get <thing>`, then the three assertion arguments?
> Does every check go through AssertionEngine, with no assertion code of the library's own?
> Do the endpoints, parameters and headers match `references/demoshop-openapi.json`?
> Do the Robot tests in `atest/` use only the library's keywords, against the local shop?

**Agent:**

I'll re-read the artifacts from disk and check them against the four questions.

*The agent runs `cd <repo>/openspec/changes/add-demoshop-library && grep -nE 'X-Session-ID|X-Workshop-Space|Accept|Evaluate|Run Keyword|Should |localhost:1|AS +|every request|stay as it was|unchanged|from before' proposal.md design.md tasks.md specs/*/spec.md`*

```
proposal.md:14:  optional `space`. When `space` is given, every request carries it in the `X-Workshop-Space` header.
proposal.md:16:  that send no `X-Session-ID`, so the library generates a session id per instance and sends it with every request.
design.md:21:- A request without `X-Session-ID` uses the shared cart `"session": "workshop-demo"`.
design.md:74:`Accept: application/json` and `X-Session-ID: <session_id>`, and `X-Workshop-Space: <space>` only when `space` is not
design.md:151:requests: path, `X-Session-ID`, `X-Workshop-Space` and body.
design.md:163:### 8. Acceptance tests: one resource and one suite per capability
design.md:176:single space. Expected failures use `Run Keyword And Expect Error`. The check that the default cart is left untouched
design.md:178:`Evaluate    requests.get(...).json()    modules=requests`, before and after adding a product. The suites run with
tasks.md:17:  `session_id`, and creates a `requests.Session` with the default headers `Accept`, `X-Session-ID` and, only when
tasks.md:18:  `space` is set, `X-Workshop-Space`. It also provides `request(method, path, action, json=None)` with a 10-second
tasks.md:20:  `/`; the space header is present only when `space` is given; two clients have different session ids; every request
tasks.md:21:  carries `X-Session-ID`; a POST body is sent as JSON.
... (22 more lines)
```

*The agent writes `<repo>/openspec/changes/add-demoshop-library/specs/library-import/spec.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/specs/library-import/
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/specs/cart-keywords/spec.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/specs/cart-keywords/s
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/specs/cart-keywords/spec.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/specs/cart-keywords/s
```

**Agent:**

Next, the proposal.

*The agent edits `<repo>/openspec/changes/add-demoshop-library/proposal.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/proposal.md has been 
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/proposal.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/proposal.md has been 
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/proposal.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/proposal.md has been 
```

**Agent:**

Now the design. I'll re-read it before editing the sections that change.

*The agent reads `<repo>/openspec/changes/add-demoshop-library/design.md`*

*The agent reads `<repo>/openspec/changes/add-demoshop-library/design.md`*

**Agent:**

Before writing the acceptance-test check into the design, I'll confirm that Robot 7.5's result model exposes which library a keyword came from.

*The agent runs `<repo>/.venv/bin/python -c "
from robot.result import Keyword
k = Keyword(name='Get Cart Total', owner='ShopA')
print(k.owner, '|', k.full_name)
"`*

```
ShopA | ShopA.Get Cart Total
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/design.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/design.md has been up
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/design.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/design.md has been up
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/design.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/design.md has been up
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/design.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/design.md has been up
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/design.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/design.md has been up
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/design.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/design.md has been up
```

**Agent:**

Now the tasks.

*The agent reads `<repo>/openspec/changes/add-demoshop-library/tasks.md`*

*The agent edits `<repo>/openspec/changes/add-demoshop-library/tasks.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/tasks.md has been upd
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/tasks.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/tasks.md has been upd
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/tasks.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/tasks.md has been upd
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/tasks.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/tasks.md has been upd
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/tasks.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/tasks.md has been upd
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/tasks.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/tasks.md has been upd
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/tasks.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/tasks.md has been upd
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/design.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/design.md has been up
```

*The agent runs `cd <repo> && openspec validate add-demoshop-library --strict && openspec status --change add-demoshop-library && echo "--- leftovers:" && grep -nE 'Accept|Run Keyword And Expect|Evaluate +requests|localhost:1|OtherShop|stay as it was|every request\b' openspec/changes/add-demoshop-library/{proposal.md,design.md,tasks.md} openspec/changes/add-demoshop-library/specs/*/spec.md`*

```
Change 'add-demoshop-library' is valid
- Loading change status...
Change: add-demoshop-library
Schema: spec-driven
Change root: <repo>/openspec/changes/add-demoshop-library
Progress: 4/4 artifacts complete

[x] proposal
[x] specs
[x] design
[x] tasks

... (17 more lines)
```

**Agent:**

1. **Keywords like the examples?** Yes, no change needed: the four `Get` keywords take the keyword's own argument (`product_id` for `Get Product Price`), then `assertion_operator`, `assertion_expected` and `message`, typed like Browser's `Get Element Count`; only `Add Product To Cart`, the name you asked for, is not a getter, so it has no assertion arguments.
2. **Every check through AssertionEngine?** Yes, no change needed: every check calls AssertionEngine's `int_str_verify_assertion` or `float_str_verify_assertion`, which call `verify_assertion`, and the library itself only translates shop errors.
3. **Endpoints, parameters and headers match the OpenAPI document?** No, now fixed: `X-Session-ID` goes only on cart requests, where the document declares it, and the undeclared `Accept` header is gone; `X-Workshop-Space` is still undeclared but stays because `AGENTS.md` requires it, which the design now says.
4. **`atest/` uses only the library's keywords, against the local shop?** No, now fixed: I removed `Evaluate` with `requests`, `Run Keyword And Expect Error`, the `localhost:1` test and the ambiguous two-instance import (now `ShopA`/`ShopB`), so the suites call only library keywords against `${SHOP_URL}`, failure cases move to the unit tests, and new task 7.6 checks this in `output.xml`.

I also dropped "the cart stays as it was" from the cart spec, because that is the shop's behaviour and no test could check it. The change still passes `openspec validate --strict`.

## Step 7 - Apply it

*The rehearsal tool stopped the first `/opsx:apply` session after 13 of the change's 22 tasks, at its own time limit; that session is not recorded. A new `/opsx:apply` continued from the ticked tasks, as you would after an interruption.*

**Prompt:**

> /opsx:apply

*The agent runs `openspec list --json`*

```
{
  "changes": [
    {
      "name": "add-demoshop-library",
      "completedTasks": 13,
      "totalTasks": 22,
      "lastModified": "2026-10-06T18:26:40.002Z",
      "status": "in-progress"
    }
  ],
  "root": {
    "path": "<repo>",
... (3 more lines)
```

**Agent:**

Using change: **add-demoshop-library** (override with `/opsx:apply <other>`).

*The agent runs `openspec status --change "add-demoshop-library" --json && echo ---- && openspec instructions apply --change "add-demoshop-library" --json`*

```
{
  "changeName": "add-demoshop-library",
  "schemaName": "spec-driven",
  "planningHome": {
    "kind": "repo",
    "root": "<repo>",
    "changesDir": "<repo>/openspec/changes",
    "defaultSchema": "spec-driven"
  },
  "changeRoot": "<repo>/openspec/changes/add-demoshop-library",
  "artifactPaths": {
    "proposal": {
... (242 more lines)
```

*The agent reads `<repo>/openspec/changes/add-demoshop-library/tasks.md`*

*The agent reads `<repo>/openspec/changes/add-demoshop-library/design.md`*

*The agent reads `<repo>/openspec/changes/add-demoshop-library/proposal.md`*

*The agent reads `<repo>/openspec/changes/add-demoshop-library/specs/cart-keywords/spec.md`*

*The agent reads `<repo>/openspec/changes/add-demoshop-library/specs/getter-assertions/spec.md`*

*The agent reads `<repo>/openspec/changes/add-demoshop-library/specs/library-import/spec.md`*

*The agent reads `<repo>/openspec/changes/add-demoshop-library/specs/product-keywords/spec.md`*

**Agent:**

Now the existing code and references.

*The agent runs `git ls-files --others --exclude-standard | grep -v '^openspec/' ; echo ---; ls -la atest docs 2>&1; cat .gitignore; echo ---; cat pyproject.toml; echo ---; cat README.md`*

```
.claude/commands/opsx/apply.md
.claude/commands/opsx/archive.md
.claude/commands/opsx/explore.md
.claude/commands/opsx/propose.md
.claude/commands/opsx/sync.md
.claude/commands/opsx/update.md
.claude/skills/openspec-apply-change/SKILL.md
.claude/skills/openspec-archive-change/SKILL.md
.claude/skills/openspec-explore/SKILL.md
.claude/skills/openspec-propose/SKILL.md
.claude/skills/openspec-sync-specs/SKILL.md
.claude/skills/openspec-update-change/SKILL.md
... (90 more lines)
```

*The agent reads `<repo>/src/demoshop_library/library.py`*

*The agent reads `<repo>/src/demoshop_library/products.py`*

*The agent reads `<repo>/src/demoshop_library/cart.py`*

*The agent reads `<repo>/references/browser-get-text.md`*

*The agent reads `<repo>/references/browser-get-element-count.md`*

**Agent:**

Keyword docs and `atest/` files already exist even though their tasks are unchecked. Let me look at them and the remaining source.

*The agent runs `for f in atest/resources/demoshop.resource atest/*.robot src/demoshop_library/__init__.py src/demoshop_library/assertions.py src/demoshop_library/client.py; do echo "=== $f"; cat -A "$f" | grep -c '\^M' ; cat "$f"; done`*

```
=== atest/resources/demoshop.resource
0
*** Settings ***
Documentation       Variables shared by the acceptance suites: where the shop runs and its seed data.
...                 Override any of them with ``--variable``, for example ``--variable WORKSHOP_SPACE:team-7``.


*** Variables ***
${SHOP_URL}             http://localhost:9090
# Not ${SPACE}, which is Robot Framework's built-in variable holding a single space.
${WORKSHOP_SPACE}       ${NONE}

... (270 more lines)
```

*The agent runs `uv run pytest -q 2>&1 | tail -5; echo ---; curl -s -m 5 -o /dev/null -w '%{http_code}\n' http://localhost:9090/api/products/ ; curl -s -m 5 http://localhost:9090/health; echo`*

```
........................................................................ [ 94%]
....                                                                     [100%]
76 passed in 0.17s
---
200
{"status":"ok","version":"0.3.0"}
```

*The agent runs `uv run python -m robot.libdoc demoshop_library.DemoShopLibrary docs/DemoShopLibrary.html && uv run python -m robot.libdoc --specdocformat HTML demoshop_library.DemoShopLibrary <scratch> >/dev/null && uv run python - <<'EOF'
import json, re
d = json.load(open("<scratch>"))
print("intro has Assertions anchor:", 'id="Assertions"' in d["doc"])
print("intro anchors:", re.findall(r'<h2 id="([^"]+)"', d["doc"]))
print("init doc names url/space:", all(f"<code>{a}</code>" in d["inits"][0]["doc"] for a in ("url", "space")))
for kw in d["keywords"]:
    doc = kw["doc"]
    links = set(re.findall(r'href="#([^"]+)"', doc))
    args = [a["name"] for a in kw["args"]]
    print(f'- {kw["name"]}: args={args} tags={kw["tags"]} links={sorted(links)} '
          f'table={"=Arguments=" in doc or "<th>Arguments</th>" in doc} example={"Example:" in doc} '
          f'optional={"Optionally asserts" in doc}')
    for l in links:
        assert l in ("Assertions", "Carts and library scope") or l.replace("%20"," ") in [k["name"] for k in d["keywords"]], l
EOF
grep -o 'id="Carts and library scope"\|id="Assertions"' /dev/null; ls -la docs/`*

```
Library 'demoshop_library.DemoShopLibrary' expected 1 to 2 arguments, got 0.

Try --help for usage information.
total 236
drwxr-xr-x  2 user user   4096 Oct  6 20:26 .
drwxr-xr-x 13 user user   4096 Oct  6 20:27 ..
-rw-r--r--  1 user user 230311 Oct  6 20:26 DemoShopLibrary.html
```

**Agent:**

libdoc fails with the exact command that task 6.1, the `library-import` spec and `AGENTS.md` all prescribe. I'll check how Robot 7.5's libdoc builds a library before deciding what to do.

*The agent runs `RF=.venv/lib/python3.12/site-packages/robot; grep -n "from_name\|args" $RF/libdocpkg/robotbuilder.py | head -20; echo ---; grep -n "def get_keyword_names\|instance" $RF/running/testlibraries.py | grep -n "Dynamic\|get_keyword_names\|def instance" | head; echo ---; uv run python -m robot.libdoc --help | grep -n -A3 "::"`*

```
38:        name, args = self._split_library_name_and_args(library)
39:        lib = TestLibrary.from_name(name, args=args)
57:    def _split_library_name_and_args(self, library):
58:        args = library.split(self._argument_separator)
59:        name = args.pop(0)
60:        return self._normalize_library_path(name), args
72:        if lib.init.args:
82:            for name, type_info in self._yield_names_and_infos(kw.args):
92:    def _yield_names_and_infos(self, args: ArgumentSpec):
93:        for arg in args:
97:        if args.return_type:
98:            for type_info in self._yield_infos(args.return_type):
... (28 more lines)
```

*The agent runs `uv run python -m robot.libdoc demoshop_library.DemoShopLibrary::http://localhost:9090 docs/DemoShopLibrary.html && uv run python -m robot.libdoc --specdocformat HTML demoshop_library.DemoShopLibrary::http://localhost:9090 <scratch> >/dev/null && uv run python - <<'EOF'
import json, re
d = json.load(open("<scratch>"))
anchors = re.findall(r'<h2 id="([^"]+)"', d["doc"])
print("intro sections:", anchors)
print("init args:", [a["name"] for a in d["inits"][0]["args"]])
names = [k["name"] for k in d["keywords"]]
for kw in d["keywords"]:
    doc = kw["doc"]
    links = sorted(set(re.findall(r'href="#([^"]+)"', doc)))
    bad = [l for l in links if l not in anchors and l.replace("%20", " ") not in names]
    print(f'- {kw["name"]}({", ".join(a["repr"] for a in kw["args"])}) tags={kw["tags"]}')
    print(f'    links={links} broken={bad} optional_asserts={"Optionally asserts" in doc} example={"Example:" in doc}')
    if kw["name"].startswith("Get"):
        row = re.search(r'<code>assertion_operator</code></td>\s*<td>(.*?)</td>', doc).group(1)
        print("    operator row:", re.sub(r"<[^>]+>", "", row), "| links Assertions:", 'href="#Assertions"' in row)
EOF`*

```
<repo>/docs/DemoShopLibrary.html
intro sections: ['Shop and workshop space', 'Carts and library scope', 'Assertions', 'Shop errors']
init args: ['url', 'space']
- Add Product To Cart(product_id: int, quantity: int = 1) tags=['Cart', 'Setter']
    links=['Add%20Product%20To%20Cart', 'Carts%20and%20library%20scope', 'Get%20Cart%20Item%20Count'] broken=['Carts%20and%20library%20scope'] optional_asserts=False example=True
- Get Cart Item Count(assertion_operator: AssertionOperator | None = None, assertion_expected: int | str = 0, message: str | None = None) tags=['Assertion', 'Cart', 'Getter']
    links=['Add%20Product%20To%20Cart', 'Assertions', 'Get%20Cart%20Item%20Count'] broken=[] optional_asserts=True example=True
    operator row: See Assertions for further details. Defaults to None. | links Assertions: True
- Get Cart Total(assertion_operator: AssertionOperator | None = None, assertion_expected: float | str = 0, message: str | None = None) tags=['Assertion', 'Cart', 'Getter']
    links=['Add%20Product%20To%20Cart', 'Assertions', 'Get%20Cart%20Total'] broken=[] optional_asserts=True example=True
    operator row: See Assertions for further details. Defaults to None. | links Assertions: True
- Get Product Count(assertion_operator: AssertionOperator | None = None, assertion_expected: int | str = 0, message: str | None = None) tags=['Assertion', 'Getter', 'Products']
... (5 more lines)
```

*The agent runs `uv run robot --dryrun --outputdir <scratch> atest 2>&1 | tail -25`*

```
------------------------------------------------------------------------------
Atest.Library Import :: Importing the library: URL, workshop space... | PASS |
6 tests, 6 passed, 0 failed
==============================================================================
Atest.Product Keywords :: Product keywords against the shop's seed catalogue. 
==============================================================================
Count Of The Seed Catalogue                                           | PASS |
------------------------------------------------------------------------------
Count With Assertion                                                  | PASS |
------------------------------------------------------------------------------
Price Of A Product                                                    | PASS |
------------------------------------------------------------------------------
... (13 more lines)
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/tasks.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/tasks.md has been upd
```

**Agent:**

✓ Task 7.1 complete (dry run: 26 tests, 0 failures).

Working on tasks 7.2–7.5: each suite exists and covers the scenarios its task lists. Next I'll run each one against the shop.

*The agent runs `for s in product_keywords cart_keywords getter_assertions library_import; do echo "##### $s"; uv run robot --outputdir results/$s --console dotted atest/$s.robot 2>&1 | grep -E "tests?, |FAIL|Error|\[ ERROR|\[ WARN"; echo "rc=$?"; done`*

```
##### product_keywords
5 tests, 5 passed, 0 failed
rc=0
##### cart_keywords
7 tests, 7 passed, 0 failed
rc=0
##### getter_assertions
8 tests, 8 passed, 0 failed
rc=0
##### library_import
6 tests, 6 passed, 0 failed
rc=0
```

**Agent:**

All four suites pass against the shop: 5 + 7 + 8 + 6 tests, with no errors or warnings.

*The agent runs `sed -i -E 's/^- \[ \] (7\.[2-5] )/- [x] \1/' openspec/changes/add-demoshop-library/tasks.md && grep -n '^- \[' openspec/changes/add-demoshop-library/tasks.md | sed -n '13,22p'`*

```
95:- [ ] 6.1 Write the documentation of the five keywords in the shape of `references/browser-get-text.md` and
101:- [x] 6.2 Settle the open question about generated docs: commit `docs/DemoShopLibrary.html`, or add `docs/` to
114:- [x] 7.1 Create `atest/resources/demoshop.resource` holding variables only: `${SHOP_URL}` (default
118:- [x] 7.2 Write `atest/product_keywords.robot`. It imports the library with `url=${SHOP_URL}` and
122:- [x] 7.3 Write `atest/cart_keywords.robot`. It covers the passing scenarios of `specs/cart-keywords/spec.md`:
131:- [x] 7.4 Write `atest/getter_assertions.robot`. It covers the passing scenarios of `specs/getter-assertions/spec.md`:
138:- [x] 7.5 Write `atest/library_import.robot`. It imports the library twice, as `ShopA` with `url=${SHOP_URL}` and as
148:- [ ] 7.6 Check that the acceptance tests use only the library's keywords. Verify by reading `results/output.xml`
154:- [ ] 8.1 Add a README usage section with the import example, the five keywords, and the commands for unit tests,
156:- [ ] 8.2 Run the whole suite. Verify that `uv run pytest` and `uv run robot --outputdir results atest` both pass with
```

**Agent:**

✓ Tasks 7.2–7.5 complete.

Working on task 7.6: full run, then I'll check every executed keyword's `owner` in `results/output.xml`.

*The agent runs `rm -rf results/product_keywords results/cart_keywords results/getter_assertions results/library_import && uv run robot --outputdir results --console quiet atest; echo "robot rc=$?"; uv run python - <<'EOF'
from collections import Counter
from robot.api import ExecutionResult, ResultVisitor

ALLOWED = {"demoshop_library.DemoShopLibrary", "ShopA", "ShopB"}

class Owners(ResultVisitor):
    def __init__(self):
        self.owners, self.bad, self.other = Counter(), [], Counter()
    def start_keyword(self, kw):
        self.owners[kw.owner] += 1
        if kw.owner not in ALLOWED:
            self.bad.append((kw.parent.name if kw.parent else "?", kw.full_name))
    def start_body_item(self, item):
        if item.type not in ("KEYWORD", "SETUP", "TEARDOWN"):
            self.other[item.type] += 1
        super().start_body_item(item)

result = ExecutionResult("results/output.xml")
v = Owners()
result.visit(v)
s = result.statistics.total
print(f"tests: {s.total} passed={s.passed} failed={s.failed}")
print("owners:", dict(v.owners))
print("non-keyword body items:", dict(v.other))
print("violations:", v.bad)
assert not v.bad and s.failed == 0
print("7.6 check: OK")
EOF`*

```
robot rc=0
tests: 26 passed=26 failed=0
owners: {'demoshop_library.DemoShopLibrary': 54, 'ShopA': 9, 'ShopB': 5}
non-keyword body items: {'MESSAGE': 6}
violations: []
7.6 check: OK
```

**Agent:**

All 26 tests pass. The 68 executed keywords are owned only by `demoshop_library.DemoShopLibrary` (54), `ShopA` (9) and `ShopB` (5). The 6 `MESSAGE` items are log lines, not keywords.

*The agent edits `<repo>/openspec/changes/add-demoshop-library/tasks.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/tasks.md has been upd
```

**Agent:**

✓ Task 7.6 complete.

Before pausing, I'll run the one 8.2 check I haven't run yet, the wheel contents. I'm building into a temp directory so nothing is left in the repo.

*The agent runs `uv build --out-dir <scratch> 2>&1 | tail -2 && uv run python -c "
import zipfile, glob
names = zipfile.ZipFile(glob.glob('<scratch>')[0]).namelist()
print('\n'.join(names))
print('tests/atest in wheel:', [n for n in names if n.startswith(('tests/', 'atest/'))])
"`*

```
Successfully built <scratch>
Successfully built <scratch>
demoshop_library/
demoshop_library/__init__.py
demoshop_library/assertions.py
demoshop_library/cart.py
demoshop_library/client.py
demoshop_library/library.py
demoshop_library/products.py
demoshop_library/py.typed
demoshop_library-0.1.0.dist-info/
demoshop_library-0.1.0.dist-info/WHEEL
... (3 more lines)
```

**Agent:**

## Implementation paused

**Change:** add-demoshop-library (spec-driven)
**Progress:** 19 of 22 tasks done

### Done this session
Most of the remaining work was already on disk but had never been checked. I ran each task's check against the shop at `localhost:9090` (version 0.3.0) and only marked tasks whose check passed:
- [x] 7.1 `demoshop.resource`: the dry run has 26 tests, all passing.
- [x] 7.2–7.5 Product (5 tests), cart (7), assertion (8) and import (6) suites: all pass against the shop.
- [x] 7.6 Full run: 26 of 26 pass. Every executed keyword belongs to `demoshop_library.DemoShopLibrary`, `ShopA` or `ShopB`.

### Problem: libdoc fails with the command the plan prescribes
Task 6.1, the `library-import` spec ("Generate documentation") and `AGENTS.md` all use:

```
uv run python -m robot.libdoc demoshop_library.DemoShopLibrary docs/DemoShopLibrary.html
```

It fails with `Library 'demoshop_library.DemoShopLibrary' expected 1 to 2 arguments, got 0.` libdoc has to create the library to list its keywords, and the spec makes `url` a required argument. The plan contradicts itself here; this is not a coding mistake.

The documentation itself is finished. With the URL passed in, libdoc succeeds, lists all five keywords, and every `Get` keyword's `assertion_operator` row links to `Assertions`. So 6.1 stays unchecked only because its check fails as written.

### Options
1. **Pass the URL to libdoc (recommended):** `uv run python -m robot.libdoc demoshop_library.DemoShopLibrary::http://localhost:9090 docs/DemoShopLibrary.html`. This works now with no code change. Importing never contacts the shop, so any URL would work. The command needs updating in `AGENTS.md`, the spec scenario and task 6.1 (`/opsx:update` covers the plan files).
2. **Make `url` optional**, defaulting to `http://localhost:9090`. The plain command would then work, but this changes the spec's "required `url`" rule, the design and the unit tests.

### Still to do once you decide
- **6.1:** mark it done once its check matches your choice.
- **8.1:** write the README usage section. It includes the libdoc command, so I held off.
- **8.2:** I ran its checks now and they all pass: 76 unit tests, 26 acceptance tests, the 7.6 check, and a wheel with the required modules and `py.typed` but no `tests/` or `atest/`. I'll mark it done only after a final run, because option 2 changes code.

Which option do you want? Then run `/opsx:apply` again to finish.

## Step 7 - Apply it, continued

*The apply paused on a defect of the lab's first text: its libdoc command did not pass the library's `url`. The lab now gives the corrected command. The rehearsal told the agent, as you would, and applied the rest.*

**Prompt:**

> Your apply paused on the libdoc command: libdoc imports the library, so it needs the url the library takes. Use this command in AGENTS.md and in the change's tasks instead: `uv run python -m robot.libdoc "demoshop_library.DemoShopLibrary::url=http://localhost:9090" docs/DemoShopLibrary.html`. Change nothing else.

*The agent searches for `robot\.libdoc`*

```
AGENTS.md:11:  `uv run python -m robot.libdoc demoshop_library.DemoShopLibrary docs/DemoShopLibrary.html`.
openspec/config.yaml:13:  - Keyword documentation: `uv run python -m robot.libdoc demoshop_library.DemoShopLibrary docs/DemoShopLibrary.html`.
openspec/changes/add-demoshop-library/tasks.md:99:  `uv run python -m robot.libdoc demoshop_library.DemoShopLibrary docs/DemoShopLibrary.html` succeeds, and that the
openspec/changes/add-demoshop-library/specs/library-import/spec.md:108:- **WHEN** `uv run python -m robot.libdoc demoshop_library.DemoShopLibrary docs/DemoShopLibrary.html` is run
```

*The agent reads `<repo>/AGENTS.md`*

*The agent reads `<repo>/openspec/changes/add-demoshop-library/tasks.md`*

*The agent edits `<repo>/AGENTS.md`*

```
The file <repo>/AGENTS.md has been updated successfully.
```

*The agent edits `<repo>/openspec/changes/add-demoshop-library/tasks.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/tasks.md has been upd
```

**Agent:**

I replaced the libdoc command with yours in two places and changed nothing else:

- `AGENTS.md:11`
- `openspec/changes/add-demoshop-library/tasks.md:99` (task 6.1)

I didn't run the command, because that would write `docs/DemoShopLibrary.html`.

The old command, without the url, is still in two places I left alone:

- `openspec/config.yaml:13`
- `openspec/changes/add-demoshop-library/specs/library-import/spec.md:108`, inside a scenario's **WHEN** step

The spec scenario will still disagree with task 6.1 until it's updated. Do you want me to change these two as well?

**Prompt:**

> /opsx:apply

*The agent runs `openspec list --json`*

```
{
  "changes": [
    {
      "name": "add-demoshop-library",
      "completedTasks": 19,
      "totalTasks": 22,
      "lastModified": "2026-10-06T20:21:23.598Z",
      "status": "in-progress"
    }
  ],
  "root": {
    "path": "<repo>",
... (3 more lines)
```

**Agent:**

Using change: **add-demoshop-library** (override with `/opsx:apply <other>`).

*The agent runs `openspec status --change "add-demoshop-library" --json && openspec instructions apply --change "add-demoshop-library" --json`*

```
{
  "changeName": "add-demoshop-library",
  "schemaName": "spec-driven",
  "planningHome": {
    "kind": "repo",
    "root": "<repo>",
    "changesDir": "<repo>/openspec/changes",
    "defaultSchema": "spec-driven"
  },
  "changeRoot": "<repo>/openspec/changes/add-demoshop-library",
  "artifactPaths": {
    "proposal": {
... (241 more lines)
```

*The agent reads `<repo>/openspec/changes/add-demoshop-library/tasks.md`*

*The agent reads `<repo>/openspec/changes/add-demoshop-library/proposal.md`*

*The agent reads `<repo>/openspec/changes/add-demoshop-library/design.md`*

*The agent reads `<repo>/openspec/changes/add-demoshop-library/specs/cart-keywords/spec.md`*

*The agent reads `<repo>/openspec/changes/add-demoshop-library/specs/getter-assertions/spec.md`*

*The agent reads `<repo>/openspec/changes/add-demoshop-library/specs/library-import/spec.md`*

*The agent reads `<repo>/openspec/changes/add-demoshop-library/specs/product-keywords/spec.md`*

*The agent runs `git status --short && ls -la && find src tests atest references docs -type f 2>/dev/null | grep -v __pycache__ && cat .gitignore pyproject.toml README.md`*

```
?? .claude/
?? .gitignore
?? .python-version
?? AGENTS.md
?? README.md
?? atest/
?? openspec/
?? pyproject.toml
?? references/
?? results-assert/
?? src/
?? tests/
... (90 more lines)
```

*The agent reads `<repo>/src/demoshop_library/library.py`*

*The agent reads `<repo>/src/demoshop_library/products.py`*

*The agent reads `<repo>/src/demoshop_library/cart.py`*

*The agent reads `<repo>/src/demoshop_library/assertions.py`*

*The agent reads `<repo>/src/demoshop_library/__init__.py`*

*The agent reads `<repo>/src/demoshop_library/client.py`*

*The agent reads `<repo>/references/browser-get-text.md`*

*The agent reads `<repo>/references/browser-get-element-count.md`*

*The agent runs `curl -s -m 5 http://localhost:9090/api/products/ | head -c 300; echo; echo "---"; uv run pytest -q 2>&1 | tail -5; ls results results-assert dist docs; git log --oneline 2>&1 | head`*

```
{"items":[{"id":5,"name":"Atlas Standing Desk","sku":"ATL-DSK-005","price":799.0,"description":"Programmable standing desk with posture coaching, ambient wellness reminders, and built-in cable managem
---
........................................................................ [ 94%]
....                                                                     [100%]
76 passed in 0.16s
dist:
demoshop_library-0.1.0-py3-none-any.whl
demoshop_library-0.1.0.tar.gz

docs:
DemoShopLibrary.html

... (10 more lines)
```

*The agent runs `uv run python -m robot.libdoc "demoshop_library.DemoShopLibrary::url=http://localhost:9090" docs/DemoShopLibrary.html; echo "exit=$?"; echo "--- without url arg:"; uv run python -m robot.libdoc demoshop_library.DemoShopLibrary /tmp/libdoc-nourl.html; echo "exit=$?"`*

```
<repo>/docs/DemoShopLibrary.html
exit=0
--- without url arg:
Library 'demoshop_library.DemoShopLibrary' expected 1 to 2 arguments, got 0.

Try --help for usage information.
exit=252
```

*The agent runs `uv run python - <<'EOF'
import json, re
html = open("docs/DemoShopLibrary.html", encoding="utf-8").read()
m = re.search(r"libdoc = (\{.*?\});\s*</script>", html, re.S)
data = json.loads(m.group(1))
intro = data["doc"]
anchors = set(re.findall(r'<h2 id="([^"]+)"', intro)) | {"Importing", "Keywords"}
print("intro sections:", sorted(re.findall(r'<h2 id="([^"]+)"', intro)))
print("keywords:", [k["name"] for k in data["keywords"]])
for kw in [data["inits"][0] if data["inits"] else None] + data["keywords"]:
    if kw is None: continue
    links = re.findall(r'<a href="#([^"]+)" class="name">', kw["doc"])
    broken = [l for l in links if l not in anchors and l not in {k["name"] for k in data["keywords"]}]
    print(f'{kw["name"]!r}: args={[a["repr"] for a in kw["args"]]} tags={kw.get("tags")} links={sorted(set(links))} broken={broken}')
    first = re.sub("<.*?>", "", kw["doc"]).strip().splitlines()[0]
    print("   summary:", first)
    print("   has Example:", "Example" in kw["doc"], "| optional-assert para:", "Optionally asserts" in kw["doc"])
intro_links = re.findall(r'<a href="#([^"]+)" class="name">', intro)
print("intro links:", sorted(set(intro_links)), "broken:", [l for l in intro_links if l not in anchors and l not in {k["name"] for k in data["keywords"]}])
EOF`*

```
Exit code 1
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
AttributeError: 'NoneType' object has no attribute 'group'
```

*The agent runs `grep -o 'libdoc[^=]\{0,20\}=' docs/DemoShopLibrary.html | sort | uniq -c | head; grep -o '<script type="text/javascript">[^<]\{0,80\}' docs/DemoShopLibrary.html | head -5`*

```
      1 libdoc =
      1 libdoc"),rA=
      1 libdoc-logo" aria-hidden=
      1 libdoc-overview"><div id=
      1 libdoc-title" href=
      1 libdoc-title"),t=
      1 libdoc.keywords.map(e=
      1 libdoc.keywords].forEach(e=
      3 libdoc.selectedTag=
      1 libdoc;const rL=
<script type="text/javascript">
```

*The agent runs `uv run python - <<'EOF'
import json, re
html = open("docs/DemoShopLibrary.html", encoding="utf-8").read()
i = html.index("libdoc = ") + len("libdoc = ")
data, _ = json.JSONDecoder().raw_decode(html[i:])
intro = data["doc"]
sections = re.findall(r'<h2 id="([^"]+)"', intro)
kwnames = {k["name"] for k in data["keywords"]}
anchors = set(sections) | {"Importing", "Keywords"} | kwnames
print("intro sections:", sections)
print("keywords:", [k["name"] for k in data["keywords"]])
for kw in data["inits"] + data["keywords"]:
    links = re.findall(r'<a href="#([^"]+)" class="name">', kw["doc"])
    broken = [l for l in links if l not in anchors]
    print(f'{kw["name"]!r}: args={[a["repr"] for a in kw["args"]]} tags={kw.get("tags")}')
    print("   links:", sorted(set(links)), "broken:", broken)
    print("   summary:", re.sub("<.*?>", "", kw["doc"]).strip().splitlines()[0])
    print("   Example:", "Example" in kw["doc"], "| Optionally asserts:", "Optionally asserts" in kw["doc"],
          "| table:", "Arguments" in kw["doc"])
intro_links = re.findall(r'<a href="#([^"]+)" class="name">', intro)
print("intro links:", sorted(set(intro_links)), "broken:", [l for l in intro_links if l not in anchors])
EOF`*

```
intro sections: ['Shop and workshop space', 'Carts and library scope', 'Assertions', 'Shop errors']
keywords: ['Add Product To Cart', 'Get Cart Item Count', 'Get Cart Total', 'Get Product Count', 'Get Product Price']
'__init__': args=['url: str', 'space: str | None = None'] tags=[]
   links: [] broken: []
   summary: Imports the library for the shop at url.
   Example: True | Optionally asserts: False | table: True
'Add Product To Cart': args=['product_id: int', 'quantity: int = 1'] tags=['Cart', 'Setter']
   links: [] broken: []
   summary: Adds quantity of the product with product_id to the cart.
   Example: True | Optionally asserts: False | table: True
'Get Cart Item Count': args=['assertion_operator: AssertionOperator | None = None', 'assertion_expected: int | str = 0', 'message: str | None = None'] tags=['Assertion', 'Cart', 'Getter']
   links: [] broken: []
... (15 more lines)
```

*The agent runs `uv run python - <<'EOF'
import json, re
html = open("docs/DemoShopLibrary.html", encoding="utf-8").read()
i = html.index("libdoc = ") + len("libdoc = ")
data, _ = json.JSONDecoder().raw_decode(html[i:])
doc = next(k for k in data["keywords"] if k["name"] == "Get Product Price")["doc"]
print(doc[:1500])
print("=== h2 sample:", re.findall(r'<h2[^>]*>', data["doc"]))
EOF`*

```
<p>Returns the price of the product with <code>product_id</code> as a float.</p>
<table border="1">
<tr>
<th>Arguments</th>
<th>Description</th>
</tr>
<tr>
<td><code>product_id</code></td>
<td>Id of the product, an integer. An unknown id fails the keyword with the shop's <code>Product not found</code>.</td>
</tr>
<tr>
<td><code>assertion_operator</code></td>
... (19 more lines)
```

*The agent runs `uv run python - <<'EOF'
import json, re
from urllib.parse import unquote
html = open("docs/DemoShopLibrary.html", encoding="utf-8").read()
i = html.index("libdoc = ") + len("libdoc = ")
data, _ = json.JSONDecoder().raw_decode(html[i:])
sections = set(re.findall(r'<h2 id="([^"]+)"', data["doc"]))
anchors = sections | {"Importing", "Keywords"} | {k["name"] for k in data["keywords"]}
for name, doc in [("__intro__", data["doc"])] + [(k["name"], k["doc"]) for k in data["inits"] + data["keywords"]]:
    links = {unquote(l) for l in re.findall(r'<a href="#([^"]+)"[^>]*class="name"', doc)}
    unresolved = re.findall(r'<span class="name">([^<]+)</span>', doc)
    print(f"{name}: links={sorted(links)} broken={sorted(links - anchors)} unresolved={unresolved}")
EOF`*

```
__intro__: links=['Add Product To Cart', 'Assertions', 'Get Cart Item Count', 'Get Cart Total', 'Get Product Count', 'Get Product Price', 'Importing'] broken=[] unresolved=[]
__init__: links=['Carts and library scope'] broken=[] unresolved=[]
Add Product To Cart: links=['Add Product To Cart', 'Carts and library scope', 'Get Cart Item Count'] broken=[] unresolved=[]
Get Cart Item Count: links=['Add Product To Cart', 'Assertions', 'Get Cart Item Count'] broken=[] unresolved=[]
Get Cart Total: links=['Add Product To Cart', 'Assertions', 'Get Cart Total'] broken=[] unresolved=[]
Get Product Count: links=['Assertions', 'Get Product Count'] broken=[] unresolved=[]
Get Product Price: links=['Assertions', 'Get Product Price'] broken=[] unresolved=[]
```

**Agent:**

Libdoc lists all five keywords. Every `Assertions` link resolves, and so does every other link. Marking 6.1 done, then moving to the README.

*The agent edits `<repo>/openspec/changes/add-demoshop-library/tasks.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/tasks.md has been upd
```

**Agent:**

Working on task 8.1: README usage section.

*The agent reads `<repo>/atest/resources/demoshop.resource`*

*The agent reads `<repo>/atest/cart_keywords.robot`*

*The agent writes `<repo>/README.md`*

```
File created successfully at: <repo>/README.md (file state is current in yo
```

**Agent:**

Now I'll check the README against the libdoc signatures and run its example test against the shop.

*The agent runs `uv run python - <<'EOF'
import json, re
html = open("docs/DemoShopLibrary.html", encoding="utf-8").read()
i = html.index("libdoc = ") + len("libdoc = ")
data, _ = json.JSONDecoder().raw_decode(html[i:])
readme = open("README.md", encoding="utf-8").read()
rows = dict(re.findall(r"^\| `([^`]+)` \| (.+?) \|", readme, re.M))
rows.pop("Keyword", None)
assert set(rows) == {k["name"] for k in data["keywords"]}, rows.keys()
for kw in data["keywords"]:
    libdoc_args = [a["name"] + (f"={a['defaultValue']}" if a["defaultValue"] is not None else "") for a in kw["args"]]
    readme_args = re.findall(r"`([^`]+)`", rows[kw["name"]])
    print(("OK  " if libdoc_args == readme_args else "DIFF"), kw["name"], libdoc_args, readme_args)
init = [a["name"] for a in data["inits"][0]["args"]]
print("init args:", init)
EOF
mkdir -p /tmp/readme-check && awk '/```robotframework/{f=1;next} /```/{f=0} f' README.md > /tmp/readme-check/readme_example.robot && cat /tmp/readme-check/readme_example.robot && uv run robot --outputdir /tmp/readme-check /tmp/readme-check/readme_example.robot | tail -8`*

```
OK   Add Product To Cart ['product_id', 'quantity=1'] ['product_id', 'quantity=1']
OK   Get Cart Item Count ['assertion_operator=None', 'assertion_expected=0', 'message=None'] ['assertion_operator=None', 'assertion_expected=0', 'message=None']
OK   Get Cart Total ['assertion_operator=None', 'assertion_expected=0', 'message=None'] ['assertion_operator=None', 'assertion_expected=0', 'message=None']
OK   Get Product Count ['assertion_operator=None', 'assertion_expected=0', 'message=None'] ['assertion_operator=None', 'assertion_expected=0', 'message=None']
OK   Get Product Price ['product_id', 'assertion_operator=None', 'assertion_expected=0', 'message=None'] ['product_id', 'assertion_operator=None', 'assertion_expected=0', 'message=None']
init args: ['url', 'space']
*** Settings ***
Library    demoshop_library.DemoShopLibrary    url=http://localhost:9090    space=team-7

*** Test Cases ***
Buy Two Desks
    Get Product Price      5    ==    799
... (11 more lines)
```

**Agent:**

The README signatures match libdoc, and its example test passes against the shop. Marking 8.1 done and starting the final full run (8.2).

*The agent edits `<repo>/openspec/changes/add-demoshop-library/tasks.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/tasks.md has been upd
```

*The agent runs `echo "=== pytest" && uv run pytest -q 2>&1 | tail -3 && echo "=== robot" && uv run robot --outputdir results atest 2>&1 | grep -E "^(Atest|[0-9]+ tests?,)|FAIL" ; echo "robot exit=${PIPESTATUS[0]}"`*

```
=== pytest
........................................................................ [ 94%]
....                                                                     [100%]
76 passed in 0.13s
=== robot
Atest                                                                         
Atest.Cart Keywords :: Cart keywords. Every test starts with an empty cart ...
Atest.Cart Keywords :: Cart keywords. Every test starts with an em... | PASS |
7 tests, 7 passed, 0 failed
Atest.Getter Assertions :: The assertion arguments shared by every Get keyw...
Atest.Getter Assertions :: The assertion arguments shared by every... | PASS |
8 tests, 8 passed, 0 failed
... (9 more lines)
```

**Agent:**

Unit tests (76) and acceptance tests (26) pass. Next I'll run the 7.6 keyword-owner check and inspect the built wheel.

*The agent runs `uv run python - <<'EOF'
from collections import Counter
from robot.api import ExecutionResult, ResultVisitor

ALLOWED = {"demoshop_library.DemoShopLibrary", "ShopA", "ShopB"}

class Owners(ResultVisitor):
    def __init__(self):
        self.owners = Counter()
        self.bad = []
    def start_keyword(self, kw):
        self.owners[kw.owner] += 1
        if kw.owner not in ALLOWED:
            self.bad.append((kw.parent.full_name if hasattr(kw.parent, "full_name") else kw.parent, kw.full_name))

result = ExecutionResult("results/output.xml")
v = Owners()
result.visit(v)
print("stats:", result.statistics.total.passed, "passed,", result.statistics.total.failed, "failed")
print("owners:", dict(v.owners))
print("violations:", v.bad or "none")
EOF
echo "=== build"; rm -rf dist && uv build 2>&1 | tail -3 && uv run python -c "
import zipfile, glob
whl = glob.glob('dist/*.whl')[0]
names = zipfile.ZipFile(whl).namelist()
print(whl); [print('  ', n) for n in names]
need = [f'demoshop_library/{m}.py' for m in ('__init__','library','client','products','cart')] + ['demoshop_library/py.typed']
print('missing:', [n for n in need if n not in names] or 'none')
print('tests/atest present:', [n for n in names if n.startswith(('tests/','atest/'))] or 'none')
"`*

```
stats: 26 passed, 0 failed
owners: {'demoshop_library.DemoShopLibrary': 54, 'ShopA': 9, 'ShopB': 5}
violations: none
=== build
Building wheel from source distribution (uv build backend)...
Successfully built dist/demoshop_library-0.1.0.tar.gz
Successfully built dist/demoshop_library-0.1.0-py3-none-any.whl
dist/demoshop_library-0.1.0-py3-none-any.whl
   demoshop_library/
   demoshop_library/__init__.py
   demoshop_library/assertions.py
   demoshop_library/cart.py
... (10 more lines)
```

**Agent:**

Every check in 8.2 passes. Marking it done.

*The agent edits `<repo>/openspec/changes/add-demoshop-library/tasks.md`*

```
The file <repo>/openspec/changes/add-demoshop-library/tasks.md has been upd
```

*The agent runs `openspec instructions apply --change "add-demoshop-library" --json | uv run python -c "import json,sys; d=json.load(sys.stdin); print(d['state'], d['progress'])"; openspec validate add-demoshop-library 2>&1 | tail -2`*

```
all_done {'total': 22, 'complete': 22, 'remaining': 0}
Change 'add-demoshop-library' is valid
```

**Agent:**

## Implementation Complete

**Change:** add-demoshop-library
**Schema:** spec-driven
**Progress:** All 22 tasks are done, and `openspec validate` reports the change as valid.

### Completed This Session
- [x] **6.1 Keyword documentation:** No changes were needed; the docstrings already followed the reference shape. I checked the generated `docs/DemoShopLibrary.html`: it lists all five keywords, every `Get` keyword's `assertion_operator` row links to `Assertions`, and every other link works too.
- [x] **8.1 README:** I wrote a usage section in `README.md` with an import example, a table of the five keywords, and the commands for unit tests, acceptance tests, libdoc and build. The table's arguments match the libdoc output, and the README's example test passed against the shop.
- [x] **8.2 Final run:**
  - `uv run pytest`: 76 passed.
  - `uv run robot --outputdir results atest`: 26 passed, 0 failed.
  - The 7.6 check found every executed keyword owned by `demoshop_library.DemoShopLibrary`, `ShopA` or `ShopB`.
  - `uv build`: the wheel contains the required modules and `py.typed`, and no `tests/` or `atest/`.

### Two things to fix in the plan before archiving
1. **The spec's libdoc command fails.** The "Generate documentation" scenario in `specs/library-import/spec.md` uses `robot.libdoc demoshop_library.DemoShopLibrary ...` without the URL. That fails with `expected 1 to 2 arguments, got 0`, because `url` is required. Task 6.1 and `AGENTS.md` use the form with `::url=http://localhost:9090`, which works, and that's the form I used. The project context returned by the OpenSpec CLI has the same broken command. I'd update the spec scenario to the `::url=` form (`/opsx:update`) rather than make `url` optional, which would go against the import requirement.
2. **An extra module isn't in the design.** `src/demoshop_library/assertions.py` was added in an earlier session. It rejects text operators before any request is sent, which task 4.2 needs. The package layout in `design.md` (decision 1) doesn't list it. One line in the design would fix that.

Once those are updated, you can archive with `/opsx:archive`.

**The participant runs** `grep -c '^- \[x\]' openspec/changes/*/tasks.md; grep '^- \[ \]' openspec/changes/*/tasks.md || echo 'no open task'`:

```
22
no open task
```

**The participant runs** `uv run pytest
uv run robot --outputdir results atest
uv run python -m robot.libdoc "demoshop_library.DemoShopLibrary::url=http://localhost:9090" docs/DemoShopLibrary.html
uv build`:

```
------------------------------------------------------------------------------
Two Instances Have Separate Carts                                     | PASS |
------------------------------------------------------------------------------
Test Adds Products                                                    | PASS |
------------------------------------------------------------------------------
Cart Does Not Carry Over To The Next Test                             | PASS |
------------------------------------------------------------------------------
Test Setup Shares The Test's Cart                                     | PASS |
------------------------------------------------------------------------------
Suite Setup Cart Is Not Visible To Tests                              | PASS |
------------------------------------------------------------------------------
Atest.Library Import :: Importing the library: URL, workshop space... | PASS |
... (28 more lines)
```

**The participant runs** `cat > results-assert.robot <<'ROBOT'
*** Settings ***
Library    demoshop_library.DemoShopLibrary    url=http://localhost:9090

*** Test Cases ***
The price passes
    Get Product Price    1    ==    249.99

The wrong price fails with AssertionEngine's message
    Run Keyword And Expect Error    *    Get Product Price    1    ==    1
    ${message}=    Run Keyword And Expect Error    *    Get Product Price    1    ==    1
    Log To Console    ${message}
ROBOT
uv run robot --outputdir results-assert results-assert.robot; rm -f results-assert.robot`:

```
==============================================================================
Results-Assert                                                                
==============================================================================
The price passes                                                      | PASS |
------------------------------------------------------------------------------
The wrong price fails with AssertionEngine's message                  Product 1 price '249.99' (float) should be '1.0' (float)
| PASS |
------------------------------------------------------------------------------
Results-Assert                                                        | PASS |
2 tests, 2 passed, 0 failed
==============================================================================
Output:  <repo>/results-assert/output.xml
... (2 more lines)
```

## Step 8 - Compare it with user keywords

**Prompt:**

> Compare this library with ../ai-engineering-robotframework/resources/api.resource, which reaches the same API with user keywords and RequestsLibrary. Name one thing the library gives that the resource does not, and one thing it costs. Three sentences at most.

*The agent runs `ls ../ai-engineering-robotframework/resources/ 2>&1; ls ../ai-engineering-robotframework/resources/ 2>&1; ls src/demoshop_library tests atest`*

```
api.resource
catalogue.resource
checkout.resource
legacy.resource
shop.resource
api.resource
catalogue.resource
checkout.resource
legacy.resource
shop.resource
atest:
cart_keywords.robot
... (23 more lines)
```

*The agent runs `cat ../ai-engineering-robotframework/resources/api.resource; echo ----; cat src/demoshop_library/library.py src/demoshop_library/client.py src/demoshop_library/cart.py src/demoshop_library/products.py src/demoshop_library/assertions.py`*

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
... (405 more lines)
```

**Agent:**

**Gives:** The library's keywords check the result in the same step, and their failures are worded in shop terms. For example, `Get Product Price    1    ==    249.99` compares two floats and fails with `Getting product 999999 failed: Product not found (HTTP 404)`, whereas `Get Catalogue From API` returns raw JSON, so the test has to make its own checks and gets RequestsLibrary's generic HTTP error. **Costs:** The library is a Python package with its own unit tests, dependency pins, build and release, so supporting a new endpoint means writing Python, while the resource is about 25 lines of Robot that any tester can edit in place.
