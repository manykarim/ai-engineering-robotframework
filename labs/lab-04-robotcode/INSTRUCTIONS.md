# Lab 4 - RobotCode

Teach your agent to work like a Robot Framework engineer who knows your setup: ask the project instead of grepping
it, look up the installed libraries instead of guessing, and debug a failing test at a live breakpoint instead of
re-running it blindly. All of it through the [RobotCode](../../GLOSSARY.md#robotcode) command line. No server is
involved.

| | |
|---|---|
| Module | 4 - RobotCode for Agents |
| Time | 25 minutes |
| Shop preset | `clean` |
| You need | Lab 0 done |
| You start from | `main`, plus your work from Labs 2 and 3 if you have it |

## Steps

1. **Install the RobotCode plugin** for your agent, from its marketplace. The version is recorded in `SETUP.md`:

   | Claude Code | Codex | GitHub Copilot |
   |---|---|---|
   | `claude plugin marketplace add --scope project robotcodedev/robotframework-agent-plugins` | `codex plugin marketplace add robotcodedev/robotframework-agent-plugins` | `copilot plugin marketplace add robotcodedev/robotframework-agent-plugins` |
   | `claude plugin install --scope project robotcode@robotframework-agent-plugins` | `codex plugin add robotcode@robotframework-agent-plugins` | `copilot plugin install robotcode@robotframework-agent-plugins` |
   | recorded in `.claude/settings.json`, so your fork remembers it | installed for your user | installed for your user |

   Start a new session afterwards, so that the agent loads it.

2. **Tie it to your context.** Add one line to `AGENTS.md`, so that every session knows the plugin's commands apply
   here:

   ```markdown
   Use RobotCode through uv (`uv run robotcode ...`) to discover tests and keywords, read library docs, debug
   failing tests and read results.
   ```

3. **Ask a discovery question:**

   > Which tests of this repository carry the tag ui, and in which files are they? Ask the project; don't grep.

   Watch the tool calls: the answer should come from `uv run robotcode discover`, which resolves tests and tags
   the way Robot Framework does at run time. Reading the files gets half the story: tags can also come from
   settings and from the command line.

4. **Ask a library question:**

   > Which keyword of the installed Browser library reads the state of a checkbox, and what are its arguments?

   The answer should come from `uv run robotcode libdoc Browser`: the version this repository pins, not the one
   the model remembers.

5. **Debug a broken test.** One of the two tests that fail on purpose is yours now:

   > The test "WEB-002_AC-12 Handpicked Highlights" fails. Find out why with the RobotCode debugger: stop at the
   > assertion that fails and look at the variables it compares. Don't guess from the failure message. Then tell me
   > the cause before you change anything.

   The agent should run `uv run robotcode robot-debug` with a breakpoint, and report what it saw. Check its
   explanation against what the criterion says in `openspec/specs/shop/catalogue`. Then:

   > Fix the test so that it verifies what the criterion says, remove its broken tag, and run it.

   The test passes. It is no longer broken on purpose, so it no longer carries the tag.

6. **Explore with the REPL.** The REPL is for flows no test covers yet. The price range filter (WEB-002_AC-8) is
   one:

   > No test covers the price range filter yet. Explore it with the RobotCode REPL and a visible browser
   > (HEADLESS set to False): open the products page through resources/shop.resource, set the range to $100-$300,
   > apply the filters, and tell me which keywords and locators would work for a test. Don't write a test file.

   A browser window opens and follows the agent's steps. The REPL is the right tool *only* here. An agent that
   opens the REPL to investigate the failing test of step 5 is misusing it: look out for that in the debrief.

## Stretch

Ask a results question about the last run:

> Of the tests tagged WEB-002 in the last run, which failed and why? Use the results, not output.xml.

It should use `uv run robotcode results show` with a tag filter.

## If your agent fails

Follow [the recorded walkthrough of this lab](../../transcripts/lab-04-robotcode.md). You can also run steps 3 and 4
yourself: `uv run robotcode discover tests` and `uv run robotcode libdoc Browser list`.
