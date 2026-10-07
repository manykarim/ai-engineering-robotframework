# Rehearsal record

*Facilitator material.* Every lab is rehearsed before the workshop tag, so that nobody meets a broken step for the
first time live. This page records each run: when, with which agent, what diverged, and what changed as a result.

## Agents and versions

| Agent | Version | Model |
|---|---|---|
| Claude Code | 2.1.281 | the default of the maintainer's plan |
| Codex | codex-cli 0.156.1 | the maintainer's configured model |
| GitHub Copilot CLI | 1.0.88 | the default, a GPT model |

## Lab assets

### Hooks (2026-09-24)

All three hooks were wired as `hooks/README.md` describes, in a fresh clone, and driven by the prompt in its *Try
them* section. The local shop was `clean`.

| Agent | Inline locator added to a test | Resource or test edited | `git commit` after a red run |
|---|---|---|---|
| Claude Code | rejected, reason shown to the agent | affected tests ran, "1 passed, 1 failed" reported | blocked, failing test named |
| Codex | rejected | affected tests ran, failure reported | blocked |
| GitHub Copilot | rejected | affected tests ran, failure reported | blocked |

Observed along the way, and now covered by the wiring or `hooks/README.md`:
- Codex edits files through `apply_patch` and passes the patch as `tool_input.command`. Copilot does the same with
  a GPT model, and passes the patch as a plain string.
- Copilot runs repository hooks only in a folder the user trusts. In prompt mode (`copilot -p`) nobody is asked, so
  hooks stay off unless the folder was trusted interactively before.
- Codex runs project hooks only once they are trusted.
- Each agent ignores the others' wiring. Copilot reads `.claude/settings.json` but runs none of its hooks.

### Subagents (2026-09-24)

| Agent | Lists writer, reviewer, runner | Reviewer asked to rename a test |
|---|---|---|
| Claude Code | yes | no edit; reviewed the rename instead and gave a verdict |
| Codex | yes | no edit; reported the rename as outstanding because its role is read-only |
| GitHub Copilot | yes | no edit, but in prompt mode (`copilot -p --agent reviewer`) it did not finish within 10 minutes |

- Copilot parses the frontmatter strictly as YAML: a description containing `: ` broke it until the descriptions
  were quoted.
- In Lab 7, Copilot users start the reviewer interactively (`/agent reviewer`), not in prompt mode.

### MCP (2026-09-24)

| Agent | Server listed | Connected | Notes |
|---|---|---|---|
| Claude Code | `claude mcp list` | yes | A project `.mcp.json` server waits for approval on the first interactive start. |
| Codex | `codex mcp list` | yes | Every tool call needs approval; `codex exec` refuses them unless `default_tools_approval_mode = "approve"`. |
| GitHub Copilot | `copilot mcp list`, under *Workspace servers* | yes | Only in a trusted folder. |

- With Claude Code, the shared profile and a throwaway space, a page opened through the server via
  `resources/shop.resource` reported that space in `data-workshop-space`.
- The server does not read `robot.toml`, so `shop/variables.py` failed to import until `PYTHONPATH=.` was added to
  every configuration.

## Labs with Claude Code (2026-09-24)

A fresh clone, a freshly reset local shop, Claude Code 2.1.281 headless (`claude -p`), one session per prompt group,
the labs in order. Prompts were the labs' own. Where a lab has participants edit a file by hand, the agent drafted it
from the same instructions, and the transcript says so. Tokens are input (mostly cached) and output, summed over the
lab's sessions.

| Lab | Result | Duration | Tokens (in / out) |
|---|---|---|---|
| 0 | checklist holds: `setup-check` green, 11 passed and the 2 `broken` failed, the agent explained the repository | 1.5 min | 135 k / 2 k |
| 2 | checklist holds: `AGENTS.md` with the five sections in 34 lines, one section in `docs/agent-environment.md`, `CLAUDE.md` unchanged, before and after saved | 4 min | 1.4 M / 23 k |
| 3 | checklist holds after one fix (below): skills installed into the repository, the convention-2 skill loaded on the review prompt and not on the unrelated one | 9 min | 1.7 M / 57 k |
| 4 | checklist holds: `discover` and `libdoc` through the plugin's skill, the debugger stopped at the assertion, the Module 4 test fixed and untagged, the REPL explored the price range | 8 min | 3.2 M / 34 k |

Found and fixed:
- **Lab 3:** Claude Code guards `.claude/`. It asks before any write there, and in prompt mode refuses even with an
  allow rule. The agent's rewrite of the skill was refused twice. Lab 3's stretch goal now says to approve the write;
  the rehearsal approved it (`bypassPermissions`) and re-ran the lab from step 6.
