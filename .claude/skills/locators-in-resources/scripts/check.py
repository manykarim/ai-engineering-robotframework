"""Report every argument in a test file that looks like a locator: convention 2, "Locators live in resources".

    uv run --no-sync python .claude/skills/locators-in-resources/scripts/check.py tests/ [more files or folders]

Run it from the repository root. It parses the files with Robot Framework's own parser, so it sees every argument
exactly as Robot Framework does: in test cases, in setups and teardowns, and in the file's own *** Variables *** and
*** Keywords *** sections. It follows the resources a file imports, so a test that passes a resource variable that
holds a locator, such as ${GRID} or ${GRID} >> article, is reported too. Exits with 1 when an argument is a locator.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from robot.api import get_model, get_resource_model
from robot.api.parsing import ModelVisitor, Token

TAG = (r"(?:a|article|aside|button|dialog|div|fieldset|footer|form|h[1-6]|header|img|input|label|li|main|nav|ol"
       r"|option|p|section|select|span|table|tbody|td|textarea|th|thead|tr|ul)")
LOCATOR = re.compile(
    rf"""
        ^(?:css|xpath|text|role|data-testid|data-test-id|data-test)=  # a selector engine: role=button[name="Apply"]
      | ^id=[A-Za-z]                            # id=email; id=1 is more likely a named argument
      | ^\(?//                                  # XPath: //button, (//a)[2]
      | ^\\?\#[A-Za-z]                          # #email, which a .robot file writes as \#email
      | ^\.[A-Za-z]                             # .product-grid
      | ^\[[A-Za-z][\w-]*\s*(?:[~|^$*]?=|\])    # [name="email"], [disabled]
      | ^{TAG}(?:[\[.\#:]|\s+[>+~]\s)           # a[href="/cart"], div.card, button:has-text("Add"), ul > li
      | \s>>\s                                  # a chain: form >> role=textbox, ${{GRID}} >> article
    """,
    re.X,
)
# A named argument, such as selector=#email, or an argument's default value, such as ${field}=[name="email"].
NAMED = re.compile(r"^(?:[A-Za-z_]\w*|\$\{[^}]+\})=(?P<value>.+)$")
VARIABLE = re.compile(r"\$\{([^{}]+)\}")
# Statements whose arguments are text, tags or imports, never data a keyword turns into a locator.
NOT_DATA = {"Documentation", "Metadata", "Tags", "TestTags", "DefaultTags", "KeywordTags",
            "LibraryImport", "ResourceImport", "VariablesImport"}


def normalize(name: str) -> str:
    """A variable name as Robot Framework matches it: ignoring case, spaces and underscores."""
    return re.sub(r"[\s_]", "", name).lower()


def looks_like_locator(value: str) -> bool:
    named = NAMED.match(value)
    return any(LOCATOR.search(v) for v in (value, named["value"] if named else ""))


def locator_variables(path: Path, model, seen: set[Path]) -> dict[str, str]:
    """{normalized name: "${NAME} from <file>"} for the scalar variables that hold a locator, in `model` and in
    every resource it imports."""
    found: dict[str, str] = {}
    for node in (n for section in model.sections for n in section.body):
        if type(node).__name__ == "ResourceImport":
            name = node.name.replace("${CURDIR}", str(path.parent))
            resource = next((f for f in (path.parent / name, Path(name)) if f.is_file()), None)
            if resource and resource.resolve() not in seen:
                seen.add(resource.resolve())
                found |= locator_variables(resource, get_resource_model(str(resource)), seen)
        elif type(node).__name__ == "Variable" and node.name.startswith("$"):
            refers = any(normalize(v) in found for value in node.value for v in VARIABLE.findall(value))
            if refers or any(looks_like_locator(value) for value in node.value):
                found[normalize(node.name.rstrip("= ")[2:-1])] = f"{node.name.rstrip('= ')} from {path}"
    return found


class Arguments(ModelVisitor):
    def __init__(self):
        self.arguments: list[tuple[int, str]] = []

    def visit_Statement(self, node):  # noqa: N802 - Robot Framework's visitor naming
        if type(node).__name__ not in NOT_DATA:
            self.arguments += [(token.lineno, token.value) for token in node.get_tokens(Token.ARGUMENT)]


def findings(path: Path) -> list[str]:
    model = get_model(str(path))
    variables = locator_variables(path, model, {path.resolve()})
    visitor = Arguments()
    visitor.visit(model)
    problems = []
    for line, value in visitor.arguments:
        held = [variables[normalize(v)] for v in VARIABLE.findall(value) if normalize(v) in variables]
        if looks_like_locator(value) or held:
            problems.append(f"{path}:{line}: '{value}' is a locator" + (f" ({', '.join(held)})" if held else ""))
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
