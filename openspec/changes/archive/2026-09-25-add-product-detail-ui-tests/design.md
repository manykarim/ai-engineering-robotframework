# Design

## Context

See `proposal.md` for the motivation and `specs/suite/product-detail/spec.md` for what each test checks. The facts
below come from the local shop at version `0.3.0`: its served HTML for `/products/1`, `/products/9999`,
`/products/abc` and `/products`, its `/static/app.js`, and `GET /api/products/1`. The space was in its reset state:
`clean` and `stage1` both hold. Nothing was checked in a browser yet, so task 1.1 confirms the locators there first.

- **The product's own section has no landmark and no name.** `/products/1` answers `200`. Its `main` holds several
  plain `<section>`s. The first is the product's own section, and it is the only one with an `h1`, which reads
  "Aurora Neural Headphones". The section holds:
  - one image, whose alt text is "Aurora Neural Headphones product photo";
  - a category badge, a `span` whose whole text is "Audio". The API lists product 1 with the category "Audio";
  - a rating: an element with the `group` role and the label "Rated 4.8 out of 5 stars from 214 reviews". It holds
    "4.8", five star icons, which are `aria-hidden`, and "(214)". "214 reviews" stands next to it;
  - a paragraph with the description, the API's `description` word for word, and the price "$249.99";
  - a button whose visible text is "Add to cart". Its accessible name is "Add Aurora Neural Headphones to cart", and a
    content data attribute carries the product's ID. That attribute is not named `data-product-id`;
  - a link "Buy now" to `/checkout`, and the product highlights.
- **The page holds five "Add to cart" buttons.** Below the product's section come "Why you'll love it", "You might also
  like" and "Trending in the studio". The four cards of "You might also like" each have their own "Add to cart" button
  and their own rating group. Only the button in the product's section is the one AC-3 means.
- **Adding sends one POST.** A click handler of `app.js` sends `POST /api/cart/items` with the JSON body
  `{"product_id": 1, "quantity": 1}` and an `X-Session-ID` header. The header's value comes from a `session_id`
  cookie. A fresh context has no such cookie, so it gets a new random session and an empty cart. The response is the
  updated cart. `shop/cart` names the endpoint for detail pages (WEB-005_AC-1), and it names the body field and the
  response's `items` entries (API-005_AC-2, API-005_AC-11).
- **Navigation.** The site header, `role=banner`, holds a navigation labelled "Primary navigation". Its links go to
  `/`, `/products`, `/cart` and `/checkout`. The footer also links to `/products`. On `/products`, the grid card of
  product 1 links to `/products/1` twice: from the name inside its `h3`, and from a "View details" link.
- **Unknown IDs get a not-found page.** `/products/9999` and `/products/abc` both answer `404` with the same page. Its
  `main` holds one section: an `h1` "Product not found", a paragraph "We couldn't find a product at this address…",
  and a link "Browse all products" to `/products`. It has no element with the alert role, no "Add to cart" button and
  no "Buy now" link.
- The shipped suite verifies no WEB-003 criterion on purpose (`workshop/baseline-suite`). These tests are the
  participant's addition to it. The archived `add-search-ui-tests` change describes search tests and a search
  resource that are not in this working tree. This change depends on neither.

## Goals / Non-Goals

**Goals:**
- Six tests that pass in a freshly reset space, alone or together, in any order, locally and on the shared instance.
- Every locator is built from a role, an accessible name or visible text, apart from one link target (D2). All of
  these belong to the stable contract, so the tests also pass under the drift stages `stage1` to `stage4`.

**Non-Goals:**
- The rest of WEB-003: AC-2 and AC-4 to AC-7. The AC-1 test checks that a rating and a review count are there, not
  their values, which AC-2 checks. The AC-9 test looks for the absence of "Buy Now" but never clicks it, which AC-4
  would check.
- Products other than 1. The story's test data lists product 12 as an edge case, but the spec's scenarios name
  `/products/1` only.
- The HTTP status of the not-found page. It is `404` today, but the spec does not require any status.
- The cart page and the header's cart badge after "Add to Cart". They belong to WEB-005_AC-3 and WEB-005_AC-2.
- Updating `docs/facilitator/suite-outcomes.toml`. It records the shipped suite for the maintainers.
  `tools/verify_outcomes.py` applies presets, so it is not run here.

## Decisions

### D1. Two new files and one new keyword

