## Context

See proposal.md for why. The facts this design builds on:

- **The day is fixed.** It runs from 09:00 to 17:00, Modules 0 to 10, on 2026-10-07. Module 10 (10 min) closes with the "Monday plan": `AGENTS.md`, then the RobotCode plugin and the Agent Skills, then one CI triage step. `main` is not tagged yet.
- **The lab contract** lists nine lab folders. `tools/check_labs.py` ties each to a module, its timetable minutes and a preset, and rejects any other folder under `labs/`. The site's sidebar turns every folder under `labs/` into a lab category.
- **Already installed in the workshop's environment:**
  - AssertionEngine 5.0.1. `Browser/keywords/getters.py` shows how Browser uses it, for example in `get_text(selector, assertion_operator, ...)`.
  - PythonLibCore 4.6.0.
  - robotframework-heal, whose `heal/rf/listener.py` is a listener with API version 3.
  - `requests`.
- **The shop publishes `/openapi.json`:** version 0.3.0 locally, 12 paths. The public DemoShop at `https://demoshop.makrocode.de/docs` runs version `dev`.
- **Version-pinned references exist for Robot Framework 7.5:**
  - the User Guide at `https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html`, with anchors `#creating-test-libraries`, `#library-scope`, `#hybrid-library-api`, `#dynamic-library-api`, `#libdoc`, `#listener-interface`, `#listener-version-3` and `#listener-examples`;
  - the Robot API at `https://robot-framework.readthedocs.io/en/v7.5/`. `ListenerV3` is documented on the `robot.api` page (`#robot.api.interfaces.ListenerV3`), not on a page of its own.
- **External references:**
  - GitHub's REST docs for issues are fetchable, and so is GitHub's OpenAPI description, about 10 MB.
  - TestRail's API manual answers automated requests with 403.
- **`openspec init --tools claude`** (or `codex`, `github-copilot`) sets OpenSpec up without prompts.

## Goals / Non-Goals

**Goals:**
- A participant who finished the day can build a small, packaged Robot Framework library and a listener with their agent, from a context they wrote themselves, without help.
- Every reference the labs name opens at the version in use, and needs no account beyond the workshop's own.
- Nothing about the day changes except one sentence in Module 10.

**Non-Goals:**
- Publishing to PyPI. `uv build` is the end point.
- A TestRail lab: it serves only as the example of a reference behind a bot wall.
- A second agent's rehearsal of the bonus labs.
- Creating real GitHub issues during the rehearsal (D6).

## Decisions

### D1. Folders, names and the contract

| | Bonus 1 | Bonus 2 |
|---|---|---|
| lab folder | `labs/bonus-1-library/` | `labs/bonus-2-tool/` |
| header *Module* | `Bonus 1 - Building a library with an agent` | `Bonus 2 - Building a tool with an agent` |
| header *Time* | `about 120 minutes, self-paced` | `about 60 minutes, self-paced` |
| preset | `clean` | `clean` |
| the participant's project | `../demoshop-library/` | `../robotframework-github-reporter/` |

- `tools/check_labs.py` gets a second table, `BONUS`. Its checks are those of `LABS`, except that *Module* starts with `Bonus <n> ` and *Time* holds `<minutes> minutes` and `self-paced`. Every other check applies unchanged: sections, links, giveaways, transcript and reference links on the branch.
- The site's sidebar keeps *Labs* for `lab-*` and adds a *Bonus* category for `bonus-*`, built the same way.
- `labs/README.md` gets a short *Bonus labs* table after the day's table.

*Alternative:* numbering them as Labs 11 and 12. Rejected: they are not modules, and a lab number implies a slot on the day.

### D2. The chapter: one guide, two labs

`docs/building-with-agents.md` holds the method, so that both labs stay short and point to it.

1. **Start outside every other project.**
   - Claude Code loads `CLAUDE.md` files from the folders above the working directory.
   - Codex loads `AGENTS.md` from the git root down.
   - OpenSpec uses the nearest `openspec/`.

   A project inside the workshop clone would inherit the clone's context. The guide shows how to check what loaded.
2. **The five kinds of context** are headings of the new project's `AGENTS.md`, with a skeleton:
   - *Toolstack*: `uv init --lib`, `uv add`, `uv run pytest`, `uv build`, and the dependency policy;
   - *References*: links to the pinned versions, and saved files;
   - *Concepts*: what the code must follow;
   - *Examples*: what to imitate, saved as files where possible;
   - *Specification*: OpenSpec, and the current change.
