# Spec Delta

## Purpose

Turns the failed tests of a Robot Framework run into GitHub issues, one per test. A test that fails again gets a
comment on its open issue rather than a second issue, and a dry run shows exactly which requests would be sent.

## ADDED Requirements

### Requirement: Listener registration and arguments
The reporter SHALL be a Robot Framework listener, version 3, importable as
`robotframework_github_reporter.GitHubIssues`. It SHALL be registered with `--listener` and import from the package's
source folder alone (`--pythonpath`), without reading installed package metadata. At run time it SHALL need nothing
beyond the Python standard library and Robot Framework. It SHALL accept three arguments:
- `repo`, the target repository as `owner/name`. Without a valid one the reporter does nothing.
- `dry_run`, which defaults to `true`. Only a value Robot Framework converts to false, such as `false`, `no`, `off` or
  `0`, turns on a live run.
- `label`, which defaults to `robot-failure`. It must be non-empty and contain no comma.

No argument mistake SHALL stop the listener from loading. Each SHALL become a warning instead. The mistakes covered
are:
- a missing or malformed `repo`
- an invalid label
- an unknown named argument
- an extra positional argument
- a `dry_run` value that is neither true nor false

A warning about unknown arguments SHALL name them without their values.

#### Scenario: Defaults
- **WHEN** a run uses `--listener robotframework_github_reporter.GitHubIssues:repo=octo-org/demo`
- **THEN** the reporter runs as a dry run and uses the label `robot-failure`

#### Scenario: Arguments given by name
- **WHEN** a run uses `--listener robotframework_github_reporter.GitHubIssues:repo=octo-org/demo:dry_run=false:label=flaky`
- **THEN** the reporter runs live, targets `octo-org/demo` and uses the label `flaky`

#### Scenario: Imported from the source folder
- **WHEN** a run uses `--pythonpath src` in a Python environment where Robot Framework 7.5 is the only installed
  package, so that neither this package nor its metadata is installed
- **THEN** the listener loads and reports failures as it would if the package were installed

#### Scenario: Missing repository
- **WHEN** a run uses `--listener robotframework_github_reporter.GitHubIssues` with no arguments
- **THEN** the listener loads, logs one warning that `repo` is missing, reports nothing, and writes no
  `github-requests.json`

#### Scenario: Malformed repository
- **WHEN** `repo` is not of the form `owner/name`, with both parts non-empty and exactly one `/`
- **THEN** the reporter logs one warning naming the bad value, reports nothing for the rest of the run, and writes no
  `github-requests.json`

#### Scenario: Invalid label
- **WHEN** `label` is empty or contains a comma
- **THEN** the reporter logs one warning naming the bad value, reports nothing for the rest of the run, and writes no
  `github-requests.json`

#### Scenario: Unknown or extra arguments
- **WHEN** a run uses `repo=octo-org/demo:labels=flaky`, or passes a fourth positional argument
- **THEN** the listener loads, logs one warning naming `labels` (or the count of extra arguments) without their values,
  ignores them, and otherwise behaves as configured

#### Scenario: Unrecognized dry_run value
- **WHEN** a run uses `repo=octo-org/demo:dry_run=maybe`
- **THEN** the reporter logs one warning naming the value and runs as a dry run

### Requirement: One report per failed test
The reporter SHALL produce one report for each test whose status is FAIL, when that test ends. It SHALL produce none
for tests that pass or are skipped.

#### Scenario: Mixed results
- **WHEN** a suite has two failing tests, one passing test and one skipped test
- **THEN** the reporter produces two reports, one for each failing test

#### Scenario: No failures
- **WHEN** every test in the run passes
- **THEN** the reporter opens no issue and adds no comment

### Requirement: Issue content
A new issue SHALL be titled `Failing test: <full name>`, where `<full name>` is the test's full name (for example
`Suite.Sub Suite.Test Name`). It SHALL carry the configured label. Its body SHALL contain:
- the test's failure message, unchanged
- the test's source file and line, with the path relative to the current working directory when the file lies under
  it, and unchanged otherwise
- when the run happens in GitHub Actions (`GITHUB_ACTIONS` is `true`), the run's URL, built as
  `${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}`

