# workshop/solutions Specification

## Purpose
Keeps reference solutions for every lab available to participants and facilitators without ever changing the starting state participants fork.

## Requirements

### Requirement: A solutions branch
The repository SHALL have a `solutions` branch that starts from `main` and adds the result of each lab that produces files, in lab order, one commit per lab, in the same folder structure. Each lab commit's message SHALL start with the lab's folder name.

On top of the lab commits, the branch SHALL hold the reference material, in commits whose messages start with `reference`:
- the reference pages under `solutions/`;
- the transcripts under `transcripts/`;
- the facilitators' answer sheet under `docs/facilitator/`.

#### Scenario: Comparing with the reference
- **WHEN** a participant runs `git log --oneline main..origin/solutions`
- **THEN** they see one commit per lab that produces files, then the reference commits, and can diff any lab's result against their own

#### Scenario: Finding the reference material
- **WHEN** a maintainer checks out the `solutions` branch
- **THEN** `solutions/` holds a reference page per lab, `transcripts/` a transcript per lab, and `docs/facilitator/` the expected outcomes of the suite with their reasons

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

### Requirement: Reference pages
For every lab, the `solutions` branch SHALL hold a page under `solutions/`. It SHALL show:
- the lab's reference result, with its key files;
- why that is a good result;
- the answers a facilitator debriefs;
- how participants compare their own work with it.

The pages SHALL be published on the documentation site, and every lab SHALL link its page there.

#### Scenario: Comparing an AGENTS.md
- **WHEN** a participant opens Lab 2's reference page from Lab 2
- **THEN** they read the reference `AGENTS.md` in full, why each of its sections is there, and the command that diffs their own file against it

#### Scenario: A lab that produces no files
- **WHEN** a participant opens Lab 9's reference page
- **THEN** it shows what the lab's result looks like on GitHub, and links the transcript that recorded it

### Requirement: No answers on main
No file on `main` SHALL contain:
- a lab's reference result, a transcript or the facilitators' answer sheet;
- a statement of the cause of a test broken on purpose, of a planted defect, or of where the suite's inline locator is.

Exempt are the tests and resources the labs work on, and the shop's specifications, which state correct behaviour. A check SHALL scan every file on `main` for these answers. The places the reference material lives on the `solutions` branch SHALL be ignored by git on `main`.

#### Scenario: An agent searches for a broken test
- **WHEN** an agent searches `main` for the name of a test broken on purpose
- **THEN** no line it finds states that test's cause

#### Scenario: An answer slips back in
- **WHEN** a commit on `main` adds a sentence that states a planted defect
- **THEN** the check names the file and what it gives away, and exits with a non-zero status

#### Scenario: Building the site locally
- **WHEN** a maintainer adds the reference material to a checkout of `main` to build the site
- **THEN** git does not offer those files for a commit

### Requirement: Reference projects of the bonus labs
The `solutions` branch SHALL hold the reference project of each bonus lab under `bonus/<lab folder>/`, without its virtual environment or build output, in a commit whose message starts with the bonus lab's folder name. The reference project's own checks SHALL pass: its unit tests, its Robot Framework tests against a freshly reset local shop where it has any, and `uv build`.

#### Scenario: Comparing a library with the reference
- **WHEN** a participant fetches the `solutions` branch after the library lab
- **THEN** `bonus/bonus-1-library/` holds the rehearsal's library, with its `AGENTS.md`, its `openspec/` folder, its saved references and its tests

#### Scenario: Checking the reference projects
- **WHEN** a maintainer runs each reference project's checks from a checkout of the `solutions` branch
- **THEN** they pass
