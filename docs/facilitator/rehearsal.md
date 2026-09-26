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

## Still to do before the workshop tag

| Check | Who | State |
|---|---|---|
| The toolchain on macOS 13+ on Apple silicon (`setup-check` green, the suite runs) | a maintainer with a Mac | open |
| One human walkthrough of Labs 2 to 6, to find what an agent rehearsal cannot: unclear wording | a maintainer | open |
| Lab 7's filing step, from a test fork | a maintainer | open |
| Lab 9's Claude tier, with a Claude credential set on the repository | a maintainer | open |
