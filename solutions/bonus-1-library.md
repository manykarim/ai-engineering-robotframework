# Bonus 1 - A library: the reference

[Bonus 1](../labs/bonus-1-library/INSTRUCTIONS.md) has you build a Robot Framework library for the DemoShop's REST
API, with your agent, from a context you write before the first prompt. The reference is the rehearsal's result,
with Claude Code, recorded in the [transcript](../transcripts/bonus-1-library.md). Its project is on this branch,
under `bonus/bonus-1-library/`.

## The reference

`AGENTS.md`, written from the lab's list in step 3, with the libdoc command as the lab now gives it:

```markdown
# AGENTS.md

## Toolstack

- Python 3.12 with uv.
- Run-time dependencies: Robot Framework 7.5, AssertionEngine, PythonLibCore and requests, pinned in `pyproject.toml`.
- Unit tests: `uv run pytest`.
- Robot tests live in `atest/` and run against the local shop at `http://localhost:9090`:
  `uv run robot --outputdir results atest`.
- Keyword documentation:
  `uv run python -m robot.libdoc "demoshop_library.DemoShopLibrary::url=http://localhost:9090" docs/DemoShopLibrary.html`.
- Packaging: `uv build`.

## References

- `references/demoshop-openapi.json`: the API of the shop version under test.
- Robot Framework 7.5 User Guide:
  [Creating test libraries](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#creating-test-libraries)
  and [Library scope](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#library-scope).

## Concepts

- Every `Get` keyword takes `assertion_operator`, `assertion_expected` and `message`, and checks with
  AssertionEngine's `verify_assertion` (see `references/assertion_engine.py` and
  `references/assertionengine-readme.md`).
- The library is built on PythonLibCore.
- It is imported with `url` and an optional `space`, which it sends as the `X-Workshop-Space` header.
- Each library instance keeps one cart.

## Examples

- `references/browser-get-text.md` and `references/browser-get-element-count.md`: imitate their keyword names,
  arguments and documentation.

## Specification

- OpenSpec, under `openspec/changes/`.
```

`demoshop_library.DemoShopLibrary`, in about 400 lines: a `DynamicCore` from PythonLibCore, with the keywords in
`products.py` and `cart.py`, the HTTP calls in `client.py` and AssertionEngine's operators in `assertions.py`. A
keyword, with the argument table Browser's `Get Text` has:

```python
    @keyword(tags=("Assertion", "Getter", "Products"))
    def get_product_price(
        self,
        product_id: int,
        assertion_operator: AssertionOperator | None = None,
        assertion_expected: float | str = 0,
        message: str | None = None,
    ) -> float:
        """Returns the price of the product with ``product_id`` as a float.

        | =Arguments= | =Description= |
        | ``product_id`` | Id of the product, an integer. An unknown id fails the keyword with the shop's ``Product not found``. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the assertion |
        | ``message`` | overrides the default error message for assertion. |
```

76 unit tests run against a fake shop, and 26 Robot tests in `atest/` run every keyword against the local shop.
`Get Product Price    1    ==    249.99` passes, and `Get Product Price    1    ==    1` fails with AssertionEngine's
message:

```text
Product 1 price '249.99' (float) should be '1.0' (float)
```

## Why it is a good result

- **The context came first.** `AGENTS.md` names the toolstack, the saved API description of the pinned shop,
  AssertionEngine's code and README, and two Browser keywords to imitate. The keywords' names, arguments and
  documentation follow those examples.
- **Every check goes through AssertionEngine.** The library has no assertion code of its own, so its operators and
  messages are those of Browser's `Get` keywords.
- **The endpoints and headers come from the saved description:** the space in `X-Workshop-Space`, the cart in
  `X-Session-ID`.
- **A cart per test.** The library's `TEST` scope gives every test a new instance, so no test inherits another's
  cart. Its documentation says so, with an example of two carts in one test.

## What to debrief

- **What the lab got wrong.** The lab's first text gave a libdoc command without the library's `url`. libdoc
  imports the library to read its keywords, so the command failed, and the agent paused instead of guessing. The
  lab now gives the command with `::url=http://localhost:9090`. An agent that stops on a wrong instruction is worth
  more than one that works around it.
- **The size of the slice.** For five keywords, the agent planned 22 tasks, and propose, review and apply took more
  than an hour. Review the tasks before you apply them.
- **Library or user keywords?** Asked to compare the library with `resources/api.resource`, the agent answered:

  > **Gives:** The library's keywords check the result in the same step, and their failures are worded in shop terms. For example, `Get Product Price    1    ==    249.99` compares two floats and fails with `Getting product 999999 failed: Product not found (HTTP 404)`, whereas `Get Catalogue From API` returns raw JSON, so the test has to make its own checks and gets RequestsLibrary's generic HTTP error. **Costs:** The library is a Python package with its own unit tests, dependency pins, build and release, so supporting a new endpoint means writing Python, while the resource is about 25 lines of Robot that any tester can edit in place.

## Compare yours

The reference is on the `solutions` branch, which your fork does not have. From your workshop clone:

```bash
git fetch upstream solutions
mkdir -p ../reference && git archive upstream/solutions bonus/bonus-1-library | tar -x -C ../reference
diff ../reference/bonus/bonus-1-library/AGENTS.md ../demoshop-library/AGENTS.md
```

No `upstream` remote yet? [Add it first](README.md#compare-your-files-with-the-reference).
