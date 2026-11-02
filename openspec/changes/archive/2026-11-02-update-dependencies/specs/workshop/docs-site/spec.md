## ADDED Requirements

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
