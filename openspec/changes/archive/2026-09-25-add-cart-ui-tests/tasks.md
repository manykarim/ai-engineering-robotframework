# Tasks

## 1. Resources

- [x] 1.1 Confirm the locators of design D3 in the running shop before you write any keyword. Use
  `uv run robotcode repl`. Import `resources/shop.resource`, and open every new context with `Start Shop Test`, so
  that it carries the space when one is set. Each context writes only to the cart of its own new session. Do not apply
  a preset, and do not reset the shop.
  - **Desktop.** In a fresh context:
    - Open `/products/1`. Start `Promise To    Wait For Response    matcher=**/api/cart/items`, click the product's
      "Add to Cart" button, and wait for the promise.
    - Check that `role=banner >> a[href="/cart"] >> text=/^\d+$/` resolves to exactly one visible element whose text
      is `1`. Add once more and check that its text is `2`.
    - Open `/products/2` and add once.
  - **Cart page.** Open `/cart` and check the following:
    - `role=main >> role=article` counts 2.
    - `role=main >> article:has-text("Aurora Neural Headphones")` resolves to exactly one element, and that element
      is one of those two articles. Its text contains "$249.99" and "$499.98". Without the name and the amounts, the
      only whole number left in it is `2`.
    - `role=complementary` resolves to exactly one element.
    - The summary-entry locator resolves to exactly one element for each pairing:
      - `subtotal` with the amount pattern;
      - `shipping` with "Complimentary";
      - `tax` with "Calculated at checkout";
      - `total` with the amount pattern.

      The subtotal's entry and the total's entry both show 539.48, and they are different elements.
  - **Small screen.** In a new context, call `Set Viewport Size    390    844` before you open any page. Then:
    - open `/products/1`, add once, and check that the badge is not visible yet;
    - check that `role=banner >> role=button[name=/navigation|menu/i]` resolves to exactly one visible button;
    - click it, and check that the badge is visible and shows `1`.

  Verify: every row of D3 resolves as the table says. Where a row does not, update it and its reason in `design.md`
  before you go on.
- [x] 1.2 Confirm that the keywords this change reuses exist:
  - `Go To Product Page`, `Product Detail Should Show` and `Click Add To Cart` in `resources/product_detail.resource`;
  - `Get Product From API` in `resources/api.resource`;
  - `Go To Cart Page`, `${SUMMARY}` and `Amount From Text` in `resources/checkout.resource`.

  Verify with `uv run --no-sync python -m robot.libdoc <file> list` for each resource, and read the `*** Variables ***`
  section for `${SUMMARY}`. If anything is missing, stop and report it. Do not write it again.
- [x] 1.3 Write `resources/cart.resource` per design D1 to D7. It imports `shop.resource`, `checkout.resource` and
  `product_detail.resource`, and it holds these keywords:
  - Adding (D2): `Click Add To Cart And Confirm    ${product_id}    ${name}` and
    `Add Product To Cart    ${product_id}    ${name}    ${times}=1`. The confirmation asserts only that the response
    succeeded.
  - Badge and small screen (D3, D4): `Use Small Screen`, `Open Navigation Menu` and `Cart Badge Should Show    ${count}`.
  - Lines (D5, D7): `Cart Line Should Show    ${name}    ${quantity}    ${unit_price}    ${line_total}`,
    `Cart Line Quantity Should Be    ${name}    ${quantity}` and `Cart Should Have Lines    ${count}`.
  - Summary (D3, D6): `Get Cart Summary Amount    ${word}`, `Cart Summary Amount Should Be    ${word}    ${amount}` and
    `Cart Summary Should Show    ${word}    ${text}`.

  A keyword that builds a locator from an argument returns it from one helper, as `Product Section` does in
  `product_detail.resource`. Every failure message names what is missing, and what was found instead. Each keyword
  that is not self-explanatory gets a one-line `[Documentation]`.

  Verify:
  - `uv run robotcode analyze code resources/cart.resource` reports no errors;
  - the file contains no `id=`, `#id`, `.class`, `data-` attribute or `xpath` locator;
  - its only `href` is `/cart`, and its only `name=` is the menu button's;
  - it does not call `Cart Request Should Add Product`, and no keyword in it checks a request's method or body.
    Those checks belong to WEB-005_AC-1 (D2);
  - every UI word in it can be found in `openspec/specs/shop/cart/spec.md`, ignoring case: "navigation", "menu",
    "subtotal", "shipping", "tax" and "total";
  - `git status -- resources` shows `resources/cart.resource` as the only new file. `git diff -- resources` shows
    only the participant's earlier edits.

