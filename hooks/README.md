# Hooks

Hooks are guardrails an agent cannot skip: the agent calls them itself, before or after it uses a tool. Lab 7
wires them. The three scripts are the same for every agent. Only the wiring differs.

| Script | When | What it does |
|---|---|---|
| `no_inline_locators.py` | before a file edit | Rejects an edit that adds a locator literal to a `.robot` file under `tests/`, citing convention 2 of `docs/conventions.md`. Locators already in a file do not block other edits to it. |
| `run_affected_tests.py` | after a file edit | Runs the tests the edit affects: the edited test file, or every test file that imports the edited resource, directly or through other resources. Tests tagged `broken` are left out. The result goes back to the agent. |
| `green_before_commit.py` | before a shell command | Blocks `git commit` when `results/output.xml` is missing, older than the newest file under `tests/` or `resources/`, or holds a failed test not tagged `broken`. Every other command passes. |

`hookio.py` reads each agent's hook input and answers in the form that agent understands.

## Wiring

Copy the file for your agent into place. If the target file already exists, merge the `hooks` section by hand.

| Agent | Copy | To |
|---|---|---|
| Claude Code | `hooks/claude-code.settings.json` | `.claude/settings.json` |
| Codex | `hooks/codex.hooks.json` | `.codex/hooks.json` |
| GitHub Copilot | `hooks/copilot.hooks.json` | `.github/hooks/workshop.json` |

Then start your agent in the repository root. Each agent reads only its own wiring, and runs a repository's hooks
only once you trust them:

- **Claude Code** runs them once you have trusted the folder, which it asks about on first start. `/hooks` lists
  what is active.
- **Codex** asks you to trust the project's hooks the first time it meets them. Accept.
- **GitHub Copilot** asks whether you trust the folder the first time you start it there. Answer yes. Hooks never run
  in a folder you did not trust.

Copilot and Codex edit files through patches when they use a GPT model. The wiring covers that too (`apply_patch`).

## Try them

Give your agent this prompt:

> Do these three steps in order, and after each one report exactly what happened. Do not work around anything that
> is blocked or rejected; just report it and continue with the next step.
> 1. In tests/ui/checkout.robot, add the line "    Click    css=button.buy" as the last step of the test
>    "WEB-006_AC-7 Successful Order".
> 2. In tests/api/smoke.robot, in the test "Health Reports Ok", change the expected status value ok to okay.
> 3. Run the shell command: git commit -am "hook check"

Expected:
1. The edit is rejected, with the reason.
2. The edit is made, and the agent reports one failed test.
3. The commit is blocked because of that failure.

Undo step 2 afterwards: `git checkout -- tests/api/smoke.robot`.

## Without an agent

Each script also runs as a plain command:

```bash
uv run --no-sync python hooks/no_inline_locators.py tests/              # every locator literal in the test files
uv run --no-sync python hooks/run_affected_tests.py resources/api.resource
uv run --no-sync python hooks/green_before_commit.py --check           # may I commit now?
```

A hook that cannot read its input lets the action through and says so. A broken guardrail must not stop the agent.
