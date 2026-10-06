## 1. Contract, site and the day's sentence

- [x] 1.1 Accept bonus labs in `tools/check_labs.py`: a `BONUS` table with the folder, label and estimated minutes, with *Module* starting `Bonus <n> ` and *Time* holding `<n> minutes` and `self-paced` (design D1). Verify:
  - with only the day's labs, it passes as before;
  - a scratch copy with a bonus folder whose *Time* lacks `self-paced` is reported;
  - an unknown folder under `labs/` is still reported.
- [ ] 1.2 Add the *Bonus* category to `website/sidebars.js`, keeping *Labs* to `lab-*`, and a *Bonus labs* table to `labs/README.md` (design D1). Verify: after `npm run reference`, the site builds, and the sidebar shows *Labs* with the nine labs and *Bonus* with the two bonus labs.
- [x] 1.3 Name the bonus chapters in Module 10's Monday plan, in the curriculum and the run sheet (design D7). Verify: the diff of both files is that one addition, and the timetable is unchanged.

## 2. The chapter

- [ ] 2.1 Write `docs/building-with-agents.md` (design D2), add it to *Guides* on the site and to `PARTICIPANT_FILES` in `tools/check_labs.py`. Verify:
  - every URL in it answers with HTTP 200, at Robot Framework 7.5 where it names a version;
  - every command in it ran;
  - `tools/check_labs.py` passes;
  - the site builds.
- [ ] 2.2 Add *Assertion engine*, *PythonLibCore* and *Listener* to `GLOSSARY.md` (design D8). Verify: each entry is at most three lines, and `tools/check_labs.py` passes.

## 3. Bonus 2: a listener that reports to GitHub

- [x] 3.1 Write `labs/bonus-2-tool/INSTRUCTIONS.md` and `checklist.md` (design D4). Verify:
  - `tools/check_labs.py` accepts the lab's header, sections and links, the transcript and reference links pending until 3.3;
  - every command that saves a reference ran.
- [ ] 3.2 Rehearse the lab with Claude Code in a fresh sibling folder (design D6). Verify:
  - the project's unit tests and Robot tests pass;
  - `uv build` builds it;
  - the workshop's suite with the listener in a dry run lists the two tests broken on purpose, sends nothing, and has the same result as without it;
  - the agent loaded the project's `AGENTS.md` and not the clone's.
- [ ] 3.3 Record its transcript, write its reference page, and add the project as `bonus/bonus-2-tool/` to the `solutions` branch (design D5). Verify:
  - the transcript scan finds no secret, local path, user or host;
  - the project's checks pass from the branch checkout.

## 4. Bonus 1: a DemoShop library

- [ ] 4.1 Write `labs/bonus-1-library/INSTRUCTIONS.md` and `checklist.md` (design D3). Verify:
  - `tools/check_labs.py` accepts the lab, the transcript and reference links pending until 4.3;
  - every command that saves a reference ran.
- [ ] 4.2 Rehearse the lab with Claude Code in a fresh sibling folder (design D6). Verify:
  - `uv run pytest` and `uv run robot atest` pass against a freshly reset local shop;
  - `Get Product Price    1    ==    249.99` passes, and `Get Product Price    1    ==    1` fails with AssertionEngine's message;
  - libdoc writes the library's documentation, and `uv build` builds it;
  - the agent loaded the project's `AGENTS.md` and not the clone's.
- [ ] 4.3 Record its transcript, write its reference page, and add the project as `bonus/bonus-1-library/` to the `solutions` branch (design D5). Verify:
  - the transcript scan finds no secret, local path, user or host;
  - the project's checks pass from the branch checkout.

## 5. Close-out

- [ ] 5.1 Push the bonus commits to `solutions` without a force-push, record both rehearsals in `docs/facilitator/rehearsal.md`, and open the `main` pull request (design, migration plan). Verify:
  - `openspec validate --all --strict` and `tools/check_labs.py` pass, the latter without pending links;
  - the pull request's site build passes;
  - no file of the bonus projects is on `main`.
- [ ] 5.2 After the merge, rebase `solutions` onto `main`, check the redeployed site, and archive the change. Verify:
  - both bonus labs, their transcripts and their reference pages answer with HTTP 200 on the site;
  - the specs gain *Bonus labs*, *Reference projects of the bonus labs* and *A guide to building libraries and tools*.
