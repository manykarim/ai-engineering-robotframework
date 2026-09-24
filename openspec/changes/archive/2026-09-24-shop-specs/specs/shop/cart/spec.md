## Purpose

Describes the shopping cart as a shopper experiences it on the shop's pages and as an API consumer uses it through the cart API: adding items, the cart page and its summary, sessions, validation and clearing.

## ADDED Requirements

### Requirement: Add to Cart sends an API request (WEB-005_AC-1)
When a shopper clicks the "Add to Cart" button on a product card on any page - the home page, the products page or a detail page - a POST request SHALL be sent to `/api/cart/items` with the product's ID, and the request SHALL include the shopper's session identification (see WEB-005_AC-10).

#### Scenario: Adding from the products page
- **WHEN** a shopper clicks "Add to Cart" on a product card on `/products`
- **THEN** a POST request to `/api/cart/items` carries that product's ID and the shopper's session identification

### Requirement: Cart badge updates (WEB-005_AC-2)
After a shopper clicks "Add to Cart" and the API responds successfully, the cart count badge in the navigation header SHALL update to the new total item count. The badge SHALL be visible in the desktop navigation and, on small screens, in the mobile navigation once the shopper opens the navigation menu.

#### Scenario: Desktop navigation
- **WHEN** a shopper with an empty cart adds one product
- **THEN** the cart badge in the header shows 1

#### Scenario: Mobile navigation
- **WHEN** a shopper on a small screen adds a product and then opens the navigation menu
- **THEN** the cart badge with the updated count is visible in the opened menu

### Requirement: Cart page lists the items (WEB-005_AC-3)
When a shopper who has added items opens the cart page, `/cart`, every item SHALL be listed with its product name, quantity, unit price and line total, where the line total is the quantity times the unit price.

#### Scenario: Two units of one product
- **WHEN** a shopper has added Aurora Neural Headphones twice and opens `/cart`
- **THEN** the line shows the name, quantity 2, unit price $249.99 and line total $499.98

### Requirement: Cart summary (WEB-005_AC-4)
With items in the cart, the cart page's summary SHALL display the subtotal (the sum of all line totals), shipping as "Complimentary", tax as "Calculated at checkout", and a total equal to the subtotal.

#### Scenario: Summary of a filled cart
- **WHEN** the cart page is loaded with items
- **THEN** the summary shows the subtotal, "Complimentary" shipping, "Calculated at checkout" tax, and a total equal to the subtotal

### Requirement: Proceed to Checkout (WEB-005_AC-5)
With items in the cart, the cart page SHALL show a "Proceed to Checkout" button, and clicking it SHALL navigate to `/checkout`.

#### Scenario: Going to checkout
- **WHEN** a shopper with items in the cart clicks "Proceed to Checkout"
- **THEN** the browser is on `/checkout`

### Requirement: Continue Shopping (WEB-005_AC-6)
The cart page SHALL show a "Continue Shopping" button or link, and clicking it SHALL navigate to `/products`.

#### Scenario: Back to shopping
- **WHEN** a shopper on the cart page clicks "Continue Shopping"
- **THEN** the browser is on `/products`

### Requirement: Empty cart state (WEB-005_AC-7)
When a shopper with no items opens the cart page, the message "Your cart is still empty" SHALL be displayed together with a "Browse" or equivalent button leading to the products page, and neither the cart summary nor the checkout button SHALL be displayed.

#### Scenario: Opening an empty cart
- **WHEN** a shopper with an empty cart opens `/cart`
- **THEN** "Your cart is still empty" and a button to the products page are shown, and there is no summary and no "Proceed to Checkout"

### Requirement: Adding a product again increments its quantity (WEB-005_AC-9)
When a shopper who already has product 1 in the cart clicks "Add to Cart" on product 1 again, that item's quantity SHALL increase by 1 and no new line item SHALL be created.

#### Scenario: Second add of the same product
- **WHEN** a shopper adds Aurora Neural Headphones, then adds it again
- **THEN** the cart has one line for it with quantity 2

### Requirement: Session identification (WEB-005_AC-10)
Every cart API request SHALL be identified by its `X-Session-ID` request header. Without that header, the session SHALL be `workshop-demo`, also when a `session_id` cookie is sent. On the shop's pages, the shopper's cart SHALL be identified by the `session_id` cookie.

#### Scenario: Cookie without header on the API
- **WHEN** an API request to the cart carries a `session_id` cookie but no `X-Session-ID` header
- **THEN** the request is handled in session `workshop-demo`

#### Scenario: Header on the API
- **WHEN** an API request to the cart carries `X-Session-ID: test-123`
- **THEN** the request is handled in session `test-123`

### Requirement: Empty cart through the API (API-005_AC-1)
For a session whose cart is empty, `GET /api/cart/` SHALL respond with status `200` and a body whose `session` is the session key (`workshop-demo` by default), whose `items` is an empty array, and whose `total` is `0`.

