## Purpose

Defines how every requirement under `shop/*` is read and checked, so that a test written from these specs passes or fails for the same reasons as the shop's own acceptance checks.

## ADDED Requirements

### Requirement: Clean state
Every requirement under `shop/*` SHALL hold in a freshly reset workshop space, in which the seeded catalogue of 12 products is unchanged and the cart is empty unless a requirement says otherwise.

#### Scenario: After a reset
- **WHEN** a participant resets their space and then checks any `shop/*` requirement
- **THEN** the requirement holds

### Requirement: Quoted UI text is visible text
Where a requirement quotes the text of a button, link, heading or label, it SHALL be satisfied by an element whose visible text - its rendered text content, not its accessible name - contains the quoted phrase. The comparison SHALL ignore case, SHALL trim leading and trailing whitespace, and SHALL count every run of whitespace in either text, including line breaks and indentation in the markup, as one space. Whitespace SHALL never be removed, so a word break matters.

#### Scenario: Case and a more specific accessible name
- **WHEN** a requirement quotes "Add to Cart" and a button's visible text is "Add to cart" while its accessible name is "Add Aurora Neural Headphones to cart"
- **THEN** the button satisfies the quoted text

#### Scenario: Phrase inside longer text
- **WHEN** a requirement quotes "Tax" and the element's visible text is "Estimated tax"
- **THEN** the element satisfies the quoted text

#### Scenario: Text split across lines in the markup
- **WHEN** a requirement quotes "Log out" and the element's text is "Log" followed by a line break and "out"
- **THEN** the element satisfies the quoted text

#### Scenario: A word break matters
- **WHEN** a requirement quotes "Logout" and the element's visible text is "Log out"
- **THEN** the element does not satisfy the quoted text

### Requirement: Accessible names only where a name is meant
Accessible names - an `aria-label`, alternative text or an associated label - SHALL be used only where a requirement speaks of a label or a name, for a form field identified by its label, or for a control without visible text. A difference between a quoted phrase and an accessible name SHALL NOT count as a deviation.

#### Scenario: Form field found by its label
- **WHEN** a requirement names the full name field of the checkout form
- **THEN** the field is identified by its associated label, "Full name"

#### Scenario: Control without visible text
- **WHEN** a requirement names the close button of the sign-in dialog, which shows only "×"
- **THEN** the button is identified by its accessible name

### Requirement: What counts as an error message
"An error message is displayed", and every equivalent wording, SHALL mean a message that appears as a result of the shopper's action, either in an element with the alert role or next to the field concerned. Text that was already on the page before the action SHALL NOT count.

#### Scenario: Help text present before submitting
- **WHEN** a form shows a hint beside a field before it is submitted, and the submission is invalid
- **THEN** only a message that appears after the submission counts as the error message

### Requirement: Examples are not requirements
Values introduced by "e.g." or "or equivalent", and example values, requests and responses, SHALL NOT be required. A requirement that shows a value only as an example SHALL be satisfied by any value that meets its normative wording. Scenarios MAY use such values as concrete instances.

#### Scenario: Example empty-state wording
- **WHEN** a requirement shows "No products found" as an example of an empty-state message
- **THEN** any visible, user-friendly message stating that no products were found satisfies it

### Requirement: Traceable to one criterion
Every behaviour requirement under `shop/*` SHALL name exactly one active acceptance criterion of the demo-webshop story set as `<STORY>_<AC>`, and SHALL NOT use a withdrawn criterion ID.

#### Scenario: Withdrawn IDs
- **WHEN** the requirements under `shop/*` are listed
- **THEN** each names one active criterion, and `WEB-004_AC-4`, `WEB-005_AC-8` and `WEB-006_AC-9` appear nowhere
