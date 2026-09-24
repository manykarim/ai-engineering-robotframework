"""setup-check: one command that verifies the workshop environment (spec: workshop/setup-check).

    uv run --no-sync python setup-check/check.py [--json] [--offline]

``--no-sync`` matters: plain ``uv run`` repairs the environment before running,
which would hide exactly the drift this check exists to find.

The check only reads and reports. It never installs, starts or stops anything;
its only side effects are a headless browser opening ``about:blank`` and
read-only requests. Expected versions come from ``uv.lock``, the
``[tool.workshop]`` table of ``pyproject.toml`` and ``shop/compose.yaml`` -
never from a list of its own (design D6).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
import tomllib
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import dotenv_values  # noqa: E402

from shop.config import USER_AGENT  # noqa: E402
from shop.config import load as load_shop  # noqa: E402

PYPROJECT = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
PINS = PYPROJECT["tool"]["workshop"]
COMPOSE = ROOT / "shop" / "compose.yaml"
IMAGE_RE = re.compile(r"^\s*image:\s*(ghcr\.io/manykarim/demo-webshop):(\S+)\s*$", re.M)
ROBOTCODE_HABITS = ("discover", "libdoc", "robot-debug", "repl", "results")
AGENTS = ("claude", "codex", "copilot")
HEAL_SETTINGS = ("HEAL_MODEL", "HEAL_BASE_URL", "HEAL_API_KEY")
SECRET_NAME = re.compile(r"KEY|TOKEN|SECRET|PASSWORD|PASSWD", re.I)
#: How long to wait for a local shop that is still starting (seconds).
STARTUP_GRACE = 60

# SETUP.md headings the fixes point to (their GitHub anchors).
GUIDE = {
    "install": "SETUP.md#install",
    "browsers": "SETUP.md#browsers",
    "local": "SETUP.md#the-local-shop",
    "shared": "SETUP.md#the-shared-instance",
    "agent": "SETUP.md#coding-agent",
    "robotcode": "SETUP.md#robotcode",
    "node": "SETUP.md#nodejs-and-openspec",
    "gh": "SETUP.md#github-cli",
    "optional": "SETUP.md#optional-tracks",
    "heal": "SETUP.md#healing-api-key",
    "platforms": "SETUP.md#platforms",
}


@dataclass
class Result:
    id: str
    title: str
    module: str
    status: str  # pass | warn | fail | skip
    detail: str = ""
    fix: str = ""
    guide: str = ""


# --- small helpers -----------------------------------------------------------

def run(cmd: list[str], timeout: float = 60, cwd: Path | None = None) -> tuple[int, str]:
    """Run a command; return (exit status, combined output). Missing command -> 127."""
    exe = shutil.which(cmd[0]) or cmd[0]
    try:
        done = subprocess.run([exe, *cmd[1:]], capture_output=True, text=True, timeout=timeout,
                              cwd=cwd, encoding="utf-8", errors="replace")
        return done.returncode, (done.stdout or "") + (done.stderr or "")
    except FileNotFoundError:
        return 127, f"{cmd[0]}: not found"
    except subprocess.TimeoutExpired:
        return 124, f"{cmd[0]}: no answer within {timeout:.0f} s"


def version_tuple(text: str) -> tuple[int, ...]:
    match = re.search(r"(\d+(?:\.\d+)*)", text or "")
    return tuple(int(p) for p in match.group(1).split(".")) if match else ()


def satisfies(found: str, requirement: str) -> bool:
    """``found`` against ``>=X.Y`` or an exact ``X.Y.Z``."""
    if requirement.startswith(">="):
        return version_tuple(found) >= version_tuple(requirement[2:])
    return version_tuple(found) == version_tuple(requirement)


def first_version(output: str) -> str:
    match = re.search(r"\d+\.\d+(?:\.\d+)*", output)
    return match.group(0) if match else ""


def pinned_image() -> tuple[str, str]:
    match = IMAGE_RE.search(COMPOSE.read_text(encoding="utf-8"))
    if not match:
        raise SystemExit(f"setup-check: no pinned shop image found in {COMPOSE}")
    return match.group(1), match.group(2)


def browser_dirs() -> tuple[Path | None, Path | None]:
    """(node_modules of Browser's wrapper, the Playwright browsers directory) - wherever the package lives."""
    spec = importlib.util.find_spec("Browser")
    if not spec or not spec.origin:
        return None, None
    node_modules = Path(spec.origin).parent / "wrapper" / "node_modules"
    return node_modules, node_modules / "playwright-core" / ".local-browsers"


# --- the checks ---------------------------------------------------------------

class SetupCheck:
    def __init__(self, offline: bool):
        self.offline = offline
        self.results: list[Result] = []
        self.shop = load_shop()
        self.image, self.tag = pinned_image()
        self.dotenv = dotenv_values(ROOT / ".env") if (ROOT / ".env").is_file() else {}

    def add(self, *args, **kwargs) -> None:
        self.results.append(Result(*args, **kwargs))

    # M0 ------------------------------------------------------------------
    def python(self) -> None:
        want = (ROOT / ".python-version").read_text(encoding="utf-8").strip()
        have = platform.python_version()
        if version_tuple(have)[:2] == version_tuple(want)[:2]:
            self.add("python", "Python", "M0", "pass", f"{have}, as .python-version pins {want}")
        else:
            self.add("python", "Python", "M0", "fail", f"{have} found, {want} expected",
                     "uv sync --locked   (uv installs the right Python)", GUIDE["install"])

    def locked_environment(self) -> None:
        uv = os.environ.get("UV") or shutil.which("uv") or "uv"
        cmd = [uv, "sync", "--locked", "--dry-run"] + (["--offline"] if self.offline else [])
        status, out = run(cmd, timeout=180, cwd=ROOT)
        if status != 0:
            reason = "uv.lock does not match pyproject.toml" if "needs to be updated" in out else out.strip().splitlines()[-1:]
            self.add("locked-environment", "Locked environment", "M0", "fail", str(reason),
                     "git checkout -- pyproject.toml uv.lock, then uv sync --locked", GUIDE["install"])
            return
        removed = dict(re.findall(r"^\s*-\s+([A-Za-z0-9_.\-]+)==(\S+)", out, re.M))
        added = dict(re.findall(r"^\s*\+\s+([A-Za-z0-9_.\-]+)==(\S+)", out, re.M))
        if not removed and not added:
            self.add("locked-environment", "Locked environment", "M0", "pass", "every installed package matches uv.lock")
            return
        problems = []
        for name in sorted(set(removed) | set(added)):
            if name in removed and name in added:
                problems.append(f"{name} {removed[name]} installed, {added[name]} locked")
            elif name in added:
                problems.append(f"{name} {added[name]} missing")
            else:
                problems.append(f"{name} {removed[name]} not in uv.lock")
        self.add("locked-environment", "Locked environment", "M0", "fail", "; ".join(problems),
                 "uv sync --locked", GUIDE["install"])

    def browser_runtime(self) -> None:
        node_modules, _ = browser_dirs()
        if node_modules is None:
            self.add("browser-runtime", "Browser runtime", "M0", "fail", "Browser Library is not installed",
                     "uv sync --locked", GUIDE["install"])
            return
        if importlib.util.find_spec("BrowserBatteries") is None:
            self.add("browser-runtime", "Browser runtime", "M0", "fail", "the batteries package with the bundled Node runtime is missing",
                     "uv sync --locked", GUIDE["browsers"])
            return
        # Batteries alone leave exactly one entry here; `rfbrowser init` adds the
        # separate Node dependencies (@grpc, playwright, ...) next to it.
        extra = sorted(p.name for p in node_modules.iterdir() if p.name != "playwright-core") if node_modules.is_dir() else []
        packages = [name for name in extra if not name.startswith(".")]
        if extra:
            self.add("browser-runtime", "Browser runtime", "M0", "fail",
                     f"`rfbrowser init` installed {len(packages)} Node packages next to the bundled runtime ({', '.join(packages[:3])}, ...)",
                     "uv run --no-sync rfbrowser clean-node, then uv run --no-sync rfbrowser install chromium", GUIDE["browsers"])
        else:
            self.add("browser-runtime", "Browser runtime", "M0", "pass", "bundled Node runtime, no separate Node dependencies")

    def browser_binaries(self) -> bool:
        _, browsers = browser_dirs()
        found = sorted(p.name for p in browsers.iterdir() if p.name.startswith("chromium")) if browsers and browsers.is_dir() else []
        if found:
            self.add("browser-binaries", "Browser binaries", "M0", "pass", ", ".join(found))
            return True
        self.add("browser-binaries", "Browser binaries", "M0", "fail",
                 "no Chromium inside .venv (recreating .venv removes it)",
                 "uv run --no-sync rfbrowser install chromium   (Linux: add --with-deps)", GUIDE["browsers"])
        return False

    def browser_launch(self, binaries: bool) -> None:
        if not binaries:
            self.add("browser-launch", "Headless browser", "M0", "skip", "no browser binaries to launch")
            return
        suite = ("*** Settings ***\nLibrary    Browser\n\n*** Test Cases ***\nOpen A Blank Page\n"
                 "    New Browser    chromium    headless=True\n    New Page    about:blank\n    Get Url    ==    about:blank\n")
        with tempfile.TemporaryDirectory(prefix="setup-check-") as tmp:
            (Path(tmp) / "launch.robot").write_text(suite, encoding="utf-8")
            status, out = run([sys.executable, "-m", "robot", "--outputdir", tmp, "--output", "NONE", "--report", "NONE",
                               "--log", "NONE", "--console", "quiet", "launch.robot"], timeout=180, cwd=Path(tmp))
        if status == 0:
            self.add("browser-launch", "Headless browser", "M0", "pass", "Chromium opened about:blank")
        else:
            last = next((line for line in reversed(out.strip().splitlines()) if line.strip()), "no output")
            self.add("browser-launch", "Headless browser", "M0", "fail", last[:200],
                     "uv run --no-sync rfbrowser install --with-deps chromium", GUIDE["browsers"])

    def container_runtime(self) -> None:
        if self.shop.shared:
            self.add("container-runtime", "Container runtime", "M0", "skip", "not needed with the shared instance")
            return
        status, out = run(["docker", "version", "--format", "{{.Server.Version}}"], timeout=30)
        if status != 0:
            self.add("container-runtime", "Container runtime", "M0", "fail", "Docker is not installed or not running",
                     "start Docker, or use the shared instance instead", GUIDE["local"])
            return
        engine = out.strip().splitlines()[-1]
        _, compose_out = run(["docker", "compose", "version", "--short"], timeout=30)
        compose = first_version(compose_out)
        problems = []
        if not satisfies(engine, PINS["docker"]):
            problems.append(f"Docker {engine} found, {PINS['docker']} needed")
        if not compose or not satisfies(compose, PINS["compose"]):
            problems.append(f"Compose {compose or 'v2 plugin missing'} found, {PINS['compose']} needed")
        if problems:
            self.add("container-runtime", "Container runtime", "M0", "fail", "; ".join(problems),
                     "update Docker (Compose v2 ships with it)", GUIDE["local"])
        else:
            self.add("container-runtime", "Container runtime", "M0", "pass", f"Docker {engine}, Compose {compose}")

    def shop_image(self) -> None:
        if self.shop.shared:
            self.add("shop-image", "Shop image", "M0", "skip", "not needed with the shared instance")
            return
        ref = f"{self.image}:{self.tag}"
        status, _ = run(["docker", "image", "inspect", ref], timeout=30)
        if status == 0:
            self.add("shop-image", "Shop image", "M0", "pass", ref)
        else:
            self.add("shop-image", "Shop image", "M0", "fail", f"{ref} is not on this machine",
                     "docker compose -f shop/compose.yaml pull", GUIDE["local"])

    def local_shop_starting(self) -> bool:
        """Whether a container of the pinned image is running and has not finished starting yet."""
        status, out = run(["docker", "ps", "--filter", f"ancestor={self.image}:{self.tag}", "--format", "{{.Status}}"], timeout=30)
        return status == 0 and "health: starting" in out

    def shop_health(self) -> None:
        if self.shop.shared and self.offline:
            self.add("shop-health", "Shop health", "M0", "skip", "offline mode")
            return
        guide = GUIDE["shared" if self.shop.shared else "local"]
        request = urllib.request.Request(self.shop.url + "/health", headers={"User-Agent": USER_AGENT, **self.shop.headers()})
        # A local shop that was just started seeds itself before it answers: a few
        # seconds usually, up to about 40 on a slow machine. While a container of the
        # pinned image is still starting, wait for it instead of failing a participant
        # who ran this right after `docker compose up -d`.
        deadline = time.monotonic() + STARTUP_GRACE
        while True:
            try:
                with urllib.request.urlopen(request, timeout=10) as response:
                    version = json.loads(response.read()).get("version", "?")
                break
            except urllib.error.HTTPError as error:
                self.add("shop-health", "Shop health", "M0", "fail", f"{self.shop.url} refused the health check with HTTP {error.code}",
                         "check SHOP_URL, and any proxy between you and the shop", guide)
                return
            except (urllib.error.URLError, TimeoutError, ConnectionError, ValueError):
                if self.shop.shared or time.monotonic() >= deadline or not self.local_shop_starting():
                    fix = "check SHOP_URL and your network" if self.shop.shared else "docker compose -f shop/compose.yaml up -d"
                    self.add("shop-health", "Shop health", "M0", "fail", f"nothing answers at {self.shop.url}", fix, guide)
                    return
                time.sleep(1)
        if not self.shop.shared and version != self.tag:
            self.add("shop-health", "Shop health", "M0", "fail",
                     f"the shop at {self.shop.url} reports version {version}, shop/compose.yaml pins {self.tag}",
                     "docker compose -f shop/compose.yaml up -d --force-recreate", GUIDE["local"])
        else:
            self.add("shop-health", "Shop health", "M0", "pass", f"{self.shop.url} answers, version {version}")

    def space(self) -> None:
        if self.shop.problem:
            self.add("space", "Workshop space", "M0", "fail", self.shop.problem,
                     "set SHOP_SPACE=<your GitHub handle> in .env", GUIDE["shared"])
        elif self.shop.space:
            self.add("space", "Workshop space", "M0", "pass", self.shop.space)
        else:
            self.add("space", "Workshop space", "M0", "pass", "none needed for the local shop")

    # M2-M8 ------------------------------------------------------------------
    def coding_agent(self) -> None:
        found = []
        for name in AGENTS:
            if shutil.which(name):
                _, out = run([name, "--version"], timeout=30)
                found.append(f"{name} {first_version(out) or '(version unknown)'}")
        if found:
            self.add("coding-agent", "Coding agent", "M2", "pass", ", ".join(found))
        else:
            self.add("coding-agent", "Coding agent", "M2", "fail", "none of claude, codex or copilot is on PATH",
                     "install one supported coding agent", GUIDE["agent"])

    def robotcode_commands(self) -> None:
        # robotcode has no __main__: call the console script next to this interpreter
        # (.venv/bin on Linux and macOS, .venv\\Scripts on Windows).
        exe = shutil.which("robotcode", path=str(Path(sys.executable).parent))
        if exe is None:
            self.add("robotcode-commands", "RobotCode commands", "M4", "fail", "RobotCode is not installed in the project environment",
                     "uv sync --locked", GUIDE["robotcode"])
            return
        _, out = run([exe, "--help"], timeout=60)
        commands = set(re.findall(r"^\s{2}([a-z][a-z-]+)\s", out, re.M))
        missing = [c for c in ROBOTCODE_HABITS if c not in commands]
        if missing:
            self.add("robotcode-commands", "RobotCode commands", "M4", "fail", f"missing: {', '.join(missing)}",
                     "uv sync --locked", GUIDE["robotcode"])
        else:
            self.add("robotcode-commands", "RobotCode commands", "M4", "pass", ", ".join(ROBOTCODE_HABITS))

    def robotcode_on_path(self) -> None:
        venv_bin = Path(sys.executable).parent.resolve()
        outside = os.pathsep.join(p for p in os.environ.get("PATH", "").split(os.pathsep)
                                  if p and Path(p).resolve() != venv_bin)
        other = shutil.which("robotcode", path=outside)
        if other:
            self.add("robotcode-path", "RobotCode on PATH", "M4", "warn",
                     f"typing `robotcode` without `uv run` starts {other}, not the project's {venv_bin}, "
                     "and it cannot see the project's libraries",
                     "always run `uv run robotcode ...`, or uninstall the global one", GUIDE["robotcode"])
        else:
            self.add("robotcode-path", "RobotCode on PATH", "M4", "pass", "only the project's RobotCode, through uv run")

    def node(self) -> None:
        status, out = run(["node", "--version"], timeout=30)
        found = first_version(out) if status == 0 else ""
        if found and satisfies(found, PINS["node"]):
            self.add("node", "Node.js", "M5", "pass", f"{found} ({PINS['node']} needed)")
        else:
            self.add("node", "Node.js", "M5", "fail", f"{found or 'not installed'}, {PINS['node']} needed",
                     "install Node.js 22 LTS", GUIDE["node"])

    def openspec(self) -> None:
        status, out = run(["openspec", "--version"], timeout=30)
        found = first_version(out) if status == 0 else ""
        if found and satisfies(found, PINS["openspec"]):
            self.add("openspec", "OpenSpec", "M5", "pass", found)
        else:
            self.add("openspec", "OpenSpec", "M5", "fail", f"{found or 'not installed'}, {PINS['openspec']} expected",
                     f"npm install -g @fission-ai/openspec@{PINS['openspec']}", GUIDE["node"])

    def github_cli(self) -> None:
        status, out = run(["gh", "--version"], timeout=30)
        found = first_version(out) if status == 0 else ""
        if not found or not satisfies(found, PINS["gh"]):
            self.add("github-cli", "GitHub CLI", "M7", "fail", f"{found or 'not installed'}, {PINS['gh']} needed",
                     "install the GitHub CLI", GUIDE["gh"])
            return
        if self.offline:
            self.add("github-cli", "GitHub CLI", "M7", "pass", f"{found} (sign-in not checked offline)")
            return
        status, _ = run(["gh", "auth", "status"], timeout=30)
        if status == 0:
            self.add("github-cli", "GitHub CLI", "M7", "pass", f"{found}, signed in")
        else:
            self.add("github-cli", "GitHub CLI", "M7", "fail", f"{found}, not signed in", "gh auth login", GUIDE["gh"])

    def azure_cli(self) -> None:
        if shutil.which("az"):
            self.add("azure-cli", "Azure CLI (optional)", "M7", "pass", "installed")
        else:
            self.add("azure-cli", "Azure CLI (optional)", "M7", "warn", "not installed - only the optional Azure DevOps track uses it",
                     "install it only for the Azure DevOps track", GUIDE["optional"])

    def healing(self) -> None:
        present = [name for name in HEAL_SETTINGS if os.environ.get(name) or self.dotenv.get(name)]
        if len(present) == len(HEAL_SETTINGS):
            self.add("healing", "Healing endpoint", "M8", "pass", "HEAL_MODEL, HEAL_BASE_URL and HEAL_API_KEY are set")
        else:
            missing = [name for name in HEAL_SETTINGS if name not in present]
            self.add("healing", "Healing endpoint", "M8", "warn", f"not set: {', '.join(missing)} - optional until the workshop says otherwise",
                     "add the HEAL_* settings to .env if your workshop uses an LLM for healing", GUIDE["heal"])

    def platform_support(self) -> None:
        system, machine = platform.system(), platform.machine().lower()
        tested = False
        if system == "Windows":
            tested = machine in {"amd64", "x86_64"}
        elif system == "Darwin":
            tested = version_tuple(platform.mac_ver()[0])[:1] >= (13,) and machine in {"arm64", "x86_64"}
        elif system == "Linux":
            libc, libc_version = platform.libc_ver()
            tested = machine in {"x86_64", "aarch64", "arm64"} and libc == "glibc" and version_tuple(libc_version) >= (2, 28)
        label = f"{system} {machine}"
        if tested:
            self.add("platform", "Platform", "-", "pass", label)
        else:
            self.add("platform", "Platform", "-", "warn", f"{label} is outside the tested set",
                     "see the fallback for your platform", GUIDE["platforms"])

    def run_all(self) -> list[Result]:
        self.python()
        self.locked_environment()
        self.browser_runtime()
        self.browser_launch(self.browser_binaries())
        self.container_runtime()
        self.shop_image()
        self.shop_health()
        self.space()
        self.coding_agent()
        self.robotcode_commands()
        self.robotcode_on_path()
        self.node()
        self.openspec()
        self.github_cli()
        self.azure_cli()
        self.healing()
        self.platform_support()
        return self.results


# --- output -------------------------------------------------------------------

def secret_values(dotenv: dict) -> list[str]:
    """Values of every setting whose name looks secret - to strip from any output."""
    values = [v for k, v in os.environ.items() if SECRET_NAME.search(k) and v]
    values += [v for k, v in dotenv.items() if SECRET_NAME.search(k) and v]
    return sorted({v for v in values if len(v) >= 6}, key=len, reverse=True)


def redact(text: str, secrets: list[str]) -> str:
    for value in secrets:
        text = text.replace(value, "[redacted]")
    return text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="setup-check", description="Verify the workshop environment. Read-only.")
    parser.add_argument("--json", action="store_true", help="print the full result as JSON (for the setup-problem issue)")
    parser.add_argument("--offline", action="store_true", help="skip every check that needs network access")
    args = parser.parse_args(argv)

    check = SetupCheck(offline=args.offline)
    results = check.run_all()
    counts = {s: sum(r.status == s for r in results) for s in ("pass", "warn", "fail", "skip")}
    mode = "shared" if check.shop.shared else "local"
    proxies = [n for n in ("HTTPS_PROXY", "HTTP_PROXY", "https_proxy", "http_proxy", "NO_PROXY", "no_proxy") if os.environ.get(n)]
    secrets = secret_values(check.dotenv)

    if args.json:
        report = {
            "shop": {"mode": mode, "url": check.shop.url, "space": check.shop.space, "pinned_image": f"{check.image}:{check.tag}"},
            "environment": {"python": platform.python_version(), "platform": f"{platform.system()} {platform.machine()}",
                            "offline": args.offline, "proxy_settings": proxies},
            "checks": [asdict(r) for r in results],
            "summary": counts,
        }
        print(redact(json.dumps(report, indent=2), secrets))
    else:
        space = f"space {check.shop.space}" if check.shop.space else "no space"
        lines = [f"setup-check - {mode} shop at {check.shop.url}, {space}"
                 + (f"; proxy settings: {', '.join(proxies)}" if proxies else ""), ""]
        for r in results:
            lines.append(f"  {r.status.upper():4}  {r.module:2}  {r.title:22} {r.detail}")
            if r.status in ("fail", "warn") and r.fix:
                lines.append(f"{'':12}fix:   {r.fix}")
                lines.append(f"{'':12}guide: {r.guide}")
        lines += ["", f"{len(results)} checks: {counts['pass']} passed, {counts['warn']} warnings, "
                      f"{counts['fail']} failed, {counts['skip']} skipped"]
        print(redact("\n".join(lines), secrets))
    return 1 if counts["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
