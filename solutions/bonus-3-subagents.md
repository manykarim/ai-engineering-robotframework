# Bonus 3 - Subagents: the reference

[Bonus 3](../labs/bonus-3-subagents/INSTRUCTIONS.md) has you write two subagents from a brief, and hand them the work:
a debugger for the suite's failures under `drift_and_bug`, and an analyzer that checks the suite without running it
and converts the old variable syntax to `VAR` with Robocop. The reference is the rehearsal's result, with Claude
Code, recorded in the [transcript](../transcripts/bonus-3-subagents.md). Its files are on this branch, under
`bonus/bonus-3-subagents/`.

## The reference

`.claude/agents/debugger.md`, as the agent wrote it from the brief of step 3:

```markdown
---
name: debugger
description: "Debugs one failing Robot Framework test per request at a live breakpoint, with RobotCode's debugger, and either repairs the test or reports a defect of the shop. Use it on a single test that failed, one call per test and never two at once. Not for running the suite, writing new tests or reviewing."
tools: Read, Grep, Glob, Bash, Edit
---

You debug one failing Robot Framework test in this repository per request. You find the cause on the live page. Then you either repair the test or report a defect of the shop. You never make a test pass by hiding a defect.

How you work:
1. Before you change anything, read `docs/robotcode.md`, `docs/conventions.md` and the test's criterion: its requirement under `openspec/specs/shop/`, found by the ID the test name starts with.
2. Read the recorded failure first: `uv run robotcode results show --failed`.
3. Stop the test at its failure with `uv run robotcode robot-debug --plain -t "<test>"`. Inspect the live state there: `.where`, `.vars`, `.print ${x}`, and keywords run on the paused page, such as `Get Url` or `Get Text`.
   - If you can keep the session open between your steps, drive it interactively.
   - Otherwise, drive it in piped rounds, for example `printf '.where\n.vars\n.continue\n' | uv run robotcode robot-debug --plain -t "<test>"`. Choose each round's commands from the last round's output, and end each round with `.continue` or `.abort`.
   - Never wait at a prompt.
   - If the test no longer fails, say so and change nothing.
4. Try a fix at the paused prompt before you write it into a file.
5. After you write a keyword into `resources/`, check it on its own in `uv run robotcode repl --plain`: import the resource, open the page with the keywords of `resources/shop.resource`, run the keyword there, and end piped input with `.exit`.
6. Repair a test only so that it verifies what its criterion says, with locators from the stable contract, in `resources/`. Never change an expected value, an assertion or a tag so that a test passes. Never edit `resources/legacy.resource`, and never apply a preset or reset the shop. When the shop contradicts its specification, leave the test failing and report the defect with your evidence.
7. Run the test again after a change: `uv run robotcode robot -t "<test>"`.

With the shared instance, put `-p shared` before `robot`, `robot-debug` and `repl`, as in `uv run robotcode -p shared robot-debug ...`.

End with a report:
- the cause: a test to repair, or a defect of the shop;
- the evidence: what the paused page showed, next to what the criterion says;
- the change as a diff, from `git diff -- tests resources`, or "none";
- the test's result after your last run.
```

`.claude/agents/analyzer.md`, from the brief of step 4:

```markdown
---
name: analyzer
description: "Checks Robot Framework tests and resources without running them, with RobotCode's analyze code and Robocop, sorts every finding into fix, keep or false positive, and changes files only through Robocop's fixes and formatters. It returns the diff first and writes only when called again with the person's agreement. Use it to review files, or to apply a Robocop formatter or fix such as ReplaceWithVAR. Not for debugging a failing test, writing tests, or a change Robocop cannot make."
tools: Read, Grep, Glob, Bash
---

You check Robot Framework tests and resources in this repository without running them, and sort what you find. You have no tool to edit a file, and you never write one by other means: a file changes only through Robocop, after the person has agreed to the diff.

How you work:
1. Read `docs/robotcode.md`, its *Analyze* section and its *Traps*, and `docs/conventions.md`.
2. Run both checks on the paths you are given: `uv run robotcode analyze code <paths>` and `uv run robocop check <paths>`.
3. Sort every finding into fix, keep or false positive, each with its reason. Before you call a finding a false positive, read the line it points to.
4. Change files only through Robocop:
   - a formatter: `uv run robocop format --select <formatter> <paths>`, such as `ReplaceWithVAR` for the old variable syntax;
   - a rule's fix: `uv run robocop check --fix --select <rule> <paths>`. Repeat `--select` for each rule: a comma-separated list matches no rule.
   - Add `--exclude resources/legacy.resource` to every command that may write: never change that file.
   - Run each first without writing: `format` with `--diff --no-overwrite`, `check` with `--diff`. Put the diff in your report and stop there. You cannot ask the person yourself: write only when the request says they agreed to that diff, and then run the same command without the diff options.
   - Never edit a file by hand, nor through a shell command such as `sed`, a redirect or a script. Report what Robocop cannot change as a finding, with the change it needs, and leave the file as it is.
5. Right before you write, run `uv run robotcode robot --exclude broken` and note its result: that is the run before.
6. After a change, run `uv run robocop check` on the same paths again, then `uv run robotcode robot --exclude broken`. Compare the result with the run before, and name every test whose result differs.

Never apply a preset or reset the shop. With the shared instance, put `-p shared` before `robot`, as in `uv run robotcode -p shared robot --exclude broken`.

End with a report:
- the findings: file and line, the rule or error, the verdict (fix, keep or false positive) and its reason;
- what changed: the Robocop command and its diff, or "none", and the changes left as findings because Robocop cannot make them;
- the suite's result after the change, next to the run before, or "not run" when nothing changed.
```

