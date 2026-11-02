# workshop/docs-site Specification

## Purpose
Publishes the labs, guides, transcripts and facilitator material as one website from the same Markdown files participants read on GitHub, so that nothing is copied and nothing drifts.

## Requirements

### Requirement: One source
The site SHALL render, each from where it lives and without committed copies, generated duplicates or front matter added to them:
- from `main`: `README.md`, `SETUP.md`, `GLOSSARY.md` and the Markdown files under `labs/` and `docs/`;
- from the `solutions` branch: the Markdown files under `transcripts/` and `solutions/`, and the facilitators' answer sheet.

The build SHALL take the branch's files into its own workspace only. `README.md` SHALL be the site's home page.

#### Scenario: A lab is edited
- **WHEN** a lab's `INSTRUCTIONS.md` is changed on `main`
- **THEN** the next deployment of the site shows the change, and no other file needed editing

#### Scenario: A transcript is edited
- **WHEN** a transcript is changed on the `solutions` branch
- **THEN** the next deployment of the site shows the change, and nothing on `main` changed

### Requirement: Markdown as written
The site SHALL parse `.md` files as CommonMark, so that Robot Framework syntax such as `${VARIABLE}` and HTML comments in prose render as written and do not break the build.

A fenced code block marked `mermaid` SHALL render as a diagram on the site, as it does on GitHub, in the light and the dark theme. Every other code block SHALL render as code.

#### Scenario: A variable in prose
- **WHEN** a page contains `${SHOP_URL}` outside a code block
- **THEN** the site builds, and the page shows `${SHOP_URL}` literally

#### Scenario: A diagram
- **WHEN** a page contains a fenced code block marked `mermaid`
- **THEN** the site builds, and the page shows the diagram, not its source

### Requirement: Links are checked
The site's build SHALL fail on any broken link or anchor between its pages. Every link that works on GitHub between the rendered files SHALL also work on the site.

#### Scenario: A lab links a missing transcript
- **WHEN** a lab links a transcript file that does not exist
- **THEN** the build fails and names the link

### Requirement: Deployed from the workshop's repository only
The site SHALL be deployed to GitHub Pages only from the workshop's repository, whenever `main` or the `solutions` branch changes, and always from `main` together with the `solutions` branch. It SHALL be built without deploying for pull requests to either branch. Forks SHALL neither build nor deploy it.

#### Scenario: A fork enables Actions
- **WHEN** a participant's fork runs its workflows
- **THEN** no site job runs there

#### Scenario: A reference page is pushed
- **WHEN** a reference page changes on the `solutions` branch of the workshop's repository
- **THEN** the site is built from `main` and the branch, and deployed

### Requirement: Reproducible build
The site SHALL build from a lockfile with pinned dependency versions, on the Node.js version the setup guide names.

#### Scenario: Building twice
- **WHEN** the site is built from a clean checkout twice
- **THEN** both builds install the same dependency versions from the lockfile

### Requirement: Found from the repository
`README.md` SHALL link the published site by its absolute address, above its first section, and SHALL say what a
participant finds there: the labs, the setup guide, the glossary and the guides under `docs/`. The link SHALL lead to
the workshop's site from the workshop's repository and from every fork, and SHALL read correctly on the site's home
page, which is the same file.

#### Scenario: Opening the repository on GitHub
- **WHEN** a participant opens the repository's or their fork's page on GitHub
- **THEN** the README shows a link to the published site before the Quickstart, and the link opens the site's home
  page

#### Scenario: Reading the site's home page
- **WHEN** a participant reads the home page of the published site
- **THEN** the same sentence reads correctly there, and the link leads to the page they are on
