# workshop/toolchain Specification

## Purpose
Gives every participant the same reproducible toolchain from one documented install path, so that labs behave identically on every machine, on the day and afterwards.

## Requirements

### Requirement: Locked Python environment
The repository SHALL resolve every Python dependency exclusively from a committed lockfile, SHALL pin every direct dependency to an exact version, and SHALL keep the lockfile consistent with the project manifest. The documented install command MUST refuse to install when the lockfile is out of date rather than resolve anew.

#### Scenario: Locked install on a fresh clone
- **WHEN** a participant runs the documented install command on a fresh clone
- **THEN** the environment contains exactly the package versions recorded in the lockfile and no dependency is resolved at install time

#### Scenario: Stale lockfile
- **WHEN** a direct dependency is changed in the manifest without updating the lockfile and the install command is run
- **THEN** the command fails and reports that the lockfile is out of date

### Requirement: Stable releases only
The locked environment SHALL resolve with pre-release versions disallowed. A dependency whose optional features pull in a pre-release MUST be installed with only the features the workshop uses.

#### Scenario: Resolution without pre-releases
- **WHEN** the lockfile is regenerated with pre-release resolution disabled
- **THEN** resolution succeeds and every locked package is a final release

### Requirement: Workshop tool set
The environment SHALL provide Robot Framework, a Playwright-based browser library that runs without a separately installed Node.js toolchain, an HTTP API keyword library, the RobotCode command line with discovery, library documentation, debugging, an interactive REPL and results inspection, the Robot Framework MCP server with web and API support, and the self-healing listener.

#### Scenario: RobotCode habits are available
- **WHEN** a participant asks the project environment's RobotCode for help on `discover`, `libdoc`, `robot-debug`, `repl` and `results`
- **THEN** each of the five commands exists

#### Scenario: Browser library without a Node.js toolchain
- **WHEN** Node.js is absent from the machine and the documented install steps have been followed
- **THEN** a headless browser session can be opened from Robot Framework

### Requirement: RobotCode resolves the project's libraries
The documented way to run RobotCode SHALL execute the RobotCode installed in the project environment, so that discovery and library documentation reflect the project's installed libraries and versions, even when another RobotCode installation is on the participant's `PATH`.

#### Scenario: Global installation present
- **WHEN** a participant also has RobotCode installed globally and runs RobotCode the documented way
- **THEN** the project environment's RobotCode runs and reports the library versions from the lockfile

### Requirement: Named prerequisites outside Python
The setup guide SHALL name every prerequisite that is not installed by the locked environment - a container runtime for the local shop, Node.js for the OpenSpec command line, the OpenSpec command line at the pinned version, the GitHub command line, and at least one supported coding agent - each with its minimum version and the first module that needs it.

#### Scenario: Reading the prerequisites
- **WHEN** a participant reads the prerequisites in the setup guide
- **THEN** every entry shows a minimum version and the first module that needs it

### Requirement: Supported platforms
The toolchain SHALL install and run on Windows x64, macOS 13 or newer on Apple silicon and Intel, and Linux x64 and arm64 with glibc 2.28 or newer. The setup guide SHALL name every other platform as outside the tested set, together with its fallback.

#### Scenario: Platform outside the tested set
- **WHEN** a participant on Windows on Arm follows the setup guide
- **THEN** the guide names the fallback for that platform, and the environment check reports the platform as outside the tested set
