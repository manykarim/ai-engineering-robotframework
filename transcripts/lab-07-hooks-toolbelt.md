# Lab 7 - Hooks and the toolbelt: the recorded walkthrough

*Recorded with Claude Code 2.1.281, from the lab's instructions. Results are shortened; your agent's answers will differ in wording.*

## Step 1 - Wire the hooks

*Lab 4 recorded the plugin in `.claude/settings.json`, so the hooks section is merged into it.*

**The participant runs** `uv run --no-sync python -c "import json,pathlib; p=pathlib.Path('.claude/settings.json'); s=json.loads(p.read_text()) if p.exists() else {}; s['hooks']=json.loads(pathlib.Path('hooks/claude-code.settings.json').read_text())['hooks']; p.write_text(json.dumps(s, indent=2)+chr(10))" && cat .claude/settings.json`:

```
    }
  },
  "enabledPlugins": {
    "robotcode@robotframework-agent-plugins": true
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
... (28 more lines)
```

## Step 2 - Try them

**Prompt:**

> Do these three steps in order, and after each one report exactly what happened. Do not work around anything that is blocked or rejected; just report it and continue with the next step.
> 1. In tests/ui/checkout.robot, add the line "    Click    css=button.buy" as the last step of the test "WEB-006_AC-7 Successful Order".
> 2. In tests/api/smoke.robot, in the test "Health Reports Ok", change the expected status value ok to okay.
> 3. Run the shell command: git commit -am "hook check"

**Agent:**

I'll start by reading the target files and the conventions doc.

*The agent reads `<repo>/tests/ui/checkout.robot`*

*The agent reads `<repo>/tests/api/smoke.robot`*

*The agent reads `<repo>/docs/conventions.md`*

*The agent edits `<repo>/tests/ui/checkout.robot`*

```
PreToolUse:Edit hook error: [uv run --no-sync --project "$CLAUDE_PROJECT_DIR" python "$CLAUDE_PROJECT_DIR/hooks/no_inline_locators.py"]: Rejected: this edit adds the locator literal 'css=button.buy' t
```

**Agent:**

A hook rejected step 1. As you asked, I won't work around it. Moving on to step 2.

*The agent edits `<repo>/tests/api/smoke.robot`*

```
The file <repo>/tests/api/smoke.robot has been updated successfully. (file state
```

**Agent:**

The step 2 edit was written, but a post-edit hook ran the affected tests and "Health Reports Ok" failed. I'm leaving the edit as it is and moving on to step 3.

*The agent runs `git commit -am "hook check"`*

```
PreToolUse:Bash hook error: [uv run --no-sync --project "$CLAUDE_PROJECT_DIR" python "$CLAUDE_PROJECT_DIR/hooks/green_before_commit.py"]: Commit blocked: The latest suite run has 1 failed test(s): Hea
```

**Agent:**

A hook blocked steps 1 and 3; step 2's edit went in but its test failed.

**1. Adding `Click    css=button.buy` to "WEB-006_AC-7 Successful Order": rejected.** The `hooks/no_inline_locators.py` hook blocked the edit before it was written. Its message: "this edit adds the locator literal 'css=button.buy' to tests/ui/checkout.robot… test files call keywords, and every locator is written inside a keyword under resources/." `tests/ui/checkout.robot` is unchanged.

**2. Changing `ok` to `okay` in "Health Reports Ok": written, then the test failed.** The edit was saved to `tests/api/smoke.robot:14`. Right after, `hooks/run_affected_tests.py` ran that file's tests: 1 passed and 1 failed. "Health Reports Ok" failed with `ok != okay`, because the shop reports `ok`. The edit is still in the working tree.

**3. `git commit -am "hook check"`: blocked.** `hooks/green_before_commit.py` stopped the command before it ran: "Commit blocked: The latest suite run has 1 failed test(s): Health Reports Ok. Fix them before you commit." Nothing was committed.

The `smoke.robot` edit is the only change left behind. `git checkout tests/api/smoke.robot` would undo it; I haven't run that.

