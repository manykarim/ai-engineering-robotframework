## Context

See `proposal.md` for the motivation, and `specs/` for the requirements. The facts below were checked on the maintainer's machine on 2026-09-24, not assumed.

- **The repository already ships** the pinned stack, `setup-check`, the shop helper with presets and spaces, the `shop/*` specs, the baseline suite with its outcome matrix, and the `heal` profile. Labs build on these and change none of them.
- **The agents** are Claude Code 2.1, Codex 0.156 and GitHub Copilot CLI 1.0. All three have skills, MCP servers, hooks, custom subagents and plugin marketplaces. They differ in folders and file formats:

  | | Claude Code | Codex | GitHub Copilot |
  |---|---|---|---|
  | skills | `.claude/skills/` | `.agents/skills/` | `.github/skills/` |
  | subagents | `.claude/agents/*.md` | TOML agent files | `.github/agents/*.agent.md` |
  | MCP | `claude mcp add` | `codex mcp add` | `copilot mcp add` |
  | hooks | `.claude/settings.json` | hooks (stable feature) | hooks (plugins and config) |

  OpenSpec's generated skills already use the three skill folders.
- **The RobotCode agent plugin** comes from the marketplace `robotcodedev/robotframework-agent-plugins`, as plugin `robotcode`, for Claude Code, Codex and Copilot alike. The marketplace has no tags, so its latest commit, `7c753f8adca1` of 2026-09-21, is the reference point.
- **The Robot Framework Agent Skills** come from `manykarim/robotframework-agentskills`. Its content is at `v1.2.0`, and its installer `rf-agentskills` at `0.6.0`. The installer takes `--agent <name> --scope project --project <dir>` and `--dry-run`.
- **The MCP server** is `rf-mcp` 0.35.0. It is installed in the project environment and started as `uv run --no-sync rf-mcp`, speaking stdio by default.
- **RobotCode 2.7** offers `discover`, `libdoc`, `robot-debug`, `repl` and `results`: every habit Module 4 teaches.
- **Healing needs a model** (baseline-suite design). Under `drift_and_bug`, the maintainer's run healed 5 locators with 17,079 tokens.

## Goals / Non-Goals

**Goals:**
- A participant can do every lab from its instructions alone, in any of the three agents. They can catch up at every module, and fall back to a transcript when their agent fails.
- Facilitators run the day from `docs/facilitator/` without the master document open.
- Every lab has been done at least once, end to end, before the workshop tag.

**Non-Goals:**
- The workflows and the documentation site (`ci-and-site`). Lab 9 is written here against the workflow contract of `ci-and-site`'s proposal, and rehearsed there.
- Slides, recordings of talks, and the organisers' emails.
- Making every agent behave identically. Where they differ, the labs name the difference.

## Decisions

### D1. The lab contract

Every `INSTRUCTIONS.md` opens with the same table:

