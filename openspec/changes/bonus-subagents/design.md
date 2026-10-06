## Context

See proposal.md for why. The facts this design builds on, checked on `main` at a16535d with the pinned stack:

- **RobotCode 2.7.0:**
  - `robot-debug` takes `robotcode robot`'s options, pauses at the first uncaught failure by default, and reads line by line with `--plain`.
  - `repl` keeps a browser and its variables alive for one session.
  - `analyze code` reports errors, warnings, information and hints. Its exit code combines their bits.
  - `tests/` has no `__init__.robot`, so `-t "<test>"` keeps each file's suite setup, as the cheat sheet's examples do.
- **`robotcode analyze code tests resources`** reports 8 files and one error: `VariableNotFound` for `${HEADLESS}` in `resources/shop.resource`. It is a false positive. The keyword reads the variable with `Get Variable Value` and a default, on purpose: the cheat sheet's trap table says why.
- **Robocop 9.0.0** comes into the locked environment through `robotcode[all]`, and `uv.lock` records it. It is not a direct dependency.
  - `robocop check tests resources` reports 22 findings: DOC01 9, DEPR06 6, IMP01 4, DOC02 2, SPC15 1.
  - DEPR06 (`replace-create-with-var`) and DEPR05 (`replace-set-variable-with-var`) are not marked fixable. `main` has no DEPR05 finding.
  - The formatter `ReplaceWithVAR` is off by default. `robocop format --select ReplaceWithVAR --diff --no-overwrite tests resources` shows seven conversions in five files: the six DEPR06 findings and one `Catenate`.
  - Robot Framework 7.5 runs the `VAR    &{name}=    &{EMPTY}` form the formatter writes. This was checked in a scratch suite.
  - Robocop caches into `.robocop_cache/`, which git already ignores.
- **Under `drift_and_bug`, with `broken` excluded,** four tests fail. Two fail only on drift. Two fail on drift and then on a defect of the shop. The answer sheet on `solutions` names them, and this design does not. Two of the four share one legacy keyword. `tools/verify_outcomes.py` checks these outcomes against the pinned shop.
- **Subagent formats,** from `agents/`:
  - Claude Code: `.claude/agents/<name>.md`, with `tools:`.
  - Codex: `.codex/agents/<name>.toml`, with `sandbox_mode`. Codex limits a subagent through its sandbox alone: `read-only` would stop Robocop from writing as well.
  - GitHub Copilot: `.github/agents/<name>.agent.md`, with `tools: [...]`.
- **Driving the debugger:**
  - The RobotCode plugin's debugging reference prefers driving the debugger interactively, when the agent can keep a terminal open between its steps.
  - The cheat sheet documents the piped form, in which every command finishes.
  - Claude Code's shell commands run to completion.
- **A participant's suite after the day differs from `main`'s.** Labs 4 and 5 repair the two broken tests, Lab 7 moves the inline locator, and Lab 8's stretch goal repairs one drifted test.
- **The site and the contract:**
  - The site's sidebar makes a *Bonus* category of every `labs/bonus-*` folder.
  - `tools/check_labs.py` ties each bonus folder to a label, its estimated minutes and its preset, in its `BONUS` table.

## Goals / Non-Goals

**Goals:**
- A participant writes two subagents of their own, from a brief, and sees what a subagent changes: its own context, its own tools, and a report instead of a transcript in the main conversation.
- The debugger shows the difference between repairing a test and hiding a defect.
- The analyzer changes files only through a deterministic tool, and the participant sees the diff first.
- Nothing about the day changes except one sentence in Lab 7's stretch goal.

**Non-Goals:**
- Changing `agents/`, its three subagents, or Lab 7's own steps.
- A Robocop configuration on `main`. Robocop runs with its defaults, and a team's own configuration is the stretch goal.
- Making the suite clean of Robocop's findings on `main`. The suite is lab material, and the lab works on its findings.
- Changing `setup-check`, `uv.lock` or the timetable.
- Rehearsing with a second agent.

## Decisions

### D1. Folder, header and contract

| | Bonus 3 |
|---|---|
| lab folder | `labs/bonus-3-subagents/` |
| header *Module* | `Bonus 3 - Subagents for debugging and analysis` |
| header *Time* | `about 60 minutes, self-paced`, corrected from the rehearsal |
| preset | `drift_and_bug`, applied in one step and reset in a later one |
| subagent names | `debugger`, `analyzer` |

- `tools/check_labs.py` gets a `BONUS` row: `"bonus-3-subagents": ("Bonus 3", 60, "drift_and_bug")`.
- `labs/README.md` adds the row to its Bonus table. Its intro sentence changes: Bonus 1 and 2 follow the building guide, and Bonus 3 builds on Labs 4 and 7.
- The names do not collide with `writer`, `reviewer` or `runner`, so both sets can be installed at once.

