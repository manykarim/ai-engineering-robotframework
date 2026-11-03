# Design

## Context

See proposal.md for why. What exists today:

- **Lab 3** (`labs/lab-03-skills/INSTRUCTIONS.md`, 25 minutes):
  - installs the Robot Framework Agent Skills (step 1);
  - has participants copy `skills/template/` into their agent's skill folder (step 5) and rewrite it for one
    convention;
  - checks that the skill loads for a review prompt (step 7) and stays quiet for an unrelated one (step 8).
- **Its only theory** is three lines under the lab's table, and the glossary's *Skill* and *Trigger* entries.
- **`skills/template/SKILL.md`** is a complete skill for convention 1, *Criterion ID first*:
  - a third-person "what" sentence followed by "Use when…";
  - the rule, why, how to apply it, a bundled script with documented exit codes, and examples.
  
  It already follows most of the advice below, so it is the worked example.
- **Lab 3's reference on `solutions`** is a skill for convention 2, *Locators live in resources*. The page must not
  read like it.
- **Where the agents look for skills**, from their documentation, checked 2026-11-03:

  | Folder | Claude Code | Codex | Copilot (CLI, cloud agent, VS Code) |
  |---|---|---|---|
  | `.claude/skills/` | yes | no | yes |
  | `.agents/skills/` | not in its documentation | yes | yes |
  | `.github/skills/` | no | no | yes |

  Sources:
  - code.claude.com/docs/en/skills;
  - learn.chatgpt.com/docs/build-skills;
  - docs.github.com/en/copilot/concepts/agents/about-agent-skills;
  - code.visualstudio.com/docs/copilot/customization/agent-skills.
- **The Lab 3 folders are inconsistent:**
  - Step 1 installs the Robot Framework skills for Copilot into `.claude/skills/`.
  - Step 5 and `docs/environments.md` send Copilot users' own skill to `.github/skills/`.
- **Research sources** (collected 2026-11-03):
  - **Anthropic:**
    - *Skill authoring best practices* (platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices);
    - *Agent Skills overview*;
    - the engineering post *Equipping agents for the real world with Agent Skills*;
    - the `skill-creator` skill (github.com/anthropics/skills).
  - **The Agent Skills standard:** agentskills.io, namely the specification, *Best practices*, *Optimizing
    descriptions*, *Using scripts* and *Evaluating skills*.
  - **OpenAI:** the Codex *Build skills* page.
  - **GitHub:** the Copilot pages on creating skills.
  - **VS Code:** its agent skills page.

## Goals / Non-Goals

**Goals:**
- A participant who has never written a skill can read the page in about ten minutes and write one in Lab 3.
- Every rule on the page has a reason and a source link. The page states only what all three agents share, and names
  each agent where they differ.

**Non-Goals:**
- No reference for frontmatter that only one agent knows. That covers Claude Code's `context: fork`, `paths`, `hooks`,
  `allowed-tools` and `!` commands, and Codex's `agents/openai.yaml`. One sentence links each agent's full list.
- No tooling tutorial for `skill-creator`, `claude plugin eval` or `skills-ref`. They get one line under *Going further*.
- No change to Lab 3's time, steps 1–4 and 6–8, its checklist, the template's skill or script, or anything on
  `solutions`.

## Decisions

**D1. One page, `docs/skills.md`, shaped like `docs/hooks.md`.**
- **Sections:**
  - **Intro.** A skill is a request loaded on demand, as opposed to `AGENTS.md`, which is always loaded, and a hook,
    which is enforced.
  - *How an agent loads a skill*, with a Mermaid flowchart.
  - *What goes in the folder*.
  - *Where your agent finds it*.
  - *Skill, context file, hook, MCP server or subagent?*
  - *Worked example: the template*.
  - *Writing a good skill*.
  - *Evaluate your skill*.
  - *Trust*.
  - *Going further*.