The agent added rules of its own, from `docs/conventions.md`: neither subagent may change
`resources/legacy.resource`, which the conventions keep on purpose, and neither may apply a preset or reset the shop. `bonus/bonus-3-subagents/`
holds both subagents for each agent: `claude-code/` as rehearsed, and `codex/` and `copilot/` with the same
instructions in each agent's format, as `agents/` has them. Those two were not rehearsed.

What the debugger found under `drift_and_bug`, one test per call:

| Test | Cause | Change | Result |
|---|---|---|---|
| WEB-002_AC-1 Card Prices Are The Product Prices | the grid's class drifted. Behind it, a defect: four cards show 1.15 times the product's price | a new keyword, `Get Grid Card Prices`, by each card's visible price | fails on the defect: `$90.85 != $79.00` |
| WEB-002_AC-7 Audio Filter Shows Only Audio | the grid's class drifted | a new keyword, `Get Grid Card Elements` | passes |
| WEB-006_AC-1 Order Total Adds Up | the total's `data-test` hook drifted. Behind it, a defect: the total leaves out the tax | a new keyword, `Get Summary Total`, by the label with the word "Total" | fails on the defect: `249.99 != 267.49` |
| WEB-006_AC-7 Successful Order | the form fields' ids drifted | the test calls the existing `Fill Checkout Form`, which finds the fields by their labels | passes |

It stopped each test at its failure with `robot-debug`, 11 rounds in all, piped: Claude Code's commands run to
completion. After it wrote a keyword, it checked the keyword on its own in the REPL, three times, for example
`Get Grid Card Elements` on the catalogue: 12 cards, then 2 with the Audio filter, both `audio`. Under `clean`, all
four tests pass: the two that stay red under `drift_and_bug` fail on the shop, not on the test.

The analyzer reported 23 findings in step 8, and changed nothing: 18 to fix (six `Create List` or
`Create Dictionary`, four imports out of order, eight keywords without documentation), 4 to keep (a deliberate
indent, and documentation the names make unnecessary), and one false positive, `${HEADLESS}`. In step 9 it showed
the diff of Robocop's `ReplaceWithVAR` formatter, wrote it after the yes, and ran the suite before and after: 11
passed both times. The conversion, from `suite.patch`:

```diff
--- resources/api.resource
-    &{headers}=    Create Dictionary
+    VAR    &{headers}=    &{EMPTY}
--- resources/catalogue.resource
-    @{texts}=    Create List
+    VAR    @{texts}=    @{EMPTY}
-    @{prices}=    Create List
+    VAR    @{prices}=    @{EMPTY}
--- resources/checkout.resource
-    @{texts}=    Create List
+    VAR    @{texts}=    @{EMPTY}
-    ${message}=    Catenate    @{texts}
+    VAR    ${message}=    @{texts}    separator=${SPACE}
--- resources/shop.resource
-        &{headers}=    Create Dictionary    X-Workshop-Space=${SHOP_SPACE}
+        VAR    &{headers}=    X-Workshop-Space=${SHOP_SPACE}
--- tests/ui/checkout.robot
-    &{before}=    Create Dictionary
+    VAR    &{before}=    &{EMPTY}
```

