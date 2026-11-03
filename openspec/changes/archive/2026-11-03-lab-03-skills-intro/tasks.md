# Tasks

All work on `main` happens on the branch `lab-03-skills-intro`.

## 1. Check the folder first

- [x] 1.1 Check D4 in GitHub Copilot CLI before changing any table:
  - copy `skills/template` to `.claude/skills/criterion-id-first/` in a scratch clone;
  - ask Copilot which skills it has, then give it step 7's review prompt.

  Verify that it lists the skill and loads it. If it does not, stop and revisit D4; `.github/skills/` is the fallback.

## 2. The page

- [x] 2.1 Write `docs/skills.md` with the sections of D1, the rules of D2, the evaluation section of D3 and the shared
  facts of D5:
  - a Mermaid flowchart of how a skill loads;
  - the folder table per agent;
  - the "skill, context file, hook, MCP server or subagent?" table;
  - the template explained part by part;
  - a source link for every rule;
  - a "checked on 2026-11-03" line.

  Verify:
  - the page is no longer than `docs/hooks.md`;
  - convention 2 and the reference skill's wording appear nowhere;
  - every external link answers.
- [x] 2.2 Add `docs/skills` to `website/sidebars.js`, after `docs/robotcode` and before `docs/hooks`. Add
  `docs/skills.md` to `PARTICIPANT_FILES` in `tools/check_labs.py`.

  Verify that `npm run build` in `website/` succeeds and the Mermaid diagram renders in light and dark mode.

## 3. Lab 3 and the links

- [x] 3.1 In `labs/lab-03-skills/INSTRUCTIONS.md`:
  - link the page from the intro paragraph, and tell participants to read it before step 4;
  - change step 5's Copilot column to `cp -r skills/template .claude/skills/locators-in-resources`.
- [x] 3.2 Make the same change to the "your own skill" row of `docs/environments.md`, and to the folder list in the
  comment of `skills/template/SKILL.md`. Leave the skill itself untouched.
- [x] 3.3 Link `docs/skills.md` from the *Skill* and *Trigger* entries of `GLOSSARY.md`.
- [x] 3.4 Verify:
  - `uv run --no-sync python tools/check_labs.py` passes;
  - `openspec validate --all --strict` gives the same result as before;
  - `grep -rn "github/skills"` finds no participant-facing file on `main`.

## 4. Ship

- [x] 4.1 Commit, push the branch and open a PR. Verify that "Build the site" and both "Robot Framework suite" runs pass.

## Workflow follow-up

- After the merge: archive the change, syncing the `workshop/lab-assets` delta into the main spec.
- Rebase `solutions` onto `main` and force-push it with the lease. The `solutions` content is unchanged.
- Check that the live site shows the new page.
