# Agentic Engineering with Robot Framework

The participant repository of the workshop *Agentic Engineering with Robot Framework: From a Markdown File to
a Self-Healing Pipeline*. Over one day, you climb the agentic maturity ladder: context, skills, tooling, live
access, orchestration. Every rung works on its own, and you leave with your own working setup.

The system under test is a small demo shop that runs from a published container image.

## Quickstart

With the [prerequisites](SETUP.md#prerequisites) installed:

```bash
git clone https://github.com/<you>/ai-engineering-robotframework.git   # your fork
cd ai-engineering-robotframework
uv sync --locked
uv run --no-sync rfbrowser install chromium
docker compose -f shop/compose.yaml up -d
uv run --no-sync python setup-check/check.py
```

The last command checks everything the workshop needs, and prints a fix for anything that is missing. The full
guide, including the shared instance for machines without Docker, is [SETUP.md](SETUP.md).

## What is in here

| Path | What |
|---|---|
| `labs/` | The labs of the day, one folder each, with instructions and a checklist. Start at `labs/README.md`. |
| `GLOSSARY.md` | The words of the day, in about ten minutes. |
| `AGENTS.md` | The project context every coding agent reads. Deliberately short: Lab 2 builds it out. |
| `tests/`, `resources/` | The test suite, deliberately imperfect, and its keywords. `docs/conventions.md` says how tests are written here. |
| `skills/`, `hooks/`, `agents/`, `mcp/` | What the labs install: a skill template and a Jira skill, three hooks, three subagents, and the MCP server's configuration for each agent. |
| `transcripts/` | Recorded walkthroughs of the labs, for when your agent fails. |
| `shop/` | The pinned shop (`compose.yaml`) and a helper: `uv run --no-sync python -m shop status`. |
| `setup-check/` | The environment check. |
| `robot.toml` | Robot Framework settings and the `local`, `shared` and `heal` profiles. |
| `openspec/` | Specifications: `shop/*` describes the shop, `suite/*` what your tests verify, `workshop/*` this repository. |
| `docs/` | Conventions, environments and agent choice, and `docs/facilitator/` for the people running the day. |
| `tools/` | Maintainer checks: the lab contract, the suite's expected outcomes, transcripts. |

## License

See [LICENSE](LICENSE).
