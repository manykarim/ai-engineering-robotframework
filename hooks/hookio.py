"""What an agent's hook call is about, whichever agent sent it, and how to answer it.

Claude Code, Codex and GitHub Copilot each pass a JSON object on stdin, in their own shape:

    Claude Code  {"tool_name": "Write"|"Edit"|"MultiEdit"|"Bash", "tool_input": {...}}
    Codex        {"tool_name": "apply_patch"|"Bash", "tool_input": {"command": <patch or shell>}}
    Copilot      {"toolName": "create"|"edit"|"bash", "toolArgs": {...}}

read_call() turns any of them into a Call; deny() and report() answer in the way the sending
agent understands. Input that cannot be read lets the action through, with a warning: a
guardrail that breaks must not stop the agent.
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Edit:
    path: Path  # relative to the repository root when inside it
    before: str  # the file's text before the edit ("" for a new file)
    after: str  # the file's text after it (for a Codex patch: before plus the added lines)


@dataclass
class Call:
    agent: str  # "claude-code", "codex" or "copilot"
    kind: str  # "edit", "shell" or "other"
    edits: list[Edit] = field(default_factory=list)
    command: str = ""


def _relative(path: str, cwd: str) -> Path:
    absolute = Path(path) if Path(path).is_absolute() else Path(cwd) / path
    try:
        return absolute.resolve().relative_to(ROOT)
    except ValueError:
        return absolute


def _current(path: Path) -> str:
    file = path if path.is_absolute() else ROOT / path
    try:
        return file.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def _replaced(path: Path, replacements: list[tuple[str, str, bool]]) -> Edit:
    before = after = _current(path)
    for old, new, every in replacements:
        after = after.replace(old, new) if every else after.replace(old, new, 1)
    return Edit(path, before, after)


def _patch_edits(patch: str, cwd: str) -> list[Edit]:
    """The files of a Codex apply_patch envelope, each with its added lines appended."""
    edits: dict[Path, list[str]] = {}
    current = None
    for line in patch.splitlines():
        for marker in ("*** Add File: ", "*** Update File: "):
            if line.startswith(marker):
                current = _relative(line[len(marker):].strip(), cwd)
                edits.setdefault(current, [])
                break
        else:
            if line.startswith("*** "):
                current = None
            elif current is not None and line.startswith("+"):
                edits[current].append(line[1:])
    return [Edit(path, _current(path), _current(path) + "\n" + "\n".join(lines)) for path, lines in edits.items()]


def parse(payload: dict) -> Call:
    cwd = payload.get("cwd") or os.getcwd()
    if "toolName" in payload:  # GitHub Copilot
        tool, args = payload["toolName"], payload.get("toolArgs") or {}
        if isinstance(args, str):
            args = json.loads(args)
        path = _relative(args.get("path", ""), cwd)
        if tool == "create":
            return Call("copilot", "edit", [Edit(path, _current(path), args.get("file_text") or "")])
        if tool == "edit":
            return Call("copilot", "edit", [_replaced(path, [(args.get("old_str", ""), args.get("new_str", ""), False)])])
        if tool in ("bash", "powershell"):
            return Call("copilot", "shell", command=args.get("command", ""))
        return Call("copilot", "other")
    tool, args = payload.get("tool_name", ""), payload.get("tool_input") or {}
    agent = "codex" if "turn_id" in payload or tool == "apply_patch" or "model" in payload else "claude-code"
    if tool == "apply_patch":
        return Call(agent, "edit", _patch_edits(args.get("command") or args.get("input") or "", cwd))
    path = _relative(args.get("file_path", ""), cwd)
    if tool == "Write":
        return Call(agent, "edit", [Edit(path, _current(path), args.get("content", ""))])
    if tool == "Edit":
        change = (args.get("old_string", ""), args.get("new_string", ""), bool(args.get("replace_all")))
        return Call(agent, "edit", [_replaced(path, [change])])
    if tool == "MultiEdit":
        changes = [(e.get("old_string", ""), e.get("new_string", ""), bool(e.get("replace_all")))
                   for e in args.get("edits", [])]
        return Call(agent, "edit", [_replaced(path, changes)])
    if tool in ("Bash", "shell"):
        return Call(agent, "shell", command=args.get("command", ""))
    return Call(agent, "other")


def read_call() -> Call | None:
    """The hook call on stdin, or None when there is none (the script runs as a command).

    Scripts call it only when they got no command-line arguments: an agent passes none.
    """
    if sys.stdin.isatty():
        return None
    raw = sys.stdin.read()
    if not raw.strip():
        return None
    try:
        return parse(json.loads(raw))
    except (ValueError, AttributeError, TypeError) as exc:
        print(f"hook: could not read the agent's input ({type(exc).__name__}); letting the action through",
              file=sys.stderr)
        sys.exit(0)


def deny(call: Call, reason: str) -> None:
    """Refuse the action about to happen, and tell the agent why."""
    if call.agent == "copilot":
        print(json.dumps({"permissionDecision": "deny", "permissionDecisionReason": reason}))
    print(reason, file=sys.stderr)
    sys.exit(2)


def report(call: Call, message: str, problem: bool) -> None:
    """After an action: give the agent a result it must take into account."""
    if call.agent == "copilot":
        print(json.dumps({"additionalContext": message}))
        sys.exit(0)
    if problem:
        print(message, file=sys.stderr)
        sys.exit(2)
    print(message)
    sys.exit(0)
