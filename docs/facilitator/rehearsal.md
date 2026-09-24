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
