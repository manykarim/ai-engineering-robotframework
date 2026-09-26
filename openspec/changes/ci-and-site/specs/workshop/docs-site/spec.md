## Purpose

Publishes the labs, guides, transcripts and facilitator material as one website from the same Markdown files participants read on GitHub, so that nothing is copied and nothing drifts.

## ADDED Requirements

### Requirement: One source
The site SHALL render `README.md`, `SETUP.md`, `GLOSSARY.md` and the Markdown files under `labs/`, `docs/` and `transcripts/` directly from where they live in the repository, without copies, generated duplicates or front matter added to them. `README.md` SHALL be the site's home page.

#### Scenario: A lab is edited
- **WHEN** a lab's `INSTRUCTIONS.md` is changed on `main`
- **THEN** the next deployment of the site shows the change, and no other file needed editing

### Requirement: Markdown as written
The site SHALL parse `.md` files as CommonMark, so that Robot Framework syntax such as `${VARIABLE}` and HTML comments in prose render as written and do not break the build.

#### Scenario: A variable in prose
- **WHEN** a page contains `${SHOP_URL}` outside a code block
- **THEN** the site builds, and the page shows `${SHOP_URL}` literally

### Requirement: Links are checked
The site's build SHALL fail on any broken link or anchor between its pages. Every link that works on GitHub between the rendered files SHALL also work on the site.

#### Scenario: A lab links a missing transcript
- **WHEN** a lab links a transcript file that does not exist
- **THEN** the build fails and names the link

### Requirement: Deployed from the workshop's repository only
The site SHALL be built and deployed to GitHub Pages only from the `main` branch of the workshop's repository, and SHALL be built without deploying for pull requests to it. Forks SHALL neither build nor deploy it.

#### Scenario: A fork enables Actions
- **WHEN** a participant's fork runs its workflows
- **THEN** no site job runs there

### Requirement: Reproducible build
The site SHALL build from a lockfile with pinned dependency versions, on the Node.js version the setup guide names.

#### Scenario: Building twice
- **WHEN** the site is built from a clean checkout twice
- **THEN** both builds install the same dependency versions from the lockfile