## 2. Cart tests

- [x] 2.1 Write `tests/ui/cart.robot` per design D1, with exactly these five tests from `specs/suite/cart`:
  - `WEB-005_AC-2 Cart Badge Counts Added Items`
  - `WEB-005_AC-2 Cart Badge Shows In Mobile Menu`
  - `WEB-005_AC-3 Cart Page Lists Name Quantity And Prices`
  - `WEB-005_AC-4 Cart Summary Shows Subtotal Shipping Tax And Total`
  - `WEB-005_AC-9 Adding Product Again Increments Quantity`

  The steps of each test follow D4 to D7:
  - The AC-3 test passes "Aurora Neural Headphones", `2`, `$249.99` and `$499.98`, as the spec writes them.
  - The AC-4 test reads products 1 and 2 with `Get Product From API`, and computes the expected subtotal inline
    (D6).
  - Each test has a one-line `[Documentation]`, and it calls keywords only.

  Verify:
  - `uv run --no-sync python hooks/no_inline_locators.py tests/ui/cart.robot` reports nothing;
  - `uv run robotcode analyze code tests/ui/cart.robot` reports no errors;
  - `uv run robotcode robot --dryrun --include WEB-005` lists exactly these five tests, each tagged `WEB-005` and
    `ui`;
  - every expected text in the file can be found in `openspec/specs/shop/cart/spec.md`: "Aurora Neural Headphones",
    "$249.99", "$499.98", "Complimentary" and "Calculated at checkout".
- [x] 2.2 Run the new tests against the local shop. Verify:
  - `uv run robotcode robot tests/ui/cart.robot` passes 5 of 5;
  - each test passes on its own, with `uv run robotcode robot --test "<test name>"`;
  - the file passes three runs in a row.

  If a test fails, read the failure in `results/` and state the evidence before you change anything. Change the
  keyword or the locator, never an expectation that the spec sets.
- [x] 2.3 Prove that each check can fail. Make a throwaway copy of `tests/ui/cart.robot` under `results/`, which git
  ignores, and change it:
  - in the AC-2 desktop test, expect the badge to show `3` after the second add;
  - in the AC-2 small-screen test, expect the badge to show `2`;
  - in the AC-3 test, expect quantity `3`;
  - in the AC-4 test, compute the expected subtotal with twice the price of product 2;
  - in the AC-9 test, delete the second `Add Product To Cart`.

  Run the copy with `uv run robotcode robot results/<copy>.robot`. Verify that all five tests fail, and that their
  messages name, in order:
  1. the badge and the count it showed;
  2. the badge and the count it showed;
  3. the quantity it found in the line;
  4. the subtotal it found and the one it expected;
  5. the quantity 1 where it expected 2.

  Delete the copy afterwards. `git status -- tests resources` then shows only `tests/ui/cart.robot` and
  `resources/cart.resource` as new, besides the participant's earlier edits.

## 3. Close-out

- [x] 3.1 Validate the change. Verify that `openspec validate add-cart-ui-tests --strict` passes.
- [x] 3.2 Run the new tests and the rest of the suite one last time. Verify:
  - `uv run robotcode robot tests/ui/cart.robot` passes 5 of 5;
  - `uv run robotcode robot --exclude broken` runs the whole suite, and the five new tests pass. A failure of any
    other test is reported with its message and left alone, because it is outside this change;
  - no step applied a preset or reset the shop.