- `tests/ui/product_detail.robot` has the same frame as `tests/ui/catalogue.robot`:
  - Suite Setup `Open Shop Browser` and `Open Shop API`, Suite Teardown `Close Browser`, Test Setup `Start Shop Test`;
  - `Test Tags    WEB-003    ui`.

  The API session serves the AC-1 test only (D3). The file imports `shop.resource`, `api.resource` and
  `product_detail.resource`. It does not import `legacy.resource`.
- `resources/product_detail.resource` holds every locator and keyword of the detail page and of the not-found page.
  It imports `shop.resource` for `Go To Shop Page`. It also imports `catalogue.resource` for `Go To Catalogue`,
  `${GRID}`, `${CARD PRICE}` and `Format Price`.
- `resources/api.resource` gains `Get Product From API    ${product_id}`. It returns the product with that ID from
  `Get Catalogue From API` and fails when there is none. It reads the listing, `GET /api/products/`, which the suite
  already uses. It does not use `GET /api/products/{id}`, which exists but which no spec names.

*Alternatives:*
- Add the keywords to `catalogue.resource`. Rejected: that file is about another page, and it holds the participant's
  uncommitted work.
- Look the product up with an inline `Evaluate`, as `catalogue.robot` does. Rejected: a keyword reads as behaviour,
  and the AC-1 test would otherwise start with a Python expression.

### D2. Locators

Every locator is written in `resources/product_detail.resource`. Tests contain none. `${PRODUCT}` is the product's
own section, built from the product's name. So every keyword that looks inside that section takes the name as its
first argument. The tests pass "Aurora Neural Headphones", as the spec quotes it.

| Element | Locator | Why |
|---|---|---|
| Product's section | `role=main >> section:has(h1:has-text("<product name>"))` | Visible text: the section whose main heading shows the product's name, ignoring case (see below). |
| Product image (AC-1) | `${PRODUCT} >> role=img[name=/<product name>/i]`, with the name regex-escaped | An image has no visible text, so its alt text, which is its accessible name, identifies it. An alt text that names the product makes it the product's image. The name is a regex because a quoted `name` in a `role=` selector must match the whole accessible name, even with the `i` flag, and the alt text is longer than the name (task 1.1 found 0 elements). The name filter is needed: without it, `role=img` also finds the cart icon of the "Add to Cart" button. The star icons are `aria-hidden`, so a role lookup skips them. |
| Name (AC-1) | `${PRODUCT} >> role=heading[level=1]` | The page's main heading. Its visible text must contain the name. |
| Category badge (AC-1) | `${PRODUCT} >> text=/^<category>$/i`, with the category regex-escaped | Visible text: an element whose whole text is the category, ignoring case. A contained match would also hit the description, "Spatial audio headphones…". |
| Star rating (AC-1) | `${PRODUCT} >> role=group[name=/star/i]` | The stars have no visible text, so the group's label identifies the rating. "star" is the spec's own word. The section scope leaves out the rating groups of the recommended cards. |
| Review count (AC-1) | `${PRODUCT} >> text=/\d+\s+reviews?\b\|\(\d+\)/i`, first match | Visible text in either form that WEB-003_AC-2 quotes, "214 reviews" or "(214)", with any whole number. |
| Price (AC-1) | `${PRODUCT} >> ${CARD PRICE}` | Reuses the price pattern of `catalogue.resource`: an element whose whole text is a dollar amount with cents. |
| Description (AC-1) | `${PRODUCT} >> text=<description>` | Visible text that contains the description, ignoring case. |
| "Add to Cart" (AC-3) | `${PRODUCT} >> button:has-text("Add to Cart")` | Visible text, ignoring case, as a contained phrase, and quoted as the spec writes it. It never uses the accessible name (interpretation rules). The section scope picks one of the page's five buttons. |
| Product link in the grid (AC-8) | `${GRID} >> role=heading >> a:has-text("<product name>")` | Visible text: the name link inside the card's heading, with the name as the spec quotes it. The card's second link to the same page reads "View details", so it does not match. |
| Navigation link (AC-8) | `role=banner >> role=navigation >> a[href="/products"]` | **The one link target** (see below). The header scope leaves out the footer's link to the same target. |
| Not-found message (AC-9) | `role=main >> text=/not[\s-]+found/i`, first match | Visible text: the spec's term "not-found message", with a space or a hyphen, ignoring case. |
| Detail actions (AC-9) | `role=main >> button:has-text("Add to Cart")` and `role=main >> :is(a, button):has-text("Buy Now")` | Visible text, as quoted in the spec. Both must count 0. |

