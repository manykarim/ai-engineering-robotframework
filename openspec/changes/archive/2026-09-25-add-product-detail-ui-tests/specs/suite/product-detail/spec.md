# Spec Delta

## Purpose

Records which product-detail criteria of `shop/product-detail` the suite verifies through the shop's pages, what each test checks, and which test verifies each criterion.

## ADDED Requirements

### Requirement: Product core information is verified (WEB-003_AC-1)
The suite SHALL verify WEB-003_AC-1 on `/products/1`, the seeded product Aurora Neural Headphones. Once the page has loaded, the product's own section SHALL show all of the following: a visible, loaded image whose alternative text names the product; the name "Aurora Neural Headphones" as its main heading; a category badge whose visible text is the product's category; a visible star rating; a review count written as a whole number, as "<n> reviews" or "(<n>)"; the product's price, written as a dollar amount with cents; and the product's description. The expected category, price and description SHALL be those of product 1 in the shop's catalogue, read through the shop's API in the same space, because `shop/product-detail` does not state them. The star rating and the review count SHALL be checked for presence only: their values belong to WEB-003_AC-2, which the suite does not verify here.

#### Scenario: WEB-003_AC-1 Detail Page Shows Product Information
- **WHEN** the test opens `/products/1` in a fresh browser context
- **THEN** the product's section shows its image, the name "Aurora Neural Headphones", a badge with the product's category, a star rating, a review count, the product's price and the product's description

### Requirement: The Add to Cart button is verified (WEB-003_AC-3)
The suite SHALL verify WEB-003_AC-3 on `/products/1`. The product's own section SHALL show a button whose visible text contains "Add to Cart", ignoring case. The "Add to Cart" buttons on the cards of recommended products further down the page SHALL NOT count. The test SHALL click that button. The click SHALL send a POST request whose body carries the product ID 1, which shows that the button identifies the product it adds. The request SHALL succeed, and the cart it returns SHALL hold an entry for product 1. The test SHALL NOT require any particular attribute on the button, because the specification names none.

#### Scenario: WEB-003_AC-3 Add To Cart Posts The Product
- **WHEN** the test opens `/products/1` in a fresh browser context and clicks the product's "Add to Cart" button
- **THEN** a POST request carrying product ID 1 is sent, it succeeds, and the cart it returns holds product 1

### Requirement: Navigation back to the catalogue is verified (WEB-003_AC-8)
The suite SHALL verify WEB-003_AC-8 for both ways the specification names, with one test each: the browser's back button and a navigation link. For the back button, the test SHALL open `/products`, follow the name link of Aurora Neural Headphones in the product grid, wait for its detail page, and go back. For the navigation link, the test SHALL open `/products/1` directly, so that no browser history leads back, and follow the site header's link to `/products`. In both tests, the products page SHALL then be shown: the URL's path SHALL be `/products`, and the product grid SHALL be visible. The specification quotes no text for the navigation link, so the test SHALL find it by its target, `/products`, and SHALL NOT expect any wording.

#### Scenario: WEB-003_AC-8 Back Button Returns To Catalogue
- **WHEN** the test opens `/products`, follows the link of Aurora Neural Headphones to its detail page, and goes back with the browser's back button
- **THEN** the URL's path is `/products` and the product grid is visible

#### Scenario: WEB-003_AC-8 Navigation Link Returns To Catalogue
- **WHEN** the test opens `/products/1` in a fresh browser context and follows the site header's navigation link to `/products`
- **THEN** the URL's path is `/products` and the product grid is visible

### Requirement: Invalid product IDs are verified (WEB-003_AC-9)
The suite SHALL verify WEB-003_AC-9 for both IDs the specification's scenarios name: `9999`, a number that no product has, and `abc`, which is not a number. For each, the test SHALL open `/products/{id}`. The page's main content SHALL then show a visible message that contains "not found", ignoring case and whether the two words are joined by a space or a hyphen. The main content SHALL NOT show a product detail page: it SHALL hold no button whose visible text contains "Add to Cart", and no link or button whose visible text contains "Buy Now". The test SHALL NOT require an HTTP status or any further wording, because the specification requires neither.

#### Scenario: WEB-003_AC-9 Unknown Product ID Shows Not Found
- **WHEN** the test opens `/products/9999` in a fresh browser context
- **THEN** the main content shows a visible not-found message, no "Add to Cart" button and no "Buy Now" link

#### Scenario: WEB-003_AC-9 Non-Numeric Product ID Shows Not Found
- **WHEN** the test opens `/products/abc` in a fresh browser context
- **THEN** the main content shows a visible not-found message, no "Add to Cart" button and no "Buy Now" link
