## Purpose

Defines the hands-on labs participants work through on the day: where each lab lives, what it states before the first step, the state it starts from and what "done" means, so that every participant can follow, catch up, or rejoin at the next module.

## ADDED Requirements

### Requirement: One folder per lab
The repository SHALL contain one folder under `labs/` for each module with hands-on work: `lab-00-arrival`, `lab-02-context`, `lab-03-skills`, `lab-04-robotcode`, `lab-05-prompt-to-green`, `lab-06-mcp`, `lab-07-hooks-toolbelt`, `lab-08-healing` and `lab-09-ci`. Each folder SHALL contain `INSTRUCTIONS.md` and `checklist.md`.

#### Scenario: Listing the labs
- **WHEN** the `labs/` folder is listed
- **THEN** it contains exactly those nine folders, and each holds an `INSTRUCTIONS.md` and a `checklist.md`

### Requirement: What every lab states up front
Every `INSTRUCTIONS.md` SHALL state, before its first step: the module, the lab's time budget, the preset the shop must be in, the prerequisites, and the starting state. It SHALL then give numbered steps, a stretch goal and a pointer to the lab's fallback transcript. The time budget SHALL equal the lab share of that module in the timetable of the master preparation document.

#### Scenario: Reading a lab's header
- **WHEN** a participant opens any lab's `INSTRUCTIONS.md`
- **THEN** the module, time budget, preset, prerequisites and starting state appear before step 1

#### Scenario: Checking time budgets
- **WHEN** the lab time budgets are compared with the timetable
- **THEN** Lab 2 and Lab 3 have 25 minutes, Lab 4 25, Lab 5 30, Lab 6 25, Lab 7 20, Lab 8 12 and Lab 9 15, and Lab 0 fills its 30-minute module

### Requirement: Done is checkable
Every `checklist.md` SHALL list what "done" looks like as items a participant can check without a facilitator: a file that exists, a command whose output they compare, or a test result.

#### Scenario: Checking a lab off
- **WHEN** a participant has finished a lab's steps
- **THEN** every item of its checklist names something they can verify on their own machine

### Requirement: Rejoin at any module
Every lab SHALL start from a state that `main` provides, plus at most the result of earlier labs that its instructions name, and SHALL say how to catch up when that earlier result is missing. A participant who missed a lab SHALL be able to start the next one.

#### Scenario: A participant missed Lab 3
- **WHEN** a participant starts Lab 4 without having done Lab 3
- **THEN** Lab 4's instructions either do not need Lab 3's result or say how to obtain it

### Requirement: The preset is always explicit
Every lab SHALL state which preset the shop needs and how to apply it, for the local shop and for a space on the shared instance alike. Labs SHALL apply presets only through the shop helper, and the lab that ends in a changed preset SHALL end by resetting it.

#### Scenario: Module 8 on the shared instance
- **WHEN** a participant working in their own space starts Lab 8
- **THEN** the instructions apply `drift_and_bug` to their space with the shop helper, and the last step resets it

### Requirement: Module 5 is spec-driven
Lab 5 SHALL have the participant pick one story - WEB-004 (easier), WEB-003 (medium) or WEB-005 (harder) - and automate a named slice of three or four of its criteria through OpenSpec: propose, a pair review of the plan in a breakout before any test exists, apply, then run and refine. WEB-007 SHALL be documented as the swap-in story and API-005 as the stretch goal. Lab 5 SHALL also have the participant debug the suite's Module 5 broken test in conversation. Lab 5 MUST work with Tiers 1 to 3 alone and MUST NOT require an MCP server.

#### Scenario: The pair review
- **WHEN** a participant has run the propose step
- **THEN** the lab has them review the proposal, specs and tasks with a partner before they apply it

#### Scenario: Without MCP
- **WHEN** Lab 5 is followed with no MCP server configured
- **THEN** every step can be completed

### Requirement: Only the lab stories are copied
The story files of WEB-003, WEB-004, WEB-005, WEB-007 and API-005 SHALL be copied from the demo shop's repository into `labs/lab-05-prompt-to-green/stories/`, unchanged. No other story file, and nothing from the demo shop's conformance record, SHALL be copied.

#### Scenario: Listing the stories
- **WHEN** `labs/lab-05-prompt-to-green/stories/` is listed
- **THEN** it holds exactly the five story files, each identical to its source at the pinned shop version

### Requirement: Module 8 shows both healing paths
Lab 8 SHALL apply `drift_and_bug`, run the suite with the healing profile, and have participants triage every heal of the healing report as accept, reject or investigate, while the price and total failures stay red. It SHALL offer a path for participants without a healing model, and SHALL offer repairing a drifted locator in conversation with the coding agent, using `robotcode robot-debug` and the MCP server, as its stretch goal.

#### Scenario: A participant without a healing model
- **WHEN** a participant has no `HEAL_*` settings
- **THEN** Lab 8 has them triage a recorded healing report instead, and the agentic stretch goal still works for them

### Requirement: Labs do not give the answers away
Participant-facing lab material SHALL NOT name the planted defects, the suite's inline locator, or the cause of a test broken on purpose. It MAY say where to look.

#### Scenario: Reading Lab 7
- **WHEN** a participant reads Lab 7's instructions before running the suite under `buggy`
- **THEN** they learn how to find and file a defect, but not which defects exist

### Requirement: Rehearsed labs
Before the workshop's `main` is tagged, every lab SHALL have been run end to end with the pinned stack on a clean checkout, Lab 5 without an MCP server, and Labs 2 to 4 once more with a second supported agent. Each rehearsal SHALL leave a transcript.

#### Scenario: Checking the rehearsal record
- **WHEN** a facilitator prepares the workshop
- **THEN** a transcript exists for every lab, and the facilitator guide records the second-agent run of Labs 2 to 4 and where its instructions diverged
