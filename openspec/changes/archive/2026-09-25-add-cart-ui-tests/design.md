# Design

## Context

See `proposal.md` for the motivation and `specs/suite/cart/spec.md` for what each test checks. The facts below come
from the local shop at version `0.3.0`, with the space in its reset state (`clean` and `stage1` both hold). They were
read from:
- the served HTML of `/cart` for an empty cart, and its header;
- `/static/app.js` and the stylesheet;
- `GET /api/products/` and `GET /api/cart/`.

To serve a filled cart page, something has to write to a cart, and the planning step wrote nothing. So the markup of
a filled cart comes from the cart page's template in the running shop container. Nothing was checked in a browser
yet, so task 1.1 confirms the locators there first.

- **The cart badge.** The site header, `role=banner`, holds the navigation labelled "Primary navigation". Its link to
  `/cart` shows "Cart" and a badge. The badge is a `span` with `aria-live="polite"` and the label "Cart items". While
  the cart is empty, the badge has no text and is not displayed.
  - After each successful add, `app.js` sets the badge's text to the sum of the quantities in the cart the POST
    returned, and makes the badge visible. There is no page reload.
  - On every page load, it reads the cart and sets the badge the same way.
- **Small screens.** At a width of 600 pixels or less, the header shows a menu button. Its only text,
  "Toggle navigation", is visually hidden, so that text is the button's accessible name. The navigation's items,
  including the cart link, stay hidden until the button is clicked. Above 600 pixels, the button is not displayed
  and the items are always shown.
- **Adding to the cart.** Each click on a product's "Add to Cart" button sends `POST /api/cart/items` with quantity 1
  and an `X-Session-ID` header. (The shop's visible text on the button reads "Add to cart".) The header's value comes
  from the `session_id` cookie, which `app.js` sets on the first page load of a fresh context. The cart page finds its
  cart through the same cookie (WEB-005_AC-10). So a test that adds through the pages sees its own cart on `/cart`.
  `resources/product_detail.resource` already has:
  - `Click Add To Cart`, which clicks the button in the product's own section and returns the POST's response;
  - `Cart Request Should Add Product`, which checks the request's method and the product ID it carries. That is
    WEB-005_AC-1, so D2 does not use it.
- **The cart page with items.** `main` holds a section headed "Your cart".
  - Each cart line is an `article`. It holds an `h3` with the product's name, a paragraph "2 × $249.99" (quantity
    and unit price), and a separate element with the line total, "$499.98". The line has no labels.
  - The summary is an `aside`, the complementary landmark, with the heading "Summary". It lists "Subtotal" with an
    amount, "Shipping" with "Complimentary", and "Estimated tax" with "Calculated at checkout", as term and
    description pairs. Then comes a separate entry, "Total due", with an amount, and then the checkout and
    continue-shopping links.
  - The chat widget's `aside` is hidden, so the summary is the only visible complementary landmark.
  - Amounts are written as `$` and a number with thousands separators and cents.
- **Catalogue.** Product 1 is Aurora Neural Headphones at 249.99. Product 2 is Insight Smart Notebook at 39.50. No
  product's name contains another product's name.
- **Existing keywords.** `resources/checkout.resource` describes itself as "the cart and checkout pages". It has:
  - `Go To Cart Page`;
  - `${SUMMARY}` (`role=complementary`), which the shipped checkout tests already use for an `aside` nested in a
    section, as on the cart page;
  - `Amount From Text`;
  - `Add Product To Cart From Its Page`, which D2 does not reuse.
- The shipped suite verifies no WEB-005 criterion on purpose (`workshop/baseline-suite`). This change builds on
  work from the archived `add-product-detail-ui-tests` change that is not committed yet:
  - `resources/product_detail.resource`, which is untracked;
  - `Get Product From API` in `resources/api.resource`, which is an uncommitted edit.

## Goals / Non-Goals

**Goals:**
- Five tests that pass in a freshly reset space, alone or together, in any order, locally and on the shared
  instance.
- Every locator is built from the stable contract: roles, visible text and one link target. There is one accessible
  name, for the menu button, which has no visible text (D3). So the tests also pass under the drift stages `stage1`
  to `stage4`.

