# Tasks

All work on `main` happens on a branch `apply-lab-07-hooks-intro` from `main`.

## 1. Hooks

- [x] 1.1 Add `# robotcode: ignore[variable-not-found]` to the `${HEADLESS}` line of `resources/shop.resource`
  (design.md, D3). Update `docs/robotcode.md`: the *Analyze* example output, and the trap row, which now says the
  line is already marked. Verify:
  - `uv run --no-sync robotcode analyze code tests resources` reports `Errors: 0` and exits 0;
  - `uv run robotcode robot --exclude broken` against a clean shop passes as before.
- [x] 1.2 Write `hooks/static_check.py` (D2), in the style of the other hooks, with a module docstring that says
  how to use it as a hook and as a command. Verify:
  - as a command over `tests resources`, it prints nothing and exits 0;
  - on a scratch copy of a test file with a misspelled keyword, it prints only that file's `[ERROR]` line(s) and
    exits 1;
  - fed a recorded hook payload for each agent (Claude Code `Edit`, Codex `apply_patch`, Copilot `edit`), it answers
    in that agent's form;
  - a non-Robot file, or a file outside `tests/` and `resources/`, gives no output.
- [x] 1.3 Teach `hooks/hookio.py` session start and `context()` (D4), and update its docstring table. Verify: a
  session-start payload from each of the three agents parses to `kind == "session"`. `context()` prints plain text
  for Claude Code and Codex, and `{"additionalContext": ...}` for Copilot. The existing three hooks behave
  unchanged on their recorded payloads.
- [x] 1.4 Wire the static check in `hooks/claude-code.settings.json`, `hooks/codex.hooks.json` and
  `hooks/copilot.hooks.json`, after an edit and before `run_affected_tests.py`, with a 60 s timeout (`timeoutSec`
  for Copilot). Update `hooks/README.md`: the table of four scripts, and `static_check.py` under *Without an agent*.
  Verify: every wiring file parses as JSON, and `hooks/README.md` names all four scripts.

## 2. The page and the site

- [x] 2.1 Add Mermaid to the site (D7): `@docusaurus/theme-mermaid` at the core's exact version in
  `website/package.json` and the lockfile, plus `markdown.mermaid`, `themes` and `themeConfig.mermaid` in
  `website/docusaurus.config.js`. Verify:
  - `npm ci && npm run build` in `website/` succeeds;
  - a CommonMark `.md` page with a `mermaid` block shows an SVG diagram in the built HTML, not the source;
  - other code blocks still render as code;
  - `${SHOP_URL}` in prose still renders literally.
  - If Mermaid does not render in `.md`, stop: use the ASCII fallback, and drop the docs-site delta after asking
    the user.
- [x] 2.2 Write `docs/hooks.md` (D1, D2, D4, D5) and add it to *Guides* in `website/sidebars.js`. It contains:
  - the loop as one Mermaid diagram;
  - the shared events table with links to each agent's documentation;
  - how a hook answers;
  - wiring side by side;
  - the "any edit" and "`.robot`/`.resource` only" examples;
  - the static check explained, with `robotcode robot --dryrun` as the next rung and why plain `robot` fails;
  - the session-start context example;
  - the menu, and how to unwire a hook.

  Verify:
  - the site builds with no broken link or anchor;
  - `uv run --no-sync python tools/check_labs.py` passes, including its no-answers scan;
  - every command on the page runs as shown.
- [x] 2.3 In `GLOSSARY.md`, link `docs/hooks.md` from the *Hook* entry, next to the existing Claude Code link. Name
  Codex's and Copilot's hook documentation too, labelled with whose they are. Verify: the site builds, and the
  facilitation scenario "Reading on after the day" holds for hooks in all three agents.

## 3. Lab 7 and the timetable

- [x] 3.1 Rewrite `labs/lab-07-hooks-toolbelt/INSTRUCTIONS.md` with the ten steps of D6:
  - step 1 sends the participant to `docs/hooks.md`;
  - step 3's prompt gains a misspelled keyword for the static check;
  - step 4 gives the prompt for the agent to write and wire a hook from the menu, and a prompt to trigger it.

  Update the header's time to 30 minutes and the fallback line's step numbers. Add the two own-hook items to
  `checklist.md` (D6). Verify: `uv run --no-sync python tools/check_labs.py` passes with Lab 7 at 30 minutes, and
  the site builds.
