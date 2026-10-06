# Tasks

## 1. Project setup and test seam

- [x] 1.1 Add `[tool.pytest.ini_options] testpaths = ["tests"]` to `pyproject.toml`, replace the placeholder
  `description`, and add `results/` to `.gitignore`. Verify that `uv run pytest --collect-only` collects nothing from
  `references/` or `atest/`.
- [x] 1.2 Create `tests/conftest.py` with `FakeShop(requests.adapters.BaseAdapter)` (design decision 7). It records
  each `PreparedRequest` and returns canned responses registered by `(method, path)`. Add a `json_response(status,
  body)` helper and a `library` fixture factory that builds `DemoShopLibrary("http://shop.test", space=...)` and mounts
  the fake on its client session. Verify with a smoke test that a canned `GET /health` round-trips through a mounted
  plain `requests.Session`.

## 2. HTTP client (`src/demoshop_library/client.py`)

- [x] 2.1 Implement `ShopClient(url, space=None)` as in design decision 2:
  - remove any trailing slash from `url` and generate a `uuid4` hex `session_id`;
  - create a `requests.Session` whose only default header is `X-Workshop-Space`, set only when `space` is given;
  - provide `request(method, path, action, json=None, with_session=False)` with a 10-second timeout. It adds
    `X-Session-ID` only when `with_session` is true and returns the decoded JSON.

  Verify with `tests/test_client.py`:
  - no doubled slash when `url` ends with `/`;
  - the space header is present only when `space` is given;
  - `X-Session-ID` is present only when `with_session=True`;
  - two clients have different session ids;
  - no `Accept` header beyond requests' default is set;
  - a POST body is sent as JSON.
- [x] 2.2 Implement `DemoShopError` (`ROBOT_SUPPRESS_NAME = True`) and the error translation of design decision 6.
  Verify with unit tests that:
  - a 404 `{"detail":"Product not found"}` gives `<action> failed: Product not found (HTTP 404)`;
  - a 422 detail list gives `quantity: Input should be less than or equal to 20` and `HTTP 422`;
  - a 500 with a text body includes that text;
  - a non-JSON 200 gives `unexpected response`;
  - `requests.ConnectionError` gives a message containing the base URL.

## 3. Library class (`src/demoshop_library/library.py`)

- [x] 3.1 Create `DemoShopLibrary(DynamicCore)`. `__init__(url, space=None)` builds one `ShopClient` and the keyword
  components (an empty list until groups 4 and 5 register theirs). Set `ROBOT_LIBRARY_SCOPE = "TEST"` and
  `ROBOT_LIBRARY_VERSION` from package metadata. In `src/demoshop_library/__init__.py`, export `DemoShopLibrary` and
  `__version__` and remove `hello()`. Verify with `tests/test_library.py`: importing sends no request; the scope is
  `"TEST"`; two instances have different session ids; `from demoshop_library import DemoShopLibrary` works.
- [x] 3.2 Write the library introduction, covering `url`, `space`, one cart per instance and the `TEST` scope, with an
  `= Assertions =` section that holds AssertionEngine's operator table, and the `__init__` import documentation.
  Verify that `DemoShopLibrary(...).get_keyword_documentation("__intro__")` contains `= Assertions =` and that the
  `__init__` documentation names both arguments.

## 4. Product keywords (`src/demoshop_library/products.py`)

- [x] 4.1 Implement `Get Product Count` (`GET /api/products/`, `len(items)`, `int_str_verify_assertion`, subject
  `Product count`, tags `Assertion`, `Getter`, `Products`) and register `ProductKeywords` in the library. Verify with
  unit tests through `run_keyword`:
  - it sends `GET /api/products/` without an `X-Session-ID` header;
  - it returns `12` for a 12-item fake catalogue;
  - `AssertionOperator["=="]` with `"12"` passes;
  - a mismatch fails with `Product count '12' (int) should be '13' (int)`.
- [x] 4.2 Implement `Get Product Price` (`product_id: int`, `GET /api/products/{id}`, `float(price)`,
  `float_str_verify_assertion`, subject `Product <id> price`). Verify with unit tests:
  - it sends `GET /api/products/1` without an `X-Session-ID` header;
  - it returns the float `249.99`, and a price of `799` is returned as `799.0`;
  - `==` with `"249.99"` and with `"799"` passes;
  - a mismatch with `"10"` fails with `Product 1 price '249.99' (float) should be '10.0' (float)`;
  - `validate` passes and fails as specified, and `then` with `value * 2` returns `499.98`;
  - `contains` fails as not allowed and sends no request;
  - a 404 fails with a message containing `999999`, `Product not found` and `404`.

## 5. Cart keywords (`src/demoshop_library/cart.py`)

- [x] 5.1 Implement `Add Product To Cart` (`product_id: int`, `quantity: int = 1`, `POST /api/cart/items`, tags
  `Setter`, `Cart`) and register `CartKeywords` in the library. Verify with unit tests:
  - the default body is `{"product_id": 1, "quantity": 1}` and an explicit quantity is sent as given;
  - the request carries the instance's `X-Session-ID`, the same one as a later `GET /api/cart/` from that instance;
  - a 404 fails with a message containing the product id, `Product not found` and `404`;
  - a 422 fails with a message containing the shop's validation message and `422`.
- [x] 5.2 Implement `Get Cart Item Count` (`GET /api/cart/`, the sum of `quantity` over `items`,
  `int_str_verify_assertion`, subject `Cart item count`, tags `Assertion`, `Getter`, `Cart`). Verify with unit tests
  that an empty cart gives `0`, lines with quantities 2 and 1 give `3`, and `>` with `"0"` on an empty cart fails with
  `Cart item count '0' (int) should be greater than '0' (int)`.
