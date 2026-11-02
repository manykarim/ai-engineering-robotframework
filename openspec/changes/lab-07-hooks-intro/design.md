# Design

## Context

See proposal.md for why. What exists today:

- `hooks/` holds three scripts and one wiring file per agent. `hookio.py` reads each agent's hook input into one
  `Call` (an edit, a shell command, or something else). It answers with `deny()` before an action and `report()`
  after it, in the form the sending agent understands. Every hook so far is a tool hook. No hook adds context, and
  `hookio` cannot parse a session-start payload.
- **Agents installed here:** Claude Code 2.1.296, Codex CLI 0.165.0 and GitHub Copilot CLI 1.0.92.
- **Each agent's current documentation**, checked 2026-11-02:
  - Claude Code: code.claude.com/docs/en/hooks.
  - Codex: learn.chatgpt.com/docs/hooks. Hooks have been on by default since 0.124.
  - Copilot: docs.github.com, *CLI hooks reference* and *About hooks*.

  All three call the shared events in the same loop, but under their own names:

  | Moment | Claude Code | Codex | Copilot | A hook can |
  |---|---|---|---|---|
  | Session starts | `SessionStart` | `SessionStart` | `sessionStart` | add context |
  | Before a tool | `PreToolUse` | `PreToolUse` | `preToolUse` | refuse, with a reason |
  | After a tool | `PostToolUse` | `PostToolUse` | `postToolUse` | report a result the agent must take in |
  | Agent stops | `Stop` | `Stop` | `agentStop` | send it back to work, at most 8 times in a row |
  | Prompt sent | `UserPromptSubmit` | `UserPromptSubmit` | `userPromptSubmitted` | block or add context, except in Copilot |

  Other differences:
  - **Edit tools:** `Write` and `Edit` in Claude Code; `apply_patch` in Codex; `create`, `edit` and `apply_patch`
    in Copilot.
  - **Command key:** `command` in Claude Code and Codex; `bash` and `powershell` in Copilot.
  - **Timeout:** `timeout` in Claude Code and Codex, default 600 s; `timeoutSec` in Copilot, default 30 s.
  - **Adding context:**
    - Claude Code: plain stdout at session start becomes context.
    - Codex: plain stdout at session start becomes context, but stdout is ignored after a tool.
    - Copilot: only JSON `additionalContext` adds context.
  - **Copilot also reads `.claude/settings.json`.** Its documentation now lists inline `hooks` there as a source.
    The September rehearsal (`docs/facilitator/rehearsal.md`) saw it read the file but run none of its hooks.
  - **`MultiEdit`:** it was in our Claude Code matcher, but Claude Code no longer has the tool: its tools reference
    lists `Edit`, `Write` and `NotebookEdit` for edits, and its hooks guide matches `Edit|Write`.
- **Static analysis today:**
  - `uv run robotcode analyze code tests resources` takes 1.3 s for the whole suite.
  - On one file, it takes about 0.2 s of analysis and about 2 s including `uv`.
  - Its one finding on `main` is the `${HEADLESS}` false positive in `resources/shop.resource:17`.
    `docs/robotcode.md` lists it as a trap and names the ignore comment.
  - `uv run robotcode robot --dryrun tests` passes 13 of 13 in about 5 s.
  - Plain `robot --dryrun` fails every file: it ignores `robot.toml`'s python path, so `resources/...` is not found.
- **The timetable:**
  - Module 7 is 40 minutes (15/20/5).
  - The numbers appear in `docs/WWWW_Workshop_Master_Preparation.md` (the table and the Module 7 to 9 headings),
    `docs/facilitator/run-sheet.md`, `labs/README.md` and `tools/check_labs.py`.
  - `workshop/labs` requires the lab budget to equal the timetable's lab share.
- **The site:** Docusaurus 3.10.2, with `markdown.format: 'detect'`, so `.md` files are CommonMark. It has no
  Mermaid theme.
