"""The text of issues and comments: pure functions, with every input passed in."""

from __future__ import annotations

import os
import re
from collections.abc import Mapping
from pathlib import Path

TITLE_PREFIX = "Failing test: "


def title(full_name: str) -> str:
    return f"{TITLE_PREFIX}{full_name}"


def run_url(environ: Mapping[str, str] = os.environ) -> str | None:
    """The GitHub Actions run's URL, or `None` outside GitHub Actions."""
    if environ.get("GITHUB_ACTIONS") != "true":
        return None
    server = environ.get("GITHUB_SERVER_URL")
    repository = environ.get("GITHUB_REPOSITORY")
    run_id = environ.get("GITHUB_RUN_ID")
    if not (server and repository and run_id):
        return None
    return f"{server}/{repository}/actions/runs/{run_id}"


def location(source: str | os.PathLike[str] | None, lineno: int | None, cwd: Path | None = None) -> str:
    """`path:line`, with the path relative to `cwd` when the file lies under it."""
    if not source:
        path = "unknown"
    else:
        cwd = Path.cwd() if cwd is None else cwd
        try:
            path = Path(source).relative_to(cwd).as_posix()
        except ValueError:
            path = str(source)
    return f"{path}:{lineno}" if lineno else path


def body(
    message: str,
    source: str | os.PathLike[str] | None,
    lineno: int | None,
    run_url: str | None,
    cwd: Path | None = None,
) -> str:
    # A fence longer than any run of backticks in the message, so the message cannot close it.
    longest = max((len(run) for run in re.findall("`+", message)), default=0)
    fence = "`" * max(3, longest + 1)
    lines = [
        "**Failure message**",
        "",
        f"{fence}text",
        message,
        fence,
        "",
        f"**Source:** `{location(source, lineno, cwd)}`",
    ]
    if run_url:
        lines.append(f"**Run:** {run_url}")
    return "\n".join(lines) + "\n"


def comment(
    message: str,
    source: str | os.PathLike[str] | None,
    lineno: int | None,
    run_url: str | None,
    cwd: Path | None = None,
) -> str:
    return "Failed again.\n\n" + body(message, source, lineno, run_url, cwd)
