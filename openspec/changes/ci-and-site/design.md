## Context

See `proposal.md` for the motivation, and `specs/` for the requirements. The facts below were checked on 2026-09-26.

- **The repository** is public, with `main` as the default branch. Discussions and Pages are not enabled yet.
- **The shop image** `ghcr.io/manykarim/demo-webshop:0.3.0` is public. Actions can start it as a service container without credentials.
- **The suite** runs green on `main` once `--exclude broken` leaves out the two tests that fail on purpose. `setup-check`, the shop helper (`python -m shop wait`) and the `heal` profile exist already.
- **GitHub Models was retired on 2026-07-30.** Its inference endpoint now answers with a placeholder, so no free, keyless model is available to a workflow. The triage agent therefore needs a credential the fork's owner sets. Without one, the lab falls back to the results summary.
- **The Claude Code GitHub Action** (`anthropics/claude-code-action`, v1.0.235 at `756cc22e`) accepts `anthropic_api_key` or `claude_code_oauth_token`, which a Claude subscription can generate with `claude setup-token`. It takes a `prompt`, CLI arguments in `claude_args` (model, turns, allowed tools), and plugins from a marketplace.
- **The latest releases** of the actions used: `actions/checkout` v7.0.1, `astral-sh/setup-uv` v10.2.0, `actions/cache` v6.1.0, `actions/upload-artifact` v7.0.1, `actions/download-artifact` v8.0.1, `actions/setup-node` v7.0.0, and for Pages `configure-pages` v6.0.0, `upload-pages-artifact` v5.0.0 and `deploy-pages` v5.0.1. Docusaurus is at 3.10.2 and needs Node.js 20 or newer.
- **Forks:** GitHub copies `.github/` into every fork. A workflow runs there once the owner enables Actions, with the fork's secrets, which are usually none.

## Goals / Non-Goals

**Goals:**
- A participant's fork needs no setup beyond enabling Actions. A secret only adds the agent's analysis.
- Every agent action in CI is bounded and leaves a reviewable artifact.
- The site is the labs and guides as they are in the repository.

**Non-Goals:**
- Azure DevOps or Jira pipelines. Module 9 mentions them as the same pattern; no files are provided.
- Custom site styling beyond Docusaurus' classic theme, a logo and the navigation.
- Running the site build on forks.

## Decisions

### D1. The workflows

| Workflow | Trigger | Runs on forks | Needs a secret |
|---|---|---|---|
| `run-tests.yml` | `push`, `pull_request` | yes | no |
| `agent-triage.yml` | `workflow_run` of *Run tests*, completed and failed, for a `pull_request` | yes | optional: Claude credential, or `TRIAGE_*` |
| `heal-suggestions.yml` | `workflow_dispatch`, with the preset as input (default `stage4`) | yes, when started | `HEAL_*`; without them it ends with a notice |
| `docs-site.yml` | `pull_request` and `push` to `main`, on changes to Markdown or `website/` | no: every job checks the repository's name | no |

`agent-triage.yml` is a separate workflow triggered by `workflow_run` rather than a job of `run-tests.yml`. A `workflow_run` workflow runs with the repository's own token and secrets, even when the triggering run had a read-only token. It reads the pull request number from the triggering run. When that list is empty, for a pull request from another fork to the workshop's repository, it ends without commenting. The upstream repository therefore never runs an agent on a stranger's pull request.

*Alternative:* one workflow with a triage job after the tests. Rejected: on pull requests from forks to the upstream, that job has neither secrets nor permission to comment, and it would fail for reasons unrelated to the tests.

### D2. Running the suite in CI

- The shop is a service container from the pinned image, on port 9090. `uv run --no-sync python -m shop wait` waits for its health.
- `astral-sh/setup-uv` installs uv at the version `pyproject.toml` requires. `uv sync --locked` creates the environment, and `actions/cache` keeps `.venv` and the uv cache, keyed on `uv.lock`.
- `uv run --no-sync rfbrowser install --with-deps chromium` installs the browser and its system libraries into `.venv`.
- `uv run robotcode robot --exclude broken` runs the suite. `results/` is uploaded as the artifact `robot-results` in every case, and the job summary gets `robotcode results summary`.
- The job has a timeout of 20 minutes.

### D3. Triage in three tiers

`agent-triage.yml` downloads `robot-results` from the triggering run, checks out the pull request's head, and writes the comment in one of three ways:

1. **A Claude credential is set** (`ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN`): the Claude Code Action runs with a fixed prompt. The prompt says: read the failed tests with `uv run --no-sync robotcode results show --failed -o <output.xml>`, read the pull request's diff from a file the workflow wrote, find the change that caused each failure, and write the analysis to `triage.md`.
   - `claude_args` pins the model (`claude-sonnet-5`) and 15 turns, and allows only `Read`, `Grep`, `Glob`, `Write` and `Bash(uv run --no-sync robotcode results:*)`.
   - The job's timeout is 15 minutes.
   - The RobotCode plugin is installed through the action's `plugins` input, so the agent in CI has the habits the labs teach.
2. **Otherwise the `TRIAGE_*` settings are set** (`TRIAGE_MODEL`, `TRIAGE_BASE_URL`, `TRIAGE_API_KEY`): `tools/triage.py` makes one chat-completion call to that endpoint.
   - The input is the failed tests, their messages and the diff, capped at 20,000 characters.
   - The call has `max_tokens` 1,200 and a timeout of 120 s.
   - The script writes `triage.md`. Participants can reuse the provider of their healing key.
3. **Otherwise**, `tools/triage.py --summary-only` writes the results summary and a line naming the secrets that would add an analysis.