**Non-Goals:**
- The rest of WEB-005:
  - AC-1: the tests check only that each add's response succeeded. That is the precondition WEB-005_AC-2 names,
    "the API responds successfully". They check neither the request's method nor the product ID it carries (D2);
  - AC-5 and AC-6: the AC-4 test never clicks "Proceed to Checkout" or "Continue Shopping";
  - AC-7 and AC-10.
- How the badge looks before the first add. No scenario of the specification states it.
- Adding from the home page or the products page. The scenarios of these four criteria don't name a page, so every
  test adds from the detail page.
- Other screen sizes, and touch emulation. One phone-sized window stands for "a small screen".
- The cart API itself. API-005 is this lab's stretch goal.
- Updating `docs/facilitator/suite-outcomes.toml`. It records the shipped suite for the maintainers.

## Decisions

### D1. Two new files; the shipped resources stay as they are

- `tests/ui/cart.robot` has the same frame as `tests/ui/product_detail.robot`:
  - Suite Setup `Open Shop Browser` and `Open Shop API`, Suite Teardown `Close Browser`, Test Setup
    `Start Shop Test`;
  - `Test Tags    WEB-005    ui`.

  It imports `shop.resource`, `api.resource` and `cart.resource`. The API session serves the AC-4 test only (D6).
- `resources/cart.resource` holds the locators and keywords of the header's cart badge, the navigation menu button,
  the cart lines and the cart summary. It imports:
  - `shop.resource`;
  - `checkout.resource`, for `Go To Cart Page`, `${SUMMARY}` and `Amount From Text`;
  - `product_detail.resource`, for `Go To Product Page`, `Product Detail Should Show` and `Click Add To Cart`. It
    also brings in `catalogue.resource`.

*Alternative:* add the keywords to `checkout.resource`, whose documentation covers the cart page too. Rejected:
- the file belongs to the shipped WEB-006 tests;
- the new keywords would sit next to `Add Product To Cart From Its Page`, which adds products differently (D2).

A separate file leaves the shipped file untouched and reuses what it already has, so no locator is written twice.

### D2. Adding products through the detail page, each add confirmed by its response

Two new keywords:
- `Click Add To Cart And Confirm    ${product_id}    ${name}` works on the detail page that is already open. It calls
  `Click Add To Cart`, then asserts that the response succeeded. On a failure, the message names the product and the
  response's status.
- `Add Product To Cart    ${product_id}    ${name}    ${times}=1` opens `/products/{id}` with `Go To Product Page`
  and waits with `Product Detail Should Show`. It then runs `Click Add To Cart And Confirm` `times` times on the same
  page.

The AC-2 tests call the first keyword, because the badge must be checked between clicks, without a reload. The
AC-3, AC-4 and AC-9 tests call the second.

*Why not `Add Product To Cart From Its Page` from `checkout.resource`:*
- it finds the button by its accessible name, "Add … to cart". The spec quotes "Add to Cart", which convention 4
  and the interpretation rules match as visible text;
- it confirms the add by waiting for a digit in the header's cart link, which is the badge. That badge is what
  WEB-005_AC-2 tests, so a badge defect would fail the AC-3, AC-4 and AC-9 tests for the wrong reason. Confirming
  each add by the POST's own response avoids that.

*Why only success, and not `Cart Request Should Add Product`:* that keyword asserts the request's method and the
product ID it carries, which is WEB-005_AC-1 and outside this slice. A defect there would fail all five tests with an
AC-1 message, so the suite would verify AC-1 without saying so. The only precondition the spec names is "the API
responds successfully". Whether the right product landed in the cart is what the cart page shows, and the AC-3 and
AC-9 tests check that there. So the returned cart is not inspected either.

*Why the pages and not the API:* the scenarios describe a shopper who adds products. Also, the cart page finds its
cart by the `session_id` cookie (WEB-005_AC-10). Adding through the API would mean copying the cookie's value into an
`X-Session-ID` header by hand. Adding through the page keeps the cookie and the cart in step without that.

### D3. Locators

Every locator is written in `resources/cart.resource`. Tests contain none.

