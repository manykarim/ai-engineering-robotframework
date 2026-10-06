import json
import logging
import urllib.error
from dataclasses import dataclass
from io import StringIO
from pathlib import Path

import pytest
import robot
from conftest import ISSUES_URL, LOOKUP_URL, FakeResponse, created_comment, http_error, issue
from robot.api import ExecutionResult

from robotframework_github_reporter import GitHubIssues
from robotframework_github_reporter.github import GitHub

LISTENER = "robotframework_github_reporter.GitHubIssues"

FAILING_SUITE = """\
*** Test Cases ***
Login Works
    Fail    Expected 200 but got 500

Logout Works
    Fail    Session still open\\n```not closed

Passes
    No Operation

Is Skipped
    Skip    Not today
"""

PASSING_SUITE = """\
*** Test Cases ***
Passes
    No Operation

Is Skipped
    Skip    Not today
"""

STATUSES = {
    "Login Works": ("FAIL", "Expected 200 but got 500"),
    "Logout Works": ("FAIL", "Session still open\n```not closed"),
    "Passes": ("PASS", ""),
    "Is Skipped": ("SKIP", "Not today"),
}

LOGIN = "Failing test: Demo.Login Works"
LOGOUT = "Failing test: Demo.Logout Works"
FALLBACK = "github-reporter: no GITHUB_TOKEN or GH_TOKEN; falling back to a dry run"


@dataclass
class Run:
    rc: int
    stdout: str
    stderr: str
    output_dir: Path

    @property
    def statuses(self) -> dict[str, tuple[str, str]]:
        result = ExecutionResult(str(self.output_dir / "output.xml"))
        return {test.name: (test.status, test.message) for test in result.suite.all_tests}

    @property
    def warnings(self) -> list[str]:
        return [line.removeprefix("[ WARN ] ") for line in self.stderr.splitlines() if line.startswith("[ WARN ]")]

    @property
    def requests_file(self) -> Path:
        return self.output_dir / "github-requests.json"

    @property
    def requests(self) -> list[dict]:
        return json.loads(self.requests_file.read_text(encoding="utf-8"))

    def assert_unchanged(self, statuses: dict[str, tuple[str, str]] = STATUSES, rc: int = 2) -> None:
        """No test was failed, skipped or changed by the reporter, and Robot reported no error."""
        assert self.statuses == statuses
        assert self.rc == rc
        assert "[ ERROR ]" not in self.stderr
        assert "into use failed" not in self.stderr


