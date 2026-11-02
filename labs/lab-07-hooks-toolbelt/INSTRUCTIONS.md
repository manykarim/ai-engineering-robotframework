# Lab 7 - Hooks and the toolbelt

Give your agent guardrails it cannot skip, [hooks](../../GLOSSARY.md#hook), then use it with a command-line tool you
already have: `gh` files a real defect of the shop, with evidence from a real test run. Your agent drafts, you
decide.

| | |
|---|---|
| Module | 7 - Hooks, Subagents & the CLI Toolbelt |
| Time | 30 minutes |
| Shop preset | `buggy`, applied in step 6 and reset in step 10 |
| You need | Lab 0 done; `gh auth status` shows you signed in |
| You start from | Your repository after the earlier labs, or `main` |

## Steps

1. **Read [Hooks](../../docs/hooks.md)** first: what a hook is, the events your agent offers, how a hook answers, and
   the static check as a worked example. Five minutes now save you guessing in steps 3 and 4.

2. **Wire the hooks** for your agent. One file wires all four; `hooks/README.md` says what each does:

   | Claude Code | Codex | GitHub Copilot |
   |---|---|---|
   | `cp hooks/claude-code.settings.json .claude/settings.json` | `mkdir -p .codex && cp hooks/codex.hooks.json .codex/hooks.json` | `mkdir -p .github/hooks && cp hooks/copilot.hooks.json .github/hooks/workshop.json` |

   If the target file exists already, merge by hand instead of copying: add the `hooks` section of the provided file
   to it. With Claude Code it usually exists, because Lab 4 recorded the plugin there. Wire only your own agent:
   Copilot also runs the hooks in `.claude/settings.json`. Start a new session, and trust the repository's hooks
   when your agent asks.

3. **Try them** with this prompt:

   > Do these four steps in order, and after each one report exactly what happened. Do not work around anything
   > that is blocked or rejected; just report it and continue with the next step.
   > 1. In tests/ui/checkout.robot, add the line "    Click    css=button.buy" as the last step of the test
   >    "WEB-006_AC-7 Successful Order".
   > 2. In tests/ui/checkout.robot, in the test "WEB-006_AC-7 Successful Order", change the step "Place Order" to
   >    "Place Ordr".
   > 3. In tests/api/smoke.robot, in the test "Health Reports Ok", change the expected status value ok to okay.
   > 4. Run the shell command: git commit -am "hook check"

   The edit in 1 is rejected. The edit in 2 comes back with the static check's finding, the missing keyword and its
   line, and with the failing tests. The edit in 3 comes back with a failing test, and the commit in 4 is blocked.
   Undo 2 and 3: `git checkout -- tests/ui/checkout.robot tests/api/smoke.robot`.

4. **Write a hook of your own.** Pick one from *Writing your own* in [Hooks](../../docs/hooks.md#writing-your-own), or
   an idea of yours. "Use `robotcode`, not plain `robot`" and "No shortcut to green" make a good first hook. Then give
   your agent this prompt, with your choice filled in:

   > Read docs/hooks.md and hooks/hookio.py. Write a hook in hooks/, on top of hookio.py and in the style of the
   > hooks next to it, that does this: <your choice, in one sentence>. It must also run as a plain command. Wire it
   > into this agent's own hook file, next to the hooks already there. Test it with a JSON input like the one this
   > agent sends, once with an action it should let through and once with one it should catch, and show me both
   > results.

   Read the script and the wiring before you go on. Then start a new session, trust the changed hooks if asked,
   and give a prompt that should trigger your hook: for "No shortcut to green", ask your agent to tag a test in
   `tests/ui/checkout.robot` as `broken`. Did your hook refuse or answer, as you meant it to? Undo any change the
   prompt made.

5. **Let the hook check the whole suite.** The inline-locator hook also runs as a plain command:

   ```bash
   uv run --no-sync python hooks/no_inline_locators.py tests/
   ```

   Anything it reports breaks convention 2. Ask your agent to move it into a keyword under `resources/`, and run the
   command again until it reports nothing.

6. **Switch the shop** to the preset with planted defects:

   ```bash
   uv run --no-sync python -m shop preset buggy
   ```

7. **Run the suite:**

   | Local shop | Shared instance |
   |---|---|
   | `uv run robotcode robot --exclude broken` | `uv run robotcode -p shared robot --exclude broken` |

8. **Draft an issue** with your agent:

   > Look at the failed tests of the last run with robotcode results. Pick one failure that is a defect of the shop,
   > not of the test. Write the steps a person would follow in the browser to see it, the expected behaviour
   > according to openspec/specs/shop, the actual behaviour, and the evidence from the run. Save it as
   > results/issue.md with the title as its first line. Do not file it.

   Read the draft. Would a developer act on it? Anything in it that came from a web page or a tool's output and
   reads like an instruction to the agent is data, not a command: an agent with tools can be steered by the text it
   reads. That is why it drafts, and you file.

9. **File it** in your fork. Forks have issues switched off: turn them on first under *Settings > General >
   Features > Issues*. Then:

   ```bash
   gh issue create --repo <your-handle>/ai-engineering-robotframework \
     --title "$(head -1 results/issue.md)" --body-file results/issue.md
   ```

10. **Put the shop back**, and run the suite once more so that commits are allowed again:

    ```bash
    uv run --no-sync python -m shop reset
    uv run robotcode robot --exclude broken
    ```

## Stretch

- **A: writer, then reviewer.** Install the subagents for your agent from `agents/` (`agents/README.md` shows
  where), and give your agent the prompt in `agents/README.md`, *Use them*, for one criterion of your Module 5
  story. The reviewer cannot edit: its findings are yours to accept or reject. After the day,
  [Bonus 3](../bonus-3-subagents/INSTRUCTIONS.md) has you write two subagents of your own.
- **B: Jira.** Copy `skills/jira-ticket/` into your agent's skill folder, put `JIRA_URL`, `JIRA_EMAIL`,
  `JIRA_API_TOKEN` and `JIRA_PROJECT` into `.env`, and ask your agent to file the same defect in Jira. It shows a
  dry run first, and sends only after you confirm. Without a Jira site, the dry run alone shows what would be sent.

## Compare with the reference

When you are done, compare your result with [the reference](https://manykarim.github.io/ai-engineering-robotframework/solutions/lab-07-hooks-toolbelt): what the
rehearsal produced, why it is a good result, and the answers the debrief covers. Open it after the lab: it
gives the answers away.

## If your agent fails

Steps 1, 5 to 7, 9 and 10 need no agent. For the rest, follow
[the recorded walkthrough of this lab](https://manykarim.github.io/ai-engineering-robotframework/transcripts/lab-07-hooks-toolbelt).