In every tier, the workflow, not the agent, posts `triage.md` with `gh pr comment --edit-last --create-if-none`, so each pull request keeps one comment that later failures update. The comment starts with the results summary from the run, then the analysis, then a footer naming the tier and the model. The agent cannot push, comment or run anything but `robotcode results`. A prompt injection in the diff can at most change the text of `triage.md`, which a person reads.

*Alternative:* the Claude Code Action posting the comment itself. Rejected: it would need write permission on pull requests inside the agent, which the fixed posting step avoids.

### D4. Heal suggestions

`heal-suggestions.yml` starts the shop, applies the preset given as input with the shop helper (default `stage4`: drift without planted defects), and runs `uv run robotcode -p heal -p heal-patch robot --exclude broken`. A new profile `heal-patch` in `robot.toml` sets `HEAL_FIX_TIER=patch`, so the run writes `results/heal/heal.patch`.
- When the patch is not empty, the workflow applies it on a new branch `heal-suggestions/<run id>`, commits it, and opens a pull request with the heal report's summary as its body.
- Without `HEAL_MODEL`, the workflow writes a notice to the job summary and ends successfully.
- The job has a timeout of 30 minutes. The heal profile's budget per failure applies.

### D5. Fork safety

- Every job that deploys, or that should run only in the workshop's repository, starts with `if: github.repository == 'manykarim/ai-engineering-robotframework'`.
- Every workflow declares least-privilege `permissions`.
- Secrets are passed to steps as environment variables and are never echoed. `tools/triage.py` reads its key from the environment and does not print it.
- A missing secret decides a tier, never a failure.

### D6. The site

`website/` holds a Docusaurus 3.10.2 site with exact versions in `package.json` and a committed `package-lock.json`:
- **One docs plugin with the repository root as its path**, `path: '..'`. It includes `README.md`, `SETUP.md`, `GLOSSARY.md` and `labs/**/*.md`, `docs/**/*.md` and `transcripts/**/*.md`, and excludes everything else.
  - One instance keeps every relative link between those files resolvable, because Docusaurus resolves `.md` links only within an instance. This is the same set `tools/check_labs.py` allows links into.
  - `README.md` files become their folder's index, so the repository's `README.md` is the home page, at `routeBasePath: '/'`.
- **`markdown.format: 'detect'`** parses `.md` as CommonMark. `onBrokenLinks`, `onBrokenAnchors` and the Markdown-link hook are all set to `'throw'`.
- **Sidebars are generated** from the folders. Labs, guides, transcripts and facilitator material become categories, in the order of `labs/README.md`.
- **The deployment** goes to `https://manykarim.github.io/ai-engineering-robotframework/`, through the Pages actions, from `main` only. Pull requests build without deploying.

*Alternative:* copying files into `website/docs` at build time. Rejected: two copies drift, and links would be rewritten twice.

### D7. Participation

- **`.github/ISSUE_TEMPLATE/`** holds three files:
  - `setup-problem.yml`: a form for OS, shop mode, agent, and the `setup-check --json` output, with a warning against pasting `.env`;
  - `bug-report.yml`: steps, expected with its criterion, actual, evidence, and environment. These are the sections of Lab 7's draft, in the same order;
  - `config.yml`: points questions to Discussions and disables blank issues.
- **Discussions** is enabled through the API. Its categories (Q&A, Show your setup, After the workshop) can only be created in the web interface, so that is a manual step with the exact names.
- **`CONTRIBUTING.md`**: changes go through OpenSpec, and the checks to run are `tools/check_labs.py`, `tools/verify_outcomes.py` and the site build.

### D8. Lab 9 and the rehearsal

Lab 9's text is aligned with D3: it names the Claude credential and the `TRIAGE_*` settings as the ways to add an analysis, and drops its maintainer comment.

The rehearsal runs on the workshop's own repository, with a pull request that breaks a test, once per tier:
- **without any secret**;
- **with `TRIAGE_*`**, set from the maintainer's healing provider;
- **with a Claude credential**. This one needs the maintainer to run `claude setup-token` and set the secret; the rehearsal records it as a manual step if that has not happened.

The pull request is closed afterwards. `transcripts/lab-09-ci.md` records the run, and `tools/check_labs.py` drops Lab 9 from its list of transcripts recorded elsewhere.

Lab 9 produces no files, so `solutions` gets no Lab 9 commit. It is rebased onto `main` once more after this change.

## Risks / Trade-offs

- [A Claude subscription token in a fork is the participant's own quota] → Documented in `SETUP.md` and Lab 9 as optional, with the spending-cap warning. The summary tier needs nothing.
- [The `TRIAGE_*` endpoint is any provider, with any quality] → The comment's footer names the tier and the model, so a weak analysis is attributable. The summary is always above it.
- [`workflow_run` runs the default branch's version of `agent-triage.yml`] → Intended: a pull request cannot change how it is triaged. Changes to the triage workflow take effect after merging.
- [Browser installation dominates CI time] → `.venv` is cached on `uv.lock`, and only the system libraries are reinstalled on each run.
- [About forty forks run the suite at once on the workshop day] → Each fork runs on its own GitHub-hosted runners and its own shop container. Nothing touches the shared instance.
- [The site renders facilitator material publicly] → It is public in the repository already, as the master document intends.
- [Docusaurus changes how it handles broken Markdown links between releases] → Versions are exact, and a failing build is the signal.

## Migration Plan

This change adds workflows, templates, `CONTRIBUTING.md`, `website/`, `tools/triage.py` and the `heal-patch` profile, and edits Lab 9. The manual steps are:
- enabling Pages with "GitHub Actions" as its source;
- creating the Discussions categories;
- optionally, the upstream's triage secrets.

Rollback is a revert: nothing outside the repository depends on these files.
