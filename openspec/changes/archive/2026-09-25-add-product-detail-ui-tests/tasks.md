# Tasks

## 1. Resources

- [x] 1.1 Confirm the locators of design D2 against the running shop before writing any keyword. Use
  `uv run robotcode repl` with Browser in a new context.
  - On `/products/1`, check with `Get Element Count` that the product's section for "Aurora Neural Headphones"
    resolves to exactly one element, which shows that `:has-text()` works inside `:has()`. Check that its image
    named "Aurora Neural Headphones", its level-1 heading, the category badge for "Audio", the star-rating group, the
    price and the "Add to Cart" button each resolve to exactly one element. Check that the review-count and
    description locators find at least one visible element. Check that `${PRODUCT} >> role=img` without a name finds
    only the product photo, with no icon.
  - On `/products`, check that the grid's name link for "Aurora Neural Headphones" resolves to exactly one element,
    and that it leads to `/products/1`. On `/products/1`, check that the header's navigation link to `/products`
    resolves to exactly one visible element.
  - Open `/products/9999` and `/products/abc` with `Go To Shop Page`. Check that the keyword does not fail on the
    `404` status, that the not-found locator finds a visible element, and that both action locators count 0.
  - Start `Promise To    Wait For Response    matcher=**/api/cart/items`, click the product's "Add to Cart" button,
    and `Wait For` the promise. Check that the result holds `request.method`, `request.postData.product_id`, `ok` and
    `body.items`, as D4 expects.

  Verify: every row of D2 resolves as the table says. Where one does not, update that row and its reason in
  `design.md` before going on.
- [x] 1.2 Add `Get Product From API    ${product_id}` to `resources/api.resource` per design D1. It returns the
  product with that ID from `Get Catalogue From API` and fails with a message naming the ID when there is none. It
  gets a one-line `[Documentation]`, like the keywords around it. Verify:
  - `uv run robotcode analyze code resources/api.resource` reports no errors;
  - `git diff resources/api.resource` shows only the new keyword.
- [x] 1.3 Write `resources/product_detail.resource` per design D1 to D6. It imports `shop.resource` and
  `catalogue.resource`. Every keyword that looks inside the product's section takes the product's name as its first
  argument and builds the section's locator from it (D2). It holds these keywords:
  - `Go To Product Page` (by product ID) and `Product Detail Should Show` (by name: waits for the section whose main
    heading shows the name, ignoring case, and fails with a message naming it);
  - for AC-1: `Product Image Should Be Shown`, `Category Badge Should Show`, `Star Rating Should Be Shown`,
    `Review Count Should Be Shown`, `Product Price Should Be` (formats the amount with `Format Price`) and
    `Product Description Should Be Shown`. Each failure message names the missing item (D3);
  - for AC-3: `Click Add To Cart`, which returns the response (D4), and `Cart Request Should Add Product`, which
    checks the method, the body's product ID, `ok` and the returned cart's items;
  - for AC-8: `Open Product From Grid` (by name), `Follow Navigation Link To Products` and
    `Products Page Should Be Shown`;
  - for AC-9: `Not Found Message Should Be Shown` and `Product Actions Should Not Be Shown`.

  Each keyword that is not self-explanatory gets a one-line `[Documentation]`, as in `catalogue.resource`.

  Verify:
  - `uv run robotcode analyze code resources/product_detail.resource` reports no errors;
  - the file contains no `id=`, `#id`, `.class`, `data-` attribute or `xpath` locator;
  - every locator is built from a role, an accessible name or visible text. The only exception is the header's
    navigation link, which is found by its target, `/products`, as D2 explains. The file contains no
    `section:has(h1)` without the product's name, and no `href` other than `/products`;
  - every UI text in it can be found in `openspec/specs/shop/product-detail/spec.md`, ignoring case: "Add to Cart" and
    "Buy Now" as quoted there, "not found" as its term "not-found", "star" from "star rating", and "reviews" from the
    review-count texts it quotes;
  - `resources/legacy.resource` and `resources/catalogue.resource` are unchanged (`git diff` shows only the
    participant's earlier edits).

## 2. Product-detail tests

- [x] 2.1 Write `tests/ui/product_detail.robot` per design D1, with exactly these six tests from
  `specs/suite/product-detail`:
  - `WEB-003_AC-1 Detail Page Shows Product Information`
  - `WEB-003_AC-3 Add To Cart Posts The Product`
  - `WEB-003_AC-8 Back Button Returns To Catalogue`
  - `WEB-003_AC-8 Navigation Link Returns To Catalogue`
  - `WEB-003_AC-9 Unknown Product ID Shows Not Found`
  - `WEB-003_AC-9 Non-Numeric Product ID Shows Not Found`

  The tests pass the name "Aurora Neural Headphones", as the spec quotes it, to every keyword that takes a product
  name. The AC-1 test reads product 1 with `Get Product From API` and passes its category, price and description to
  the AC-1 keywords. The AC-3 test passes the response of `Click Add To Cart` to `Cart Request Should Add Product` with
  the product ID 1. Each test has a one-line `[Documentation]` and calls keywords only. Verify:
  - `uv run --no-sync python hooks/no_inline_locators.py tests/ui/product_detail.robot` reports nothing;
  - `uv run robotcode analyze code tests/ui/product_detail.robot` reports no errors;
  - `uv run robotcode robot --dryrun --include WEB-003` lists exactly these six tests, each tagged `WEB-003` and `ui`;
  - every expected text in the file ("Aurora Neural Headphones", the IDs `1`, `9999` and `abc`) can be found in
    `openspec/specs/shop/product-detail/spec.md`.
- [x] 2.2 Run the new tests against the local shop. Verify:
  - `uv run robotcode robot tests/ui/product_detail.robot` passes 6 of 6;
  - each test passes on its own with `uv run robotcode robot --test "<test name>"`;
  - the file passes three runs in a row.

  If a test fails, read the failure in `results/` and state the evidence before changing anything. Change the
  keyword or the locator, never the expectation that the spec sets.
- [x] 2.3 Prove that the AC-1, AC-3 and AC-9 checks can fail. Make a throwaway copy of
  `tests/ui/product_detail.robot` under `results/`, which git ignores:
  - in the AC-1 test of the copy, replace "Aurora Neural Headphones" with "Aurora Neural Headphones Pro";
  - in the AC-3 test of the copy, expect the product ID 2 instead of 1 in `Cart Request Should Add Product`;
  - in the `WEB-003_AC-9 Unknown Product ID Shows Not Found` test of the copy, replace `9999` with `1`;
  - in the `WEB-003_AC-9 Non-Numeric Product ID Shows Not Found` test of the copy, replace `abc` with `1` and delete
    the `Not Found Message Should Be Shown` step.

  Run the copy with `uv run robotcode robot results/<copy>.robot`. Verify: these four tests fail, and their messages
  name, in order, the product name the heading lacks, the product ID the request carried, the missing not-found
  message, and the "Add to Cart" button found in the main content. Delete the copy afterwards. `git status -- tests
  resources` then shows only the two new files and the change to `resources/api.resource`, besides the participant's
  earlier edits.

## 3. Close-out

- [x] 3.1 Validate the change. Verify: `openspec validate add-product-detail-ui-tests --strict` passes.
- [x] 3.2 Run the new tests and the rest of the suite one last time. Verify:
  - `uv run robotcode robot tests/ui/product_detail.robot` passes 6 of 6;
  - `uv run robotcode robot --exclude broken` runs the whole suite. The six new tests pass. A failure of any other
    test is reported with its message and left alone, because it is outside this change;
  - no step applied a preset or reset the shop.
