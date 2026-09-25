# Proposal

## Why

No test in the suite covers product search: the shipped suite leaves WEB-004 to Module 5 on purpose. This change
automates four search criteria as Robot Framework UI tests: WEB-004_AC-1, WEB-004_AC-3, WEB-004_AC-6 and
WEB-004_AC-7. Each test checks the behaviour that `openspec/specs/shop/search` specifies. The story's wording is not
the reference.

## What Changes

- A new test file for search, with one or more tests for each of the four criteria. Each test name starts with its
  criterion ID, and each test carries the tags `WEB-004` and `ui`.
  - **WEB-004_AC-1**: the home page, `/`, shows a visible search input in its hero section. The hero is the page's
    first screen, which opens with its main heading (design D2). The input's placeholder or label says that it is
    for searching.
  - **WEB-004_AC-3**: on `/`, entering "headphones" and submitting shows a search results section. It lists Aurora
    Neural Headphones as a product card with its name, a loaded image and its price. The expected price comes from
    the shop's catalogue API. There are two tests, one for each way the spec names: pressing Enter and clicking the
    search button (design D5).
  - **WEB-004_AC-6**: with results for "headphones" displayed, clicking the "Clear search" or "Clear results" button
    hides the results section, shows the page's normal content again and empties the search input. There are two
    tests, one for each normal content the spec names: the hero section on `/` and the product grid on `/products`
    (design D6).
  - **WEB-004_AC-7**: on `/`, submitting "xyz123" shows, inside the search results section, a visible message saying
    that no products were found, and no product card.
- A new search resource that holds every locator these tests need: the page's main heading, the search form, its
  input and button, the search results section, a result card, the clear button and the empty-state message. The locators are
  built from roles, labels and visible text. The resource reuses `resources/shop.resource` to open pages and
  `resources/catalogue.resource` for the product grid and prices.
- Nothing changes in the existing tests or keywords, in `resources/legacy.resource`, or in `openspec/specs/shop/`.

## Capabilities

### New Capabilities
- `suite/search`: what the suite verifies of `shop/search`. It has one requirement per automated criterion
  (WEB-004_AC-1, AC-3, AC-6 and AC-7), and each requirement names the tests that verify it.

### Modified Capabilities
None. `shop/search` describes the shop and does not change. `workshop/baseline-suite` keeps WEB-004 out of the shipped
suite. The tests added here are the participant's intended addition to it, so that requirement does not change either.

## Impact

- New files: `tests/ui/search.robot` and `resources/search.resource`.
- No existing file changes. The AC-3 tests read product 1 with `Get Product From API`, which `resources/api.resource`
  already has as an uncommitted edit.
- There are no new dependencies, and nothing installs a tool. The tests use Browser and RequestsLibrary, which are
  already pinned.
- Search writes nothing, so the tests change no state in the shop. Every test runs in its own browser context. No
  preset is applied and no space is reset. The tests pass locally and on the shared instance, in any order.
- The tests expect the seeded catalogue of a freshly reset space: product 1 is Aurora Neural Headphones, and no
  product matches "xyz123".
