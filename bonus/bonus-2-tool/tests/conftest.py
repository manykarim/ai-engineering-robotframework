"""A fake `urllib.request.urlopen` that answers from a queue of replies and records every request."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from email.message import Message
from typing import Any

import pytest

ISSUES_URL = "https://api.github.com/repos/o/r/issues"
LOOKUP_URL = f"{ISSUES_URL}?state=open&labels=robot-failure&per_page=100"


class FakeResponse:
    def __init__(self, data: Any, link: str | None = None, status: int = 200, raw: bytes | None = None):
        self._payload = json.dumps(data).encode("utf-8") if raw is None else raw
        self.headers = Message()
        if link:
            self.headers["Link"] = link
        self.status = status

    def read(self) -> bytes:
        return self._payload

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *exc_info: object) -> None:
        pass


@dataclass
class Call:
    method: str
    url: str
    headers: dict[str, str]
    body: Any
    timeout: float | None


class FakeUrlopen:
    def __init__(self) -> None:
        self.replies: list[FakeResponse | BaseException] = []
        self.calls: list[Call] = []

    def reply(self, *replies: FakeResponse | BaseException) -> FakeUrlopen:
        self.replies.extend(replies)
        return self

    def __call__(self, request: urllib.request.Request, timeout: float | None = None) -> FakeResponse:
        self.calls.append(
            Call(
                request.get_method(),
                request.full_url,
                {name.lower(): value for name, value in request.header_items()},
                json.loads(request.data) if request.data else None,
                timeout,
            )
        )
        if not self.replies:
            pytest.fail(f"unexpected request: {request.get_method()} {request.full_url}")
        reply = self.replies.pop(0)
        if isinstance(reply, BaseException):
            raise reply
        return reply

    @property
    def requests(self) -> list[tuple[str, str]]:
        return [(call.method, call.url) for call in self.calls]


def issue(number: int, title: str, **fields: Any) -> dict[str, Any]:
    return {
        "number": number,
        "title": title,
        "state": "open",
        "html_url": f"https://github.com/o/r/issues/{number}",
        **fields,
    }


def created_comment(number: int, comment_id: int = 1) -> dict[str, Any]:
    return {"id": comment_id, "html_url": f"https://github.com/o/r/issues/{number}#issuecomment-{comment_id}"}


def http_error(code: int, reason: str, url: str = ISSUES_URL) -> urllib.error.HTTPError:
    return urllib.error.HTTPError(url, code, reason, Message(), None)


@pytest.fixture
def urlopen(monkeypatch: pytest.MonkeyPatch) -> FakeUrlopen:
    fake = FakeUrlopen()
    monkeypatch.setattr(urllib.request, "urlopen", fake)
    return fake


@pytest.fixture
def no_network(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail(request: urllib.request.Request, *args: object, **kwargs: object) -> None:
        pytest.fail(f"urlopen was called: {request.get_method()} {request.full_url}")

    monkeypatch.setattr(urllib.request, "urlopen", fail)
