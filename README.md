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
| `AGENTS.md` | The project context every coding agent reads. Deliberately short: Lab 2 builds it out. |
| `shop/` | The pinned shop (`compose.yaml`) and a helper: `uv run --no-sync python -m shop status`. |
| `setup-check/` | The environment check. |
| `robot.toml` | Robot Framework settings and the `local` and `shared` profiles. |
| `openspec/` | Specifications: `shop/*` describes the shop, `workshop/*` this repository. |

## License

See [LICENSE](LICENSE).
