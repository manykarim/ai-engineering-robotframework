## Why

The labs teach agents to write and run tests. Many participants also write Robot Framework libraries and tools: keyword libraries for their own systems, listeners, and integrations with test-management services. Agents can do that work well, if they start from the right context.

That context has five parts:
- the toolstack: `uv` for dependencies and packaging;
- the reference that matches the versions in use: the User Guide chapter, the Robot API page, the service's API description;
- the concepts the library must follow, such as AssertionEngine;
- keywords to imitate, such as Browser's;
- a specification to work from.

None of the nine labs covers building a library or tool, and the day has no room for it. The workshop is on 2026-10-07, so these chapters are self-paced afterwards. Module 10 introduces them briefly on the day.

## What Changes

- **A shared chapter:** `docs/building-with-agents.md` covers:
  - the five kinds of context;
  - why the new project starts in a folder outside the workshop clone: the clone's `AGENTS.md`, `CLAUDE.md` and `openspec/` would otherwise leak into it;
  - an `AGENTS.md` skeleton;
  - `openspec init` with that context;
  - the references, pinned to Robot Framework 7.5;
  - saving into the project any reference an agent cannot fetch. TestRail's API manual answers automated requests with 403.
- **Bonus 1, a library:** `labs/bonus-1-library/`. Participants build a Python library for the DemoShop's REST API, with an agent, spec-driven:
  - assertion operators come from AssertionEngine;
  - keywords follow Browser's `Get … == expected` style;
  - the reference is the pinned shop's `/openapi.json`, saved into the project, with the public DemoShop docs for people;
  - the lab compares the library with the user keywords of `resources/api.resource`.
- **Bonus 2, a tool:** `labs/bonus-2-tool/`. Participants build a ListenerV3 that reports failed tests to the public GitHub API as issues in their fork:
  - it runs dry by default, and takes its token from the environment, for example from `gh auth token`;
  - the references are the User Guide's listener chapter, the Robot API pages and GitHub's REST docs.
- **The lab contract** allows bonus labs:
  - folders `bonus-<n>-<name>`, with an estimated time instead of a timetable share;
  - a *Bonus* group on the site and in `labs/README.md`;
  - the same sections and checks as every lab: steps, stretch goal, a reference and a transcript.
- **The solutions branch** holds each bonus lab's reference project under `bonus/<lab folder>/`, with the bonus lab's transcript and reference page. None of it is on `main`.
- **Module 10's Monday plan** names the bonus chapters as a fourth step, in the curriculum and the run sheet.
- **Rehearsal:** both bonus labs are rehearsed today with Claude Code before they count as done.
- **The glossary** gains *Assertion engine*, *PythonLibCore* and *Listener*, as the bonus labs use them.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `workshop/labs`:
  - *One folder per lab* adds the two bonus folders;
  - *What every lab states up front* lets bonus labs state an estimated time;
  - new: *Bonus labs*.
- `workshop/solutions`: new: *Reference projects of the bonus labs*.
- `workshop/facilitation`: new: *A guide to building libraries and tools*.

## Impact

- **New on `main`:**
  - `docs/building-with-agents.md`;
  - `labs/bonus-1-library/` and `labs/bonus-2-tool/`, each with `INSTRUCTIONS.md` and `checklist.md`.
- **Changed on `main`:**
  - `labs/README.md` and `website/sidebars.js`: the *Bonus* group;
  - `tools/check_labs.py`: the bonus labs' contract;
  - `GLOSSARY.md`;
  - the curriculum's Module 10 and the run sheet's Module 10 row;
  - `docs/facilitator/rehearsal.md`.
- **New on `solutions`:**
  - `bonus/bonus-1-library/` and `bonus/bonus-2-tool/`: the rehearsals' reference projects;
  - their transcripts and reference pages.
- **Unchanged:**
  - every lab of the day, its timing, and the timetable;
  - the suite, and its outcomes under every preset;
  - the participant environment. The bonus projects have their own `uv` environments.
- **Risk to the day:** the changes to `main` are additive, and the site build and `tools/check_labs.py` check them before the merge. Tag `main` after this lands.
