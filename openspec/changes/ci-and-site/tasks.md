## 1. Building blocks

- [x] 1.1 Write `tools/triage.py` (design D3). It takes `--output` (an `output.xml`), `--diff` (a file) and `--out` (the comment), and `--summary-only`. It calls the `TRIAGE_*` endpoint when all three settings are set and `--summary-only` is not given. Verify:
  - on a red `output.xml` without settings, it writes the summary with the failed tests and messages, plus the line naming the secrets;
  - against a local stub endpoint, it sends one request with the model, `max_tokens` 1,200 and the capped input, and puts the answer under the summary with a footer naming the tier and model;
  - with the endpoint unreachable, it falls back to the summary and exits 0;
  - it never prints the key.
- [x] 1.2 Add the `heal-patch` profile to `robot.toml` (design D4). Verify: `uv run robotcode -p heal -p heal-patch config show` sets `HEAL_FIX_TIER=patch`, and `-p heal` alone still sets `report`.

## 2. Workflows

- [ ] 2.1 Write `.github/workflows/run-tests.yml` (design D2). Verify:
  - `actionlint` passes;
  - on a push to a branch of the workshop's repository, the run is green, `robot-results` can be downloaded, and the job summary shows the results summary;
  - a pushed break fails the run and names the test.
- [ ] 2.2 Write `.github/workflows/agent-triage.yml` (design D1, D3). Verify:
  - `actionlint` passes;
  - with no triage secret, a pull request that breaks a test gets one comment with the summary and the secrets line, and a second failing push updates that comment instead of adding one.
- [ ] 2.3 Write `.github/workflows/heal-suggestions.yml` (design D4). Verify:
  - `actionlint` passes;
  - started without `HEAL_*` secrets, it succeeds with the notice;
  - started with `HEAL_*` secrets and preset `stage4`, it opens a pull request whose diff replaces the drifted locators, and nothing is merged.
- [x] 2.4 Write `.github/workflows/docs-site.yml` (design D6). Verify: `actionlint` passes, and every job carries the repository-name guard.
- [x] 2.5 Check pinning and fork safety across all workflows (design D5). Verify:
  - a script lists every `uses:` line and finds each ending in a 40-character SHA with a release comment;
  - every workflow declares `permissions`;
  - every deploy or upstream-only job carries the repository-name guard;
  - no step echoes a secret.

## 3. Participation

- [ ] 3.1 Write `.github/ISSUE_TEMPLATE/setup-problem.yml`, `bug-report.yml` and `config.yml` (design D7). Verify:
  - GitHub's issue chooser on the pushed branch shows both forms and the Discussions link;
  - the bug-report fields match, in order, the sections Lab 7 drafts;
  - the setup form warns against pasting `.env`.
- [x] 3.2 Write `CONTRIBUTING.md` (design D7). Verify: it names the OpenSpec flow and the three checks, and every command in it runs.
- [ ] 3.3 Enable Discussions on the workshop's repository through the API, and document the categories as a manual step for the maintainer in the pull request. Verify: the repository reports `has_discussions: true`.

## 4. The site

- [x] 4.1 Create `website/` with Docusaurus 3.10.2 at exact versions, a committed `package-lock.json`, and the configuration of design D6. Verify:
  - `npm ci && npm run build` succeeds from a clean checkout;
  - the build contains a page for every Markdown file under `labs/`, `docs/` and `transcripts/`, plus `SETUP.md` and `GLOSSARY.md`;
  - the home page is `README.md`.
- [x] 4.2 Check the site's safeguards. Verify:
  - a page with `${SHOP_URL}` in prose builds and shows it literally;
  - a deliberately broken link and a broken anchor each fail the build;
  - outside `website/`, only link fixes that work on GitHub as well were needed, and the pull request lists them.
- [ ] 4.3 Enable GitHub Pages with "GitHub Actions" as the source, and deploy once from `main` after the merge. Verify: the site answers at `https://manykarim.github.io/ai-engineering-robotframework/`, and a lab page's links work there.

## 5. Lab 9

- [x] 5.1 Align Lab 9 with design D3 and D8: the secrets that add an analysis, the tiers, and no maintainer comment. Verify: `tools/check_labs.py` passes, and every workflow and secret name the lab uses exists.
- [ ] 5.2 Rehearse Lab 9 on the workshop's repository with a pull request that breaks a test (design D8). Verify:
  - the summary tier without secrets;
  - the `TRIAGE_*` tier with the maintainer's endpoint;
  - the Claude tier with a Claude credential, or recorded as open when none is set;
  - the heal-suggestion stretch goal;
  - each outcome recorded in `docs/facilitator/rehearsal.md`, and the pull requests closed.
- [ ] 5.3 Record `transcripts/lab-09-ci.md` from the rehearsal, and remove Lab 9 from the transcripts `tools/check_labs.py` accepts as recorded elsewhere. Verify: `tools/check_labs.py` passes without exceptions, and the transcript scan finds no secret or local path.
- [x] 5.4 Add the triage secrets to `SETUP.md` (the Claude credential and `TRIAGE_*`, optional, with the spending-cap warning). Verify: `setup-check`'s guide references still resolve.

## 6. Close-out

- [ ] 6.1 After this change is merged, rebase `solutions` onto `main` and push it. Verify: its suite passes, and `main` is unchanged.
- [ ] 6.2 Validate and archive. Verify: `openspec validate ci-and-site --strict` passes. After the merge, the archive creates `workshop/ci`, `workshop/docs-site` and `workshop/participation` with their Purpose.