- **On `solutions`:**
  - `010282d lab-07-hooks-toolbelt` holds `.claude/settings.json` (the Lab 4 plugin plus the three hooks) and the
    inline locator moved into a keyword.
  - The later commits do not touch `.claude/settings.json` or `resources/shop.resource`.
  - The transcript was recorded with Claude Code 2.1.281 through `tools/transcript.py`.

## Goals / Non-Goals

**Goals:**
- After the page and the lab, a participant can write a hook that works in their own agent and wire it, and knows how
  to port it to the other two.
- Every provided hook behaves the same in Claude Code, Codex and Copilot, and so does the page's context example.
- The static check is fast and quiet enough to stay wired every day.

**Non-Goals:**
- Teaching every event of every agent. The page links each agent's full list.
- Hooks of other types (Claude Code's `prompt`, `agent` and `http` hooks; Copilot's `exec`), and hooks set by
  managed policy.
- Changing the three existing hooks' behaviour, the suite, or Modules 8 and 9's content.
- Copilot's cloud agent. The labs use the CLI; the page notes that the cloud agent supports fewer events.

## Decisions

### D1. One page, `docs/hooks.md`, under *Guides*; the lab links it
- **Placement:** the theory lives on the page, and Lab 7 keeps only steps. Step 1 is "read the page".
- **Order of sections:**
  1. What a hook is.
  2. The loop, as one diagram.
  3. The shared events, as the table above.
  4. How a hook answers: exit code 2 and stderr; Copilot's JSON; context.
  5. Wiring side by side, with the smallest examples: "after any edit" and "after an edit to `.robot` or
     `.resource`". The type filter sits in the script, because a matcher sees only the tool name, never the file.
  6. The static check as the worked example (D2).
  7. Writing your own on top of `hookio.py` (D5).
- **Format:** definition lists and tables wherever they suffice. Only the loop gets a diagram, because the
  diagram's point is *where* a hook interrupts, and a list hides that.
- **Links:** the page links each agent's hook documentation, the way `GLOSSARY.md` does. The glossary's *Hook*
  entry links the page.
- **Rejected alternatives:**
  - Expanding `hooks/README.md`: it stays the reference for the provided files, and is not on the site.
  - Putting the theory into the lab: it would push the steps below the fold, and the theory is reread after the day.

### D2. The static check runs `robotcode analyze code` on the edited file only
Design of `hooks/static_check.py`, after an edit:
1. It keeps only the edited `.robot` and `.resource` files under `tests/` and `resources/`.
2. It runs `robotcode analyze code <files>` from the environment's own `robotcode`, as `run_affected_tests.py` does.
3. It keeps the lines with `[ERROR]`, drops the `Files: ...` summary, and caps the output at 5 lines plus "and N
   more".
4. With nothing to report, it stays silent (exit 0).
5. With errors, it uses `report(..., problem=True)`.

As a command, it takes files and folders, like the other hooks.

- **Why only the edited file:**
  - It is the change the agent just made, so a finding is actionable.
  - Checking the whole suite would repeat findings from files the agent did not touch.
- **Why errors only:** warnings and hints are noise for an agent mid-task. The page says how to widen it.
- **Why `analyze` and not `--dryrun`:**
  - It needs no test run.
  - It reports file, line and column.
  - It catches the same unknown keywords, variables and wrong argument counts, faster.
  - The page shows `uv run robotcode robot --dryrun <file>` as the next rung, and why plain `robot --dryrun`
    fails. That is the AGENTS.md trap, and the demo shows it live.
- **Placement in the wiring:** the hook is wired after an edit, before `run_affected_tests.py`.
  - Each agent runs both, and they are independent.
  - It is deliberately not a gate for the test run: the hooks stay simple, one job each.
  - Timeout: 60 s in every agent. Copilot's default of 30 s is too tight on a cold `uv`.

### D3. Silence the false positive at its line
`resources/shop.resource:17` gets `# robotcode: ignore[variable-not-found]`, which is RobotCode's own mechanism and
what `docs/robotcode.md` already recommends. Effects:
- `analyze code` on `main` reports nothing, so the static check is silent on an untouched suite.
- `docs/robotcode.md`'s *Analyze* example output and its trap row change: the trap row says the line is already
  marked.
