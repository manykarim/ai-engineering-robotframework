# Tasks

## 1. Resources

- [x] 1.1 Confirm the locators of design D2 in the running shop before you write any keyword. Planning checked them
  already, and this repeats the check against the shop as it runs now. Use
  `uv run robotcode repl --plain --no-history`. Import `resources/shop.resource` and `resources/catalogue.resource`,
  and open every new context with `Start Shop Test`, so that it carries the space when one is set. Search writes
  nothing. Do not apply a preset, and do not reset the shop.
  - **Home page, before a search.** Open `/`. Check that each of these resolves to exactly one element:
    - `role=main >> role=heading[level=1]`;
    - `role=main >> role=search`;
    - `role=main >> role=searchbox`;
    - `role=main >> role=search >> button:has-text("Search")`.

    Check that `role=banner >> role=searchbox` counts 0. Before anything scrolls, read `Get Viewport Size` and the
    `Get BoundingBox` of the main heading and of the search input. Check that each lies entirely within the window.
    Planning measured 284 to 457 px and 581 to 624 px in a 1280 × 720 window.

    Check that `role=region[name=/search results/i]` counts 0 while the section is hidden. Read the input's
    `placeholder`, and check that `role=searchbox[name=/search/i]` finds the input.
  - **Enter.** Fill the input with "headphones" and press Enter in it with `Press Keys`. Then check:
    - the results section becomes visible;
    - `article:has-text("Aurora Neural Headphones")` inside it resolves to exactly one element;
    - inside that card, the image named `/Aurora Neural Headphones/i`, the heading and `${CARD PRICE}` each resolve
      to exactly one element;
    - the image's `naturalWidth` is above 0, and the price reads "$249.99".
  - **Clear on `/`.** Wait 1 s, then click the clear-button locator, which must resolve to exactly one element.
    Check that the section becomes hidden, the main heading stays visible and the input's `value` is empty. After
    another 1.5 s, check that the results section still counts 0.
  - **Button.** In a new context, open `/`, fill in "headphones" and click the search button. Check that the card of
    Aurora Neural Headphones becomes visible and that the URL is still `/`.
  - **Clear on `/products`.** Open `/products` with `Go To Catalogue`, search for "headphones" with Enter, wait 1 s,
    and click the clear button. Check that the section becomes hidden, `${GRID}` is visible and the input is empty.
  - **Empty state.** On `/`, search for "xyz123" with Enter. Check that the first match of
    `role=region[name=/search results/i] >> text=/no products/i` becomes visible, and that the section holds 0
    `role=article`. Check that "No results" in the suggestions is outside the section.

  Verify: every row of D2 resolves as the table says. Where a row does not, update that row and its reason in
  `design.md` before you go on.
- [x] 1.2 Confirm that the keywords and variables this change reuses exist:
  - `Go To Shop Page` in `resources/shop.resource`;
  - `Go To Catalogue`, `Format Price`, `${GRID}` and `${CARD PRICE}` in `resources/catalogue.resource`;
  - `Get Product From API` in `resources/api.resource`.

  Verify with `uv run --no-sync python -m robot.libdoc <file> list` for each resource, and read the
  `*** Variables ***` section of `catalogue.resource`. If anything is missing, stop and report it. Do not write it
  again.
- [x] 1.3 Write `resources/search.resource` per design D1 to D7. It imports `shop.resource` and `catalogue.resource`.
  It holds the locators of D2 as variables, and `${SEARCH SETTLE}` (1 s) with a comment that says why it exists
  (D6). It holds these keywords:
  - Pages: `Go To Home Page`, which opens `/`.
  - AC-1 (D3): `Hero Search Input Should Be Shown` and `Search Input Should Indicate Its Purpose`.
  - Searching (D4): `Submit Search With Enter    ${query}` and `Submit Search With Button    ${query}`.
  - Results (D4): `Search Results Should Be Shown`, `Search Results Should List    ${name}`,
    `Search Result Card    ${name}`, which returns the card's locator, and
    `Search Result Card Should Show    ${name}    ${amount}`.
  - AC-6 (D6): `Clear Search Results`, which waits `${SEARCH SETTLE}` and then clicks. Also
    `Search Results Should Be Hidden`, `Hero Section Should Be Shown`, `Product Grid Should Be Shown` and
    `Search Input Should Be Empty`.
  - AC-7 (D7): `Empty Search Message Should Be Shown` and `Search Results Should Hold No Cards`.

  Every failure message names what is missing, and what was found instead where that helps. Each keyword that is not
  self-explanatory gets a one-line `[Documentation]`, as in `catalogue.resource`.

  Verify:
  - `uv run robotcode analyze code resources/search.resource` reports no errors;
  - the file contains no `id=`, `#id`, `.class`, `data-` attribute, `href` or `xpath` locator;
  - every locator is built from a role, a label or visible text, with no exception. In particular, the file contains
    no `section:has(h1)` and no other locator built from the markup alone (D2);
  - every UI word in it can be found in `openspec/specs/shop/search/spec.md`, ignoring case: "search",
    "search results", "Clear search", "Clear results" and "no products";
  - `git status -- resources` shows `resources/search.resource` as the only new file. `git diff -- resources` shows
    only the participant's earlier edits.