**The product's section is found by the text of its heading.** On the detail page, that section is a plain
`<section>` with no role and no accessible name. What identifies it is its main heading, which shows the product's
name. The locator finds it the way `${GRID}` in `catalogue.resource` finds the product grid,
`section:has(h2:text-is("All products"))`: the section whose heading shows a given text. It uses `:has-text()`
instead of `:text-is()`, so the name matches as a contained phrase, ignoring case (interpretation rules). It uses no
id, no class and no `data-test` hook. Alternatives considered:
- *`section:has(h1)`, anchored on the heading element alone.* Rejected: it rests on the markup structure only, not on
  a role, a label or visible text.
- *Scope to `role=main` only.* Rejected: the recommended cards further down have their own "Add to Cart" buttons,
  ratings, images and prices. AC-1 and AC-3 would then find elements that are not the product's.
- *`role=heading[level=1]` inside the filter, through Playwright's `internal:has=`.* Rejected: that syntax is internal
  to Playwright and not documented for selectors.
- *The category badge by the `data-category` content attribute*, as `Get Card Category` in `catalogue.resource`
  does. Rejected: the plan-review checklist asks for roles, labels or visible text, and the badge's text is enough.

**The header's navigation link is the one link target.** The spec quotes no text for that link. It names only its
destination, "the products page, `/products`". Visible text would make the test expect wording the spec doesn't
contain, such as "Products", and the link has no accessible name of its own. `docs/conventions.md` (section 3) and
`workshop/test-conventions` list link targets as part of the stable contract. *Alternative:* the visible text
"products", the spec's word in "the products page". Rejected: a link to `/products` with other wording would satisfy
the spec but fail the test.

### D3. What the AC-1 test compares with

The spec quotes the product's name, "Aurora Neural Headphones", and nothing else about product 1. The expected
category, price and description therefore come from `Get Product From API    1`, in the test's space. The price goes
through `Format Price`, so it reads "$249.99". The test `WEB-002_AC-1 Card Prices Are The Product Prices` compares with
the catalogue API the same way.

Each item gets its own keyword, and each failure message names the missing item:
- **Image**: visible, and loaded, meaning that its `naturalWidth` is above 0. A broken image element is visible, but
  it displays no image. Browser's assertion retries until the timeout, so a slow image load does not fail the check.
- **Name**: the heading's visible text contains the name, ignoring case.
- **Category badge**: found exactly once, and visible.
- **Star rating**: visible. The icons themselves are not inspected. They are `aria-hidden` decoration without a
  contract, and their value belongs to AC-2.
- **Review count**: its first match is visible.
- **Price**: exactly one price in the section, and it equals the expected price.
- **Description**: visible.

*Alternatives:*
- *Seven tests, one per item.* Rejected: that is seven page loads for one scenario, and the failure message names
  the item anyway.
- *Hard-code "Audio" and "$249.99" from the story's test data.* Rejected: the story is not the reference, and
  `shop/product-detail` contains neither value.

### D4. Capturing the POST (AC-3)

`Click Add To Cart` starts `Promise To    Wait For Response    matcher=**/api/cart/items` before it clicks the
product's button. It then waits for that promise and returns the response. `shop/cart` WEB-005_AC-1 names that
endpoint for detail pages too. The matcher filters on the URL only, and the method is asserted afterwards: if the
request used the wrong method, the test would fail with a message that says so, instead of timing out.

The test then checks:
- the request's method is `POST`;
- the request body's `product_id` is `1`. This is the field name `shop/cart` API-005_AC-2 uses. It proves that the
  button identifies the product it adds;
- the response is `ok`, and its `items` hold an entry whose `product_id` is `1`.

*Why the product ID the click sends, and not an attribute:* the spec says "identifies the product it adds" and names
no attribute. The story's `data-product-id` is an example, and examples are not requirements (interpretation rules).
The shop's attribute also has a different name. The ID that the click sends is the observable proof, whatever the
markup.

*Why the POST's own response, and not the cart page or the cart badge:* the spec says that the POST request adds the
product to the cart, and the response of that request is the cart after it. The cart page belongs to WEB-005_AC-3
and the badge to WEB-005_AC-2. A defect in either would fail this test for the wrong reason.

The test's fresh context gets its own session, so the POST only fills a new, empty cart. On the shared instance, the
request carries the space header, because the context sends it with every request (`shop.resource`).

### D5. AC-8: both ways, one test each

The requirement says that the shopper "SHALL be able to return … with the browser's back button or a navigation
link". Its scenario reads "WHEN a shopper … goes back, or follows a navigation link … THEN the products page is
shown". The scenario states the outcome for either action, so the suite checks both, one test each, and a failure
names the way that broke.
- **Back button**: `Go To Catalogue`, follow the grid's name link of "Aurora Neural Headphones", wait until the
  detail page shows that name, then Browser's `Go Back`.