- Behaviour does not change: the comment is not Robot Framework syntax that runs.

Rejected: filtering `${HEADLESS}` inside the hook. It would hide a real finding of that kind elsewhere, and it
teaches the wrong habit.

### D4. `hookio` learns session start and context
- **Parsing:** `parse()` recognises a session-start payload as `Call(kind="session")`:
  - Claude Code and Codex: `hook_event_name == "SessionStart"`;
  - Copilot: the payload has no `toolName` and carries `source`.
- **Answering:** a new `context(call, text)` answers in each agent's form:
  - Claude Code and Codex: plain stdout, exit 0;
  - Copilot: `{"additionalContext": text}`.
- **Use:** none of the four provided hooks uses it. The page's example does: a session-start hook that adds
  `python -m shop status`. That also makes it the D5 menu's context example.
- **Agent detection:** it stays as it is. Copilot's camelCase payload is unmistakable, and Codex differs from Claude
  Code only by fields neither hook needs.

### D5. "Write your own": the agent writes it, the participant chooses and checks
The participant gives their agent a short prompt from the lab. The agent writes `hooks/<name>.py` on top of
`hookio.py`, using the page and the existing hooks as the example, and wires it into the agent's own file. The
participant then triggers it with a prompt of their own.

This is agentic engineering, and it fits about 8 minutes. Typing the wiring by hand would teach syntax, not the idea.

The page's menu has one line each, with the event and what it teaches:

| Hook | Event | Kind of answer |
|---|---|---|
| Use `robotcode`, not plain `robot`: refuse a shell command that runs `robot` or `python -m robot`, and name the right command | before a shell command | refuse |
| No shortcut to green: refuse an edit that adds the `broken` tag, `Skip`, `Run Keyword And Ignore Error` or `Pass Execution` to a test | before an edit | refuse |
| Criterion ID first: refuse a new test whose name does not start with `<STORY>_<AC>` and has no `smoke` tag | before an edit | refuse |
| The specs are the reference: refuse edits under `openspec/specs/shop/` | before an edit | refuse |
| Robocop on the edited file | after an edit | report |
| The shop's status at session start | session start | context |

*Done means green*, a stop hook, is described with its cost (up to 8 extra rounds) and not offered for the lab.

The lab recommends the first or the second hook for a first try. The rehearsal writes "No shortcut to green", and
that is what `solutions` records.

The page gives no lab answer away: it names no planted defect, no inline locator and no broken test's cause. The
menu describes behaviour; `main` ships none of these hooks.

### D6. Lab 7's steps and time

| Step | What | Minutes |
|---|---|---|
| 1 | Read `docs/hooks.md` | 3 |
| 2 | Wire the four hooks | 3 |
| 3 | Try them: the existing three-part prompt, plus a misspelled keyword | 4 |
| 4 | Write your own hook with your agent, wire it, trigger it | 8 |
| 5 | Scan the suite with the inline-locator hook | 3 |
| 6 to 10 | `buggy`, run, draft, file with `gh`, reset | 9 |

The lab gets 30 minutes; with the debrief and the talk, Module 7 is 15/30/5, 50 minutes.

The 10 minutes come from:
- Module 8: 30 becomes 25 (10/12/3);
- Module 9: 35 becomes 30 (10/15/5).

New times: 15:05-15:55, 15:55-16:20 and 16:20-16:50. The day still ends at 17:00, and the lab budgets of 8 and 9 are
unchanged, as the user decided. Only the numbers change, in:
- the master document's table and headings;
- the run sheet;
- `labs/README.md`;
- `tools/check_labs.py`;
- the spec scenario.

Two prose lines need updating: "Self-healing at 15:45" in the master document, and the 15:45 start in the run
sheet.

The steps keep their wording where they do not change. The checklist gains two items: "your own hook is wired in
your agent's file", and "it refused or answered one action".

