## MODIFIED Requirements

### Requirement: Reference projects of the bonus labs
The `solutions` branch SHALL hold the reference result of each bonus lab under `bonus/<lab folder>/`, in a commit whose message starts with the bonus lab's folder name.

For each of the two building labs, the result SHALL be the reference project, without its virtual environment or build output. The reference project's own checks SHALL pass: its unit tests, its Robot Framework tests against a freshly reset local shop where it has any, and `uv build`.

For the subagents lab, the result SHALL be:
- the debugger and the analyzer, in the format of each supported agent;
- the rehearsal's changes to the suite, as a patch against `main`.

The patch SHALL apply to `main`. With the patch applied:
- under `clean`, the only failing tests SHALL be the two that `main` ships broken on purpose;
- under `drift_and_bug`, with those two excluded, the only failing tests SHALL be those that fail on a defect of the shop;
- `robocop check` SHALL report no `replace-set-variable-with-var` or `replace-create-with-var` finding.

#### Scenario: Comparing a library with the reference
- **WHEN** a participant fetches the `solutions` branch after the library lab
- **THEN** `bonus/bonus-1-library/` holds the rehearsal's library, with its `AGENTS.md`, its `openspec/` folder, its saved references and its tests

#### Scenario: Comparing subagents with the reference
- **WHEN** a participant fetches the `solutions` branch after the subagents lab
- **THEN** `bonus/bonus-3-subagents/` holds the debugger and the analyzer for Claude Code, Codex and GitHub Copilot, and the patch the rehearsal made to the suite

#### Scenario: Checking the reference projects
- **WHEN** a maintainer runs each bonus lab's reference checks from a checkout of the `solutions` branch
- **THEN** they pass