The `Catenate` has no Robocop rule of its own: the formatter converts it along with the others. In step 10, asked
for a `[Documentation]` line, the analyzer left the file unchanged and wrote the line as a finding: no Robocop fix
writes documentation, and the `GenerateDocumentation` formatter would have put a placeholder into four keywords.

## Why it is a good result

- **No expected value moved.** The patch changes which keyword four tests call, and adds three keywords on the
  stable contract. Every assertion, expected value and tag is as `main` ships it. Two tests stay red, and the
  reports say why: the price the page showed against the price the API and the specification give.
- **Each tool did its own job.** The debugger tried a fix at the paused prompt in the test's own context, the REPL
  proved the keyword in the file on its own, and only then did the test run again.
- **The main conversation got reports, not sessions.** The four debug sessions stayed in the debugger's context;
  the main agent saw four reports and wrote one summary. In Lab 4, the session itself fills the conversation.
- **The analyzer changed files only through Robocop,** showed the diff first, and wrote only after the yes. It ran
  the suite before and after, and compared the two runs.
- **The descriptions say when to use each subagent, and when not:** the debugger's says "one call per test and never
  two at once", and the main agent handed over the four tests one at a time.

## What to debrief

- **Repair or report.** For two of the four tests, repairing the locator was half the answer: the test then failed
  on a real defect. A debugger allowed to edit could have made them green by changing the expected value. The brief
  forbids it, and the report is what you file, as in Lab 7.
- **A tool needs a job in the brief.** The first rehearsal's brief offered the REPL only as an alternative to the
  paused prompt, and the debugger never used it: the paused prompt was enough. The brief now gives each tool its own
  job, and the second rehearsal used both.
- **What a finding is measured against.** The rehearsal's branch held the day's repairs in its last commit, so the
  analyzer read step 1's restore as new changes. Among "problems neither tool reports", it listed the two tests
  broken on purpose and the inline locator, as if the participant had just broken them. Before you act on a
  finding, ask what it was compared with.
- **A tool limit is not a sandbox.** The analyzer has no edit tool, and its own instructions add "nor with a shell
  command such as `sed`, a redirect or a script". Its shell could still write a file. The guardrail that holds is a hook, as in
  Lab 7. Codex limits a subagent only through its sandbox, so there the rule lives in the instructions alone.
- **Claude Code guards `.claude/`.** Writing a subagent needs your permission, even when edits are otherwise allowed.
  A session without a person cannot give it: the rehearsal allowed the write the agent asked for, unchanged, and
  the transcript says so.
- **One step up is still structure.** `Get Summary Total` finds the label by its visible text, then its row with
  `xpath=..`. The text is stable contract; the step to the parent is not. Is that good enough, or should the row
  have an accessible name of its own?
- **What they left alone.** `Get Card Category` reads the `data-category` attribute, which the conventions call an
  implementation detail. Both rehearsals left it, because the visible badge reads "Audio" and the comparison would
  change. A subagent that stops there, and says so, is doing its job.
- **Robocop's `--select` takes one rule each.** A comma-separated list matches no rule, and Robocop reports no issues.

## Compare yours

The reference is on the `solutions` branch, which your fork does not have. From your workshop clone, on your
`bonus-3` branch:

```bash
git fetch upstream solutions
mkdir -p ../reference && git archive upstream/solutions bonus/bonus-3-subagents | tar -x -C ../reference
diff ../reference/bonus/bonus-3-subagents/claude-code/debugger.md .claude/agents/debugger.md
git diff upstream/main -- tests resources | diff ../reference/bonus/bonus-3-subagents/suite.patch -
```

With Codex, compare `codex/debugger.toml` with `.codex/agents/debugger.toml`; with GitHub Copilot,
`copilot/debugger.agent.md` with `.github/agents/debugger.agent.md`. No `upstream` remote yet?
[Add it first](README.md#compare-your-files-with-the-reference).

## Check the reference

With your own changes committed or stashed, apply the patch to a branch of `main` and run the suite in both layouts:

```bash
git switch -c check-bonus-3 upstream/main
git apply ../reference/bonus/bonus-3-subagents/suite.patch
uv run --no-sync python -m shop reset
uv run robotcode robot                              # only the two tests broken on purpose fail
uv run --no-sync python -m shop preset drift_and_bug
uv run robotcode robot --exclude broken             # only the two defects fail
uv run --no-sync python -m shop reset
uv run robocop check --select replace-set-variable-with-var --select replace-create-with-var tests resources
```