### D7. Mermaid through `@docusaurus/theme-mermaid`, pinned to the core version
- **Setup:** add `@docusaurus/theme-mermaid@3.10.2` (the same version as the core), set `markdown.mermaid: true`,
  add `themes: ['@docusaurus/theme-mermaid']`, and set `themeConfig.mermaid.theme` to `{light: 'neutral', dark:
  'dark'}`.
- **Why Mermaid:** GitHub renders the same block natively, so the page reads the same in a fork.
- **Check:** the build must show the diagram on a CommonMark `.md` page, not only in MDX. If it cannot, the fallback
  is an ASCII diagram in a code block, and the docs-site delta is dropped.

### D8. Re-check every provided hook in every agent, and settle the double-wiring question
- **Every hook:** the three-part prompt plus the misspelled keyword runs in a fresh clone, once per agent:
  - Claude Code: interactive or `-p` in a trusted folder;
  - Codex: `exec`, with the hooks trusted through `/hooks` first;
  - Copilot: interactive, in a trusted folder. `-p` alone runs no hooks.
- **The context example** runs at session start in each agent.
- **Copilot and Claude Code's wiring:** Copilot is started where only `.claude/settings.json` carries hooks.
  - If it runs them, the page and `hooks/README.md` say to wire only one agent's file per clone, or that Copilot
    users with both files get every hook twice. The wiring scenario in `workshop/lab-assets` then holds only with
    that advice.
  - If it does not, the rehearsal note stands.
- **`MultiEdit`:** removed. The workshop targets the latest Claude Code only, so the matcher is `Write|Edit`, and
  `hooks/hookio.py` and `tools/transcript.py` drop their `MultiEdit` branches.

### D9. `solutions`: re-rehearse Lab 7 and rebuild its commit from the rehearsal
1. Rebase `solutions` onto the new `main` with the sequence editor of the last change, marking
   `lab-07-hooks-toolbelt` and `reference: one page per lab` as `edit`, plus the reference commit that holds the
   transcripts (`acb9e65 reference: the transcripts ...`).
2. At the Lab 7 stop, rehearse the new Lab 7 with Claude Code in a WSL clone of the commit before it, recording the
   events for `tools/transcript.py`.
3. The rehearsal's files become the commit:
   - `.claude/settings.json` with four hooks plus the own hook;
   - the own hook's script;
   - the inline locator moved, as before.

   The message keeps its prefix and says what is new. Its subject must start with `lab-07-hooks-toolbelt`.
4. The reference page gets the own hook and why it is a good one.
5. The transcript is replaced with the new recording.
6. Then the suite runs (every test must pass) and the branch is force-pushed with a lease, as in the last two
   changes.

Lab 7's step 7 (filing in a fork) stays unrehearsed, as `docs/facilitator/rehearsal.md` already records.

## Risks / Trade-offs

- **[Hook formats change quickly]** → Agent versions go into the transcript and `docs/facilitator/rehearsal.md`. The
  page links each agent's documentation for anything beyond the shared events.
- **[Copilot runs `.claude/settings.json` hooks too]** → D8 tests it; the page then says to wire only your agent's
  file.
- **[An own hook blocks the participant's later steps]** For example, "use `robotcode`" also stops the participant's
  own agent from running plain `robot`, which is intended. A broken hook could block more than intended → the page
  says how to unwire it, and `hookio` already lets an action through when it cannot read the input.
- **[The static check doubles the time after every edit]** → about 2 s, which is small next to the affected tests
  it runs beside.
- **[Re-rehearsing Lab 7 with `buggy` and `gh` takes long, and the agent may write a different hook]** → The lab
  prompt names the choice. The rehearsal records whatever the agent writes, if it passes the checklist.
- **[Mermaid does not render in CommonMark `.md`]** → D7's fallback.
- **[Module 8 and 9 talks lose 5 minutes each on paper]** → The user accepted this, since the times are estimates.
  Their cut order is unchanged.
