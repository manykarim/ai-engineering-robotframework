# workshop/test-conventions Specification

## Purpose
Defines the conventions the shipped suite follows and that the labs, the Lab 3 skill and the Lab 7 hook rely on, so that tests written by participants and by agents read and behave like the suite they extend.

## Requirements

### Requirement: Criterion ID first
A test that verifies a story criterion SHALL start its name with the criterion ID as `<STORY>_<AC>`. Several tests of one criterion SHALL share the prefix and differ in the rest of the name. Tests that verify no criterion SHALL carry the `smoke` tag instead.

#### Scenario: Tracing a failure
- **WHEN** a test named `WEB-006_AC-1 Order Total Adds Up` fails
- **THEN** its criterion is identified by the name alone

### Requirement: Locators live in resources
Test files SHALL contain keyword calls only. Every locator SHALL be written in a keyword under `resources/`.

#### Scenario: Reviewing a test file
- **WHEN** a test file is reviewed
- **THEN** it contains no locator literal, apart from the one documented exception of the shipped suite

### Requirement: The stable contract first
Locators SHALL be built from the shop's stable contract: roles with accessible names, visible text, labels, form-field names and link targets. Ids, classes and `data-test` hooks SHALL appear only in the legacy resource, which the conventions document lists as a known deviation.

#### Scenario: A new keyword
- **WHEN** a keyword for a new element is added outside the legacy resource
- **THEN** its locator uses a role, text, label, field name or link target, not an id, class or `data-test` hook

### Requirement: Quoted text is visible text
Where a specification quotes UI text, a test SHALL match it against the element's visible text, as `shop/interpretation-rules` defines, and SHALL use accessible names only where a name or label is meant.

#### Scenario: A button quoted as "Add to Cart"
- **WHEN** a test locates the button the specification quotes as "Add to Cart"
- **THEN** it matches the visible text, ignoring case, not the more specific accessible name

### Requirement: Field locators are scoped to their form
A locator for a form field SHALL be scoped to the form it belongs to, because the same field name can occur in more than one form on a page.

#### Scenario: The checkout email field
- **WHEN** a test fills the checkout form's email field on a page that also contains the sign-in dialog
- **THEN** its locator resolves to exactly one element

### Requirement: Isolated tests
Every UI test SHALL run in its own browser context, with its own cookies and therefore its own cart. Tests MUST NOT apply presets or reset spaces; the state they need is created through the shop's own pages or API within their session.

#### Scenario: Two checkout tests in a row
- **WHEN** one test leaves items in its cart and the next test starts
- **THEN** the next test starts with an empty cart

### Requirement: Tags
Every test SHALL carry its story ID as a tag (for example `WEB-002`) or `smoke`, and its layer, `ui` or `api`. The two tests broken on purpose SHALL carry `broken`, and no other test SHALL.

#### Scenario: Selecting by tag
- **WHEN** a participant runs the suite with `--include WEB-006`
- **THEN** exactly the WEB-006 tests run
