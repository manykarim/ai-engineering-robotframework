## MODIFIED Requirements

### Requirement: Workshop tool set
The environment SHALL provide Robot Framework, a Playwright-based browser library that runs without a separately installed Node.js toolchain, an HTTP API keyword library, the RobotCode command line with discovery, library documentation, debugging, an interactive REPL, results inspection and static analysis, the Robocop linter and formatter, the Robot Framework MCP server with web and API support, and the self-healing listener.

#### Scenario: RobotCode habits are available
- **WHEN** a participant asks the project environment's RobotCode for help on `discover`, `libdoc`, `robot-debug`, `repl`, `results` and `analyze`
- **THEN** each of the six commands exists

#### Scenario: Robocop is available
- **WHEN** a participant runs `uv run robocop --version` in the project environment
- **THEN** it prints the version that `uv.lock` records

#### Scenario: Browser library without a Node.js toolchain
- **WHEN** Node.js is absent from the machine and the documented install steps have been followed
- **THEN** a headless browser session can be opened from Robot Framework
