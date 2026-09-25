# Proposal

## Why

No test in the suite covers the cart. The shipped suite leaves WEB-005 to Module 5 on purpose. This change automates
four cart criteria as Robot Framework UI tests: WEB-005_AC-2, WEB-005_AC-3, WEB-005_AC-4 and WEB-005_AC-9. Each test
checks the behaviour that `openspec/specs/shop/cart` specifies. The story's wording is not the reference.

## What Changes

- A new test file for the cart, with one or more tests for each of the four criteria. Each test name starts with its
  criterion ID, and each test carries the tags `WEB-005` and `ui`. Every test fills its own cart the way a shopper
  does: it clicks "Add to Cart" on a product's detail page, in its own fresh session.
  - **WEB-005_AC-2**: two tests, one for each scenario in the spec.
    - Desktop: after the product is added, the cart badge in the header shows 1 without a page reload. After a
      second add it shows 2, the total item count.
    - Small screen: after the product is added and the shopper opens the navigation menu, the badge is visible in
      the menu and shows 1.
  - **WEB-005_AC-3**: after Aurora Neural Headphones is added twice, `/cart` lists it with its name, quantity 2, unit
    price $249.99 and line total $499.98. These are the values in the spec's scenario.
  - **WEB-005_AC-4**: with two different products in the cart (product 1 twice, product 2 once), the summary on
    `/cart` shows:
    - a subtotal equal to the sum of the line totals, computed from the catalogue prices the shop's API lists;
    - shipping as "Complimentary";
    - tax as "Calculated at checkout";
    - a total equal to the subtotal.
  - **WEB-005_AC-9**: after Aurora Neural Headphones is added once, `/cart` has exactly one line, with quantity 1.
    After it is added again, the cart still has exactly one line, now with quantity 2.
- A new cart resource that holds every locator these tests need: the header's cart badge, the navigation menu
  button, the cart page's lines and its summary. The locators are built from roles, visible text and one link
  target. To add products and open the cart page, the resource reuses keywords of `resources/product_detail.resource`
  and `resources/checkout.resource`. It adds nothing to those files.
- Nothing changes in the existing tests or keywords, in `resources/legacy.resource`, or in `openspec/specs/shop/`.

## Capabilities

### New Capabilities
- `suite/cart`: what the suite verifies of `shop/cart`. It has one requirement per automated criterion (WEB-005_AC-2,
  AC-3, AC-4 and AC-9), and each requirement names the tests that verify it.

### Modified Capabilities
None. `shop/cart` describes the shop and does not change. `workshop/baseline-suite` keeps WEB-005 out of the shipped
suite. The tests added here are the participant's intended addition to it, so that requirement does not change either.

## Impact

- New files: `tests/ui/cart.robot` and `resources/cart.resource`. The resource reuses:
  - `resources/shop.resource` for the browser, contexts and pages;
  - `resources/product_detail.resource` to open a detail page and click its "Add to Cart" button;
  - `resources/checkout.resource` for `Go To Cart Page`, the summary landmark and reading an amount.
- No existing file changes. The tests read products with `Get Product From API`, which `resources/api.resource`
  already has.
- There are no new dependencies, and nothing installs a tool. The tests use Browser and RequestsLibrary, which are
  already pinned.
- Every test runs in its own browser context, so it has its own session and an empty cart. The tests change only
  the carts of their own new sessions. No preset is applied and no space is reset. The tests pass locally and on the
  shared instance, in any order.
- The tests expect the seeded catalogue of a freshly reset space: product 1 is Aurora Neural Headphones at $249.99,
  and product 2 exists.
