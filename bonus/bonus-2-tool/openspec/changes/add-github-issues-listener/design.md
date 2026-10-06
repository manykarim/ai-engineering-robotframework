# Design

## Context

See `proposal.md` for the motivation, and `specs/github-issue-reporting/spec.md` for the behavior. This section only
covers what shapes the approach.

- **The package** is the `uv init` placeholder. It is a `src/` layout built with `uv_build`, with a `py.typed`, and
  `__init__.py` holds only `hello()`. The `.venv` has Robot Framework 7.5 and pytest 9.1.
- **Robot Framework 7.5**, checked against the installed code and a throwaway run:
  - Listener arguments go through type conversion based on the `__init__` type hints (`robot/utils/importer.py`), so
    `dry_run=false` becomes `False` when it is annotated `bool`.
  - `robot.api.logger.warn` from a listener's `__init__` or the top-level `end_suite` reaches the console and
    `output.xml`'s errors. From `close()` it reaches the console only, because the output is already written.
  - `BuiltIn().get_variable_value("${OUTPUT DIR}")` works in `start_suite`.
  - `logger.console` called in `end_test` prints between the test's name and its `| FAIL |`, which garbles the
    console.
  - When Robot runs a directory, it skips files and folders whose names start with `_` or `.`
    (`robot/parsing/suitestructure.py`).
  - Robot catches exceptions that escape a listener method, but reports them as errors, not warnings.
  - With `--exitonerror`, any error fails every test, including passing ones. That covers a listener that fails to
    load. A probe confirmed it: with a required `repo` that was left out, a passing test reported `FAIL`. A misspelled
    named argument such as `labels=x` fails the import the same way. Warnings do not trigger `--exitonerror`.
  - A `bool` argument that Robot cannot convert, such as `dry_run=maybe`, arrives as the string `'maybe'` rather than
    failing.
  - A signature with defaults plus `*extra` and `**unknown` loads with no arguments, with misspelled names and with
    extra positional arguments (probed).
  - `data.source`, `data.lineno`, `result.full_name`, `result.message` and `result.failed` hold everything a report
    needs.
- **Environments**:
  - `uv sync` installs the project in editable mode into `.venv`, with `robotframework_github_reporter.pth` and its
    dist-info. A run that uses `.venv` therefore cannot show that the listener works without being installed.
  - `uv run --isolated --no-project --with robotframework==7.5 python` gives a temporary environment holding Robot
    Framework 7.5 and nothing else. In it the package cannot be imported and has no metadata (probed).
- **GitHub REST API** (`references/github-issues.json`):
  - `GET /repos/{owner}/{repo}/issues` takes `state`, `labels` (comma-separated), `per_page` (at most 100) and `page`,
    and paginates through the `Link` header. It returns pull requests too, which carry a `pull_request` key.
  - `POST /repos/{owner}/{repo}/issues` takes `title`, `body` and `labels`, and answers `201` or one of
    `400/403/404/410/422/503`. Labels are silently dropped when the token lacks push access.
  - `POST /repos/{owner}/{repo}/issues/{issue_number}/comments` takes `body`, and answers `201` or one of
    `403/404/410/422`.
  - Both `POST` endpoints are subject to secondary rate limits.
- **Project constraints**:
  - `urllib.request` is the only HTTP client.
  - The listener imports from its source folder alone and reads no package metadata.
  - The token comes from the environment only.
  - Every error becomes a warning.

## Goals / Non-Goals

**Goals:**
- Keep the Robot glue thin, and keep the GitHub logic and the issue text in plain modules that are easy to unit test.
- Give a dry run and a live run one code path, so the dry run shows what a live run would do.
- Make `urllib.request.urlopen` the only network seam, so unit tests replace just that.

**Non-Goals:**
- Closing or relabelling issues when a test passes again.
- GitHub Enterprise Server (`GITHUB_API_URL`): the API base is fixed to `https://api.github.com`.
- Retrying or backing off on rate limits, and creating or checking the label up front.
- Reporting suite setup or teardown failures separately. Robot marks the suite's tests failed, and those tests are
  reported.
- Deduplicating across processes, as with pabot: each process looks up issues on its own.
- Reading a previous `github-requests.json`. Each dry run overwrites it.

## Decisions

### 1. Modules: listener, content and GitHub client

```
src/robotframework_github_reporter/
  __init__.py   # from .listener import GitHubIssues; __all__ = ["GitHubIssues"]
  listener.py   # GitHubIssues: Robot hooks, argument validation, token, output dir, warnings
  content.py    # title, body, comment, run URL, relative source path: pure functions
  github.py     # GitHubError, Request, GitHub: lookup / create / comment, record or send
```