- **Placement:** in the sidebar after `docs/robotcode`, before `docs/hooks`, following the order of the modules.
- **Alternative rejected:** a longer intro section inside Lab 3's instructions. It would push the steps below the fold,
  and Lab 7 set the precedent of a separate page.

**D2. The rules, distilled to about eight, each one line plus its reason.**

The sources agree on these:
1. **The description does all the triggering.** It says what the skill does and when to use it, in the words a
   prompt would contain, in the third person. Agents tend to under-trigger, so name the situations rather than the
   topic.
2. **Cut what the model already knows.** Every line costs context once the skill loads. Keep `SKILL.md` well under
   500 lines.
3. **Explain why**, rather than shouting ALWAYS or NEVER. A model that knows the reason applies the rule to cases you
   did not list.
4. **One job per skill.** A skill that does two jobs triggers for both and does each half-well.
5. **Give a default, not a menu.** Name one tool or one way, with an escape hatch if needed.
6. **Use a script for what must be exact.** Say whether to run it or read it. A script should never prompt for
   input, and its exit codes and output should say what went wrong.
7. **Record the gotchas.** A gotcha is a fact about this repository that a reasonable model gets wrong; this is often
   the most valuable part of a skill. Put the key rule at the top, because after a long session the start of a
   skill is what survives.
8. **Keep references one level deep, and say when to read each.** For example: "Read `references/x.md` when …".

The examples come from convention 1 (the template) or outside the repository, never from convention 2.

**D3. *Evaluate your skill* is brief, and builds on steps 7 and 8.**
- **Three checks:**
  - a prompt that should load the skill;
  - one that should not;
  - the same task with and without the skill, compared on the result rather than on whether the skill loaded.
- **Then a misfire table:**
  - never loads: the description is too vague or uses the wrong words;
  - loads for everything: it is too broad;
  - loads but is ignored: it is too long, or the rule is not at the top.
- **One sentence on the "one session writes, a fresh session tests" loop**, which is the next level, and on keeping
  the test prompts for the next change.
- **Alternative rejected:** a full eval harness. It does not fit Lab 3's 25 minutes, and `skill-creator` exists for
  that.

**D4. Copilot's own skill goes into `.claude/skills/`.**
- **Why:** Copilot reads that folder, and step 1 already relies on it. One folder per agent then appears in both the
  page and the lab. It also means one fewer folder: Claude Code and Copilot share theirs, and only Codex differs.
- **What changes:** step 5's table, `docs/environments.md` and the template's comment.
- **Before the tables change:** re-check in Copilot CLI that a skill copied to `.claude/skills/<name>/` is listed and
  loads.
- **Alternative rejected:** `.agents/skills/`, the folder Copilot and Codex share. Claude Code's documentation does not
  list it, so it would split the two agents most participants use.

**D5. The page states only what the three agents share, with each agent's name where it differs.**
- **What it states:** the two required fields and their rules.
  - `name`: lowercase letters, digits and hyphens, at most 64 characters, matching the folder's name.
  - `description`: at most 1024 characters.
- **Where they differ:** explicit invocation, which is `/name` in Claude Code and Copilot and `$name` in Codex, and
  how the session shows that a skill loaded.

## Risks / Trade-offs

- **The documentation changes faster than the workshop.** Each claim links its source, and the page carries a
  "checked on" date.
- **Copilot might stop reading `.claude/skills/`.** Then step 1 breaks too. The re-check in D4 catches that before the
  workshop, and `.github/skills/` is the fallback.
- **The page could grow into a reference nobody reads.** Mitigations:
  - a size target of about the hooks page's length or shorter;
  - per-agent extras only as links;
  - the rules as a list, not as essays.
- **The page could give Lab 3's answer away.** The `check_labs` no-answers scan runs on the page. A manual read checks
  that convention 2 appears nowhere.
- **The recorded Lab 3 transcript quotes the template's old comment**, which names `.github/skills/`. It stays as
  recorded, like the transcript's older skill names, which the reference page already explains.
