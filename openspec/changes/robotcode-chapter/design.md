## Context

See proposal.md for why. The facts this design builds on:

- **The report stays outside the repository.** Its findings were made with the versions pinned here: RobotCode 2.7.0, Robot Framework 7.5, Browser 20.5.0 and RequestsLibrary 0.9.7. Only its Python was newer (3.13).
- **`HEADLESS`**:
  - `resources/shop.resource` declares `${HEADLESS}    ${True}` in its variable table.
  - A command-line `-v HEADLESS:False` wins in a normal run, where the resource is imported in the settings.
  - It loses after a run-time `Import Resource`. Checked while exploring: in the REPL, and in a plain `robotcode robot` run that imports the resource at run time, `${HEADLESS}` reads `False` before the import and `True` after it. This is Robot Framework's behaviour, not RobotCode's.
  - `shop.resource` is the only file that uses `HEADLESS`.
  - The MCP server of Lab 6 imports it too, and reads no `robot.toml`.
- **The REPL does not create its output directory**, and `New Browser` then fails with `FileNotFoundError` for `playwright-log.txt`. `results/` exists after Lab 0's first run, so the trap bites only when an agent passes its own `-d`. The Lab 4 rehearsal's agent did exactly that.
- **Driving the debugger:**
  - The installed RobotCode plugin tells agents to drive the REPL and the debugger interactively, and to pipe a fixed command sequence only as a fallback.
  - The three supported agents run shell commands to completion. The rehearsal's agent therefore kept the debugger alive in tmux, which Windows does not have.
  - The report shows the pipe is reliable: `--plain`, one command per line, and the run resumes when the input ends.
- **Checks:**
  - `tools/check_labs.py` checks `labs/**/*.md`, `GLOSSARY.md` and `docs/environments.md` for giveaways, among them the cause of the Module 4 broken test.
  - It checks links in every page the site renders.
- **The site:** `website/sidebars.js` lists *Guides* by hand: `docs/environments`, `docs/conventions`.

## Goals / Non-Goals

**Goals:**
- Every command on the cheat sheet has run in this repository, with the pinned versions, before it is published.
- Lab 4 keeps its steps, its checklist and its 25 minutes.
- The suite's behaviour under every preset is unchanged.

**Non-Goals:**
- Changing what the RobotCode plugin teaches, or Lab 4's `AGENTS.md` line (D3).
- Renaming the tiers or the modules (D4).
- A PowerShell form of the piped examples (Risks).

## Decisions

### D1. `HEADLESS` gets its default in the keyword, not in a variable table

- `Open Shop Browser` reads the value with `Get Variable Value    ${HEADLESS}    ${True}` and passes it to `New Browser`.
- The variable table loses `${HEADLESS}`.
- A run-time import then has nothing to overwrite, so the command-line value holds in the REPL too. Without the variable, every caller gets `True`, including the MCP server.

*Alternatives:*
- The default in `robot.toml`'s `[variables]`. Rejected: the MCP server and anything else that does not read `robot.toml` would lose the default.
- Documenting the workaround (`Set Global Variable` after the import). Rejected: every participant's agent would still hit the trap first, in a 25-minute lab.

*Verification:*
- Repeat the exploration's probe: in the REPL, `${HEADLESS}` stays `False` after the import.
- `New Browser` logs `"headless": false` in a REPL session and in a run with `-v HEADLESS:False`.
- `tools/verify_outcomes.py` still matches every preset.

### D2. The cheat sheet is written for this repository, from evidence

`docs/robotcode.md`, in this order:

1. **Which tool for which question**: a table, adapted from the report's recommendations.
2. **The commands**:
   - `discover`, `libdoc`, `robot-debug`, `repl` and `results`;
   - each with one or two examples against this suite and shop, shortened like the transcripts' output;
   - `-p shared` is mentioned once, not repeated.
3. **Driving RobotCode from an agent**:
   - interactively when the agent can hold a terminal;
   - otherwise piped with `--plain`, one command per line, ending with `.continue` or `.exit`;
   - the input ending resumes the run, so nothing waits forever;
   - at a breakpoint in a Browser test, the page is still open, and `Get Url` or `Get Element Count` run against it.
4. **Traps** that the pinned versions show and a participant can meet:
   - the REPL's output directory;
   - a run-time import overriding `-v`, now fixed in this suite but still a trap in participants' own projects;
   - `.break` with quotes at the prompt never matches;
   - the REPL's exit code and its `output.xml` say PASS whatever failed;
   - `.save` keeps lines that failed;
   - `discover --search` also matches keyword calls;
   - RequestsLibrary logs request and response bodies, credentials included, which matters for Lab 5's API stretch goal and for results uploaded from a public fork.
5. **Further reading**: the RobotCode reference pages.

