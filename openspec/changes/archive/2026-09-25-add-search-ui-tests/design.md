# Design

## Context

See `proposal.md` for the motivation and `specs/suite/search/spec.md` for what each test checks. The facts below come
from the local shop at version `0.3.0`, with the space in its reset state (`clean` and `stage1` both hold). They were
read from:
- the served HTML of `/` and `/products`;
- `/static/app.js`;
- the results the shop renders for "headphones" and "xyz123";
- `GET /api/products/` and `GET /api/search/?query=headphones`.

Unlike the earlier changes, planning also tried the locators of D2 in a browser. It used `uv run robotcode repl` with
`Start Shop Test`, in fresh contexts. Search writes nothing, so the probe changed no state. Task 1.1 repeats the
checks before any keyword is written.

- **The search form.** On `/` and on `/products`, `main` holds exactly one form with the `search` role. It holds:
  - a search input, role `searchbox`, labelled "Search products" on `/` and "Search the catalogue" on `/products`.
    Its placeholders are "Search headphones, notebooks, wearables..." and "Search the full collection...";
  - one button, whose visible text is "Search".

  There is no other search form on either page.
- **The hero.** On `/`, the form sits in the first section of `main`. It is a plain `<section>` with no role and no
  name. The page has one `h1`, "Upgrade your workspace with AI-first essentials", and this section is the only one
  that holds it. In a new context's window of 1280 × 720, before any scrolling, the heading spans 284 to 457 px from
  the top and the search input 581 to 624 px. The site header holds no search input, and the main content of `/cart`
  holds none either.
- **The results section.** Each page has a `section` with the region role and the label "Search results". It stays
  hidden until a search. It holds:
  - a heading, "Search results";
  - a button that reads "Clear results" on `/` and "Clear search" on `/products`;
  - a grid that the results fill.

  A role lookup finds no region while the section is hidden.
- **Submitting.** Enter and the button both submit the form. The page does not navigate, and the URL stays `/`. The
  script fetches the results as HTML from an endpoint that no spec names, renders them into the section, and then
  shows the section. A query shorter than two characters does nothing.
- **The shop also searches while the shopper types.** Every input event starts two 300 ms timers:
  - one asks `/api/search/suggest` for suggestions and shows them in a dropdown under the input;
  - the other runs the same search a submit runs.

  Neither a submit nor the clear button cancels these timers. Planning measured the effect on `/`: Clear was clicked
  as soon as the results for "headphones" appeared. The section was then hidden and the input empty. 1.5 s later, the
  results were shown again, the input was still empty, and the suggestions dropdown was open. When the test waited
  1.5 s before clicking Clear, the section stayed hidden.
- **A result card.** For "headphones", the section holds one `article`, Aurora Neural Headphones. It holds:
  - an image whose alt text is "Aurora Neural Headphones product photo". It had loaded, with a `naturalWidth` of
    1024 in a 1280 × 720 window. It is the card's only element with the `img` role, because the star icons are
    `aria-hidden`;
  - an `h3` whose text is the name, and a link to `/products/1`;
  - a category badge, the description and a rating group;
  - one price, "$249.99". `GET /api/products/` lists product 1 at 249.99;
  - an "Add to cart" button and a "View details" link.
- **The empty state.** For "xyz123", the section holds the paragraph "No products matched your query." and no
  `article`. 300 ms after typing, the suggestions dropdown opens in the hero and shows "No results", which is outside
  the results section. No element with the alert role appears.
- **The normal content stays.** While results are shown, the hero on `/` and the product grid on `/products` stay
  visible. The shop hides neither, and the spec does not require it to.
- **Existing keywords.**
  - `resources/shop.resource` has `Go To Shop Page`.
  - `resources/catalogue.resource` has `Go To Catalogue`, `${GRID}`, `${CARD PRICE}` and `Format Price`.
  - `resources/api.resource` has `Get Product From API`, an uncommitted edit from the product-detail work.
  - `resources/product_detail.resource` and `resources/cart.resource` are untracked. This change depends on neither.
