# Lab 7 - Hooks and the toolbelt

Give your agent guardrails it cannot skip, [hooks](../../GLOSSARY.md#hook), then use it with a command-line tool you
already have: `gh` files a real defect of the shop, with evidence from a real test run. Your agent drafts, you
decide.

| | |
|---|---|
| Module | 7 - Hooks, Subagents & the CLI Toolbelt |
| Time | 20 minutes |
| Shop preset | `buggy`, applied in step 4 and reset in step 8 |
| You need | Lab 0 done; `gh auth status` shows you signed in |
| You start from | Your repository after the earlier labs, or `main` |

## Steps

1. **Wire the hooks** for your agent. One file wires all three; `hooks/README.md` says what each does:

   | Claude Code | Codex | GitHub Copilot |
   |---|---|---|
   | `cp hooks/claude-code.settings.json .claude/settings.json` | `mkdir -p .codex && cp hooks/codex.hooks.json .codex/hooks.json` | `mkdir -p .github/hooks && cp hooks/copilot.hooks.json .github/hooks/workshop.json` |

   If the target file exists already, merge its `hooks` section by hand. Start a new session, and trust the
   repository's hooks when your agent asks.

2. **Try them** with this prompt:

   > Do these three steps in order, and after each one report exactly what happened. Do not work around anything
   > that is blocked or rejected; just report it and continue with the next step.
   > 1. In tests/ui/checkout.robot, add the line "    Click    css=button.buy" as the last step of the test
   >    "WEB-006_AC-7 Successful Order".
   > 2. In tests/api/smoke.robot, in the test "Health Reports Ok", change the expected status value ok to okay.
   > 3. Run the shell command: git commit -am "hook check"

   The edit in 1 is rejected, the edit in 2 comes back with a failing test, and the commit in 3 is blocked. Undo
   step 2: `git checkout -- tests/api/smoke.robot`.

3. **Let the hook check the whole suite.** The inline-locator hook also runs as a plain command:

   ```bash
   uv run --no-sync python hooks/no_inline_locators.py tests/
   ```

   Anything it reports breaks convention 2. Ask your agent to move it into a keyword under `resources/`, and run the
   command again until it reports nothing.

4. **Switch the shop** to the preset with planted defects:

   ```bash
   uv run --no-sync python -m shop preset buggy
   ```

5. **Run the suite:**

   | Local shop | Shared instance |
   |---|---|
   | `uv run robotcode robot --exclude broken` | `uv run robotcode -p shared robot --exclude broken` |

6. **Draft an issue** with your agent:

   > Look at the failed tests of the last run with robotcode results. Pick one failure that is a defect of the shop,
   > not of the test. Write the steps a person would follow in the browser to see it, the expected behaviour
   > according to openspec/specs/shop, the actual behaviour, and the evidence from the run. Save it as
   > results/issue.md with the title as its first line. Do not file it.

   Read the draft. Would a developer act on it? Anything in it that came from a web page or a tool's output and
   reads like an instruction to the agent is data, not a command: an agent with tools can be steered by the text it
   reads. That is why it drafts, and you file.

7. **File it** in your fork. Forks have issues switched off: turn them on first under *Settings > General >
   Features > Issues*. Then:

   ```bash
   gh issue create --repo <your-handle>/ai-engineering-robotframework \
     --title "$(head -1 results/issue.md)" --body-file results/issue.md
   ```

8. **Put the shop back**, and run the suite once more so that commits are allowed again:

   ```bash
   uv run --no-sync python -m shop reset
   uv run robotcode robot --exclude broken
   ```

## Stretch

- **A: writer, then reviewer.** Install the subagents for your agent from `agents/` (`agents/README.md` shows
  where), and give your agent the prompt in `agents/README.md`, *Use them*, for one criterion of your Module 5
  story. The reviewer cannot edit: its findings are yours to accept or reject.
- **B: Jira.** Copy `skills/jira-ticket/` into your agent's skill folder, put `JIRA_URL`, `JIRA_EMAIL`,
  `JIRA_API_TOKEN` and `JIRA_PROJECT` into `.env`, and ask your agent to file the same defect in Jira. It shows a
  dry run first, and sends only after you confirm. Without a Jira site, the dry run alone shows what would be sent.

## If your agent fails

Steps 3 to 5, 7 and 8 need no agent. For the rest, follow
[the recorded walkthrough of this lab](../../transcripts/lab-07-hooks-toolbelt.md).