**The participant runs** `git checkout -- tests/api/smoke.robot && git status --short tests`:

```
 M tests/ui/catalogue.robot
?? tests/api/AGENTS.md
?? tests/ui/cart.robot
?? tests/ui/product_detail.robot
?? tests/ui/search.robot
```

## Step 3 - Let the hook check the whole suite

**The participant runs** `uv run --no-sync python hooks/no_inline_locators.py tests/; echo "exit $?"`:

```
tests/ui/catalogue.robot:68: locator literal 'role=link[name="Reset"]' in a test file
exit 1
```

**Prompt:**

> uv run --no-sync python hooks/no_inline_locators.py tests/ reports a locator literal in a test file. Move it into a keyword under resources/, following docs/conventions.md, and run the affected test.

*The agent runs `uv run --no-sync python hooks/no_inline_locators.py tests/; echo "exit=$?"`*

```
tests/ui/catalogue.robot:68: locator literal 'role=link[name="Reset"]' in a test file
exit=1
```

*The agent reads `<repo>/docs/conventions.md`*

*The agent reads `<repo>/docs/agent-environment.md`*

*The agent reads `<repo>/tests/ui/catalogue.robot`*

*The agent reads `<repo>/resources/catalogue.resource`*

*The agent runs `git diff -- tests/ui/catalogue.robot resources/catalogue.resource`*

```
diff --git a/resources/catalogue.resource b/resources/catalogue.resource
index 0b9bc0b..6a09c9a 100644
--- a/resources/catalogue.resource
+++ b/resources/catalogue.resource
@@ -95,6 +95,16 @@ Get Highlight Prices
     END
     RETURN    ${prices}
 
+Get Highlight Names
+    [Documentation]    The product names shown in "Handpicked highlights", in page order.
+    @{links}=    Get Texts    ${HIGHLIGHTS} >> role=link
+    @{names}=    Create List
... (47 more lines)
```

*The agent runs `grep -rn "AC-10" openspec/specs/shop/ | head; ls openspec/specs/shop/; cat hooks/no_inline_locators.py`*