## 2. Search tests

- [x] 2.1 Write `tests/ui/search.robot` per design D1, with exactly these six tests from `specs/suite/search`:
  - `WEB-004_AC-1 Home Page Hero Shows Search Input`: `Go To Home Page`, `Hero Search Input Should Be Shown`,
    `Search Input Should Indicate Its Purpose`.
  - `WEB-004_AC-3 Enter Shows Matching Results`: read product 1 with `Get Product From API`, then `Go To Home Page`,
    `Submit Search With Enter` with "headphones", `Search Results Should List` and `Search Result Card Should Show`.
    Both take "Aurora Neural Headphones", and the card check takes the product's price.
  - `WEB-004_AC-3 Search Button Shows Matching Results`: the same steps, with `Submit Search With Button`.
  - `WEB-004_AC-6 Clear Results On Home Page`: `Go To Home Page`, `Submit Search With Enter` with "headphones",
    `Search Results Should List` with "Aurora Neural Headphones", `Clear Search Results`,
    `Search Results Should Be Hidden`, `Hero Section Should Be Shown`, `Search Input Should Be Empty`.
  - `WEB-004_AC-6 Clear Search On Products Page`: the same steps, starting with `Go To Catalogue` and ending with
    `Product Grid Should Be Shown` instead of the hero.
  - `WEB-004_AC-7 Unmatched Query Shows Empty State`: `Go To Home Page`, `Submit Search With Enter` with "xyz123",
    `Search Results Should Be Shown`, `Empty Search Message Should Be Shown`, `Search Results Should Hold No Cards`.

  Each test has a one-line `[Documentation]` and calls keywords only. Verify:
  - `uv run --no-sync python hooks/no_inline_locators.py tests/ui/search.robot` reports nothing;
  - `uv run robotcode analyze code tests/ui/search.robot` reports no errors;
  - `uv run robotcode robot --dryrun --include WEB-004` lists exactly these six tests, each tagged `WEB-004` and
    `ui`;
  - every expected text in the file can be found in `openspec/specs/shop/search/spec.md`: "headphones",
    "Aurora Neural Headphones" and "xyz123". The product ID `1` comes from `/products/1` there.
- [x] 2.2 Run the new tests against the local shop. Verify:
  - `uv run robotcode robot tests/ui/search.robot` passes 6 of 6;
  - each test passes on its own, with `uv run robotcode robot --test "<test name>"`;
  - the file passes three runs in a row.

  If a test fails, read the failure in `results/` and state the evidence before you change anything. Change the
  keyword or the locator, never an expectation that the spec sets.
- [x] 2.3 Prove that each check can fail. Make a throwaway copy of `tests/ui/search.robot` under `results/`, which git
  ignores, and change it:
  - in the AC-1 test, replace `Go To Home Page` with `Go To Shop Page    /cart`;
  - in the AC-3 Enter test, search for "xyz123" instead of "headphones";
  - in the AC-3 button test, read product 2 instead of product 1 with `Get Product From API`;
  - in the AC-6 home-page test, delete the `Clear Search Results` step;
  - in the AC-6 products-page test, replace `Clear Search Results` with `Submit Search With Enter    headphones`;
  - in the AC-7 test, search for "headphones" instead of "xyz123".

  Run the copy with `uv run robotcode robot results/<copy>.robot`. Verify that all six tests fail, and that their
  messages name, in order:
  1. the missing search input in the main content;
  2. the missing card of Aurora Neural Headphones;
  3. the price the card showed and the one expected;
  4. the results section that is still shown;
  5. the results section that is still shown;
  6. the missing "no products" message.

  Delete the copy afterwards. `git status -- tests resources` then shows only `tests/ui/search.robot` and
  `resources/search.resource` as new, besides the participant's earlier edits.

## 3. Close-out

- [x] 3.1 Validate the change. Verify that `openspec validate add-search-ui-tests --strict` passes.
- [x] 3.2 Run the new tests and the rest of the suite one last time. Verify:
  - `uv run robotcode robot tests/ui/search.robot` passes 6 of 6;
  - `uv run robotcode robot --exclude broken` runs the whole suite, and the six new tests pass. A failure of any
    other test is reported with its message and left alone, because it is outside this change;
  - no step applied a preset or reset the shop.
