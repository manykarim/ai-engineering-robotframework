## 1. A visible browser on request

- [ ] 1.1 Move the default of `HEADLESS` from the variable table of `resources/shop.resource` into `Open Shop Browser` (design D1). Verify:
  - in a REPL session started with `-v HEADLESS:False`, `${HEADLESS}` still reads `False` after `Import Resource` of `resources/shop.resource`;
  - `New Browser` logs `"headless": false` there, and in a run with `-v HEADLESS:False`;
  - without the variable, it logs `"headless": true`;
  - `tools/verify_outcomes.py` matches every preset.

## 2. The cheat sheet

- [ ] 2.1 Write `docs/robotcode.md` (design D2). Verify:
  - every example ran in this repository with the shop in `clean`, and its shown output is what it printed, shortened;
  - the piped debugger example ends without input from anyone;
  - no debugger example stops in a test tagged `broken`;
  - the first line names the pinned RobotCode version.
- [ ] 2.2 Link the page, and add it to the participant files (design D2):
  - from Lab 4's opening paragraph, and from the glossary's RobotCode entry;
  - as the third item under *Guides* in `website/sidebars.js`;
  - in `PARTICIPANT_FILES` of `tools/check_labs.py`.

  Verify:
  - `tools/check_labs.py` passes;
  - on a scratch copy with the Module 4 cause written into the page, it reports a giveaway;
  - the site builds, and lists the page under *Guides*.
- [ ] 2.3 Add "run the examples of `docs/robotcode.md` again" to the maintainers' checklist in `SETUP.md` (*changing a pinned version*). Verify: `setup-check`'s guide references still resolve.

## 3. Lab 4 and the facilitators

- [ ] 3.1 Add one sentence to Lab 4's REPL step: an output directory the agent passes with `-d` must exist (design D3). Verify:
  - `git diff` shows that sentence and the link of 2.2, and no other change to the steps;
  - the checklist is unchanged, and `tools/check_labs.py` passes.
- [ ] 3.2 Add two entries to the triage playbook's *Not caught by the check* (design D3):
  - an agent waiting at the `(rdb)` or REPL prompt, or reaching for tmux on Windows, and the piped form to ask for;
  - the REPL's `FileNotFoundError` for `playwright-log.txt`, and the fix.

  Verify: each entry names the symptom as the participant sees it, and the piped command it gives ends without input.

## 4. One boundary between Tier 3 and Tier 4

- [ ] 4.1 Update the glossary's ladder and its entries *Tier* and *MCP* (design D4). Verify:
  - "without live access" no longer appears;
  - each entry grew by at most one sentence;
  - `tools/check_labs.py` passes.
- [ ] 4.2 Update the curriculum (design D4):
  - Module 4's `robot-debug` habit;
  - the Module 5 debrief;
  - Module 6;
  - the tooling table's RobotCode and MCP rows.

  Verify:
  - "couldn't peek at the live page" and `pip install robotcode` no longer appear;
  - the tier names and module titles are unchanged;
  - the site builds.
- [ ] 4.3 Rewrite Lab 6's opening paragraph (design D4). Verify:
  - it names what the MCP server adds to Lab 4's REPL, and no longer says the agent never saw the page;
  - `tools/check_labs.py` passes.

## 5. Rehearsal

- [ ] 5.1 Rehearse Lab 4's step 6 again with Claude Code, in a clone at the state after step 5 (design D5). Verify:
  - the agent opens a visible browser with `-v HEADLESS:False` and no workaround (`"headless": false` in its output);
  - it writes no test file, and names keywords and locators for the price range;
  - Lab 4's checklist items for step 6 hold.
- [ ] 5.2 Replace step 6 and its caveat in `transcripts/lab-04-robotcode.md` with the new run, and record the run in `docs/facilitator/rehearsal.md`, including why the Codex run of Lab 4 still stands. Verify:
  - the transcript scan finds no secret, local path, user or host name;
  - `tools/check_labs.py` passes.

## 6. Close-out

- [ ] 6.1 Run the repository's checks. Verify:
  - `openspec validate --all --strict`, `tools/check_labs.py`, `tools/verify_outcomes.py` and the site build pass;
  - no commit contains `docs/robotcode-reports/` or any other part of the report.
- [ ] 6.2 Archive after the merge. Verify: `workshop/facilitation` gains *A RobotCode cheat sheet* and *One boundary between Tier 3 and Tier 4*, and `workshop/baseline-suite` gains *A visible browser on request*.
