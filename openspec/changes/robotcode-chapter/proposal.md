## Why

A report of 121 scripted experiments with RobotCode 2.7.0 exists outside this repository. It tested Robot Framework 7.5, Browser 20.5.0 and RequestsLibrary 0.9.7, the exact versions this workshop pins. It shows which RobotCode commands answer which questions, how an agent drives the REPL and the debugger without blocking at a prompt, and which traps the pinned versions have. The Lab 4 rehearsal hit two of those traps and lost time on both. Participants have no page that collects this, for the day or for Monday.

The report also shows that the workshop draws the line between Tier 3 and Tier 4 in the wrong place. The glossary says Tiers 1 to 3 work "without live access", and Lab 6 opens with "your agent wrote tests without ever seeing the page". But in Lab 4 the agent already drives a visible browser through the REPL. At a Browser failure, the debugger also leaves the page open for the agent to query. The real difference is persistence. A RobotCode session lasts as long as one command. An MCP session stays open across the agent's steps.

## What Changes

- **A RobotCode cheat sheet for participants**, `docs/robotcode.md`, written for this repository rather than copied from the report:
  - which command answers which question;
  - each command with an example that runs here;
  - how an agent drives the REPL and the debugger: piped input with `--plain`, ending with a resuming command;
  - the traps of the pinned versions that participants can meet.
  - It is linked from Lab 4 and from the glossary's RobotCode entry, and published on the site under *Guides*.
- **Lab 4 loses two traps**:
  - **`HEADLESS`**: a visible browser now follows `-v HEADLESS:False` everywhere. Today, importing `resources/shop.resource` at run time, as the REPL does, sets `${HEADLESS}` back to `True`. This is Robot Framework's own behaviour with a variable table. The default moves out of the table, and the browser stays headless by default.
  - **The REPL's output directory**: RobotCode does not create it, and `New Browser` then fails. The fix belongs upstream, so Lab 4's REPL step gets a one-line hint, and the triage playbook gets the symptom and the fix.
- **A debugger note for facilitators**. It covers what to do when an agent waits at the `(rdb)` or REPL prompt, or reaches for tmux, which Windows does not have: pipe the commands with `--plain`, and end with `.continue` or `.exit`. It goes into the triage playbook.
- **One boundary between Tier 3 and Tier 4**, persistence rather than live access, in all of these:
  - the glossary's ladder and its Tier and MCP entries;
  - the curriculum's Module 4 and Module 5 text and its tooling table;
  - Lab 6's opening paragraph.
  - Tier names and module titles stay as they are.
- **The curriculum's RobotCode entry** says `pip install robotcode`. It now says how this repository installs and runs it: the locked environment and `uv run robotcode`.
- **Lab 4 is rehearsed again**, from the REPL step onward, and its transcript is updated. The recorded workaround for `HEADLESS` would otherwise teach a problem that no longer exists.

The report itself stays out of the repository. Its re-run instructions use `rfbrowser init`, which `SETUP.md` forbids, and refer to an experiments project that is not here.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `workshop/facilitation`: adds a RobotCode cheat sheet requirement, and a requirement that the glossary, the curriculum and the labs draw the Tier 3 / Tier 4 boundary the same way.
- `workshop/baseline-suite`: adds a requirement that a command-line `HEADLESS` holds in a test run and in a REPL session, and that the browser is headless by default.

## Impact

- **New**: `docs/robotcode.md`.
- **Changed**:
  - `resources/shop.resource`: `HEADLESS`;
  - `labs/lab-04-robotcode/INSTRUCTIONS.md`: cheat sheet link, REPL hint;
  - `labs/lab-06-mcp/INSTRUCTIONS.md`: opening paragraph;
  - `GLOSSARY.md`;
  - `docs/WWWW_Workshop_Master_Preparation.md`: Modules 4 to 6, tooling table;
  - `docs/facilitator/triage-playbook.md`;
  - `docs/facilitator/rehearsal.md`;
  - `transcripts/lab-04-robotcode.md`: the re-rehearsed steps;
  - `website/sidebars.js`: *Guides*;
  - `tools/check_labs.py`: the cheat sheet joins the participant files checked for giveaways.
- **Unchanged**:
  - the suite's outcomes under every preset (`docs/facilitator/suite-outcomes.toml`);
  - Lab 4's steps, checklist and timing;
  - the `AGENTS.md` line of Lab 4 step 2.
- **Out of scope**, as follow-ups:
  - a debugger-first variant of Lab 8's stretch goal;
  - a `results diff` regression gate for Lab 9;
  - the RobotCode issues the report found, which belong upstream.
- **Order**: independent of `ci-and-site`, which only waits for its archive. The cheat sheet's place on the site needs `website/` from `main`, which is there.