@pytest.fixture(autouse=True)
def environment(monkeypatch, tmp_path):
    for name in ("GITHUB_TOKEN", "GH_TOKEN", "GITHUB_ACTIONS"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.chdir(tmp_path)


@pytest.fixture
def run(tmp_path, capfd):
    def run(listener, suite: str = FAILING_SUITE) -> Run:
        source = tmp_path / "demo.robot"
        source.write_text(suite, encoding="utf-8")
        output_dir = tmp_path / "results" / "run1"
        stdout, stderr = StringIO(), StringIO()
        capfd.readouterr()
        rc = robot.run(
            str(source),
            listener=listener,
            exitonerror=True,
            outputdir=str(output_dir),
            log="NONE",
            report="NONE",
            stdout=stdout,
            stderr=stderr,
        )
        # `logger.console` writes to `sys.__stdout__`, which only file descriptor capture sees.
        console = capfd.readouterr()
        return Run(rc, stdout.getvalue() + console.out, stderr.getvalue() + console.err, output_dir)

    return run


def warnings(caplog) -> list[str]:
    return [record.getMessage() for record in caplog.records if record.levelno == logging.WARNING]


def create(title: str, body: str, label: str = "robot-failure") -> dict:
    return {"method": "POST", "url": ISSUES_URL, "body": {"title": title, "body": body, "labels": [label]}}


def body(message: str, line: int, fence: str = "```") -> str:
    return f"**Failure message**\n\n{fence}text\n{message}\n{fence}\n\n**Source:** `demo.robot:{line}`\n"


# Arguments


def test_defaults(caplog):
    listener = GitHubIssues(repo="octo-org/demo")
    assert listener.client.dry_run
    assert listener.client.repo == "octo-org/demo"
    assert listener.client.label == "robot-failure"
    assert warnings(caplog) == []


def test_arguments_given_by_name(caplog, monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "env-t0ken")
    listener = GitHubIssues(repo="octo-org/demo", dry_run=False, label="flaky")
    assert not listener.client.dry_run
    assert listener.client.repo == "octo-org/demo"
    assert listener.client.label == "flaky"
    assert warnings(caplog) == []


@pytest.mark.parametrize(
    "variables, expected",
    [
        ({"GITHUB_TOKEN": "github-t0ken", "GH_TOKEN": "gh-t0ken"}, "github-t0ken"),
        ({"GH_TOKEN": "gh-t0ken"}, "gh-t0ken"),
        ({"GITHUB_TOKEN": "", "GH_TOKEN": "gh-t0ken"}, "gh-t0ken"),
    ],
)
def test_token_variables(run, urlopen, monkeypatch, variables, expected):
    for name, value in variables.items():
        monkeypatch.setenv(name, value)
    urlopen.reply(FakeResponse([]), FakeResponse(issue(1, LOGIN)), FakeResponse(issue(2, LOGOUT)))
    result = run(f"{LISTENER}:repo=o/r:dry_run=false")
    result.assert_unchanged()
    assert result.warnings == []
    assert [call.headers["authorization"] for call in urlopen.calls] == [f"Bearer {expected}"] * 3
    assert not result.requests_file.exists()


def test_live_run_prints_outcomes(run, urlopen, monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "env-t0ken")
    urlopen.reply(FakeResponse([issue(7, LOGIN)]), FakeResponse(created_comment(7)), FakeResponse(issue(8, LOGOUT)))
    result = run(f"{LISTENER}:repo=o/r:dry_run=false")
    result.assert_unchanged()
    assert f"github-reporter: commented on https://github.com/o/r/issues/7#issuecomment-1 ({LOGIN})" in result.stdout
    assert f"github-reporter: opened https://github.com/o/r/issues/8 ({LOGOUT})" in result.stdout
    assert "env-t0ken" not in result.stdout + result.stderr


def test_fallback_warning(caplog):
    listener = GitHubIssues(repo="o/r", dry_run=False)
    assert listener.client.dry_run
    assert warnings(caplog) == [FALLBACK]


@pytest.mark.parametrize(
    "arguments, warning",
    [
        ({}, "repo is missing"),
        ({"repo": "octo-org"}, "repo must be owner/name, not 'octo-org'"),
        ({"repo": "a/b/c"}, "repo must be owner/name, not 'a/b/c'"),
        ({"repo": "/demo"}, "repo must be owner/name, not '/demo'"),
        ({"repo": "octo-org/"}, "repo must be owner/name, not 'octo-org/'"),
        ({"repo": "octo org/demo"}, "repo must be owner/name, not 'octo org/demo'"),
        ({"repo": "o/r", "label": ""}, "label must be non-empty and contain no comma, not ''"),
        ({"repo": "o/r", "label": "a,b"}, "label must be non-empty and contain no comma, not 'a,b'"),
    ],
)
def test_misconfiguration_disables_the_listener(caplog, arguments, warning):
    listener = GitHubIssues(**arguments)
    assert listener.client is None
    [message] = warnings(caplog)
    assert message.startswith("github-reporter: ")
    assert warning in message


def test_unknown_argument_warns_by_name(caplog):
    listener = GitHubIssues(repo="o/r", labels="secret-value")
    assert listener.client.label == "robot-failure"
    assert warnings(caplog) == ["github-reporter: ignoring unknown arguments: labels"]


def test_extra_positional_argument_warns_with_count(caplog):
    listener = GitHubIssues("o/r", True, "flaky", "secret-value")
    assert listener.client.label == "flaky"
    assert warnings(caplog) == ["github-reporter: ignoring 1 extra positional argument"]


def test_unrecognized_dry_run_value_stays_a_dry_run(caplog, monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "env-t0ken")
    listener = GitHubIssues(repo="o/r", dry_run="maybe")
    assert listener.client.dry_run
    assert warnings(caplog) == ["github-reporter: dry_run must be true or false, not 'maybe', so this is a dry run"]


def test_token_argument_is_ignored(caplog, monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "env-t0ken")
    listener = GitHubIssues(repo="o/r", dry_run=False, token="s3cret")
    assert not listener.client.dry_run
    assert warnings(caplog) == [
        "github-reporter: tokens are read from GITHUB_TOKEN or GH_TOKEN only, so the token argument is ignored"
    ]
    for text in warnings(caplog) + [repr(listener), repr(listener.client)]:
        assert "s3cret" not in text
        assert "env-t0ken" not in text


# Hooks


def test_only_failed_tests_are_reported(run, no_network):
    result = run(GitHubIssues(repo="o/r"))
    result.assert_unchanged()
    titles = [request["body"]["title"] for request in result.requests if request["method"] == "POST"]
    assert titles == [LOGIN, LOGOUT]


def test_statuses_unchanged_when_lookup_fails(run, urlopen, monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "env-t0ken")
    urlopen.reply(http_error(502, "Bad Gateway", LOOKUP_URL), http_error(502, "Bad Gateway", LOOKUP_URL))
    result = run(GitHubIssues(repo="o/r", dry_run=False))
    result.assert_unchanged()
    assert result.warnings == [
        f"github-reporter: could not report 'Demo.Login Works': GET {LOOKUP_URL}: HTTP 502 Bad Gateway",
        f"github-reporter: could not report 'Demo.Logout Works': GET {LOOKUP_URL}: HTTP 502 Bad Gateway",
    ]


def test_network_unavailable_sends_nothing_more(run, urlopen, monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "env-t0ken")
    urlopen.reply(urllib.error.URLError("Connection refused"))
    result = run(GitHubIssues(repo="o/r", dry_run=False))
    result.assert_unchanged()
    [warning] = result.warnings
    assert warning.startswith(f"github-reporter: could not report 'Demo.Login Works': GET {LOOKUP_URL}: ")
    assert warning.endswith("GitHub cannot be reached, so no more requests are sent in this run")
    assert len(urlopen.calls) == 1


def test_unexpected_exception_becomes_warning(run, no_network, monkeypatch):
    def report(self, title, body, comment=None):
        raise RuntimeError("boom")

    monkeypatch.setattr(GitHub, "report", report)
    result = run(GitHubIssues(repo="o/r"))
    result.assert_unchanged()
    assert result.warnings == [
        "github-reporter: could not report 'Demo.Login Works': RuntimeError: boom",
        "github-reporter: could not report 'Demo.Logout Works': RuntimeError: boom",
    ]


@pytest.mark.parametrize(
    "arguments, warning",
    [
        ("", "github-reporter: repo is missing"),
        (":repo=o/r:labels=x", "github-reporter: ignoring unknown arguments: labels"),
        (":repo=o/r:dry_run=maybe", "github-reporter: dry_run must be true or false, not 'maybe'"),
        (":repo=o/r:token=s3cret", "github-reporter: tokens are read from GITHUB_TOKEN or GH_TOKEN only"),
        (":o/r:true:robot-failure:extra", "github-reporter: ignoring 1 extra positional argument"),
    ],
)
def test_misconfigured_string_listener_loads(run, no_network, arguments, warning):
    result = run(LISTENER + arguments)
    result.assert_unchanged()
    [message] = result.warnings
    assert message.startswith(warning)
    assert "s3cret" not in result.stdout + result.stderr + "".join(
        path.read_text(encoding="utf-8") for path in result.output_dir.iterdir()
    )


# Dry-run output


def test_dry_run_of_a_failing_suite(run, no_network):
    result = run(f"{LISTENER}:repo=octo-org/demo")
    result.assert_unchanged()
    url = "https://api.github.com/repos/octo-org/demo/issues"
    assert result.requests == [
        {"method": "GET", "url": f"{url}?state=open&labels=robot-failure&per_page=100"},
        {**create(LOGIN, body("Expected 200 but got 500", 2)), "url": url},
        {**create(LOGOUT, body("Session still open\n```not closed", 5, fence="````")), "url": url},
    ]
    assert result.requests_file.read_text(encoding="utf-8").endswith("]\n")
    assert f"github-reporter (dry run): GET {url}?state=open&labels=robot-failure&per_page=100\n" in result.stdout
    assert result.stdout.count(f"github-reporter (dry run): POST {url}\n") == 2
    assert json.dumps(result.requests[1]["body"], indent=2) in result.stdout


def test_dry_run_with_no_failures_writes_empty_array(run, no_network):
    result = run(f"{LISTENER}:repo=o/r", suite=PASSING_SUITE)
    result.assert_unchanged({"Passes": ("PASS", ""), "Is Skipped": ("SKIP", "Not today")}, rc=0)
    assert result.requests_file.read_text(encoding="utf-8") == "[]\n"
    assert "github-reporter (dry run)" not in result.stdout


def test_token_during_dry_run_is_not_printed_or_written(run, no_network, monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "env-t0ken")
    result = run(f"{LISTENER}:repo=o/r")
    result.assert_unchanged()
    assert len(result.requests) == 3
    assert "env-t0ken" not in result.stdout + result.stderr + result.requests_file.read_text(encoding="utf-8")


def test_unwritable_output_file_becomes_warning(run, no_network, tmp_path):
    (tmp_path / "results" / "run1" / "github-requests.json").mkdir(parents=True)
    result = run(f"{LISTENER}:repo=o/r")
    result.assert_unchanged()
    [warning] = result.warnings
    assert warning.startswith(f"github-reporter: could not write {result.requests_file}: ")


def test_disabled_listener_writes_no_file(run, no_network):
    result = run(f"{LISTENER}:repo=octo-org")
    result.assert_unchanged()
    assert not result.requests_file.exists()


# Required unit coverage (design §8)


def test_opens_new_issue(run, urlopen, monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "env-t0ken")
    urlopen.reply(FakeResponse([]), FakeResponse(issue(8, LOGIN)), FakeResponse(issue(9, LOGOUT)))
    result = run(f"{LISTENER}:repo=o/r:dry_run=false")
    result.assert_unchanged()
    assert urlopen.requests == [("GET", LOOKUP_URL), ("POST", ISSUES_URL), ("POST", ISSUES_URL)]
    assert urlopen.calls[1].body == {
        "title": LOGIN,
        "body": body("Expected 200 but got 500", 2),
        "labels": ["robot-failure"],
    }
    assert result.warnings == []


def test_comments_on_open_issue(run, urlopen, monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "env-t0ken")
    urlopen.reply(
        FakeResponse([issue(7, LOGIN), issue(9, LOGOUT)]),
        FakeResponse(created_comment(7)),
        FakeResponse(created_comment(9, comment_id=2)),
    )
    result = run(f"{LISTENER}:repo=o/r:dry_run=false")
    result.assert_unchanged()
    assert urlopen.requests == [
        ("GET", LOOKUP_URL),
        ("POST", f"{ISSUES_URL}/7/comments"),
        ("POST", f"{ISSUES_URL}/9/comments"),
    ]
    assert urlopen.calls[1].body == {"body": "Failed again.\n\n" + body("Expected 200 but got 500", 2)}
    assert ("POST", ISSUES_URL) not in urlopen.requests
    assert result.warnings == []


def test_dry_run_sends_nothing(run, no_network):
    result = run(f"{LISTENER}:repo=o/r")
    result.assert_unchanged()
    assert [(request["method"], request["url"]) for request in result.requests] == [
        ("GET", LOOKUP_URL),
        ("POST", ISSUES_URL),
        ("POST", ISSUES_URL),
    ]
    assert result.warnings == []


def test_missing_token_falls_back_to_dry_run(run, no_network):
    result = run(f"{LISTENER}:repo=o/r:dry_run=false")
    result.assert_unchanged()
    assert result.warnings == [FALLBACK]
    assert len(result.requests) == 3


def test_api_error_becomes_warning(run, urlopen, monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "env-t0ken")
    cases = [
        ([http_error(502, "Bad Gateway", LOOKUP_URL), FakeResponse([])], f"GET {LOOKUP_URL}: HTTP 502 Bad Gateway"),
        ([FakeResponse([]), http_error(422, "Unprocessable Entity")], f"POST {ISSUES_URL}: HTTP 422 Unprocessable Entity"),
        ([FakeResponse([issue(7, LOGIN)]), http_error(403, "Forbidden")], f"POST {ISSUES_URL}/7/comments: HTTP 403 Forbidden"),
    ]
    for replies, error in cases:
        urlopen.calls.clear()
        urlopen.reply(*replies, FakeResponse(issue(9, LOGOUT)))
        result = run(f"{LISTENER}:repo=o/r:dry_run=false")
        result.assert_unchanged()
        assert result.warnings == [f"github-reporter: could not report 'Demo.Login Works': {error}"]
        # The next failure is still reported.
        assert urlopen.requests[-1] == ("POST", ISSUES_URL)
        assert urlopen.calls[-1].body["title"] == LOGOUT
        assert urlopen.replies == []
