# workshop/solutions Specification

## Purpose
Keeps reference solutions for every lab available to participants and facilitators without ever changing the starting state participants fork.

## Requirements

### Requirement: A solutions branch
The repository SHALL have a `solutions` branch that starts from `main` and adds the result of each lab that produces files, in lab order, one commit per lab, in the same folder structure. Each commit message SHALL start with the lab's folder name.

#### Scenario: Comparing with the reference
- **WHEN** a participant runs `git log --oneline main..origin/solutions`
- **THEN** they see one commit per lab that produces files, and can diff any lab's result against their own

### Requirement: Never merged into main
The `solutions` branch MUST NOT be merged into `main`, and `main` MUST NOT contain any lab's solution.

#### Scenario: Inspecting main
- **WHEN** `main` is inspected after a workshop
- **THEN** `AGENTS.md` is still the thin starting state, and no participant-built skill, hook wiring, MCP configuration or Module 5 test is present

### Requirement: Solutions pass
On the `solutions` branch, in a freshly reset space, every test SHALL pass, including the two tests `main` ships broken on purpose, which Labs 4 and 5 repair.

#### Scenario: Running the reference suite
- **WHEN** the suite runs on `solutions` against a clean shop
- **THEN** every test passes

### Requirement: Kept current with main
When `main` changes after the `solutions` branch was created, the branch SHALL be rebased onto the new `main` before the workshop tag, and SHALL still pass.

#### Scenario: A fix lands on main
- **WHEN** a fix is merged into `main` before the workshop
- **THEN** `solutions` is rebased onto it and its suite passes again