- Every import is relative and nothing reads `importlib.metadata`, so `--pythonpath src` is enough.
- `GitHubIssues` is a plain class with `ROBOT_LISTENER_API_VERSION = 3`, like `references/example-listener.py`.
  Subclassing `robot.api.interfaces.ListenerV3` would only add base-class no-op hooks.
- *Alternative*: a single module. Rejected because content and HTTP tests would then have to go through Robot
  objects.

### 2. A dry run and a live run share one flow; only `_send` differs

`GitHub(repo, label, token | None)` has one public method, `report(title, body)`, and a `requests` list.
- `report` checks the open-issue cache (loading it first if needed). It then either comments on the matching issue or
  creates one.
- Every request goes through `_send(method, url, body)`:
  - **Dry run** (`token is None`): it appends `Request(method, url, body)` to `requests` and returns `None`, with no
    data and no `Link` header. The lookup therefore records one `GET` (first page only), finds nothing, and every
    failure is recorded as a `POST` to create an issue, exactly as the spec says.
  - **Live**: it calls `urllib.request.urlopen` and returns the parsed JSON and the `Link` header.
- An issue created live is added to the cache with its `number`, so a second failure with the same full name comments
  on it. In a dry run there is no number, so nothing is cached.
- *Alternative*: separate dry and live reporter classes. Rejected because two flows could drift, and then the dry run
  would stop showing what live does.

### 3. Lookup: list open labelled issues once per run, then match titles in memory

- On the first `report`, the client fetches
  `GET /repos/{owner}/{repo}/issues?state=open&labels=<label>&per_page=100` and follows `rel="next"` links from
  `Link`.
- It builds `dict[title, number]`, skipping items with `pull_request`. The first item for a title wins: the default
  `sort=created, direction=desc` makes that the newest.
- The title match is exact, and the server's `labels` filter guarantees the label.
- If the lookup fails, the cache stays unloaded, so the next failed test tries again (spec: *Lookup fails*).
- *Alternatives*:
  - The search API (`/search/issues?q=...`). It is absent from the reference, limited to 30 requests per minute, and
    matches titles fuzzily.
  - One listing per failed test. It is simpler but costs N times the requests.

### 4. HTTP through `urllib.request`, with a single seam

- `github.py` does `import urllib.request` and calls `urllib.request.urlopen(request, timeout=10)` through the module
  attribute. Unit tests then patch `urllib.request.urlopen` with `monkeypatch`; a `from urllib.request import urlopen`
  would escape the patch.
- Request headers:
  - `Accept: application/vnd.github+json`
  - `Authorization: Bearer <token>`
  - `X-GitHub-Api-Version: 2022-11-28`
  - `User-Agent: robotframework-github-reporter`, without a version, since metadata is off limits
  - `Content-Type: application/json` when there is a body
- The JSON body is UTF-8. The owner and name are `quote`d as path segments, and the query string comes from
  `urlencode`.
- Failures are normalised into `GitHubError(message, unreachable: bool)`:
  - `HTTPError` gives `"<METHOD> <url>: HTTP <code> <reason>"`, with `unreachable=False`.
  - `URLError`, `TimeoutError` and other `OSError`s set `unreachable=True`.
  - A response that is not valid JSON sets `unreachable=False`.
- After an unreachable error, `GitHub` flags itself as offline, and later `report` calls do nothing (spec: *Network
  unavailable*). Ten seconds bounds one request. Without this rule, an unreachable network would add ten seconds to
  every failed test.
- *Alternatives*: `http.client`, which means more code and the same dependency footprint, and `requests`, which is a
  run-time dependency the project rules out.

### 5. Issue content (`content.py`)

