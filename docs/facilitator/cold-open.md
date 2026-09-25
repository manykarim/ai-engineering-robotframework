# Cold open

*Facilitator material.* The first five minutes of Module 1: the destination before the theory. One prompt becomes a
green test, the shop's layout drifts and breaks the suite, and the suite heals itself. No slides.

**It may not flake.** Rehearse it until it is boring. If any step does not show its expected output, do not debug it
on stage: switch to the recorded backup, `transcripts/cold-open.md`, which you keep open in a browser tab.

## Before the session (T-15 minutes)

On your own machine, in your clone of the repository, with the local shop running:

```bash
uv run --no-sync python -m shop reset
git status                      # clean working tree
uv run --no-sync python setup-check/check.py
```

`setup-check` must show *Healing endpoint* as passed: the cold open heals with your own `HEAL_*` settings in `.env`.

Rehearsed it in this clone already? Then `results/heal/history.sqlite` remembers the repairs, and the live run reuses
them without asking the model: faster and deterministic, and the console says *"proactively replaced known-broken
locator ... (from history)"*. Keep it for a safe run on stage, or `rm -rf results/heal` for a fresh heal.

Open three windows side by side: a terminal, your agent (Claude Code) in the repository root, and the shop in a
browser at `http://localhost:9090/products`. Open `transcripts/cold-open.md` in a browser tab and leave it there.

## The five minutes

| # | Say | Do | Expected |
|---|---|---|---|
| 1 | "Here is a user story criterion. Let's hand it to an agent." | Give Claude Code the prompt below. | The agent reads the spec and the conventions, adds a keyword to a resource and a test in `tests/ui/cold_open.robot`, runs it: **1 test, 1 passed**. |
| 2 | "Now the shop gets a redesign overnight." | `uv run --no-sync python -m shop preset stage4`, then reload the shop in the browser. | The page looks the same to a person. |
| 3 | "And the suite?" | `uv run robotcode robot --exclude broken` | **12 tests, 8 passed, 4 failed**: card prices, audio filter, order total and successful order. They are all locator failures. Your new test still passes: it uses the stable contract. |
| 4 | "Same suite, unchanged, with a healing listener attached." | `uv run robotcode -p heal robot --exclude broken` | **12 tests, 12 passed.** The console reports each heal in a `heal:` line. |
| 5 | "Every heal is a proposal, not a silent edit." | Open `results/heal/heal_report.html`; then `git status -- tests resources`. | About five heals, each with the old and new locator. `git status` shows only your new test and keyword: the heals changed no file. |
| 6 | "Today you build every piece of this yourself, rung by rung." | Back to the slides: the ladder. | |

The prompt for step 1:

> Write a Robot Framework test for criterion WEB-004_AC-2 of this repository, following docs/conventions.md. Put the
> test in tests/ui/cold_open.robot and any keyword it needs in resources/, then run the test.

## After the session

```bash
uv run --no-sync python -m shop reset
git checkout -- resources && rm -f tests/ui/cold_open.robot
```

## Why these steps

- `stage4` drifts every fragile locator kind at once and switches on no planted defect. Everything the drift breaks
  can heal. Module 8 later adds the defects, and shows that healing does not hide them.
- WEB-004_AC-2 is outside every lab slice, so the cold open solves nobody's exercise.
- The heal count varies between models and runs. The pass count does not. Say "about five heals".
