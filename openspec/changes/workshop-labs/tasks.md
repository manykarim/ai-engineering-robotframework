## 1. Namespace and scaffolding

- [ ] 1.1 Add the `suite/*` namespace to `openspec/config.yaml` (design D3): the context describes three namespaces and says a change that adds tests writes to `suite/<area>`, and a spec rule says `suite/*` requirements name the `<STORY>_<AC>` they verify and never a locator or keyword. Verify:
  - `openspec instructions specs --change workshop-labs --json` returns a context naming `shop/*`, `suite/*` and `workshop/*`, and the new rule beside the `shop/*` rule;
  - `openspec validate --specs --strict` still passes.
- [ ] 1.2 Create the nine lab folders and `labs/README.md`, the index with module, time and preset (design D1, D2). Verify: `ls labs` shows exactly the nine folders of spec *One folder per lab*, plus `README.md`.
- [ ] 1.3 Copy the five story files (WEB-003, WEB-004, WEB-005, WEB-007, API-005) from demo-webshop at the pinned `v0.3.0` into `labs/lab-05-prompt-to-green/stories/`. Verify: each file is byte-identical to `git show v0.3.0:docs/user-stories/<file>` in demo-webshop, and no other story or `CONFORMANCE.md` is present.
- [ ] 1.4 Write `tools/check_labs.py`, which checks the lab contract. Verify that it reports each of the following on a deliberately broken copy, and passes once the labs exist:
  - a missing folder or file;
  - a header table without module, time, preset, prerequisites or starting state;
  - a time budget that differs from the timetable (Labs 2-9 per spec *What every lab states up front*);
  - a relative link outside `labs/`, `docs/`, `transcripts/`, `SETUP.md` and `GLOSSARY.md`;
  - participant-facing text naming a planted defect, the inline locator, or a broken test's cause.

## 2. Lab assets

- [ ] 2.1 Write `skills/template/` (`SKILL.md` and `scripts/check.py`) per design D5. Verify: copied into a scratch clone's skill folder for each agent, Claude Code, Codex and GitHub Copilot each list the skill; in Claude Code, a headless prompt that matches the description triggers it and an unrelated prompt does not.
- [ ] 2.2 Write `skills/jira-ticket/` (`SKILL.md` and `scripts/file_issue.py`). Verify:
  - without Jira settings, the script prints the issue it would file and names the missing settings;
  - with settings and without `--send`, it prints the request and sends nothing (checked with no network route);
  - `git grep` finds no Jira credential in the repository.
- [ ] 2.3 Write the three hook scripts and their input-normalising module in `hooks/` (design D5). Verify, as plain commands:
  - `no_inline_locators.py tests/` on `main` reports exactly one finding;
  - an edit payload adding `Click    css=button.buy` to a test file is rejected, in the input shape of each of the three agents;
  - `green_before_commit.py` blocks with a missing, a stale and a red `results/output.xml`, and allows a fresh green one, a run whose only failures are `broken`, and any command that is not `git commit`;
  - `run_affected_tests.py` runs `tests/ui/checkout.robot` for a change to `resources/checkout.resource`, and reports the verdict.
- [ ] 2.4 Write `hooks/README.md` with the wiring for Claude Code, Codex and GitHub Copilot. Verify: in a scratch clone, each hook fires once in each agent - an inline-locator edit is rejected, an affected run is reported, a commit after a red run is blocked - and the observed behaviour is recorded in `docs/facilitator/rehearsal.md`.
- [ ] 2.5 Write the writer, reviewer and runner subagents in `agents/claude-code/`, `agents/copilot/` and `agents/codex/`, and `agents/README.md` with where each agent loads them. Verify: each agent lists the three; asked to change a file, the reviewer makes no change and reports a finding, in Claude Code and one other agent.
- [ ] 2.6 Write `mcp/README.md` with the `mcp add` command per agent and the snippets `mcp/claude-code.mcp.json`, `mcp/codex.toml` and `mcp/copilot.json`. Verify:
  - each agent lists the server as connected;
  - in Claude Code with the shared profile and a throwaway space, a page opened through the server via `resources/shop.resource` reports that space;
  - the snippets contain no secret and no space name.
- [ ] 2.7 Pin the third-party plugins (design D5), and add both to `SETUP.md` with their versions. Verify:
  - `uvx rf-agentskills@0.6.0 install --agent claude-code --scope project --project <clone>` writes only inside the clone, and the installed skills report content `v1.2.0`;
  - the RobotCode plugin installs from its marketplace in Claude Code, at the recorded commit where a ref is supported;
  - `setup-check`'s guide references still resolve.

## 3. Labs

- [ ] 3.1 Write Lab 0 (`lab-00-arrival`). Verify: `tools/check_labs.py` passes for it, and its done criteria match a fresh run: `setup-check` green, and exactly the two `broken` tests fail.
- [ ] 3.2 Write Lab 2 (`lab-02-context`): the `AGENTS.md` checklist, the split into a referenced file, the before/after prompt, and the nested `tests/api/AGENTS.md` stretch. Verify: `check_labs.py` passes, and the checklist keeps the result within the agent-context rules (one context file, no secrets).
- [ ] 3.3 Write Lab 3 (`lab-03-skills`): the RF Agent Skills install, the before/after prompt, and the convention skill from `skills/template/` with trigger and no-trigger prompts. The stretch goal bundles the helper script. Verify: `check_labs.py` passes.
- [ ] 3.4 Write Lab 4 (`lab-04-robotcode`): the plugin install, a discovery and a libdoc question, step-debugging the Module 4 broken test, and a REPL exploration with a visible browser. The stretch goal is a results query by tag. Verify: `check_labs.py` passes, and the lab names the broken test and the tool but not the cause.
- [ ] 3.5 Write Lab 5 (`lab-05-prompt-to-green`): the story choice with the slices of design D3, propose, the pair review with its checklist, apply, run and refine, conversational debugging of the Module 5 broken test, WEB-007 as swap-in, and the API-005 stretch goal. Include the per-agent command table. Verify: `check_labs.py` passes, and no step needs an MCP server.
- [ ] 3.6 Write Lab 6 (`lab-06-mcp`): connect rf-mcp from `mcp/`, rebuild one Module 5 test stepwise, and compare. The stretch goal changes the page mid-session. Verify: `check_labs.py` passes.
- [ ] 3.7 Write Lab 7 (`lab-07-hooks-toolbelt`):
  - wire two hooks from `hooks/`;
  - apply `buggy`, run the suite, and file one defect with `gh` from the run's evidence, in the participant's fork;
  - stretch A: writer then reviewer;
  - stretch B: the Jira skill;
  - reset the space.

  Verify: `check_labs.py` passes, and the lab names no defect.
