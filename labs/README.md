# Labs

One folder per lab. Each has `INSTRUCTIONS.md` (what to do) and `checklist.md` (what "done" looks like). Every lab
starts with a table that says how long it takes, which preset the shop must be in, and what you need to have done
before. Missed a lab? Each lab says how to catch up, so you can always join the next one.

| Lab | Module | Time | Shop preset |
|---|---|---|---|
| [Lab 0 - Arrival](lab-00-arrival/INSTRUCTIONS.md) | 0 - Arrival & Environment Check | 30 min | `clean` |
| [Lab 2 - Context](lab-02-context/INSTRUCTIONS.md) | 2 - Context Engineering | 25 min | `clean` |
| [Lab 3 - Skills](lab-03-skills/INSTRUCTIONS.md) | 3 - Agent Skills | 25 min | `clean` |
| [Lab 4 - RobotCode](lab-04-robotcode/INSTRUCTIONS.md) | 4 - RobotCode for Agents | 25 min | `clean` |
| [Lab 5 - Prompt to green](lab-05-prompt-to-green/INSTRUCTIONS.md) | 5 - Natural Prompt Automation & Debugging | 30 min | `clean` |
| [Lab 6 - MCP](lab-06-mcp/INSTRUCTIONS.md) | 6 - Robot Framework MCP | 25 min | `clean` |
| [Lab 7 - Hooks and toolbelt](lab-07-hooks-toolbelt/INSTRUCTIONS.md) | 7 - Hooks, Subagents & the CLI Toolbelt | 20 min | `buggy` |
| [Lab 8 - Healing](lab-08-healing/INSTRUCTIONS.md) | 8 - Self-Healing Tests | 12 min | `drift_and_bug` |
| [Lab 9 - CI](lab-09-ci/INSTRUCTIONS.md) | 9 - CI & Toolchain Integration | 15 min | `clean` |

Module 1 (the cold open) and Module 10 (wrap-up) have no lab.

## How a lab works

- **Steps** are either a command to run or a prompt to give your coding agent. Prompts are quoted in full: paste
  them as they are, so that everyone's agent gets the same input. Your agent's answer will still differ from your
  neighbour's. Comparing the two is part of the lesson.
- **Presets** switch the shop between behaviours: `clean`, the drift stages and the planted-bug presets. Apply them
  only with the shop helper, `uv run --no-sync python -m shop preset <name>`. It works for the local shop and for
  your own space on the shared instance alike. The labs that change the preset reset it in their last step.
- **Claude Code, Codex and GitHub Copilot** all work. Where they differ, a step shows a table with one column per
  agent. The facilitator demonstrates with Claude Code.
- **If your agent fails** mid-lab, every lab links to a recorded walkthrough of the same lab in
  [`transcripts/`](../transcripts/README.md). Follow along there, and rejoin at the next module.
- **Stretch goals** are for when you finish early. Nothing later depends on them.

Words you have not met before are in the [glossary](../GLOSSARY.md).
