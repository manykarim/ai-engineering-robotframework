# Lab 5 - Prompt to green: the reference

[Lab 5](../labs/lab-05-prompt-to-green/INSTRUCTIONS.md) has you automate a slice of one story through OpenSpec,
review the plan with a partner, and repair the Module 5 test from the repository's files alone. The rehearsal did all
three stories. [Transcript](../transcripts/lab-05-prompt-to-green.md).

## The reference

| Story | Slice | Tests | Keywords | Suite spec |
|---|---|---|---|---|
| WEB-004 (easier) | AC-1, AC-3, AC-6, AC-7 | `tests/ui/search.robot` | `resources/search.resource` | `openspec/specs/suite/search` |
| WEB-003 (medium) | AC-1, AC-3, AC-8, AC-9 | `tests/ui/product_detail.robot` | `resources/product_detail.resource` | `openspec/specs/suite/product-detail` |
| WEB-005 (harder) | AC-2, AC-3, AC-4, AC-9 | `tests/ui/cart.robot` | `resources/cart.resource` | `openspec/specs/suite/cart` |

Each change is archived with its proposal, design and tasks under
[`openspec/changes/archive/`](https://github.com/manykarim/ai-engineering-robotframework/tree/solutions/openspec/changes/archive).

WEB-004's suite spec, the contract its tests fulfil:

```markdown
# suite/search Specification

## Purpose
Records which search criteria of `shop/search` the suite verifies through the shop's pages, what each test checks, and which test verifies each criterion.

## Requirements

### Requirement: The home page's search input is verified (WEB-004_AC-1)
The suite SHALL verify WEB-004_AC-1 on the home page, `/`. The specification names the hero section but gives it no text, role or label. The test SHALL therefore recognise it the way a shopper does: as the first screen of the page, which opens with the page's main heading. Once the page has loaded, and before it is scrolled, the page's main heading and exactly one search input of the main content SHALL both be visible and lie entirely within the browser window. A search input in the site header SHALL NOT count. The input's placeholder or its label SHALL contain "search", ignoring case, so that it indicates its purpose. Either one is enough, because the specification says "a placeholder or label". The specification quotes no wording for either, so the test SHALL NOT expect any wording beyond that word.

#### Scenario: WEB-004_AC-1 Home Page Hero Shows Search Input
- **WHEN** the test opens `/` in a fresh browser context
- **THEN** the page's main heading and one visible search input lie within the first screen, and the input's placeholder or label contains "search"

### Requirement: Search submission is verified (WEB-004_AC-3)
The suite SHALL verify WEB-004_AC-3 with the specification's query, "headphones", on `/`. It SHALL do so once for each way of submitting that the specification names, with one test each: pressing Enter in the search input, and clicking the search form's button. After the submission, a search results section SHALL be visible and SHALL show at least one product card. One of the cards SHALL be the card of Aurora Neural Headphones, and that card SHALL show all of the following:
- the name "Aurora Neural Headphones" as visible text;
- a visible, loaded image whose alternative text names the product;
- exactly one price, written as a dollar amount with cents, which equals the price of product 1 in the shop's catalogue.

The price SHALL be read through the shop's API in the same space, because `shop/search` does not state it. The "Add to Cart" button and the link to the detail page SHALL NOT be checked: they belong to WEB-004_AC-8, which the suite does not verify here.

#### Scenario: WEB-004_AC-3 Enter Shows Matching Results
- **WHEN** the test opens `/` in a fresh browser context, enters "headphones" in the search input and presses Enter
- **THEN** a search results section lists Aurora Neural Headphones as a card with its name, a loaded image and its catalogue price

#### Scenario: WEB-004_AC-3 Search Button Shows Matching Results
- **WHEN** the test opens `/` in a fresh browser context, enters "headphones" in the search input and clicks the search button
- **THEN** a search results section lists Aurora Neural Headphones as a card with its name, a loaded image and its catalogue price

### Requirement: Clearing search results is verified (WEB-004_AC-6)
The suite SHALL verify WEB-004_AC-6 on both pages whose normal content the specification names, with one test each: the home page, `/`, whose normal content is its hero section, and the products page, `/products`, whose normal content is its product grid. Each test SHALL search for "headphones" by pressing Enter, and wait until the search results section shows the card of Aurora Neural Headphones. The shop also searches by itself shortly after the shopper types. Before the click, the test SHALL give that search time to finish, so that the results are settled, as a shopper who reads them sees them. The test SHALL then click the button in the search results section whose visible text contains "Clear search" or "Clear results", ignoring case. It SHALL accept either label on either page, because the specification quotes both. After the click, all of the following SHALL hold:
- the search results section is hidden;
- the page's normal content is visible: the hero section on `/`, recognised by the page's main heading, and the product grid on `/products`;
- the search input is empty.

#### Scenario: WEB-004_AC-6 Clear Results On Home Page
- **WHEN** the test opens `/` in a fresh browser context, searches for "headphones", waits for its results and clicks the clear button
- **THEN** the search results section is hidden, the hero section is visible and the search input is empty

#### Scenario: WEB-004_AC-6 Clear Search On Products Page
- **WHEN** the test opens `/products` in a fresh browser context, searches for "headphones", waits for its results and clicks the clear button
- **THEN** the search results section is hidden, the product grid is visible and the search input is empty

### Requirement: The empty state is verified (WEB-004_AC-7)
The suite SHALL verify WEB-004_AC-7 with the specification's query, "xyz123", on `/`, submitted by pressing Enter. The search results section SHALL then show a visible message whose visible text contains "no products", ignoring case. These are the specification's own words, from "no products were found" and from its example "No products found". The test SHALL NOT require the example's full wording, because examples are not requirements. Only a message inside the search results section SHALL count, so that another message on the page, such as the suggestion list's, cannot satisfy the test. The search results section SHALL hold no product card.

#### Scenario: WEB-004_AC-7 Unmatched Query Shows Empty State
- **WHEN** the test opens `/` in a fresh browser context, enters "xyz123" in the search input and presses Enter
- **THEN** the search results section shows a visible message containing "no products", and no product card
```

Its tests:

```robotframework
*** Settings ***
Documentation       Product search on the home page and the products page (spec: shop/search).

Resource            resources/shop.resource
Resource            resources/api.resource
Resource            resources/search.resource

Suite Setup         Run Keywords    Open Shop Browser    AND    Open Shop API
Suite Teardown      Close Browser
Test Setup          Start Shop Test

Test Tags           WEB-004    ui


*** Test Cases ***
WEB-004_AC-1 Home Page Hero Shows Search Input
    [Documentation]    The first screen of / shows the main heading and a search input whose placeholder or label says "search".
    Go To Home Page
    Hero Search Input Should Be Shown
    Search Input Should Indicate Its Purpose

WEB-004_AC-3 Enter Shows Matching Results
    [Documentation]    Searching "headphones" with Enter lists Aurora Neural Headphones with its name, image and price.
    ${product}=    Get Product From API    1
    Go To Home Page
    Submit Search With Enter    headphones
    Search Results Should List    Aurora Neural Headphones
    Search Result Card Should Show    Aurora Neural Headphones    ${product}[price]

WEB-004_AC-3 Search Button Shows Matching Results
    [Documentation]    Searching "headphones" with the search button lists Aurora Neural Headphones with its name, image and price.
    ${product}=    Get Product From API    1
    Go To Home Page
    Submit Search With Button    headphones
    Search Results Should List    Aurora Neural Headphones
    Search Result Card Should Show    Aurora Neural Headphones    ${product}[price]

WEB-004_AC-6 Clear Results On Home Page
    [Documentation]    On /, clearing the results hides them, shows the hero again and empties the search input.
    Go To Home Page
    Submit Search With Enter    headphones
    Search Results Should List    Aurora Neural Headphones
    Clear Search Results
    Search Results Should Be Hidden
    Hero Section Should Be Shown
    Search Input Should Be Empty

WEB-004_AC-6 Clear Search On Products Page
    [Documentation]    On /products, clearing the search hides the results, shows the grid again and empties the search input.
    Go To Catalogue
    Submit Search With Enter    headphones
    Search Results Should List    Aurora Neural Headphones
    Clear Search Results
    Search Results Should Be Hidden
    Product Grid Should Be Shown
    Search Input Should Be Empty

WEB-004_AC-7 Unmatched Query Shows Empty State
    [Documentation]    Searching "xyz123" shows a "no products" message in the search results, and no card.
    Go To Home Page
    Submit Search With Enter    xyz123
    Search Results Should Be Shown
    Empty Search Message Should Be Shown
    Search Results Should Hold No Cards
```

The repaired Module 5 test:

```diff
--- a/tests/ui/catalogue.robot
+++ b/tests/ui/catalogue.robot
@@ -45,9 +45,8 @@ WEB-002_AC-2 Categories Filter Group
 
 WEB-002_AC-4 Rating Filter
     [Documentation]    A rating filter offers an unchecked minimum-rating checkbox.
-    [Tags]    broken
     Go To Catalogue
-    Checkbox Should Be Unchecked    4 stars and up
+    Checkbox Should Be Unchecked    4 stars & up
 
 WEB-002_AC-7 Audio Filter Shows Only Audio
     [Documentation]    With only "Audio" checked, the grid shows only audio products.
```

## Why it is a good result

- **The suite spec names each criterion and what is checked,** and no locator, keyword or file.
- **One test per criterion, or one per way of meeting it:** AC-3 has a test for Enter and one for the search button,
  AC-6 one for each page.
- **Keyword calls only.** Every locator sits in `resources/search.resource`, built from roles, labels and visible
  text.
- **The expected texts are the specification's own:** "headphones", "Aurora Neural Headphones", "xyz123".
- **Each test creates its own state:** its own browser context, and no preset.

## What to debrief

- **The cause of `WEB-002_AC-4 Rating Filter`.** The test waits for a checkbox named "4 stars and up", and
  `openspec/specs/shop/catalogue` quotes "4 stars & up". An agent with the specifications and no live page finds it.
- **The time it takes.** The rehearsal's agent needed 14 minutes to propose WEB-004 and 7 to apply it. The
  two-criteria slice fits a tight lab.

## Compare yours

```bash
git fetch upstream solutions
REF=$(git log -1 --format=%H --grep '^lab-05-prompt-to-green' upstream/solutions)
git diff "$REF" -- tests/ui/search.robot resources/search.resource openspec/specs/suite/search/spec.md
```

The lines marked `-` are the reference's, the lines marked `+` yours. No `upstream` remote yet? [Add it first](README.md#compare-your-files-with-the-reference).

For another story, take its files from the table.
