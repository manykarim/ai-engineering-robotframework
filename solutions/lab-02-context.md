# Lab 2 - Context: the reference

[Lab 2](../labs/lab-02-context/INSTRUCTIONS.md) has you write `AGENTS.md`, move one section into its own file, and
compare a test written before and after. The reference is the rehearsal's result, recorded in the
[transcript](../transcripts/lab-02-context.md).

## The reference

`AGENTS.md`, 31 lines:

```markdown
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
```

The section it moved into its own file, `docs/agent-environment.md`:

```markdown
# Environment

- Install: `uv sync --locked`, then `uv run --no-sync rfbrowser install chromium`.
- Check the environment: `uv run --no-sync python setup-check/check.py`.
- Run the suite: `uv run robotcode robot`. Plain `robot` ignores `robot.toml` and cannot find the shop.
- Run one test: `uv run robotcode robot -t "<test name>"`.
- `-p shared` selects the shared instance: `uv run robotcode -p shared robot`. Without it, the local shop.
- Logs and reports go to `results/`, which git ignores.
```

The stretch goal, `tests/api/AGENTS.md`, which applies only to the API tests:

```markdown
# AGENTS.md

API tests for the demo shop.

- Import `resources/api.resource` and call `Open Shop API` in `Suite Setup`.
- Send requests through its session `shop`, which sends your space in `X-Workshop-Space`.
- Tag every test `api`, with `Test Tags` in the suite settings.
```

## Why it is a good result

- **The checklist's five sections, and nothing else:** environment (one line that points to its own file), system
  under test, conventions, specifications and boundaries.
- **Conventions are a link, not a copy,** so `docs/conventions.md` stays the one place they are written.
- **It says what is true here, not what any agent knows:** that `openspec/specs/shop/` is the reference for expected
  behaviour, and how to reach the shop and read its state. Its environment file adds the commands that differ from a
  plain Robot Framework project.
- **Its boundaries are concrete:** never edit `resources/legacy.resource`, never apply a preset on its own
  initiative, never read `.env`, never install what the repository does not pin.
- **No lists of files, tests or keywords.** The agent finds those itself, and a list would go stale.
- **One line says when to read the split-off file:** before installing anything or running tests.
- **The nested file holds only what API tests need,** where only API tests load it.

## What to debrief

- **The "before" and "after" tests.** In the rehearsal they came out identical: the keyword the test needed already
  existed, and the specification left nothing to guess. Look for what your "before" had to guess: a label it made up
  instead of copying it from `openspec/specs/shop/`, a locator written into the test, or a missing story tag.
- `CLAUDE.md` still holds only `@AGENTS.md`.

## Compare yours

```bash
git fetch upstream solutions
REF=$(git log -1 --format=%H --grep '^lab-02-context' upstream/solutions)
git diff "$REF" -- AGENTS.md docs/agent-environment.md
```

The lines marked `-` are the reference's, the lines marked `+` yours. No `upstream` remote yet? [Add it first](README.md#compare-your-files-with-the-reference).
