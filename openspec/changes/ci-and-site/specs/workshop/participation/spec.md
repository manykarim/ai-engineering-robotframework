## Purpose

Gives participants one place to ask for setup help before the day, a format for the defects they file in Module 7, and a way to come back and contribute afterwards.

## ADDED Requirements

### Requirement: A setup-problem template
The repository SHALL offer an issue template for setup problems that asks for the output of `setup-check --json`, the operating system, the shop mode and the coding agent, and warns not to paste `.env` or any key.

#### Scenario: A participant cannot get green
- **WHEN** a participant opens a new issue in the workshop's repository
- **THEN** they can choose the setup-problem form, which asks for the check's JSON output and warns against pasting secrets

### Requirement: A bug-report template for the shop
The repository SHALL offer a bug-report template for defects of the demo shop, with fields for the steps to reproduce, the expected behaviour and the criterion it comes from, the actual behaviour, the evidence from a test run, and the environment (shop version, preset, space). Its fields SHALL match the sections Lab 7 has participants draft.

#### Scenario: Filing the Lab 7 defect
- **WHEN** a participant files the issue drafted in Lab 7 in their fork
- **THEN** each section of the draft has a matching field in the template

### Requirement: Discussions for the long tail
The workshop's repository SHALL have GitHub Discussions with the categories Q&A, Show your setup and After the workshop, and the issue chooser SHALL point questions to Discussions.

#### Scenario: A question after the workshop
- **WHEN** a former participant opens a new issue to ask a question
- **THEN** the issue chooser offers Discussions for questions

### Requirement: A contribution guide
`CONTRIBUTING.md` SHALL explain how to propose a change to the repository: as an OpenSpec change, with the checks that must pass - the lab contract, the expected-outcome matrix and the site build - and how to suggest a new lab or skill.

#### Scenario: Suggesting a new lab
- **WHEN** a contributor wants to add a lab
- **THEN** `CONTRIBUTING.md` tells them to propose it as an OpenSpec change and which checks it must pass