### D2. Participants write the subagents, from a brief

The lab quotes one prompt per subagent. Each holds the brief:
- what the subagent does;
- what it must never do;
- which tools it gets;
- what its report contains.

It also names the example to imitate, `agents/<agent>/runner.*`, and asks the agent to show the file before saving it. The *Install* table of `agents/README.md` says where each agent loads subagents from, and the lab links it instead of repeating it.

*Alternative:* shipping both subagents in `agents/`. Rejected: writing the description, the limits and the report is the lesson.

### D3. The starting state

Participants work in their own clone, on a new branch. One step takes the suite back to the workshop's `main`, with the `upstream` remote that Lab 5's step 0 adds:

```bash
git switch -c bonus-3
git fetch upstream main
git checkout upstream/main -- tests resources
```

- Their `AGENTS.md`, the RobotCode plugin and Lab 7's hooks stay.
- Everyone meets the same four failures, and the reference patch applies to what they have.

*Alternatives:*
- A branch from `upstream/main` alone. Rejected: it drops the context files and the plugin the participant built.
- The suite as the participant left it. Rejected: the failures would differ from person to person, and from the reference.

### D4. The debugger's failures come from `drift_and_bug`

Its outcomes are verified, and they mix the two cases the debugger must tell apart: a test to repair, and a defect to report.

*Alternatives:*
- `stage2`: drift only, so there is no defect to report.
- `buggy`: defects only, so there is nothing to repair.
- `stage3` followed by `buggy`: an unverified composition.
- The two broken tests: Labs 4 and 5 use them.

One of the four tests is the one in Lab 8's stretch goal. That lab repairs it in the main conversation, and Bonus 3 hands all four to a subagent.

### D5. One test per call, in sequence

The main agent hands the `debugger` one failed test at a time.
- Tests share resource keywords, so subagents running in parallel would edit the same file.
- A repair can fix a second test. The `debugger` then finds that test passing, which the debrief uses: the report says so, and nothing more is changed.
- The main conversation receives four short reports, not four debug sessions. The lab has the participant compare that with Lab 4, where the session itself sits in the main conversation.

### D6. How the debugger drives RobotCode

The brief tells it:
1. Read the recorded failure with `robotcode results show --failed`.
2. Run `uv run robotcode robot-debug --plain -t "<test>"`, which stops at the failure. Inspect there with `.where`, `.vars`, `.print`, and keywords on the paused page.
3. Drive the session interactively if the agent can keep it open between steps. Otherwise, drive it in piped rounds: each round's commands are chosen from the last round's output, and each round ends with `.continue` or `.abort`. Never wait at a prompt.
4. Try the candidate fix at the paused prompt before writing it.
5. Read `docs/robotcode.md`, `docs/conventions.md` and the test's criterion in `openspec/specs/shop/` before changing anything.
6. Repair in `resources/`, onto the stable contract.
7. Check a keyword it wrote on its own in `uv run robotcode repl --plain`: import the resource, open the page with `resources/shop.resource`, and run the keyword. Then run the test again.

Each tool has its own job:
- the paused prompt tries a fix in the test's own context;
- the REPL proves that the keyword in the file works by itself, before the test runs again.

A first rehearsal offered the REPL only as an alternative to the paused prompt. The debugger then never used it, because the paused prompt was enough. The rehearsal records which driving mode Claude Code used. The Codex and Copilot references keep the same instructions.

### D7. The analyzer's tools, fixes and verdicts

| Agent | Tools |
|---|---|
| Claude Code | `Read, Grep, Glob, Bash` |
| GitHub Copilot | `["read", "search", "execute"]` |
| Codex | `sandbox_mode = "workspace-write"`. The rule against hand edits lives in its instructions, because `read-only` would also stop Robocop. |

- It runs `uv run robotcode analyze code` and `uv run robocop check` on the paths it is given. It changes files only with `uv run robocop format --select <formatter>` and `uv run robocop check --fix`, and runs each first with `--diff --no-overwrite`, or `--diff` for `check`.
- For `VAR`, the formatter is `ReplaceWithVAR`. Afterwards, `robocop check --select replace-set-variable-with-var --select replace-create-with-var` must report nothing.
  - Repeat `--select` for each rule. A comma-separated list matches no rule, and Robocop then says "No issues found".
