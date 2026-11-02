## Why

Lab 7 starts with "copy this file". Participants wire three hooks that are already written, watch them fire, and move
on. Nothing explains what a hook is, when an agent calls it, or how to write one, and no step has participants
write a hook of their own. The glossary's two lines and a link to one agent's guide are all the theory there is.
Hooks are the cheapest guardrail a team can add on Monday, so participants should leave able to write one for
every agent they use.

## What Changes

- **A hooks page, `docs/hooks.md`**, on the site under *Guides*. Lab 7 sends participants there first. It covers:
  - what a hook is, and the agent loop with the points where a hook can act, as one Mermaid diagram;
  - the events Claude Code, Codex and GitHub Copilot share: session start, before a tool, after a tool and stop,
    with each agent's name for them, what each can do, and a link to each agent's full list;
  - how a hook answers: refuse with a reason, report a result, add context;
  - the wiring for each agent side by side, and what differs: event and tool names, the command and timeout keys;
  - small examples: after any file edit, and after an edit to a `.robot` or `.resource` file only;
  - the worked example, the static check below, explained step by step;
  - a menu of hooks worth writing for Robot Framework work, and how to write one on top of `hookio.py`.
- **A fourth provided hook, `hooks/static_check.py`**. After an edit to a `.robot` or `.resource` file, it runs
  `robotcode analyze code` on that file. It stays silent when the file is clean. On findings, it returns only the
  error lines, a few at most, so a check costs seconds and few tokens. It is wired for all three agents in the
  provided wiring files, and the facilitator demonstrates it in Module 7's talk. The page explains why it calls
  `robotcode` and never plain `robot --dryrun`: plain `robot` ignores `robot.toml` and fails every test file.
- **`hookio.py`** gains a way to add context to the conversation in each agent's form, so a session-start hook
  works in all three agents.
- **The `${HEADLESS}` false positive** of `analyze code` in `resources/shop.resource` is silenced with RobotCode's
  ignore comment. Otherwise the static check would flag every edit of that file.
- **Lab 7** has these steps:
  - read the page;
  - wire the four hooks;
  - try them, including a misspelled keyword that the static check catches;
  - write a hook of your own with your agent, from the page's menu, then wire and trigger it;
  - then, as today, the suite scan, the `buggy` run and the issue filed with `gh`.
  The lab's time grows from 20 to 30 minutes, and its checklist gains the own hook.
- **The timetable:** Module 7 grows to 50 minutes (15/30/5). The time comes from Module 8's demo (15 to 10 minutes)
  and Module 9's talk (15 to 10 minutes), so the day still ends at 17:00. Their content is unchanged; the times are
  estimates. This is reflected in the master document, the run sheet and the lab contract check.
- **The site** renders Mermaid diagrams. The glossary's *Hook* entry links the new page.
- **On `solutions`:**
  - the `lab-07-hooks-toolbelt` commit gains the static check's wiring and the rehearsal's own hook;
  - the Lab 7 reference page explains that hook;
  - Lab 7 is rehearsed again with the new steps, and its transcript is replaced.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `workshop/lab-assets`:
  - *Hooks as guardrails* adds the static check, so there are four hooks;
  - *Hooks for every supported agent* adds the hooks page and adding context.
- `workshop/labs`:
  - *What every lab states up front* changes Lab 7's time budget to 30 minutes;
  - new: *Module 7 has participants write a hook*.
- `workshop/docs-site`: *Markdown as written* renders Mermaid code blocks as diagrams.

## Impact

- **New on `main`:**
  - `docs/hooks.md`;
  - `hooks/static_check.py`.
- **Changed on `main`:**
  - `hooks/hookio.py`, `hooks/README.md` and the three wiring files;
  - `resources/shop.resource`, by one comment;
  - `labs/lab-07-hooks-toolbelt/INSTRUCTIONS.md` and `checklist.md`;
  - `GLOSSARY.md`;
  - `docs/robotcode.md`: the trap row about the false positive;
  - the timetable: `docs/WWWW_Workshop_Master_Preparation.md` and `docs/facilitator/run-sheet.md`;
  - `tools/check_labs.py`;
  - `docs/facilitator/rehearsal.md`;
  - the site: `website/package.json`, the lockfile, `docusaurus.config.js` and `sidebars.js`.
- **Changed on `solutions`:**
  - the `lab-07-hooks-toolbelt` commit;
  - `solutions/lab-07-hooks-toolbelt.md`;
  - `transcripts/lab-07-hooks-toolbelt.md`.
- **Unchanged:**
  - the suite's tests and their outcomes under every preset;
  - the three existing hooks' behaviour;
  - Modules 8 and 9's content and labs;
  - `uv.lock`: `robotcode analyze` is already locked.
- **Risks:**
  - Hook formats are young and keep changing. Every provided hook is checked again in all three agents.
  - Copilot's documentation now says it also reads hooks from `.claude/settings.json`, which the September
    rehearsal did not see. If true, a participant who wires both files gets every hook twice.
