# Spec Delta

## Purpose

Defines the keywords that fill and inspect the cart that belongs to a library instance. With them, a test can add
products and check the cart's item count and total as the shop computes them.

## ADDED Requirements

### Requirement: Add Product To Cart
The library SHALL provide `Add Product To Cart` with a required `product_id` argument and an optional `quantity`
argument, both integers; `quantity` defaults to 1. It adds that quantity of the product to the library instance's
cart. When the product is already in the cart, the shop increases that line's quantity instead of adding a second
line. The library SHALL leave the validation of `product_id` and `quantity` to the shop. When the shop rejects the
request, the keyword SHALL fail with the shop's message.

#### Scenario: Default quantity
- **WHEN** a test runs `Add Product To Cart    1` on an empty cart
- **THEN** `Get Cart Item Count` returns 1

#### Scenario: Explicit quantity
- **WHEN** a test runs `Add Product To Cart    1    quantity=3` on an empty cart
- **THEN** `Get Cart Item Count` returns 3

#### Scenario: Same product added twice
- **WHEN** a test runs `Add Product To Cart    1    2` and then `Add Product To Cart    1`
- **THEN** `Get Cart Item Count` returns 3, and `Get Cart Total` returns 749.97

#### Scenario: Unknown product
- **WHEN** a test runs `Add Product To Cart    999999`
- **THEN** the keyword fails with a message containing `999999`, `Product not found` and `404`

#### Scenario: Quantity above the shop's limit
- **WHEN** a test runs `Add Product To Cart    1    21`
- **THEN** the keyword fails with a message containing `Input should be less than or equal to 20` and `422`

#### Scenario: Quantity below one
- **WHEN** a test runs `Add Product To Cart    1    0`
- **THEN** the keyword fails with a message containing `Input should be greater than or equal to 1` and `422`

### Requirement: Get Cart Item Count
The library SHALL provide `Get Cart Item Count`. It returns the number of items in the library instance's cart as an
integer: the sum of the quantities of all cart lines, which is what the shop's cart badge shows. It takes the
assertion arguments of every `Get` keyword.

#### Scenario: Empty cart
- **WHEN** a test runs `Get Cart Item Count    ==    0` before adding anything
- **THEN** the keyword passes

#### Scenario: Quantities summed across lines
- **WHEN** a test adds product 1 with quantity 2 and product 2 with quantity 1, then runs `Get Cart Item Count`
- **THEN** the keyword returns 3, not the number of lines (2)

### Requirement: Get Cart Total
The library SHALL provide `Get Cart Total`. It returns the total of the library instance's cart, as the shop computes
it, as a float. It takes the assertion arguments of every `Get` keyword.

#### Scenario: Empty cart total
- **WHEN** a test runs `${total} =    Get Cart Total` before adding anything
- **THEN** `${total}` is the float `0.0`

#### Scenario: Total of several lines
- **WHEN** a test adds product 1 (249.99) with quantity 2 and product 2 (39.5) with quantity 1, then runs
  `Get Cart Total    ==    539.48`
- **THEN** the keyword passes

#### Scenario: Total with assertion after one add
- **WHEN** a test runs `Add Product To Cart    1    2` and then `Get Cart Total    ==    499.98`
- **THEN** the keyword passes
