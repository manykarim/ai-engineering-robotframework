"""The Robot Framework listener: argument checks, the token, the output directory and warnings.

Every error of its own becomes a warning, never an error, so that even `--exitonerror` cannot fail a test because of
the reporter.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

from . import content
from .github import GitHub, GitHubError

REQUESTS_FILE = "github-requests.json"
REPO = re.compile(r"[^/\s]+/[^/\s]+")


def _warn(message: str) -> None:
    logger.warn(f"github-reporter: {message}")


class GitHubIssues:
    """Opens a GitHub issue for each failed test, or comments on its open issue.

    Use as `--listener robotframework_github_reporter.GitHubIssues:repo=owner/name[:dry_run=false][:label=...]`.
    """

    ROBOT_LISTENER_API_VERSION = 3

    # Every parameter has a default and the catch-alls absorb anything else, so that Robot can always import the
    # listener: a failed import is an error, which `--exitonerror` would turn into failed tests.
    def __init__(
        self,
        repo: str = "",
        dry_run: bool = True,
        label: str = "robot-failure",
        *extra: str,
        **unknown: str,
    ):
        self.client: GitHub | None = None
        self._output_dir: Path | None = None
        try:
            self.client = self._configure(repo, dry_run, label, extra, unknown)
        except Exception as error:
            _warn(f"could not start, so nothing is reported: {type(error).__name__}: {error}")

    @staticmethod
    def _configure(
        repo: str, dry_run: object, label: str, extra: tuple[str, ...], unknown: dict[str, str]
    ) -> GitHub | None:
        if "token" in unknown:
            del unknown["token"]
            _warn("tokens are read from GITHUB_TOKEN or GH_TOKEN only, so the token argument is ignored")
        if unknown:
            _warn(f"ignoring unknown arguments: {', '.join(unknown)}")
        if extra:
            _warn(f"ignoring {len(extra)} extra positional argument{'s' if len(extra) > 1 else ''}")
        if not isinstance(dry_run, bool):
            _warn(f"dry_run must be true or false, not '{dry_run}', so this is a dry run")
        if not repo:
            _warn("repo is missing, so nothing is reported: use repo=owner/name")
            return None
        if not REPO.fullmatch(repo):
            _warn(f"repo must be owner/name, not '{repo}', so nothing is reported")
            return None
        if not label or "," in label:
            _warn(f"label must be non-empty and contain no comma, not '{label}', so nothing is reported")
            return None
        token = None
        if dry_run is False:
            token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
            if not token:
                _warn("no GITHUB_TOKEN or GH_TOKEN; falling back to a dry run")
        return GitHub(repo, label, token)

    def start_suite(self, data, result) -> None:
        try:
            if data.parent is None:
                output_dir = BuiltIn().get_variable_value("${OUTPUT DIR}")
                self._output_dir = Path(output_dir) if output_dir else None
        except Exception as error:
            _warn(f"could not read the output directory: {type(error).__name__}: {error}")

    def end_test(self, data, result) -> None:
        if self.client is None or not result.failed:
            return
        full_name = result.full_name
        try:
            url = content.run_url()
            self.client.report(
                content.title(full_name),
                content.body(result.message, data.source, data.lineno, url),
                content.comment(result.message, data.source, data.lineno, url),
            )
        except GitHubError as error:
            reason = str(error)
            if error.unreachable:
                reason += "; GitHub cannot be reached, so no more requests are sent in this run"
            _warn(f"could not report '{full_name}': {reason}")
        except Exception as error:
            _warn(f"could not report '{full_name}': {type(error).__name__}: {error}")

    def end_suite(self, data, result) -> None:
        if self.client is None or data.parent is not None:
            return
        try:
            if self.client.dry_run:
                self._write_requests()
            else:
                for outcome in self.client.outcomes:
                    logger.console(f"github-reporter: {outcome.action} {outcome.url} ({outcome.title})")
        except Exception as error:
            _warn(f"could not finish: {type(error).__name__}: {error}")

    def _write_requests(self) -> None:
        requests = self.client.requests
        for request in requests:
            logger.console(f"github-reporter (dry run): {request.method} {request.url}")
            if request.body is not None:
                logger.console(json.dumps(request.body, indent=2, ensure_ascii=False))
        path = (self._output_dir or Path.cwd()) / REQUESTS_FILE
        text = json.dumps([request.to_json() for request in requests], indent=2, ensure_ascii=False) + "\n"
        try:
            path.write_text(text, encoding="utf-8")
        except OSError as error:
            _warn(f"could not write {path}: {error}")
