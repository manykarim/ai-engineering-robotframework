## MODIFIED Requirements

### Requirement: Markdown as written
The site SHALL parse `.md` files as CommonMark, so that Robot Framework syntax such as `${VARIABLE}` and HTML comments in prose render as written and do not break the build.

A fenced code block marked `mermaid` SHALL render as a diagram on the site, as it does on GitHub, in the light and the dark theme. Every other code block SHALL render as code.

#### Scenario: A variable in prose
- **WHEN** a page contains `${SHOP_URL}` outside a code block
- **THEN** the site builds, and the page shows `${SHOP_URL}` literally

#### Scenario: A diagram
- **WHEN** a page contains a fenced code block marked `mermaid`
- **THEN** the site builds, and the page shows the diagram, not its source