- The shipped suite verifies no WEB-004 criterion on purpose (`workshop/baseline-suite`).

## Goals / Non-Goals

**Goals:**
- Six tests that pass in a freshly reset space, alone or together, in any order, locally and on the shared instance.
- Every locator this change writes is built from roles, labels and visible text (D2). None uses an id, a class or a
  `data-test` hook, so the tests also pass under the drift stages `stage1` to `stage4`.

**Non-Goals:**
- The rest of WEB-004:
  - AC-2: the AC-6 test on `/products` uses that page's search form but does not check it as AC-2 would;
  - AC-5: no test looks at the suggestions. The AC-7 test only makes sure it cannot count their "No results";
  - AC-8: the AC-3 tests check neither the card's "Add to Cart" button nor its link;
  - AC-9: the search API.
- Whether the results replace the normal content or overlay it. That is a note in the story, not a requirement.
- Case-insensitive search, special characters, the typing delay and how fast suggestions come. These are story notes
  outside this slice.
- Whether every result matches the query. `shop/search` doesn't say which fields a search matches. The AC-3 tests
  check that Aurora Neural Headphones is listed, as the scenario says. The AC-7 test shows that a query without matches
  lists nothing.
- Updating `docs/facilitator/suite-outcomes.toml`. It records the shipped suite for the maintainers.

## Decisions

### D1. Two new files; the shipped resources stay as they are

- `tests/ui/search.robot` has the same frame as `tests/ui/product_detail.robot`:
  - Suite Setup `Open Shop Browser` and `Open Shop API`, Suite Teardown `Close Browser`, Test Setup
    `Start Shop Test`;
  - `Test Tags    WEB-004    ui`.

  It imports `shop.resource`, `api.resource` and `search.resource`. The API session serves the AC-3 tests only (D4).
- `resources/search.resource` holds every locator and keyword of the search form, the results section, the clear
  button and the empty state. It imports `shop.resource`, and `catalogue.resource` for `Go To Catalogue`, `${GRID}`,
  `${CARD PRICE}` and `Format Price`.

*Alternatives:*
- Add the keywords to `catalogue.resource`. Rejected: that file is about the products page, search lives on two
  pages, and the file holds the participant's uncommitted work.
- Import `product_detail.resource` for `Products Page Should Be Shown`. Rejected: that keyword also checks the URL,
  and one wait for `${GRID}` does not justify depending on untracked work.

### D2. Locators

Every locator is written in `resources/search.resource`. Tests contain none. Planning found each row to resolve as
described.

| Element | Locator | Why |
|---|---|---|
| Main heading (AC-1, AC-6) | `role=main >> role=heading[level=1]` | A role: the page's main heading, which opens the hero (see below). Found exactly once on `/`. |
| Search form | `role=main >> role=search` | A role: the form's search landmark. Found exactly once on each page. |
| Search input | `role=main >> role=searchbox` | A role. The main content holds exactly one on each page, and the site header holds none. It is not scoped to the form, because the spec asks for "a search form or input". |
| Search button (AC-3) | `${SEARCH FORM} >> button:has-text("Search")` | Visible text: the spec's word in "the search button". The form holds only this button. |
| Results section | `role=region[name=/search results/i]` | A role and its label, which is the spec's term "search results section" (see below). |
| Result cards (AC-7) | `${RESULTS} >> role=article` | A role. It counts the cards. |
| A product's card (AC-3, AC-6) | `${RESULTS} >> article:has-text("<product name>")` | Visible text: the card that shows the product's name, ignoring case. `cart.resource` finds cart lines the same way. |
| Card name (AC-3) | `${CARD} >> role=heading` | A role. Its visible text must contain the name. |
| Card image (AC-3) | `${CARD} >> role=img[name=/<product name>/i]`, with the name regex-escaped | An image has no visible text, so its alt text, which is its accessible name, identifies it. `product_detail.resource` finds the product's image the same way. |
| Card price (AC-3) | `${CARD} >> ${CARD PRICE}` | Reuses the price pattern of `catalogue.resource`: an element whose whole text is a dollar amount with cents. |
| Clear button (AC-6) | `${RESULTS} >> :is(button:has-text("Clear search"), button:has-text("Clear results"))` | Visible text, ignoring case: either label, as the spec quotes both. The scope is the results section. |
| Empty-state message (AC-7) | `${RESULTS} >> text=/no products/i`, first match | Visible text: the spec's words (D7). The scope leaves out the suggestions' "No results". |
| Product grid (AC-6) | `${GRID}` | Reused from `catalogue.resource`. |