- **Navigation link**: open `/products/1` directly, wait for the same detail page, then follow the header link.
  Opening the page directly proves that the link works without any history to go back to.
- **"The products page is shown"**: the URL ends with `/products`, and `${GRID}` is visible. The URL check uses the
  operator `$=`, as `checkout.robot` does with `/checkout`, because `${SHOP_URL}` differs between profiles.

*Alternative:* one test that passes when either way works. Rejected: it would leave one way unverified, and the
scenario reads as a statement about both. **Review point:** if the pair review reads "or" as "either one is enough",
drop the navigation-link test and keep the back-button test, which follows the scenario's own sequence.

### D6. AC-9: a not-found message and no detail page

`Go To Shop Page` opens the URL. Browser's `Go To` does not fail on a `404` status (task 1.1 confirms this). The test
then:
1. waits until the first not-found match in `main` is visible;
2. counts, in `main`, the "Add to Cart" buttons and the "Buy Now" links or buttons, and expects 0 of each. These are
   the detail page's two actions (AC-3 and AC-4). A broken or empty detail page would still render them. The page is
   rendered on the server, so its content is complete once the message is visible.

*The error-message rule is not applied.* `shop/interpretation-rules` says that "an error message is displayed"
means a message in an element with the alert role, or next to the field concerned. That rule is about a message
that a page shows in response to an action on it, such as a form submission. Here, the action is opening the URL, and
the whole page is the response. The spec asks for "an appropriate error state or not-found message", not for "an
error message". Requiring an alert role would demand more than the spec does.

*Two tests instead of a `[Template]`:* the spec has two scenarios, and the conventions name each test by its
criterion and its behaviour. No test file in the suite uses a template.

### D7. Test data comes from the specs

"Aurora Neural Headphones", "Add to Cart", "Buy Now", `/products`, `/products/1`, `/products/9999` and `/products/abc`
appear in `shop/product-detail` word for word. "not found" is its term "not-found message". "star" comes from its
"star rating". The two review-count forms come from the texts that WEB-003_AC-2 quotes. The endpoint `/api/cart/items`
and the field `product_id` come from `shop/cart`. The category, the price and the description come from the catalogue
API (D3). Nothing is taken from the story alone, such as "Audio", "$249.99", `data-product-id` or the status 404.
Nothing is taken from what the shop happens to show, such as "Product not found", the link text "Products", "View
details" or "out of 5 stars".

## Risks / Trade-offs

- **The product's section is found by its heading's text** (D2). If the main heading stops showing the product's
  name, the AC-1 and AC-3 tests fail on that lookup. For AC-1 that is the right outcome, because the name is one of
  its items. For AC-3 the failure names the missing heading, not the button. If a second section's `h1` also named
  the product, the lookup would match twice.
  → Task 1.1 checks that it resolves to exactly one element. `Product Detail Should Show` runs first in every test
  that uses the section, so a failure names the heading, and it does not hide a product defect.
- **The image is identified by an alt text that names the product.** A page whose product image had another alt text
  would fail AC-1, although it shows an image.
  → Accepted: the alt text is the only non-structural way to tell the product's image from the other images, and the
  failure message names the image.
- **The category badge is found by its whole text.** A badge that reads "Category: Audio" would not be found.
  → Accepted. The failure message names the badge and the category it looked for.
- **The AC-8 reading of "or"** (D5) decides whether the suite has one AC-8 test or two.
  → It is flagged as a review point, and dropping a test changes nothing else in the plan.
- **The not-found wording.** A message that says "doesn't exist" without "not found" would fail AC-9, although the
  spec might accept it.
  → The phrase is the spec's own term. The failure message shows what the page's main content says.
- **Some locators were read from HTML, not tried in a browser.** These are Playwright's accessible names, which
  element a `text=` regex matches, `:has-text()` inside `:has()`, whether any icon matches `role=img`, and
  navigation to a `404` page.
  → Task 1.1 checks each row of D2 in the running shop before the keywords are written. Any locator that resolves
  differently is changed in the resource, and its row in D2 is updated.
- **A test could pass without checking anything**, for example an absence check that runs before the page is loaded.
  → Every presence check waits for its element or asserts a count. The absence checks of AC-9 run only after the
  not-found message is visible. Task 2.3 proves that the AC-1, AC-3 and AC-9 checks can fail.
- **The AC-3 test writes to the cart.** It adds one item, in its own new session only, and never touches another
  session's cart. No preset is applied and no space is reset.
