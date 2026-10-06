# workshop/labs Specification

## Purpose
Defines the hands-on labs participants work through on the day: where each lab lives, what it states before the first step, the state it starts from and what "done" means, so that every participant can follow, catch up, or rejoin at the next module.

## Requirements

### Requirement: One folder per lab
The repository SHALL contain one folder under `labs/` for each module with hands-on work: `lab-00-arrival`, `lab-02-context`, `lab-03-skills`, `lab-04-robotcode`, `lab-05-prompt-to-green`, `lab-06-mcp`, `lab-07-hooks-toolbelt`, `lab-08-healing` and `lab-09-ci`. It SHALL also contain the folders of the two bonus labs, `bonus-1-library` and `bonus-2-tool`. Each folder SHALL contain `INSTRUCTIONS.md` and `checklist.md`.

#### Scenario: Listing the labs
- **WHEN** the `labs/` folder is listed
- **THEN** it contains exactly those nine lab folders and the two bonus folders, and each holds an `INSTRUCTIONS.md` and a `checklist.md`

### Requirement: What every lab states up front
Every `INSTRUCTIONS.md` SHALL state, before its first step: the module, or for a bonus lab its bonus chapter; the lab's time budget; the preset the shop must be in; the prerequisites; and the starting state. It SHALL then give numbered steps, a stretch goal and a pointer to the lab's fallback transcript.

For a lab of the timetable, the time budget SHALL equal the lab share of that module in the timetable of the master preparation document. A bonus lab SHALL state an estimated time instead, and that it is self-paced.

#### Scenario: Reading a lab's header
- **WHEN** a participant opens any lab's `INSTRUCTIONS.md`
- **THEN** the module, time budget, preset, prerequisites and starting state appear before step 1

#### Scenario: Checking time budgets
- **WHEN** the lab time budgets are compared with the timetable
- **THEN** Lab 2 and Lab 3 have 25 minutes, Lab 4 25, Lab 5 30, Lab 6 25, Lab 7 20, Lab 8 12 and Lab 9 15, and Lab 0 fills its 30-minute module

#### Scenario: Reading a bonus lab's header
- **WHEN** a participant opens a bonus lab's `INSTRUCTIONS.md`
- **THEN** it names its bonus chapter, states an estimated time, and says it is self-paced and not part of the day's timetable

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
Participant-facing material on `main` SHALL NOT name the planted defects, the suite's inline locator, or the cause of a test broken on purpose. It MAY say where to look. The reference pages and transcripts on the `solutions` branch show these answers by design. A lab MAY link them, and SHALL NOT quote them.

#### Scenario: Reading Lab 7
- **WHEN** a participant reads Lab 7's instructions before running the suite under `buggy`
- **THEN** they learn how to find and file a defect, but not which defects exist

#### Scenario: Following a reference link
- **WHEN** a participant opens Lab 4's reference page on the site
- **THEN** it explains the cause of the Module 4 broken test, while no file on `main` states it

### Requirement: Rehearsed labs
Before the workshop's `main` is tagged, every lab SHALL have been run end to end with the pinned stack on a clean checkout, Lab 5 without an MCP server, and Labs 2 to 4 once more with a second supported agent. Each rehearsal SHALL leave a transcript.

#### Scenario: Checking the rehearsal record
- **WHEN** a facilitator prepares the workshop
- **THEN** a transcript exists for every lab, and the facilitator guide records the second-agent run of Labs 2 to 4 and where its instructions diverged

### Requirement: Bonus labs
The bonus labs SHALL teach how to build a Robot Framework library and a Robot Framework tool with an agent, spec-driven:
- `bonus-1-library`: a Python library for the DemoShop's REST API, with assertion operators from AssertionEngine and keywords in the style of Browser's;
- `bonus-2-tool`: a listener, version 3, that reports failed tests to the public GitHub API as issues, and makes no request in its default dry run.

Each bonus lab SHALL:
- build its project in a new folder outside the workshop clone;
- have the participant write the project's `AGENTS.md` and OpenSpec context before the first prompt: the toolstack, with `uv` for dependencies and packaging; the references, for the versions in use; the concepts to follow; and keywords or code to imitate;
- save into the project every reference the agent needs and might not be able to fetch;
- need no account beyond those the workshop's setup already asks for.

The bonus labs SHALL be self-paced, outside the day's timetable and its cut order. They SHALL follow every other rule for labs: a checklist, a stretch goal, a rehearsal that leaves a transcript, and a reference page.

#### Scenario: Starting the library lab
- **WHEN** a participant follows `bonus-1-library` after the workshop, with the local shop running
- **THEN** they end with a package that `uv build` builds, whose keywords pass their own acceptance tests against the shop, and whose `Get` keywords accept an assertion operator

#### Scenario: Starting the tool lab without a token
- **WHEN** a participant runs the workshop's suite with the `bonus-2-tool` listener and no GitHub token
- **THEN** the run reports the issue it would open for each failed test, sends nothing, and its result is the same as without the listener

#### Scenario: A new project's context
- **WHEN** a participant starts either bonus lab's project
- **THEN** its agent loads the new project's `AGENTS.md`, and not the workshop clone's
