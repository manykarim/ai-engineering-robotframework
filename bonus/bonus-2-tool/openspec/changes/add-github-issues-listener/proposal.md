# Proposal

## Why

When a Robot Framework test fails in CI, its failure only lives in that run's `log.html`, so a broken test is easy
to miss and hard to track over time. Filing one GitHub issue per failing test, then commenting on it when the test
fails again, turns failures into tracked work without anyone copying them over by hand. The package is still the
`uv init` placeholder (`hello()`), so this is its first real feature.

## What Changes

- A version 3 listener, `robotframework_github_reporter.GitHubIssues`, registered with
  `--listener robotframework_github_reporter.GitHubIssues:repo=owner/name[:dry_run=false][:label=...]`.
  - `repo`: the target repository, `owner/name`. Without it the listener does nothing.
  - `dry_run`: `true` by default. Only an explicit false value makes a run live.
  - `label`: `robot-failure` by default.
  - Leaving out `repo`, misspelling an argument, or passing an unknown argument or value gives a warning. The listener
    still loads, so even `--exitonerror` cannot turn a configuration mistake into failed tests.
- For every failed test, it opens an issue in `repo` titled `Failing test: <the test's full name>`, with the label.
  The body holds the failure message, the test's source and line, and the run's URL when it runs in GitHub Actions.
- If an open issue with that exact title and the label already exists, it adds a comment to that issue instead.
- In a dry run, the default, it sends nothing. It prints each request it would send to the console and writes them
  all to `github-requests.json` in the output directory.
- Live, it reads the token from `GITHUB_TOKEN`, then `GH_TOKEN`, and never from an argument. With no token, it warns
  and falls back to a dry run.
- It never fails, skips or changes a test. Any error of its own, such as a bad `repo`, an HTTP error, a timeout or a
  file it cannot write, becomes a warning and never an error.
- It sends HTTP through `urllib.request` only. Robot Framework stays the only run-time dependency, and the package
  imports from its source folder alone (`--pythonpath src`).
- Unit tests under `tests/` (pytest) replace `urllib.request.urlopen`. They cover:
  - a new issue
  - a comment on an open issue
  - a dry run
  - a missing token
  - API errors
- Robot tests under `atest/` run a failing suite with the listener in a dry run and check what it recorded. They run it
  in an isolated environment that holds only Robot Framework, which shows that the listener works from `src/` without
  being installed.
- The `hello()` placeholder is removed, and the README and the `pyproject.toml` description document the listener.

## Capabilities

### New Capabilities

- `github-issue-reporting`: turning a run's failed tests into GitHub issues, or comments on matching open issues.
  Covers the listener's arguments, issue content, deduplication, dry-run output, token handling and the
  never-fail guarantee.

### Modified Capabilities

None. `openspec/specs/` has no capabilities yet.

## Impact

- **Code**: new modules under `src/robotframework_github_reporter/`, and the package `__init__.py` exports
  `GitHubIssues` in place of `hello()`.
- **Tests**: a new `tests/` folder (pytest) and a new `atest/` folder (Robot Framework). The failing suite lives in a
  folder whose name starts with `_`, so `uv run robot --outputdir results atest` does not collect it. The Robot tests
  call `uv run --isolated`, which needs uv and either its cache or the network.
- **External system**: live runs call the GitHub REST API (`api.github.com`). They list a repository's issues, create
  issues and create issue comments, as described in `references/github-issues.json`. The token needs permission to
  write issues in `repo`.
- **Dependencies**: none added. Robot Framework 7.5 stays the only run-time dependency, and pytest stays a dev
  dependency.
- **Files**: dry runs write `github-requests.json` to the output directory, and `results/` (from the Robot tests)
  should be git-ignored.
