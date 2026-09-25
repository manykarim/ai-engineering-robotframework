# Lab 0 - Arrival: the recorded walkthrough

*Recorded with Claude Code 2.1.281, from the lab's instructions. Results are shortened; your agent's answers will differ in wording.*

## Steps 1-2 - Fork and clone

The rehearsal starts in a fresh clone, as your fork would be after `git clone`.

## Step 3 - Install

**The participant runs** `uv sync --locked`:

```
 + watchfiles==1.3.0
 + wcwidth==0.8.5
 + websocket-client==1.9.2
 + websockets==17.1
 + wrapt==2.4.1
 + wsproto==1.3.2
```

**The participant runs** `uv run --no-sync rfbrowser install chromium`:

```
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                |  80% of 114.3 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■        |  90% of 114.3 MiB
|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■| 100% of 114.3 MiB
Chrome Headless Shell 153.0.8010.12 (playwright chromium-headless-shell v1243) downloaded to <scratch>
```

## Step 4 - Start the shop

**The participant runs** `docker compose -f shop/compose.yaml up -d`:

```
 Container shop-shop-1  Running
```

## Step 5 - Check everything

**The participant runs** `uv run --no-sync python setup-check/check.py`:

```
setup-check - local shop at http://localhost:9090, no space

  PASS  M0  Python                 3.12.11, as .python-version pins 3.12
  PASS  M0  Locked environment     every installed package matches uv.lock
  PASS  M0  Browser runtime        bundled Node runtime, no separate Node dependencies
  PASS  M0  Browser binaries       chromium-1243, chromium_headless_shell-1243
  PASS  M0  Headless browser       Chromium opened about:blank
  PASS  M0  Container runtime      Docker 23.0.1, Compose 2.16.0
  PASS  M0  Shop image             ghcr.io/manykarim/demo-webshop:0.3.0
  PASS  M0  Shop health            http://localhost:9090 answers, version 0.3.0
  PASS  M0  Workshop space         none needed for the local shop
  PASS  M2  Coding agent           claude 2.1.281, codex 0.156.1, copilot 1.0.88
... (14 more lines)
```

## Step 7 - The shop's state

**The participant runs** `uv run --no-sync python -m shop status`:

```
shop     http://localhost:9090  (version 0.3.0)
space    default
presets  clean, stage1
```

## Step 8 - Run the suite once

**The participant runs** `uv run robotcode robot`:

```
WEB-002_AC-10 Reset Filters :: "Reset" clears every filter and bri... | PASS |
------------------------------------------------------------------------------
WEB-002_AC-12 Handpicked Highlights :: "Handpicked highlights" sho... | FAIL |
The highlights should show the three highest prices, highest first.
------------------------------------------------------------------------------
Tests.Ui.Catalogue :: The products page, /products (spec: shop/cat... | FAIL |
7 tests, 5 passed, 2 failed
==============================================================================
Tests.Ui.Checkout :: Checkout, /checkout (spec: shop/checkout). Every test ...
==============================================================================
WEB-006_AC-1 Order Total Adds Up :: The order total is subtotal pl... | PASS |
------------------------------------------------------------------------------
... (18 more lines)
```

## Step 9 - Read the result

**The participant runs** `uv run robotcode results summary`:

```
# Summary — results/output.xml

- _Status:_ ❌ **FAIL**
- _Total:_ 13
- _Passed:_ 11
- _Failed:_ 2
- _Skipped:_ 0
- _Started:_ 2026-09-24 21:47:42
- _Ended:_ 2026-09-24 21:48:05
- _Elapsed:_ 23.11 s
- _Messages:_ 2 FAIL
```

**The participant runs** `uv run robotcode results show --failed`:

```
# Show — results/output.xml

- ❌ **FAIL** Tests.Ui.Catalogue.WEB-002_AC-4 Rating Filter (`tests/ui/catalogue.robot:46`) _(21:47:46 · 10.28 s)_
  > TimeoutError: locator.elementHandle: Timeout 10000ms exceeded.
- ❌ **FAIL** Tests.Ui.Catalogue.WEB-002_AC-12 Handpicked Highlights (`tests/ui/catalogue.robot:76`) _(21:48:01 · 266 ms)_
  > The highlights should show the three highest prices, highest first.

## Statistics

- _Total:_ 2
- _Passed:_ 0
- _Failed:_ 2
... (6 more lines)
```

## Step 10 - Start your agent

**Prompt:**

> What is this repository, and how do I run its tests?

*The agent runs `ls -A && echo --- && cat robot.toml 2>/dev/null && echo --- && git ls-files | grep -E '\.robot$|\.resource$' | head -50`*

```
.agents
.claude
.env.example
.git
.github
.gitignore
.python-version
.venv
AGENTS.md
CLAUDE.md
GLOSSARY.md
LICENSE
... (56 more lines)
```

*The agent runs `head -40 README.md && echo --- && ls labs tests tests/* && echo --- && cat shop/compose.yaml`*

