## Purpose

Tells each participant before the workshop, with one command, whether their environment will work on the day, and exactly how to fix it if it will not.

## ADDED Requirements

### Requirement: One command for the whole environment
The repository SHALL provide one documented command, run from the repository root, that checks every component the core track needs from Module 0 to Module 9. It MUST exit with status 0 when no check fails and with a non-zero status when any check fails.

#### Scenario: Everything in place
- **WHEN** every required component is installed at its pinned version and the shop is reachable
- **THEN** every check passes or warns and the command exits with status 0

#### Scenario: A required component missing
- **WHEN** a component the core track needs is absent
- **THEN** its check fails and the command exits with a non-zero status

### Requirement: Versions, not presence
For every pinned component, the check SHALL compare the installed version with the pinned version and SHALL fail on any mismatch, naming both versions.

#### Scenario: Wrong version installed
- **WHEN** Robot Framework is installed at a version other than the pinned one
- **THEN** the check fails and reports the version found and the version expected

### Requirement: One source for expected versions
The expected versions SHALL be read from the same sources the installation uses: the lockfile for Python packages, the manifest's workshop settings for tools outside Python, and the shop's compose file for the shop image. The check MUST NOT keep its own list of versions.

#### Scenario: Pinned version bumped
- **WHEN** a pinned version is changed in its source and the environment is updated accordingly
- **THEN** the check expects the new version without any edit to the check itself

### Requirement: Known pitfalls are detected
The check SHALL detect and explain each of these known failure causes: RobotCode on the `PATH` resolving outside the project environment; the browser library's separate Node.js dependencies installed on top of the bundled runtime; browser binaries missing from the project environment, for example after it was recreated; and a headless browser that cannot be started.

#### Scenario: Browser binaries missing after the environment was recreated
- **WHEN** the project environment has been recreated and the browser binaries were not installed again
- **THEN** the check fails and prints the command that installs them

#### Scenario: Separate Node.js dependencies installed
- **WHEN** the browser library's separate Node.js dependencies have been installed alongside the bundled runtime
- **THEN** the check fails, explains the conflict, and prints the command that removes them

#### Scenario: Global RobotCode first on PATH
- **WHEN** the first `robotcode` on the `PATH` does not belong to the project environment
- **THEN** the check warns and names both installations

### Requirement: The shop is reachable in the chosen mode
The check SHALL verify the shop in the mode the participant has configured. In local mode it MUST verify that the container runtime is reachable, that the pinned shop image is available, and that the shop answers its health check with the pinned version. In shared mode it MUST verify that the shared instance answers its health check and that a space is configured, valid for the shop's space format, and not `default`.

#### Scenario: Local shop not running
- **WHEN** no space is configured and nothing answers at the configured shop URL
- **THEN** the check fails and prints the command that starts the local shop

#### Scenario: Shared mode without a space
- **WHEN** the shop URL points at the shared instance and no space is configured
- **THEN** the check fails and explains how to set the space to the participant's GitHub handle

#### Scenario: Invalid space
- **WHEN** the configured space is `-bad--name-`
- **THEN** the check fails and describes the allowed format

### Requirement: Severity follows the curriculum
Every check SHALL name the first module that needs its component. A missing component that the core track needs SHALL fail; a missing component of an optional track, such as Azure DevOps or Jira, SHALL only warn.

#### Scenario: Optional track component missing
- **WHEN** the Azure command line is not installed
- **THEN** its check warns, names the module that uses it, and the command still exits with status 0

### Requirement: Every problem comes with a fix
Every failed or warned check SHALL print a one-line fix and a reference to the matching section of the setup guide.

#### Scenario: A failed check
- **WHEN** any check fails
- **THEN** its output contains a fix and a setup guide reference

### Requirement: Shareable output without secrets
The check SHALL be able to report its full result as JSON suitable for pasting into the setup-problem issue template. Neither form of output MUST contain the value of a credential, token or API key; a configured secret MUST be reported only as present or absent.

#### Scenario: API key configured
- **WHEN** a healing API key is configured and the JSON report is requested
- **THEN** the report states that the key is present and does not contain its value

### Requirement: Offline mode
The check SHALL offer an offline mode that skips every check needing network access and reports those checks as skipped rather than failed.

#### Scenario: Behind a blocking proxy
- **WHEN** the check runs in offline mode without network access
- **THEN** the network checks are reported as skipped and the command's exit status reflects only the local checks

### Requirement: Read-only
The check SHALL NOT install, modify, start or stop anything. Its only side effects SHALL be starting and closing a headless browser and sending read-only requests.

#### Scenario: Shop stopped
- **WHEN** the local shop is not running
- **THEN** the check reports it and does not start it
