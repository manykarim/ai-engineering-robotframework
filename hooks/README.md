# Hooks

Hooks are guardrails an agent cannot skip: the agent calls them itself, before or after it uses a tool. Lab 7
wires them. The four scripts are the same for every agent. Only the wiring differs.
[Hooks](../docs/hooks.md) explains how hooks work, and how to write your own.

| Script | When | What it does |
|---|---|---|
| `no_inline_locators.py` | before a file edit | Rejects an edit that adds a locator literal to a `.robot` file under `tests/`, citing convention 2 of `docs/conventions.md`. Locators already in a file do not block other edits to it. |
| `static_check.py` | after a file edit | Checks the edited `.robot` and `.resource` files under `tests/` and `resources/` with `robotcode analyze code`, without running them and without the shop, in about two seconds. A clean file gives no output; otherwise the agent gets the errors, five at most. |
| `run_affected_tests.py` | after a file edit | Runs the tests the edit affects: the edited test file, or every test file that imports the edited resource, directly or through other resources. Tests tagged `broken` are left out. The result goes back to the agent. |
| `green_before_commit.py` | before a shell command | Blocks `git commit` when `results/output.xml` is missing, older than the newest file under `tests/` or `resources/`, or holds a failed test not tagged `broken`. Every other command passes. |

`hookio.py` reads each agent's hook input and answers in the form that agent understands: it refuses an action,
reports a result, or adds context.

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

> Do these four steps in order, and after each one report exactly what happened. Do not work around anything that
> is blocked or rejected; just report it and continue with the next step.
> 1. In tests/ui/checkout.robot, add the line "    Click    css=button.buy" as the last step of the test
>    "WEB-006_AC-7 Successful Order".
> 2. In tests/ui/checkout.robot, in the test "WEB-006_AC-7 Successful Order", change the step "Place Order" to
>    "Place Ordr".
> 3. In tests/api/smoke.robot, in the test "Health Reports Ok", change the expected status value ok to okay.
> 4. Run the shell command: git commit -am "hook check"

Expected:
1. The edit is rejected, with the reason.
2. The edit is made, and the agent reports the static check's finding, `KeywordNotFound` with the line, and the
   failed tests of `tests/ui/checkout.robot`.
3. The edit is made, and the agent reports one failed test.
4. The commit is blocked because of those failures.

Undo steps 2 and 3 afterwards: `git checkout -- tests/ui/checkout.robot tests/api/smoke.robot`.

## Without an agent

Each script also runs as a plain command:

```bash
uv run --no-sync python hooks/no_inline_locators.py tests/              # every locator literal in the test files
uv run --no-sync python hooks/static_check.py tests/ resources/         # errors robotcode analyze finds
uv run --no-sync python hooks/run_affected_tests.py resources/api.resource
uv run --no-sync python hooks/green_before_commit.py --check            # may I commit now?
```

A hook that cannot read its input lets the action through and says so. A broken guardrail must not stop the agent.
