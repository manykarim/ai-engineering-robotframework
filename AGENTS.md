# AGENTS.md

Participant repository of the workshop "Agentic Engineering with Robot Framework".
The system under test is the demo shop, which runs from a published image.

This file is deliberately short: Lab 2 builds it out.

## Setup

- Install: `uv sync --locked`, then `uv run --no-sync rfbrowser install chromium`.
- Check the environment: `uv run --no-sync python setup-check/check.py`.

## The shop

- Local (default): `docker compose -f shop/compose.yaml up -d`, then `http://localhost:9090`.
- Shared instance: set `SHOP_URL` and `SHOP_SPACE` (your GitHub handle) in `.env`.
- Status, presets and resets: `uv run --no-sync python -m shop status`.

## Running tests

- `uv run robotcode robot <path>`; add `-p shared` for the shared instance.
- Plain `robot` ignores `robot.toml` and does not know where the shop is.
