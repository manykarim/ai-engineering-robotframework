"""Check docs/facilitator/suite-outcomes.toml against the pinned shop (spec: workshop/baseline-suite).

    uv run --no-sync python tools/verify_outcomes.py [--heal] [--preset NAME ...] [--data PATH] [--keep DIR]

For every preset: apply it through the shop helper, run the unmodified suite with
RobotCode, and compare the failing tests with the data. It works in whichever mode
SHOP_URL and SHOP_SPACE select, and always resets the space when it finishes.
Exits with status 1 on any difference.

--heal checks drift_and_bug with the heal profile instead, and leaves out the tests
tagged broken, as Module 8 does. It needs a healing model (HEAL_MODEL or
HEAL_LOCATOR_MODEL, in the environment or .env); without one, robotframework-heal
skips healing and the check would prove nothing.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import dotenv_values  # noqa: E402

from shop.config import load  # noqa: E402

DATA = ROOT / "docs" / "facilitator" / "suite-outcomes.toml"
MODEL_SETTINGS = ("HEAL_MODEL", "HEAL_LOCATOR_MODEL")


def helper(*args: str) -> None:
    done = subprocess.run([sys.executable, "-m", "shop", *args], cwd=ROOT, capture_output=True, text=True)
    if done.returncode != 0:
        raise SystemExit(f"verify-outcomes: `python -m shop {' '.join(args)}` failed: {done.stderr.strip()}")


def run_suite(profiles: list[str], options: list[str], outdir: Path) -> tuple[set[str], set[str]]:
    """Run the suite; return the names of the failed and the passed tests."""
    robotcode = shutil.which("robotcode", path=str(Path(sys.executable).parent)) or "robotcode"
    subprocess.run([robotcode, *profiles, "robot", *options, "--outputdir", str(outdir), "--report", "NONE",
                    "--log", "NONE", "--console", "quiet"], cwd=ROOT, capture_output=True, text=True)
    output = outdir / "output.xml"
    if not output.is_file():
        raise SystemExit("verify-outcomes: the suite produced no output.xml - see `uv run robotcode robot` for the error")
    failed, passed = set(), set()
    for test in ET.parse(output).getroot().iter("test"):
        (failed if test.find("status").get("status") == "FAIL" else passed).add(test.get("name"))
    return failed, passed


def model_configured() -> bool:
    dotenv = dotenv_values(ROOT / ".env") if (ROOT / ".env").is_file() else {}
    return any(os.environ.get(name) or dotenv.get(name) for name in MODEL_SETTINGS)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="verify-outcomes", description=__doc__.split("\n\n")[0])
    parser.add_argument("--heal", action="store_true", help="check drift_and_bug with the heal profile (needs a model)")
    parser.add_argument("--preset", action="append", help="check only this preset (repeatable)")
    parser.add_argument("--data", type=Path, default=DATA, help="the outcomes file (default: %(default)s)")
    parser.add_argument("--keep", type=Path, metavar="DIR",
                        help="keep each preset's results, including a healing report, under DIR/<preset>/")
    args = parser.parse_args(argv)

    data = tomllib.loads(args.data.read_text(encoding="utf-8"))
    settings = load()
    if settings.problem:
        raise SystemExit(f"verify-outcomes: {settings.problem}")
    if args.heal and not model_configured():
        print("verify-outcomes: --heal needs a healing model (HEAL_MODEL or HEAL_LOCATOR_MODEL in the environment "
              "or .env). Without one, robotframework-heal skips healing and this check would prove nothing.", file=sys.stderr)
        return 2

    expectations = data["heal"] if args.heal else data["presets"]
    presets = args.preset or list(expectations)
    profiles = ["-p", "shared" if settings.shared else "local"] + (["-p", "heal"] if args.heal else [])
    # Module 8 runs without the tests broken on purpose: the Module 5 one fails only on a
    # wrong label, which a model may well heal (docs/facilitator/suite-outcomes.md).
    options = ["--exclude", "broken"] if args.heal else []
    inventory = {name for name, kind in data["tests"].items() if not (args.heal and kind == "broken")}
    where = f"{settings.url}" + (f", space {settings.space}" if settings.space else "")
    print(f"verify-outcomes - {where}{' - with healing' if args.heal else ''}")

    differences = 0
    try:
        for preset in presets:
            expected = expectations[preset]
            # Presets compose: `buggy` switches only the bug flags and keeps the current
            # locator stage. Every preset is therefore measured from `clean`.
            helper("preset", "clean")
            if preset != "clean":
                helper("preset", preset)
            if args.keep:
                outdir = args.keep / preset
                outdir.mkdir(parents=True, exist_ok=True)
                failed, passed = run_suite(profiles, options, outdir)
            else:
                with tempfile.TemporaryDirectory(prefix=f"outcomes-{preset}-") as tmp:
                    failed, passed = run_suite(profiles, options, Path(tmp))
            problems = []
            for name in sorted((failed | passed) - inventory):
                problems.append(f"{name}: not in [tests] - add it to {args.data.name}")
            for name in sorted(inventory - (failed | passed)):
                problems.append(f"{name}: did not run")
            for name in sorted(failed - set(expected)):
                problems.append(f"{name}: expected to pass, failed")
            for name in sorted(set(expected) - failed):
                problems.append(f"{name}: expected to fail ({', '.join(expected[name])}), passed")
            differences += len(problems)
            status = "ok" if not problems else f"{len(problems)} difference{'s' if len(problems) > 1 else ''}"
            print(f"  {preset:14} {status:15} {len(failed)} failed, {len(passed)} passed")
            for problem in problems:
                print(f"      {problem}")
    finally:
        helper("reset")
    print("matches the recorded outcomes" if not differences else f"{differences} difference(s) from {args.data.name}")
    return 1 if differences else 0


if __name__ == "__main__":
    sys.exit(main())
