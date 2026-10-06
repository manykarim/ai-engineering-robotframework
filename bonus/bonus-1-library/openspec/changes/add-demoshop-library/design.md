# Design

## Context

See `proposal.md` for the motivation and `specs/` for the required behaviour. The package `demoshop_library` holds only
the uv template (`hello()` in `src/demoshop_library/__init__.py`). The run-time dependencies are already pinned and
installed: Robot Framework 7.5, PythonLibCore 4.6.0, AssertionEngine 5.0.1 and requests 2.34.2.

The OpenAPI document (`references/demoshop-openapi.json`) gives no response schemas. The shapes below were observed
on the local shop (version 0.3.0) at `http://localhost:9090`:

| Request | Response |
|---|---|
| `GET /api/products/` | `{"items": [{"id", "name", "price", ...}, ...]}`, 12 items, no paging fields |
| `GET /api/products/{id}` | `{"product": {"id", "price", ...}}`; unknown id gives 404 `{"detail": "Product not found"}` |
| `GET /api/cart/` | `{"session", "items": [{"product_id", "name", "quantity", "unit_price", "total_price"}], "total"}`; an empty cart has `"total": 0`, an integer |
| `POST /api/cart/items` `{"product_id", "quantity"}` | the updated cart, in the same shape; the same product merges into one line; 404 for an unknown product; 422 for a quantity outside 1–20, with `detail` as a list of `{"loc", "msg", ...}` |

What the OpenAPI document declares for the operations this slice uses:

- `GET /api/products/` and `GET /api/products/{product_id}`, where `product_id` is an integer path parameter. These
  operations declare no header parameters.
- `GET /api/cart/` and `POST /api/cart/items` declare one optional header, `X-Session-ID`. The body of
  `POST /api/cart/items` is `AddToCartRequest`: `product_id`, an integer of at least 1, required; and `quantity`, an
  integer from 1 to 20, default 1, sent as `application/json`.
- Only status codes 200 and 422 are declared. The 404 for an unknown product was observed, not documented.
- `X-Workshop-Space` is not declared anywhere. It comes from the project's `AGENTS.md`, and the shop answered 200 to a
  product request carrying it.

Constraints found while checking:

- A request without `X-Session-ID` uses the shared cart `"session": "workshop-demo"`.
- The shop's front end (`/static/app.js`) shows the sum of the item quantities in its cart badge.
- With an argument typed `float | str`, Robot Framework 7.5 keeps `"249.99"` as a string, because `str` is in the
  union. Passing it straight to `verify_assertion` therefore fails with
  `'249.99' (float) should be '249.99' (str)`.
- Under the `TEST` scope, a test's setup and body share one instance. The suite setup gets an instance of its own,
  and a library imported with `AS` is a separate instance.

## Goals / Non-Goals

**Goals:**

- A package layout built on PythonLibCore components, so that later slices add keywords without touching the
  library class.
- A single HTTP client per library instance that owns the base URL, the headers, the timeout and the translation of
  errors.
- Unit tests that run the real request-building code and replace only the network transport.

**Non-Goals:**

- Retrying or polling assertions until a timeout, as Browser's `with_assertion_polling` does. Shop values do not change
  asynchronously, so each assertion is checked once.
- AssertionEngine formatters (`strip`, `case insensitive`, ...). Every keyword in this slice returns a number.
- Validating `product_id` or `quantity` in the client. The shop's 404 and 422 responses are the source of truth.
- Clearing, removing from, or checking out the cart, and keywords for search, login or documents.
- A configurable timeout or any import argument besides `url` and `space`.

## Decisions

### 1. Package layout: a `DynamicCore` library with keyword components

```
src/demoshop_library/
  __init__.py   # exports DemoShopLibrary and __version__; the template hello() is removed
  library.py    # class DemoShopLibrary(DynamicCore): import arguments, scope, intro docs with "= Assertions ="
  client.py     # class ShopClient (requests session, headers, timeout, errors); class DemoShopError
  products.py   # class ProductKeywords: Get Product Count, Get Product Price
  cart.py       # class CartKeywords: Add Product To Cart, Get Cart Item Count, Get Cart Total
```