| | |
|---|---|
| Module | 5 - Natural Prompt Automation & Debugging |
| Time | 30 minutes |
| Shop preset | `clean` |
| You need | Labs 0 and 2 done; your coding agent signed in |
| You start from | `main`, plus your `AGENTS.md` from Lab 2 (or `solutions`' version: step 0 says how) |

Then come numbered steps, *Stretch*, and *If your agent fails*, which links to `transcripts/`. Each step is either a command to run or a prompt to give the agent, and prompts are quoted in full so that every agent gets the same input. Where agents differ, a step gives a three-column table, with Claude Code first because the facilitator demonstrates with it.

`checklist.md` lists *done* as checkable items (spec *Done is checkable*). `labs/README.md` indexes the labs with module, time and preset.

**Links.** Labs link with relative Markdown links only inside `labs/`, `docs/`, `transcripts/` and to the root guides (`SETUP.md`, `GLOSSARY.md`). Other repository files are named as code paths (`tests/ui/catalogue.robot`). The `ci-and-site` site renders Markdown and fails on broken links, so this keeps the lab texts renderable without edits.

*Alternative:* one long lab document. Rejected: the site, the transcripts and the catch-up rule all work per lab.

### D2. What each lab does

| Lab | Preset | The participant... | Done when |
|---|---|---|---|
| 0 arrival | `clean` | forks, installs, starts the shop or sets a space, runs `setup-check`, runs the suite once | `setup-check` green, and the suite shows exactly the 2 tests failing on purpose |
| 2 context | `clean` | runs one generation prompt, writes `AGENTS.md` from a checklist, moves one section into a referenced file, runs the same prompt again | `AGENTS.md` covers the checklist and stays short, and the before/after outputs are saved side by side |
| 3 skills | `clean` | installs the RF Agent Skills, reruns a prompt, turns `skills/template/` into a skill for one convention, checks trigger and no-trigger | the skill triggers on a matching prompt and stays quiet on an unrelated one |
| 4 robotcode | `clean` | installs the RobotCode plugin; asks a discovery question, a libdoc question; step-debugs the Module 4 broken test; explores a flow in the REPL | the broken test passes, and the agent used `discover`, `libdoc` and `robot-debug` (visible in the session) |
| 5 prompt to green | `clean` | picks a story and runs propose, pair review, apply, run; debugs the Module 5 broken test in conversation | the slice's tests pass, follow the conventions, and the change's specs are under `suite/*` |
| 6 mcp | `clean` | connects rf-mcp, rebuilds one Module 5 test stepwise, compares | a stepwise-built test passes, with a note on what live access changed |
| 7 hooks and toolbelt | `buggy` | wires two hooks and sees them fire; runs the suite, files one real defect with `gh` | an edit with an inline locator is rejected, and an issue with reproduction steps exists |
| 8 healing | `drift_and_bug` | runs the heal profile and triages each heal | every heal is marked accept, reject or investigate, and the two defects are named as defects |
| 9 ci | `clean` | enables the workflow on their fork, pushes a break, opens a PR | the PR has the triage comment |

Every lab ends in `clean`: Labs 7 and 8 reset their preset as their last step. Lab 8's stretch is the agentic path: the coding agent repairs one drifted locator with `robotcode robot-debug` and rf-mcp, onto the stable contract.

The labs leave the answers out (spec *Labs do not give the answers away*). Lab 4 names the broken test and the tool, not the cause. Lab 7 says "run the suite under `buggy` and file what you find". The answers stay in `docs/facilitator/`.

### D3. Module 5 slices and the `suite/*` namespace

| Story | Difficulty | Slice |
|---|---|---|
| WEB-004 search | easier | AC-1, AC-3, AC-6, AC-7 |
| WEB-003 product detail | medium | AC-1, AC-3, AC-8, AC-9 |
| WEB-005 cart | harder | AC-2, AC-3, AC-4, AC-9 |
| WEB-007 sign-in (swap-in) | medium | AC-2, AC-3, AC-4, AC-8 |
| API-005 cart API (stretch) | stretch | AC-1, AC-2, AC-4, AC-7 |

Each slice starts on a page the suite does not cover and can be verified through the stable contract. None of the slices needs a preset other than `clean`. WEB-003 participants who follow card links from the catalogue will meet the broken card links under `buggy` in Module 7. That is the find the baseline-suite design left for them.

The participant's change writes its delta specs to **`suite/<area>`**, named after the `shop/*` area it verifies, for example `suite/search`. Each requirement names the criterion it verifies, as in *"The suite SHALL verify WEB-004_AC-3 ..."*. `openspec/config.yaml` gains the third namespace in its context and a rule for it: `suite/*` requirements name the `<STORY>_<AC>` they verify and never a locator or a keyword. Without a namespace, `/opsx:propose` would invent a capability, most likely `search`, and so compete with `shop/search`. The spec-level change is the *Spec namespaces* modification of `workshop/agent-context`.

*Alternative:* `skip_specs` for participants' changes. Rejected: the propose workflow would still try to write specs unless every participant set the flag by hand, and a record of what the suite covers is worth keeping.

The pair review is on the plan: proposal, specs and tasks, before any test exists. The review checklist sits in `labs/lab-05-prompt-to-green/checklist.md`, and the facilitator's whiteboard template in the run sheet.

### D4. How Module 8 participants get a model

- **Participants who have an OpenAI-compatible endpoint** use their own `HEAL_*` settings, as `SETUP.md` already describes, with a spending cap.
- **The facilitator may hand out** a capped workshop key for a specific workshop. The run sheet says how: a key per participant, with a cap and an expiry, delivered in the meeting chat and never committed.
- **Everyone else** triages the recorded healing report of the rehearsal run, `transcripts/lab-08-healing/`, and does the agentic stretch goal with the coding agent they already use. That path needs no extra key.

Lab 8 is demo-led either way: the facilitator's live run is the shared picture, and the recorded report makes the triage identical for everyone. Rejected alternatives:
- one shared key for the room: a leak risk in a public call, and no per-person cap;
- a local model: a new install on the day, and heal's selection mode is unproven on small local models;
- the agentic path only: it drops the listener, which is Module 8's topic.

### D5. The assets

- **Skills.**
  - `skills/template/` holds `SKILL.md` (frontmatter `name` and `description`, then instructions) and `scripts/check.py`, a small example helper that the instructions call through `uv run --no-sync`.
  - Lab 3 copies the template into the agent's skill folder (table in Context).
  - `skills/jira-ticket/` holds `SKILL.md` and `scripts/file_issue.py`. The script uses `requests` from the project environment, reads `JIRA_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` and `JIRA_PROJECT` from the environment or `.env`, and is a dry run unless all four are set and `--send` is given.
- **Hooks.** `hooks/` holds three Python scripts, run as `uv run --no-sync python hooks/<script>.py`, plus a shared module that normalises each agent's hook input to "tool, file, new text, command":
  - `run_affected_tests.py` (after an edit): for a changed `tests/**/*.robot`, runs that file; for a changed `resources/*.resource`, runs the test files that import it. Runs use `--exclude broken`, and the verdict goes back to the agent.
  - `no_inline_locators.py` (before an edit): rejects new text that puts a locator literal into a test or task body. A locator literal is an argument that starts with `css=`, `xpath=`, `id=`, `text=`, `role=`, `//`, `#`, `.` followed by a letter, `[`, or contains ` >> `. Run as a command over paths, it reports each finding. Over `tests/` on `main`, that is exactly the inline locator the baseline suite ships.
  - `green_before_commit.py` (before a shell command): lets anything through that is not `git commit`. It blocks a commit when `results/output.xml` is missing, is older than the newest file under `tests/` or `resources/`, or contains a failure outside `broken`.

  `hooks/README.md` gives the wiring for each agent, verified by making each hook fire once in each agent. Claude Code's wiring is the one demonstrated.
- **Subagents.** `agents/claude-code/`, `agents/copilot/` and `agents/codex/` each hold `writer`, `reviewer` and `runner` in that agent's format. The instructions are the same, and the tool lists use each agent's own tool names:
  - the reviewer can read and search only;
  - the runner can read and run commands, but not edit;
  - the writer can edit.

  One canonical file cannot serve all three, because the tool names and file formats differ.
- **MCP.** `mcp/README.md` gives, for each agent, the `mcp add` command that starts `uv run --no-sync rf-mcp` from the repository root, plus the equivalent file snippet: `mcp/claude-code.mcp.json`, `mcp/codex.toml` and `mcp/copilot.json`. The server runs in the project environment, so it sees the pinned libraries and `shop/variables.py`. Lab 6 tells the agent to open pages through `resources/shop.resource`, whose `Start Shop Test` already sends the space. No snippet contains a secret or a space name.
- **Third-party plugins.**
  - The RF Agent Skills are installed with `uvx rf-agentskills@0.6.0 install --agent <agent> --scope project --project .`, so they land inside the fork.
  - The RobotCode plugin is installed from its marketplace. It is pinned to the commit above wherever the agent's marketplace command takes a ref; otherwise `SETUP.md` records the commit it was verified at.
  - `SETUP.md` gains both names and versions.

### D6. Facilitation documents

- **`GLOSSARY.md`**: one paragraph per term, grouped by the five tiers. The terms are those the labs use (spec *A glossary*), plus the repository's own: preset, space, stable contract.
- **`docs/environments.md`**: local shop, shared instance, no Docker; the agent choice table (cost, sign-in, where the labs differ). It is written for the setup email at T-2 weeks.
- **`docs/facilitator/`**:
  - `run-sheet.md`: one row per module with time, preset, demonstration, lab, fallback and overrun action; the cut order and the beginner plan; the preset commands for the room;
  - `cold-open.md`: the five minutes, command by command, with expected output. The backup is `transcripts/cold-open.md`;
  - `triage-playbook.md`: the `setup-check` findings by frequency, with their fixes;
  - `rehearsal.md`: the rehearsal record, with the date, the agent and version, per-lab notes, and where the second agent diverged.

  `suite-outcomes.{toml,md}` stay where the baseline-suite put them.

### D7. Rehearsal and transcripts

A rehearsal is a lab done by an agent from its instructions, headless, in a fresh clone of `main`:
1. `uv sync --locked` and `rfbrowser install chromium`;
2. a freshly reset space;
3. the agent's user-level configuration as installed, with nothing project-level left behind.

The labs run in order in one clone, so that each builds on the last, as it does for a participant. Two further runs complete the gate:
- **Lab 5 without MCP**: Claude Code with `--strict-mcp-config` and no servers;
- **Labs 2 to 4 with Codex** (`codex exec`), in a second clone.

The clean-room install itself was proven by `workshop-foundation`'s container run and is not repeated. The macOS check it carried over (its task 1.4) stays a task here, for a maintainer with an Apple silicon Mac.

Transcripts are converted from the agents' JSON event streams by `tools/transcript.py` into Markdown. Each shows the prompts, the tool calls, shortened results and the agent's answers. The script replaces the clone's path with `<repo>` and the home directory with `~`, drops reasoning blocks, and refuses to write a transcript in which the secret scan finds anything. `transcripts/cold-open.md` is recorded the same way from the cold-open script.

*Alternative:* hand-written walkthroughs. Rejected: a fallback must show what an agent really does, including its detours.

### D8. The solutions branch

The rehearsal clone's state after each lab becomes one commit on `solutions`, in lab order, after review. Labs 4 and 5 repair the two broken tests, so the suite on `solutions` passes completely. Lab 9's commit comes with `ci-and-site`. The branch is pushed once `main` has this change. Before the workshop tag it is rebased onto `main` and its suite re-run (spec *Kept current with main*). It is never merged: `ci-and-site` can add a check that fails when a merge from `solutions` reaches `main`.

## Risks / Trade-offs

- [An agent rehearsal is not a participant] → It proves the instructions are complete and the steps work, not that they are clear. The dry-run gate still needs a human pass, which `rehearsal.md` records as a separate row for the maintainer.
- [Agents change faster than the workshop] → Versions are named in `SETUP.md` and in `rehearsal.md`. Where an agent differs, a lab gives a table rather than prose, so a changed command is a one-cell edit.
- [Hook payloads differ between agents and may change] → One normalising module, and each wiring is verified by making the hook fire. A hook that cannot parse its input lets the action through and says so, rather than blocking the agent.
- [The affected-tests hook is slow for UI tests] → It runs only the changed file or the files importing a changed resource, and skips `broken`. Lab 7 names the delay as the cost of the guardrail.
- [Transcripts leak something] → The converter refuses on a secret-scan hit, and paths are rewritten. The rehearsal runs with a `.env` that holds only `SHOP_*` and the rehearsal's `HEAL_*`, and the key never enters a prompt.
- [The Module 5 slices prove too hard without MCP] → The rehearsal without MCP decides. If a slice fails, it is shortened or the story swaps with WEB-007, as the master document's risk table prescribes, and `rehearsal.md` says so.
- [The site cannot render links to `transcripts/` or the root guides] → D1 limits links to those locations. `ci-and-site` must render them or rewrite them, and its proposal already takes over Lab 9's rehearsal.
- [Rehearsals spend the maintainer's agent quota] → About a dozen headless sessions. Their token counts go into `rehearsal.md`, which facilitators use to size a workshop key (D4).

## Migration Plan

This change adds files and a branch. `openspec/config.yaml` gains the `suite/*` namespace, and `SETUP.md` the plugin versions. Rollback is a revert on `main` and a deleted `solutions` branch.
