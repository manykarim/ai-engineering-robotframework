"""Where the shop is and which workshop space to use (spec: workshop/shop-access).

Two settings select everything: ``SHOP_URL`` and ``SHOP_SPACE``. They are read
from the process environment or from the git-ignored ``.env`` in the repository
root, and the process environment wins. Every tool in this repository - the run
profiles, the ``shop`` helper and ``setup-check`` - resolves them here, so they
can never disagree.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping
from urllib.parse import urlsplit

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parent.parent
DOTENV = ROOT / ".env"

LOCAL_URL = "http://localhost:9090"
SHARED_URL = "https://demoshop.makrocode.de"
PROFILES = ("local", "shared")

#: The shop's own rule for a space: the GitHub username format, compared in
#: lowercase (demo-webshop spec ``workshop-spaces``).
SPACE_PATTERN = re.compile(r"^[a-z0-9](?:[a-z0-9]|-(?=[a-z0-9])){0,38}$")

#: The header that carries the space. It takes precedence over ``?space=`` and
#: the space cookie in the shop, and covers pages, assets and API calls alike.
SPACE_HEADER = "X-Workshop-Space"

SPACE_FORMAT = "1 to 39 letters, digits or single hyphens, not starting or ending with a hyphen"

#: Sent by the repository's own HTTP clients. The CDN in front of the shared
#: instance answers 403 to Python's default ``Python-urllib`` agent (measured);
#: requests, httpx, curl and browsers are let through, so tests are unaffected.
USER_AGENT = "ai-engineering-robotframework"


@dataclass(frozen=True)
class ShopSettings:
    url: str
    #: Lowercase, or "" when no space is set.
    space: str
    profile: str
    #: Why these settings cannot be used, or None.
    problem: str | None

    @property
    def shared(self) -> bool:
        """Whether this is (or must be treated as) the shared instance."""
        return self.profile == "shared" or not is_loopback(self.url)

    def headers(self) -> dict[str, str]:
        """The headers every request to the shop carries."""
        return {SPACE_HEADER: self.space} if self.space else {}


def is_loopback(url: str) -> bool:
    host = (urlsplit(url).hostname or "").lower()
    return host in {"localhost", "::1"} or host.startswith("127.")


def _setting(name: str, environ: Mapping[str, str], dotenv: Mapping[str, str | None]) -> str:
    value = environ.get(name)
    if value is None:
        value = dotenv.get(name)
    return (value or "").strip()


def load(profile: str | None = None, environ: Mapping[str, str] | None = None, dotenv_path: Path | None = None) -> ShopSettings:
    """Resolve the shop settings: process environment, then ``.env``, then the profile's default.

    Only ``SHOP_URL`` and ``SHOP_SPACE`` are read from ``.env``. The file may
    hold API keys, and loading all of it into the environment would expose them
    to every test run.
    """
    environ = os.environ if environ is None else environ
    path = DOTENV if dotenv_path is None else dotenv_path
    dotenv = dotenv_values(path) if path.is_file() else {}

    profile = (profile or environ.get("SHOP_PROFILE") or "local").strip().lower()
    url = (_setting("SHOP_URL", environ, dotenv) or (SHARED_URL if profile == "shared" else LOCAL_URL)).rstrip("/")
    raw_space = _setting("SHOP_SPACE", environ, dotenv)
    space = raw_space.lower()

    problem = None
    needs_space = profile == "shared" or not is_loopback(url)
    if profile not in PROFILES:
        problem = f"Unknown profile {profile!r}; use one of: {', '.join(PROFILES)}."
    elif space and not SPACE_PATTERN.fullmatch(space):
        problem = f"SHOP_SPACE {raw_space!r} is not a valid workshop space. A space is your GitHub handle: {SPACE_FORMAT}."
    elif needs_space and not space:
        problem = (f"SHOP_SPACE is not set, but {url} is the shared workshop instance, where everyone works in their own space. "
                   "Set SHOP_SPACE to your GitHub handle in .env (see SETUP.md, 'The shared instance').")
    elif needs_space and space == "default":
        problem = "SHOP_SPACE is 'default', the baseline everyone shares. Set it to your GitHub handle instead."
    return ShopSettings(url=url, space=space, profile=profile, problem=problem)
