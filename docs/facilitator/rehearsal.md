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
