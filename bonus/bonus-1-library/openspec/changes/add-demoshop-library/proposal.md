# Proposal

## Why

Robot Framework tests of the DemoShop drive its REST API through generic HTTP keywords, so every suite has to
build URLs, manage sessions and dig values out of JSON itself, and assertions read as plumbing rather than intent.
A dedicated library, `demoshop_library.DemoShopLibrary`, gives testers shop-level keywords with Browser-style inline
assertions (`Get Product Price    1    ==    249.99`). The package currently holds only the uv template stub, so
this first slice sets up the library's shape for later keywords to follow.

## What Changes

- New Robot Framework library `demoshop_library.DemoShopLibrary`, built on PythonLibCore, imported with `url` and an
  optional `space`. When `space` is given, every request carries it in the `X-Workshop-Space` header.
- Each library instance keeps one cart of its own. The shop shares a single `workshop-demo` cart among all callers
  that send no `X-Session-ID`, so the library generates a session id per instance and sends it with every cart
  request, the only operations for which the shop's API declares that header. The library uses the `TEST` scope, so
  every test starts with an empty cart.
- First slice of keywords:
  - `Get Product Count`: the number of products in the catalogue.
  - `Get Product Price`: the price of a product, given its id.
  - `Add Product To Cart`: adds a product to the cart, given its id and an optional quantity (default 1).
  - `Get Cart Item Count`: the number of items in the cart, counting quantities the way the shop's cart badge does.
  - `Get Cart Total`: the cart's total as computed by the shop.
- Every `Get` keyword takes `assertion_operator`, `assertion_expected` and `message` and checks with AssertionEngine,
  converting the expected value so that numbers written in Robot data compare as numbers.
- Errors returned by the shop (unknown product, invalid quantity, unexpected status) fail the keyword with the
  shop's own message.
- Keyword documentation, modelled on Browser's `Get Text` and `Get Element Count`, can be generated with libdoc.
- Unit tests (pytest) that replace the HTTP layer and cover every behaviour, including failures. Robot acceptance
  tests in `atest/` run every keyword against the local shop, using only the library's own keywords, with every check
  made by a `Get` keyword's inline assertion.
- Removes the template `hello()` function from `demoshop_library/__init__.py`.

## Capabilities

### New Capabilities

- `library-import`: importing the library with `url` and `space`, the headers it sends, one cart per library
  instance and test-scoped instances, and how shop errors are reported.
- `getter-assertions`: the shared assertion contract of every `Get` keyword: arguments, operators, expected-value
  conversion, failure messages and return values.
- `product-keywords`: `Get Product Count` and `Get Product Price`.
- `cart-keywords`: `Add Product To Cart`, `Get Cart Item Count` and `Get Cart Total`.

### Modified Capabilities

None. No specs exist yet.

## Impact

- Code: new modules under `src/demoshop_library/`; `__init__.py` now exports `DemoShopLibrary` in place of `hello()`.
- Dependencies: none added. Uses the pinned `robotframework`, `robotframework-pythonlibcore`,
  `robotframework-assertion-engine` and `requests`; `pytest` stays a dev dependency.
- Shop API used: `GET /api/products/`, `GET /api/products/{product_id}`, `GET /api/cart/`, `POST /api/cart/items`
  and the header `X-Session-ID` (shop version 0.3.0, `references/demoshop-openapi.json`). The `X-Workshop-Space`
  header is not in that document; it is sent because the project requires it (`AGENTS.md`).
- Tests: new `tests/` (pytest, no network) and `atest/` (Robot, requires the shop at `http://localhost:9090`). The
  acceptance tests rely on the shop's seed catalogue (12 products; product 1 costs 249.99).
- Docs: `docs/DemoShopLibrary.html` can be generated with libdoc. The empty `README.md` and the placeholder
  `description` in `pyproject.toml` get short usage notes.
