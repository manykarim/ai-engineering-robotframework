---
name: locators-in-resources
description: Checks that Robot Framework test files in this repository contain keyword calls only, and that every locator (role=, text=, CSS or XPath selectors, >> chains) is written in a keyword under resources/, never in a .robot test file. Use when writing, changing or reviewing test cases in .robot files, when deciding where a locator or a new keyword belongs, or when asked whether tests follow the conventions of this repository.
---

# Locators live in resources

## The rule

Test files call keywords. Every locator is written inside a keyword under `resources/`:

```robotframework
*** Test Cases ***
WEB-002_AC-7 Audio Filter Shows Only Audio
    Go To Catalogue
    Check Category    Audio
```

The test passes data, such as a category, a product name or an email address. The keyword in
`resources/catalogue.resource` turns it into the locator. A test file has no locator anywhere: not in a test case, not
in its own `*** Variables ***` section and not in its own `*** Keywords ***` section.

## Why

When the page changes, there is exactly one place to fix, and a test reads as behaviour rather than markup.

## How to apply it

- When you write a test, call keywords from the resources under `resources/`. When the element you need has no keyword
  yet, add one to the resource for that page, never to `resources/legacy.resource`, and call it from the test.
- When you review a test file, and before you finish writing or changing one, run the bundled script from the
  repository root. It reads the files the way Robot Framework does and reports every argument that looks like a
  locator:

  ```bash
  uv run --no-sync python .claude/skills/locators-in-resources/scripts/check.py tests/
  ```

  It prints `<file>:<line>: '<argument>' is a locator` for each finding and exits with status 1, or prints nothing
  and exits with 0. It follows the resources a file imports, so it also reports a test that passes a resource
  variable holding a locator, such as `${GRID}`, and names the resource.
- The script matches patterns, so read every argument of every call as well, and list each one that is a locator,
  with its file and line. A locator is a selector for the page: a `role=`, `text=`, `css=`, `xpath=` or `id=`
  selector, a `>>` chain, CSS such as `#email`, `.product-grid`, `[name="email"]` or `:has-text(...)`, or XPath such
  as `//button`. A locator that a test builds from a resource variable, such as `${GRID} >> article`, counts too.
- Data is not a locator: product names, labels and values a keyword turns into a locator, URL paths and expected
  values. When the script reports data, such as a keyword's named argument `text=Hello`, say so instead of moving it.
- To fix a finding, move the locator into a keyword in the page's resource and call that keyword from the test.

## Examples

| In a test file | Verdict |
|---|---|
| `Check Category    Audio` | follows the rule: the keyword builds the locator |
| `Fill Checkout Form    test@example.com    Test User    123 Test Street, City` | follows the rule: every argument is data |
| `Click    role=button[name="Apply filters"]` | breaks it: a locator literal in a test |
| `Fill Text    form[action="/checkout"] >> role=textbox[name="Email"]    test@example.com` | breaks it: a locator literal in a test |
| `${count}=    Get Element Count    ${GRID} >> article` | breaks it: the test builds a locator from a resource variable |
| `${EMAIL FIELD}    [name="email"]` in the file's `*** Variables ***` | breaks it: the locator belongs in a resource |
