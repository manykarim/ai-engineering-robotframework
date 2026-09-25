# Spec Delta

## Purpose

Records which search criteria of `shop/search` the suite verifies through the shop's pages, what each test checks, and which test verifies each criterion.

## ADDED Requirements

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
