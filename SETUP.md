# Setup

Set up your machine **before the workshop day**. It takes about twenty minutes,
most of it downloads. When you are done, one command tells you whether
everything will work on the day:

```bash
uv run --no-sync python setup-check/check.py
```

If anything stays red, see [If something stays red](#if-something-stays-red).

## Prerequisites

Python is not on this list: uv installs Python 3.12 for the project.

| What | Minimum | Needed from | Notes |
|---|---|---|---|
| [uv](https://docs.astral.sh/uv/getting-started/installation/) | 0.8.15 | Module 0 | Already installed? Run `uv self update`. |
| Docker Engine with Compose v2 | 20.10, Compose 2.0 | Module 0 | Runs the shop locally. No Docker allowed at work? Use [the shared instance](#the-shared-instance). |
| A coding agent | current release | Module 2 | Agents update themselves; no lab depends on a specific version. See [Coding agent](#coding-agent). |
| Node.js | 20.19 | Module 5 | 22 LTS recommended. Needed by OpenSpec. |
| OpenSpec | 1.13.1 | Module 5 | See [Node.js and OpenSpec](#nodejs-and-openspec). |
| GitHub CLI (`gh`) | 2.40, signed in | Module 7 | See [GitHub CLI](#github-cli). |
| Azure CLI, Jira Cloud | - | Module 7 | Optional tracks only. See [Optional tracks](#optional-tracks). |

## Install

1. Fork this repository on GitHub, then clone **your fork**. Lab 9 runs GitHub Actions on it.
2. Install the pinned Python environment:

   ```bash
   uv sync --locked
   ```

   Every package comes from `uv.lock`, at exactly the version the workshop was tested with. If uv reports that
   its version does not match, run `uv self update`. Do not install anything with `pip`.

## Browsers

Install the browser the tests use:

```bash
uv run --no-sync rfbrowser install chromium
```

On Linux, add `--with-deps` to install the system libraries Chromium needs (this asks for `sudo`).

- **Never run `rfbrowser init`.** This project uses Browser Library's batteries package, which brings its own
  Node.js runtime. `rfbrowser init` installs a second, separate set of Node packages on top of it. If you ran it,
  undo it with `uv run --no-sync rfbrowser clean-node`, then install the browser again.
- **The browser lives inside `.venv`.** If you delete or recreate `.venv`, install the browser again.

## The local shop

The system under test is the demo shop, pinned to one version in `shop/compose.yaml`.

```bash
docker compose -f shop/compose.yaml up -d                  # start: http://localhost:9090
docker compose -f shop/compose.yaml up -d --force-recreate # a freshly seeded shop
docker compose -f shop/compose.yaml down                   # stop
```

Restarting keeps the shop's data; recreating reseeds it. `uv run --no-sync python -m shop status` shows the
version and what is active.

## The shared instance

If you cannot run Docker, use the shared workshop instance instead. Put two lines in `.env` (copy
`.env.example` to start):

```bash
SHOP_URL=https://demoshop.makrocode.de
SHOP_SPACE=your-github-handle
```

Everyone on the shared instance works in their own **space**, named after their GitHub handle, so your presets,
cart and orders never affect anyone else. Run tests with the shared profile:

```bash
uv run robotcode -p shared robot <path>
```

Without a space, the run stops before its first test and tells you what to set.

## Coding agent

The workshop is demonstrated with **Claude Code**. **Codex** and **GitHub Copilot** work for every lab. Install
one and sign in before the workshop, following its vendor's instructions.

| Agent | Spec-driven workflow in Module 5 |
|---|---|
| Claude Code | `/opsx:propose`, `/opsx:apply`, `/opsx:archive`, `/opsx:explore` |
| Codex | `$openspec-propose` and the other `openspec-*` skills |
| GitHub Copilot | `/opsx-propose` and the other `opsx-*` prompts |

`AGENTS.md` is the project context every agent reads; `CLAUDE.md` only imports it.

## RobotCode

Always run RobotCode through uv: `uv run robotcode ...`. That is the RobotCode installed in this project, which
sees the project's libraries at their pinned versions. A RobotCode installed globally (with pipx or
`uv tool`) cannot see them. `setup-check` warns if one would start when you type `robotcode` alone.

## Node.js and OpenSpec

Install Node.js 22 LTS (at least 20.19), then OpenSpec at the pinned version:

```bash
npm install -g @fission-ai/openspec@1.13.1
openspec --version   # 1.13.1
```

## GitHub CLI

Install the [GitHub CLI](https://cli.github.com/) and sign in with `gh auth login`. Module 7 files an issue with
it, and Module 9 runs on your fork.

## Optional tracks

- **Azure CLI** (`az`), for the Azure DevOps variant of Module 7.
- **A free Jira Cloud site**, for the Jira stretch goal of Module 7.

Skip both if you do not use them at work; `setup-check` only warns.

## Healing API key

Module 8 heals drifted locators with `robotframework-heal`. The facilitators will tell you before the workshop
whether your workshop needs an LLM for it. If it does, add three settings to `.env`:

```bash
HEAL_MODEL=...
HEAL_BASE_URL=...
HEAL_API_KEY=...
```

**Set a spending cap on the key before you use it.** An agent or a healing run can make many requests quickly.
Never commit `.env`, and never paste its content into an issue.

## Platforms

Tested: Windows x64, macOS 13 or newer (Apple silicon and Intel), and Linux x64 and arm64 with glibc 2.28 or
newer. On other platforms (for example Windows on Arm, or macOS before 13), the batteries package has no build:
remove `robotframework-browser-batteries` from your environment and run `rfbrowser init` instead, which needs
Node.js and npm. Tell the facilitators before the workshop.

## Corporate proxies

Set `HTTPS_PROXY` (and `NO_PROXY=localhost,127.0.0.1`) before installing. The setup downloads from:

- `pypi.org` and `files.pythonhosted.org` (Python packages)
- `github.com` and `*.githubusercontent.com` (Python itself, via uv)
- `ghcr.io` and `pkg-containers.githubusercontent.com` (the shop image)
- `registry.npmjs.org` (OpenSpec)
- `cdn.playwright.dev` and `playwright.download.prss.microsoft.com` (Chromium)
- `demoshop.makrocode.de` (the shared instance)

## Check everything

```bash
uv run --no-sync python setup-check/check.py            # the full check
uv run --no-sync python setup-check/check.py --offline  # without network access
```

Keep `--no-sync`: plain `uv run` would repair the environment before checking it, and hide what is wrong.
Every failed check prints a fix and the section of this guide to read.

## If something stays red

Open an issue in this repository and paste the output of:

```bash
uv run --no-sync python setup-check/check.py --json
```

The output never contains your keys or tokens. Before the workshop there is also an optional drop-in setup call.

## For maintainers: changing a pinned version

Change these together, in one pull request:

1. The pin in `pyproject.toml` (`[project]` dependencies, or `[tool.workshop]` for tools outside Python), then
   `uv lock`.
2. The shop tag in `shop/compose.yaml`: always a version tag, never `edge` or `sha-...`.
3. The numbers in this guide's prerequisites table.

`setup-check` reads its expectations from `uv.lock`, `[tool.workshop]` and `shop/compose.yaml`, so it needs no
edit. Run it afterwards on a clean machine.