- [x] 3.2 Update the timetable (D6):
  - the table and the Module 7, 8 and 9 headings in `docs/WWWW_Workshop_Master_Preparation.md`, and its line
    "Self-healing at 15:45";
  - the rows of Modules 7, 8 and 9 in `docs/facilitator/run-sheet.md`, including Module 7's demo cell (the static
    check) and fallback step numbers;
  - `labs/README.md`'s Lab 7 row;
  - the minutes in `tools/check_labs.py`.

  Verify:
  - `tools/check_labs.py` passes;
  - the run sheet's times add up from 15:05 to 17:00 without a gap;
  - the Module 7 to 9 numbers agree in all four files.

## 4. Check in every agent

- [x] 4.1 In a fresh clone at a short path (`C:\workspace\h7` on Windows; WSL's agents are too old), with the shop
  clean, wire the four hooks for each agent in turn and run Lab 7's step 3 prompt (D8):
  - Claude Code 2.1.296;
  - Codex 0.165.0, hooks trusted;
  - Copilot 1.0.92, interactive in a trusted folder.

  Verify in each: the locator edit is refused; the misspelled keyword comes back from the static check within
  seconds; the smoke edit comes back with one failed test; the commit is blocked.
- [x] 4.2 Run the page's session-start example in each agent, and ask the new session which presets hold. Verify:
  each answers from the added context without running a command.
- [x] 4.3 Start Copilot in a clone where only `.claude/settings.json` carries the hooks, and make an edit that a
  hook refuses (D8). Record whether Copilot runs them. If it does, add the "wire only your agent's file" advice to
  `docs/hooks.md` and `hooks/README.md`. Record the result, and the agent versions, in
  `docs/facilitator/rehearsal.md` under *Hooks*.
- [x] 4.3a Remove `MultiEdit`, which the latest Claude Code no longer has (D8): from the Claude Code matcher, from
  `hooks/hookio.py` and from `tools/transcript.py`. Verify: `git grep MultiEdit` finds it only in this change's
  artifacts, and the hooks behave unchanged on recorded `Write` and `Edit` payloads.
- [x] 4.4 Open a pull request to `main` with groups 1 to 4. Verify: "Run tests" and "Build the site" pass. Merge it
  after the user agrees.

## 5. Solutions

- [x] 5.1 Note the tip of `origin/solutions`. Rebase `solutions` onto the new `main`, with a sequence editor that
  marks as `edit`:
  - `lab-07-hooks-toolbelt`;
  - `reference: one page per lab`;
  - `reference: the transcripts and the facilitators' answer sheet`.

  Verify: the rebase stops at `lab-07-hooks-toolbelt` without a conflict.
- [x] 5.2 Rehearse the new Lab 7 with Claude Code (D9) in a WSL clone of the commit before the stop:
  - record steps, prompts and commands as `workshop.*` lines with the `claude -p --output-format stream-json
    --verbose` events;
  - for the own hook, choose "No shortcut to green";
  - stop before step 9 (filing), as in September.

  Make the stop's commit hold the rehearsal's result:
  - `.claude/settings.json` with the plugin, the four hooks and the own hook;
  - the own hook's script;
  - the moved inline locator.

  Amend with a subject that starts `lab-07-hooks-toolbelt:` and names the own hook. Verify:
  - the checklist holds, except the filing;
  - the own hook refused an edit that adds the `broken` tag;
  - the commit contains no path from the machine.
- [x] 5.3 At the reference stops:
  - update `solutions/lab-07-hooks-toolbelt.md`: the wiring with four hooks plus the own hook, and why the own hook
    is a good one;
  - write `transcripts/lab-07-hooks-toolbelt.md` with `tools/transcript.py` from the recording (`--secrets .env`).

  Verify:
  - `tools/transcript.py` writes without refusing;
  - the transcript holds no local path;
  - the rebase finishes with the same commit subjects in the same order, apart from the Lab 7 subject;
  - `git range-diff` shows changes only in the three stopped commits.
- [x] 5.4 On the rebased `solutions`, run `uv sync --locked`, reset the shop and run the whole suite. Verify: every
  test passes. Then `git push --force-with-lease=solutions:<tip from 5.1> origin solutions`, after the user agrees.
  Verify:
  - `origin/main` is an ancestor of `origin/solutions`;
  - the site's deployment succeeds;
  - the Lab 7 reference page and transcript show the new steps;
  - `docs/hooks` shows its diagram.

## Workflow follow-up

- Archive the change on a branch `archive-lab-07-hooks-intro` after the merge, syncing the three delta specs, and
  rebase `solutions` again once the archive lands on `main`.
