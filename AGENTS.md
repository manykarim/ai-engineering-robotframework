# AGENTS.md

Participant repository of the workshop "Agentic Engineering with Robot Framework": a Robot Framework suite that
tests the demo shop.

Before installing anything or running tests, read docs/agent-environment.md.

## System under test

- The demo shop: a web shop with a UI and an API, run from a published image pinned in `shop/compose.yaml`.
- Local (default): `docker compose -f shop/compose.yaml up -d`, then `http://localhost:9090`.
- Shared: one instance for everyone, one space per participant, configured in `.env`.
- `uv run --no-sync python -m shop status` shows the shop's version, the space and the presets that hold.

## Conventions

Before writing or changing a test or a keyword, read [docs/conventions.md](docs/conventions.md).

## Specifications

- `openspec/specs/shop/` describes what the shop does, one requirement per criterion, such as `WEB-002_AC-5`.
- It is the reference for expected behaviour: assert what the spec says, not what the shop happens to do.
- `openspec/specs/workshop/` describes this repository, not the shop. Tests do not need it.

## Boundaries

- Never edit `resources/legacy.resource`.
- Never apply a preset or reset the shop from a test, nor on your own initiative.
- Never read, print or copy `.env`.
- Never install tools the repository does not pin: no `pip install`, no `rfbrowser init`, no new dependencies.
- Never change `openspec/specs/shop/` to match what the shop does.
