# Building libraries and tools with an agent

The agent that writes your tests can also write a Robot Framework library or tool: keywords for your own system, a
listener, an integration with a test-management service. It does that well when it starts from the right context,
and badly when it starts from what it remembers. This page is the method of the two bonus labs,
[Bonus 1](../labs/bonus-1-library/INSTRUCTIONS.md) and [Bonus 2](../labs/bonus-2-tool/INSTRUCTIONS.md). The
references are for Robot Framework 7.5, the version this workshop pins.

## 1. Start outside every other project

Agents collect instructions from more than the folder they start in:
- **Claude Code** reads `CLAUDE.md` from the working folder and every folder above it.
- **Codex** reads `AGENTS.md` from the git repository's root down to the working folder.
- **OpenSpec** uses the nearest `openspec/` folder.

A library created inside the workshop clone would get the clone's rules: the demo shop, the test conventions, the
boundaries of the labs. Create it next to the clone instead. `uv init` makes it a git repository of its own:

```bash
cd ..                                # the folder that holds ai-engineering-robotframework
uv init --lib demoshop-library
cd demoshop-library
```

Before the first real prompt, ask your agent which instruction files it loaded (in Claude Code, `/memory` lists
them). If it names a file from outside the new project, move the project somewhere without one.

## 2. Five kinds of context

Write them into the project's `AGENTS.md` before you ask for any code:

| Context | What it says | Example |
|---|---|---|
| **Toolstack** | how the project is built, tested and packaged, and what it may depend on | `uv add`, never pip; `uv run pytest`; `uv build` |
| **References** | the specifications to build against, at the versions in use, as saved files where possible | the service's OpenAPI description; a User Guide chapter for 7.5 |
| **Concepts** | the ideas the code must follow | AssertionEngine's operators; the listener interface, version 3 |
| **Examples** | code or keywords to imitate | Browser's `Get Text`, saved from libdoc |
| **Specification** | where the agreed behaviour lives, and that work follows it | OpenSpec: `openspec/changes/<name>/` |

A skeleton:

```markdown
# AGENTS.md

<One sentence: what this project is, and who uses it.>

## Toolstack
- Python 3.12, managed with uv: `uv add <package>` for every dependency, never pip.
- Unit tests: `uv run pytest`. Robot Framework tests: `uv run robot atest`.
- Package: `uv build`. Dependencies at run time: <the list>, pinned in pyproject.toml.

## References
- <the interface or API to build against: a saved file under references/>
- <the User Guide chapter for it, at Robot Framework 7.5>
- <the Robot API page for it, at Robot Framework 7.5>

## Concepts
- <what the code must follow, and where to read about it>

## Examples
- <keywords or code to imitate: saved files under references/>

## Specification
- Every change goes through OpenSpec, under openspec/changes/. Build only what the current change's tasks say.
```

Keep it short. It is loaded into every session, and the references it names are read only when needed.

## 3. Spec-driven from the first prompt

Set OpenSpec up in the new project, for your agent:

```bash
openspec init --tools claude         # or: codex, github-copilot
```

`openspec/config.yaml` then holds a commented example of `context:`. Uncomment it, and write the five kinds of
context in a few lines each. Every proposal, spec, design and task list the agent writes then starts from them.
Then propose one slice, for example *"the catalogue keywords"*: `/opsx:propose` (Claude Code), `$openspec-propose`
(Codex) or `/opsx-propose` (GitHub Copilot). It is the same flow as Lab 5.

## 4. Where Robot Framework documents what you build

All links are for Robot Framework 7.5. A link without a version, such as `latest`, moves on to the next release,
while your project stays on its pinned one.

