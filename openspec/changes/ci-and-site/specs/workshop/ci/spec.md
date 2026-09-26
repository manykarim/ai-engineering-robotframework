## Purpose

Runs the suite in GitHub Actions on every participant's fork and on the workshop's repository, explains failures on pull requests, and proposes heals, without ever failing, deploying or spending money merely because a fork enabled Actions.

## ADDED Requirements

### Requirement: The suite runs on every push and pull request
A workflow SHALL run the suite on every push and every pull request, against the shop started from the image `shop/compose.yaml` pins, and SHALL upload the run's results as an artifact whether the run passes or fails. It SHALL leave out the tests tagged `broken`, so that `main` is green.

#### Scenario: A fresh fork
- **WHEN** a participant enables Actions on a fork of `main` and pushes a commit that changes nothing in `tests/` or `resources/`
- **THEN** the workflow passes, and its results can be downloaded from the run

#### Scenario: A pushed break
- **WHEN** a participant pushes a commit that makes one test fail
- **THEN** the workflow fails and names that test

### Requirement: Failures on a pull request are explained
When the suite fails for a pull request within the same repository, a workflow SHALL post one comment on that pull request that summarises the failed tests from the run's results. It SHALL add a root-cause analysis written by an agent:
- through the Claude Code GitHub Action when an Anthropic API key or a Claude Code OAuth token is configured;
- otherwise through a single model call to any OpenAI-compatible endpoint when its model, address and key are configured.

Without any of these, the comment SHALL hold the summary alone and say how to enable the analysis. A later failure of the same pull request SHALL update that comment, not add another.

#### Scenario: No credential at all
- **WHEN** the suite fails for a pull request and no model credential is configured
- **THEN** the pull request gets a comment with the failed tests and their messages, and a line naming the secrets that would add an analysis, and the triage workflow succeeds

#### Scenario: A Claude credential
- **WHEN** the suite fails for a pull request and a Claude credential is configured
- **THEN** the comment contains a root-cause analysis that names the failing test and the change in the pull request that caused it

#### Scenario: An OpenAI-compatible endpoint
- **WHEN** no Claude credential but the `TRIAGE_*` settings are configured
- **THEN** the comment contains a root-cause analysis from a single call to that endpoint

### Requirement: Agents in CI are bounded
Every workflow that calls a model SHALL pin the model, cap the number of agent turns or the tokens of the call, and set a job timeout. The triage agent SHALL be able to read the repository and the run's results and nothing else: it MUST NOT edit files, push, or run commands other than reading results. Every agent action SHALL leave a reviewable artifact: the comment, the job summary, or a pull request.

#### Scenario: A prompt injection in a pull request
- **WHEN** a pull request's diff contains text instructing the agent to push a commit or reveal a secret
- **THEN** the triage agent has no tool to do either, and the only output is the comment

### Requirement: Pinned actions
Every third-party action SHALL be referenced by a full commit SHA, with the release it corresponds to in a comment. Tools installed in a workflow SHALL be installed at the versions the repository pins.

#### Scenario: Reviewing a workflow
- **WHEN** any workflow file is inspected
- **THEN** every `uses:` line ends in a 40-character SHA followed by a release comment

### Requirement: Heal suggestions on demand
A workflow started by hand SHALL run the suite with the healing profile against a drifted shop and, when heals were made, open a pull request that proposes them as changes. It MUST NOT merge that pull request or push to the default branch. Without a configured healing model, it SHALL end successfully with a notice that healing needs one.

#### Scenario: Starting the heal suggestions
- **WHEN** a participant with a healing model configured starts the workflow
- **THEN** a pull request appears whose diff replaces the drifted locators, and nothing is merged

#### Scenario: No healing model
- **WHEN** the workflow is started without `HEAL_*` settings
- **THEN** it succeeds, and its summary says that healing needs a model and where to configure it

### Requirement: Fork safety
Enabling Actions on a fork SHALL NOT make any workflow fail for a reason other than the tests, deploy anything, or call a paid service without a secret the fork's owner set. Jobs meant only for the workshop's repository SHALL be guarded by the repository's name. No workflow SHALL print a secret.

#### Scenario: A fork with no secrets
- **WHEN** a participant enables Actions on a fork and opens a pull request that breaks a test
- **THEN** only the suite's run fails, the triage comment is the summary, and no deployment or paid call happens