`DemoShopLibrary.__init__(url, space=None)` creates one `ShopClient` and passes `[ProductKeywords(client),
CartKeywords(client)]` to `DynamicCore.__init__`. The keywords are methods decorated with `@keyword(tags=...)`.
Robot resolves `demoshop_library.DemoShopLibrary` as the attribute `DemoShopLibrary` of the package, and libdoc uses
the same name. The library class docstring becomes the libdoc introduction, and `__init__`'s docstring documents
importing. `ROBOT_LIBRARY_VERSION` comes from `importlib.metadata.version("demoshop-library")`.

*Alternatives:* one class holding every keyword is simpler today, but it grows into a single file as slices are
added, and it leaves PythonLibCore's component model unused. `HybridCore` gives no benefit here, and `DynamicCore` is
what Browser uses.

### 2. Headers: `X-Workshop-Space` on every request, `X-Session-ID` on cart requests only

`ShopClient.__init__` sets `session_id = uuid.uuid4().hex` and removes any trailing `/` from `url`. Its
`requests.Session` has one default header, `X-Workshop-Space: <space>`, and only when `space` is not `None`.
`request(..., with_session=False)` adds `X-Session-ID: <session_id>` when `with_session` is true. The cart keywords
pass it and the product keywords do not, which matches the operations that declare the header. The client sets no
other header; requests adds `Content-Type: application/json` for the `AddToCartRequest` body. The import makes no
request.

*Alternatives:*
- Making `X-Session-ID` a default header on every request is simpler, but the OpenAPI document declares it only for
  the cart and checkout operations.
- An `Accept: application/json` header was dropped because the document does not declare it.
- Letting the shop assign a session is not possible, because it falls back to the shared `workshop-demo` cart.
- Sending the session as a cookie is not possible either: the API reads only the header, and the front end copies its
  cookie into that header.

### 3. Library scope: `TEST`

`ROBOT_LIBRARY_SCOPE = "TEST"`. A new instance, and with it a new session id and an empty cart, is created for every
test. This keeps cart tests independent of execution order. In this slice that matters most, because no keyword
clears the cart.

*Alternatives:* with `SUITE`, carts would carry over between tests in a suite. Without a `Clear Cart` keyword, every
test after the first would depend on the tests before it. `GLOBAL`, as in Browser and RequestsLibrary, has the same
problem across the whole run. Users who need two carts in one test import the library twice, each time with its own
`AS` alias.

### 4. Assertions: AssertionEngine's numeric helpers, with signatures modelled on `Get Element Count`

The counts call `int_str_verify_assertion` and the amounts call `float_str_verify_assertion`. Both are part of
AssertionEngine. They convert `assertion_expected` to `int` or `float` for the comparison operators, pass it through
as a string for `validate` and `then`, reject every other operator with `ValueError("Operator '<name>' is not
allowed.")`, and then delegate to `verify_assertion`. A probe against the installed versions produced exactly the
messages quoted in `specs/getter-assertions/spec.md`.

The signatures follow Browser's `Get Element Count`:

```python
assertion_operator: AssertionOperator | None = None
assertion_expected: int | str = 0      # counts; amounts use float | str = 0
message: str | None = None
```

The subject prefix passed to the helper is `Product count`, `Product <id> price`, `Cart item count` or `Cart total`.
The tags are `Assertion`, `Getter` and an area tag, `Products` or `Cart`, in the place of Browser's `PageContent`.
`Add Product To Cart` is tagged `Setter` and `Cart`. The documentation of each keyword follows the shape of the
reference files: a summary line, an `| =Arguments= | =Description= |` table whose `assertion_operator` row says
"See `Assertions` for further details. Defaults to None.", the paragraph "Optionally asserts ...", and an `Example:`
block.

*Alternatives:* calling `verify_assertion` directly with `assertion_expected: float | str` fails on every
text-written number (see Context). Typing it `float | None` lets Robot convert numbers, but then `validate` and
`then` expressions fail to convert. Converting in the library and then calling `verify_assertion` duplicates the
helpers.