| Element | Locator | Why |
|---|---|---|
| Cart badge (AC-2) | `role=banner >> a[href="/cart"] >> text=/^\d+$/` | **The one link target**, plus visible text. It is the element inside the header's link to the cart page whose whole visible text is a whole number. The spec names the cart page, `/cart`, and quotes no text for the link or the badge. |
| Navigation menu button (AC-2, small screen) | `role=banner >> role=button[name=/navigation\|menu/i]` | **The one accessible name.** The button's only text is visually hidden, so it is a control without visible text, and the interpretation rules allow its accessible name. The regex uses the spec's own words, "navigation menu". A role lookup skips hidden buttons, such as the account menu. |
| Cart line (AC-3, AC-9) | `role=main >> article:has-text("<product name>")` | Visible text: the line in the main content that shows the product's name, ignoring case. A role lookup can't filter by visible text, so this uses the element that carries the `article` role. `catalogue.resource` finds grid cards as `article`s the same way. No product's name contains another's, so the name selects one line. |
| All cart lines (AC-9) | `role=main >> role=article` | A role: counts the lines. On `/cart`, the lines are the only articles. Task 1.1 checks that the named line is one of them. |
| Summary entry (AC-4) | `${SUMMARY} >> text=/\b<word>\b[\s\S]*<value>/i` | Visible text: the smallest element of the summary whose text holds the word, and after it the value. `<word>` is `subtotal`, `shipping`, `tax` or `total`. `<value>` is either the amount pattern `\$[0-9,]+\.[0-9]{2}` or the regex-escaped quoted value. |

**Why the badge is found by the link target.** `checkout.resource` has `${CART LINK}`, but that finds the link by
an accessible name that starts with "Cart", and the spec gives no such name. The badge's label, "Cart items", is not
visible either, and the spec speaks of a badge, not a label. The link target is the page the spec names, and
`docs/conventions.md` (section 3) lists link targets as part of the stable contract.
- *Alternative:* the badge's `aria-live` attribute, which `app.js` uses itself. Rejected: that is markup, not a role,
  a label or visible text.

**Why summary entries are found by a word followed by a value.**
- One pattern pairs each label with its value, without depending on the markup. The first three entries are term and
  description pairs, but the total is not.
- `\b` makes the spec's word a whole word, so "Subtotal" never counts as the total. It still matches "Estimated tax",
  as the interpretation rules' example for "Tax" requires, and "Total due".
- *Alternative:* `dt:text-is(...) + dd`, as `Get Summary Amount` in `checkout.resource` does. Rejected: it can't find
  the total, and `text-is` would miss "Estimated tax".

**Small screen.** `Use Small Screen` calls Browser's `Set Viewport Size    390    844` on the test's fresh page,
before it opens any shop page. So the shop's script sees the small screen from its first load.
- *Alternative:* a context with a viewport. Rejected: `Start Shop Test` in `shop.resource` creates the context, and
  it also sends the space header. A second context would repeat that logic, and changing the shipped keyword is out
  of scope.

### D4. AC-2: the badge after each add

`Cart Badge Should Show    ${count}` waits until the badge is visible, then asserts that its text equals `count`.
Browser's assertion retries until the timeout, so the badge's asynchronous update is awaited.
- **Desktop:** `Click Add To Cart And Confirm`, then the badge shows 1. The same click again, then it shows 2. There
  is no navigation in between, which proves that the badge updates without a reload. The count of 2 proves that the
  badge shows the total item count, not the number of distinct products.
- **Small screen:** `Use Small Screen`, then the add, then `Open Navigation Menu`, then the badge shows 1. This
  follows the order of the spec's scenario. The click on the menu button also proves the small-screen layout: at
  desktop size that button is not displayed, and the click would fail.

### D5. AC-3: what a line shows

`Cart Line Should Show    ${name}    ${quantity}    ${unit_price}    ${line_total}` checks, and each failure message
names what is missing:
- the line for `name` is visible;
- its visible text contains `unit_price` and `line_total`, as the spec writes them: "$249.99" and "$499.98";
- `Cart Line Quantity Should Be    ${name}    ${quantity}` passes. It removes the name, ignoring case, and every
  dollar amount from the line's visible text. The whole numbers left must be exactly `quantity`. "2 × $249.99"
  leaves "2". On a failure, the message shows the numbers found and the line's text.

The spec gives no labels, and the shop shows none, so the test doesn't decide which amount is which. With quantity
2, the unit price and the line total differ, so both appearing in the line is the observable check. For these values,
the line total is the quantity times the unit price: 2 × 249.99 = 499.98.

