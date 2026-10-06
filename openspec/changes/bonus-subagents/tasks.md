## 1. Contract, pointers and references on `main`

- [ ] 1.1 Add `"bonus-3-subagents": ("Bonus 3", 60, "drift_and_bug")` to `BONUS` in `tools/check_labs.py`, the Bonus 3 row and the new intro sentence to `labs/README.md`, and one sentence to Lab 7's stretch goal A that points to Bonus 3 (design D1, D12). Verify:
  - `tools/check_labs.py` reports only the missing `labs/bonus-3-subagents/` until 2.1 exists;
  - Lab 7's diff is that one sentence;
  - the site's sidebar shows three bonus labs after 2.1.
- [ ] 1.2 Add `analyze code` to `docs/robotcode.md`: the row, the *Analyze* section with the example on `tests resources`, and the `VariableNotFound` trap (design D8). Verify:
  - the example ran with the shop in `clean`, and prints what the page shows, allowing for shortened output;
  - `tools/check_labs.py` passes.
- [ ] 1.3 Add *Static analysis* to `GLOSSARY.md`, with a *Read more* line for Robocop's and RobotCode's documentation, and name `analyze` and Robocop in the comment on `robotcode[all]` in `pyproject.toml` (design D9, D12). Verify:
  - each linked URL answers with HTTP 200;
  - `uv lock --check` passes, and `uv.lock` is unchanged;
  - `uv run robocop --version` prints 9.0.0;
  - `uv run robotcode analyze --help` lists `code`.

## 2. The lab

- [ ] 2.1 Write `labs/bonus-3-subagents/INSTRUCTIONS.md` and `checklist.md` (design D2 to D7):
  - the header;
  - the step that takes the suite back to `upstream/main`;
  - one prompt per subagent with its brief, the example to imitate, and a link to the *Install* table of `agents/README.md`;
  - `drift_and_bug` and the run with `broken` excluded;
  - the delegation one test at a time;
  - the analyzer's report, then its `VAR` conversion with the diff first;
  - the run under `clean`, and the reset;
  - a stretch goal: a Robocop configuration the team agrees on, written by the analyzer.

  Verify:
  - `tools/check_labs.py` accepts the header, the sections and the giveaway scan, with the transcript and reference links pending until 3.2;
  - every command in the lab that needs no agent ran;
  - `robocop check` with each of the two rules given by its own `--select` reports the six findings on `main`.

## 3. Rehearsal and reference

- [ ] 3.1 Rehearse Bonus 3 with Claude Code in a fresh clone, through the streaming driver, with the local shop (design D11). Verify:
  - the two subagents were written from the briefs and listed by `/agents`;
  - each of the four failures was handed to `debugger` alone, and its report names cause, evidence, change and result;
  - the tests that fail only on drift pass under `drift_and_bug` and under `clean`;
  - the others still fail, with no expected value, assertion or tag changed;
  - the analyzer reported every finding with a verdict, converted with `ReplaceWithVAR` after showing the diff, and the two rules then report nothing;
  - the suite under `clean` has the same result as before the conversion;
  - the transcript shows `robot-debug` and the REPL, and which driving mode ran;
  - the shop is reset, and the time measured sets *Time* in the lab and in `BONUS`.
- [ ] 3.2 Record the transcript with `tools/transcript.py`, write `solutions/bonus-3-subagents.md`, and add `bonus/bonus-3-subagents/` to a local `solutions` branch, in a `bonus-3-subagents:` commit and a `reference:` commit (design D10). The folder holds the Claude Code subagents as rehearsed, the Codex and Copilot ones with the same instructions, and `suite.patch`. Verify:
  - the transcript scan finds no secret, local path, user or host;
  - `git apply --check suite.patch` passes on `main`;
  - with the patch, the suite under `clean` fails only the two broken tests, and under `drift_and_bug`, with `broken` excluded, only the tests that fail on a defect;
  - the two rules report nothing;
  - the Codex and Copilot files parse like their counterparts in `agents/`.

## 4. Close-out

- [ ] 4.1 Record the rehearsal in `docs/facilitator/rehearsal.md`, and open the `main` pull request. Verify:
  - `openspec validate --all --strict` passes;
  - `tools/check_labs.py` passes without pending links, against the local `solutions` commits;
  - the pull request's checks pass;
  - no file of `bonus/bonus-3-subagents/`, no transcript and no reference page is on `main`.
- [ ] 4.2 After the merge, rebase the Bonus 3 commits of `solutions` onto `main`, run its suite, push with a lease, check the redeploy, and archive the change. Verify:
  - `solutions` passes 30 of 30;
  - the lab, its transcript and its reference page answer with HTTP 200 on the site;
  - the specs gain *The subagents lab*, and the changed *Bonus labs*, *Reference projects of the bonus labs* and *Workshop tool set*.