| You build | User Guide | Robot API |
|---|---|---|
| a keyword library | [Creating test libraries](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#creating-test-libraries), [library scope](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#library-scope), [hybrid library API](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#hybrid-library-api), [dynamic library API](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#dynamic-library-api), [Libdoc](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#libdoc) | the [`keyword`](https://robot-framework.readthedocs.io/en/v7.5/autodoc/robot.api.html#robot.api.deco.keyword) and [`library`](https://robot-framework.readthedocs.io/en/v7.5/autodoc/robot.api.html#robot.api.deco.library) decorators |
| a listener | [Listener interface](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#listener-interface), [version 3](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#listener-version-3), [examples](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#listener-examples) | [`ListenerV3`](https://robot-framework.readthedocs.io/en/v7.5/autodoc/robot.api.html#robot.api.interfaces.ListenerV3), and the [`running`](https://robot-framework.readthedocs.io/en/v7.5/autodoc/robot.running.html#robot.running.model.TestSuite) and [`result`](https://robot-framework.readthedocs.io/en/v7.5/autodoc/robot.result.html#robot.result.model.TestSuite) models it receives |
| a pre-run modifier | [Modifying executed suites and tests](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#modifying-executed-suites-and-tests) | [`SuiteVisitor`](https://robot-framework.readthedocs.io/en/v7.5/autodoc/robot.model.html#robot.model.visitor.SuiteVisitor) |
| a tool that reads results | [Modifying results](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#modifying-results) | [`ExecutionResult`](https://robot-framework.readthedocs.io/en/v7.5/autodoc/robot.result.html#robot.result.resultbuilder.ExecutionResult), [`ResultVisitor`](https://robot-framework.readthedocs.io/en/v7.5/autodoc/robot.result.html#robot.result.visitor.ResultVisitor) |
| a parser for test data | [Parser interface](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#parser-interface) | the [`robot.api`](https://robot-framework.readthedocs.io/en/v7.5/autodoc/robot.api.html) page, *parsing* |

Concepts other libraries share:
- [AssertionEngine](https://github.com/MarketSquare/AssertionEngine): the assertion operators of Browser's `Get`
  keywords (`Get Text    h1    ==    Welcome`), as a library your own keywords can use.
- [PythonLibCore](https://github.com/robotframework/PythonLibCore): the structure Browser and others build their
  libraries on, with keywords spread over several classes.

Both are installed in the workshop's environment, as dependencies of Browser, so an agent can read their code there.

## 5. Save what the agent cannot read

A link helps only if the agent can open it. Save every reference it needs into the project, under `references/`,
and name the files in `AGENTS.md`:

- **An API's description:** export it, at the version you build against. The workshop's shop is pinned, while the
  public DemoShop runs a newer development version:

  ```bash
  curl http://localhost:9090/openapi.json -o references/demoshop-openapi.json
  ```

- **The part you need of a large description:** GitHub's REST description is about 10 MB. Keep the paths you use:

  ```bash
  uv run --no-project python -c "
  import json, urllib.request
  url = 'https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/dereferenced/api.github.com.deref.json'
  spec = json.load(urllib.request.urlopen(url))
  keep = ['/repos/{owner}/{repo}/issues', '/repos/{owner}/{repo}/issues/{issue_number}/comments']
  json.dump({path: spec['paths'][path] for path in keep}, open('references/github-issues.json', 'w'), indent=1)
  "
  ```

- **Keywords to imitate:** save their documentation from a project where the library is installed, for example
  Browser's from the workshop clone:

  ```bash
  uv run robotcode libdoc Browser show "Get Text" > ../demoshop-library/references/browser-get-text.md
  ```

- **A manual that refuses agents:** some answer automated requests with *403 Forbidden*, as TestRail's API manual
  does. Open it in your browser and save the pages you need under `references/`, or export the service's API
  description if it offers one.

## 6. One slice at a time

Propose a slice of three to five keywords, or one event of a listener. Read the proposal as you would review a
colleague's: is every keyword named the way the examples are, does every assertion use the concepts you named? Then
apply it, run the checks, and look at the result before you propose the next slice.
