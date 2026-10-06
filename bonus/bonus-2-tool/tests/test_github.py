import urllib.error

import pytest
from conftest import ISSUES_URL, LOOKUP_URL, FakeResponse, created_comment, http_error, issue

from robotframework_github_reporter.github import GitHub, GitHubError, Request

TITLE = "Failing test: Demo.Login Works"
BODY = "**Failure message**\n..."
COMMENT = "Failed again.\n\n" + BODY


def live() -> GitHub:
    return GitHub("o/r", "robot-failure", "t0ken")


# Requests


def test_live_request_headers_and_timeout(urlopen):
    urlopen.reply(FakeResponse([]), FakeResponse(issue(8, TITLE)))
    live().report(TITLE, BODY)
    lookup, create = urlopen.calls
    for call in lookup, create:
        assert call.headers["authorization"] == "Bearer t0ken"
        assert call.headers["accept"] == "application/vnd.github+json"
        assert call.headers["x-github-api-version"] == "2022-11-28"
        assert call.headers["user-agent"] == "robotframework-github-reporter"
        assert call.timeout == 10
    assert "content-type" not in lookup.headers
    assert create.headers["content-type"] == "application/json"


def test_repository_is_quoted_in_the_url(urlopen):
    urlopen.reply(FakeResponse([]), FakeResponse(issue(1, TITLE)))
    GitHub("octo org/dé mo", "robot-failure", "t0ken").report(TITLE, BODY)
    assert urlopen.calls[1].url == "https://api.github.com/repos/octo%20org/d%C3%A9%20mo/issues"


def test_http_error_is_not_unreachable(urlopen):
    urlopen.reply(http_error(404, "Not Found", LOOKUP_URL))
    with pytest.raises(GitHubError) as error:
        live().report(TITLE, BODY)
    assert str(error.value) == f"GET {LOOKUP_URL}: HTTP 404 Not Found"
    assert error.value.unreachable is False


@pytest.mark.parametrize(
    "failure",
    [urllib.error.URLError("Name or service not known"), TimeoutError("timed out"), ConnectionResetError()],
)
def test_network_error_is_unreachable(urlopen, failure):
    urlopen.reply(failure)
    with pytest.raises(GitHubError) as error:
        live().report(TITLE, BODY)
    assert error.value.unreachable is True
    assert str(error.value).startswith(f"GET {LOOKUP_URL}: ")


def test_invalid_json_is_not_unreachable(urlopen):
    urlopen.reply(FakeResponse(None, raw=b"<html>"))
    with pytest.raises(GitHubError, match="not valid JSON") as error:
        live().report(TITLE, BODY)
    assert error.value.unreachable is False


def test_unexpected_lookup_response_is_an_error(urlopen):
    urlopen.reply(FakeResponse({"message": "nope"}))
    with pytest.raises(GitHubError, match="not a list of issues"):
        live().report(TITLE, BODY)


# Lookup


def test_lookup_query(urlopen):
    urlopen.reply(FakeResponse([]), FakeResponse(issue(1, "Failing test: X")))
    GitHub("o/r", "flaky", "t0ken").report("Failing test: X", BODY)
    assert urlopen.calls[0].method == "GET"
    assert urlopen.calls[0].url == f"{ISSUES_URL}?state=open&labels=flaky&per_page=100"


def test_match_on_second_page(urlopen):
    page_2 = f"{ISSUES_URL}?state=open&labels=robot-failure&per_page=100&page=2"
    urlopen.reply(
        FakeResponse([issue(3, "Failing test: Other")], link=f'<{page_2}>; rel="next", <{page_2}>; rel="last"'),
        FakeResponse([issue(7, TITLE)], link=f'<{LOOKUP_URL}&page=1>; rel="prev", <{LOOKUP_URL}&page=1>; rel="first"'),
        FakeResponse(created_comment(7)),
    )
    live().report(TITLE, BODY, COMMENT)
    assert urlopen.requests == [("GET", LOOKUP_URL), ("GET", page_2), ("POST", f"{ISSUES_URL}/7/comments")]


def test_pull_requests_closed_issues_and_other_titles_are_ignored(urlopen):
    urlopen.reply(
        FakeResponse(
            [
                issue(9, TITLE, pull_request={"url": "https://api.github.com/repos/o/r/pulls/9"}),
                issue(8, TITLE, state="closed"),
                issue(6, TITLE + " Again"),
                issue(5, TITLE.lower()),
            ]
        ),
        FakeResponse(issue(10, TITLE)),
    )
    live().report(TITLE, BODY)
    assert urlopen.requests[-1] == ("POST", ISSUES_URL)


def test_newest_issue_wins(urlopen):
    urlopen.reply(FakeResponse([issue(12, TITLE), issue(7, TITLE)]), FakeResponse(created_comment(12)))
    live().report(TITLE, BODY)
    assert urlopen.requests[-1] == ("POST", f"{ISSUES_URL}/12/comments")


def test_one_lookup_for_several_reports(urlopen):
    urlopen.reply(FakeResponse([]), *(FakeResponse(issue(number, f"Failing test: T{number}")) for number in (1, 2, 3)))
    client = live()
    for number in (1, 2, 3):
        client.report(f"Failing test: T{number}", BODY)
    assert urlopen.requests == [("GET", LOOKUP_URL)] + [("POST", ISSUES_URL)] * 3