**The hero is the first screen, not a container.** The spec names the hero section, but it gives it no text, no role
and no label. In the markup, the hero is a plain `<section>` with neither role nor name (Context). So no role, label or
visible text can find it as a container. The tests recognise the hero the way a shopper does: it is the part of the
home page that is seen first, before any scrolling, and it opens with the page's main heading. So AC-1 checks where
the main heading and the search input lie, not what contains them (D3). Alternatives:
- *`role=main >> section:has(h1)`*, the section that holds the main heading. Rejected: it rests on the markup alone,
  on `section` and `h1`. It is built from no role, label or visible text, which the plan-review checklist requires.
  Planning found that it resolves to the hero.
- *`role=main >> section >> nth=0`.* Rejected: it rests on the order of the sections alone.
- *The heading's text.* Rejected: it is marketing copy that the spec doesn't contain.
- *`role=heading[level=1]` inside the filter.* Rejected: CSS `:has()` does not take a role selector, and
  `internal:has=` is internal to Playwright (as in the product-detail design).
- **Review point:** the first-screen reading depends on the window size and on the hero's height (Risks). If the pair
  prefers a container, the fallback is `section:has(h1)`, recorded as a deliberate exception to the checklist.

**The results section is found by its role and label.** The interpretation rules restrict accessible names to where
a requirement speaks of a label or a name, so that quoted text is never matched against a name. The spec quotes no
text for this section. It speaks of "a search results section", and the section's label, "Search results", is what
assistive technology announces for it. `docs/conventions.md` (section 3) puts a role and its accessible name first in
the stable contract.
- *Alternative:* the heading's visible text, `role=main >> section:has(h2:has-text("Search results"))`. Planning
  found that it resolves to the same element. Rejected: it depends on the heading's level and on how sections nest,
  as `${GRID}` shows with its `:not(:has(section))`.
- **Review point:** if the pair prefers visible text here, swap the locator. Nothing else in the plan changes.

### D3. AC-1: the input and its purpose

- `Hero Search Input Should Be Shown` runs right after the page is opened, before anything scrolls:
  - it asserts that the main content holds exactly one `searchbox`, and waits until it is visible;
  - it waits until the main heading is visible;
  - it reads the window's size with `Get Viewport Size`, and the positions of the main heading and of the input with
    `Get BoundingBox`. Each must lie entirely within the window: its top at 0 or lower down, and its bottom no lower
    than the window's height. The failure message gives the element's top, its bottom and the window's height.
- `Search Input Should Indicate Its Purpose` passes when the input's `placeholder` contains "search", ignoring case,
  or when the input has an accessible name that contains "search". The spec says "a placeholder or
  label", so the label is a place where a name is meant, and the interpretation rules allow the accessible name there.
  On a failure, the message shows the placeholder and says that no label names a search.

*Why "search":* the spec calls the field a "search input". A placeholder or label indicates its purpose when it says
that the field is for searching. The shop's label, "Search products", and its placeholder both do.
- *Alternative:* any non-empty placeholder or label. Rejected: "Type here" would pass without indicating any purpose.
- **Review point:** if the pair reads "indicating its purpose" more broadly, for example to accept "Find products",
  relax the check to a non-empty placeholder or label.

### D4. Submitting a search, and the result card