#### Scenario: Failure outside GitHub Actions
- **WHEN** the test `Demo.Login Works`, at line 12 of `atest/demo.robot` under the working directory, fails with the
  message `Expected 200 but got 500`, and `GITHUB_ACTIONS` is not set
- **THEN** the issue's title is `Failing test: Demo.Login Works`
- **AND** its labels are exactly the configured label
- **AND** its body contains `Expected 200 but got 500` and `atest/demo.robot:12`, and no run URL

#### Scenario: Failure in GitHub Actions
- **WHEN** a test fails with `GITHUB_ACTIONS=true`, `GITHUB_SERVER_URL=https://github.com`,
  `GITHUB_REPOSITORY=octo-org/app` and `GITHUB_RUN_ID=42`
- **THEN** the body also contains `https://github.com/octo-org/app/actions/runs/42`

#### Scenario: Multi-line message
- **WHEN** the failure message spans several lines or contains backticks
- **THEN** the body shows the whole message verbatim, and its formatting does not leak into the rest of the body

### Requirement: Comment on a matching open issue
Before it opens an issue in a live run, the reporter SHALL look for an open issue in `repo` that carries the label and
whose title equals the new issue's title exactly. If one exists, the reporter SHALL add a comment to it instead of
opening a new issue. The comment SHALL contain the same failure message, source and line, and run URL that a new issue
would. The reporter SHALL ignore pull requests, closed issues and issues without the label. It SHALL fetch the list of
open labelled issues at most once per run, through every page, and SHALL count issues it opened earlier in the same
run as open.

#### Scenario: Matching open issue exists
- **WHEN** a live run fails `Demo.Login Works` and `repo` has open issue #7, titled `Failing test: Demo.Login Works`
  and labelled `robot-failure`
- **THEN** the reporter adds a comment to issue #7 and opens no new issue

#### Scenario: Only a closed issue matches
- **WHEN** the only issue with that title and label is closed
- **THEN** the reporter opens a new issue

#### Scenario: Title matches but the label is missing
- **WHEN** an open issue has that title but not the label
- **THEN** the reporter opens a new issue

#### Scenario: A pull request has that title
- **WHEN** the only open item with that title and label is a pull request
- **THEN** the reporter opens a new issue

#### Scenario: Matching issue on a later page
- **WHEN** the matching open issue is on the second page of results
- **THEN** the reporter finds it and adds a comment

#### Scenario: Several failures in one run
- **WHEN** three tests fail in one live run
- **THEN** the reporter lists the repository's open labelled issues once, not once per test

#### Scenario: Same full name twice in one run
- **WHEN** two tests with the same full name fail in one live run
- **THEN** the first opens an issue and the second adds a comment to it

### Requirement: Dry run
In a dry run the reporter SHALL NOT send any request, including the lookup. For each failed test it SHALL record the
requests a live run would send, assuming no matching issue exists:
- the lookup of open labelled issues, recorded once, before the first issue request
- the creation of an issue

When the top-level suite ends, the reporter SHALL print every recorded request to the console, in order, with its
method, URL and JSON body. It SHALL also write them, in the same order, to `github-requests.json` in the run's output
directory. The file SHALL be a JSON array whose items have `method` and `url`, plus `body` when the request has one.
The file SHALL be written even when nothing failed, as an empty array. Neither the console output nor the file SHALL
contain a token or any request header.

#### Scenario: Dry run of a failing suite
- **WHEN** a dry run with `repo=octo-org/demo` and two failing tests ends
- **THEN** no network request was made
- **AND** `github-requests.json` in the output directory holds, in order: a `GET` of
  `https://api.github.com/repos/octo-org/demo/issues` with `state=open`, `labels=robot-failure` and `per_page=100`,
  then two `POST`s to `https://api.github.com/repos/octo-org/demo/issues`, each with the issue's `title`, `body` and
  `labels`
- **AND** the console shows each of those three requests

#### Scenario: Dry run with no failures
- **WHEN** a dry run ends and no test failed
- **THEN** `github-requests.json` contains `[]`

#### Scenario: Custom output directory
- **WHEN** the run uses `--outputdir results/run1`
- **THEN** the file is written to `results/run1/github-requests.json`