### 5. Money values are floats taken from the shop

`Get Product Price` returns `float(body["product"]["price"])`, and `Get Cart Total` returns
`float(body["total"])`, so the integer `0` of an empty cart becomes `0.0`. The library never adds up prices itself.
`Get Cart Item Count` returns `sum(item["quantity"] for item in body["items"])`, which matches the cart badge.
`Get Product Count` returns `len(body["items"])`.

*Alternatives:* computing the total from the cart lines duplicates the shop's rounding and risks float drift.
`Decimal` does not work with the float helper, because `Decimal("249.99") == 249.99` is `False`.

### 6. Error translation in one place

`ShopClient.request(method, path, action, json=None, with_session=False)` sends the request with a fixed 10-second
timeout and returns the decoded JSON. It raises `DemoShopError`, a subclass of `Exception` with `ROBOT_SUPPRESS_NAME = True` so that Robot
shows only the message, in these cases:

- `requests.RequestException` (connection refused, timeout):
  `"<action> failed: could not reach the shop at <url>: <exception>"`.
- Status 400 or higher: `"<action> failed: <detail> (HTTP <status>)"`. Here `<detail>` is the shop's `detail` when it
  is a string. When `detail` is a list of validation errors, it is `"; ".join(f"{loc[-1]}: {msg}")`, for example
  `quantity: Input should be less than or equal to 20`. Otherwise it is the response text.
- A body that is not JSON, or that is missing an expected key: `"<action> failed: unexpected response from the shop"`.

The actions are, for example, `Getting product 999999`, `Adding 2 x product 1 to the cart` and `Getting the cart`, so
each message names the product id.

### 7. Unit tests replace the transport, not the client

`tests/conftest.py` provides a `FakeShop(requests.adapters.BaseAdapter)`. It records each `PreparedRequest` and
returns canned `requests.Response` objects, which a test registers by `(method, path)`. A fixture builds
`DemoShopLibrary("http://shop.test", space=...)` and mounts the fake with `library_client.session.mount("http://",
fake)`. URL joining, default headers and JSON body encoding therefore run for real. The tests check the final
requests: the path, `X-Session-ID` (present on cart requests, absent on product requests), `X-Workshop-Space` and the
body.

The keyword tests call the library through PythonLibCore's dynamic API (`run_keyword`, `get_keyword_names`,
`get_keyword_arguments`, `get_keyword_types`, `get_keyword_tags`), as Robot does. That API does not convert arguments,
so the tests pass `AssertionOperator["=="]` and the expected value as a string, the same values Robot would pass after
its own conversion.

The unit tests are the only place where failures are verified (decision 8), so they cover:
- shop errors, with canned bodies copied verbatim from the local shop (see Context);
- the unreachable shop;
- the exact assertion failure messages, the custom message, and the rejected text operators;
- the values returned by `then` and their types.

They also check the declared argument types (`product_id: int`, `quantity: int`,
`assertion_operator: AssertionOperator | None`). Robot uses those types to reject `abc` and `===` before the library
is called.

*Alternatives:* monkeypatching `Session.request` skips the merging of headers, so the header tests would prove
nothing. `responses` and `requests-mock` would each add a dev dependency to replace about 30 lines. A fake
`ShopClient` would skip exactly the code that most needs testing.

### 8. Acceptance tests: only the library's keywords, against the local shop

```
atest/
  resources/demoshop.resource   # variables only: ${SHOP_URL} (default http://localhost:9090),
                                # ${WORKSHOP_SPACE} (default ${NONE}), seed data (${PRODUCT_COUNT}=12, product 1 = 249.99,
                                # product 2 = 39.5, product 5 = 799)
  library_import.robot          # trailing-slash url, space, ShopA/ShopB instances, TEST scope
  getter_assertions.robot       # positional and named arguments, operator aliases, validate
  product_keywords.robot
  cart_keywords.robot
```

The rules for every suite:
- Test cases, setups and teardowns call only `DemoShopLibrary` keywords. They use no BuiltIn keywords (no
  `Should ...`, `Run Keyword And Expect Error` or `Evaluate`), no other library and no direct HTTP.
