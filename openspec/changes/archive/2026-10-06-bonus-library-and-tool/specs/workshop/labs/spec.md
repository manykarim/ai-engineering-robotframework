## MODIFIED Requirements

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

## ADDED Requirements

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
