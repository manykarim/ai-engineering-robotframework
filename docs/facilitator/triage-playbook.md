# Triage playbook

*Facilitator material, for the co-host.* When a participant is stuck, ask for the output of

```bash
uv run --no-sync python setup-check/check.py
```

and find the red or yellow line below. Each check prints its own fix and a link into `SETUP.md`. This page adds what
to do when the fix does not work, and when to stop trying.

## The rule of the room

**Ten minutes, then move.** If a participant is not green ten minutes into Module 0, move them to the shared instance
(no Docker needed) or pair them with a neighbour. They can finish the setup in a break. Nobody debugs a laptop
while the room waits.

## By check, in the order they usually fail

| Check | Typical cause | Fix | If that fails |
|---|---|---|---|
| **Container runtime** | Docker Desktop not started; on Linux, the user is not in the `docker` group | start Docker; `sudo usermod -aG docker $USER`, then log in again | Shared instance: create `.env` with `SHOP_URL` and `SHOP_SPACE` |
| **Shop image** | The image pull was blocked by a proxy, or never ran | `docker compose -f shop/compose.yaml pull` | Shared instance |
| **Shop health** | The shop container is still starting, or port 9090 is taken | wait a minute and rerun; `docker compose -f shop/compose.yaml ps`; free the port | Shared instance |
| **Workshop space** | `SHOP_SPACE` missing or not a GitHub handle, with `SHOP_URL` set to the shared instance | set `SHOP_SPACE=<handle>` in `.env` | Give them a handle-shaped name of their choice |
| **Browser binaries** | `rfbrowser install chromium` not run, or run in another environment | `uv run --no-sync rfbrowser install chromium` | Pair |
| **Headless browser** | Missing system libraries on Linux | `uv run --no-sync rfbrowser install --with-deps chromium` (needs sudo) | Pair |
| **Locked environment** | Installed without `--locked`, or packages added by hand | `uv sync --locked` | Delete `.venv` and run the install again |
| **Browser runtime** | `rfbrowser init` was run instead of `install`, or the batteries package is missing | `uv sync --locked`, then `uv run --no-sync rfbrowser install chromium` | Delete `.venv`, install again |
| **Python** | uv picked another interpreter | `uv python install 3.12`, then `uv sync --locked` | Pair |
| **Coding agent** | No agent on `PATH`, or installed in another shell | install one per its vendor, open a new terminal | Pair with someone whose agent works; the transcripts carry the rest |
| **Node.js**, **OpenSpec** | Node older than 20.19, or OpenSpec not installed at the pinned version | install Node 22 LTS; `npm install -g @fission-ai/openspec@1.13.1` | Lab 5 works in pairs: one OpenSpec per pair |
| **GitHub CLI** | Not installed, or not signed in | `gh auth login` | Lab 7's issue can be filed in the browser instead |
| **RobotCode commands** | The environment is out of date | `uv sync --locked` | Pair |
| **RobotCode on PATH** (warning) | A global RobotCode from pipx or `uv tool` shadows the project's | always use `uv run robotcode` | Nothing to do if they use `uv run` |
| **Healing endpoint** (warning) | No `HEAL_*` settings | expected unless the workshop hands out keys | Lab 8's recorded report |
| **Azure CLI** (warning) | Not installed | optional | Nothing to do |
| **Platform** (warning) | Windows on Arm, macOS before 13, or an old or non-glibc Linux | the fallback in `SETUP.md`, *Platforms*: `rfbrowser init` with Node.js | Shared instance and pairing; the browser labs need a working Browser Library |

## Not caught by the check

- **Agent sign-in or quota fails mid-day.** The lab's *If your agent fails* section points to its transcript. The
  participant follows it and rejoins at the next module. Modules 2 to 4 need the least cloud access: the safe
  harbour.
- **"Mine looks different."** Expected: agents are non-deterministic. Ask them to keep both results for the debrief.
- **The suite fails more than the two `broken` tests in Module 0.** Check `uv run --no-sync python -m shop status`:
  a preset other than `clean` is on. `uv run --no-sync python -m shop reset` fixes it.
- **Hooks or MCP do nothing in Copilot or Codex.** The folder, or the hooks, are not trusted yet. Start the agent
  interactively in the repository once and accept.
- **Codex cannot reach the shop from a test run.** Its sandbox blocks network access; see `docs/environments.md`.
- **A corporate proxy blocks the agent.** Nothing to fix on the day: pair them, and give them the transcripts.