- Every check is a `Get` keyword's inline assertion, for example `Get Cart Total    ==    499.98`, so all checks go
  through AssertionEngine.
- Every import points at `${SHOP_URL}`, the local shop. No test uses an unreachable URL or a fake.

Asserting that a keyword fails needs a BuiltIn keyword, so the acceptance tests cover the passing paths. The unit tests
cover failures (decision 7):

| Spec area | `atest/` (local shop) | `tests/` (fake transport) |
|---|---|---|
| Import, URL, space | trailing-slash URL; keywords pass with `space` set | headers and URLs of every request; no request at import |
| One cart per instance, `TEST` scope | `ShopA`/`ShopB`; next test empty; `[Setup]` shares the cart; suite-setup cart invisible | `X-Session-ID` on cart requests only; distinct per instance |
| Shop errors, unreachable shop | — | all scenarios |
| Assertions | passing operators, aliases, named arguments, `validate` | failure messages, custom message, `then` return values, rejected operators, declared types |
| Products and cart | every keyword against the seed data | the same values from canned responses |

The two-instance suite imports the library twice, `AS    ShopA` and `AS    ShopB`. With one unaliased import and one
alias, unqualified keyword names would be ambiguous. The variable is named `${WORKSHOP_SPACE}`, not `${SPACE}`, because
`${SPACE}` is a built-in Robot variable holding a single space. The suites run with
`uv run robot --outputdir results atest`, and any variable can be overridden with `--variable`.

To verify the first rule, a run's `results/output.xml` is read with `robot.api.ExecutionResult`. Every executed
keyword's `owner` must be `demoshop_library.DemoShopLibrary`, `ShopA` or `ShopB`.

### 9. Project configuration

`pyproject.toml` gets `[tool.pytest.ini_options] testpaths = ["tests"]`, so that `uv run pytest` does not collect from
`references/` or `atest/`. `.gitignore` gets `results/`. No dependencies change.

## Risks / Trade-offs

- [The acceptance tests depend on the shop's seed data (12 products, the prices of products 1, 2 and 5)] → The
  values live in one place, `demoshop.resource`, and a wrong value fails with the assertion message, which shows the
  actual figure.
- [The acceptance tests never exercise a failure against the real shop, so a change in the shop's error format would
  go unnoticed there] → The unit tests' canned error bodies are copied verbatim from the shop (see Context), and the
  reference OpenAPI document pins the shop version to 0.3.0.
- [`X-Workshop-Space` is not declared in the OpenAPI document] → It is sent because `AGENTS.md` requires it, and the
  shop accepts it. If a later version of the document declares the header, its name and scope are aligned then.
- [Every test leaves an abandoned cart on the shop, because carts are never cleared] → This is acceptable for the
  local workshop shop. A later slice can add `Clear Cart` or a library listener `close()` that deletes the cart.
- [The `TEST` scope surprises users who expect a cart to persist across tests or from suite setup] → The library
  introduction states the behaviour, and a spec scenario covers it. Changing it later is a spec change, not a bug fix.
- [A float `==` fails if the shop ever returns unrounded totals] → The shop returns 2-decimal values today. Users can
  write `validate    abs(value - 539.48) < 0.005`.
- [`Get Product Count` assumes the product list is not paged] → Version 0.3.0 has no paging fields. The seed-data
  test fails if that changes.
- [`float_str_verify_assertion` ignores `assertion_expected` when no operator is given, where `verify_assertion`
  raises] → This is the same behaviour as Browser's `Get Element Count`, and it is harmless.
- [The unit tests reach the client's `session` attribute] → The attribute is part of `ShopClient`'s public surface
  within the package and is documented as the test seam.

## Migration Plan

The package is new, so nothing needs migrating. Removing `hello()` affects no caller. To roll back, revert the change.

## Open Questions

- Whether the generated `docs/DemoShopLibrary.html` is committed or git-ignored. This affects neither behaviour nor
  tasks beyond one `.gitignore` line.
