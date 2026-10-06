# workshop/facilitation Specification

## Purpose
Gives facilitators and participants the shared vocabulary, the environment choices, the run sheet for the day and the fallbacks for when something fails live, so that the workshop runs the same way whoever leads it.

## Requirements

### Requirement: A glossary
`GLOSSARY.md` SHALL define every term the labs use that a Robot Framework user without agent experience may not know, including the five tiers of the maturity ladder, context engineering and spec-driven development, and SHALL be readable in about ten minutes.

Where an entry names agent tooling or a practice, it SHALL link the documentation a reader goes to next: the standard, the tool's repository, or an agent's own documentation, labelled with whose it is.

#### Scenario: A term from a lab
- **WHEN** a lab uses a term such as "skill", "hook", "subagent", "MCP", "preset", "space", "heal" or "context engineering"
- **THEN** `GLOSSARY.md` defines it

#### Scenario: Reading on after the day
- **WHEN** a participant wants to know more about skills, subagents, hooks, context files, context engineering or spec-driven development
- **THEN** the glossary entry links a source to read next, and says whose documentation it is

### Requirement: Environments and agent choice
`docs/environments.md` SHALL describe the ways to run the workshop - local shop, shared instance, and a machine without Docker - and SHALL help a participant choose between Claude Code, Codex and GitHub Copilot, naming where the labs differ between them.

#### Scenario: A participant without Docker
- **WHEN** a participant cannot run Docker
- **THEN** `docs/environments.md` tells them to use a space on the shared instance and how to set it up

### Requirement: A run sheet
`docs/facilitator/` SHALL contain a run sheet listing, for every module: its start time and duration, the preset the shop must be in, what the facilitator demonstrates, the lab, the fallback, and the recovery action when the module overruns.

#### Scenario: Checking the preset for a module
- **WHEN** a facilitator looks up Module 7 in the run sheet
- **THEN** it names `buggy` as the preset and how to apply it to every participant's space

### Requirement: A cold-open script
`docs/facilitator/` SHALL contain a step-by-step script for the five-minute cold open - one prompt becomes a green test, the drift preset breaks the suite, healing repairs it - with the exact commands, the expected output of each step, and a recorded backup to switch to without debugging on stage.

#### Scenario: The cold open flakes
- **WHEN** a step of the cold open does not produce its expected output
- **THEN** the script names the recorded backup and where it is

### Requirement: The cut order
`docs/facilitator/` SHALL state the pre-agreed cut order for overruns - the Module 8 lab, then the Module 9 stretch goal, then Module 7's stretch B - and the plan for a beginner-heavy audience: Module 8 as demo only, its lab time given to Module 2.

#### Scenario: Running 15 minutes late after lunch
- **WHEN** the facilitator is behind schedule at Module 8
- **THEN** the run sheet says to show Module 8 as a demo and skip its lab

### Requirement: A triage playbook
`docs/facilitator/` SHALL contain a playbook for the co-host: the failures participants most likely hit, how `setup-check` reports each, and the fix, plus when to move a participant to the shared instance or pair them up.

#### Scenario: A participant's Docker is blocked by a proxy
- **WHEN** the co-host looks up a blocked image pull
- **THEN** the playbook names the check that reports it and the move to the shared instance

### Requirement: Fallback transcripts
The `solutions` branch SHALL contain, under `transcripts/`, one recorded agent walkthrough per lab, taken from the rehearsal runs, so that a participant whose agent fails can follow along. The transcripts SHALL be published on the documentation site, and each lab SHALL link its transcript there. Transcripts SHALL contain no credential, token or API key, and no path or name from the machine they were recorded on.

#### Scenario: A participant's agent fails in Lab 6
- **WHEN** a participant's agent access fails during Lab 6
- **THEN** Lab 6 links its transcript on the site, which shows every prompt and the agent's actions and results

#### Scenario: Scanning the transcripts
- **WHEN** the transcripts are scanned for secrets and local paths
- **THEN** nothing is found

### Requirement: A RobotCode cheat sheet
`docs/robotcode.md` SHALL tell participants, for this repository:
- which RobotCode command answers which question;
- an example of each command that runs here;
- how an agent drives the REPL and the debugger without waiting at a prompt;
- the traps of the pinned versions a participant can meet in the labs.

It SHALL be linked from Lab 4 and from the glossary's RobotCode entry, and published on the documentation site. It SHALL NOT name a planted defect, the suite's inline locator or the cause of a test broken on purpose.

#### Scenario: Running the examples
- **WHEN** a participant runs the page's examples on a fresh checkout, after Lab 0, with the shop in `clean`
- **THEN** each runs and prints what the page shows, allowing for shortened output

#### Scenario: An agent at the debugger
- **WHEN** an agent inspects a failing test with the debugger the way the page describes
- **THEN** the run ends without anyone typing at a prompt

#### Scenario: Finding the page
- **WHEN** a participant reads Lab 4 or the glossary's RobotCode entry
- **THEN** a link leads to the cheat sheet, and the site lists it under *Guides*

#### Scenario: Checked like lab material
- **WHEN** `tools/check_labs.py` runs
- **THEN** it checks the cheat sheet for giveaways, as it checks the labs and the glossary

### Requirement: One boundary between Tier 3 and Tier 4
The glossary, the curriculum and the labs SHALL tell Tier 3 from Tier 4 by persistence:
- tools of Tier 3, such as RobotCode's REPL and debugger, reach the running system only while one command runs;
- Tier 4 keeps a session open across the agent's steps.

None of them SHALL say that Tiers 1 to 3 cannot reach the running system.

#### Scenario: Reading the glossary
- **WHEN** a participant reads the ladder and the entries *Tier* and *MCP* in `GLOSSARY.md`
- **THEN** they name a session that stays open across the agent's steps as what Tier 4 adds

#### Scenario: From Lab 4 to Lab 6
- **WHEN** a participant who drove a visible browser through the REPL in Lab 4 starts Lab 6
- **THEN** Lab 6's opening says what the MCP server adds to that, and does not claim the agent has never seen the page

### Requirement: A guide to building libraries and tools
`docs/building-with-agents.md` SHALL describe, for participants, how to prepare an agent before it builds a Robot Framework library or tool:
- the five kinds of context, as headings in a project's `AGENTS.md`: toolstack, references, concepts, examples and the specification;
- why the project starts outside any other project's folder;
- which User Guide chapters and Robot API pages to point the agent to, for the pinned Robot Framework version;
- how to save a reference the agent cannot fetch.

It SHALL be linked from both bonus labs and listed on the site. The curriculum's Module 10 and the run sheet SHALL name the bonus chapters in the Monday plan.

#### Scenario: Preparing an agent for a listener
- **WHEN** a participant reads the guide before writing a listener
- **THEN** it names the User Guide's *Listener interface* chapter and the `robot.api.interfaces.ListenerV3` entry on the Robot API's `robot.api` page, both for Robot Framework 7.5

#### Scenario: A reference behind a bot wall
- **WHEN** the agent cannot fetch a service's API manual, as with TestRail's
- **THEN** the guide says how to save the reference into the project and point the agent to the saved file