- [ ] 3.8 Write Lab 8 (`lab-08-healing`): apply `drift_and_bug`, run with `-p heal`, and triage each heal. Include the no-model path of design D4 and the agentic stretch goal, and reset the space. Verify: `check_labs.py` passes.
- [ ] 3.9 Write Lab 9 (`lab-09-ci`) against the workflow contract of `ci-and-site`'s proposal: enable the workflow on the fork, push a break, open a PR, and read the triage comment; the no-key fallback; and the heal-suggestion stretch goal. Verify: `check_labs.py` passes, and the lab says its workflows arrive with `ci-and-site`.

## 4. Facilitation

- [ ] 4.1 Write `GLOSSARY.md`, grouped by the five tiers. Verify:
  - every term in the list of spec *A glossary* is defined, as is every term `check_labs.py` collects from the labs' bold terms;
  - the file is under 1,800 words (about ten minutes).
- [ ] 4.2 Write `docs/environments.md`: the local shop, the shared instance, no Docker, and the agent choice with where the labs differ. Verify: every lab difference named in a per-agent table of Labs 3-7 appears in it.
- [ ] 4.3 Write `docs/facilitator/run-sheet.md`: one row per module with time, preset, demonstration, lab, fallback and overrun action; the cut order and the beginner plan; the preset commands for the room; the workshop-key procedure of design D4; and the Module 5 whiteboard template. Verify: the times equal the timetable, and every preset named matches its lab.
- [ ] 4.4 Write `docs/facilitator/cold-open.md` with commands, expected output and the backup `transcripts/cold-open.md`. Verify: each command runs against the local shop and shows the output the script expects.
- [ ] 4.5 Write `docs/facilitator/triage-playbook.md`. Verify: every `setup-check` check that can fail is named with its fix, and each name matches a check in `setup-check/check.py`.
- [ ] 4.6 Update `README.md`'s "What is in here" with the new folders and guides. Verify: every path listed exists.

## 5. Rehearsal

- [ ] 5.1 Write `tools/transcript.py` (design D7). Verify: on a recorded Claude Code and a recorded Codex event stream, it writes Markdown with prompts, tool calls and answers; it rewrites the clone path and home directory; and it refuses when the stream contains a planted fake key.
- [ ] 5.2 Rehearse Labs 0 and 2-8 with Claude Code, headless, in lab order in one fresh clone and a freshly reset space. Save a transcript per lab, and fix every instruction the run showed to be wrong or missing. Verify: each lab's checklist holds in the clone, and `rehearsal.md` records the date, agent version, duration and tokens per lab.
- [ ] 5.3 Rehearse Lab 5 with Claude Code and no MCP server (`--strict-mcp-config`). Verify: the slice's tests pass, and the run used no MCP tool.
- [ ] 5.4 Rehearse Labs 2-4 with Codex in a second fresh clone. Verify: `rehearsal.md` lists where Codex diverged from the instructions, and each divergence is either fixed in the lab or named in its per-agent table.
- [ ] 5.5 Record the Lab 8 healing report for the no-model path in `transcripts/lab-08-healing/`: the heals with old and new locator, the results, and a triage table. Verify: the secret scan finds nothing, and the report matches the `[heal.drift_and_bug]` outcomes.
- [ ] 5.6 Record the cold open in `transcripts/cold-open.md`. Verify: it follows `cold-open.md` step by step.
- [ ] 5.7 Scan `transcripts/` for secrets and local paths. Verify: no key, token, `.env` value, home directory or clone path is found.
- [ ] 5.8 Carried over from `workshop-foundation` 1.4: install and check the toolchain on macOS 13+ on Apple silicon, with a maintainer's Mac. Verify: `setup-check` is green there, and `rehearsal.md` records it.

## 6. The solutions branch

- [ ] 6.1 Build `solutions` from the rehearsal clone: one commit per lab that produces files, in lab order, each message starting with the lab folder's name (design D8). Verify:
  - `git log --oneline main..solutions` shows the lab commits;
  - in a freshly reset space, the whole suite on `solutions` passes, including the two tests `main` ships broken and the rehearsed Module 5 tests.
- [ ] 6.2 After this change is merged, rebase `solutions` onto `main` and push it. Verify:
  - the suite on the pushed branch passes;
  - `main` still has the thin `AGENTS.md` and none of the lab results.

## 7. Close-out

- [ ] 7.1 Validate and archive. Verify: `openspec validate workshop-labs --strict` passes. After the merge, the archive creates `workshop/labs`, `workshop/lab-assets`, `workshop/facilitation` and `workshop/solutions` with their Purpose, and renames and updates `workshop/agent-context`'s namespace requirement.