Content rules:
- The debugger examples break inside a passing test, never at a test broken on purpose, so the page cannot hint at a cause.
- `docs/robotcode.md` joins `PARTICIPANT_FILES` in `tools/check_labs.py`.
- It is linked from Lab 4's opening paragraph, next to the existing link to the glossary, and from the glossary's RobotCode entry.
- On the site it is the third item under *Guides*.

*Alternative:* the report's cheat sheet as it is. Rejected: it covers other systems, it uses `rfbrowser init`, and it covers features no lab uses, such as wrappers and `xvfb`.

### D3. The debugger advice goes to facilitators and the cheat sheet, not into the agent's context

Lab 4 examines whether the plugin teaches the habits: it looks for the REPL misfire, and whether the answers came from `discover` and `libdoc`. Pointing `AGENTS.md` at the cheat sheet would put our advice in front of the plugin's, and the lab would no longer measure what it claims.

The advice therefore goes to two places:
- the triage playbook, under *Not caught by the check*, gets two entries:
  - an agent waits at a prompt, or reaches for tmux on Windows: stop it, and ask for the piped form;
  - the REPL's `FileNotFoundError`: create the output directory;
- Lab 4's REPL step gets one sentence on the output directory.

*Alternative:* extending the `AGENTS.md` line of step 2. Rejected for the reason above. A participant may still add it on Monday.

### D4. Tier names stay; the explanations change

"Live access" and "The Live-Access Upgrade" are in the published agenda, the run sheet and the site. Renaming them costs more than it clarifies. The texts under them change instead:

| Where | Today | After |
|---|---|---|
| `GLOSSARY.md`, the ladder | "4. Live access: a running session the agent steps through" | the same, plus "that stays open between its steps" |
| `GLOSSARY.md`, *Tier* | "Tiers 1 to 3 … without live access" | "… without a session that stays open between the agent's steps" |
| `GLOSSARY.md`, *MCP* | "runs keywords in a session that stays open" | the same, plus the contrast: RobotCode's REPL and debugger reach the page too, for one command |
| the curriculum, Module 4 | `robot-debug`: "live breakpoint, real variables" | the same, plus: at a Browser failure, the live page |
| the curriculum, Module 5 debrief | "the agent couldn't peek at the live page mid-draft" | every look at the page cost a fresh command, and nothing stayed open between steps |
| the curriculum, Module 6, tooling table | "Tier 4: live stepwise execution" | "stepwise execution in a session that stays open" |
| the curriculum, tooling table, RobotCode | "`pip install robotcode` in the project venv" | "in the locked environment: `uv run robotcode`" |
| Lab 6, opening paragraph | "wrote tests without ever seeing the page" | Lab 5 had no page, and Lab 4's REPL had one only for as long as a command ran; MCP keeps the session open |

The glossary stays readable in about ten minutes: each entry grows by at most one sentence.

### D5. Lab 4 is rehearsed again from step 6

- **Which steps:** D1 and D3 change step 6 only. Steps 1 to 5 keep their instructions, and their recording stays valid.
- **The run:** step 6 is run again with Claude Code, in a clone at the state after step 5, the way the other rehearsals ran.
- **The transcript:** the new run replaces step 6 of `transcripts/lab-04-robotcode.md`, including its caveat about `-v`.
- **The record:** `docs/facilitator/rehearsal.md` records the result.
- **Codex** is not run again (see Risks).

## Risks / Trade-offs

- **The suite could change behaviour through the `HEADLESS` edit.** → `tools/verify_outcomes.py` over every preset, and CI.
- **Lab 6's transcript shows the MCP server loading `HEADLESS` from the resource, which it will no longer do.** → A transcript records a past run, and Lab 6 does not use the variable. Nothing to change.
- **The cheat sheet goes stale when a pin moves.** → Its first line names the RobotCode version. The maintainers' checklist in `SETUP.md` (*changing a pinned version*) gets one item: run the cheat sheet's examples again.
- **The plugin says "interactive first", and the cheat sheet says "pipe" for agents that run commands to completion.** → The page states both and says when each applies, which matches the plugin's own fallback.
- **The piped examples are POSIX shell only.** That is the shell Claude Code uses, including Git Bash on Windows. A PowerShell form is unverified. → The page names the principle (pipe the commands, end with a resuming one), so an agent in PowerShell can translate it. A verified PowerShell form can follow once someone runs it on Windows.
- **Only Claude Code re-rehearses step 6.** The labs spec wants Labs 2 to 4 run with a second agent, and the Codex run of Lab 4 predates D1. → D1 removes a trap without changing a step, so the Codex run stays valid for everything it recorded. The rehearsal record says so.

## Migration Plan

- The change lands on `main` before the workshop tag, so participants fork it with the change in place.
- Rollback: revert the commit. D1 has no other dependents.
