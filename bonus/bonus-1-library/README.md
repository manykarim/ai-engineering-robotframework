# demoshop-library

Robot Framework library for testing the DemoShop through its REST API. Its `Get` keywords take Browser-style
inline assertions, for example `Get Product Price    1    ==    249.99`.

## Usage

Import the library with the shop's base URL and, optionally, a workshop space. When `space` is given, every request
carries it in the `X-Workshop-Space` header.

```robotframework
*** Settings ***
Library    demoshop_library.DemoShopLibrary    url=http://localhost:9090    space=team-7

*** Test Cases ***
Buy Two Desks
    Get Product Price      5    ==    799
    Add Product To Cart    5    quantity=2
    Get Cart Item Count    ==    2
    Get Cart Total         ==    1598
```

| Keyword | Arguments | Returns |
|---|---|---|
| `Get Product Count` | `assertion_operator=None`, `assertion_expected=0`, `message=None` | the number of products, an `int` |
| `Get Product Price` | `product_id`, `assertion_operator=None`, `assertion_expected=0`, `message=None` | the product's price, a `float` |
| `Add Product To Cart` | `product_id`, `quantity=1` | nothing |
| `Get Cart Item Count` | `assertion_operator=None`, `assertion_expected=0`, `message=None` | the sum of the quantities in the cart, an `int` |
| `Get Cart Total` | `assertion_operator=None`, `assertion_expected=0`, `message=None` | the cart's total, a `float` |

Without `assertion_operator`, a `Get` keyword returns its value without checking it. The operators are those of
[AssertionEngine](https://github.com/MarketSquare/AssertionEngine) that compare numbers: `==`, `!=`, `<`, `<=`, `>`,
`>=`, their aliases such as `should be` and `greater than`, `validate` and `then`.

Each library instance keeps one cart of its own. The library uses the `TEST` scope, so every test starts with an
empty cart. To use two carts in one test, import the library twice with `AS    ShopA` and `AS    ShopB`.

## Development

Unit tests, which need no shop:

```bash
uv run pytest
```

Acceptance tests, which run against the shop at `http://localhost:9090`:

```bash
uv run robot --outputdir results atest
```

Use `--variable SHOP_URL:<url>` or `--variable WORKSHOP_SPACE:<space>` to point them elsewhere.

Keyword documentation:

```bash
uv run python -m robot.libdoc "demoshop_library.DemoShopLibrary::url=http://localhost:9090" docs/DemoShopLibrary.html
```

Package:

```bash
uv build
```