#### Scenario: Fresh session
- **WHEN** an API consumer sends `GET /api/cart/` for a session with an empty cart
- **THEN** the status is 200 and the body has the session key, `items: []` and `total: 0`

### Requirement: Add an item through the API (API-005_AC-2)
`POST /api/cart/items` with body `{"product_id": 1, "quantity": 2}` SHALL respond with status `200` and the updated cart state. Its `items` array SHALL contain an entry with `product_id` `1`, `name` `"Aurora Neural Headphones"`, `quantity` `2`, `unit_price` `249.99` and `total_price` `499.98`, and the cart's `total` SHALL be `499.98`.

#### Scenario: Two headphones
- **WHEN** an API consumer posts `{"product_id": 1, "quantity": 2}` to an empty cart
- **THEN** the status is 200, the item shows quantity 2 at 249.99 with total_price 499.98, and total is 499.98

### Requirement: Adding the same product through the API increments it (API-005_AC-3)
When the cart already contains product `1` with quantity `2`, `POST /api/cart/items` with `{"product_id": 1, "quantity": 1}` SHALL respond with status `200`, and the item SHALL have quantity `3` and `total_price` `749.97`.

#### Scenario: One more headphone
- **WHEN** the cart holds product 1 with quantity 2 and one more is posted
- **THEN** the status is 200 and the item has quantity 3 with total_price 749.97

### Requirement: At most 20 per item (API-005_AC-4)
`POST /api/cart/items` with a `quantity` of `21` SHALL respond with status `422`, and the body SHALL indicate that the quantity must be at most 20.

#### Scenario: Quantity 21
- **WHEN** an API consumer posts `{"product_id": 1, "quantity": 21}`
- **THEN** the status is 422 and the body says the quantity must be at most 20

### Requirement: At least 1 per item (API-005_AC-5)
`POST /api/cart/items` with a `quantity` of `0` SHALL respond with status `422`, and the body SHALL indicate that the quantity must be at least 1.

#### Scenario: Quantity 0
- **WHEN** an API consumer posts `{"product_id": 1, "quantity": 0}`
- **THEN** the status is 422 and the body says the quantity must be at least 1

### Requirement: Product ID of at least 1 (API-005_AC-6)
`POST /api/cart/items` with a `product_id` of `0` SHALL respond with status `422`, and the body SHALL indicate that the product ID must be at least 1.

#### Scenario: Product ID 0
- **WHEN** an API consumer posts `{"product_id": 0, "quantity": 1}`
- **THEN** the status is 422 and the body says product_id must be at least 1

### Requirement: Unknown product (API-005_AC-7)
`POST /api/cart/items` for a product ID that does not exist SHALL respond with status `404` and the body `{"detail": "Product not found"}`.

#### Scenario: Product 999
- **WHEN** an API consumer posts `{"product_id": 999, "quantity": 1}`
- **THEN** the status is 404 and the body is `{"detail": "Product not found"}`

### Requirement: Clear the cart (API-005_AC-8)
When the cart contains one or more items, `DELETE /api/cart/` SHALL respond with status `200` and the body `{"status": "cleared", "session": "workshop-demo"}` for the default session.

#### Scenario: Clearing the default cart
- **WHEN** the default session's cart holds items and an API consumer sends `DELETE /api/cart/` without `X-Session-ID`
- **THEN** the status is 200 and the body is `{"status": "cleared", "session": "workshop-demo"}`

### Requirement: Session from the X-Session-ID header (API-005_AC-9)
A `POST /api/cart/items` and a following `GET /api/cart/`, both sent with `X-Session-ID: test-session-123`, SHALL share one cart: the response SHALL contain `"session": "test-session-123"`, and its items SHALL reflect the product added before.

#### Scenario: Round trip in one session
- **WHEN** product 1 is posted and the cart is then read, both with `X-Session-ID: test-session-123`
- **THEN** the cart reports session `test-session-123` and contains product 1

### Requirement: Default session key (API-005_AC-10)
`GET /api/cart/` without an `X-Session-ID` header SHALL respond with `"session": "workshop-demo"`.

#### Scenario: No session header
- **WHEN** an API consumer reads the cart without `X-Session-ID`
- **THEN** the body contains `"session": "workshop-demo"`

### Requirement: Cart item structure (API-005_AC-11)
With items in the cart, every entry of the `items` array returned by `GET /api/cart/` SHALL contain `product_id` (integer), `name` (string), `quantity` (integer), `unit_price` (number) and `total_price` (number), where `total_price` is `unit_price` times `quantity`, rounded to two decimal places.

#### Scenario: Reading a filled cart
- **WHEN** an API consumer reads a cart with items
- **THEN** every item has those five fields with those types, and each total_price equals unit_price times quantity to two decimals
