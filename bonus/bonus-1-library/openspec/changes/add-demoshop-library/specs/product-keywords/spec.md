# Spec Delta

## Purpose

Defines the keywords that read the DemoShop's product catalogue, so that tests can check how many products the shop
offers and what a given product costs.

## ADDED Requirements

### Requirement: Get Product Count
The library SHALL provide `Get Product Count`. It returns the number of products in the shop's catalogue as an
integer and takes the assertion arguments of every `Get` keyword.

#### Scenario: Count of the seed catalogue
- **WHEN** a test runs `${count} =    Get Product Count` against the shop's seed catalogue
- **THEN** `${count}` is `12`

#### Scenario: Count with assertion
- **WHEN** a test runs `Get Product Count    ==    12` against the shop's seed catalogue
- **THEN** the keyword passes

### Requirement: Get Product Price
The library SHALL provide `Get Product Price` with a required `product_id` argument, an integer. It returns the
product's price as a float and takes the assertion arguments of every `Get` keyword.

#### Scenario: Price of a product
- **WHEN** a test runs `${price} =    Get Product Price    1`
- **THEN** `${price}` is the float `249.99`

#### Scenario: Price with assertion
- **WHEN** a test runs `Get Product Price    1    ==    249.99`
- **THEN** the keyword passes

#### Scenario: Whole-number price is a float
- **WHEN** a test runs `${price} =    Get Product Price    5`, and product 5 costs 799
- **THEN** `${price}` is the float `799.0`

#### Scenario: Unknown product
- **WHEN** a test runs `Get Product Price    999999`
- **THEN** the keyword fails with a message containing `999999`, `Product not found` and `404`

#### Scenario: Product id is not an integer
- **WHEN** a test runs `Get Product Price    abc`
- **THEN** the keyword fails with an argument conversion error for `product_id`, and no request is sent
