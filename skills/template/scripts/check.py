"""Report test cases whose name does not start with <STORY>_<AC> and that carry no smoke tag.

    uv run --no-sync python scripts/check.py tests/ [more files or folders]

The helper script of the Lab 3 skill template. It parses the files with Robot Framework's own
parser, so it sees the test names and tags exactly as Robot Framework does. Exits with 1 when a
test breaks the rule.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from robot.api import get_model
from robot.api.parsing import ModelVisitor

CRITERION = re.compile(r"^[A-Z]+-\d{3}_AC-\d+ ")


class Tests(ModelVisitor):
    def __init__(self):
        self.default_tags: list[str] = []
        self.tests: list[tuple[str, int, list[str]]] = []

    def visit_TestTags(self, node):  # noqa: N802 - Robot Framework's visitor naming
        self.default_tags += list(node.values)

    def visit_TestCase(self, node):  # noqa: N802
        tags = [t for statement in node.body if type(statement).__name__ == "Tags" for t in statement.values]
        self.tests.append((node.name, node.lineno, tags))


def findings(path: Path) -> list[str]:
    visitor = Tests()
    visitor.visit(get_model(str(path)))
    problems = []
    for name, line, tags in visitor.tests:
        if not CRITERION.match(name) and "smoke" not in visitor.default_tags + tags:
            problems.append(f"{path}:{line}: '{name}' starts with no <STORY>_<AC> ID and has no smoke tag")
    return problems


def main(argv: list[str]) -> int:
    paths = [Path(a) for a in argv] or [Path("tests")]
    files = [f for p in paths for f in (sorted(p.rglob("*.robot")) if p.is_dir() else [p])]
    problems = [problem for f in files for problem in findings(f)]
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
