# Contributing

This repository is the workshop's home before, during and after the day, and it improves with every group that
works through it. Fixes to a lab, a better skill, a new lab: all welcome.

## Before you start

- **Questions and ideas** go to [Discussions](https://github.com/manykarim/ai-engineering-robotframework/discussions).
  *Show your setup* is the place for the `AGENTS.md`, skills and hooks you built.
- **A defect of the demo shop** is part of the exercise: file it in your own fork, as Lab 7 does. The shop itself
  lives in [demo-webshop](https://github.com/manykarim/demo-webshop).
- **A problem with the setup** goes into an issue with the *Setup problem* form.

## How a change is made

Every change to this repository goes through [OpenSpec](https://github.com/Fission-AI/OpenSpec), the same
spec-driven flow Lab 5 teaches. `openspec/changes/archive/` shows how this repository itself was built.

1. **Fork** the repository and install it (`SETUP.md`).
2. **Propose** the change with your agent: `/opsx:propose <what you want to change>` (Claude Code),
   `$openspec-propose` (Codex) or `/opsx-propose` (GitHub Copilot). It writes a proposal, specs, a design and
   tasks under `openspec/changes/<name>/`.
3. **Open a pull request with the plan first**, so that the plan can be discussed before anything is built.
4. **Apply** it: `/opsx:apply`. Tick each task only when its verification holds.
5. **Run the checks** below, and open the pull request with the implementation.

Specs live in three namespaces (`openspec/config.yaml`): `shop/*` describes the demo shop and never changes here;
`workshop/*` describes this repository; `suite/*` is for what participants' own tests verify.

## The checks

Run all of them before you ask for a review:

```bash
openspec validate --all --strict                          # the specs and changes
uv run --no-sync python tools/check_labs.py               # the lab contract: times, headers, links, no answers given away
uv run --no-sync python tools/verify_outcomes.py          # the suite under every preset, against the local shop
cd website && npm ci && npm run build                     # the documentation site; broken links fail it
```

`tools/verify_outcomes.py` needs the local shop running (`docker compose -f shop/compose.yaml up -d`), and resets
it when it finishes. The CI workflows run the suite and build the site on every pull request as well.

## Suggesting a new lab or skill

- **A lab** follows the contract in `openspec/specs/workshop/labs/spec.md`: its own folder under `labs/` with
  `INSTRUCTIONS.md` and `checklist.md`, the header table, numbered steps, a stretch goal and a fallback transcript.
  `tools/check_labs.py` checks most of it. A lab needs a rehearsal and a transcript before it counts as done
  (`docs/facilitator/rehearsal.md`).
- **A skill** starts from `skills/template/` and enforces something `docs/conventions.md` says. Check that it
  triggers on a matching prompt and stays quiet on an unrelated one.

## Rules of the repository

- **No secrets.** Keys and tokens belong in `.env`, which git ignores, or in your fork's Actions secrets. Never in a
  file, an issue or a transcript.
- **Pinned versions.** Python dependencies come from `uv.lock`, the shop from `shop/compose.yaml`, actions by
  commit SHA. A version change is its own OpenSpec change, with `setup-check` and the outcome matrix updated.
- **Labs do not give answers away.** The planted defects, the causes of the broken tests and the inline locator
  are for facilitators only (`docs/facilitator/`).
