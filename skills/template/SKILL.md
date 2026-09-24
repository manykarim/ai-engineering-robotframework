---
name: criterion-id-first
description: Checks that Robot Framework test names in this repository start with the story criterion they verify (<STORY>_<AC>, for example WEB-006_AC-1) or carry the smoke tag. Use when writing, renaming or reviewing test cases in .robot files, or when asked whether tests follow the naming convention.
---

# Criterion ID first

<!--
  This is the template for Lab 3. It is a complete, working skill for convention 1 of docs/conventions.md.
  To make your own skill:
    1. Copy this folder into your agent's skill folder and rename it: .claude/skills/<name>/ (Claude Code),
       .agents/skills/<name>/ (Codex) or .github/skills/<name>/ (GitHub Copilot).
    2. Change `name` above to the folder's name.
    3. Rewrite `description`. The agent decides from the description alone whether to load the skill, so say
       what the skill does AND when to use it, with the words a prompt would contain.
    4. Replace the rule, the reason and the examples below with your convention.
  Delete this comment when you are done.
-->

## The rule

Every test case that verifies a story criterion starts its name with the criterion's ID, `<STORY>_<AC>`, followed by a
space and a short description of the behaviour:

```robotframework
WEB-006_AC-1 Order Total Adds Up
```

When one criterion needs several tests, they share the prefix. A test that verifies no criterion carries the `smoke`
tag instead of an ID.

## Why

A failing test then names the requirement it protects, and every result traces back to its criterion in
`openspec/specs/shop/`.

## How to apply it

- When you write a test, look up the criterion in `openspec/specs/shop/` and start the name with its ID.
- When you review tests, list every test whose name does not start with an ID and that has no `smoke` tag.
- Check your work with the bundled script, which reads the test files the way Robot Framework does:

  ```bash
  uv run --no-sync python <this skill's folder>/scripts/check.py tests/
  ```

  It prints each test that breaks the rule and exits with status 1, or prints nothing and exits with 0.

## Examples

| Test name | Verdict |
|---|---|
| `WEB-002_AC-7 Audio Filter Shows Only Audio` | follows the rule |
| `Health Reports Ok`, tagged `smoke` | follows the rule |
| `Audio Filter Works` | breaks it: no criterion ID and no `smoke` tag |
| `AC-7 Audio Filter` | breaks it: the story is missing |
