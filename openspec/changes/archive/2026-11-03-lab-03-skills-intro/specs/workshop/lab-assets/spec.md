## ADDED Requirements

### Requirement: A skills page for newcomers
`docs/skills.md` SHALL introduce skills to a participant who has never written one: what a skill is, and when to use one rather than a context file, hook, MCP server or subagent; how an agent loads it; the folder and its required fields; where each agent finds skills; the template as a worked example; rules for a good skill, with their sources; and how to evaluate one. It SHALL give no lab's answer away.

#### Scenario: Reading the skills page
- **WHEN** a participant who has never written a skill reads `docs/skills.md`
- **THEN** they can say why the description decides whether a skill loads, and find their own agent's skill folder

#### Scenario: Evaluating a skill
- **WHEN** a participant has written a skill and follows the page's evaluation section
- **THEN** they have a prompt that should load it, one that should not, and a way to compare a task's result with and without it

#### Scenario: One folder per agent
- **WHEN** the skills page and Lab 3 name the folder for a participant's own skill
- **THEN** both name the same folder for each agent
