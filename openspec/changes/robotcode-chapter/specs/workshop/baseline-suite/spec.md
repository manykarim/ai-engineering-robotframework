## ADDED Requirements

### Requirement: A visible browser on request
The suite's browser SHALL run headless unless the variable `HEADLESS` is set to false. A value given on the command line SHALL hold in a test run and in a RobotCode REPL session, also after the session imports the suite's resource files at run time. Without the variable, test runs, REPL sessions and MCP sessions SHALL start the browser headless.

#### Scenario: A visible browser in the REPL
- **WHEN** a REPL session starts with `-v HEADLESS:False`, imports `resources/shop.resource` and opens the shop's browser
- **THEN** the browser is visible

#### Scenario: A visible browser in a run
- **WHEN** a test is run with `-v HEADLESS:False`
- **THEN** its browser is visible

#### Scenario: Headless by default
- **WHEN** a test run, a REPL session or an MCP session opens the shop's browser without the variable
- **THEN** the browser is headless, and every preset's expected outcomes stay as recorded