3. **OpenSpec from zero:** `openspec init --tools <agent>`, then the same five points, short, as `context` in `openspec/config.yaml`.
4. **The reference map** for Robot Framework 7.5: which User Guide anchor and which Robot API page or entry fits a library, a listener, a pre-run modifier, a result tool, and a parser for test data.
5. **Saving references:**
   - export an OpenAPI description, for example `curl …/openapi.json -o references/…`;
   - extract the part you need from a large one, such as GitHub's issue paths from its 10 MB description;
   - save libdoc output of a library to imitate (`robotcode libdoc Browser show "Get Text"`);
   - when a manual blocks automated access, as TestRail's does, export or copy it by hand.
6. **One slice at a time:** propose, review, apply, then look at the result before the next slice.

### D3. Bonus 1: a DemoShop library

**The slice the lab asks for:** session, catalogue and cart.

| Keyword | Notes |
|---|---|
| `Get Product Count` | takes an optional assertion |
| `Get Product Price` | takes an `id`, and an optional assertion |
| `Add Product To Cart` | takes an `id` and an optional `quantity` |
| `Get Cart Item Count` | takes an optional assertion |
| `Get Cart Total` | takes an optional assertion |

- The library takes `url` and an optional `space` on import, and sends the space as `X-Workshop-Space`. It keeps the cart's session for its lifetime.
- The `Get` keywords take `assertion_operator`, `assertion_expected` and `message` as AssertionEngine defines them: `Get Product Price    1    ==    249.99`.

**What the participant puts into the project before the first prompt:**
- the pinned shop's description: `curl http://localhost:9090/openapi.json -o references/demoshop-openapi.json`;
- Browser's `Get Text` and `Get Element Count` as libdoc Markdown, from the workshop clone: `uv run robotcode libdoc Browser show ...`. These are the keywords to imitate;
- AssertionEngine's README, saved, as the concept;
- the guide's `AGENTS.md` skeleton, filled in. Its toolstack names `uv`, Python 3.12, `robotframework==7.5`, `robotframework-assertion-engine` and `robotframework-pythonlibcore`, pinned, plus `pytest` for unit tests and Robot tests in `atest/` against the local shop.

**Steps:**
1. `uv init --lib`
2. `uv add` the dependencies.
3. Write the references and `AGENTS.md`.
4. `openspec init --tools <agent>`, with the context in `config.yaml`.
5. Propose, then a pair or self review against a short checklist, then apply.
6. Run `uv run pytest`, then `uv run robot atest`, then `uv run python -m robot.libdoc …`, then `uv build`.
7. Compare with `resources/api.resource`: what the library gives that user keywords don't. That's assertion operators, typed arguments, a session, packaging and generated documentation. And the reverse: more code to maintain.

**Stretch goal:** the next slice, checkout and order confirmation.

### D4. Bonus 2: a listener that reports to GitHub

**The slice:** a `ListenerV3` class, `GitHubIssues`, in package `robotframework_github_reporter`.
- **Arguments:** `repo` (`owner/name`), `dry_run` (true by default) and `label` (`robot-failure`).
- **On a failed test,** in `end_test`, it opens an issue titled `Failing test: <long name>`, with the message, `source:lineno` and, under GitHub Actions, the run's URL. If an open issue with that title and label exists, it adds a comment instead.
- **In a dry run,** it writes each request it would send to the console and to `<output dir>/github-requests.json`, and sends nothing.
- **Live,** it reads the token from `GITHUB_TOKEN` or `GH_TOKEN`; locally `GH_TOKEN=$(gh auth token)`. Without a token it falls back to a dry run with a warning.
- **It never fails or alters a test.** Every API error becomes a warning.
- **It needs no dependencies at run time beyond Robot Framework:** HTTP goes through the standard library (`urllib.request`). That is the dependency policy the lab puts into `AGENTS.md`. It also means the listener runs inside any project's environment with `--pythonpath`.

**References saved into the project:**
- the issue and issue-comment paths, extracted from GitHub's OpenAPI description by a short Python command the lab gives;
- links to the User Guide's `#listener-interface`, `#listener-version-3` and `#listener-examples`, and to the `robot.api` page's `ListenerV3` entry, all at 7.5;
- as the example, the workshop environment's `heal/rf/listener.py`, copied in.