- [x] 5.3 Implement `Get Cart Total` (`GET /api/cart/`, `float(total)`, `float_str_verify_assertion`, subject
  `Cart total`). Verify with unit tests that an integer `0` total returns `0.0`, a total of `539.48` passes `==` with
  `"539.48"`, and `message=Total was {value}, wanted {expected}` with `==` and `"5"` on an empty cart fails with
  `Total was 0.0, wanted 5.0`.
- [x] 5.4 Check the public keyword surface. Verify with a unit test that `get_keyword_names()` returns exactly the
  five keywords. For each keyword, `get_keyword_arguments`, `get_keyword_types` and `get_keyword_tags` must match
  design decision 4:
  - every `Get` keyword ends with `assertion_operator`, `assertion_expected` and `message`, with the defaults
    `None`/`0`/`None`;
  - `product_id` and `quantity` are typed `int`, and `assertion_operator` is typed `AssertionOperator | None`. These
    types make Robot reject `abc` and `===`;
  - the tags are as listed.

## 6. Keyword documentation

- [x] 6.1 Write the documentation of the five keywords in the shape of `references/browser-get-text.md` and
  `references/browser-get-element-count.md`: a summary line, an `| =Arguments= | =Description= |` table whose operator
  row links to `Assertions`, the "Optionally asserts ..." paragraph for `Get` keywords, and an `Example:` block, for
  example `Get Product Price    1    ==    249.99`. Verify that
  `uv run python -m robot.libdoc "demoshop_library.DemoShopLibrary::url=http://localhost:9090" docs/DemoShopLibrary.html` succeeds, and that the
  page lists all five keywords with working `Assertions` links.
- [x] 6.2 Settle the open question about generated docs: commit `docs/DemoShopLibrary.html`, or add `docs/` to
  `.gitignore`. Verify that `git status` matches the choice.

## 7. Acceptance tests (`atest/`, against `http://localhost:9090`)

The rules of design decision 8 apply to every suite:
- test cases, setups and teardowns call only `DemoShopLibrary` keywords, with no BuiltIn keywords, no other libraries
  and no direct HTTP;
- every check is a `Get` keyword's inline assertion;
- every import points at `${SHOP_URL}`.

Failure scenarios are verified in groups 2, 4 and 5.

- [x] 7.1 Create `atest/resources/demoshop.resource` holding variables only: `${SHOP_URL}` (default
  `http://localhost:9090`), `${WORKSHOP_SPACE}` (default `${NONE}`; not `${SPACE}`), and the seed data
  (`${PRODUCT_COUNT}` 12, product 1 `249.99`, product 2 `39.5`, product 5 `799`). Verify that
  `uv run robot --dryrun atest` passes once the suites exist.
- [x] 7.2 Write `atest/product_keywords.robot`. It imports the library with `url=${SHOP_URL}` and
  `space=${WORKSHOP_SPACE}` and runs `Get Product Count    ==    ${PRODUCT_COUNT}`, `Get Product Price    1    ==    249.99`
  and `Get Product Price    5    ==    799`. Verify that `uv run robot --outputdir results atest/product_keywords.robot`
  passes.
- [x] 7.3 Write `atest/cart_keywords.robot`. It covers the passing scenarios of `specs/cart-keywords/spec.md`:
  - an empty cart: count `0`, total `0`;
  - the default quantity;
  - an explicit quantity;
  - the same product added twice: count `3`, total `749.97`;
  - two products: count `3`, total `539.48`;
  - one add with quantity 2: total `499.98`.

  Each check is `Get Cart Item Count` or `Get Cart Total` with `==`. Verify that the suite passes against the shop.
- [x] 7.4 Write `atest/getter_assertions.robot`. It covers the passing scenarios of `specs/getter-assertions/spec.md`:
  - positional and named assertion arguments, for example `Get Cart Total    assertion_operator=>=    assertion_expected=0`;
  - the operator aliases (`should be`, `greater than`, ...);
  - the remaining comparison operators;
  - `validate    100 < value < 300`.

  Verify that the suite passes against the shop.
- [x] 7.5 Write `atest/library_import.robot`. It imports the library twice, as `ShopA` with `url=${SHOP_URL}` and as
  `ShopB` with `url=${SHOP_URL}/` and `space=atest`, and has these tests:
  - `ShopB` keywords pass, covering the trailing-slash URL and the space;
  - `ShopA.Add Product To Cart    1`, then `ShopB.Get Cart Item Count    ==    0` and
    `ShopA.Get Cart Item Count    ==    1`;
  - a test that adds products, followed by a test whose `ShopA.Get Cart Item Count    ==    0` passes;
  - a `[Setup]` that adds product 1, with the body checking `==    1`;
  - a `Suite Setup` that adds product 1, with a test checking `==    0`.

  Verify that the suite passes against the shop.
- [x] 7.6 Check that the acceptance tests use only the library's keywords. Verify by reading `results/output.xml`
  from a full `uv run robot --outputdir results atest` run with `robot.api.ExecutionResult`: every executed keyword's
  `owner` must be `demoshop_library.DemoShopLibrary`, `ShopA` or `ShopB`.

## 8. Final checks

- [x] 8.1 Add a README usage section with the import example, the five keywords, and the commands for unit tests,
  acceptance tests and libdoc. Verify that the README's examples match the keyword signatures in the libdoc output.
- [x] 8.2 Run the whole suite. Verify that `uv run pytest` and `uv run robot --outputdir results atest` both pass with
  no failures, that the 7.6 check passes, and that `uv build` produces a wheel containing `demoshop_library/{__init__,library,client,products,cart}.py`
  and `py.typed`, but not `tests/` or `atest/`.
