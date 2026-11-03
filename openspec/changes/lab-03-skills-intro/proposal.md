## Why

Lab 3 explains skills in three lines at the top of its instructions, plus two glossary entries. Participants copy a
template and rewrite it without learning how an agent finds and loads a skill, what makes a description trigger, or
what separates a good skill from a long prompt. Lab 7 got an introduction page for hooks; skills deserve the same,
grounded in what the agents' own documentation and the Agent Skills standard recommend today.

## What Changes

- **A skills page, `docs/skills.md`**, on the site under *Guides*, next to the hooks page. Lab 3 sends participants
  there first. It covers:
  - what a skill is, and where it sits next to `AGENTS.md`, hooks, MCP servers and subagents: one table, when to use
    which;
  - how an agent loads a skill, as one Mermaid diagram: names and descriptions at the start, the body when a task
    matches, the folder's other files only when the body points to them;
  - what goes in the folder: `SKILL.md` with its two required fields and their rules, and `scripts/`, `references/`
    and `assets/`;
  - where each agent finds skills, side by side, and how a participant sees that one loaded;
  - the worked example: `skills/template/`, explained part by part;
  - how to write a good skill: a short list of rules, each with its reason, distilled from Anthropic's authoring
    guide, the Agent Skills standard and the Codex and Copilot documentation, with links;
  - a brief *Evaluate your skill* section: prompts that should and should not load it, the same task with and without
    the skill, and what to change when it misfires;
  - trust: a skill is code and instructions you run, so read it before installing it.
- **Lab 3's folder for Copilot.** Copilot reads `.claude/skills/`, as Lab 3's step 1 already relies on. Step 5 sends
  Copilot users there as well instead of to `.github/skills/`, so the lab and the page name one folder per agent:
  - `labs/lab-03-skills/INSTRUCTIONS.md`: step 5's table; the lab's intro paragraph links the page;
  - `docs/environments.md`: the "your own skill" row;
  - `skills/template/SKILL.md`: the folder list in its comment.
- **The glossary's** *Skill* and *Trigger* entries link the new page.
- **Nothing changes on `solutions`.** The Lab 3 reference uses `.claude/skills/`, and the recorded transcript keeps the
  template's old comment as it was recorded.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `workshop/lab-assets`: new requirement *A skills page for newcomers*, like *A hooks page for newcomers*.

## Impact

- **New on `main`:** `docs/skills.md`.
- **Changed on `main`:**
  - `labs/lab-03-skills/INSTRUCTIONS.md`;
  - `skills/template/SKILL.md`, its comment only;
  - `docs/environments.md`;
  - `GLOSSARY.md`;
  - `website/sidebars.js`.
- **Unchanged:**
  - Lab 3's time budget, checklist and reference;
  - the template's skill itself, its script and its behaviour;
  - the suite's tests and their outcomes.
- **Risks:**
  - Skill formats keep changing; the page names only what all three agents share, and links each agent's
    documentation for the rest.
  - Copilot reading `.claude/skills/` is checked again in Copilot CLI before the lab's table changes.
  - The page must not give Lab 3's answer away: its examples use convention 1, which the template already covers,
    never convention 2.