```
# Agentic Engineering with Robot Framework

The participant repository of the workshop *Agentic Engineering with Robot Framework: From a Markdown File to
a Self-Healing Pipeline*. Over one day, you climb the agentic maturity ladder: context, skills, tooling, live
access, orchestration. Every rung works on its own, and you leave with your own working setup.

The system under test is a small demo shop that runs from a published container image.

## Quickstart

With the [prerequisites](SETUP.md#prerequisites) installed:

... (67 more lines)
```

*The agent runs `ls tools && grep -ril "expected outcome" tools docs openspec 2>/dev/null | head`*

```
check_labs.py
transcript.py
verify_outcomes.py
openspec/changes/archive/2026-09-24-baseline-suite/tasks.md
```

*The agent runs `head -40 tools/verify_outcomes.py`*

```
"""Check docs/facilitator/suite-outcomes.toml against the pinned shop (spec: workshop/baseline-suite).

    uv run --no-sync python tools/verify_outcomes.py [--heal] [--preset NAME ...] [--data PATH] [--keep DIR]

For every preset: apply it through the shop helper, run the unmodified suite with
RobotCode, and compare the failing tests with the data. It works in whichever mode
SHOP_URL and SHOP_SPACE select, and always resets the space when it finishes.
Exits with status 1 on any difference.

--heal checks drift_and_bug with the heal profile instead, and leaves out the tests
tagged broken, as Module 8 does. It needs a healing model (HEAL_MODEL or
HEAL_LOCATOR_MODEL, in the environment or .env); without one, robotframework-heal
... (28 more lines)
```

*The agent runs `head -40 docs/facilitator/suite-outcomes.toml`*

```
# Which tests of the shipped suite fail under each preset, and why.
# Derived from the test inventory (baseline-suite design D1) and the shop's drift
# and defect tables; checked against the pinned shop by tools/verify_outcomes.py.
#
# A test that is not listed under a preset is expected to pass.
# Reasons: "broken" (fails on purpose), "drift:<kind>" (its locator kind drifts
# in this preset: id, class or data-test), "defect:<criterion>" (a planted defect
# breaks the criterion the test verifies).

# Every test of the suite and the kind of locator its one fragile element uses
# (design D1): "stable" (the stable contract only), "id", "class", "data-test",
# "api", or "broken". A test added to the suite must be added here.
... (28 more lines)
```

**Agent:**

This is the participant repo for a one-day workshop, **"Agentic Engineering with Robot Framework"**. Over nine labs in `labs/`, you set up coding agents for a Robot Framework test suite, one step at a time: project context, skills, RobotCode, MCP, hooks, self-healing and CI. The suite tests a small demo shop that runs from a published Docker image (`ghcr.io/manykarim/demo-webshop:0.3.0`, pinned in `shop/compose.yaml`).

## What's in it

- **`tests/`**: 13 tests. `tests/api/smoke.robot` has two API checks. `tests/ui/catalogue.robot` and `tests/ui/checkout.robot` are browser tests.
- **`resources/`**: the keywords the tests use. `docs/conventions.md` describes how tests are written here.
- **`robot.toml`**: the run settings, with three profiles: `local` (the default), `shared` and `heal`.
- **Lab material**: `skills/`, `hooks/`, `agents/` and `mcp/` hold what the labs install. `openspec/` holds specs, and `tools/` holds maintainer checks.

## Running the tests

1. **Install** (once):
   ```bash
   uv sync --locked
   uv run --no-sync rfbrowser install chromium
   uv run --no-sync python setup-check/check.py   # checks the setup and prints a fix for anything missing
   ```
2. **Start the shop.** It runs at `http://localhost:9090`:
   ```bash
   docker compose -f shop/compose.yaml up -d
   ```
   Without Docker, you can use the shared instance instead. Set `SHOP_URL` and `SHOP_SPACE` (your GitHub handle) in `.env`, starting from `.env.example`.
3. **Run the suite:**
   ```bash
   uv run robotcode robot              # whole suite, local shop
   uv run robotcode robot tests/ui     # one folder or file
   uv run robotcode -p shared robot    # against the shared instance
   ```
   Results go to `results/`.

**Use `robotcode robot`, not plain `robot`.** Plain `robot` ignores `robot.toml`, so it won't find the shop URL, the variable file or the preflight check. The preflight check stops the run before the first test if the shop settings can't work.

## Some failures are intentional

The README calls the suite "deliberately imperfect." Even on a clean shop, two tests fail by design:
- `WEB-002_AC-4 Rating Filter`
- `WEB-002_AC-12 Handpicked Highlights`

Other shop presets add broken locators or planted bugs, which make more tests fail. `docs/facilitator/suite-outcomes.toml` lists the expected failures for each preset. To see or change the shop's current preset, run `uv run --no-sync python -m shop status`.

I only read the repo and didn't run anything, so I haven't checked whether the shop is running or the suite passes on your machine.
