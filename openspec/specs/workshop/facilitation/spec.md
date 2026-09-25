# workshop/facilitation Specification

## Purpose
Gives facilitators and participants the shared vocabulary, the environment choices, the run sheet for the day and the fallbacks for when something fails live, so that the workshop runs the same way whoever leads it.

## Requirements

### Requirement: A glossary
`GLOSSARY.md` SHALL define every term the labs use that a Robot Framework user without agent experience may not know, including the five tiers of the maturity ladder, and SHALL be readable in about ten minutes.

#### Scenario: A term from a lab
- **WHEN** a lab uses a term such as "skill", "hook", "subagent", "MCP", "preset", "space" or "heal"
- **THEN** `GLOSSARY.md` defines it

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
`transcripts/` SHALL contain one recorded agent walkthrough per lab, taken from the rehearsal runs, so that a participant whose agent fails can follow along. Transcripts SHALL contain no credential, token or API key, and no path or name from the machine they were recorded on.

#### Scenario: A participant's agent fails in Lab 6
- **WHEN** a participant's agent access fails during Lab 6
- **THEN** Lab 6 points them to its transcript, which shows every prompt and the agent's actions and results

#### Scenario: Scanning the transcripts
- **WHEN** the transcripts are scanned for secrets and local paths
- **THEN** nothing is found
