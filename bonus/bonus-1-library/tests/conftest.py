"""Shared test seam: a fake shop that replaces only the network transport.

The library's client builds and sends real ``requests`` requests: URL joining, default headers and JSON body
encoding all run as in production. ``FakeShop`` is mounted on the client's ``requests.Session`` in place of the HTTP
adapter, records every ``PreparedRequest`` and answers with canned responses.
"""

import copy
import json
from types import SimpleNamespace
from urllib.parse import urlsplit

import pytest
import requests
from robot.libraries.BuiltIn import BuiltIn
from robot.variables import Variables

from demoshop_library import DemoShopLibrary

SHOP_URL = "http://shop.test"


def json_response(status: int, body) -> requests.Response:
    """Returns a canned response whose body is ``body`` encoded as JSON."""
    return text_response(status, json.dumps(body), "application/json")


def text_response(status: int, text: str, content_type: str = "text/plain") -> requests.Response:
    """Returns a canned response whose body is ``text`` as is."""
    response = requests.Response()
    response.status_code = status
    response.headers["Content-Type"] = content_type
    response.encoding = "utf-8"
    response._content = text.encode("utf-8")
    return response


class FakeShop(requests.adapters.BaseAdapter):
    """A transport adapter that answers requests from canned responses registered by ``(method, path)``."""

    def __init__(self):
        super().__init__()
        self.requests: list[requests.PreparedRequest] = []
        self.responses: dict[tuple[str, str], requests.Response] = {}

    def add(self, method: str, path: str, response: requests.Response) -> None:
        self.responses[(method, path)] = response

    def send(self, request, **kwargs):
        self.requests.append(request)
        key = (request.method, urlsplit(request.url).path)
        if key not in self.responses:
            raise AssertionError(f"FakeShop has no response for {key[0]} {key[1]}")
        response = copy.copy(self.responses[key])
        response.request = request
        response.url = request.url
        return response

    def close(self):
        pass


@pytest.fixture
def fake_shop() -> FakeShop:
    return FakeShop()


@pytest.fixture
def library(fake_shop):
    """Returns a factory that builds a ``DemoShopLibrary`` for ``SHOP_URL`` talking to ``fake_shop``."""

    def make(space: str | None = None) -> DemoShopLibrary:
        lib = DemoShopLibrary(SHOP_URL, space=space)
        lib.client.session.mount("http://", fake_shop)
        return lib

    return make


@pytest.fixture
def robot_variables(monkeypatch):
    """Lets ``validate`` and ``then`` run outside Robot Framework.

    AssertionEngine evaluates expressions with ``BuiltIn().evaluate``, which needs the variables of a running
    execution. An empty variable store is enough for expressions that use only ``value``.
    """
    monkeypatch.setattr(BuiltIn, "_variables", property(lambda self: SimpleNamespace(current=Variables())))
