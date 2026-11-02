## MODIFIED Requirements

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

## ADDED Requirements

### Requirement: A hooks page for newcomers
`docs/hooks.md` SHALL introduce hooks to a participant who has never written one: what a hook is and where in the agent's loop it acts; the events the three agents share, under each agent's name, with links to their documentation; the three ways a hook answers; the wiring for each agent, side by side; the static check as a worked example; and hooks worth writing for Robot Framework work, in all three agents. The page SHALL give no lab's answer away.

#### Scenario: Reading the hooks page
- **WHEN** a participant who has never written a hook reads `docs/hooks.md`
- **THEN** they can name the event to use for a check after every edit of a `.robot` file, and find its name and the wiring in their own agent
