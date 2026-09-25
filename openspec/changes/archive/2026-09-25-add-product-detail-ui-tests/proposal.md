# Proposal

## Why

No test in the suite covers the product detail page: the shipped suite leaves WEB-003 to Module 5 on purpose. This
change automates four product-detail criteria as Robot Framework UI tests: WEB-003_AC-1, WEB-003_AC-3, WEB-003_AC-8
and WEB-003_AC-9. Each test checks the behaviour `openspec/specs/shop/product-detail` specifies. The story's wording
is not the reference.

## What Changes

- A new test file for the product detail page, with one or more tests for each of the four criteria. Each test name
  starts with its criterion ID, and each test carries the tags `WEB-003` and `ui`.
  - **WEB-003_AC-1**: `/products/1` shows the product's image, the name "Aurora Neural Headphones", a category badge
    with the product's category, a star rating, a review count, the product's price and its description. The
    category, the price and the description are compared with the product as the shop's catalogue API lists it.
  - **WEB-003_AC-3**: `/products/1` shows an "Add to Cart" button next to the product. Clicking it sends a POST
    request that carries the product's ID, 1, and the cart that request returns holds product 1.
  - **WEB-003_AC-8**: from a detail page, the shopper gets back to the products page, `/products`, both ways the spec
    names: with the browser's back button, after opening the detail page from `/products`, and with the site's
    navigation link to the products page. Two tests, one per way (design D5).
  - **WEB-003_AC-9**: `/products/9999` and `/products/abc` each show a not-found message, and neither shows a product
    detail page: no "Add to Cart" button and no "Buy Now" link. Two tests, one per scenario of the spec.
- A new product-detail resource that holds every locator these tests need. The locators are built from roles,
  accessible names and visible text. The product's own section has no role and no name, so it is found by the
  visible text of its main heading, the product's name. That is how the shipped suite finds the product grid by its
  heading. There is one exception: the header's link to the products page is found by its target, `/products`,
  because the spec quotes no text for it (design D2).
- One new keyword in `resources/api.resource` that returns one product of the catalogue listing the suite already
  reads.
- Nothing changes in the existing tests or in the existing keywords, in `resources/legacy.resource`, or in
  `openspec/specs/shop/`.

## Capabilities

### New Capabilities
- `suite/product-detail`: what the suite verifies of `shop/product-detail`, one requirement per automated criterion
  (WEB-003_AC-1, AC-3, AC-8 and AC-9), each naming the tests that verify it.

### Modified Capabilities
None. `shop/product-detail` describes the shop and does not change. `workshop/baseline-suite` keeps WEB-003 out of the
shipped suite. The participant's tests added here are its intended complement, so that requirement does not change
either.

## Impact

- New files: `tests/ui/product_detail.robot` and `resources/product_detail.resource`. The resource reuses
  `resources/shop.resource` for the browser, contexts and pages. It also reuses `resources/catalogue.resource` to
  open the products page, find its product grid, recognise a price and format one.
- Changed file: `resources/api.resource` gains `Get Product From API`. The file has no uncommitted edits.
- There are no new dependencies, and nothing installs a tool. The tests use Browser and RequestsLibrary, which are
  already pinned.
- Every test runs in its own browser context. Only the AC-3 test changes state: it adds one item to the cart of its
  own, fresh session. No preset is applied and no space is reset. The tests pass locally and on the shared instance,
  in any order.
- The tests expect the seeded catalogue of a freshly reset space: product 1 is Aurora Neural Headphones, and no
  product has the ID 9999.