**Checks:**
- unit tests with `urllib.request.urlopen` replaced, covering a new issue, a comment on an existing one, a dry run, no token, and an API error;
- Robot tests in `atest/` that run a failing suite with the listener in a dry run, and compare `github-requests.json`.

**Then on the workshop's own suite:**
```
uv run robotcode robot --pythonpath ../robotframework-github-reporter/src \
  --listener robotframework_github_reporter.GitHubIssues:repo=<you>/ai-engineering-robotframework
```
In a dry run this lists the two tests broken on purpose.

**Stretch goal:** run it live against your fork, then close the issues it opened.

### D5. Where the results live

- **On the `solutions` branch:** `bonus/bonus-1-library/` and `bonus/bonus-2-tool/` hold the rehearsals' projects, without `.venv`, `dist` or `results`. Each is a commit starting with the bonus folder name, on top of the existing commits.
- **Their transcripts and reference pages** follow in a `reference:` commit, as for every lab.
- **`main` gets no part of them.** The all-of-`main` scan of `tools/check_labs.py` covers the new text too.
- **Order:** these commits are appended to `origin/solutions` without a force-push before the `main` pull request, because `check_labs.py` checks the bonus labs' links on the branch. The rebase after the merge works as before.

### D6. Rehearsal today

- **The runs:** both labs run with Claude Code headless, through the rehearsal driver, in fresh sibling folders. The lab's own commands and prompts are used. Where a participant writes a file by hand (`AGENTS.md`, `config.yaml`), the agent drafts it from the lab's checklist, and the transcript says so, as in Lab 2.
- **The checks:** each rehearsal ends with D3's or D4's checks passing. The project is then copied to the branch.
- **Bonus 2's live path** is covered by unit tests, not by real issues: the workshop's repository is no place for test issues, and no throwaway repository is set up. A maintainer can run the stretch goal against a fork later.
- **The record:** the rehearsal record gets a *Bonus labs* section: result, duration, tokens, and what changed.

### D7. The day: one sentence

- **The curriculum:** Module 10's Monday plan gains a fourth step: *(4) when you build your own library or tool: the bonus chapters*.
- **The run sheet's Module 10 row** says the same.
- **Nothing else** of the day changes.

### D8. The glossary

Three short entries, in a new section *Building libraries and tools* before *This repository*:
- *Assertion engine*: the operators of Browser's `Get` keywords, as a library others can use;
- *PythonLibCore*: the structure Browser and others build libraries on;
- *Listener*: code Robot Framework calls during a run.

The glossary stays within about ten minutes.

## Risks / Trade-offs

- **[Changes to `main` the day before the workshop]**
  - All are additive: new folders and a new page, a sidebar group, a table, one sentence, and checks that accept the new folders.
  - The pull request's site build and `tools/check_labs.py` must pass, and the day's labs are unchanged.
  - Tag `main` after the merge.
- **[The rehearsal takes longer than the day allows]** → Bonus 2 is smaller and goes first. If Bonus 1 does not finish, it ships in a second pull request, and the Module 10 sentence names what exists.
- **[The agent cannot fetch a page during the rehearsal]** → Every reference the labs need is saved by a lab command before the agent starts. That is the method being taught.
- **[GitHub's API changes, or rate-limits unauthenticated calls]** → The dry run makes no call. Live calls are authenticated, and the issue paths are saved from GitHub's own description.
- **[The public DemoShop drifts from the pinned 0.3.0]** → The lab saves the local, pinned `/openapi.json`. The public docs are for reading only.
- **[Participants' parent folders hold their own `CLAUDE.md` or `AGENTS.md`]** → The guide's first step checks what the agent loaded, and says to move the project elsewhere if anything foreign appears.

## Migration Plan

1. **A branch from `main`:** the contract and the sidebar, the guide, the glossary, Module 10, and both labs' text.
2. **Rehearse Bonus 2, then Bonus 1,** from that text, and fix the text as the rehearsals show.
3. **Append to `solutions`:** the reference projects, then the transcripts and reference pages. The push redeploys the site.
4. **Open the `main` pull request.** `check_labs.py` and the site build pass against the branch.
5. **After the merge:** rebase `solutions` onto `main`, archive the change, and tag `main`.

**Rollback:** revert the pull request. The branch commits can stay, since nothing links to them.
