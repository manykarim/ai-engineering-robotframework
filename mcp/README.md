# The Robot Framework MCP server

`rf-mcp` gives your agent live access: it runs Robot Framework keywords one step at a time, in a session that stays
open, and sees the page after each step. Lab 6 connects it. It is already installed in this repository's
environment, at the version `uv.lock` pins, so every agent starts it the same way:

```bash
uv run --no-sync rf-mcp
```

## Connect it

Copy the file for your agent into place, from the repository root. Each agent can also add it with a command,
shown in the last column.

| Agent | Copy | To | Or |
|---|---|---|---|
| Claude Code | `mcp/claude-code.mcp.json` | `.mcp.json` | `claude mcp add --scope project robotframework --env PYTHONPATH=. -- uv run --no-sync rf-mcp` |
| Codex | `mcp/codex.toml` | `.codex/config.toml` | `codex mcp add robotframework --env PYTHONPATH=. -- uv run --no-sync rf-mcp` |
| GitHub Copilot | `mcp/copilot.json` | `.github/mcp.json` | `copilot mcp add robotframework --env PYTHONPATH=. -- uv run --no-sync rf-mcp` |

The commands for Codex and Copilot add the server to your user configuration, not to the repository. It then starts
in whichever folder you start your agent in, so always start it in the repository root.

Then check the connection:

- **Claude Code** asks you to approve the project's server the first time you start `claude` here. Approve it.
  `/mcp` shows it as connected.
- **Codex** asks before each call to one of the server's tools. To allow every tool of this server, add
  `default_tools_approval_mode = "approve"` under `[mcp_servers.robotframework]`.
- **GitHub Copilot** loads the server only in a folder you trust. `copilot mcp list` shows it under *Workspace
  servers*, and `/mcp` in a session shows its state.

## Reach your shop

The server runs in the repository root, with `PYTHONPATH=.`, so it can load `shop/variables.py`. That is how the
shop's address and your space get into a session: `shop/variables.py` reads `SHOP_URL` and `SHOP_SPACE` from your
environment or `.env`, exactly as the suite does. Plain `robot.toml` settings do not apply here: the server does not
read that file.

In a session, have your agent import the variable file and the shop resource first, then open pages through the
resource's keywords. They send your space with every request:

> Using the robotframework MCP server: import the variable file shop/variables.py and the resource file
> resources/shop.resource, then run Open Shop Browser and Start Shop Test.

Nothing in these files is secret, and none of them names a space: the space comes from your `.env`.
