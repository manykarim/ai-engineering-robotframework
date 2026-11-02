## MODIFIED Requirements

### Requirement: What every lab states up front
Every `INSTRUCTIONS.md` SHALL state, before its first step: the module, or for a bonus lab its bonus chapter; the lab's time budget; the preset the shop must be in; the prerequisites; and the starting state. It SHALL then give numbered steps, a stretch goal and a pointer to the lab's fallback transcript.

For a lab of the timetable, the time budget SHALL equal the lab share of that module in the timetable of the master preparation document. A bonus lab SHALL state an estimated time instead, and that it is self-paced.

#### Scenario: Reading a lab's header
- **WHEN** a participant opens any lab's `INSTRUCTIONS.md`
- **THEN** the module, time budget, preset, prerequisites and starting state appear before step 1

#### Scenario: Checking time budgets
- **WHEN** the lab time budgets are compared with the timetable
- **THEN** Lab 2 and Lab 3 have 25 minutes, Lab 4 25, Lab 5 30, Lab 6 25, Lab 7 30, Lab 8 12 and Lab 9 15, and Lab 0 fills its 30-minute module

#### Scenario: Reading a bonus lab's header
- **WHEN** a participant opens a bonus lab's `INSTRUCTIONS.md`
- **THEN** it names its bonus chapter, states an estimated time, and says it is self-paced and not part of the day's timetable

## ADDED Requirements

### Requirement: Module 7 has participants write a hook
Lab 7 SHALL send the participant to `docs/hooks.md` first, have them wire the provided hooks and see each act, and then have their agent write a hook of their own, which they wire and trigger. Its checklist SHALL cover that hook. The suite scan and the defect filed with `gh` SHALL stay.

#### Scenario: Checking the own hook off
- **WHEN** a participant reads Lab 7's checklist
- **THEN** it has them check that their own hook is in their agent's wiring and refused or answered an action

#### Scenario: Writing a hook in any agent
- **WHEN** a participant follows Lab 7 with Claude Code, Codex or GitHub Copilot
- **THEN** they end with a hook of their own in their agent's wiring, and an action of their agent that the hook refused or answered

#### Scenario: Reading Lab 7 before the hooks page
- **WHEN** a participant opens Lab 7
- **THEN** its first step sends them to `docs/hooks.md`, before any hook is wired
