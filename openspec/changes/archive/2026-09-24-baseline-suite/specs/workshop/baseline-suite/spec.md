## Purpose

Defines the test suite that ships with the participant repository: what it verifies, and how it behaves under every workshop preset, so that each module's demonstration - failures on purpose, drift, planted bugs, healing - happens identically for every participant.

## ADDED Requirements

### Requirement: Coverage of the criteria the presets break
The suite SHALL verify WEB-002_AC-1 with two separate tests - one for each card's add-to-cart control, one for each card's price - and SHALL verify WEB-006_AC-1, together with further WEB-002 and WEB-006 criteria. It MUST NOT verify any criterion of WEB-003, WEB-004, WEB-005, WEB-007 or API-005, which are the stories participants automate in Module 5.

#### Scenario: Listing the tests
- **WHEN** the suite's test names are listed
- **THEN** two names start with `WEB-002_AC-1`, one with `WEB-006_AC-1`, and none with an ID of WEB-003, WEB-004, WEB-005, WEB-007 or API-005

### Requirement: Green in the clean state
In a freshly reset space, every test that is not tagged `broken` SHALL pass, with the local shop and with the shared instance alike.

#### Scenario: A run after a reset
- **WHEN** the space is reset and the suite runs with `broken` excluded
- **THEN** every test passes

### Requirement: Stable-contract tests survive every stage
Every test whose locators all come from the shop's stable contract - roles and accessible names, visible text, labels, form-field names, link targets - SHALL pass under each of the presets `stage1`, `stage2`, `stage3` and `stage4`.

#### Scenario: Stage 4
- **WHEN** preset `stage4` is applied and the suite runs with `broken` excluded
- **THEN** every stable-contract test passes

### Requirement: Designed drift-fragile tests
The suite SHALL contain at least one test for each fragile locator kind - a covered form-field id, a covered class and a `data-test` hook - each reaching its element only through that kind of locator. Each such test SHALL fail in exactly the stages that its kind drifts in, and pass in the others: a form-field id in stages 2, 3 and 4; a class in stages 2 and 4; a `data-test` hook in stages 3 and 4.

#### Scenario: A class locator in stage 3
- **WHEN** preset `stage3` is applied
- **THEN** the class-locator test passes and the `data-test` test and the form-field-id test fail

#### Scenario: A data-test hook in stage 2
- **WHEN** preset `stage2` is applied
- **THEN** the `data-test` test passes and the class-locator test and the form-field-id test fail

### Requirement: Planted defects surface in their tests only
Under preset `buggy`, the card-control test, the card-price test and the checkout-total test SHALL fail, and every other test not tagged `broken` SHALL pass. The delay the `buggy` preset adds to the catalogue SHALL NOT make any test fail.

#### Scenario: A run under buggy
- **WHEN** preset `buggy` is applied and the suite runs with `broken` excluded
- **THEN** exactly the WEB-002_AC-1 card-control test, the WEB-002_AC-1 card-price test and the WEB-006_AC-1 test fail

### Requirement: Healing never hides a defect
Under preset `drift_and_bug`, the card-price test and the checkout-total test SHALL fail both in a plain run and in a run with the healing profile. With the healing profile and a configured model, every test whose only failure is a drifted locator SHALL pass through a healed locator, recorded as a proposal, while the two defect tests still fail on their assertions.

#### Scenario: Plain run under drift_and_bug
- **WHEN** preset `drift_and_bug` is applied and the suite runs without the healing profile
- **THEN** the card-price test, the checkout-total test and every drift-fragile test fail

#### Scenario: Healing run under drift_and_bug
- **WHEN** preset `drift_and_bug` is applied and the suite runs with the healing profile and a configured model
- **THEN** the drift-fragile tests without a defect pass, the card-price and checkout-total tests fail on their expected values, and the healing report lists every heal as a proposal

### Requirement: Two tests broken on purpose
The suite SHALL contain exactly two tests tagged `broken`, and both SHALL fail under every preset. The cause of one SHALL be observable in a variable's value at a breakpoint, for step-debugging. The cause of the other SHALL be found by comparing the test's expectation with the `shop/*` specification, for debugging in conversation without live access to the page.

#### Scenario: Running only the broken tests
- **WHEN** the suite runs with only the `broken` tag included, under any preset
- **THEN** two tests run and both fail

### Requirement: Exactly one inline locator
Exactly one statement in the suite's test files SHALL use a locator literal instead of a keyword from `resources/`. The exception MUST NOT be described in any participant-facing document.

#### Scenario: Searching the test files
- **WHEN** the test files are searched for locator literals
- **THEN** exactly one is found

### Requirement: An API smoke test
The suite SHALL include API tests that verify the health endpoint and the product listing through the API, and MUST NOT exercise the cart API.

#### Scenario: Running the API tests
- **WHEN** only the API tests run against a healthy shop
- **THEN** they pass without sending any request to `/api/cart`

### Requirement: The suite stays in its space
When `SHOP_SPACE` is set, every browser context and every API session the suite opens SHALL send that space. The suite MUST NOT apply a preset or reset a space.

#### Scenario: A run on the shared instance
- **WHEN** the suite runs with the shared profile in space `octocat`
- **THEN** the pages it opens report `octocat`, and the presets that hold in `octocat` are the same before and after the run

### Requirement: A verified expected-outcome matrix
The repository SHALL record, as data, which tests fail under each of the presets `clean`, `stage2`, `stage3`, `stage4`, `buggy` and `drift_and_bug`, and why. A documented command SHALL run the suite under each of these presets against the pinned shop, compare the results with the data, exit with a non-zero status on any difference, and leave the space reset.

#### Scenario: The image changes behaviour
- **WHEN** a test's outcome under some preset differs from the recorded matrix
- **THEN** the verification command names the test, the preset, and the recorded and actual outcomes, and exits with a non-zero status

### Requirement: A healing profile
The repository SHALL offer a `heal` run profile that attaches the healing listener to the unmodified suite, writes fixes only as proposals, and never heals assertions. It SHALL combine with the `local` and `shared` profiles. Without a configured model, a run with the profile SHALL produce the same test results as a plain run.

#### Scenario: No model configured
- **WHEN** the suite runs with the `heal` profile and no healing model is configured
- **THEN** the test results equal those of a plain run, and the healing report records that healing was skipped

#### Scenario: Test files untouched
- **WHEN** a healing run completes with heals
- **THEN** no file under `tests/` or `resources/` has changed

### Requirement: Neutral test code
Test names, documentation, tags and comments in the suite SHALL describe the behaviour a test verifies. They MUST NOT name a planted bug or a feature flag, or say why a test fails under a preset.

#### Scenario: Reading the suite
- **WHEN** the suite's files are searched for `BUG_`, `LOCATOR_` and the names of the planted-bug presets
- **THEN** nothing is found
