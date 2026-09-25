"""File a bug in Jira Cloud - or, by default, show the issue that would be filed.

    uv run --no-sync python scripts/file_issue.py --summary TEXT (--body-file FILE | --body TEXT)
                                                  [--label NAME ...] [--issue-type Bug] [--send]

Reads JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN and JIRA_PROJECT from the environment or from the
nearest .env; the environment wins. Nothing is sent unless all four are set and --send is given.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

SETTINGS = ("JIRA_URL", "JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_PROJECT")


def settings() -> dict[str, str]:
    from dotenv import dotenv_values, find_dotenv

    dotenv = dotenv_values(find_dotenv(usecwd=True)) if find_dotenv(usecwd=True) else {}
    return {name: os.environ.get(name) or dotenv.get(name) or "" for name in SETTINGS}


def adf(markdown: str) -> dict:
    """Markdown-ish text as Atlassian Document Format: paragraphs, and fenced blocks as code."""
    content, block, fence = [], [], False
    for line in markdown.splitlines() + [""]:
        if line.startswith("```"):
            if fence:
                content.append({"type": "codeBlock", "content": [{"type": "text", "text": "\n".join(block)}]})
                block = []
            elif block:
                content.append({"type": "paragraph", "content": [{"type": "text", "text": "\n".join(block)}]})
                block = []
            fence = not fence
        elif fence or line.strip():
            block.append(line)
        elif block:
            content.append({"type": "paragraph", "content": [{"type": "text", "text": "\n".join(block)}]})
            block = []
    return {"type": "doc", "version": 1, "content": content}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="file-issue", description=__doc__.split("\n\n")[0])
    parser.add_argument("--summary", required=True)
    body = parser.add_mutually_exclusive_group(required=True)
    body.add_argument("--body-file", type=Path)
    body.add_argument("--body")
    parser.add_argument("--label", action="append", default=[], help="repeatable")
    parser.add_argument("--issue-type", default="Bug")
    parser.add_argument("--send", action="store_true", help="really create the issue")
    args = parser.parse_args(argv)

    text = args.body_file.read_text(encoding="utf-8") if args.body_file else args.body
    config = settings()
    fields = {
        "project": {"key": config["JIRA_PROJECT"] or "<JIRA_PROJECT>"},
        "summary": args.summary,
        "issuetype": {"name": args.issue_type},
        "description": adf(text),
        "labels": args.label,
    }
    url = f"{(config['JIRA_URL'] or '<JIRA_URL>').rstrip('/')}/rest/api/3/issue"
    missing = [name for name in SETTINGS if not config[name]]

    if missing or not args.send:
        reason = f"missing {', '.join(missing)}" if missing else "add --send to create it"
        print(f"Dry run ({reason}). Nothing was sent.\n")
        print(f"POST {url}")
        print(f"as {config['JIRA_EMAIL'] or '<JIRA_EMAIL>'} with an API token\n")
        print(json.dumps({"fields": fields}, indent=2))
        return 0

    import requests

    try:
        response = requests.post(url, json={"fields": fields}, auth=(config["JIRA_EMAIL"], config["JIRA_API_TOKEN"]),
                                 headers={"Accept": "application/json"}, timeout=30)
    except requests.RequestException as exc:
        print(f"Could not reach Jira at {config['JIRA_URL']}: {type(exc).__name__}", file=sys.stderr)
        return 1
    if response.status_code >= 300:
        print(f"Jira refused the issue: HTTP {response.status_code}: {response.text[:500]}", file=sys.stderr)
        return 1
    key = response.json()["key"]
    print(f"Created {key}: {config['JIRA_URL'].rstrip('/')}/browse/{key}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
