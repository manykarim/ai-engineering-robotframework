# RobotCode cheat sheet

*For RobotCode 2.7.0 with Robot Framework 7.5 and Browser 20.5.0, the versions this repository pins. Every example
ran here with the shop in `clean`; the output is shortened.*

The commands your agent learns in [Lab 4](../labs/lab-04-robotcode/INSTRUCTIONS.md), on one page, with what they are
for and where they trip you up. Always run them as `uv run robotcode ...`: that is the RobotCode installed in this
project, which sees its libraries at their pinned versions. With the shared instance, put `-p shared` before the
command, for example `uv run robotcode -p shared robot-debug ...`.

## Which command for which question

| Question | Command |
|---|---|
| Which tests, suites and tags exist? | `discover tests`, `discover tags` |
| Which keyword does this, and how do I call it? | `libdoc Browser list "<pattern>"`, then `libdoc Browser show "<keyword>"` |
| What is wrong in these files, without running them? | `analyze code tests resources` |
| Why does this test fail? | `robot-debug -t "<test>"`: it stops at the failure |
| Does this step work on the page, before any test exists? | `repl` |
| What failed in the last run? | `results summary`, `results show --failed` |
| What changed between two runs? | `results diff <before> <after>` |

## Discover

Asks the project, resolved the way Robot Framework resolves it at run time, without running anything:

```text
$ uv run robotcode discover tests -i WEB-006
- **Tests.Ui.Checkout.WEB-006_AC-1 Order Total Adds Up** (`tests/ui/checkout.robot:17`)
- **Tests.Ui.Checkout.WEB-006_AC-7 Successful Order** (`tests/ui/checkout.robot:27`)
- **Tests.Ui.Checkout.WEB-006_AC-11 Validation Errors Next To Fields** (`tests/ui/checkout.robot:35`)
- **Tests.Ui.Checkout.WEB-006_AC-12 Cart Cleared After Order** (`tests/ui/checkout.robot:50`)
```

- `discover tags` lists every tag; `discover tests --tags` shows each test's tags.
- `--search "<text>"` matches keyword calls as well as names. `--search "Place Order"` lists the three tests that call
  that keyword.
- `discover info` prints the versions of Robot Framework, RobotCode and Python it runs with.
- `--format json`, before the command, gives the same as JSON for scripts: `uv run robotcode --format json discover tests`.

## Libdoc

The documentation of a library as installed here, or of one of this repository's resource files:

```text
$ uv run robotcode libdoc Browser version
20.5.0
$ uv run robotcode libdoc Browser list "Wait For*"
Wait For
Wait For Alert
Wait For Condition
Wait For Elements State
...
$ uv run robotcode libdoc Browser show "Get Title"
### Get Title
#### Arguments
* `assertion_operator` (type: `AssertionOperator | None`, default: `None`)
* `assertion_expected` (type: `Any | None`, default: `None`)
* `message` (type: `str | None`, default: `None`)
...
$ uv run robotcode libdoc resources/shop.resource list
Go To Shop Page
Open Shop Browser
Start Shop Test
```

## Analyze

Checks test and resource files without running them, resolved the way Robot Framework resolves them: keywords and
variables that do not exist, wrong arguments, imports that fail.

```text
$ uv run robotcode analyze code tests resources
resources/shop.resource:17:45: [ERROR] VariableNotFound: Variable '${HEADLESS}' not found.
Files: 8, Errors: 1, Warnings: 0, Infos: 0, Hints: 0 (in 2.44s)
```

- Name the folders to check. Without them, it checks everything below the current directory.
- `--severity error` reports only errors, and `--code KeywordNotFound` only that kind.
- The exit code adds up what it found: 1 for errors, 2 for warnings, 4 for information, 8 for hints. 0 means
  nothing.
