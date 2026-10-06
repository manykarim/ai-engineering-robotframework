## MODIFIED Requirements

### Requirement: A glossary
`GLOSSARY.md` SHALL define every term the labs use that a Robot Framework user without agent experience may not know, including the five tiers of the maturity ladder, context engineering and spec-driven development, and SHALL be readable in about ten minutes.

Where an entry names agent tooling or a practice, it SHALL link the documentation a reader goes to next: the standard, the tool's repository, or an agent's own documentation, labelled with whose it is.

#### Scenario: A term from a lab
- **WHEN** a lab uses a term such as "skill", "hook", "subagent", "MCP", "preset", "space", "heal" or "context engineering"
- **THEN** `GLOSSARY.md` defines it

#### Scenario: Reading on after the day
- **WHEN** a participant wants to know more about skills, subagents, hooks, context files, context engineering or spec-driven development
- **THEN** the glossary entry links a source to read next, and says whose documentation it is
