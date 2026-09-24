"""Turn recorded agent sessions into a Markdown transcript (spec: workshop/facilitation).

    uv run --no-sync python tools/transcript.py EVENTS.jsonl [...] --title TEXT --out FILE
                                                [--repo DIR] [--secrets .env ...] [--agent TEXT]

Reads the JSON event streams of Claude Code (`claude -p --output-format stream-json --verbose`)
and Codex (`codex exec --json`), in order, together with the rehearsal's own lines:

    {"type": "workshop.step", "title": "...", "prompt": "..."}      a lab step and the prompt it gives
    {"type": "workshop.prompt", "prompt": "..."}                   a prompt given to the agent
    {"type": "workshop.command", "command": "...", "output": "..."}  a command the participant runs
    {"type": "workshop.note", "text": "..."}                         a remark, in Markdown

Writes the prompts, the agent's answers, its tool calls with shortened results, and the commands.
Drops reasoning. Rewrites the repository path to <repo> and the home directory to ~. Refuses to
write, with exit status 1, when the result still contains a secret: a value of a key, token,
secret or password setting in the given --secrets files, or anything shaped like an API key.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SECRET_SHAPES = [
    re.compile(r"\bsk-[A-Za-z0-9_\-]{16,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"\bxox[abpr]-[A-Za-z0-9\-]{10,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)\b(api[_-]?key|token|secret|password)\s*[=:]\s*['\"]?[A-Za-z0-9_\-./+]{12,}"),
]
SECRET_SETTING = re.compile(r"(?i)(KEY|TOKEN|SECRET|PASSWORD)")
MAX_LINES = 12


def short(text: str, lines: int = MAX_LINES) -> str:
    rows = str(text).rstrip().splitlines()
    if len(rows) > lines:
        rows = rows[:lines] + [f"... ({len(rows) - lines} more lines)"]
    return "\n".join(row[:200] for row in rows)


def fence(text: str, lang: str = "") -> str:
    return f"```{lang}\n{text}\n```" if text.strip() else "*(no output)*"


def quote(text: str) -> str:
    return "\n".join("> " + line if line.strip() else ">" for line in text.strip().splitlines())


def tool_input(name: str, data: dict) -> str:
    """One line for what a tool call does."""
    if name == "Bash":
        return f"runs `{data.get('command', '')}`"
    if name in ("Write", "Edit", "MultiEdit", "Read"):
        return f"{ {'Write': 'writes', 'Edit': 'edits', 'MultiEdit': 'edits', 'Read': 'reads'}[name] } `{data.get('file_path', '')}`"
    if name in ("Grep", "Glob"):
        return f"searches for `{data.get('pattern', '')}`"
    if name == "Skill":
        return f"loads the skill `{data.get('skill') or data.get('command', '')}`"
    if name.startswith("mcp__"):
        server_tool = name.split("__", 2)[1:]
        args = json.dumps(data)[:160]
        return f"calls `{'/'.join(server_tool)}` with `{args}`"
    return f"uses `{name}` with `{json.dumps(data)[:160]}`"


def render(paths: list[Path], title: str, agent: str) -> tuple[str, dict]:
    out = [f"# {title}", ""]
    if agent:
        out += [f"*Recorded with {agent}, from the lab's instructions. Results are shortened; your agent's answers "
                f"will differ in wording.*", ""]
    totals = {"input_tokens": 0, "output_tokens": 0, "turns": 0}
    pending: dict[str, str] = {}  # Claude tool_use_id -> tool name
    for path in paths:
        for raw in path.read_text(encoding="utf-8").splitlines():
            try:
                event = json.loads(raw)
            except ValueError:
                continue
            kind = event.get("type")
            if kind == "workshop.step":
                out += [f"## {event['title']}", ""]
                if event.get("prompt"):
                    out += ["**Prompt:**", "", quote(event["prompt"]), ""]
            elif kind == "workshop.prompt":
                out += ["**Prompt:**", "", quote(event["prompt"]), ""]
            elif kind == "workshop.command":
                out += [f"**The participant runs** `{event['command']}`:", "", fence(short(event.get("output", ""))), ""]
            elif kind == "workshop.note":
                out += [event["text"], ""]
            elif kind == "assistant":  # Claude Code
                for part in event.get("message", {}).get("content", []):
                    if part.get("type") == "text" and part.get("text", "").strip():
                        out += ["**Agent:**", "", part["text"].strip(), ""]
                    elif part.get("type") == "tool_use":
                        pending[part.get("id", "")] = part.get("name", "")
                        out += [f"*The agent {tool_input(part.get('name', ''), part.get('input') or {})}*", ""]
            elif kind == "user":  # Claude Code tool results
                for part in event.get("message", {}).get("content", []) if isinstance(event.get("message", {}).get("content"), list) else []:
                    if part.get("type") != "tool_result":
                        continue
                    name = pending.get(part.get("tool_use_id", ""), "")
                    if name in ("Read", "Skill", "ToolSearch"):
                        continue
                    content = part.get("content")
                    text = content if isinstance(content, str) else "\n".join(
                        c.get("text", "") for c in content or [] if isinstance(c, dict))
                    out += [fence(short(text)), ""]
            elif kind == "result":  # Claude Code, end of a session
                usage = event.get("usage") or {}
                totals["input_tokens"] += (usage.get("input_tokens", 0) + usage.get("cache_read_input_tokens", 0)
                                           + usage.get("cache_creation_input_tokens", 0))
                totals["output_tokens"] += usage.get("output_tokens", 0)
                totals["turns"] += event.get("num_turns", 0)
            elif kind == "item.completed":  # Codex
                item = event.get("item") or {}
                it = item.get("type")
                if it == "agent_message":
                    out += ["**Agent:**", "", item.get("text", "").strip(), ""]
                elif it == "command_execution":
                    out += [f"*The agent runs* `{item.get('command', '')}` *(exit {item.get('exit_code')})*", "",
                            fence(short(item.get("aggregated_output", ""))), ""]
                elif it == "file_change":
                    for change in item.get("changes", []):
                        out += [f"*The agent {change.get('kind', 'changes')}s* `{change.get('path', '')}`", ""]
                elif it == "mcp_tool_call":
                    out += [f"*The agent calls* `{item.get('server')}/{item.get('tool')}`", ""]
            elif kind == "turn.completed":  # Codex
                usage = event.get("usage") or {}
                totals["input_tokens"] += usage.get("input_tokens", 0)
                totals["output_tokens"] += usage.get("output_tokens", 0)
                totals["turns"] += 1
    return "\n".join(out).rstrip() + "\n", totals


def secret_values(files: list[Path]) -> list[str]:
    values = []
    for file in files:
        if not file.is_file():
            continue
        for line in file.read_text(encoding="utf-8").splitlines():
            key, sep, value = line.partition("=")
            value = value.strip().strip("'\"")
            if sep and SECRET_SETTING.search(key) and len(value) >= 8:
                values.append(value)
    return values


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="transcript", description=__doc__.split("\n\n")[0])
    parser.add_argument("events", nargs="+", type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--repo", type=Path, help="the clone the session ran in; rewritten to <repo>")
    parser.add_argument("--secrets", action="append", type=Path, default=[], help=".env files whose secrets must not appear")
    parser.add_argument("--agent", default="", help='for example "Claude Code 2.1.281"')
    args = parser.parse_args(argv)

    text, totals = render(args.events, args.title, args.agent)
    for path in filter(None, [args.repo and str(args.repo.resolve()), args.repo and str(args.repo)]):
        text = text.replace(path, "<repo>")
    text = text.replace(str(Path.home()), "~")
    text = re.sub(r"/tmp/claude-\d+/[^\s`'\")]*", "<scratch>", text)

    found = [f"a value from {', '.join(map(str, args.secrets))}" for value in secret_values(args.secrets) if value in text]
    found += [f"something shaped like a secret ({pattern.pattern[:30]}...)" for pattern in SECRET_SHAPES if pattern.search(text)]
    if found:
        print(f"transcript: refusing to write {args.out}: it contains {found[0]}", file=sys.stderr)
        return 1
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(f"{args.out}: {len(text.splitlines())} lines, {totals['turns']} turns, "
          f"{totals['input_tokens']} input and {totals['output_tokens']} output tokens")
    return 0


if __name__ == "__main__":
    sys.exit(main())
