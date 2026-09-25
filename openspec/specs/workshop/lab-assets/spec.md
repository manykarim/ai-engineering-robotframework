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
`hooks/` SHALL provide three hooks: one that runs the tests affected by an edit to a test or resource file and reports the result to the agent; one that rejects an edit that writes a locator literal into a file under `tests/`; and one that blocks a commit when the latest suite run failed or is older than the latest change to `tests/` or `resources/`. Tests tagged `broken` SHALL NOT count as failures. Each hook SHALL also run as a plain command, outside any agent.

#### Scenario: An inline locator is written
- **WHEN** an agent's edit would add `Click    css=button.buy` to a test file
- **THEN** the hook rejects the edit and names the convention it breaks

#### Scenario: Scanning the shipped suite
- **WHEN** the inline-locator hook runs as a command over `tests/` on `main`
- **THEN** it reports exactly one finding

#### Scenario: Committing after a red run
- **WHEN** the latest suite run has a failing test that is not tagged `broken` and the agent runs `git commit`
- **THEN** the hook blocks the commit and says which tests failed

### Requirement: Hooks for every supported agent
`hooks/` SHALL document how to wire each hook into Claude Code, Codex and GitHub Copilot. The hooks SHALL behave the same in each agent.

#### Scenario: Wiring in a second agent
- **WHEN** a participant wires the inline-locator hook into Codex or GitHub Copilot as documented
- **THEN** an edit adding an inline locator is rejected there too

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