- `Submit Search With Enter    ${query}` fills the search input with `Fill Text`, then presses Enter in it with
  `Press Keys`.
- `Submit Search With Button    ${query}` fills it the same way, then clicks the search button.
- `Search Results Should Be Shown` waits until the results section is visible.
- `Search Results Should List    ${name}` calls `Search Results Should Be Shown`, then waits until the card for `name`
  is visible. So a failure names what is missing: the section, or the card.
- `Search Result Card Should Show    ${name}    ${amount}` checks the card. Each failure message names the missing
  item:
  - its heading's visible text contains `name`, ignoring case;
  - its image is visible and loaded, meaning that its `naturalWidth` is above 0. Browser's assertion retries until
    the timeout, so a slow load does not fail the check;
  - it shows exactly one price, and that price equals `Format Price` of `amount`.
- A helper, `Search Result Card    ${name}`, returns the card's locator, as `Product Section` does in
  `product_detail.resource`.

The AC-3 tests read the expected price with `Get Product From API    1`. `shop/search` ties Aurora Neural Headphones
to `/products/1` in its WEB-004_AC-8 scenario, and it states no price. The test `WEB-002_AC-1 Card Prices Are The
Product Prices` compares with the catalogue API the same way.

### D5. AC-3: both ways of submitting, one test each

The requirement names both ways: "either by pressing Enter or by clicking the search button". Its scenario uses
Enter. There is one test for each way, so a failure names the way that broke.

**What these tests can't show.** The shop runs the same search 300 ms after the last keystroke (Context). So neither
test can tell whether Enter or the button produced the results, or the typing did. What they do show:
- after a submission by that means, the results section lists the right card;
- the submission doesn't break the page. A submit that reloaded it, or navigated to a page without results, would
  fail.

To tell them apart, a test would have to watch the shop's own results request, whose endpoint no spec names. The
revision of WEB-004_AC-9 says that the pages load their results "from the shop itself". Or it would have to require
the results within 300 ms, which is a race.

**Review point:** if the pair finds that the button test adds too little, drop it and keep the Enter test. That test
follows the spec's scenario.

### D6. AC-6: let the search settle, clear, then check. One test per page

**Settling.** `Clear Search Results` first waits `${SEARCH SETTLE}`, which is 1 s, with BuiltIn `Sleep` and a reason.
It then clicks the clear button. Without the wait, the click comes before the shop's own search after typing. That
search then shows the results again (Context), so the test would pass at the moment it checks, while the page shows
results a moment later. The results are settled when the shopper reads them, and that is the state the spec's
"When search results are displayed" describes. 1 s is more than three times the 300 ms delay, with room
for a request on the shared instance.

*Alternatives:*
- *Wait for an event instead of a time.* Rejected: when the shop's own search finishes, the page shows nothing new,
  because it renders the same results again. The only trace is its request, to an endpoint that no spec names.
- *Wait for the suggestions, which `/api/search/suggest` delivers (WEB-004_AC-5).* Rejected: they run on a separate
  timer, so they don't prove that the search has finished. The AC-6 tests would also fail whenever AC-5 does.
- *Click at once and treat the returning results as a defect.* Rejected: the spec states no timing, and a shopper
  rarely clicks within 300 ms of the last keystroke. The tests would fail on the clean shop. This observation is
  reported with the change instead.

**Two tests.** The spec names two normal contents, the hero section and the product grid, and two labels. The story's
revision says that the two labels are shown on different pages. One test per page verifies each page with the content
it returns to:
- `/`: `Go To Home Page`, then the hero comes back;
- `/products`: `Go To Catalogue`, which waits for the grid, and then the grid comes back.

The clear keyword accepts either label on either page, because the spec allows either.

**After the click**, in this order:
1. `Search Results Should Be Hidden` waits until the section is hidden;
2. `Hero Section Should Be Shown` waits until the page's main heading is visible, or `Product Grid Should Be Shown`
   until the grid is. The hero check does not require the first screen: the click scrolls the clear button into
   view, and the spec asks for the hero to be shown again, not for the page to scroll back;
