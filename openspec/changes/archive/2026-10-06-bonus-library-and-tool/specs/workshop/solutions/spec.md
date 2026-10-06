## ADDED Requirements

### Requirement: Reference projects of the bonus labs
The `solutions` branch SHALL hold the reference project of each bonus lab under `bonus/<lab folder>/`, without its virtual environment or build output, in a commit whose message starts with the bonus lab's folder name. The reference project's own checks SHALL pass: its unit tests, its Robot Framework tests against a freshly reset local shop where it has any, and `uv build`.

#### Scenario: Comparing a library with the reference
- **WHEN** a participant fetches the `solutions` branch after the library lab
- **THEN** `bonus/bonus-1-library/` holds the rehearsal's library, with its `AGENTS.md`, its `openspec/` folder, its saved references and its tests

#### Scenario: Checking the reference projects
- **WHEN** a maintainer runs each reference project's checks from a checkout of the `solutions` branch
- **THEN** they pass
