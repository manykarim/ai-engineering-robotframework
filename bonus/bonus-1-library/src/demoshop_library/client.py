"""HTTP client for the DemoShop REST API."""

import uuid
from typing import Any

import requests

TIMEOUT = 10


class DemoShopError(Exception):
    """A request the shop rejected, could not answer, or answered in an unexpected form."""

    ROBOT_SUPPRESS_NAME = True


class ShopClient:
    """Sends the requests of one library instance to the shop at ``url``.

    The client owns the base URL, the headers, the timeout and the translation of errors into ``DemoShopError``.
    ``session_id`` identifies the instance's cart. ``session`` is the underlying ``requests.Session``; the unit tests
    mount a fake transport on it.
    """

    def __init__(self, url: str, space: str | None = None):
        self.url = url.rstrip("/")
        self.session_id = uuid.uuid4().hex
        self.session = requests.Session()
        if space is not None:
            self.session.headers["X-Workshop-Space"] = space

    def request(
        self,
        method: str,
        path: str,
        action: str,
        json: Any = None,
        with_session: bool = False,
    ) -> Any:
        """Sends a request to ``path`` and returns the decoded JSON body.

        ``action`` describes the request in error messages, for example ``Getting product 1``. With
        ``with_session``, the request carries the cart's ``X-Session-ID`` header.
        """
        headers = {"X-Session-ID": self.session_id} if with_session else None
        try:
            response = self.session.request(method, self.url + path, json=json, headers=headers, timeout=TIMEOUT)
        except requests.RequestException as error:
            raise DemoShopError(f"{action} failed: could not reach the shop at {self.url}: {error}") from error
        if response.status_code >= 400:
            raise DemoShopError(f"{action} failed: {_error_detail(response)} (HTTP {response.status_code})")
        try:
            return response.json(object_hook=lambda obj: _ShopObject(action, obj))
        except ValueError:
            raise DemoShopError(f"{action} failed: unexpected response from the shop") from None


class _ShopObject(dict):
    """A JSON object from the shop. Looking up a key it lacks fails like any other unexpected response."""

    def __init__(self, action: str, obj: dict):
        super().__init__(obj)
        self.action = action

    def __missing__(self, key):
        raise DemoShopError(f"{self.action} failed: unexpected response from the shop")


def _error_detail(response: requests.Response) -> str:
    """Returns the shop's ``detail``, joining validation errors, or the response text if there is none."""
    try:
        detail = response.json()["detail"]
        if isinstance(detail, str):
            return detail
        return "; ".join(f"{error['loc'][-1]}: {error['msg']}" for error in detail)
    except (ValueError, LookupError, TypeError):
        return response.text