def test_lookup_error_raises_and_next_report_retries(urlopen):
    urlopen.reply(http_error(502, "Bad Gateway", LOOKUP_URL), FakeResponse([]), FakeResponse(issue(1, TITLE)))
    client = live()
    with pytest.raises(GitHubError, match="HTTP 502"):
        client.report("Failing test: First", BODY)
    client.report(TITLE, BODY)
    assert urlopen.requests == [("GET", LOOKUP_URL), ("GET", LOOKUP_URL), ("POST", ISSUES_URL)]


# Reports


def test_new_issue(urlopen):
    urlopen.reply(FakeResponse([]), FakeResponse(issue(8, TITLE)))
    client = live()
    client.report(TITLE, BODY, COMMENT)
    assert urlopen.requests == [("GET", LOOKUP_URL), ("POST", ISSUES_URL)]
    assert urlopen.calls[1].body == {"title": TITLE, "body": BODY, "labels": ["robot-failure"]}
    assert [(o.action, o.url) for o in client.outcomes] == [("opened", "https://github.com/o/r/issues/8")]


def test_comment_on_open_issue(urlopen):
    urlopen.reply(FakeResponse([issue(7, TITLE)]), FakeResponse(created_comment(7)))
    client = live()
    client.report(TITLE, BODY, COMMENT)
    assert urlopen.requests == [("GET", LOOKUP_URL), ("POST", f"{ISSUES_URL}/7/comments")]
    assert urlopen.calls[1].body == {"body": COMMENT}
    assert [(o.action, o.url) for o in client.outcomes] == [
        ("commented on", "https://github.com/o/r/issues/7#issuecomment-1")
    ]


def test_same_title_twice_creates_then_comments(urlopen):
    urlopen.reply(FakeResponse([]), FakeResponse(issue(8, TITLE)), FakeResponse(created_comment(8)))
    client = live()
    client.report(TITLE, BODY, COMMENT)
    client.report(TITLE, BODY, COMMENT)
    assert urlopen.requests == [("GET", LOOKUP_URL), ("POST", ISSUES_URL), ("POST", f"{ISSUES_URL}/8/comments")]


def test_api_errors_raise_and_next_report_still_sends(urlopen):
    urlopen.reply(
        http_error(502, "Bad Gateway", LOOKUP_URL),
        FakeResponse([issue(7, "Failing test: Commented")]),
        http_error(422, "Unprocessable Entity"),
        http_error(403, "Forbidden", f"{ISSUES_URL}/7/comments"),
        FakeResponse(issue(8, TITLE)),
    )
    client = live()
    with pytest.raises(GitHubError, match="HTTP 502 Bad Gateway"):
        client.report("Failing test: Looked up", BODY)
    with pytest.raises(GitHubError, match=f"POST {ISSUES_URL}: HTTP 422 Unprocessable Entity"):
        client.report("Failing test: Created", BODY)
    with pytest.raises(GitHubError, match=f"POST {ISSUES_URL}/7/comments: HTTP 403 Forbidden"):
        client.report("Failing test: Commented", BODY)
    client.report(TITLE, BODY)
    assert urlopen.requests[-1] == ("POST", ISSUES_URL)
    assert not client.offline


def test_goes_offline_after_unreachable_error(urlopen):
    urlopen.reply(FakeResponse([]), urllib.error.URLError("Connection refused"))
    client = live()
    with pytest.raises(GitHubError):
        client.report("Failing test: First", BODY)
    client.report("Failing test: Second", BODY)
    client.report("Failing test: Third", BODY)
    assert client.offline
    assert len(urlopen.calls) == 2


def test_dry_run_records_lookup_once_then_one_create_per_report(no_network):
    client = GitHub("o/r", "robot-failure")
    client.report("Failing test: A", "a")
    client.report("Failing test: B", "b")
    client.report("Failing test: A", "a")
    assert client.dry_run
    assert client.requests == [
        Request("GET", LOOKUP_URL),
        Request("POST", ISSUES_URL, {"title": "Failing test: A", "body": "a", "labels": ["robot-failure"]}),
        Request("POST", ISSUES_URL, {"title": "Failing test: B", "body": "b", "labels": ["robot-failure"]}),
        Request("POST", ISSUES_URL, {"title": "Failing test: A", "body": "a", "labels": ["robot-failure"]}),
    ]
    assert client.outcomes == []


def test_missing_token_is_a_dry_run(no_network):
    client = GitHub("o/r", "robot-failure", "")
    client.report(TITLE, BODY)
    assert client.dry_run
    assert [request.method for request in client.requests] == ["GET", "POST"]


def test_request_to_json():
    assert Request("GET", LOOKUP_URL).to_json() == {"method": "GET", "url": LOOKUP_URL}
    assert Request("POST", ISSUES_URL, {"body": "x"}).to_json() == {
        "method": "POST",
        "url": ISSUES_URL,
        "body": {"body": "x"},
    }


def test_token_is_not_in_repr():
    assert "t0ken" not in repr(live())
