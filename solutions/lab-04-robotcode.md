# Lab 4 - RobotCode: the reference

[Lab 4](../labs/lab-04-robotcode/INSTRUCTIONS.md) installs the RobotCode plugin, ties it to `AGENTS.md`, and has your
agent debug and repair a test broken on purpose. [Transcript](../transcripts/lab-04-robotcode.md). The commands are
on the [RobotCode cheat sheet](../docs/robotcode.md).

## The reference

The plugin, recorded for the project in `.claude/settings.json`. Codex and GitHub Copilot install it for your user,
so nothing changes in the repository there.

```json
{
  "extraKnownMarketplaces": {
    "robotframework-agent-plugins": {
      "source": {
        "source": "github",
        "repo": "robotcodedev/robotframework-agent-plugins"
      }
    }
  },
  "enabledPlugins": {
    "robotcode@robotframework-agent-plugins": true
  }
}
```

The line in `AGENTS.md`:

```diff
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -29,3 +29,6 @@ Before writing or changing a test or a keyword, read [docs/conventions.md](docs/
 - Never read, print or copy `.env`.
 - Never install tools the repository does not pin: no `pip install`, no `rfbrowser init`, no new dependencies.
 - Never change `openspec/specs/shop/` to match what the shop does.
+
+Use RobotCode through uv (`uv run robotcode ...`) to discover tests and keywords, read library docs, debug
+failing tests and read results.
```

The repaired test, and the keyword it needed:

```diff
--- a/resources/catalogue.resource
+++ b/resources/catalogue.resource
@@ -95,6 +95,16 @@ Get Highlight Prices
     END
     RETURN    ${prices}
 
+Get Highlight Names
+    [Documentation]    The product names shown in "Handpicked highlights", in page order.
+    @{links}=    Get Texts    ${HIGHLIGHTS} >> role=link
+    @{names}=    Create List
+    FOR    ${text}    IN    @{links}
+        ${name}=    Replace String Using Regexp    ${text}    \\$[0-9,]+\\.[0-9]{2}    ${EMPTY}
+        Append To List    ${names}    ${name.strip()}
+    END
+    RETURN    ${names}
+
 Format Price
     [Documentation]    ``249.99`` as the shop shows it: ``$249.99``.
     [Arguments]    ${amount}
--- a/tests/ui/catalogue.robot
+++ b/tests/ui/catalogue.robot
@@ -74,11 +74,16 @@ WEB-002_AC-10 Reset Filters
     Should Be Equal As Integers    ${cards}    12
 
 WEB-002_AC-12 Handpicked Highlights
-    [Documentation]    "Handpicked highlights" shows the three highest prices, highest first.
-    [Tags]    broken
+    [Documentation]    "Handpicked highlights" shows the three most expensive products, highest price first.
     @{catalogue}=    Get Catalogue From API
-    ${expected}=    Evaluate    [str(p) for p in sorted((float(x["price"]) for x in $catalogue), reverse=True)[:3]]
+    @{top}=    Evaluate    sorted($catalogue, key=lambda product: product["price"], reverse=True)[:3]
     Go To Catalogue
-    ${shown}=    Get Highlight Prices
-    Should Be True    $shown == $expected
-    ...    msg=The highlights should show the three highest prices, highest first.
+    @{names}=    Get Highlight Names
+    @{prices}=    Get Highlight Prices
+    Length Should Be    ${names}    3
+    FOR    ${product}    ${name}    ${price}    IN ZIP    ${top}    ${names}    ${prices}
+        Should Be Equal    ${name}    ${product}[name]
+        ...    msg=The highlights should show the three most expensive products, highest price first.
+        ${expected}=    Format Price    ${product}[price]
+        Should Be Equal    ${price}    ${expected}    msg=${name} should cost ${expected}.
+    END
```

## Why it is a good result

- **The answers came from the project:** `robotcode discover` for the tests and tags, `robotcode libdoc` for the
  keyword and its arguments, not a search of the files or the model's memory.
- **The cause was read at a breakpoint,** from the values the assertion compares, before anything changed.
- **The repaired test checks what the criterion says:** the three most expensive products, highest price first, by
  name, with their prices as the shop shows them. The `broken` tag is gone.
- **The REPL explored the price range,** which no test covers yet, and was not used for the failing test.

## What to debrief

- **The cause of `WEB-002_AC-12 Handpicked Highlights`.** At a breakpoint on its assertion, the debugger shows
  `@{expected} = ['899.0', '799.0', '389.0']` beside `@{shown} = ['$899.00', '$799.00', '$389.00']`. The expected
  values come from the API as unformatted numbers. The failure message says only that the highlights are wrong.
- **The REPL misfire.** An agent that opens the REPL to investigate the failing test rebuilds what the test already
  does, without its setup. The debugger runs the real test.

## Compare yours

```bash
git fetch upstream solutions
REF=$(git log -1 --format=%H --grep '^lab-04-robotcode' upstream/solutions)
git diff "$REF" -- tests/ui/catalogue.robot resources/catalogue.resource AGENTS.md
```

The lines marked `-` are the reference's, the lines marked `+` yours. No `upstream` remote yet? [Add it first](README.md#compare-your-files-with-the-reference).
