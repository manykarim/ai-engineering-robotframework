# Bonus 1 - A library

Build a Robot Framework library with your agent: keywords for the DemoShop's REST API, with assertion operators as
Browser's `Get` keywords have them. Before the first prompt, you give the agent what it cannot guess: the toolstack,
the shop's API description at the version you test, the concept every `Get` keyword must follow, and keywords to
imitate. Then it works from a specification, slice by slice, as in Lab 5. The method is in
[Building libraries and tools with an agent](../../docs/building-with-agents.md).

| | |
|---|---|
| Module | Bonus 1 - Building a library with an agent |
| Time | about 120 minutes, self-paced |
| Shop preset | `clean` |
| You need | The workshop's clone with its environment, the local shop running, and OpenSpec (Lab 5) |
| You start from | A new folder next to your workshop clone |

## Steps

1. **Start the project next to the clone,** not inside it: the clone's `AGENTS.md` and `openspec/` would otherwise
   become the agent's context too.

   ```bash
   cd ..                                   # the folder that holds ai-engineering-robotframework
   uv init --lib demoshop-library
   cd demoshop-library
   uv add "robotframework==7.5" "robotframework-assertion-engine==5.0.1" "robotframework-pythonlibcore==4.6.0" "requests==2.34.2"
   uv add --dev pytest
   ```

2. **Save the references** the agent needs into the project. The shop's API description comes from your local,
   pinned shop: the public DemoShop at `https://demoshop.makrocode.de/docs` runs a newer development version, and
   is for reading only.

   ```bash
   mkdir references
   curl -s http://localhost:9090/openapi.json -o references/demoshop-openapi.json
   curl -sL https://raw.githubusercontent.com/MarketSquare/AssertionEngine/main/README.md -o references/assertionengine-readme.md
   # Keywords to imitate, and AssertionEngine's code, from the workshop's environment
   cd ../ai-engineering-robotframework
   uv run robotcode libdoc Browser show "Get Text" > ../demoshop-library/references/browser-get-text.md
   uv run robotcode libdoc Browser show "Get Element Count" > ../demoshop-library/references/browser-get-element-count.md
   uv run --no-sync python -c "import shutil, assertionengine.assertion_engine as m; shutil.copy(m.__file__, '../demoshop-library/references/assertion_engine.py')"
   cd ../demoshop-library
   ```

3. **Write `AGENTS.md`** yourself, from the skeleton in the
   [guide](../../docs/building-with-agents.md#2-five-kinds-of-context). For this project, it says:
   - **Toolstack:**
     - Python 3.12 with uv;
     - dependencies at run time: Robot Framework 7.5, AssertionEngine, PythonLibCore and requests, pinned in
       `pyproject.toml`;
     - unit tests with `uv run pytest`;
     - Robot tests in `atest/`, against the local shop at `http://localhost:9090`, run with
       `uv run robot --outputdir results atest`;
     - the keyword documentation is generated with
       `uv run python -m robot.libdoc "demoshop_library.DemoShopLibrary::url=http://localhost:9090" docs/DemoShopLibrary.html`: libdoc
       imports the library, so it needs the `url` the library takes;
     - packaging with `uv build`.
   - **References:**
     - `references/demoshop-openapi.json`, the API of the shop version under test;
     - the User Guide's
       [Creating test libraries](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#creating-test-libraries)
       and [library scope](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#library-scope),
       for Robot Framework 7.5.
   - **Concepts:**
     - every `Get` keyword takes `assertion_operator`, `assertion_expected` and `message`, and checks with
       AssertionEngine's `verify_assertion` (`references/assertion_engine.py`, `references/assertionengine-readme.md`);
     - the library is built on PythonLibCore;
     - it is imported with `url` and an optional `space`, which it sends as `X-Workshop-Space`;
     - each library instance keeps one cart.
   - **Examples:** `references/browser-get-text.md` and `references/browser-get-element-count.md`: keyword names,
     arguments and documentation to imitate.
   - **Specification:** OpenSpec, under `openspec/changes/`.

4. **Set up OpenSpec** for your agent, and give it the same context:

   | Claude Code | Codex | GitHub Copilot |
   |---|---|---|
   | `openspec init --tools claude` | `openspec init --tools codex` | `openspec init --tools github-copilot` |

   Uncomment `context:` in `openspec/config.yaml`, and write the five points of step 3 there in a few lines each.
   Start your agent in the project's folder, and ask it which instruction files it loaded: the project's, and none
   of the clone's.

5. **Propose the first slice** (`/opsx:propose` in Claude Code, `$openspec-propose` in Codex, `/opsx-propose` in
   GitHub Copilot):

   > A Robot Framework library, `demoshop_library.DemoShopLibrary`, for the DemoShop's REST API, built on
   > PythonLibCore, and imported with `url` and an optional `space`. A first slice of keywords: `Get Product Count`,
   > `Get Product Price` (a product id), `Add Product To Cart` (a product id and an optional quantity),
   > `Get Cart Item Count` and `Get Cart Total`. Every `Get` keyword takes `assertion_operator`,
   > `assertion_expected` and `message`, and checks with AssertionEngine, so that
   > `Get Product Price    1    ==    249.99` works as Browser's `Get Text` does. Each library instance keeps one
   > cart. Unit tests with pytest replace the HTTP layer; Robot tests in `atest/` run every keyword against the
   > local shop.

6. **Review the proposal** before anything is built, as in Lab 5:
   - Is every keyword named and argued like the examples: `Get <thing>`, then the three assertion arguments?
   - Does every check go through AssertionEngine, with no assertion code of the library's own?
   - Do the endpoints, parameters and headers match `references/demoshop-openapi.json`?
   - Do the Robot tests in `atest/` use only the library's keywords, against the local shop?

   Ask for changes until the answer to each is yes.

7. **Apply it** (`/opsx:apply`, `$openspec-apply-change` or `/opsx-apply`), then run the checks yourself:

   ```bash
   uv run pytest
   uv run robot --outputdir results atest
   uv run python -m robot.libdoc "demoshop_library.DemoShopLibrary::url=http://localhost:9090" docs/DemoShopLibrary.html
   uv build
   ```

   Open `docs/DemoShopLibrary.html`: does `Get Product Price` read like Browser's `Get Text`?

8. **Compare it with user keywords.** `resources/api.resource` in the workshop clone reaches the same API with user
   keywords and RequestsLibrary. Name one thing your library gives that the resource does not, and one thing it
   costs.

## Stretch

Propose the next slice the same way: checkout, and the confirmed order's number. Review it against the questions of
step 6 before you apply it.

## Compare with the reference

When you are done, compare your result with [the reference](https://manykarim.github.io/ai-engineering-robotframework/solutions/bonus-1-library): what the
rehearsal produced, why it is a good result, and the answers the debrief covers. Open it after the lab: it
gives the answers away.

## If your agent fails

Follow
[the recorded walkthrough of this lab](https://manykarim.github.io/ai-engineering-robotframework/transcripts/bonus-1-library).