- `title(full_name)` gives `f"Failing test: {full_name}"`.
- `body(message, source, lineno, run_url)` gives Markdown:

  ````markdown
  **Failure message**

  ```text
  <message, verbatim>
  ```

  **Source:** `atest/demo.robot:12`
  **Run:** https://github.com/octo-org/app/actions/runs/42
  ````

  - The fence is backticks, one longer than the longest run of backticks in the message, and at least three. A message
    containing ```` ``` ```` therefore cannot close it.
  - The `**Run:**` line appears only with a run URL.
  - `source` is made relative to `Path.cwd()` when it lies under it, written with `/` separators, and left as-is
    otherwise. A missing source gives `unknown`, and a missing line drops `:<line>`.
- `comment(...)` gives `"Failed again.\n\n" + body(...)`.
- `run_url(environ)` returns `{GITHUB_SERVER_URL}/{GITHUB_REPOSITORY}/actions/runs/{GITHUB_RUN_ID}` only when
  `GITHUB_ACTIONS == "true"` and all three variables are non-empty, and `None` otherwise. `GITHUB_REPOSITORY` is the
  workflow's repository, which may differ from `repo`.
- Every function takes its inputs (`environ`, `cwd`) as parameters with defaults, so tests need no patching.

### 6. Listener lifecycle (`listener.py`)

- The signature is
  `__init__(self, repo: str = "", dry_run: bool = True, label: str = "robot-failure", *extra: str, **unknown: str)`.
  - Every parameter has a default and the two catch-alls absorb anything else, so Robot's argument resolution can
    never fail the import. Under `--exitonerror`, a failed import would fail every test (see Context).
  - `repo` has a default only for that reason. The listener still treats it as required.
- The body handles each argument in turn:
  - **Repository**: `repo` must contain exactly one `/`, have non-empty parts and contain no whitespace. A missing or
    malformed `repo` gives one warning and disables the listener.
  - **Label**: an empty label, or one containing a comma, does the same. A comma would break the `labels` filter of
    the lookup and cause duplicates.
  - **Unknown and extra arguments**:
    - `**unknown` gives one warning naming the argument names only, never their values, and is otherwise ignored.
    - A `token` among them gets its own warning: tokens come from `GITHUB_TOKEN` or `GH_TOKEN`. Its value is
      dropped at once and never stored.
    - `*extra` gives one warning with its count.
  - **Mode**: only `dry_run is False` means a live run. Any other non-bool value, such as `'maybe'`, gives a warning
    and keeps the dry run.
  - **Token**: in a live run it reads `os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")`, so an empty
    value counts as unset. With no token it warns once (`github-reporter: no GITHUB_TOKEN or GH_TOKEN; falling back
    to a dry run`) and switches to a dry run.
  - **Client**: it builds `GitHub(repo, label, token)`. The token lives only on that object and is never put in a
    message or `repr`.
  - **Exceptions**: the body catches every exception, so a bug becomes a warning, not a "taking listener into use
    failed" error.
- `start_suite(data, result)` captures `${OUTPUT DIR}` when `data.parent is None`.
- `end_test(data, result)` acts only if `result.failed`. It builds the title and body from `result.full_name`,
  `result.message`, `data.source`, `data.lineno` and `run_url()`, then calls `report`. A `GitHubError` becomes
  `logger.warn(f"github-reporter: could not report '{full_name}': {error}")`.
- `end_suite(data, result)` acts only when `data.parent is None`:
  - **Dry run**: it prints each recorded request with `logger.console` and writes `github-requests.json` to the output
    directory.
  - **Live run**: it prints one line per issue opened or commented on, with the `html_url` from the response.
  - Doing this here rather than in `close()` keeps console output off the test status lines and keeps warnings in
    `log.html`.
- Every hook body is wrapped in `try/except Exception` that turns into `logger.warn`.
- The listener never assigns to `result.status` or `result.message`.
- It never calls `logger.error`. An error, unlike a warning, would let `--exitonerror` fail tests.
- Warnings are prefixed `github-reporter:`.

### 7. Dry-run output

- **Console**: each request prints as `github-reporter (dry run): <METHOD> <url>`, followed by
  `json.dumps(body, indent=2, ensure_ascii=False)` when it has a body.
- **File**: `json.dumps([...], indent=2, ensure_ascii=False)` plus a newline, written in UTF-8. Each item is
  `{"method", "url"}`, with `"body"` added only when the request has one. The `url` includes the query string.
- **Headers**: they are never recorded, so neither the console nor the file can expose a token.
- **Output directory**: if it was never captured, for example because the hooks were called outside a run, the
  current directory is used.

### 8. Tests

- **`tests/` (pytest).** `[tool.pytest.ini_options] testpaths = ["tests"]` and `pythonpath = ["src"]` make pytest
  import the source folder.
  - **`test_content.py`**: title, body, fence growth, the run URL with and without Actions variables, and relative or
    absolute source.
  - **`test_github.py`**: `monkeypatch.setattr(urllib.request, "urlopen", fake)`. The fake returns a context-manager
    response (`read()`, `headers`, `status`) or raises `HTTPError` or `URLError`, and records every `Request` it
    sees, including headers and the timeout. It covers:
    - creating an issue
    - commenting on a match
    - skipping closed issues, pull requests and mismatched titles
    - following the `Link: rel="next"` page
    - looking up once for several failures
    - caching an issue created earlier in the run
    - a lookup HTTP error followed by a retry
    - going offline on `URLError`
    - the `Authorization` header
    - a dry run that never calls `urlopen`
  - **`test_listener.py`**: runs small suites in-process with
    `robot.run(..., listener=..., exitonerror=True, outputdir=tmp_path, stdout=StringIO(), stderr=StringIO())`.
    - The suite always includes a passing test and a skipped test. With `exitonerror=True`, any error the listener
      caused would flip them to `FAIL`, so every listener test also checks that no test was failed or skipped by the
      reporter.
    - `urlopen` is patched (to `pytest.fail` for dry runs), and the token variables are set with `monkeypatch.setenv`
      or `delenv`.
    - The listener is passed either as an instance, or as the string `"robotframework_github_reporter.GitHubIssues:..."`
      so that Robot's own argument resolution is exercised.
    - It checks:
      - the defaults
      - `dry_run=false` with each token variable
      - a missing or malformed `repo`, an invalid label, unknown or extra arguments, `token=...` and `dry_run=maybe`
      - that statuses, messages and the return code are unchanged
      - `github-requests.json` content, and `[]` when nothing fails
      - a file write error turning into a warning
      - an unexpected exception from the client turning into a warning

    A warning from `__init__` in an instance built inside the test, before `robot.run` starts, goes to Python
    `logging` and is asserted with `caplog`. This was checked against Robot Framework 7.5. Warnings logged during the
    run, which includes string-form listeners, are asserted from the captured stderr
    (`[ WARN ] github-reporter: ...`).
