## Why

The curriculum exists only as the master preparation document. Participants need step-by-step labs in which the starting state, the active preset, the time budget and what "done" looks like are all explicit. They need the assets those labs install and configure, and a fallback for when their agent fails mid-lab, which the master document rates as certain to happen to someone. Several decisions made since the document was written also change the labs themselves:

- The shop is now a pinned image.
- UI drift is a preset, not a `drift.py` script.
- OpenSpec is the vehicle of Module 5.
- Self-healing has two paths.

## What Changes

- **One folder per lab**: `labs/lab-00-arrival`, then `lab-02-context` through `lab-09-ci`, each with `INSTRUCTIONS.md` and `checklist.md`. Every lab states its module, time budget from the timetable, preset, prerequisites, numbered steps, stretch goal, done-criteria and fallback transcript.
- **Module 5 becomes spec-driven.** The participant picks one story - WEB-004 search (easier), WEB-003 product detail (medium) or WEB-005 cart (harder) - scoped to a named slice of three or four criteria. The flow is `/opsx:propose`, a **pair review of the plan** in the breakout (instead of a review of the finished code), `/opsx:apply`, then run and refine. WEB-007 is the documented swap-in if a story proves too hard in dry-run. API-005 is the stretch goal. Only those five story files are copied from demo-webshop, into `labs/lab-05-*/stories/`.
- **Module 8 shows both healing paths.**
  - `robotframework-heal` under `drift_and_bug`: the listener heals the stage-4 drift, and participants triage `heal_report.html` per heal (accept, reject or investigate), while the price and total regressions stay red.
  - The agentic path: Claude Code with `robotcode robot-debug` and rf-mcp repairs a drifted locator in conversation. This is the demo and the stretch goal.
- **Lab assets**:
  - `skills/template/` (Lab 3) and `skills/jira-ticket/` (Lab 7 stretch B);
  - `hooks/`: run the affected suite after an edit, reject inline locators, block commits on red;
  - `agents/`: writer, reviewer, runner;
  - `mcp/`: rf-mcp configuration snippets for Claude Code, Codex and Copilot, including the shared-instance space.
- **Facilitation**:
  - `GLOSSARY.md` and `docs/environments.md`;
  - `docs/facilitator/`: the run sheet, the preset for each module, the cold-open script, the cut order from the master document's risk table, and the triage playbook;
  - `transcripts/`: one recorded agent walkthrough per lab, captured during the dry-runs.
- **A `solutions` branch** with reference solutions per lab in the same structure, produced during the dry-runs and never merged into `main`.
- **Dry-run evidence as a gate**:
  - every lab run end to end on a clean machine with the pinned stack;
  - Lab 5 run explicitly **without** MCP, as the master document demands;
  - Labs 2-4 spot-checked with a second agent.

## Capabilities

### New Capabilities
- `workshop/labs`: the lab folder contract and each lab's starting state, preset, time budget and done-criteria.
- `workshop/lab-assets`: the skills, hooks, subagent definitions and MCP snippets the labs use.
- `workshop/facilitation`: glossary, facilitator guide, cold-open script, cut order and fallback transcripts.
- `workshop/solutions`: the reference-solutions branch and its relationship to `main`.

### Modified Capabilities
None.

## Impact

- **New files**: `labs/`, `skills/`, `hooks/`, `agents/`, `mcp/`, `transcripts/`, `GLOSSARY.md`, `docs/environments.md`, `docs/facilitator/`; the `solutions` branch.
- **Depends on** `workshop-foundation`, `shop-specs` and `baseline-suite`.
- **Decides in its design** which spec namespace participants' Module 5 changes write to, so their work never mixes with `shop/*` or `workshop/*`.
- **Not in scope**: workflows, issue templates and the documentation site (`ci-and-site`).
