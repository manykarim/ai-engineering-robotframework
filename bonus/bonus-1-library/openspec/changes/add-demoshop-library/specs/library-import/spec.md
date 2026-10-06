# Spec Delta

## Purpose

Defines how `demoshop_library.DemoShopLibrary` is imported and configured. It covers how the library identifies its
workshop space and its cart to the shop, how long a library instance and its cart live, how shop failures are
reported, and how the library documents itself.

## ADDED Requirements

### Requirement: Import with shop URL and optional space
The library SHALL be importable as `demoshop_library.DemoShopLibrary` with a required `url` argument, the shop's base
URL, and an optional `space` argument. All keyword requests SHALL be sent to paths under `url`, whether or not `url`
ends with a slash. Importing the library SHALL NOT contact the shop.

#### Scenario: Import with URL only
- **WHEN** a suite imports `Library    demoshop_library.DemoShopLibrary    url=http://localhost:9090`
- **THEN** the import succeeds and keywords send their requests to `http://localhost:9090/api/...`

#### Scenario: URL with trailing slash
- **WHEN** the library is imported with `url=http://localhost:9090/`
- **THEN** keywords send their requests to `http://localhost:9090/api/...` without a doubled slash

#### Scenario: Shop not reachable at import time
- **WHEN** the library is imported with a `url` where no shop is running
- **THEN** the import succeeds, and the first keyword that contacts the shop fails

### Requirement: Workshop space header
When `space` is given, the library SHALL send its value in the `X-Workshop-Space` header of every request. When
`space` is not given, the library SHALL NOT send an `X-Workshop-Space` header.

#### Scenario: Space given
- **WHEN** the library is imported with `space=team-7` and any keyword is run
- **THEN** every request the keyword sends carries the header `X-Workshop-Space: team-7`

#### Scenario: Space omitted
- **WHEN** the library is imported without `space` and any keyword is run
- **THEN** no request the keyword sends carries an `X-Workshop-Space` header

### Requirement: One cart per library instance
Each library instance SHALL keep exactly one cart, identified by a session id that is unique to the instance. The
instance SHALL send that id in the `X-Session-ID` header of every request that reads or changes the cart. It SHALL NOT
send `X-Session-ID` on product requests, for which the shop's API declares no such header. Two library instances SHALL
NOT share a cart, and an instance SHALL NOT use the shop's default cart, which callers get when they send no session
id.

#### Scenario: Same instance, same cart
- **WHEN** a test runs `Add Product To Cart    1` and then `Get Cart Item Count    ==    1`
- **THEN** both cart requests carry the same `X-Session-ID`, and the test passes

#### Scenario: Product requests carry no session id
- **WHEN** a test runs `Get Product Count` or `Get Product Price    1`
- **THEN** the request carries no `X-Session-ID` header

#### Scenario: Two instances in one test
- **WHEN** a suite imports the library twice, `AS    ShopA` and `AS    ShopB`, and a test runs
  `ShopA.Add Product To Cart    1`
- **THEN** `ShopB.Get Cart Item Count    ==    0` and `ShopA.Get Cart Item Count    ==    1` both pass

#### Scenario: Default shop cart never used
- **WHEN** any cart keyword runs
- **THEN** its request carries the instance's `X-Session-ID`, so the shop never falls back to its shared default cart

### Requirement: Fresh library instance per test
The library SHALL use Robot Framework's `TEST` library scope. Each test SHALL get its own library instance, and that
instance SHALL also serve the test's setup and teardown. As a result, every test starts with an empty cart. Suite
setup and suite teardown SHALL run on an instance that no test uses.

#### Scenario: Cart does not carry over between tests
- **WHEN** one test adds products to the cart and the next test runs `Get Cart Item Count    ==    0`
- **THEN** the second test passes

#### Scenario: Test setup shares the test's cart
- **WHEN** a test's `[Setup]` runs `Add Product To Cart    1` and the test body runs `Get Cart Item Count    ==    1`
- **THEN** the test passes

#### Scenario: Suite setup cart is not visible to tests
- **WHEN** the suite setup runs `Add Product To Cart    1` and a test then runs `Get Cart Item Count    ==    0`
- **THEN** the test passes

### Requirement: Shop errors fail the keyword
When the shop answers with an error status (4xx or 5xx), the keyword SHALL fail with a message that names the action
attempted and contains the shop's error detail and the HTTP status. When the detail is a list of validation errors,
the message SHALL include each error's text. When the shop cannot be reached, the keyword SHALL fail with a message
that names the URL it tried.

#### Scenario: Error detail reported
- **WHEN** a keyword's request is answered with HTTP 404 and body `{"detail":"Product not found"}`
- **THEN** the keyword fails with a message containing `Product not found` and `404`

#### Scenario: Validation errors reported
- **WHEN** a keyword's request is answered with HTTP 422 and a `detail` list whose message is
  `Input should be less than or equal to 20`
- **THEN** the keyword fails with a message containing `Input should be less than or equal to 20` and `422`

#### Scenario: Shop unreachable
- **WHEN** the library is imported with `url=http://localhost:1` and `Get Product Count` is run
- **THEN** the keyword fails with a message containing `http://localhost:1`

### Requirement: Library documentation
Libdoc SHALL be able to generate keyword documentation for `demoshop_library.DemoShopLibrary`. The introduction SHALL
describe the `url` and `space` import arguments, the one-cart-per-instance behaviour and the `TEST` scope, and SHALL
contain an `Assertions` section that the `Get` keywords' documentation links to. Each keyword's documentation SHALL
follow the form of Browser's `Get Text` and `Get Element Count`: a one-line summary, an argument table, a note on
optional assertions where the keyword is a `Get` keyword, and at least one example.

#### Scenario: Generate documentation
- **WHEN** `uv run python -m robot.libdoc demoshop_library.DemoShopLibrary docs/DemoShopLibrary.html` is run
- **THEN** it writes `docs/DemoShopLibrary.html` listing all five keywords without errors

#### Scenario: Assertions section linked
- **WHEN** the generated documentation for `Get Product Price` is viewed
- **THEN** its `assertion_operator` description links to the `Assertions` section of the introduction
