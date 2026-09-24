# Subagents

Three subagents with divided responsibilities, for Lab 7's stretch goal A:

| Subagent | Does | Cannot |
|---|---|---|
| `writer` | drafts tests and keywords that follow `docs/conventions.md`, and runs them | - |
| `reviewer` | reviews tests and resources against the conventions and the criterion in `openspec/specs/shop/`, and ends with a verdict | edit any file |
| `runner` | runs tests through RobotCode and reports results with `robotcode results` | edit any file |

The instructions are the same for every agent. Only the file format and the tool names differ, which is why each
agent has its own folder.

## Install

Copy the files of your agent's folder into the folder it loads subagents from:

| Agent | Copy | To | Then |
|---|---|---|---|
| Claude Code | `agents/claude-code/*.md` | `.claude/agents/` | `/agents` lists them |
| Codex | `agents/codex/*.toml` | `.codex/agents/` | Codex starts one when you ask for it by name |
| GitHub Copilot | `agents/copilot/*.agent.md` | `.github/agents/` | `/agent` lists them; `copilot --agent reviewer` starts one directly |

## Use them

Ask by name, in one prompt, and leave the decisions to yourself:

> Use the writer subagent to add a test for WEB-004_AC-7 to a new file tests/ui/search.robot. Then use the reviewer
> subagent to review that file. Show me the reviewer's findings, and do not change anything they mention until I
> say so.

The reviewer cannot edit files. Asked to change something, it reports the change as a finding instead: that is the
point of dividing the work.
