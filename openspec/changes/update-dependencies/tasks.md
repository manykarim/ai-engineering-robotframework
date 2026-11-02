# Tasks

## 1. Pins and lockfile

- [ ] 1.1 On a branch `apply-update-dependencies` from `main`, raise the pins in `pyproject.toml` to `robotcode[all]==2.8.0`, `robotframework-browser==21.0.0`, `robotframework-browser-batteries==21.0.0`, `rf-mcp[web,api]==0.36.0` and `python-dotenv==1.2.4`. Leave the other pins, the extras and the comments as they are. Verify:
  - PyPI still lists each of these as the latest stable release, and 7.5, 0.9.7 and 0.4.0 as the latest stable releases of `robotframework`, `robotframework-requests` and `robotframework-heal`. If a newer final release has appeared, take it and record it in the PR description;
  - `uv sync --locked` now fails because the lockfile is out of date (`workshop/toolchain`, *Stale lockfile*).
- [ ] 1.2 Regenerate the lockfile with `uv lock` (no `--upgrade`). Verify:
  - `uv lock --check` passes;
  - every package in `uv.lock` is a final release;
  - the packages that changed are the five pins, the RobotCode sub-packages and `grpcio`/`grpcio-tools`, as design.md lists. Explain any other change in the PR description.
- [ ] 1.3 Install the way participants do: `uv sync --locked`, then `uv run --no-sync rfbrowser install chromium`. Verify:
  - `uv run --no-sync python setup-check/check.py` passes;
  - `uv run robocop --version` prints the version that `uv.lock` records;
  - `uv run robotcode --help` lists `discover`, `libdoc`, `robot-debug`, `repl`, `results` and `analyze`.

## 2. Suite and documentation

- [ ] 2.1 Start the local shop and run the suite as CI does: `uv run robotcode robot --exclude broken`. Verify: every test passes, as it does on `main` with the old pins. If a failure comes from Browser 21, pin both Browser packages back to 20.5.0, re-lock, and say so in the PR description (design.md, Migration Plan).
- [ ] 2.2 Update `docs/robotcode.md` to the new versions, and re-run each of its examples with the shop in `clean`. Verify:
  - the header names RobotCode 2.8.0, Robot Framework 7.5 and Browser 21.0.0;
  - `uv run robotcode libdoc Browser version` prints `21.0.0`, as the document shows;
  - every other example's shortened output still matches what the command prints now;
  - no other file under `docs/`, `labs/` or `README.md` names a superseded version.
- [ ] 2.3 Add a paragraph to `README.md`, between the introduction and *Quickstart*. It links `https://manykarim.github.io/ai-engineering-robotframework/` and says the labs, the setup guide, the glossary and the guides are published there, worded so it also reads correctly on the site's home page (design.md, D7). Verify:
  - the address answers with HTTP 200, and matches `url` plus `baseUrl` in `website/docusaurus.config.js`;
  - on GitHub, the rendered README shows the link before the Quickstart (`workshop/docs-site`, *Found from the repository*);
  - the site builds locally (`npm ci` and `npm run build` in `website/`) without a broken link, and its home page shows the paragraph;
  - the existing transcripts and solutions links are unchanged.

## 3. Main

- [ ] 3.1 Run the checks and open a pull request to `main`. In its description, tell participants to run `uv sync --locked` and `uv run --no-sync rfbrowser install chromium` again, and say that `solutions` will be rebased from its tip `df84f6d`. Verify:
  - `openspec validate update-dependencies --strict` passes;
  - "Run tests" passes on the pull request.
- [ ] 3.2 Merge the pull request into `main`. Verify: `git show origin/main:pyproject.toml` has the new pins.

## 4. Solutions branch

- [ ] 4.1 Rebase `solutions` onto the new `origin/main`, without changing its commits. Verify:
  - the rebase finishes without conflicts, and `git log --oneline origin/main..solutions` shows the same 16 commit subjects in the same order;
  - `git range-diff origin/solutions...solutions` shows no change inside any lab or reference commit;
  - `git diff origin/main solutions -- pyproject.toml uv.lock docs/robotcode.md` is empty.
- [ ] 4.2 On the rebased `solutions`, install with `uv sync --locked` and `uv run --no-sync rfbrowser install chromium`, reset the shop with `uv run --no-sync python -m shop reset`, and run the whole suite with `uv run robotcode robot`, without `--exclude broken` (`workshop/solutions`, *Solutions pass*). Verify:
  - every test passes, including the two that `main` ships broken;
  - `uv lock --check` passes in `bonus/bonus-1-library` and `bonus/bonus-2-tool`.
- [ ] 4.3 Push with `git push --force-with-lease=solutions:df84f6d origin solutions`. Verify: `origin/solutions` is the rebased tip, and `git merge-base --is-ancestor origin/main origin/solutions` succeeds.

## Workflow follow-up

- Archive the change on a branch `archive-update-dependencies` after the merge. Rebase `solutions` again once the archive lands on `main`.
