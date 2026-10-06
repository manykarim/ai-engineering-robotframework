## Why

Module 7 names subagents, but on the day they get only a stretch goal: three ready-made subagents (writer, reviewer, runner) that participants install. No lab has participants write a subagent themselves, decide what it may and may not do, and hand it real work.

Two jobs fit a subagent well, because they produce a lot of output that the main conversation does not need:
- **Debugging a failing test** at a live breakpoint, with `robotcode robot-debug` and `robotcode repl`. Labs 4, 5 and 8 do this in the main conversation, one test at a time.
- **Analysing the suite statically**, with `robotcode analyze code` and Robocop, and converting outdated syntax with Robocop's own fixes, such as `Create List` to `VAR`. No lab uses either tool yet.

The workshop is today, 2026-10-07, so this is a third self-paced bonus lab for after the day, next to Bonus 1 and Bonus 2.

## What Changes

- **Bonus 3, subagents:** `labs/bonus-3-subagents/`, self-paced, in the participant's workshop clone. Participants have their own agent write two subagents from a brief in the lab, imitating the `runner` of `agents/`:
  - **`debugger`** debugs one failing test per call:
    - it reads the recorded failure first;
    - it stops at the failure with `robotcode robot-debug` and inspects the live page;
    - it tries a candidate fix at the paused prompt or in `robotcode repl` before writing it into a file;
    - it repairs the test onto the stable contract, and runs it again.
    - It never changes an expected value to agree with the shop. When the shop contradicts its specification, it reports a defect with the evidence instead.
  - **`analyzer`** runs `robotcode analyze code` and `robocop check` and sorts every finding into fix, keep or false positive, with a reason for each. It has no tool to edit files: it changes them only through Robocop's fixes and formatters, shows the diff before it writes, and runs the suite afterwards.
  - The lab applies `drift_and_bug`, and the main agent hands each failed test to the `debugger`, one at a time. Back in `clean`, the `analyzer` converts the suite's `Create List`, `Create Dictionary` and `Catenate` assignments to `VAR`.
- **The lab contract** gains the third bonus folder. Bonus labs no longer all build a project outside the clone: Bonus 1 and 2 do, and Bonus 3 works inside it.
- **The solutions branch** gains `bonus/bonus-3-subagents/`, plus Bonus 3's transcript and reference page:
  - the two subagents in the format of each supported agent;
  - the rehearsal's changes to the suite as a patch against `main`.
- **The tool set** names what Bonus 3 relies on, all already in the locked environment through `robotcode[all]`:
  - `robotcode analyze`;
  - Robocop, 9.0.0 in `uv.lock`.
- **Pointers:**
  - Lab 7's stretch goal A points to Bonus 3;
  - `labs/README.md` lists Bonus 3;
  - the RobotCode cheat sheet gains `analyze code`, with its one false positive on this suite;
  - the glossary gains *Static analysis*.
- **Rehearsal:** Bonus 3 is rehearsed with Claude Code before it counts as done.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `workshop/labs`:
  - *One folder per lab* adds `bonus-3-subagents`;
  - *Bonus labs* separates the two labs that build a project from the one that works in the clone;
  - new: *The subagents lab*.
- `workshop/solutions`: *Reference projects of the bonus labs* covers Bonus 3's result. It has no project, so the result is the two subagents and a patch.
- `workshop/toolchain`: *Workshop tool set* adds RobotCode's static analysis and Robocop.

## Impact

- **New on `main`:** `labs/bonus-3-subagents/INSTRUCTIONS.md` and `checklist.md`.
- **Changed on `main`:**
  - `tools/check_labs.py`: the `BONUS` table;
  - `labs/README.md`: the Bonus table;
  - `labs/lab-07-hooks-toolbelt/INSTRUCTIONS.md`: one sentence in stretch goal A;
  - `docs/robotcode.md`: the *Analyze* section and one table row;
  - `GLOSSARY.md`;
  - the dependency comment in `pyproject.toml`. `uv.lock` is unchanged;
  - `docs/facilitator/rehearsal.md`.
- **New on `solutions`:**
  - `bonus/bonus-3-subagents/`;
  - `solutions/bonus-3-subagents.md`;
  - `transcripts/bonus-3-subagents.md`.
- **Unchanged:**
  - the timetable, the run sheet and Module 10's Monday plan;
  - the suite and its outcomes under every preset;
  - `agents/` and its three subagents;
  - `setup-check`;
  - the locked environment.
- **Risk to the day:** the changes to `main` are additive text. Lab 7 changes by one sentence in a stretch goal. The site build and `tools/check_labs.py` check everything before the merge.