- **Lab 4:** the plugin is installed with `--scope project` for Claude Code, so that the fork records it in
  `.claude/settings.json`. Lab 7 then merges its hooks into that file instead of copying over it.
- **Lab 4, REPL:** with no display available, the agent explored headless and said so. On a laptop, the browser
  window opens.

## Labs 2 to 4 with Codex (2026-09-24)

The second-agent spot check: a second fresh clone, Codex 0.156.1 (`codex exec`, workspace-write sandbox with network
access), the same prompts, the Codex rows of each lab's table.

| Lab | Result | Duration | Tokens (in / out) |
|---|---|---|---|
| 2 | as with Claude Code: `AGENTS.md` in 29 lines, before and after saved | 3.5 min | 750 k / 9 k |
| 3 | skills installed into `.agents/skills/`; Codex *read* the convention skill for the review prompt and not for the unrelated one; the rewrite of the skill was refused (below) | 9 min | 1.5 M / 24 k |
| 4 | plugin installed for the user, `discover`, `libdoc` and `robot-debug` used, the Module 4 test fixed and untagged | 9 min | 3.4 M / 17 k |

Where Codex diverged, and what changed:
- **Skills are read, not invoked.** Codex loads a skill by reading its `SKILL.md`; there is no separate "skill loaded"
  event. Lab 3's step 7 says Claude Code prints `Skill(<name>)`. For Codex, look for it reading the file.
- **`.agents/` is read-only in the sandbox.** Codex could not rewrite the skill, and offered a patch instead.
  Participants edit it by hand anyway; `docs/environments.md` and Lab 3's stretch goal now say so.
- **uv's cache.** The sandbox cannot write `~/.cache/uv`; Codex set `UV_CACHE_DIR` to a temporary folder by itself.
  Named in `docs/environments.md`.
- **Network.** Test runs need `sandbox_workspace_write.network_access=true`, as `docs/environments.md` says.
- **Plugin scope.** `codex plugin add` installs for the user only. The rehearsal removed the plugin and its
  marketplace afterwards.

## Labs 5 to 8 with Claude Code (2026-09-24 and 25)

Continued in the same clone. Lab 5 ran with `--strict-mcp-config` and no server: no MCP tool was called. Agent time
is the sum of the sessions' own durations; the clone's machine slept overnight during Lab 5.

| Lab | Result | Agent time | Tokens (in / out) |
|---|---|---|---|
| 5 | checklist holds for all three stories (WEB-004, WEB-003, WEB-005): each change proposed, reviewed against the *Plan review* list, applied with all tasks done, run green, and archived to `openspec/specs/suite/<area>`; the Module 5 test fixed from the specification alone and untagged | 28 min for WEB-004 (propose 14, review 5, apply 7, archive 3); 48 min for the two other stories | 14.6 M / 143 k for WEB-004 |
| 6 | checklist holds: the server connected, WEB-004_AC-3 rebuilt in 31 MCP calls, the agent kept the better version and deleted the other | 7 min | 3.1 M / 35 k |
| 7 | checklist holds except the filing (below): all three hooks behaved, the inline locator moved into a keyword, `buggy` failed exactly the 3 defect tests, an issue drafted for one of them, and after the reset the suite was green and commits allowed | 5 min | 1.6 M / 21 k |
| 8 | checklist holds: 4 tests failed under `drift_and_bug`, 2 with healing (the two defects), no test file changed; the stretch goal repaired `WEB-006_AC-7 Successful Order` onto the field labels, and it passes under `drift_and_bug` and `clean` | 6 min | 2.2 M / 29 k |

After all labs, the rehearsed suite has 30 tests, and all of them pass in a freshly reset shop.

Found and changed:
- **Lab 5 is tight.** Propose, pair review and apply fill the 30 minutes. Lab 5 now tells participants that the
  propose step takes minutes, and offers a two-criteria slice; the run sheet makes it the overrun action.
- **Lab 5, the first rehearsal of WEB-004** stopped half-way through apply: the agent started a check in the
  background, and a headless session ends with the agent's answer. That is a property of prompt mode, not of the
  lab. Participants work interactively. The rehearsal was repeated with foreground commands only.
- **Lab 6** writes `.robotmcp_artifacts/` into the repository root; it is now ignored by git.
- **Lab 7, step 7** was not rehearsed: the rehearsal ran in the workshop's own repository, not in a fork, and filing
  a real issue there was not wanted. The draft in `results/issue.md` was complete. **Open: file one issue from a
  test fork before the workshop.**

## Lab 9 on GitHub Actions (2026-09-26)

Rehearsed in the workshop's own repository, with pull request #15 from the branch `lab-09-break`, following the
lab's steps. Two breaks on purpose in `tests/api/smoke.robot`: the expected health status `ok` changed to `okay`,
then the catalogue's expected length 12 to 13. The pull request was closed without merging.

