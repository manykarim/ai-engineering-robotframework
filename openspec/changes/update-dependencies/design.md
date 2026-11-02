# Design

## Context

See proposal.md for why. `pyproject.toml` pins every direct dependency exactly, and `uv.lock` resolves them with
`prerelease = "disallow"`. The `workshop/toolchain` spec requires both. setup-check reads expected versions from
`uv.lock`, not from a copy of them, and CI caches `.venv` under a key that hashes `uv.lock`. So after the bump, only
`pyproject.toml`, `uv.lock` and the one document that quotes versions need to change.

Latest stable releases on PyPI, checked 2026-11-02:

| Package | Latest stable | Released |
|---|---|---|
| robotframework | 7.5 (already pinned) | 2026-09-14 |
| robotframework-browser, -batteries | 21.0.0 | 2026-11-01 |
| robotframework-requests | 0.9.7 (already pinned) | 2024-04-07 |
| robotcode | 2.8.0 | 2026-10-26 |
| rf-mcp | 0.36.0 | 2026-09-26 |
| robotframework-heal | 0.4.0 (already pinned) | 2026-06-18 |
| python-dotenv | 1.2.4 | 2026-10-01 |

A trial `uv lock` with the new pins, run in a scratch copy, resolved 150 packages without a pre-release. Besides the
five pins, it moved only the RobotCode sub-packages (to 2.8.0) and `grpcio`/`grpcio-tools` (to 1.85.0, which Browser
21 pins).

## Goals / Non-Goals

The `solutions` branch is 16 commits on top of an older `main` (lab commits, then `reference` commits). It lacks
the two commits of #34. None of its commits touches the root `pyproject.toml`, `uv.lock` or `docs/robotcode.md`.
Bonus 1 and Bonus 2 each add a separate project under `bonus/` with its own `pyproject.toml` and `uv.lock`, and their
pins are already the latest stable releases.

## Goals / Non-Goals

**Goals:**
- Every direct dependency is pinned at its latest stable release on `main`, with a lockfile that matches.
- `solutions` pins exactly the same versions as `main`, because it is `main` plus the lab results.
- The suite and setup-check pass on the new versions, locally and in CI. On `solutions`, every test passes,
  including the two that `main` ships broken.

**Non-Goals:**
- Changing extras (`robotcode[all]`, `rf-mcp[web,api]`) or adding and removing packages.
- Re-pinning the Bonus projects under `bonus/` on `solutions` (already current), and editing archived changes or
  transcripts that record the old versions.
- Updating the website's npm packages, the shop image or the `[tool.workshop]` pins.
- Rewriting tests for new Browser 21 features such as record keywords.

## Decisions

### D1. Update every direct pin, not only the named ones
The request asks for "latest stable versions" across the dependencies and gives RobotCode as the example. Updating
all five outdated pins in one lock is as much work as updating three, and a later re-lock then has nothing left to
catch up on. Alternative: bump only RobotCode, Robot Framework and Browser. Rejected, because python-dotenv and rf-mcp
would then be stale.

### D2. Robot Framework stays at 7.5
7.5 is the newest final release, so the requested update is a no-op. The lockfile setting rules out a pre-release
of a later version.

### D3. Take Browser 21.0.0 despite the major version
Upstream marks it as a major release only because BrowserBatteries now bundles Node.js 26 LTS. It still supports
Robot Framework 7.1.1+ and Python 3.11+, and was tested with Playwright 1.64.1. The workshop uses Browser through
BrowserBatteries, never through a system Node.js, so the Node change stays inside the wheel. The suite, run in full
against the shop, decides: if it fails because of Browser 21, fall back to 20.5.0 (see Migration Plan).

### D4. Regenerate the lock with `uv lock`, not `uv lock --upgrade`
Only the pins in the manifest change; uv moves transitive packages only as far as the new pins require. That keeps
the diff small enough to review. A general `--upgrade` would move every transitive package as well, which is a
separate change.

### D5. Verify with the commands participants use
`uv sync --locked`, `uv run --no-sync rfbrowser install chromium`, setup-check, and the suite through
`uv run robotcode robot`, the way CI runs it. Then re-run every example in `docs/robotcode.md`, because the document
says each one ran with the pinned versions.