- **Required unit coverage.** Each of these five cases has a client-level test in `test_github.py` and an
  end-to-end listener test in `test_listener.py`. Both replace `urllib.request.urlopen`.

  | Case | Fake `urlopen` | Asserts |
  |---|---|---|
  | New issue | lookup returns `[]` | one `POST /repos/o/r/issues` with `title`, `body` and `labels`, and no comment |
  | Comment on an open issue | lookup returns open issue #7 with the same title | one `POST /repos/o/r/issues/7/comments`, and no `POST /issues` |
  | Dry run | fails the test if called | `urlopen` never called, and the file holds the `GET` plus one `POST` per failure |
  | Missing token | fails the test if called | `dry_run=false` with both variables unset: one fallback warning, `urlopen` never called, file written |
  | API error | `HTTPError` 422 on create, 403 on comment, 502 on lookup | a warning naming the test and the status, statuses and return code unchanged, and the next failure still reported |

- **`atest/` (Robot Framework).** `atest/github_issues.robot` runs `atest/_data/failing.robot`, which has two failing
  tests, one passing and one skipped, through `Run Process`.
  - **Environment**: every inner run uses the isolated environment from Context, so each acceptance test also shows
    that the listener needs nothing but Robot Framework and `src/`, and is not installed. The command is
    `uv run --isolated --no-project --with robotframework==7.5 python -m robot --pythonpath <repo>/src --listener robotframework_github_reporter.GitHubIssues:repo=octo-org/demo --outputdir <temp> <suite>`,
    with `env:GITHUB_TOKEN=`, `env:GH_TOKEN=` and `env:GITHUB_ACTIONS=` so that the developer's or CI's environment
    cannot leak in.
  - **Checks**:
    - return code 2
    - no `Taking listener ... into use failed` on stderr
    - the requests on stdout
    - `github-requests.json` content
    - with the `GITHUB_*` Actions variables set, the run URL in each body
    - with `dry_run=false` and no token, the fallback warning on stderr and the file written
    - under `--exitonerror`, with no arguments, `labels=x`, `token=s3cret` or `dry_run=maybe`: return code 2, the
      passing test still `PASS`, a warning on stderr, and `s3cret` absent from stdout, stderr and every output file

  The `_` prefix keeps the failing suite out of `uv run robot --outputdir results atest`.

## Risks / Trade-offs

- **[Labels silently dropped]** A token without the needed access opens issues without the label, which the next
  lookup cannot see, so duplicates follow. → The README states that the token needs issue write access and label
  rights. In Actions that means `permissions: issues: write`.
- **[Secondary rate limits]** Many failures in one run can trigger them, and the affected reports are lost as
  warnings. → There is one lookup per run and no retries. The README mentions the limit.
- **[Very long messages]** GitHub rejects bodies over its size limit with `422`, which turns into a warning. → This is
  accepted, because the spec asks for the message unchanged.
- **[Argument mistakes are only warnings]** A misspelled `dry_run` leaves a run in dry-run mode without failing
  anything, so it is easy to overlook. → The warning names the unknown argument, and the dry run is the safe side.
- **[Acceptance tests need uv's cache or the network]** The isolated environment is built from uv's cache, which
  `uv sync` fills with the same Robot Framework wheel. On a fresh machine without network access the acceptance tests
  cannot run. → This is accepted. Unit tests still run from `.venv`.
- **[Renamed tests or suites]** A new full name means a new title, so a new issue opens. → This is accepted, because
  titles are the identity the request defines.
- **[A dry run cannot see existing issues]** It always shows creations, never comments. → This is stated in the spec
  and the README, and the recorded `GET` shows that a live run looks up first.
- **[Run-wide offline switch]** A single timeout stops reporting for the rest of the run, even if the network
  recovers. → This is preferred over adding ten seconds to every failed test, and the warning says why.

## Migration Plan

Nothing to migrate. Removing the `--listener` option turns the feature off, and the default dry run means a new user
cannot open issues by accident.
