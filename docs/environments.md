# Environments

How you can run the workshop, and which coding agent to bring. Read this a week before the day, together with
[SETUP.md](../SETUP.md).

## Where the shop runs

Everything in the labs runs against the demo shop. You have three options, and the labs work the same way in each:

| Option | You need | Set up | Presets |
|---|---|---|---|
| **Local shop** (recommended) | Docker with Compose | `docker compose -f shop/compose.yaml up -d`, then `http://localhost:9090` | yours alone |
| **Shared instance** | nothing but a browser and the repository | put `SHOP_URL` (from the facilitators) and `SHOP_SPACE` (your GitHub handle) into `.env` | in your own space, which nobody else sees |
| **No Docker at all** | as the shared instance | as the shared instance | as the shared instance |

With the shared instance, add `-p shared` to every test run (`uv run robotcode -p shared robot`). The shop helper
(`uv run --no-sync python -m shop ...`) and the labs pick up your space from `.env` by themselves.

Choose the local shop if Docker runs on your machine and can pull images: nothing you do depends on the network.
Choose the shared instance if Docker is blocked, forbidden or too slow on your laptop.

## Which coding agent

The facilitators demonstrate with **Claude Code**. **Codex** and **GitHub Copilot** (the CLI) work for every lab.
Bring the one you use at work, or the one your company lets you use: the labs teach patterns that carry over.

| | Claude Code | Codex | GitHub Copilot CLI |
|---|---|---|---|
| Sign-in | a Claude plan or an Anthropic API key | a ChatGPT plan or an OpenAI API key | a GitHub Copilot plan |
| Context file | `AGENTS.md`, through `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` |
| Spec-driven workflow (Lab 5) | `/opsx:propose`, `/opsx:apply`, `/opsx:archive` | `$openspec-propose`, `$openspec-apply-change`, `$openspec-archive-change` | `/opsx-propose`, `/opsx-apply`, `/opsx-archive` |
| Trust | asks once per folder | asks before it runs project hooks and before each MCP tool call | asks once per folder; hooks, agents and workspace MCP servers need it |

## Where the labs differ between agents

The labs give a table wherever the agents differ. Here are all those differences in one place:

| Lab | Claude Code | Codex | GitHub Copilot |
|---|---|---|---|
| 2: check the context loads | `/memory` | reads `AGENTS.md` on start | `copilot instruction list` |
| 3: Robot Framework Agent Skills | `--agent claude-code`, into `.claude/skills/` | `--agent codex`, into `.agents/skills/` | `--agent copilot`, into `.claude/skills/`, which Copilot also reads |
| 3: your own skill | `.claude/skills/<name>/` | `.agents/skills/<name>/` | `.github/skills/<name>/` |
| 4: RobotCode plugin | `claude plugin marketplace add --scope project ...`, `claude plugin install --scope project robotcode@robotframework-agent-plugins`, recorded in `.claude/settings.json` | `codex plugin marketplace add ...`, `codex plugin add robotcode@robotframework-agent-plugins` | `copilot plugin marketplace add ...`, `copilot plugin install robotcode@robotframework-agent-plugins` |
| 6: MCP server | `.mcp.json`, approve it on first start, `/mcp` | `.codex/config.toml`, approve each tool call or allow them all | `.github/mcp.json`, in a trusted folder, `copilot mcp list` |
| 7: hooks | `.claude/settings.json`, merged with the plugin entry of Lab 4 | `.codex/hooks.json`, trust them when asked | `.github/hooks/workshop.json`, in a trusted folder |
| 7: subagents | `.claude/agents/*.md`, `/agents` | `.codex/agents/*.toml`, ask for one by name | `.github/agents/*.agent.md`, `/agent`; start the reviewer interactively, not with `copilot -p` |

## Codex and its sandbox

Codex runs shell commands in a sandbox, which shows in three ways during the labs:

- **Network.** The sandbox blocks network access by default, and test runs reach the shop over the network. Allow it
  when Codex asks, or start Codex with network access for the workspace:

  ```bash
  codex -c sandbox_workspace_write.network_access=true
  ```

- **uv's cache.** uv keeps a download cache in your home folder, outside the workspace. Codex notices, and points
  `UV_CACHE_DIR` somewhere writable by itself. Nothing to do, but don't be surprised by it in the transcript.
- **Agent configuration.** `.agents/` and `.codex/` are read-only inside the sandbox. Codex asks before it changes
  a skill there, or you edit the file yourself, as Lab 3 does anyway.

Claude Code has the same guard for `.claude/`: it asks before it writes there.

## Cost

An agent session makes many model requests. **Set a spending cap** on any API key you use today, and prefer a
subscription plan if you have one. Healing in Module 8 needs its own model only if the facilitators say so
(`SETUP.md`, *Healing API key*); otherwise you triage a recorded report.
