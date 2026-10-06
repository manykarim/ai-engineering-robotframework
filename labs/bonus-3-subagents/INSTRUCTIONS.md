# Bonus 3 - Subagents

Write two [subagents](../../GLOSSARY.md#subagent) of your own, and hand them the work:
- a **debugger** that stops a failing test at its failure, finds the cause on the live page, and repairs the test,
  or reports a defect of the shop;
- an **analyzer** that checks the suite without running it, with RobotCode and Robocop, and changes files only
  through Robocop.

Your agent delegates, each subagent works in a context of its own and sends back a report, and you decide what
stays. The lab builds on Lab 4, which covers the debugger and the REPL, and on Lab 7, which covers subagents. Keep
[the RobotCode cheat sheet](../../docs/robotcode.md) open.

| | |
|---|---|
| Module | Bonus 3 - Subagents for debugging and analysis |
| Time | about 60 minutes, self-paced |
| Shop preset | `drift_and_bug`, applied in step 5 and reset in step 7 |
| You need | Lab 0 done; a coding agent that loads subagents from the project, as Lab 7's stretch goal A describes |
| You start from | Your clone after the day, on a new branch. Step 1 puts the suite back the way `main` ships it |

## Steps

1. **Start a branch, and put the suite back.** The labs of the day changed tests and resources. This lab needs
   them the way `main` ships them, so that you meet the same failures as the reference. Your `AGENTS.md`, the
   RobotCode plugin and your hooks stay as they are.

   ```bash
   git switch -c bonus-3
   git remote add upstream https://github.com/manykarim/ai-engineering-robotframework.git   # skip if Lab 5 added it
   git fetch upstream main
   git restore --source upstream/main --staged --worktree tests resources
   git diff upstream/main --stat -- tests resources
   ```

   The last command prints nothing. Test files you committed during the day are gone from this branch only. If
   `git status` still lists files under `tests/` as untracked (`??`), you never committed them: move them out of
   `tests/` for this lab.

2. **Look at an example.** Open your agent's `runner` from `agents/`: `agents/claude-code/runner.md`,
   `agents/codex/runner.toml` or `agents/copilot/runner.agent.md`. A subagent has three parts:
   - a **description**, which tells the main agent when to hand it work;
   - its **tools**, which say what it can do;
   - its **instructions**.

   The *Install* table of `agents/README.md` says which folder your agent loads subagents from.

3. **Write the debugger.** Give your agent this prompt:

   > Write a subagent named debugger, for the coding agent you are. Use the format of your agent's runner in
   > agents/, save it in the folder that the Install table of agents/README.md names for your agent, and show me
   > the file before you save it.
   >
   > Its description: it debugs one failing Robot Framework test per request at a live breakpoint, and either
   > repairs the test or reports a defect of the shop.
   >
   > Its tools: read, search, run commands and edit files.
   >
   > Its instructions:
   > - Before you change anything, read docs/robotcode.md, docs/conventions.md and the test's criterion in
   >   openspec/specs/shop/.
   > - Read the recorded failure first, with uv run robotcode results show --failed.
   > - Stop the test at its failure with uv run robotcode robot-debug --plain -t "<test>", and inspect the live
   >   state there: .where, .vars, .print, and keywords run on the paused page. If you can keep the session open
   >   between your steps, drive it interactively. Otherwise drive it in piped rounds: choose each round's commands
   >   from the last round's output, and end each round with .continue or .abort. Never wait at a prompt.
   > - Try a fix before you write it into a file: at the paused prompt, or on a fresh page in
   >   uv run robotcode repl --plain.
   > - Repair a test only so that it verifies what its criterion says, with locators from the stable contract, in
   >   resources/. Never change an expected value, an assertion or a tag so that a test passes. When the shop
   >   contradicts its specification, leave the test failing and report the defect with your evidence.
   > - Run the test again after a change, with uv run robotcode robot -t "<test>". With the shared instance, put
   >   -p shared before robot, robot-debug and repl.
   > - End with a report: the cause, the evidence, the change as a diff, and the test's result.

   Read the file it shows you. Is the description specific enough that the main agent picks this subagent, and
   only for this job?

4. **Write the analyzer:**

   > Write a second subagent named analyzer, the same way.
   >
   > Its description: it checks Robot Framework tests and resources without running them, with RobotCode and
   > Robocop, and changes files only through Robocop.
   >
   > Its tools: read, search and run commands. Give it no tool that edits files, if your agent lets you leave one
   > out.
   >
   > Its instructions:
   > - Run uv run robotcode analyze code and uv run robocop check on the paths you are given.
   > - Sort every finding into fix, keep or false positive, each with its reason. Read the line before you call a
   >   finding a false positive.
   > - Change files only through Robocop: uv run robocop format --select <formatter>, or uv run robocop check --fix.
   >   Run each first with --diff --no-overwrite (for check: --diff), show me the diff, and write only after I
   >   agree. Never edit a file by hand: report what Robocop cannot change as a finding.
   > - After a change, run uv run robotcode robot --exclude broken, and compare the result with the run before.
   > - End with a report: the findings with their verdicts, what changed, and the suite's result.

   Then start a new session, so that your agent loads both:

   | Claude Code | Codex | GitHub Copilot |
   |---|---|---|
   | `/agents` lists them | starts one when you ask for it by name | `/agent` lists them |
   | the analyzer gets `Read, Grep, Glob, Bash`: it has no edit tool | limits a subagent only through its sandbox, and Robocop must write files: the analyzer's rule against hand edits lives in its instructions | the analyzer gets `read`, `search` and `execute`: it has no edit tool |

5. **Let the layout drift, and run the suite:**

   ```bash
   uv run --no-sync python -m shop preset drift_and_bug
   ```

   | Local shop | Shared instance |
   |---|---|
   | `uv run robotcode robot --exclude broken` | `uv run robotcode -p shared robot --exclude broken` |

   Four tests fail. `uv run robotcode results show --failed` lists them.

6. **Hand them to the debugger, one at a time:**

   > Use the debugger subagent on each failed test of the last run: one test per call, one after the other. After
   > each call, show me its report in a few lines. Do not commit anything.

   One test at a time, because tests share keywords: two debuggers at once would edit the same file. Read each
   report, then the change:

   ```bash
   git diff -- tests resources
   ```

   - Which tests did it repair, and which did it report as a defect of the shop? Does the evidence hold up against
     the specification?
   - Did any change touch an expected value, an assertion or a tag? If one did, undo it.
   - Compare this conversation with Lab 4's. There, the debug session filled the main conversation. Here, the
     main conversation holds four reports.

7. **Check the repairs in both layouts**, then put the shop back:

   ```bash
   uv run robotcode robot --exclude broken
   uv run --no-sync python -m shop reset
   uv run robotcode robot --exclude broken
   ```

   With the shared instance, add `-p shared` as in step 5. Under `drift_and_bug`, the tests the debugger repaired
   pass, and the ones it reported still fail. Under `clean`, all of them pass: the defects were the shop's.

8. **Let the analyzer report**, and change nothing yet:

   > Use the analyzer subagent on tests/ and resources/. Report every finding with its verdict, and change
   > nothing.

   Do you agree with each verdict? For a false positive, the cheat sheet's *Traps* may say why.

9. **Convert the old variable syntax to `VAR`:**

   > Use the analyzer subagent to convert the old variable syntax in tests/ and resources/ to VAR, with Robocop.
   > Show me the diff before it writes anything.

   Robocop's `ReplaceWithVAR` formatter does the conversion. Afterwards:

   ```bash
   uv run robocop check --select replace-set-variable-with-var --select replace-create-with-var tests resources
   uv run robotcode robot --exclude broken
   ```

   Robocop reports no issues, and the suite has the same result as at the end of step 7. Give each rule its own
   `--select`: a comma-separated list matches no rule, and Robocop then reports no issues either.

10. **Ask the analyzer for something only a hand edit can do:**

    > Use the analyzer subagent to add a [Documentation] line to the keyword "Cart Should Say It Is Empty" in
    > resources/checkout.resource.

    It leaves the file unchanged, and reports the change as a finding. Removing the edit tool does not stop every
    command from writing a file. A guardrail that holds is a hook, as in Lab 7.

    Keep what you agree with, on your `bonus-3` branch.

## Stretch

Give your team's rules to Robocop. Ask the analyzer to write a documented configuration with
`uv run robocop config init`, and to tell you which rules this suite should switch off, each with a reason. Then
edit `robocop.toml` yourself: the analyzer cannot. Run `uv run robocop check tests resources` again, and compare.

## Compare with the reference

When you are done, compare your result with [the reference](https://manykarim.github.io/ai-engineering-robotframework/solutions/bonus-3-subagents): what the
rehearsal produced, why it is a good result, and the answers the debrief covers. Open it after the lab: it
gives the answers away.

## If your agent fails

Steps 1, 5 and 7 need no agent. For the rest, follow
[the recorded walkthrough of this lab](https://manykarim.github.io/ai-engineering-robotframework/transcripts/bonus-3-subagents).
