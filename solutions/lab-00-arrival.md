# Lab 0 - Arrival: the reference

[Lab 0](../labs/lab-00-arrival/INSTRUCTIONS.md) produces no files: it ends with a working setup. Its
[transcript](../transcripts/lab-00-arrival.md) shows every step.

## What done looks like

- `setup-check` shows no red line. A yellow line for an optional track, such as the Azure CLI, is fine.
- `uv run --no-sync python -m shop status` shows the preset `clean`.
- The first run reports 13 tests: 11 passed and 2 failed. The two failures are `WEB-002_AC-4 Rating Filter` and
  `WEB-002_AC-12 Handpicked Highlights`, both tagged `broken`: they fail on purpose, and Labs 5 and 4 repair them.
- Your agent starts in the repository and answers a question about it from `AGENTS.md`.

## Why it is a good result

Every later lab starts from this state: the pinned tools, the shop in `clean`, and a suite whose only failures are
the two it ships broken. When the run shows more failures, a preset other than `clean` is active, and
`uv run --no-sync python -m shop reset` fixes it.

## What to debrief

Nothing is given away yet. The two failing tests are named here, and their causes are the subject of Labs 4 and 5.

## Compare yours

Compare your `setup-check` output and your first run with the [transcript](../transcripts/lab-00-arrival.md). Your
times and your agent's answer differ; the counts do not.
