# workshop/lab-assets Specification

## Purpose
Provides the skills, hooks, subagent definitions and MCP configurations the labs install and wire, so that participants spend lab time on the ideas rather than on configuration syntax, with the same behaviour in every supported agent.

## Requirements

### Requirement: A skill template
`skills/template/` SHALL contain a `SKILL.md` with a name, a triggering description, instructions and an example of a bundled helper script, which a participant can copy and turn into a skill that enforces one convention of `docs/conventions.md`. The template SHALL load as a skill in Claude Code, Codex and GitHub Copilot once copied to that agent's skill folder.

#### Scenario: Copying the template
- **WHEN** a participant copies the template to their agent's skill folder and renames it
- **THEN** the agent lists the skill, and a prompt that matches its description triggers it while an unrelated prompt does not

### Requirement: A Jira skill without shared credentials
`skills/jira-ticket/` SHALL contain a skill that files a bug in Jira Cloud with reproduction steps from a real run. It SHALL read the Jira site, user and token only from the environment or `.env`, and SHALL offer a dry run that prints the request instead of sending it, so that it can be tried without a Jira site.

#### Scenario: No Jira site configured
- **WHEN** the skill runs without Jira settings
- **THEN** it prints the issue it would file and states which settings are missing, and sends nothing

### Requirement: Hooks as guardrails
`hooks/` SHALL provide four hooks, each of which also runs as a plain command:
- after an edit to a test or resource file, one runs the affected tests and reports the result;
- after such an edit, one checks the file statically, without the shop, and reports only its errors, briefly;
- before an edit, one rejects a locator literal written into a file under `tests/`;
- before a commit, one blocks it when the latest suite run failed or predates the latest change to `tests/` or `resources/`.

#### Scenario: An inline locator is written
- **WHEN** an agent's edit would add `Click    css=button.buy` to a test file
- **THEN** the hook rejects the edit and names the convention it breaks

#### Scenario: Scanning the shipped suite
- **WHEN** the inline-locator hook runs as a command over `tests/` on `main`
- **THEN** it reports exactly one finding

#### Scenario: Committing after a red run
- **WHEN** the latest suite run has a failing test that is not tagged `broken` and the agent runs `git commit`
- **THEN** the hook blocks the commit and says which tests failed

#### Scenario: Only tests tagged broken failed
- **WHEN** the only failing tests of the latest, up-to-date suite run are tagged `broken`, and the agent runs `git commit`
- **THEN** the hook lets the commit through: a test tagged `broken` does not count as a failure

#### Scenario: A misspelled keyword is written
- **WHEN** an agent's edit calls a keyword that no imported resource or library defines, in a test file
- **THEN** within seconds, and with the shop stopped, the static check reports the line and the missing keyword to the agent

#### Scenario: A clean file is edited
- **WHEN** an agent's edit leaves a test or resource file without errors
- **THEN** the static check gives the agent no output

#### Scenario: Checking the shipped suite statically
- **WHEN** the static check runs as a command over `tests/` and `resources/` on `main`
- **THEN** it reports no finding

### Requirement: Hooks for every supported agent
`hooks/` SHALL document how to wire each hook into Claude Code, Codex and GitHub Copilot, and the hooks SHALL behave the same in each agent. A hook that adds context, for example at the start of a session, SHALL reach the conversation in each of the three agents.

#### Scenario: Wiring in a second agent
- **WHEN** a participant wires the inline-locator hook into Codex or GitHub Copilot as documented
- **THEN** an edit adding an inline locator is rejected there too

#### Scenario: Context at the start of a session
- **WHEN** a participant wires a session-start hook as `docs/hooks.md` shows it, which adds the shop's status, and asks a new session of any of the three agents which preset the shop is in
- **THEN** the agent answers from the added context, without running a command

#### Scenario: Wiring only one agent
- **WHEN** a participant wires the provided hooks for one agent only, as documented, and works in that agent
- **THEN** every hook runs once per matching action, not twice

### Requirement: Subagents with divided responsibilities
`agents/` SHALL define three subagents: a writer that drafts tests and keywords following `docs/conventions.md`; a reviewer that reviews changes against the conventions and the `shop/*` specs and cannot edit files; and a runner that runs tests and reports results through `robotcode results` and cannot edit files. `agents/` SHALL document where each supported agent loads them from.

#### Scenario: Asking the reviewer to fix something
- **WHEN** the reviewer subagent is asked to change a file
- **THEN** it has no tool to do so and reports the change as a finding instead

### Requirement: MCP configuration per agent
`mcp/` SHALL provide a configuration of the Robot Framework MCP server for Claude Code, Codex and GitHub Copilot. Each SHALL start the server from the project's own environment at the pinned version, SHALL reach the shop that `SHOP_URL` and `SHOP_SPACE` select, and SHALL contain no credential.

#### Scenario: Live access in a shared space
- **WHEN** a participant with `SHOP_SPACE=octocat` connects the MCP server as documented and opens a shop page through it
- **THEN** the page reports the space `octocat`

### Requirement: Third-party agent plugins are pinned
The labs SHALL install the RobotCode agent plugin and the Robot Framework Agent Skills at versions the setup guide names, and SHALL install the agent skills into the project rather than the user's global configuration.

#### Scenario: Installing the agent skills in Lab 3
- **WHEN** a participant follows Lab 3's install step
- **THEN** the installed version is the one `SETUP.md` names, and the files land inside the repository

### Requirement: A hooks page for newcomers
`docs/hooks.md` SHALL introduce hooks to a participant who has never written one: what a hook is and where in the agent's loop it acts; the events the three agents share, under each agent's name, with links to their documentation; the three ways a hook answers; the wiring for each agent, side by side; the static check as a worked example; and hooks worth writing for Robot Framework work, in all three agents. The page SHALL give no lab's answer away.

#### Scenario: Reading the hooks page
- **WHEN** a participant who has never written a hook reads `docs/hooks.md`
- **THEN** they can name the event to use for a check after every edit of a `.robot` file, and find its name and the wiring in their own agent

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
