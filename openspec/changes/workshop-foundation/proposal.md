## Why

The participant repository is an empty scaffold: one master preparation document, an OpenSpec skeleton and a hello-world `main.py`. Every lab, the shipped suite and the CI workflows depend on each participant having the same working environment, and the master document names version drift as the first cause of workshop-day chaos. The stack has been shown to resolve together, 150 packages on Python 3.12, but only with `rf-mcp[web,api]`: the `rf-mcp[all]` extra used by the earlier RBCN workshop cannot resolve, because it pins a desktop-automation pre-release (and would also pull Django, `sentence-transformers` and PyTorch). This change lays the ground every later change builds on.

## What Changes

- **A pinned, locked toolchain.** `pyproject.toml` pins `robotframework==7.5`, `robotframework-browser==20.5.0` with `robotframework-browser-batteries==20.5.0`, `robotframework-requests==0.9.7`, `robotcode[all]==2.7.0`, `rf-mcp[web,api]==0.35.0` and `robotframework-heal==0.4.0`, on Python 3.12, with `uv.lock` committed and `uv sync --locked` as the only install command. The master document's `requirements.txt` and `pip install` are replaced by uv. `robotcode` lives in the project environment, never pipx or uvx, because its discovery must resolve the project's own libraries.
- **Non-Python prerequisites, named and pinned**: Docker (to run the shop locally), Node.js 20.19 or newer (the OpenSpec CLI is an npm package and Module 5 depends on it), OpenSpec `1.13.1`, `gh`, and one supported coding agent. Browser Library's own Node toolchain is *not* a prerequisite: the batteries package ships a Node runtime, so the fragile `rfbrowser init` step is replaced by `rfbrowser install chromium`.
- **`setup-check`**: one command that verifies the whole environment - versions, not just presence - and prints a fix for every failure. It catches the mistakes seen before: `robotcode` resolving outside the project environment, `rfbrowser init` run on top of the batteries package, and missing browser binaries after the virtual environment was recreated (Playwright installs them *inside* `.venv`).
- **Access to the system under test.** The shop is not in this repository (the master document's `demo-shop/` folder): it is the published image `ghcr.io/manykarim/demo-webshop`, pinned to one version tag in one place. Local Docker is the default; the shared instance at `https://demoshop.makrocode.de` is the fallback, used with the participant's GitHub handle as workshop space. `SHOP_URL` and `SHOP_SPACE` are the whole contract, read by `robot.toml` profiles (`local`, `shared`) and by a small `shop` helper for status, presets and resets.
- **Agent context, deliberately thin.** `AGENTS.md` is the single context file and starts nearly empty, because Lab 2 builds it. `CLAUDE.md` imports it; Codex and Copilot read it natively. OpenSpec is initialised for Claude Code, Codex and GitHub Copilot, so Module 5 works for every agent the workshop supports. `openspec/config.yaml` names the two spec namespaces: `shop/*` describes the system under test, `workshop/*` describes this repository.
- **Onboarding documents**: `README.md` (what this is, the five-command quickstart), `SETUP.md` (the full guide sent a week before the workshop, including the corporate-proxy note for `cdn.playwright.dev`, `ghcr.io` and npm, and the API-key cost warning) and `.env.example`.
- The scaffold's `main.py` is removed.

## Capabilities

### New Capabilities
- `workshop/toolchain`: the pinned Python stack, the named non-Python prerequisites and the single install path.
- `workshop/setup-check`: the one-command environment verification and what it must detect.
- `workshop/shop-access`: how every tool in the repository reaches the shop - pinned image, local and shared modes, the `SHOP_URL`/`SHOP_SPACE` contract, profiles and the `shop` helper.
- `workshop/agent-context`: `AGENTS.md` as the single, deliberately thin context file, the agent pointers, and the OpenSpec configuration for three agents and two namespaces.

### Modified Capabilities
None. The repository has no specs yet.

## Impact

- **New files**: `pyproject.toml` (rewritten), `uv.lock`, `robot.toml`, `setup-check/`, `shop/` (compose file and helper), `AGENTS.md`, `CLAUDE.md`, `README.md` (rewritten), `SETUP.md`, `.env.example`, `.gitignore` additions, the OpenSpec agent integrations for Codex and Copilot, `openspec/config.yaml` context.
- **Removed**: `main.py`.
- **Depends on** the published demo-webshop image; nothing in this repository builds the shop.
- **Unblocks** `shop-specs` (namespaces and neutrality rule), `baseline-suite` (profiles, shop contract), `workshop-labs` (setup-check, agent context) and `ci-and-site` (install path).
- **Not in scope**: any test, lab, spec of shop behaviour, workflow or site - each belongs to a later change.
