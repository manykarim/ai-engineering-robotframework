"""The GitHub REST client: looks up open issues, creates issues and comments, or records the requests in a dry run."""

from __future__ import annotations

import http.client
import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote, urlencode

API_URL = "https://api.github.com"
API_VERSION = "2022-11-28"
USER_AGENT = "robotframework-github-reporter"
TIMEOUT = 10


class GitHubError(Exception):
    """A failed request. `unreachable` means GitHub could not be reached at all."""

    def __init__(self, message: str, unreachable: bool = False):
        super().__init__(message)
        self.unreachable = unreachable


@dataclass(frozen=True)
class Request:
    method: str
    url: str
    body: dict[str, Any] | None = None

    def to_json(self) -> dict[str, Any]:
        item: dict[str, Any] = {"method": self.method, "url": self.url}
        if self.body is not None:
            item["body"] = self.body
        return item


@dataclass(frozen=True)
class Outcome:
    action: str  # "opened" or "commented on"
    title: str
    url: str


class GitHub:
    """Reports failures to one repository. Without a token it is a dry run and only records its requests."""

    def __init__(self, repo: str, label: str, token: str | None = None):
        owner, name = repo.split("/")
        self.repo = repo
        self.label = label
        self._token = token or None
        self._issues_url = f"{API_URL}/repos/{quote(owner, safe='')}/{quote(name, safe='')}/issues"
        self._open: dict[str, int] | None = None
        self.requests: list[Request] = []
        self.outcomes: list[Outcome] = []
        self.offline = False

    @property
    def dry_run(self) -> bool:
        return self._token is None

    def report(self, title: str, body: str, comment: str | None = None) -> None:
        """Comments on the open issue titled `title`, or opens it. `comment` defaults to `body`."""
        if self.offline:
            return
        try:
            if self._open is None:
                self._open = self._open_issues()
            number = self._open.get(title)
            if number is not None:
                action, url = "commented on", f"{self._issues_url}/{number}/comments"
                data, _ = self._send("POST", url, {"body": body if comment is None else comment})
            else:
                action, url = "opened", self._issues_url
                data, _ = self._send("POST", url, {"title": title, "body": body, "labels": [self.label]})
        except GitHubError as error:
            if error.unreachable:
                self.offline = True
            raise
        if data is None:  # A dry run.
            return
        if not isinstance(data, dict):
            raise GitHubError(f"POST {url}: the response is not a JSON object")
        if number is None:
            if not isinstance(data.get("number"), int):
                raise GitHubError(f"POST {url}: the response has no issue number")
            self._open[title] = data["number"]
        self.outcomes.append(Outcome(action, title, str(data.get("html_url", ""))))

    def _open_issues(self) -> dict[str, int]:
        """Maps the titles of the open labelled issues to their numbers, the newest issue winning."""
        issues: dict[str, int] = {}
        url: str | None = self._issues_url + "?" + urlencode(
            {"state": "open", "labels": self.label, "per_page": 100}
        )
        while url:
            data, link = self._send("GET", url)
            if data is None:
                break
            if not isinstance(data, list):
                raise GitHubError(f"GET {url}: the response is not a list of issues")
            for item in data:
                if not isinstance(item, dict) or "pull_request" in item or item.get("state", "open") != "open":
                    continue
                title, number = item.get("title"), item.get("number")
                if isinstance(title, str) and isinstance(number, int):
                    issues.setdefault(title, number)
            url = _next_url(link)
        return issues

    def _send(self, method: str, url: str, body: dict[str, Any] | None = None) -> tuple[Any, str | None]:
        """Returns the parsed JSON response and the `Link` header. A dry run records the request and returns `None`."""
        if self._token is None:
            self.requests.append(Request(method, url, body))
            return None, None
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self._token}",
            "X-GitHub-Api-Version": API_VERSION,
            "User-Agent": USER_AGENT,
        }
        data = None
        if body is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(body).encode("utf-8")
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                payload = response.read()
                link = response.headers.get("Link")
        except urllib.error.HTTPError as error:
            error.close()
            raise GitHubError(f"{method} {url}: HTTP {error.code} {error.reason}") from None
        except OSError as error:
            # URLError, TimeoutError and connection errors: GitHub cannot be reached.
            reason = getattr(error, "reason", None) or error
            raise GitHubError(f"{method} {url}: {reason}", unreachable=True) from None
        except http.client.HTTPException as error:
            raise GitHubError(f"{method} {url}: malformed response ({type(error).__name__})") from None
        try:
            return json.loads(payload), link
        except ValueError:
            raise GitHubError(f"{method} {url}: the response is not valid JSON") from None


def _next_url(link: str | None) -> str | None:
    """The `rel="next"` URL of a `Link` header."""
    for match in re.finditer(r"<([^>]*)>([^,]*)", link or ""):
        if re.search(r'\brel="?next"?', match.group(2)):
            return match.group(1)
    return None
