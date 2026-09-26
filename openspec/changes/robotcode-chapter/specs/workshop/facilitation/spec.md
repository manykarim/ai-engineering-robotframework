## ADDED Requirements

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
