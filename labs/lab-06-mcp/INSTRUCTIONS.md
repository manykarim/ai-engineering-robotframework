# Lab 6 - MCP

In Lab 5 your agent wrote tests without ever seeing the page. Now give it live access: the Robot Framework
[MCP server](../../GLOSSARY.md#mcp) runs one keyword at a time in a session that stays open, and lets the agent look
at the page before it decides the next step. Rebuild one of your Lab 5 tests that way, and compare.

| | |
|---|---|
| Module | 6 - Robot Framework MCP: The Live-Access Upgrade |
| Time | 25 minutes |
| Shop preset | `clean` |
| You need | Lab 5 done: one passing test of your own. If you have none, rebuild WEB-004_AC-3 instead |
| You start from | Your repository after Lab 5 |

## Steps

1. **Connect the server.** Copy the configuration for your agent into place, from the repository root.
   `mcp/README.md` explains each line:

   | Claude Code | Codex | GitHub Copilot |
   |---|---|---|
   | `cp mcp/claude-code.mcp.json .mcp.json` | `mkdir -p .codex && cp mcp/codex.toml .codex/config.toml` | `cp mcp/copilot.json .github/mcp.json` |

   Codex asks before each call to one of the server's tools; `mcp/README.md` shows how to allow them all.

2. **Check the connection** in a new session:

   | Claude Code | Codex | GitHub Copilot |
   |---|---|---|
   | approve the project's server when asked, then `/mcp` | `codex mcp list` | `copilot mcp list` |

3. **Rebuild one test stepwise.** Pick one criterion of your Lab 5 slice. For WEB-004_AC-3:

   > Using the robotframework MCP server, build a test for WEB-004_AC-3 step by step. First import the variable
   > file shop/variables.py and the resource file resources/shop.resource, and open the shop with Open Shop Browser
   > and Start Shop Test. Then do one step at a time, and look at the page after each step before you choose the
   > next. Use roles, labels and visible text for locators. When every step works, save the test as
   > tests/ui/search_stepwise.robot, with its locators in keywords under resources/.

   Follow the tool calls: a step runs, the agent reads the page, the next step depends on what it saw. For another
   story, name the file after its area, for example `tests/ui/cart_stepwise.robot`.

4. **Run it** yourself:

   ```bash
   uv run robotcode robot tests/ui/search_stepwise.robot
   ```

5. **Compare** the two versions of the same criterion:

   > Compare the test for WEB-004_AC-3 in tests/ui/search.robot with the one in tests/ui/search_stepwise.robot, and
   > the keywords they use. Which locators and waits differ, and which assumption of the first version did live
   > access confirm or correct?

   Note one thing live access changed, and one thing it did not. Then keep the better version and delete the
   other: two tests for one criterion help nobody.

6. **Look at the cost.** MCP tools are loaded into the agent's context. In Claude Code, `/context` shows how much
   of it the server's tools take. Files, command-line tools and skills are cheaper. Use MCP where live, stateful
   interaction earns its keep.

## Stretch

Change the page under the agent's feet. Keep the session open, and in a terminal switch the shop to a later layout:

```bash
uv run --no-sync python -m shop preset stage3
```

Ask the agent to run the steps of step 3 again, and to tell you what changed on the page. Then put the shop back:

```bash
uv run --no-sync python -m shop reset
```

## If your agent fails

Follow [the recorded walkthrough of this lab](../../transcripts/lab-06-mcp.md), which rebuilds WEB-004_AC-3.