### D6. AC-4: the expected subtotal comes from the catalogue

The test reads products 1 and 2 with `Get Product From API`. It adds product 1 twice and product 2 once, each from its
own detail page, by the name the API returns. It then computes the expected subtotal inline:
`Evaluate    round(2 * $first["price"] + $second["price"], 2)`. That is 539.48 in a reset space.
- It is written inline so that the expectation is visible in the test.
- The test `WEB-002_AC-1 Card Prices Are The Product Prices` builds its expectations from the catalogue the same way.

Keywords:
- `Get Cart Summary Amount    ${word}` reads the entry's text and turns it into a number with `Amount From Text`;
- `Cart Summary Amount Should Be    ${word}    ${amount}` compares numbers to the cent. Comparing numbers, not text,
  means the thousands separator does not matter;
- `Cart Summary Should Show    ${word}    ${text}` waits until the entry for `word` followed by `text` is visible.

The test checks `subtotal` and `total` against the expected subtotal, `shipping` against "Complimentary" and `tax`
against "Calculated at checkout".

*Why two products, one of them twice:* two lines mean that a subtotal of only one line fails. One line total that
differs from its unit price means that a subtotal of unit prices fails.
- *Alternative:* product 1 only, with the spec's $499.98. Rejected: one line cannot show a sum.
- *Alternative:* sum the line totals the page shows. Rejected: the page labels neither amount in a line, so picking
  "the line total" would rest on the markup's order, and AC-3 already checks the line totals.

### D7. AC-9: the cart page before and after the second add

`Cart Should Have Lines    ${count}` asserts the number of lines in the main content. The test runs these steps:
1. add once, then open `/cart`;
2. `Cart Line Quantity Should Be` with 1, then `Cart Should Have Lines` with 1;
3. `Add Product To Cart` again from `/products/1`, then open `/cart`;
4. quantity 2, and still one line.

The quantity check runs first, because it waits for the line. The count therefore runs on a loaded page, and a count
of 1 can't pass on a page that is still empty.

### D8. Test data comes from the specs

These values appear in `shop/cart` word for word:
- "Aurora Neural Headphones", "Add to Cart", `/products/1` and `/cart`;
- the quantity 2, "$249.99" and "$499.98";
- "Complimentary" and "Calculated at checkout";
- the words subtotal, shipping, tax, total and "navigation menu".

Product 2 and the prices in AC-4 come from the catalogue API (D6). The window size of 390 × 844 is a chosen phone
size, one instance of "a small screen".

Nothing comes from the story alone, such as its sample cart or "Another Product". Nothing comes from what the shop
happens to show either, such as "Estimated tax", "Total due", "Toggle navigation", "Cart items", "Your cart" or the
600-pixel breakpoint.

## Risks / Trade-offs

- **The filled cart's markup was read from the template, not from a browser.** Some behaviours are unverified:
  - which element a `text=` regex matches;
  - that `role=complementary` finds the summary on `/cart`;
  - the badge's text after an add;
  - the menu button's accessible name.

  → Task 1.1 checks every row of D3 in the running shop, in a fresh context that writes only to its own new cart.
  Any locator that resolves differently is changed, and its row in D3 is updated.
- **A summary entry's value must follow its word.** A layout that put the amount before its label would fail AC-4.
  → Accepted. The failure message names the entry it looked for.
- **The quantity is read from the line's visible text.** A quantity shown only as the value of an input field would
  fail AC-3 and AC-9. → Accepted: the spec says the line lists the quantity. The message shows the line's text.
- **The badge must be a whole number on its own.** A badge that read "1 item" would not be found.
  → Accepted. The failure message names the badge and the expected count.
- **The menu button must be named for navigation or a menu.** → Accepted. These are the spec's own words, and the
  failure names the button.
- **The tests depend on the product-detail work, which is not committed yet** (Context). → Task 1.2 checks that
  those keywords exist before anything is written. If they are missing, stop and report it rather than write them
  again.
- **A test could pass without checking anything**, for example a count that runs before the page is loaded.
  → Every check waits for its element, or runs after a check that waits. Task 2.3 proves that the AC-2, AC-3, AC-4
  and AC-9 checks can fail.
- **The tests write to carts,** but only to the carts of their own new sessions. No preset is applied and no space is
  reset.
