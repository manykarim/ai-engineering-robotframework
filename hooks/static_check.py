"""Check edited test and resource files statically, and tell the agent only what is wrong.

As a hook (after an edit): runs `robotcode analyze code` on the edited .robot and .resource files
under tests/ and resources/. It needs no shop and takes about two seconds. A clean file gives no
output at all; otherwise the agent gets the error lines, at most MAX_LINES of them. Warnings, hints
and the summary line are left out, so the check costs few tokens. As a command, it takes files or
folders, by default tests/ and resources/:

    uv run --no-sync python hooks/static_check.py tests/ui/checkout.robot
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

from hookio import ROOT, read_call, report

ERROR = re.compile(r"^(?P<path>.+?):(?P<line>\d+):(?P<column>\d+): \[ERROR\] (?P<message>.*)$")
MAX_LINES = 5
TIMEOUT = 50  # seconds; the wiring gives the hook 60


def is_robot_file(path: Path) -> bool:
    return path.suffix in (".robot", ".resource") and path.parts[:1] in (("tests",), ("resources",))


def errors(paths: list[Path]) -> list[str]:
    """The error findings of `robotcode analyze code` for the given files or folders."""
    robotcode = shutil.which("robotcode", path=str(Path(sys.executable).parent)) or "robotcode"
    try:
        result = subprocess.run([robotcode, "analyze", "code", *map(str, paths)],
                                cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return [f"robotcode analyze did not finish within {TIMEOUT} s."]
    found = []
    for line in result.stdout.splitlines():
        match = ERROR.match(line.strip())
        if match:
            path = Path(match["path"]).as_posix()
            found.append(f"{path}:{match['line']}:{match['column']}: {match['message']}")
    return found


def summary(found: list[str]) -> str:
    shown = found[:MAX_LINES]
    more = f"\n- and {len(found) - MAX_LINES} more" if len(found) > MAX_LINES else ""
    return (f"Static check (robotcode analyze code): {len(found)} error(s).\n"
            + "\n".join(f"- {line}" for line in shown) + more)


def main(argv: list[str]) -> int:
    call = None if argv else read_call()
    if call is None:
        paths = [Path(a) for a in argv] or [Path("tests"), Path("resources")]
        found = errors(paths)
        if found:
            print(summary(found))
        return 1 if found else 0
    if call.kind != "edit":
        return 0
    # The edit has happened: check the files as they are now, not as the hook input describes them.
    files = sorted({e.path for e in call.edits if is_robot_file(e.path) and (ROOT / e.path).is_file()})
    if not files:
        return 0
    found = errors(files)
    if found:
        report(call, summary(found), problem=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