3. `Search Input Should Be Empty` asserts that the input's `value` is empty.

Before any of this, the test has already seen the section with the same locator, through `Search Results Should
List`. So "hidden" can't pass because the locator is wrong.

### D7. AC-7: a message inside the results, and no card

- `Empty Search Message Should Be Shown` waits until the first match of the empty-state locator is visible.
- `Search Results Should Hold No Cards` then asserts that the section holds 0 `article`s. The section is shown only
  after its content has been rendered, so the count runs on complete content.

*Why "no products":* the spec's normative wording is "a visible message states that no products were found", and its
example is "No products found". The shop's message, "No products matched your query.", contains "no products".
- *"No products found".* Rejected: it is an example, and examples are not requirements. The shop's message would
  fail it.
- *"not found".* Rejected: the shop's message doesn't contain it, and the spec's normative wording doesn't use it.
- *A regex of synonyms, such as "nothing matched".* Rejected: it invents wording that the spec doesn't contain.

*Why the scope:* the suggestions dropdown shows "No results" in the hero (Context). A message outside the results
section must not satisfy the test.

*Why no card:* the query matches no product. A message next to product cards would contradict it.

### D8. Test data comes from the specs

These values appear in `shop/search` word for word:
- "headphones", "Aurora Neural Headphones" and "xyz123";
- "Clear search" and "Clear results";
- `/`, `/products` and `/products/1`, which gives the product ID 1;
- "no products", from "no products were found" and "No products found";
- "search", from "search input", "search button" and "search results section".

The price comes from the catalogue API (D4). The settle time, 1 s, is chosen from the shop's 300 ms delay (D6). The
first screen is the window of a new context, 1280 × 720 by Browser's default. The keyword reads its size rather than
hard-coding it (D3).

Nothing comes from what the shop happens to show, such as:
- "No products matched your query.", "No results" or "$249.99";
- "Search products", "Search the catalogue" or the placeholders;
- the hero's heading.

## Risks / Trade-offs

- **The typing hides which submission produced the results** (D5).
  → Accepted. The tests verify the outcome that the scenario states. The limitation is written down here.
- **The settle wait is a fixed time** (D6). It costs 1 s in each AC-6 test. On a very slow instance, the shop's own
  search could still end after the click.
  → The delay it waits for is the shop's fixed 300 ms, and 1 s leaves room. The symptom would be results shown again
  after Clear. If that happens on the shared instance, raise `${SEARCH SETTLE}` rather than remove it.
- **The hero is judged by position** (D2, D3). In the default window, the search input ends 96 px above the bottom
  of the first screen. A taller hero or a smaller window would fail AC-1, although the input would still sit in the
  hero's markup.
  → Task 1.1 measures the positions again. The failure message gives them, with the window's height. The review
  point in D2 names the fallback.
- **The purpose check requires the word "search"** (D3). A label that states the purpose in other words would fail.
  → Flagged as a review point.
- **The empty state must say "no products"** (D7). "Nothing matched" would fail, although the spec might accept it.
  → These are the spec's own words. The failure message names the phrase it looked for.
- **The image is identified by an alt text that names the product**, as on the detail page.
  → Accepted. The failure message names the image.
- **A role lookup skips hidden elements**, so the results section counts as "hidden" when it is gone too.
  → That satisfies the spec, which asks for the results to be hidden. Every test first sees the section through the
  same locator (D6).
- **A test could pass without checking anything**, for example a count that runs before the results are rendered.
  → Every presence check waits for its element. Every absence check runs after a presence check on the same section.
  Task 2.3 proves that the AC-1, AC-3, AC-6 and AC-7 checks can fail.
- **The AC-3 tests depend on `Get Product From API`, which is not committed yet.**
  → Task 1.2 checks that it exists. If it is missing, stop and report it rather than write it again.
- **No state changes.** Search writes nothing. No preset is applied and no space is reset.
