# Tasks

## 1. Main

- [x] 1.1 On a branch `apply-update-agentskills` from `main`, change `rf-agentskills@0.6.0` to `rf-agentskills@0.7.0` in `labs/lab-03-skills/INSTRUCTIONS.md` (step 1). In `SETUP.md`'s *Agent plugins and skills* table, change the version column to content `2.0.0`, installer `rf-agentskills` 0.7.0, and the command to `@0.7.0` (design.md, D1). Verify:
  - PyPI still lists 0.7.0 as the latest stable `rf-agentskills`. If a newer final release has appeared, stop and ask;
  - `git grep -n "rf-agentskills@0\.6\|rf-agentskills\` 0\.6"` on the branch finds nothing outside `openspec/changes/archive/`;
  - `uvx rf-agentskills@0.7.0 install --agent <agent> --scope project --project . --what skills --dry-run --no-input` succeeds for `claude-code`, `codex` and `copilot`, and writes to the folders Lab 3's table names.
- [ ] 1.2 Open a pull request to `main` that names the content break (skills renamed `rf-*`, generator skills retired) for anyone who installed 0.6.0. Verify: "Run tests" and "Build the site" pass. Then merge it, and verify `git show origin/main:SETUP.md` names 0.7.0.

## 2. Lab 3's result on solutions

- [ ] 2.1 Note the tip of `origin/solutions` for the lease. Rebase `solutions` onto the new `origin/main`, with a sequence editor that marks the commits `lab-03-skills: ...` and `reference: one page per lab ...` as `edit` (design.md, D2 and D4). Verify: the rebase stops at `lab-03-skills` with no conflict.
- [ ] 2.2 At that stop, in WSL, clone the repository below `/tmp`, check out the same commit, and run Lab 3's command with 0.7.0 there: `uvx rf-agentskills@0.7.0 install --agent claude-code --scope project --project . --what skills --no-input` (design.md, D3). Copy the resulting `.claude/` and `.rf-agentskills/` back over the stop's working tree. Remove any 0.6.0 skill folder or support file that is left, then `git add -A .claude .rf-agentskills`, `git commit --amend --no-edit`, and `git rebase --continue`. Verify:
  - `.claude/skills/` holds exactly the 12 `rf-*` skills and `locators-in-resources`;
  - `locators-in-resources` is byte-identical to the old commit's;
  - `.rf-agentskills/installed.json` records `bundle_version` 0.7.0, and every path in it exists;
  - no installed file contains a Windows path, and `grep -r "libdoc-search\|keyword-builder\|rf-tools" .claude` finds nothing;
  - the commit's message and position are unchanged.
- [ ] 2.3 At the stop at the reference commit, update `solutions/lab-03-skills.md` (design.md, D4): replace the 0.6.0 skill list with the 12 `rf-*` names, give Codex's folder as `.agents/skills/` and Copilot's as `.claude/skills/`, and add one sentence saying the transcript was recorded with 0.6.0, whose skills had other names. Amend and continue the rebase. Verify:
  - the rebase finishes, and `git log --oneline origin/main..solutions` shows the same commit subjects in the same order as before;
  - `git range-diff` shows changes only in those two commits;
  - `transcripts/` is unchanged.

## 3. Check and publish solutions

- [ ] 3.1 On the rebased `solutions`, run both of the reference page's debrief prompts in fresh, headless Claude Code sessions (`claude -p ... --output-format stream-json --verbose`). Verify: the review prompt loads `locators-in-resources` and the `reset` prompt does not. Also note which `rf-*` skills load. If the participant's skill no longer loads, stop and decide with the user (design.md, Risks).
- [ ] 3.2 Install with `uv sync --locked`, reset the shop, and run the whole suite with `uv run robotcode robot`. Verify: every test passes, including the two that `main` ships broken.
- [ ] 3.3 Push with `git push --force-with-lease=solutions:<tip from 2.1> origin solutions`. Verify: `origin/solutions` is the rebased tip, `origin/main` is its ancestor, and the site's deployment after the push succeeds and shows the new skill list on the Lab 3 reference page.

## Workflow follow-up

- Archive the change on a branch `archive-update-agentskills` after the merge, and rebase `solutions` again once the archive lands on `main`.