#### Scenario: Token present during a dry run
- **WHEN** `GITHUB_TOKEN` is set and the run is a dry run
- **THEN** nothing is sent, and the token appears neither on the console nor in the file

### Requirement: Token handling
A live run SHALL authenticate with the token from the `GITHUB_TOKEN` environment variable or, when that is unset or
empty, from `GH_TOKEN`. The reporter SHALL NOT accept a token from a listener argument or a file, and SHALL NOT print,
log or write it. When `dry_run` is false and neither variable holds a token, the reporter SHALL log one warning and
behave exactly as a dry run for the whole run.

#### Scenario: GITHUB_TOKEN takes precedence
- **WHEN** both `GITHUB_TOKEN` and `GH_TOKEN` are set in a live run
- **THEN** requests are authenticated with `GITHUB_TOKEN`

#### Scenario: Only GH_TOKEN is set
- **WHEN** `GITHUB_TOKEN` is unset or empty and `GH_TOKEN` is set in a live run
- **THEN** requests are authenticated with `GH_TOKEN`

#### Scenario: Token given as an argument
- **WHEN** a run passes `token=s3cret` to the listener
- **THEN** the reporter logs one warning that tokens are read from `GITHUB_TOKEN` or `GH_TOKEN` only
- **AND** `s3cret` is never used to authenticate, and appears neither on the console nor in the log or any file the
  reporter writes

#### Scenario: No token in a live run
- **WHEN** `dry_run=false` and neither variable holds a token
- **THEN** the reporter logs one warning that it is falling back to a dry run, sends nothing, prints the requests and
  writes `github-requests.json`

### Requirement: The reporter never fails or changes a test
The reporter SHALL NOT fail, skip or otherwise change any test, whether its status or its message, and SHALL NOT
change the run's exit code. Every error of its own SHALL be logged as a Robot Framework warning, never as an error,
and the run SHALL continue. Two cases would let Robot Framework report an error: an exception escaping a listener
method, or the listener failing to load. Under `--exitonerror`, Robot Framework fails every test after an error, so
neither case may happen. Its own errors include an HTTP error status, a
network error or timeout, a malformed response and a file it cannot write. When the lookup of open issues fails, the
reporter SHALL skip that test's report rather than risk a duplicate issue, and SHALL try the lookup again for the next
failed test. A request that does not answer within a bounded time SHALL count as failed. When a request cannot reach
GitHub at all, through a connection error or a timeout, the reporter SHALL send no more requests for the rest of the
run, so that an unreachable network does not slow down every later failed test.

#### Scenario: Status and exit code unchanged
- **WHEN** a suite with two failing tests, one passing test and one skipped test runs with the reporter, in a dry run
  or live
- **THEN** the tests keep the statuses FAIL, FAIL, PASS and SKIP and their original messages, and `robot` exits with
  code 2, as it would without the reporter

#### Scenario: Misconfigured listener under --exitonerror
- **WHEN** a run with `--exitonerror` gives the listener no arguments, an unknown argument or `dry_run=maybe`
- **THEN** no error is reported, and every test keeps the status it would have without the listener

#### Scenario: Unexpected error inside the reporter
- **WHEN** reporting a failed test raises an unexpected exception, in a run with `--exitonerror`
- **THEN** the reporter logs a warning naming the test and the exception, and every test keeps its status

#### Scenario: GitHub rejects a request
- **WHEN** creating an issue or a comment returns an HTTP error such as 401, 403, 404, 410 or 422
- **THEN** the reporter logs a warning naming the test and the status, and goes on to the next failed test

#### Scenario: Network unavailable
- **WHEN** a request for the first of several failed tests fails with a connection error or times out
- **THEN** the reporter logs one warning, sends no request for the remaining failed tests, and the run completes
  normally

#### Scenario: Lookup fails
- **WHEN** listing open issues returns an HTTP error status for the first failed test, and succeeds for the second
- **THEN** no issue or comment is created for the first test, a warning is logged, and the second test is reported
  normally

#### Scenario: Output file cannot be written
- **WHEN** `github-requests.json` cannot be written in a dry run
- **THEN** the reporter logs a warning and the run's results are unaffected
