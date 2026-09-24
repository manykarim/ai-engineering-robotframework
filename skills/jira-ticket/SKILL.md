---
name: jira-ticket
description: Files a bug report in Jira Cloud from a real Robot Framework run, with reproduction steps, expected and actual result, and the environment. Use when asked to file, open, create or report a Jira issue or ticket for a failing test or a defect found by the test suite.
---

# File a Jira bug from a test run

The stretch goal B of Lab 7. It turns a failing test into a Jira issue a developer can act on. **Agents draft, humans
decide**: you always show the issue to the person before anything is sent.

## Settings

The script reads four settings from the environment or from `.env`. Never read `.env` yourself, and never print or
repeat a value from it.

| Setting | Example |
|---|---|
| `JIRA_URL` | `https://your-site.atlassian.net` |
| `JIRA_EMAIL` | the Atlassian account's email |
| `JIRA_API_TOKEN` | an API token from id.atlassian.com, **never** a password |
| `JIRA_PROJECT` | the project key, for example `SHOP` |

Without all four, the script runs as a dry run: it prints the issue it would file and names the missing settings.

## Steps

1. **Collect the evidence from the run**, not from memory:

   ```bash
   uv run robotcode results
   ```

   Note the failing test, its message, and the story criterion in its name (`WEB-006_AC-1` means
   `openspec/specs/shop/checkout`, criterion AC-1).
2. **Find the expected behaviour** in the criterion's requirement under `openspec/specs/shop/`.
3. **Note the environment**: the shop URL, the space if there is one, and the preset (`uv run --no-sync python -m shop status`).
4. **Write the issue body** to a Markdown file, for example `results/issue.md`, with these sections: *Steps to
   reproduce* (numbered, as a person would do them in the browser), *Expected*, *Actual*, *Evidence* (the failing
   test and its message), *Environment*.
5. **Dry run**, and show the output to the person:

   ```bash
   uv run --no-sync python <this skill's folder>/scripts/file_issue.py --summary "<one line>" --body-file results/issue.md
   ```

6. **Send only after the person confirms**, by repeating the command with `--send`. Report the issue key and link it
   prints.

## Rules

- One defect per issue. Two failing tests with one cause are one issue; say so in the body.
- The summary states the wrong behaviour, not the test: "Cart badge stays at 0 after adding a product" rather than
  "WEB-005_AC-2 fails".
- Never put a credential, a token, a `.env` value or a local path into the issue.
