# Lab 3 - Skills: the reference

[Lab 3](../labs/lab-03-skills/INSTRUCTIONS.md) installs the Robot Framework Agent Skills into the repository, and has
you turn the template into a skill for one convention of `docs/conventions.md`. The rehearsal chose convention 2,
"Locators live in resources". [Transcript](../transcripts/lab-03-skills.md).

## The reference

**Installed** into `.claude/skills/`: `appium`, `keyword-builder`, `libdoc-explain`, `libdoc-search`, `platynui`,
`requests`, `resource-architect`, `restinstance`, `selenium` and `testcase-builder`. Codex keeps them in
`.agents/skills/`, GitHub Copilot in `.github/skills/`.

**Written:** `.claude/skills/locators-in-resources/SKILL.md`:

````markdown
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
````

It bundles `scripts/check.py`, which parses test files with Robot Framework's own parser and reports every argument
that looks like a locator. [Read it on GitHub](https://github.com/manykarim/ai-engineering-robotframework/blob/solutions/.claude/skills/locators-in-resources/scripts/check.py).

## Why it is a good result

- **The description says what the skill checks and when to use it,** in the words a prompt contains: writing,
  changing or reviewing tests, deciding where a locator belongs. That decides whether it loads.
- **The name matches the folder,** and the template's comment is gone.
- **Rule, reason and examples are the convention's own,** with both verdicts, including the tricky cases: a locator
  a test builds from a resource variable, and data that only looks like a locator.
- **The script does the mechanical part,** and the skill tells the agent what a script cannot see.

## What to debrief

- **Whether it triggers.** The review prompt, *Review tests/ui/catalogue.robot against the conventions of this
  repository*, loaded the skill. The unrelated one, *What does `uv run --no-sync python -m shop reset` do?*, did not.
- **What the review finds.** One locator written in a test file: `WEB-002_AC-10 Reset Filters` clicks
  `role=link[name="Reset"]` directly. It is the suite's only inline locator, and Lab 7 moves it into a keyword.

## Compare yours

```bash
git fetch upstream solutions
REF=$(git log -1 --format=%H --grep '^lab-03-skills' upstream/solutions)
git diff "$REF" -- .claude/skills/locators-in-resources
```

The lines marked `-` are the reference's, the lines marked `+` yours. No `upstream` remote yet? [Add it first](README.md#compare-your-files-with-the-reference).

If your skill is for another convention, it has another folder: compare its parts with the reference instead.
