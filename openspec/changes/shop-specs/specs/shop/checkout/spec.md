## Purpose

Describes checkout as a shopper experiences it: the order summary, the checkout form and its validation, placing an order, the order documents, and the state of the cart afterwards.

## ADDED Requirements

### Requirement: Order summary (WEB-006_AC-1)
When a shopper opens the checkout page, `/checkout`, with items in the cart, an order summary SHALL list the cart's items with their names and prices, together with the subtotal, the shipping cost, the tax amount and the order total. The order total SHALL equal the subtotal plus the shipping cost plus the tax amount, with "Complimentary" shipping counted as 0.

#### Scenario: Summary of a filled cart
- **WHEN** a shopper with items in the cart opens `/checkout`
- **THEN** the summary lists each item with name and price, and shows subtotal, shipping, tax and a total equal to subtotal plus shipping plus tax

### Requirement: Required form fields (WEB-006_AC-2)
The checkout form SHALL contain the required fields email address (an email input), full name (a text input) and address (a text input or text area).

#### Scenario: Required fields present
- **WHEN** the checkout page has loaded
- **THEN** the form has an email address field, a full name field and an address field

### Requirement: Optional form fields (WEB-006_AC-3)
The checkout form SHALL contain the optional fields team size (a number input) and special instructions (a text area).

#### Scenario: Optional fields present
- **WHEN** the checkout page has loaded
- **THEN** the form has a team size field and a special instructions field

### Requirement: Email validation (WEB-006_AC-4)
An invalid email address SHALL produce a validation error for the email field and SHALL prevent the form from being submitted. A valid email address SHALL produce no error for that field.

#### Scenario: Invalid email
- **WHEN** the shopper enters "notanemail" as email address and submits
- **THEN** an error is shown for the email field and no order is placed

#### Scenario: Valid email
- **WHEN** the shopper enters "test@example.com" as email address
- **THEN** no error is shown for the email field

### Requirement: Full name validation (WEB-006_AC-5)
A full name shorter than 2 characters SHALL produce a validation error for the name field. A valid full name SHALL produce no error for that field.

#### Scenario: One-character name
- **WHEN** the shopper enters "A" as full name and submits
- **THEN** an error is shown for the name field

#### Scenario: Valid name
- **WHEN** the shopper enters "Test User" as full name
- **THEN** no error is shown for the name field

### Requirement: Address validation (WEB-006_AC-6)
An address shorter than 5 characters SHALL produce a validation error for the address field. A valid address SHALL produce no error for that field.

#### Scenario: Three-character address
- **WHEN** the shopper enters "123" as address and submits
- **THEN** an error is shown for the address field

#### Scenario: Valid address
- **WHEN** the shopper enters "123 Test Street, City" as address
- **THEN** no error is shown for the address field

### Requirement: Successful order (WEB-006_AC-7)
When every required field holds valid data, the cart contains at least one item, and the shopper submits the checkout form, an order SHALL be created and a success message SHALL be displayed. The message SHALL include an order number made of `ORD-` followed by 8 characters from 0-9 and A-F, matching `^ORD-[0-9A-F]{8}$`.

#### Scenario: Placing an order
- **WHEN** a shopper with one item in the cart submits "test@example.com", "Test User" and "123 Test Street, City"
- **THEN** a success message shows an order number such as `ORD-3F9A1C2B`

### Requirement: Order document links (WEB-006_AC-8)
The success message after an order SHALL include a link to download the invoice PDF and a link to download the order summary PDF, and both links SHALL lead to valid, downloadable PDF files.

#### Scenario: Downloading the documents
- **WHEN** an order has been placed and the shopper follows the invoice link and the order summary link
- **THEN** each link delivers a PDF file

### Requirement: Empty cart at checkout (WEB-006_AC-10)
When a shopper with no items in the cart submits the checkout form, the error message "Your cart is empty" SHALL be displayed and no order SHALL be created.

#### Scenario: Submitting without items
- **WHEN** a shopper with an empty cart submits the checkout form with valid data
- **THEN** "Your cart is empty" is displayed and no order is created

### Requirement: Validation errors next to the fields (WEB-006_AC-11)
When the shopper submits the checkout form with one or more invalid fields, an error message SHALL be displayed next to each invalid field, the form SHALL NOT be submitted, and the shopper SHALL remain on the checkout page.

#### Scenario: Several invalid fields
- **WHEN** the shopper submits "notanemail", "A" and "123"
- **THEN** each of the three fields shows an error beside it, no order is placed, and the shopper is still on `/checkout`

### Requirement: Cart cleared after an order (WEB-006_AC-12)
After a successful order, the cart page, `/cart`, SHALL show an empty cart, and the cart badge in the navigation SHALL show no item count.

#### Scenario: After ordering
- **WHEN** a shopper has placed an order and opens `/cart`
- **THEN** the cart is empty and the cart badge shows no count