```
openspec/specs/shop/authentication/spec.md:84:### Requirement: Signed-in state persists across pages (WEB-007_AC-10)
openspec/specs/shop/cart/spec.md:9:When a shopper clicks the "Add to Cart" button on a product card on any page - the home page, the products page or a detail page - a POST request SHALL be sent to `/
openspec/specs/shop/cart/spec.md:68:### Requirement: Session identification (WEB-005_AC-10)
openspec/specs/shop/cart/spec.md:142:### Requirement: Default session key (API-005_AC-10)
openspec/specs/shop/catalogue/spec.md:71:### Requirement: Reset filters (WEB-002_AC-10)
openspec/specs/shop/checkout/spec.md:76:### Requirement: Empty cart at checkout (WEB-006_AC-10)
authentication
cart
catalogue
checkout
interpretation-rules
product-detail
... (86 more lines)
```

*The agent reads `<repo>/openspec/specs/shop/catalogue/spec.md`*

*The agent reads `<repo>/openspec/specs/shop/interpretation-rules/spec.md`*

*The agent runs `grep -rn "link\|has-text\|text=" resources/*.resource | grep -v legacy.resource; echo ---; uv run --no-sync python -m shop status`*

```
resources/checkout.resource:15:${CART LINK}        role=banner >> role=link[name=/^Cart/]
resources/checkout.resource:90:    [Documentation]    The visible text of the cart link in the site header.
resources/cart.resource:5:...                 visible text, and the header's link to the cart page.
resources/cart.resource:15:# The whole number inside the header's link to the cart page. The spec quotes no text
resources/cart.resource:16:# for that link or its badge, so the link is found by its target.
resources/cart.resource:17:${CART BADGE}           role=banner >> a[href="/cart"] >> text=/^\\d+$/
resources/cart.resource:62:    RETURN    role=main >> article:has-text("${name}")
resources/cart.resource:102:    RETURN    ${SUMMARY} >> text=/\\b${word}\\b[\\s\\S]*${value}/i
resources/catalogue.resource:18:${CARD PRICE}       text=/^\\$[0-9,]+\\.[0-9]{2}$/
resources/catalogue.resource:33:    ${count}=    Get Element Count    ${GRID} >> article >> button:has-text("Add to cart")
resources/catalogue.resource:90:    @{links}=    Get Texts    ${HIGHLIGHTS} >> role=link
resources/catalogue.resource:92:    FOR    ${text}    IN    @{links}
... (23 more lines)
```

**Agent:**

The locator is `role=link[name="Reset"]` on `tests/ui/catalogue.robot:68`. The shop is running locally, so I'm checking the Reset link's markup before I write the keyword.

*The agent runs `curl -s http://localhost:9090/products | grep -o -i '<a[^>]*>[^<]*reset[^<]*</a>\|<[^>]*>[^<]*Reset[^<]*<' | head; curl -s http://localhost:9090/products | grep -o -i '<aside.\{0,200\}' | head -3`*

```
<a class="button button--ghost" href="/products">Reset</a>
<p class="product-card__description">Spatial audio headphones with adaptive noise control, AI-powered equaliser presets, and all-day comfort for deep work sessions.<
<p class="product-card__description">Compact drone with autonomous flight plans, cinematic presets, and multi-sensor collision avoidance.<
<aside class="filters-panel">
<aside class="chat-widget" id="chat-widget" hidden>
```

*The agent edits `<repo>/resources/catalogue.resource`*

*The agent edits `<repo>/tests/ui/catalogue.robot`*

```
The file <repo>/resources/catalogue.resource has been updated successfully. (fil
```

```
The file <repo>/tests/ui/catalogue.robot has been updated successfully. (file st
```

*The agent runs `uv run --no-sync python hooks/no_inline_locators.py tests/; echo "hook exit=$?"; uv run robotcode robot -t "WEB-002_AC-10 Reset Filters" 2>&1 | tail -20`*

```
hook exit=0
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
==============================================================================
... (9 more lines)
```

**Agent:**

I moved the locator into a new keyword, and the affected test passes against the local shop. The locator check now finds nothing in `tests/`.

**The finding:** `tests/ui/catalogue.robot:68` clicked `role=link[name="Reset"]` directly in the test.

**The fix:**
- **`resources/catalogue.resource`**: added a `Reset Filters` keyword right after `Apply Filters`. It clicks `${FILTERS} >> a:has-text("Reset")` and waits for the product grid, like `Apply Filters` does. The spec quotes "Reset" as link text, so the keyword finds the link by its visible text rather than its accessible name (convention 4). It also only looks inside the filter sidebar. In the shop the link is `<a href="/products">Reset</a>`.
- **`tests/ui/catalogue.robot`**: the test now calls `Reset Filters` instead of clicking the locator.

`uv run robotcode robot -t "WEB-002_AC-10 Reset Filters"` passed (1 test, 1 passed, 0 failed). I only ran that one test. Both files already had uncommitted changes from earlier work; I left those alone and didn't commit anything.

**The participant runs** `uv run --no-sync python hooks/no_inline_locators.py tests/; echo "exit $?"`:

```
exit 0
```

## Step 4 - Switch the shop

**The participant runs** `uv run --no-sync python -m shop preset buggy`:

```
applied preset buggy in space default
```

## Step 5 - Run the suite

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

## Step 6 - Draft an issue

**Prompt:**

> Look at the failed tests of the last run with robotcode results. Pick one failure that is a defect of the shop, not of the test. Write the steps a person would follow in the browser to see it, the expected behaviour according to openspec/specs/shop, the actual behaviour, and the evidence from the run. Save it as results/issue.md with the title as its first line. Do not file it.

*The agent reads `<repo>/docs/agent-environment.md`*

*The agent loads the skill `robotcode:robotcode`*

*The agent reads `~/.claude/plugins/cache/robotframework-agent-plugins/robotcode/7c753f8adca1/skills/robotcode/references/results.md`*

*The agent reads `<repo>/docs/conventions.md`*

*The agent runs `ls results/ && uv run --no-sync robotcode results summary --failed`*

```
browser
compare
dryrun
final-cart
lab-02
lab-03
log.html
mutants
output.xml
playwright-log.txt
repeat
report.html
... (21 more lines)
```

*The agent runs `uv run --no-sync robotcode results show --help | head -80`*

```
Usage: robotcode results show [OPTIONS]

  List individual tests with status, source and failure message.

  One line per test: status badge, full name, `(path:line)` link, and the
  first line of any failure/skip message.

  Examples:
  ```
  robotcode results show
  robotcode results show --failed
  robotcode results show --failed --skipped --tags
... (68 more lines)
```

*The agent runs `uv run --no-sync robotcode results show --failed --tags --message-chars 0`*

```
# Show — results/output.xml

- ❌ **FAIL** Tests.Ui.Catalogue.WEB-002_AC-1 Every Card Offers Add To Cart (`tests/ui/catalogue.robot:17`) _(12:05:45 · 2.04 s)_
  > Every product card should offer "Add to cart".: 10 != 12
  - _Tags:_ ui, web-002
- ❌ **FAIL** Tests.Ui.Catalogue.WEB-002_AC-1 Card Prices Are The Product Prices (`tests/ui/catalogue.robot:26`) _(12:05:47 · 5.79 s)_
  > Cascade Water Bottle should cost $79.00.: $90.85 != $79.00
  - _Tags:_ ui, web-002
- ❌ **FAIL** Tests.Ui.Checkout.WEB-006_AC-1 Order Total Adds Up (`tests/ui/checkout.robot:17`) _(12:06:15 · 423 ms)_
  > The order total should be subtotal plus shipping plus tax.: 249.99 != 267.49
  - _Tags:_ ui, web-006

... (11 more lines)
```

**Agent:**

I'm checking the three failures from the last run against the test code and the shop spec to see which one comes from the shop rather than the test.

*The agent runs `git diff -- tests/ui/catalogue.robot resources/catalogue.resource resources/api.resource`*

```
diff --git a/resources/api.resource b/resources/api.resource
index 2596185..6dc0b45 100644
--- a/resources/api.resource
+++ b/resources/api.resource
@@ -23,3 +23,11 @@ Get Catalogue From API
     [Documentation]    Every product, as dictionaries, from ``GET /api/products/``.
     ${response}=    GET On Session    shop    /api/products/    expected_status=200
     RETURN    ${response.json()}[items]
+
+Get Product From API
+    [Documentation]    The product with the given ID, as a dictionary, from the catalogue listing.
+    [Arguments]    ${product_id}
... (84 more lines)
```

*The agent runs `uv run --no-sync robotcode results log --help | head -60`*

```
Usage: robotcode results log [OPTIONS]

  Show the execution log of each test: keywords, control flow and messages.

  Filter the same way as `show` — by status, tag, suite, or test name. Without
  filters, all tests are included. Use `--max-depth` to collapse deeply nested
  keyword calls.

  Examples:
  ```
  robotcode results log
  robotcode results log --failed
... (48 more lines)
```

*The agent runs `uv run --no-sync robotcode results log --failed --keyword-info 2>&1 | head -300`*

```
# Log

### Test: Tests.Ui.Catalogue.WEB-002_AC-1 Every Card Offers Add To Cart (`tests/ui/catalogue.robot:17`) ❌ **FAIL** _(12:05:45 · 2.04 s)_

> Every product card should offer "Add to cart".: 10 != 12

- **[SETUP]** **shop.Start Shop Test** ✅ **PASS** _(12:05:45 · 64 ms)_
  - _[Documentation]_ Opens a fresh context and page for one test.
  - **IF**
    - **IF** `"${SHOP_SPACE}"` ⏸ **NOT RUN** _(12:05:45 · 1 ms)_
      - `&{headers}` = **BuiltIn.Create Dictionary** `X-Workshop-Space=${SHOP_SPACE}` ⏸ **NOT RUN** _(12:05:45 · 0 ms)_
        - _[Documentation]_ Creates and returns a dictionary based on the given \`items\`.
... (288 more lines)
```

*The agent runs `uv run --no-sync robotcode results log --failed 2>&1 | sed -n '300,2000p' | grep -vE '^\s+- _\[(Documentation|Tags)\]_' | grep -nE 'Text:|FAIL|\$\{shown\}|@\{shown\}|should cost|^### |INFO\] \$\{|INFO\] @\{|INFO\] &\{' | head -120`*

```
1:        - `[INFO] ${text} = $79.00`
3:      - `[INFO] ${expected} = $79.00`
4:    - **BuiltIn.Should Be Equal** `${price}` `${expected}` `msg=${name} should cost ${expected}.` ❌ **FAIL** _(12:05:53 · 0 ms)_
5:      > Cascade Water Bottle should cost $79.00.: $90.85 != $79.00
6:      - `[FAIL] Cascade Water Bottle should cost $79.00.: $90.85 != $79.00`
11:### Test: Tests.Ui.Checkout.WEB-006_AC-1 Order Total Adds Up (`tests/ui/checkout.robot:17`) ❌ **FAIL** _(12:06:15 · 423 ms)_
52:      - `[INFO] Text: ['Cart\n1']`
61:    - `[INFO] Text: ['$249.99']`
62:    - `[INFO] ${text} = $249.99`
68:      - `[INFO] @{amounts} = [ 249.99 ]`
72:      - `[INFO] ${amount} = 249.99`
74:    - `[INFO] ${amount} = 249.99`
... (19 more lines)
```

*The agent runs `uv run --no-sync robotcode results log -t "*Card Prices Are The Product Prices" 2>&1 | grep -vE '^\s+- _\[(Documentation|Tags)\]_' | sed -n '/legacy.Get Card Prices/,$p' | grep -E 'Text:|FAIL|INFO\] [@$&]\{|FOR|ITER|Should|Format' | head -120`*

```
      - `[INFO] ${grid} = section:has(h2:text-is("All products")):not(:has(section)) >> .product-grid`
    - `[INFO] ${grid} = section:has(h2:text-is("All products")):not(:has(section)) >> .product-grid`
      - `[INFO] @{elements} = [ section:has(h2:text-is("All products")):not(:has(section)) >> .product-grid >> article >> text=/^\$[0-9,]+\.[0-9]{2}$/ >> nth=0 | section:has(h2:text-is("All products")
      - `[INFO] @{texts} = [ ]`
    - **FOR** `${element}` `IN` `@{elements}` ✅ **PASS** _(12:05:53 · 232 ms)_
      - **ITER** `${element}` ✅ **PASS** _(12:05:53 · 19 ms)_
          - `[INFO] Text: ['$799.00']`
          - `[INFO] ${text} = $799.00`
      - **ITER** `${element}` ✅ **PASS** _(12:05:53 · 20 ms)_
          - `[INFO] Text: ['$249.99']`
          - `[INFO] ${text} = $249.99`
      - **ITER** `${element}` ✅ **PASS** _(12:05:53 · 18 ms)_
... (49 more lines)
```

*The agent reads `<repo>/tests/ui/catalogue.robot`*

*The agent reads `<repo>/tests/ui/checkout.robot`*

*The agent runs `ls -R openspec/specs/shop/ && git log --oneline -3 -- openspec/specs/shop && git status --short openspec/specs/shop`*

```
openspec/specs/shop/:
authentication
cart
catalogue
checkout
interpretation-rules
product-detail
search

openspec/specs/shop/authentication:
spec.md

... (18 more lines)
```

*The agent reads `<repo>/openspec/specs/shop/checkout/spec.md`*

*The agent reads `<repo>/openspec/specs/shop/catalogue/spec.md`*

*The agent reads `<repo>/openspec/specs/shop/interpretation-rules/spec.md`*

**Agent:**

Three failures: two on the catalogue page (Add to Cart buttons, card prices) and one on checkout (order total). Next I'm checking the keywords behind each to rule out test-side causes.

*The agent runs `ls resources/ && wc -l resources/*.resource`*

```
api.resource
cart.resource
catalogue.resource
checkout.resource
legacy.resource
product_detail.resource
search.resource
shop.resource
   33 resources/api.resource
  127 resources/cart.resource
  117 resources/catalogue.resource
   92 resources/checkout.resource
... (5 more lines)
```

*The agent reads `<repo>/resources/checkout.resource`*

*The agent reads `<repo>/resources/legacy.resource`*

*The agent reads `<repo>/resources/catalogue.resource`*

**Agent:**

The checkout total is read through a legacy `data-test` hook, which is the kind of locator the workshop expects to drift. So I'm checking the live shop before I blame it.

*The agent runs `uv run --no-sync python -m shop status 2>&1 | head -40`*

```
shop     http://localhost:9090  (version 0.3.0)
space    default
presets  stage1, buggy
```

*The agent runs `cd /tmp && curl -s http://localhost:9090/products -o /tmp/products.html -w '%{http_code} %{size_download}\n' && grep -c '<article' /tmp/products.html; python3 - <<'EOF'
import re,html
s=open('/tmp/products.html').read()
i=s.find('All products')
print(i)
arts=re.findall(r'<article.*?</article>', s[i:], re.S)
print(len(arts))
for a in arts[:13]:
    name=re.search(r'<h3[^>]*>(.*?)</h3>',a,re.S)
    btn=re.findall(r'<button[^>]*>(.*?)</button>',a,re.S)
    prices=re.findall(r'\$[0-9,]+\.[0-9]{2}',a)
    print(re.sub(r'<[^>]+>','',name.group(1)).strip() if name else None, prices, [re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',b)).strip() for b in btn])
EOF`*

```
200 55213
18
21582
12
Atlas Standing Desk ['$799.00'] []
Aurora Neural Headphones ['$249.99'] ['Add to cart']
Cascade Water Bottle ['$90.85'] ['Add to cart']
Echo Conference Speaker ['$219.00'] []
Focus Loop Timer ['$59.00'] ['Add to cart']
Horizon Portable Display ['$389.00'] ['Add to cart']
Insight Smart Notebook ['$39.50'] ['Add to cart']
Nimbus Desk Light ['$129.00'] ['Add to cart']
... (5 more lines)
```

*The agent runs `python3 - <<'EOF'
import re
s=open('/tmp/products.html').read()
i=s.find('All products')
arts=re.findall(r'<article.*?</article>', s[i:], re.S)
for a in (arts[0], arts[1]):
    print(re.sub(r'\n\s*\n','\n',a)); print('-----')
EOF`*

```
Exit code 1
pyenv: version `3.12' is not installed (set by <repo>/.python-version)
```

*The agent runs `cd /tmp && python3 - <<'EOF'
import re
s=open('/tmp/products.html').read()
i=s.find('All products')
arts=re.findall(r'<article.*?</article>', s[i:], re.S)
for a in (arts[0], arts[1], arts[3]):
    print(re.sub(r'\n\s*\n','\n',a)); print('-----')
EOF`*

```
<article class="product-card"
  data-test="product-card">
  <div class="product-card__media">
    <picture>
      <source srcset="/static/img/atlas-desk.jpg" type="image/jpeg" />
      <img src="/static/img/atlas-desk.jpg" alt="Atlas Standing Desk product photo" loading="lazy" />
    </picture>
  </div>
  <div class="product-card__body">
    <span class="category-badge" data-category="furniture">Furniture</span>
    <h3 class="product-card__title"><a href="/products/5" data-test="product-link">Atlas Standing Desk</a></h3>
    <p class="product-card__description">Programmable standing desk with posture coaching, ambient wellness reminders, and built-in cable management.</p>
... (123 more lines)
```

*The agent runs `cd /tmp && for id in 5 10 1; do printf "product %s: " $id; curl -s http://localhost:9090/products/$id | grep -oE '<button[^>]*aria-label="Add [^"]*"[^>]*>[^<]*</button>' | sed -E 's/.*aria-label="([^"]*)".*>([^<]*)<\/button>/\1 | \2/' | head -1; echo; done; ls <repo>/results/browser | head; ls <repo>/results/browser/screenshot 2>/dev/null | head`*

```
product 5: 
product 10: 
product 1:
Shell cwd was reset to <repo>
```

**Agent:**

The two products are in stock (inventory 15 and 80), so nothing explains the missing buttons. Writing the issue now.

*The agent writes `<repo>/results/issue.md`*

```
File created successfully at: <repo>/results/issue.md (file state is current in 
```

**Agent:**

I wrote the issue to `results/issue.md`. The title is the first line and I didn't file it: **"Products page: the Atlas Standing Desk and Echo Conference Speaker cards have no "Add to Cart" button"**

**The last run:** 30 tests, 27 passed and 3 failed.

| Test | What failed | Cause |
|---|---|---|
| `WEB-002_AC-1 Every Card Offers Add To Cart` | 10 buttons instead of 12 | The shop. **This is the one I wrote up.** |
| `WEB-002_AC-1 Card Prices Are The Product Prices` | Cascade Water Bottle shows $90.85 instead of $79.00 | Also the shop. Four cards show 15% more than their price in the API. I mention it as a separate defect at the end of the issue. |
| `WEB-006_AC-1 Order Total Adds Up` | total 249.99 instead of 267.49 | Not confirmed. The total is read through a legacy `data-test` hook, the kind of locator the workshop expects to go stale. Without a closer look, I can't rule out that the test read the wrong element. |

**Why the missing buttons are the shop's fault:**
- The test finds the button by its visible text, "Add to cart", as the spec's rules require. The same locator finds it on the other 10 cards.
- The grid was fully loaded: the test counted all 12 cards first.
- I fetched the page's HTML after the run. The Atlas Standing Desk and Echo Conference Speaker cards have an empty action area with no button at all. Both products are in stock (15 and 80 units in the API).

**What the issue contains:**
- steps a person can follow in a browser;
- the expected behaviour, quoted from `openspec/specs/shop/catalogue/spec.md` and the spec's rules on matching visible text;
- the actual behaviour, with a table of the affected cards;
- evidence from the run: the failure message, the two locators with their counts (12 cards, 10 buttons), and the product stock returned by the API.

The HTML comparison is marked in the issue as a separate check made after the run, not part of it. I didn't open a browser myself: the steps are based on what the test's browser recorded and on the page's HTML.

The shop is running with the `buggy` preset (seen with `python -m shop status`), and the issue lists it under the shop details. I didn't change any presets and didn't reset anything.

**The participant runs** `cat results/issue.md`:

```
## Evidence

### From the test run (`results/output.xml`, `results/log.html`)

The test failed at 12:05:47 with:

```
Every product card should offer "Add to cart".: 10 != 12
```

The log shows the two counts it compared:

... (48 more lines)
```

## Step 7 - File it

*Not filed during the rehearsal: it ran in the workshop's own repository, not in a fork. In your fork:* `gh issue create --repo <your-handle>/ai-engineering-robotframework --title "$(head -1 results/issue.md)" --body-file results/issue.md`

## Step 8 - Put the shop back

**The participant runs** `uv run --no-sync python -m shop reset`:

```
reset space default: removed 5 flag settings, 27 cart items and 6 orders
```

**The participant runs** `uv run robotcode robot --exclude broken`:

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
Output:  <repo>/results/output.xml
Log:     <repo>/results/log.html
Report:  <repo>/results/report.html
```

**The participant runs** `uv run --no-sync python hooks/green_before_commit.py --check`:

```
The latest suite run is green and up to date: a commit may go ahead.
```