| Check | Result | Runs |
|---|---|---|
| *Run tests* on a pushed break | failed on the push and again on the pull request, naming `Health Reports Ok` | 36240802192, 36240803925 |
| Triage, summary tier (no secret) | one comment by `github-actions[bot]`: 10 passed, 1 failed, the table, and the line naming the secrets | 36241005949 |
| Triage, `TRIAGE_*` tier (MiniMax-M3 through the maintainer's endpoint) | the second break updated the same comment, still one: the table with both failures, and a root cause per test that names the right diff hunk and quotes the failure message; after the fixes below, the same comment again, clean | 36241140426, 36241604738 |
| Triage, Claude tier | **open**: no Claude credential is set on the repository | - |
| *Heal suggestions* without `HEAL_*` | succeeded with the notice; nothing changed | 36241043507 |
| *Heal suggestions* with `HEAL_*`, preset `stage4` | healed the drifted locators and pushed them to `heal-suggestions/<run id>`: five lines of `resources/legacy.resource`, nothing else, nothing merged | 36241089067, 36241288079 |

Found and changed:
- **GitHub Actions may not open pull requests.** The first heal run with a model pushed its branch, then failed:
  every repository and fork starts with *Allow GitHub Actions to create and approve pull requests* switched off.
  The workflow now ends successfully and links the branch in the job summary and a notice, so that the participant
  opens the pull request. Lab 9's stretch goal says so. The rehearsal left the setting off, as on a fork.
- **A reasoning model's thinking landed in the comment.** MiniMax-M3 starts its answer with a `<think>` block.
  `tools/triage.py` now drops a leading thinking block, and falls back to the summary when nothing else is left.
- **Long failure messages lost their verdict.** The table cut each message after 300 characters, which dropped
  "should be 13 but is 12" from the catalogue test. It now keeps the start and the end.
- **The analysis adds claims.** Both root causes were right, but the model also asserted things the evidence does
  not show (which product ids it could see, that "the other products are stable"). That is the discussion Lab 9's
  question *Would you trust it?* is for; facilitators can use this comment as the example.
- **Heals differ from run to run.** The two runs replaced `${GRID} >> .product-grid` with different locators, one
  of them no longer using `${GRID}`. Reviewing the suggestion is the lesson, as in Lab 8.

## Lab 4, step 6 again (2026-09-26)

After `robotcode-chapter`, `-v HEADLESS:False` holds in the REPL, and Lab 4 links the RobotCode cheat sheet. Step 6
was run again: Claude Code 2.1.283 headless, the lab's prompt, in a fresh clone of the change's branch with the
participant's work of Labs 2 to 4 copied from the first rehearsal's clone.

| Lab | Result | Duration | Tokens (in / out) |
|---|---|---|---|
| 4, step 6 | checklist holds: a visible browser from `-v HEADLESS:False` with no workaround (`"headless": false`, no `Set Global Variable`), the REPL piped as the cheat sheet shows, no test file, working locators and keywords for the price range | 4.5 min (7 in the first rehearsal) | 837 k / 15 k |

Found and changed:
- **The agent found the cheat sheet by itself** (`ls docs`), read it before starting the REPL, and piped every
  session instead of keeping one open.
- **The output directory bites without `-d` too.** The clone had never run a test, so `results/` did not exist and
  the first REPL failed with `FileNotFoundError`. The agent created `results/` from the cheat sheet's trap table. In
  the lab, earlier runs have created it, but the cheat sheet, Lab 4 and the triage playbook said only `-d` needed
  care. They now say that the directory must exist, whichever it is.
- **Codex was not run again.** The change removed a trap without changing a step, so the Codex run of Lab 4 above
  still stands for everything it recorded.

## Bonus labs with Claude Code (2026-10-06)

Claude Code 2.1.289 headless, with the labs' own commands and prompts. Each lab ran in a fresh folder next to a
fresh clone of the change's branch. Where a lab has you write a file (`AGENTS.md`, `config.yaml`), the agent drafted
it from the lab's own list, and the transcript says so. The review of step 6 put the lab's questions to the agent.

| Lab | Result | Agent time | Tokens (in / out) |
|---|---|---|---|
| Bonus 2 | checklist holds: the agent loaded only the project's `AGENTS.md`; 76 unit tests and 5 Robot tests pass; `uv build`; on the workshop's catalogue suite, the dry run recorded one issue per failed test, sent nothing, and the run failed the same tests as without it | 19 min recorded, plus an interrupted apply of about 15 | 5.7 M / 114 k |
| Bonus 1 | checklist holds: the agent loaded only the project's `AGENTS.md`; 76 unit tests and 26 Robot tests against the shop pass; `Get Product Price    1    ==    249.99` passes and `==    1` fails with AssertionEngine's message; libdoc and `uv build` | 24 min recorded, plus an interrupted apply of about 45 | 6.6 M / 134 k |

Found and changed:
- **Bonus 2: the listener must import from its source folder alone.** In the first rehearsal, the package read its
  own version from installed package metadata. Step 8 runs it from the workshop's clone with `--pythonpath`, where
  it is not installed. The import failed, Robot Framework skipped the listener with an error, and the run went on.
  The lab now says it in `AGENTS.md`'s concepts and in the review, and was rehearsed again from the start.
- **Bonus 1: libdoc needs the library's `url`.** libdoc imports the library, and the lab's first command passed no
  arguments. The agent paused instead of guessing. The lab now gives `::url=http://localhost:9090`, and the
  rehearsal told the agent and continued.
- **Bonus 1 takes about two hours, not 75 minutes.** Propose, review and apply took the agent more than an hour.
  The agents planned 22 and 17 tasks for one slice. The reference pages say to review the tasks' size.
- **`uv init` copies the author's name and email** from the git configuration into `pyproject.toml`. The reference
  projects carry a neutral author. Participants who publish a package should check it.
- **Transcripts.** Claude Code's notice for a large tool output names `~/.claude/projects/<path with dashes>`.
  Labs 5 and 8 carried such a path. `tools/transcript.py` now rewrites it, and the two transcripts were fixed.
- **The rehearsal tool's time limit** interrupted one apply session per lab. A new `/opsx:apply` continued from
  the ticked tasks. The interrupted sessions are not recorded, and the transcripts say so.
- **No real GitHub issue was created.** The listener's live path is covered by its unit tests. Its stretch goal,
  a live run against a fork, is open below.

## Bonus 3 with Claude Code (2026-10-07)

Claude Code 2.1.289 headless, with the lab's own commands and prompts, in a clone after the day: the lab results of
`solutions`, Labs 2 to 8, without its reference material, with Bonus 3 merged in. Where the lab says to approve
something, the rehearsal approved it: "Save it." and "I agree. Write it."

| Run | Result | Agent time | Tokens (in / out) |
|---|---|---|---|
| 1 | checklist holds, except the REPL: the debugger tried every fix at the paused prompt, and never used the REPL | 35 min | 1.6 M / 37 k |
| 2 | checklist holds: both subagents written from the briefs; four hand-overs, one test each; two tests repaired, two defects reported, no expected value changed; 11 `robot-debug` rounds and 3 REPL checks; 23 findings with verdicts; seven `VAR` conversions after the diff, the suite 11 of 11 before and after; the hand edit left as a finding | 36 min, not counting the 6 h 25 min the laptop slept during step 6 | 2.0 M / 44 k |

The token counts are the main sessions'. The subagents' own work is not counted in them.

Found and changed:
- **The REPL needs a job of its own.** Run 1's brief offered the REPL only as an alternative to the paused prompt,
  and the debugger never used it. The brief now has the debugger check each keyword it writes on its own in the
  REPL, and run 2 did so three times.
- **Claude Code asks before it writes into `.claude/`,** even in `acceptEdits` mode and with an allow rule such as
  `Edit(./.claude/agents/**)`. The lab now says to allow the write. A headless session cannot ask: the rehearsal
  wrote the content the agent asked to write, unchanged, and the transcript says so.
- **Transcripts name subagents.** `tools/transcript.py` labels a subagent's calls with its name, and shows the task
  it was handed and its report. For transcripts without subagents, its output is unchanged.
- **What a finding is measured against.** The rehearsal's branch held the day's repairs in its last commit, so the
  analyzer read step 1's restore as new changes, and listed the two broken tests and the inline locator among its
  problems. The reference page debriefs it.
- **Robocop's `--select` takes one rule each.** A comma-separated list selects no rule, and Robocop then reports no
  issues. The lab says so.

## Still to do before the workshop tag

| Check | Who | State |
|---|---|---|
| The toolchain on macOS 13+ on Apple silicon (`setup-check` green, the suite runs) | a maintainer with a Mac | open |
| One human walkthrough of Labs 2 to 6, to find what an agent rehearsal cannot: unclear wording | a maintainer | open |
| Lab 7's filing step, from a test fork | a maintainer | open |
| Lab 9's Claude tier, with a Claude credential set on the repository | a maintainer | open |
| Bonus 2's stretch goal: the listener live against a test fork, then the issues closed. Not needed for the tag | a maintainer | open |
| Bonus 3 with Codex or GitHub Copilot: their subagents carry the rehearsed instructions, unrehearsed. Not needed for the tag | a maintainer | open |