- It sorts every finding into fix, keep or false positive, with a reason. `VariableNotFound` for `${HEADLESS}` is the false positive to expect.
- It runs the suite under `clean` after a change, and compares the result with the run before.
- Removing the edit tool does not stop a shell command from writing a file. The debrief says so, and points to Lab 7's hooks as the guardrail that holds.

### D8. The cheat sheet gains `analyze code`

- One row in *Which command for which question*: "What is wrong in these files, without running them?" answered by `analyze code`.
- A short *Analyze* section, with the example on `tests resources` and its output.
- One trap row: the `VariableNotFound` for a variable read with `Get Variable Value` and a default.

Robocop is not RobotCode, and stays in the lab's text.

### D9. The tool set, without a lock change

- `workshop/toolchain` names static analysis and Robocop, which the locked environment already holds.
- `pyproject.toml`'s comment on `robotcode[all]` names `analyze` and Robocop too, so that nobody narrows the extras without seeing what depends on them.
- `uv.lock` and `setup-check` stay unchanged. Lab 0 checks what the day uses, and a new check on the day could only add a line that fails.

### D10. The reference on `solutions`

The commit `bonus-3-subagents: …` adds `bonus/bonus-3-subagents/`:
- `claude-code/debugger.md` and `claude-code/analyzer.md`, as the rehearsal wrote them;
- `codex/debugger.toml`, `codex/analyzer.toml`, `copilot/debugger.agent.md` and `copilot/analyzer.agent.md`, which carry the same instructions in each format, as `agents/` does. The reference page says they were not rehearsed;
- `suite.patch`: `git diff upstream/main -- tests resources` at the end of the rehearsal.

A `reference: …` commit adds `solutions/bonus-3-subagents.md` and `transcripts/bonus-3-subagents.md`. The page gives the checks of `workshop/solutions` as commands:
- `git apply --check`;
- the suite under `clean`, then under `drift_and_bug` with `broken` excluded;
- `robocop check` with the two rules.

### D11. The rehearsal

- It runs with Claude Code in a fresh clone, through the rehearsal driver, which streams its events.
- Any session that nears the background time limit is split at a step boundary, and the transcript notes it.
- `tools/transcript.py` renders the transcript with `--repo` and `--secrets`. It names a subagent's work after the subagent, and shows the task it was handed and its report: otherwise every call reads as the main agent's, which is the one thing this lab's transcript must not blur. On a transcript without subagents, its output is unchanged.
- Claude Code asks before it writes into `.claude/`, even in `acceptEdits` mode and with an allow rule, and a session without a person cannot ask. The lab tells participants to allow that write. The rehearsal allows it the same way: it writes the content the agent asked to write, unchanged, and the transcript says so.
- The local shop is reset after every run.
- The measured time sets *Time*, and `docs/facilitator/rehearsal.md` records the rehearsal.

### D12. Pointers and the glossary

- Lab 7's stretch goal A gains one sentence that points to Bonus 3.
- `GLOSSARY.md` gains *Static analysis*: checking test files without running them, with RobotCode's `analyze` and Robocop. It ends with a *Read more* line that links both tools' documentation.

## Risks / Trade-offs

- **[The subagent changes an expected value to make a test pass]** → The brief forbids it. The checklist has the participant check `git diff` for changed expected values, and the reference patch shows the right shape.
- **[Claude Code cannot keep the debugger open between steps]** → The brief allows piped rounds, which the cheat sheet documents and Lab 4's rehearsal used. The transcript shows which mode ran.
- **[Codex cannot withhold an edit tool from the analyzer]** → Its limit is in its instructions, and the lab's table says so. Copilot and Claude Code enforce it.
- **[Four debug sessions take longer than 60 minutes]** → The rehearsal sets the estimate. The lab lets a participant hand over two of the four failures.
- **[An answer slips onto `main`]** → The lab and this change name no defect and no failing test's cause. `tools/check_labs.py` scans every file on `main` in CI.
- **[The patch stops applying when `main`'s suite changes]** → The reference checks run when `solutions` is rebased, as *Kept current with main* already requires.
- **[A change to `main` on the workshop day]** → Everything is additive. Lab 7's own steps are untouched, and the site build and `check_labs` gate the merge.

## Migration Plan

1. Apply on a branch `apply-bonus-subagents`: the contract, the pointers, the cheat sheet and the glossary, then the lab text.
2. Rehearse. Then add the reference commits to a local `solutions` branch rebased onto the apply branch.
3. Open the `main` pull request, with `check_labs` passing against the local `solutions` commits.
4. After the merge, rebase `solutions` onto `main`, run its suite, push with a lease, check the redeploy, then archive the change.

Rollback: revert the merge commit. The `solutions` commits are separate, and can be dropped with a rebase.
