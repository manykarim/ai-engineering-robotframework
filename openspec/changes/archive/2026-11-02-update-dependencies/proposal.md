# Proposal

## Why

Several direct dependencies have newer stable releases than the versions `pyproject.toml` pins: RobotCode 2.8.0,
Browser Library 21.0.0 (with Node.js 26 LTS in BrowserBatteries), rf-mcp 0.36.0 and python-dotenv 1.2.4.
Participants should work with current releases, and `main` should carry them before the next workshop run. In the
same pass, the README should point participants to the published documentation, which it does not do today.

## What Changes

- Raise the exact pins in `pyproject.toml` to the latest stable release of every direct dependency that has one:

  | Package | Pinned | New |
  |---|---|---|
  | `robotcode[all]` | 2.7.0 | 2.8.0 |
  | `robotframework-browser` | 20.5.0 | 21.0.0 |
  | `robotframework-browser-batteries` | 20.5.0 | 21.0.0 |
  | `rf-mcp[web,api]` | 0.35.0 | 0.36.0 |
  | `python-dotenv` | 1.2.3 | 1.2.4 |

- Keep `robotframework==7.5`, `robotframework-requests==0.9.7` and `robotframework-heal==0.4.0`: each is already the
  latest stable release. Robot Framework stays on 7.5 although the request named it.
- Regenerate `uv.lock`. Pre-releases stay disallowed, and the extras stay as they are.
- **BREAKING** for anyone who reuses an environment: Browser 21.0.0 is a major release. Upstream calls it
  backwards incompatible because BrowserBatteries now ships Node.js 26 LTS. Keywords are not removed. Participants
  must run `uv sync --locked` and `uv run --no-sync rfbrowser install chromium` again.
- Update `docs/robotcode.md`: its header and its example output name the pinned versions.
- The change lands on `main` through a pull request, as every change in this repository does.
- Link the published documentation, `https://manykarim.github.io/ai-engineering-robotframework/`, from `README.md`.
  Today the README links the site's transcripts and solutions but never the site itself, so participants find the
  labs, setup guide and glossary only as files. `README.md` is also the site's home page, so the sentence has to read
  correctly in both places.
- Rebase the `solutions` branch onto the new `main`, as `workshop/solutions` (*Kept current with main*) requires, so
  it pins exactly the same versions. Its lab and reference commits stay as they are. The rebase also brings over
  the triage fix that `main` gained in #34.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `workshop/docs-site`: adds *Found from the repository*. `README.md` links the published site and says what is there.

The version bump changes no requirement. `workshop/toolchain` requires a locked environment, exact pins, stable
releases only and a named tool set, but names no version. `workshop/solutions` already requires the branch to be
rebased onto `main` and to pass.

## Impact

- `pyproject.toml`, `uv.lock`: five direct pins change. Transitively, the RobotCode sub-packages move to 2.8.0, and
  `grpcio` and `grpcio-tools` move to 1.85.0. A trial re-lock in a scratch copy changed nothing else.
- `docs/robotcode.md`: the version line, and the output of `libdoc Browser version`.
- `README.md`: one new paragraph above *Quickstart*. The docs site rebuilds from `main`, so its home page shows it after
  the merge.
- CI: the `.venv` cache key hashes `uv.lock`, so the first run after the change builds a fresh environment.
- Participants: their next `uv sync --locked` installs the new versions; the browser has to be installed again.
- `solutions` branch: rebased and force-pushed. None of its 16 commits touches the root `pyproject.toml`, `uv.lock`
  or `docs/robotcode.md`, so the new pins come over without conflicts. Anyone who has checked out `solutions` must
  reset it to `origin/solutions`; comparing with `git diff main..origin/solutions` keeps working.
- Unchanged on `solutions`: the Bonus 1 and Bonus 2 projects under `bonus/` have their own lockfiles. Their pins
  (`robotframework==7.5`, `requests==2.34.2`, `robotframework-assertion-engine==5.0.1`,
  `robotframework-pythonlibcore==4.6.0`) are already the latest stable releases. Archived changes and transcripts
  that name the old versions are historical records and are not edited.
