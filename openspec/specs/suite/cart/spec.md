# suite/cart Specification

## Purpose
Records which cart criteria of `shop/cart` the suite verifies through the shop's pages, what each test checks, and which test verifies each criterion.

## Requirements

### Requirement: The cart badge update is verified (WEB-005_AC-2)
The suite SHALL verify WEB-005_AC-2 with one test for each scenario in the specification: the desktop navigation and the mobile navigation. Each test SHALL start in a fresh browser context, with an empty cart. It SHALL open `/products/1` and click the product's own button whose visible text contains "Add to Cart", ignoring case. Before it looks at the badge, the test SHALL confirm that the add request succeeded, so that a failing API is reported as a failing API and not as a wrong badge. It SHALL check only that the request succeeded, not the request itself, which belongs to WEB-005_AC-1. The badge SHALL be the whole number shown inside the site header's link to the cart page, `/cart`. The specification quotes no wording for it, so the test SHALL NOT expect any.
- At desktop size, the badge SHALL become visible and show 1 without a page reload. After a second click on the same button, it SHALL show 2: the total item count, not the number of distinct products.
- On a small screen, a phone-sized window 390 pixels wide and 844 pixels high, the test SHALL open the navigation menu after the add. The badge SHALL then be visible in the opened menu and show 1.

#### Scenario: WEB-005_AC-2 Cart Badge Counts Added Items
- **WHEN** the test opens `/products/1` at desktop size in a fresh browser context, and clicks "Add to Cart" once and then a second time
- **THEN** the header's cart badge shows 1 after the first add and 2 after the second, and the page is never reloaded

#### Scenario: WEB-005_AC-2 Cart Badge Shows In Mobile Menu
- **WHEN** the test opens `/products/1` on a small screen in a fresh browser context, clicks "Add to Cart" and then opens the navigation menu
- **THEN** the cart badge is visible in the opened menu and shows 1

### Requirement: The cart page's lines are verified (WEB-005_AC-3)
The suite SHALL verify WEB-005_AC-3 with the specification's scenario. The test SHALL add Aurora Neural Headphones twice with its "Add to Cart" button on `/products/1`, and confirm that each add succeeded. It SHALL then open `/cart`. The cart page SHALL list a line whose visible text contains the name "Aurora Neural Headphones", the quantity 2, the unit price $249.99 and the line total $499.98. These are the values of the specification's scenario, and the line total is the quantity times the unit price. Apart from the name and the dollar amounts, the quantity SHALL be the only whole number in the line. The specification names no labels for the quantity, the unit price or the line total, so the test SHALL NOT require any.

#### Scenario: WEB-005_AC-3 Cart Page Lists Name Quantity And Prices
- **WHEN** the test adds Aurora Neural Headphones twice from `/products/1` in a fresh browser context and opens `/cart`
- **THEN** the cart lists a line with the name "Aurora Neural Headphones", quantity 2, unit price $249.99 and line total $499.98

### Requirement: The cart summary is verified (WEB-005_AC-4)
The suite SHALL verify WEB-005_AC-4 with two different products in the cart, so that the subtotal adds up more than one line total. The test SHALL add product 1, Aurora Neural Headphones, twice, and product 2 once, each with the "Add to Cart" button on its own detail page, and confirm that each add succeeded. The expected subtotal SHALL be twice the price of product 1 plus the price of product 2, rounded to cents. Both prices SHALL come from the shop's catalogue, read through the shop's API in the same space, because `shop/cart` does not state the price of product 2. On `/cart`, the cart page's summary SHALL show all of the following:
- a subtotal whose amount equals the expected subtotal;
- shipping whose value contains "Complimentary";
- tax whose value contains "Calculated at checkout";
- a total whose amount equals the expected subtotal, and so the subtotal.

Each of these is recognised by the specification's word for it: subtotal, shipping, tax or total. The word SHALL appear as a whole word in the visible text of a summary entry, ignoring case, followed by that entry's value. This way the subtotal's entry never counts as the total's. The quoted values SHALL be matched ignoring case.

#### Scenario: WEB-005_AC-4 Cart Summary Shows Subtotal Shipping Tax And Total
- **WHEN** the test adds product 1 twice and product 2 once in a fresh browser context, and opens `/cart`
- **THEN** the summary shows the sum of the two line totals as the subtotal, "Complimentary" shipping, "Calculated at checkout" tax, and a total equal to the subtotal

### Requirement: Adding a product again is verified (WEB-005_AC-9)
The suite SHALL verify WEB-005_AC-9 with the specification's scenario. It SHALL check the cart page both before and after the second add, so that the increase of 1 can be seen. The test SHALL add Aurora Neural Headphones, product 1, with its "Add to Cart" button on `/products/1`, confirm that the add succeeded, and open `/cart`. The cart SHALL then hold exactly one line, for Aurora Neural Headphones, with quantity 1. The test SHALL then click "Add to Cart" on `/products/1` again, confirm that the add succeeded, and reopen `/cart`. The cart SHALL still hold exactly one line, for Aurora Neural Headphones, now with quantity 2.

#### Scenario: WEB-005_AC-9 Adding Product Again Increments Quantity
- **WHEN** the test adds Aurora Neural Headphones from `/products/1` in a fresh browser context, opens `/cart`, then adds it again from `/products/1` and reopens `/cart`
- **THEN** the cart holds one line with quantity 1 after the first add, and still one line, now with quantity 2, after the second
