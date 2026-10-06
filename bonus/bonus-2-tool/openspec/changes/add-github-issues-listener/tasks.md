# Tasks

## 1. Project setup

- [x] 1.1 Add `[tool.pytest.ini_options]` to `pyproject.toml` with `testpaths = ["tests"]` and `pythonpath = ["src"]`,
  and replace the placeholder `description`. Verify that `uv run pytest` starts and collects from `tests/`.
- [x] 1.2 Add `results/` to `.gitignore`. Verify that `git check-ignore results/output.xml` matches.

## 2. Issue content (`content.py`)

- [x] 2.1 Implement `title(full_name)` and `run_url(environ=os.environ)` (design §5). Verify with
  `tests/test_content.py`:
  - the title format
  - a URL only when `GITHUB_ACTIONS == "true"` and the three variables are set
  - `None` when any one of them is missing
- [x] 2.2 Implement the source formatting (relative to `cwd` when under it, `/` separators, `unknown` for no source,
  no `:line` without a line), plus `body(...)` and `comment(...)` with the growing backtick fence. Verify with
  `tests/test_content.py`:
  - a multi-line message containing ```` ``` ```` stays verbatim inside one fence
  - the run line appears only when there is a URL
  - the comment starts with `Failed again.`

## 3. GitHub client (`github.py`)

- [x] 3.1 Implement `Request`, `GitHubError(message, unreachable)`, and `GitHub._send`, which records in a dry run and
  sends through `urllib.request.urlopen(..., timeout=10)` live, setting the headers from design §4. Verify with
  `tests/test_github.py`, using a fake `urlopen` installed through `monkeypatch`:
  - live requests carry `Authorization: Bearer <token>`, the API version, the `User-Agent` and a 10 s timeout
  - `HTTPError` maps to `unreachable=False`, and `URLError` or a timeout to `unreachable=True`
  - a dry run never calls `urlopen`
- [x] 3.2 Implement the lookup: `state=open&labels=<label>&per_page=100`, following `Link` `rel="next"`, skipping
  pull requests, the newest issue winning per title, and loaded once and kept after success only. Verify with
  `tests/test_github.py`:
  - a match on page 2 is found
  - pull requests and other titles are ignored
  - three reports cause one lookup
  - a lookup HTTP error raises for that report, and the next report retries
- [x] 3.3 Implement `report(title, body)`: comment on a cached match, otherwise create the issue with `labels=[label]`
  and cache its `number`. Also record each outcome's `html_url` for the summary, and go offline after an unreachable
  error. Verify with `tests/test_github.py`:
  - a match is commented on
  - a non-match creates an issue
  - two reports with the same title in one run create one issue and comment on it
  - `HTTPError` 422 on create and 403 on comment raise `GitHubError` naming the status, and the next report still
    sends
  - after `URLError` no further `urlopen` call happens
  - a dry run records `GET` once, then one `POST /issues` per report

## 4. Listener (`listener.py`, `__init__.py`)

- [x] 4.1 Implement
  `GitHubIssues.__init__(repo: str = "", dry_run: bool = True, label: str = "robot-failure", *extra, **unknown)`
  (design §6):
  - a missing or malformed `repo`, or an empty label or one containing a comma, warns and disables the listener
  - unknown named arguments warn by name only; `token` gets its own warning and its value is dropped
  - extra positional arguments warn with their count
  - live only when `dry_run is False`, so a non-bool value warns and stays a dry run
  - resolve the token, `GITHUB_TOKEN` then `GH_TOKEN`, an empty value counting as unset
  - when live without a token, fall back to a dry run with one warning
  - catch every exception, and never call `logger.error`

  Export it from `__init__.py` in place of `hello()`. Verify with `tests/test_listener.py`, using `caplog` and
  `monkeypatch.setenv`/`delenv`:
  - the defaults
  - `GITHUB_TOKEN` taking precedence
  - `GH_TOKEN` used alone
  - the fallback warning
  - one warning for each of: missing `repo`, malformed `repo`, invalid label, `labels=x`, a fourth positional
    argument, `dry_run=maybe`, and `token=s3cret`
  - neither the environment token nor `s3cret` appearing in any warning or in `repr`
- [x] 4.2 Implement the hooks:
  - `start_suite` captures `${OUTPUT DIR}` for the top-level suite
  - `end_test` reports failed tests only and turns `GitHubError` into a warning naming the test and status
  - every hook body is wrapped in `try/except` and turns errors into `logger.warn`

  Verify with in-process `robot.run(..., exitonerror=True)` tests in `tests/test_listener.py`, each on a suite with
  failing, passing and skipped tests:
  - only FAIL tests reach the client, not PASS or SKIP ones
  - statuses, messages and the return code are unchanged in a dry run, and live when `urlopen` raises `HTTPError` or
    `URLError`
  - a client that raises `RuntimeError` produces a warning, and no test changes status
  - the listener given as a string, as `...GitHubIssues` with no arguments, `...:repo=o/r:labels=x` or
    `...:repo=o/r:dry_run=maybe`, loads without `Taking listener ... into use failed`, and the passing test stays PASS
- [x] 4.3 Implement the top-level `end_suite`:
  - **Dry run**: print each request with `logger.console` (method, URL, indented JSON body) and write
    `github-requests.json` to the output directory, which is `[]` when nothing failed.
  - **Live run**: print one line per issue opened or commented on.
  - A write error becomes a warning.

  Verify with `tests/test_listener.py`:
  - the file's content and order match the spec's *Dry run of a failing suite* scenario
  - `[]` when nothing fails
  - a token set during a dry run appears neither on stdout nor in the file
  - an unwritable output directory produces a warning and leaves the run's results unchanged
- [x] 4.4 Add the five required end-to-end unit tests from design §8 (*Required unit coverage*) to
  `tests/test_listener.py`. Each runs `robot.run(..., exitonerror=True)` on a suite with two failing tests, one passing
  test and one skipped test, with `urllib.request.urlopen` replaced:
  - `test_opens_new_issue`
  - `test_comments_on_open_issue`
  - `test_dry_run_sends_nothing`
  - `test_missing_token_falls_back_to_dry_run`
  - `test_api_error_becomes_warning`

  Verify that
  `uv run pytest tests/test_listener.py -k "test_opens_new_issue or test_comments_on_open_issue or test_dry_run_sends_nothing or test_missing_token_falls_back_to_dry_run or test_api_error_becomes_warning"`
  selects exactly five tests and all pass.

## 5. Robot acceptance tests (`atest/`)

- [x] 5.1 Add `atest/_data/failing.robot` with two failing tests, one passing and one skipped, each failure with a
  distinct message, one of them multi-line. Verify that `uv run robot --dryrun --outputdir results atest` does not
  list it.
- [x] 5.2 Add `atest/github_issues.robot`. A keyword runs the failing suite through `Run Process` in an isolated
  environment holding only Robot Framework:
  `uv run --isolated --no-project --with robotframework==7.5 python -m robot --pythonpath <repo>/src --listener robotframework_github_reporter.GitHubIssues:repo=octo-org/demo`,
  with a temporary `--outputdir` and `env:GITHUB_TOKEN=`, `env:GH_TOKEN=` and `env:GITHUB_ACTIONS=`. Verify that
  `uv run robot --outputdir results atest` passes, with tests asserting:
  - return code 2
  - no `Taking listener ... into use failed` on stderr
  - stdout shows one `GET` and two `POST` requests
  - `github-requests.json` holds the expected titles, label, messages and `failing.robot:<line>`
- [x] 5.3 Add a test with `GITHUB_ACTIONS=true`, `GITHUB_SERVER_URL`, `GITHUB_REPOSITORY` and `GITHUB_RUN_ID` set,
  asserting the run URL in each recorded body. Add another with `dry_run=false` and no token, asserting the fallback
  warning on stderr and that `github-requests.json` is written. Verify that `uv run robot --outputdir results atest`
  passes.
- [x] 5.4 Add a templated test that runs the failing suite with `--exitonerror` and each misconfiguration: no
  arguments, `labels=x`, `token=s3cret` and `dry_run=maybe`. Verify that `uv run robot --outputdir results atest`
  passes, asserting for each case:
  - return code 2
  - the passing test still `PASS` in the inner `output.xml`
  - a `github-reporter:` warning on stderr
  - `s3cret` absent from stdout, stderr and every file in the inner output directory

## 6. Documentation and final checks

- [x] 6.1 Write `README.md`, covering:
  - registering the listener with `--listener` and `--pythonpath src`
  - its arguments and defaults, and that argument mistakes become warnings
  - the dry run and `github-requests.json`
  - the token variables, and a GitHub Actions snippet with `permissions: issues: write` and
    `env: GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}`
  - the known limits from design *Risks*: labels dropped without access, rate limits, and that a dry run shows
    creations only

  Verify that every command in the README runs as written.
- [x] 6.2 Run the full checks, which must all pass:
  - `uv run pytest`
  - `uv run robot --outputdir results atest`
  - `uv build`
  - `openspec validate add-github-issues-listener --strict`

  Also confirm that:
  - `pyproject.toml` still lists only `robotframework==7.5` under `dependencies`
  - a search of `src/` finds no `importlib.metadata`, `pkg_resources`, `requests`, `from urllib.request import
    urlopen` or `logger.error`