- `--format json`, before the command, gives the findings as JSON: `uv run robotcode --format json analyze code tests`.
- The one error here is a false positive: see [Traps](#traps). A finding is a question, not a verdict.

## The debugger

`robot-debug` runs real tests with every setting of `robot.toml`, and pauses:
- at the first failure, before it unwinds, with the failing values still in scope (the default);
- at a keyword, with `--break "<keyword>"`, or at a line, with `--break tests/ui/catalogue.robot:22`.

At the `(rdb)` prompt:
- `.where` shows the stack, `.list` the source, `.vars` the variables, and `.print ${x}` one value;
- any keyword you type runs inside the paused test. In a browser test, the page is still open, so `Get Url` or
  `Get Title` read the live page;
- `.step` and `.next` go on step by step, `.continue` runs on, and `.abort` stops the run.

Piped, as an agent runs it (see [Driving RobotCode from an agent](#driving-robotcode-from-an-agent)):

```text
$ printf '.where\n.print ${cards}\nGet Url\n.continue\n' | uv run robotcode robot-debug --plain \
    --break "Get Add To Cart Button Count" -t "WEB-002_AC-1 Every Card Offers Add To Cart"
* breakpoint  catalogue.Get Add To Cart Button Count  (tests/ui/catalogue.robot:22)
(rdb) > #0  catalogue.Get Add To Cart Button Count      tests/ui/catalogue.robot:22
  #1  WEB-002_AC-1 Every Card Offers Add To Cart  tests/ui/catalogue.robot:17
  ...
(rdb) ${cards} = 12
(rdb) => 'http://localhost:9090/products'
(rdb) | PASS |
```

## The REPL

For a flow no test covers yet: each line is one step, and the browser and the variables stay alive between lines
until the session ends. To debug a test that exists, use the debugger instead.

```text
$ printf 'Import Resource    ${EXECDIR}/resources/shop.resource\nOpen Shop Browser\nStart Shop Test\nGo To Shop Page    /\n${title}=    Get Title\n.kw Shop\n.exit\n' \
    | uv run robotcode repl --plain
[ INFO ] ${headless} = True
...
[ INFO ] Successfully opened URL http://localhost:9090/
[ INFO ] ${title} = Flowline Supply | Shop the Future
# Keywords matching 'Shop'
## shop (Resource)
- Go To Shop Page
- Open Shop Browser
- Start Shop Test
```

- Add `-v HEADLESS:False` to watch the browser follow the steps.
- `.kw <text>` searches the keywords of everything imported, `.imports` lists the imports, and `.vars` the variables.
- `.save -t "<test name>" <file>.robot` turns the session into a test file; quote a name of several words.
- `.exit` ends the session. So does the end of piped input.

## Results

Reads the last run's `output.xml` from `results/`, or the one you name with `-o`:

```text
$ uv run robotcode results summary
- _Status:_ ✅ **PASS**
- _Total:_ 11
- _Passed:_ 11
...
$ uv run robotcode results show -i WEB-006 --sort elapsed --top 2
- ✅ **PASS** Tests.Ui.Checkout.WEB-006_AC-12 Cart Cleared After Order (`tests/ui/checkout.robot:50`) _(22:19:54 · 859 ms)_
- ✅ **PASS** Tests.Ui.Checkout.WEB-006_AC-7 Successful Order (`tests/ui/checkout.robot:27`) _(22:19:52 · 707 ms)_
```

- `results show --failed` lists the failures with their messages; `-i <tag>` filters by tag.
- `results stats --by tag` counts passes, failures and time per tag.
- `results diff <before>/output.xml <after>/output.xml` lists new failures, new passes, other status changes, and
  tests added or removed between two runs.

## Driving RobotCode from an agent

The REPL and the debugger wait at a prompt for the next line, and an agent's shell commands usually run to
completion. There are two ways:

1. **Interactively**, when the agent can keep a terminal open between its steps. The RobotCode plugin prefers this.
2. **Piped**, when every command must finish: one command per line, ending with one that resumes, `.continue` for
   the debugger or `.exit` for the REPL. The examples above are piped.

What to know about the piped form:
- When the input ends, the debugger resumes and the run finishes, and the REPL ends. Nothing waits forever.
- `--plain` makes RobotCode read line by line. It chooses that by itself when it detects an agent; say it anyway in
  scripts.
- Each piped command is a new process: its browser and variables are gone when it ends, and the next look at the page
  starts again. A session that stays open between the agent's steps is what the [MCP server](../GLOSSARY.md#mcp) adds
  in Lab 6.
- The examples use a POSIX shell: bash, zsh, or Git Bash on Windows. In PowerShell, pipe the same lines in its own
  syntax; that form is not tested here.

## Traps

| Trap | What you see | What to do |
|---|---|---|
| The REPL does not create its output directory: `results/`, or the one given with `-d` | `FileNotFoundError: ... playwright-log.txt` when the browser opens | create the directory first. `results/` exists once a test has run in the clone |
| `Import Resource` at run time resets a variable given with `-v`, if the resource sets it in a variable table | the REPL ignores your `-v` | give the default in the keyword with `Get Variable Value`, as `resources/shop.resource` does for `HEADLESS` |
| `.break "<keyword>"` with quotes at the `(rdb)` prompt | the breakpoint never stops | leave out the quotes there: `.break Go To Catalogue`. On the command line, `--break "<keyword>"` is right |
| The REPL's exit code | always 0, and its `output.xml` says PASS, whatever failed | read the output, or run a test for a verdict |
| `.save` | lines that failed are saved too | save a clean session, or delete those lines afterwards |
| `analyze code` and a variable read with `Get Variable Value` and a default | `VariableNotFound` for `${HEADLESS}` in `resources/shop.resource`, and exit code 1 | nothing: the default makes the line safe. To silence it, put `# robotcode: ignore[variable-not-found]` at the end of that line. A variable table instead would bring back the trap with `-v` above |
| `results diff` | exits 0 even with new failures | to fail a script on new failures, count `newFailures` in `--format json` |
| RequestsLibrary's log | every request and response, with headers and body, in `output.xml` and `log.html` | never send a real credential from a test; results uploaded from a public fork are public |

## Further reading

The RobotCode reference: [discovering tests](https://robotcode.io/03_reference/discovering-tests),
[the REPL](https://robotcode.io/03_reference/repl), [the debugger](https://robotcode.io/03_reference/robot-debug),
[analyzing code](https://robotcode.io/03_reference/analyzing-code),
[analyzing results](https://robotcode.io/03_reference/analyzing-results) and
[AI agents](https://robotcode.io/03_reference/ai-agents).
