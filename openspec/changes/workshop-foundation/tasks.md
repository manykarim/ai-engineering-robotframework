## 1. Toolchain

- [x] 1.1 Rewrite `pyproject.toml` with:
  - the exact pins of design D1, including `rf-mcp[web,api]`, `robotcode[all]`, the batteries package and a direct `python-dotenv` pin;
  - `[tool.uv] package = false` and `required-version`;
  - the `[tool.workshop]` table (OpenSpec `1.13.1`, minimum Node `20.19`, and the minimum Docker, Compose and `gh` versions).

  Remove `main.py`. Verify: `uv lock` succeeds with pre-releases disallowed, and every locked package is a final release. `uv run robotcode --help` lists `discover`, `libdoc`, `robot-debug`, `repl` and `results`.
- [ ] 1.2 Commit `uv.lock`. Verify: on a fresh clone, `uv sync --locked` installs exactly the locked versions. After a direct dependency is edited in `pyproject.toml` without relocking, `uv sync --locked` fails with an out-of-date message. Revert the edit.
- [ ] 1.3 Install the browser binaries through the batteries package (design D4). Verify in a clean Linux container without Node.js on `PATH`: `uv sync --locked` followed by `uv run rfbrowser install --with-deps chromium` lets a headless Browser session open `about:blank`. Then recreate `.venv` and confirm the browser binary is gone, which proves the D4 consequence that `setup-check` must catch.
- [ ] 1.4 Verify the platforms the specs promise. Verify: `uv sync --locked`, `uv run rfbrowser install chromium` and a headless launch succeed on Windows x64 and on macOS 13 or newer on Apple silicon, with the outputs recorded in the pull request.

## 2. Shop access

- [ ] 2.1 Add `shop/compose.yaml` (design D7), pinned to the newest demo-webshop `X.Y.Z` tag at implementation time, never `edge` or `sha-`, on port 9090 with no volume. Verify:
  - after `docker compose -f shop/compose.yaml up -d`, `http://localhost:9090/health` reports that version;
  - after placing an order, `up -d --force-recreate` leaves no runtime order;
  - searching the repository for `demo-webshop:` finds this file as the only tag reference.
- [ ] 2.2 Add the variable file and the `robot.toml` profiles `local` (the default) and `shared` (design D7). Verify with a throwaway suite that is not committed, because tests belong to `baseline-suite`:
  - without settings it logs `http://localhost:9090` and no space;
  - values from `.env` are used, and the process environment wins over `.env`;
  - `-p shared` without a space stops before the first test and explains how to set one;
  - `-p shared` with `SHOP_SPACE=OctoCat` resolves to `octocat`.
- [ ] 2.3 Add the `shop` helper (`status`, `presets`, `preset`, `reset`, `wait`) with the header rule and the neutral status (design D8). Verify locally, and on the shared instance in a throwaway test space that is reset afterwards and is never `default`:
  - `preset stage2` makes the status name `stage2`;
  - `preset buggy` then names `stage2` and `buggy`, and no `BUG_` string appears in the output;
  - `reset` brings back a status naming `clean`;
  - with the shared URL and no space, `preset` sends no request (checked against a local listener standing in for the shop) and explains `SHOP_SPACE`;
  - `wait` returns once `/health` answers, and fails after its timeout when nothing listens.

## 3. setup-check

- [ ] 3.1 Implement `setup-check/check.py` with the checks, severities and modules of design D9. It reads expected versions only from `uv.lock`, `[tool.workshop]` and `shop/compose.yaml`. Verify: on a correctly prepared machine, every check passes or warns and the exit status is 0. On a copy of the repository, changing a pin in its source changes the expectation without any edit to `check.py`.
- [ ] 3.2 Stage each known pitfall on its own and restore the environment after each one. Verify that each is reported with its fix and setup guide reference:
  - Robot Framework 7.4 installed into the environment fails, naming both versions;
  - `rfbrowser init` run on top of the batteries package fails and prints the removal command. Record the exact marker that tells the two installs apart in the check;
  - browsers missing after `.venv` is recreated fail with the install command;
  - a global `robotcode` first on `PATH` warns and names both installations;
  - a stopped shop fails with the start command, and the shop stays stopped;
  - the shared URL without a space fails;
  - space `-bad--name-` fails with the format;
  - a missing Azure CLI warns while the exit status stays 0.
- [ ] 3.3 Add `--json` and `--offline`. Verify: with a planted `HEAL_API_KEY=sk-test-DO-NOT-LEAK`, both the text and the JSON output report the key as present and neither contains the value. `--offline` without network access reports the network checks as skipped, and the exit status reflects only the local checks.
- [ ] 3.4 Confirm the check is read-only. Verify: `git status`, `docker ps -a` and the environment's list of installed distributions are identical before and after a full run.

## 4. Agent context

- [ ] 4.1 Write `AGENTS.md` (under 30 lines, with the content of design D10) and `CLAUDE.md` (a single `@AGENTS.md` import). Verify:
  - `wc -l AGENTS.md` is below 30;
  - the file names none of the conventions or RobotCode habits taught in Labs 2 to 4;
  - Claude Code started in the repository root shows the content of `AGENTS.md` in its loaded memory;
  - Codex and GitHub Copilot each load `AGENTS.md`. Should Copilot not, add a pointer-only `.github/copilot-instructions.md` and check again.
- [ ] 4.2 Generate the OpenSpec integrations with `openspec init --tools claude,codex,github-copilot` at OpenSpec `1.13.1`, and commit the generated files. Verify: `openspec --version` prints `1.13.1`, and each of the three tools offers explore, propose, apply and archive.
- [ ] 4.3 Add the namespace `context` and the `rules.specs` neutrality rule, scoped to `shop/*`, to `openspec/config.yaml` (design D10). Verify: `openspec instructions specs --change workshop-foundation --json` returns both the context and the rule, and `openspec validate --all --strict` passes.
- [ ] 4.4 Check secret hygiene. Verify:
  - a secret scan (gitleaks or equivalent) over the tracked tree finds nothing;
  - `git check-ignore .env` confirms the maintainer's local `.env`, which holds deployment tokens, is ignored;
  - `.env.example` lists setting names only.

## 5. Documents

- [ ] 5.1 Rewrite `README.md` with the five-command quickstart and the link to `SETUP.md` (design D11). Verify: the quickstart matches the setup guide command for command.
- [ ] 5.2 Write `SETUP.md` with every section design D11 lists, including a version-bump procedure that names the files to change together. Verify: every prerequisite carries a minimum version and a first module, and every setup guide reference printed by `setup-check` resolves to an existing heading, checked programmatically.
- [ ] 5.3 Add `.env.example` and extend `.gitignore` (design D11). Verify: `.env.example` contains names without values, and `git check-ignore` confirms that Robot Framework output files, a healing report directory and `node_modules/` are ignored.

## 6. Clean-room verification and close-out

- [ ] 6.1 Run the whole onboarding from nothing. In a fresh Linux container with no Node.js, no RobotCode and no browsers, follow `README.md` and `SETUP.md` exactly, installing Node.js and OpenSpec as the guide says. Verify:
  - `setup-check` reports no failure in shared mode, with a throwaway test space that is reset afterwards;
  - it also reports no failure in local mode against the shop started from `shop/compose.yaml` on the host;
  - both outputs are recorded in the pull request.
- [ ] 6.2 Validate and archive. Verify: `openspec validate workshop-foundation --strict` passes. After the merge, `openspec archive workshop-foundation -y` creates `openspec/specs/workshop/toolchain`, `setup-check`, `shop-access` and `agent-context` as main specs, each with its Purpose filled in.
