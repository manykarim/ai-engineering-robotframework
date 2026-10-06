# robotframework-github-reporter

A Robot Framework listener that opens a GitHub issue for each failing test, or comments on the test's open issue
when it fails again. Failures then become tracked work instead of lines in one run's `log.html`.

It is a dry run by default: it sends nothing and only shows the requests it would send.

## Usage

The listener needs Robot Framework 7.5 and nothing else, and does not need to be installed: put this project's
`src` folder on Robot's module search path with `--pythonpath`, and register the listener with `--listener`. From
this repository's root, this runs the demo suite, which has two failing tests, in a dry run:

```bash
uv run robot --pythonpath src --listener robotframework_github_reporter.GitHubIssues:repo=octo-org/demo --outputdir results atest/_data/failing.robot
```

Robot exits with code 2 because two tests fail, as it would without the listener. From another project, point
`--pythonpath` at this project's `src` folder instead.

### Arguments

Arguments follow the listener's name, each as `name=value` after a `:`, for example
`robotframework_github_reporter.GitHubIssues:repo=octo-org/demo:dry_run=false:label=flaky`.

| Argument  | Default         | Meaning                                                                                |
|-----------|-----------------|----------------------------------------------------------------------------------------|
| `repo`    | none            | The target repository, `owner/name`. Without a valid one, nothing is reported.         |
| `dry_run` | `true`          | Only a false value, such as `false`, `no`, `off` or `0`, makes the run live.           |
| `label`   | `robot-failure` | The label of the issues it opens and looks for: non-empty, and with no comma.          |

An argument mistake is a warning, never an error, and the listener still loads. Even `--exitonerror` therefore cannot
fail a test because of it:

- A missing or malformed `repo`, or an invalid `label`, turns the listener off for the run.
- An unknown argument, such as `labels=flaky`, or an extra positional argument is ignored. The warning names unknown
  arguments without their values.
- A `dry_run` value that is neither true nor false, such as `maybe`, keeps the dry run.

## What it reports

For every test that fails, and not for those that pass or are skipped, it opens an issue in `repo`:

- titled `Failing test: <the test's full name>`, for example `Failing test: Failing.Login Works`
- with the label
- with a body that holds the failure message verbatim, the test's source file and line (relative to the current
  directory when the file lies under it), and the run's URL when it runs in GitHub Actions

If an open issue with exactly that title and the label already exists, it comments on that issue instead, with the
same content after `Failed again.` It lists the repository's open labelled issues once per run, through every page,
and ignores pull requests and closed issues. An issue it opened earlier in the same run counts as open.

The listener never fails, skips or changes a test, and never changes Robot's exit code. Its own errors, such as an HTTP
error, a timeout or a file it cannot write, become warnings. A request times out after 10 seconds, and once GitHub
cannot be reached at all, no more requests are sent for the rest of the run.

## Dry run and `github-requests.json`

A dry run sends no request at all. When the run ends, it prints each request a live run would send to the console and
writes them, in order, to `github-requests.json` in the output directory. The file is written even when nothing
failed, as `[]`. The demo command above writes `results/github-requests.json`:

```json
[
  {
    "method": "GET",
    "url": "https://api.github.com/repos/octo-org/demo/issues?state=open&labels=robot-failure&per_page=100"
  },
  {
    "method": "POST",
    "url": "https://api.github.com/repos/octo-org/demo/issues",
    "body": {
      "title": "Failing test: Failing.Login Works",
      "body": "**Failure message**\n\n```text\nExpected 200 but got 500\n```\n\n**Source:** `atest/_data/failing.robot:7`\n",
      "labels": [
        "robot-failure"
      ]
    }
  },
  ...
]
```

Neither the console nor the file shows a token or any request header.

## Live runs and the token

With `dry_run=false`, the listener authenticates with the token in `GITHUB_TOKEN` or, when that is unset or empty,
in `GH_TOKEN`. It never takes a token from an argument or a file: a `token=...` argument is ignored with a warning, and
its value is never used or shown. With neither variable set, it warns and falls back to a dry run.

The token must be able to write issues in `repo`. In GitHub Actions, give the job `issues: write` and pass the
workflow's token. This step assumes a copy of this project in `robotframework-github-reporter/`, and your tests in
`tests/`:

```yaml
jobs:
  robot:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install robotframework==7.5
      - name: Run the Robot tests
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: >-
          robot --pythonpath robotframework-github-reporter/src
          --listener robotframework_github_reporter.GitHubIssues:repo=${{ github.repository }}:dry_run=false
          --outputdir results tests
```

GitHub Actions sets `GITHUB_ACTIONS`, `GITHUB_SERVER_URL`, `GITHUB_REPOSITORY` and `GITHUB_RUN_ID`, so each issue and
comment links to its run.

## Known limits

- **Labels need access.** GitHub silently drops the labels of a new issue when the token lacks the access to set
  them. The next run's lookup then cannot find that issue, and opens a duplicate.
- **Rate limits.** Creating issues and comments is subject to GitHub's secondary rate limits. Many failures in one run
  can reach them, and each report that GitHub rejects is lost, with a warning. Nothing is retried.
- **A dry run shows creations only.** It cannot see the existing issues, so it records every failure as a new issue,
  never as a comment. The recorded `GET` shows the lookup that a live run makes first.
- **Titles are the identity.** A renamed test or suite gets a new issue.
- **One API.** Requests go to `https://api.github.com`, so GitHub Enterprise Server is not supported.

## Development

```bash
uv sync
uv run pytest
uv run robot --outputdir results atest
uv build
```

The Robot tests run the demo suite in a temporary environment that holds only Robot Framework 7.5, which uv builds
from its cache or the network.