### D6. Bring `solutions` up to date by rebasing onto the new `main`
`workshop/solutions` requires the branch to start from `main` and to be rebased whenever `main` changes. The rebase
happens after the pull request is merged, so `solutions` picks up exactly the versions `main` carries, not a second
copy of the pins. Because no `solutions` commit touches the dependency files, the rebase applies without conflicts,
and `git range-diff` can show that every lab and reference commit is unchanged. The branch is pushed with
`--force-with-lease` against the tip it was rebased from, so a push that someone else made in the meantime is not
overwritten. Alternatives:
- Cherry-pick the bump commit onto `solutions`. Rejected: `solutions` would no longer start from `main`, and
  `git log main..origin/solutions` would show a non-lab commit.
- Merge `main` into `solutions`. Rejected: it breaks the linear one-commit-per-lab history the spec describes.

### D7. One absolute link to the site, above the Quickstart, worded for both places
The site is deployed from this repository to `https://manykarim.github.io/ai-engineering-robotframework/`
(`website/docusaurus.config.js`: `url` plus `baseUrl`). Forks never deploy it (`workshop/docs-site`), so an absolute
link to the workshop's site is the right target from a fork too. A relative link cannot express that: on GitHub it
would resolve inside the repository. The paragraph goes right under the introduction, because a participant who
lands on the repository should see it before the install commands. It is worded as a description of the site ("The
labs, the setup guide, the glossary and the guides are also published as a website …"), not as "go elsewhere", so it
still reads correctly on the site's home page, where the link leads to the page being read. The existing transcripts
and solutions links stay as they are. Alternatives:
- A badge or a link in the repository's GitHub "About" box. Rejected: the About box is not part of a fork's files, and
  a badge says nothing about what is on the site.
- Hiding the paragraph on the site. Rejected: it needs site-only markup, and `workshop/docs-site` requires the
  Markdown to render as written.

## Risks / Trade-offs

- [Browser 21.0.0 is one day old when planned; a regression may surface later] → The full UI suite runs locally and in
  CI before merge. A patch release can be taken in a later change.
- [Existing environments keep a Browser 20 node runtime and the old browser] → The PR description and the commit
  message tell participants to run `uv sync --locked` and `rfbrowser install chromium` again. setup-check already
  reports a version that differs from `uv.lock`.
- [RobotCode 2.8.0 may change output that `docs/robotcode.md` shows] → D5 re-runs each example and updates the
  shortened output where it changed.
- [Robocop moves with `robotcode[all]`] → The trial lock left Robocop unchanged. The `workshop/toolchain` scenario
  "Robocop is available" is checked again anyway.
- [The rebase rewrites `solutions`; a checkout of it no longer fast-forwards] → It is a reference branch nobody
  commits to; the spec already expects it to be rebased. The old tip, `df84f6d`, is noted in the pull request so it
  can be restored.
- [The lab solutions (Bonus 3's subagents, the RobotCode habits in Lab 4) may rely on RobotCode 2.7.0 behaviour] →
  The full suite on `solutions`, including the repaired tests, runs on a freshly reset shop before the push.
- [The site's address changes, for example when the repository moves] → The link is absolute and the site build does
  not check external links. The task checks it answers with HTTP 200, and the address lives in one place in the
  README, next to `website/docusaurus.config.js`'s `url`.

## Migration Plan

1. On a branch from `main`: change the pins, run `uv lock`, and run `uv sync --locked` and the browser install.
2. Run setup-check and the suite against the local shop; update `docs/robotcode.md`.
3. Open a pull request to `main`. "Run tests" must pass. Merge it.
4. Rebase `solutions` onto the new `main`, reinstall, run the full suite on a reset shop, and push it with
   `--force-with-lease`.
5. Rollback: revert the merge commit on `main`. `pyproject.toml` and `uv.lock` return together, and so does the old CI
   cache key. Then rebase `solutions` onto that revert again, or force-push its old tip `df84f6d`. If only Browser 21
   is the problem, pin both Browser packages back to 20.5.0 and re-lock, keeping the other bumps.
