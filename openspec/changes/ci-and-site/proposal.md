## Why

Module 9 runs on each participant's fork: a pushed break must reach a pull request as a root-cause comment. The repository also needs a public face that participants can read a week before the workshop, follow during it and return to afterwards. Both carry a risk the master document does not spell out: around forty forks will enable GitHub Actions for Lab 9. A workflow that deploys a site, needs a secret nobody set, or fails for reasons unrelated to the lab would turn the module into support work.

## What Changes

- **`run-tests.yml`**: runs the suite against the shop, started as a service container from the pinned image, and uploads the results.
- **`agent-triage.yml`**: when the suite fails, the run's `robotcode results` go to an agent, which posts a root-cause comment on the pull request.
  - With a Claude credential (an API key, or the OAuth token of a Claude subscription), the agent is the Claude Code GitHub Action.
  - Otherwise, with the `TRIAGE_*` settings of any OpenAI-compatible endpoint, a pinned script makes one model call.
  - **Without either, it degrades** to posting the `robotcode results` summary alone, so the lab still works.
  - It is pinned throughout: action SHAs, the model versions, timeouts and a turn or token budget. The credentials are repository or fork secrets, documented with a bold spending-cap warning.
- **`heal-suggestions.yml`** (Lab 9 stretch): `robotframework-heal` at its `patch` tier turns heals into a suggestion pull request, never an automatic merge. Without a healing model it ends with a notice instead of failing.
- **`docs-site.yml`**: builds the site on pull requests and deploys it from `main`, in the workshop's repository only.
- **Fork-safe by rule**: nothing fails, deploys or spends money merely because a fork enabled Actions. Anything upstream-only is guarded by the repository name.
- **Participation**:
  - issue templates: `setup-problem.yml` asks for `setup-check --json` output; `bug-report.yml` doubles as the Lab 7 target format;
  - the Discussions categories (Q&A, Show-your-setup, After-the-workshop);
  - `CONTRIBUTING.md`.
- **A Docusaurus 3.10 site** in `website/`:
  - it renders `labs/` and `docs/` from a single source, with no copies;
  - it sets `markdown.format: 'detect'`, so `.md` files are parsed as CommonMark. Without it, every Robot Framework `${VARIABLE}` in prose becomes an MDX expression and breaks the build;
  - broken links fail the build;
  - it is deployed to GitHub Pages only from the upstream repository.

## Capabilities

### New Capabilities
- `workshop/ci`: the three workflows, their pinning, budgets and no-key fallback, and fork safety.
- `workshop/docs-site`: the single-source Docusaurus site and its deployment.
- `workshop/participation`: issue templates, Discussions categories and the contribution guide.

### Modified Capabilities
None.

## Impact

- **New files**: `.github/workflows/`, `.github/ISSUE_TEMPLATE/`, `CONTRIBUTING.md`, `website/`.
- **Depends on** `workshop-foundation` (install path), `baseline-suite` (what CI runs) and `workshop-labs` (what the site renders). The site skeleton can start as soon as the foundation exists.
- **Manual steps**, documented as tasks: enabling Pages, creating the Discussions categories, and the upstream secret.
- **Takes over from `workshop-labs`** the rehearsal of Lab 9 and its fallback transcript, which need the workflows, and rebases the `solutions` branch once more.
- **Not in scope**: lab content, skills and the suite itself. The one exception is Lab 9's text, which names the secrets and workflows this change defines.
