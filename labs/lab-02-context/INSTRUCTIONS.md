# Lab 2 - Context

Write the [context file](../../GLOSSARY.md#context-file) every agent reads, `AGENTS.md`, and see what it changes. You
need nothing but a text editor for the writing. The agent comes in before and after.

| | |
|---|---|
| Module | 2 - Context Engineering |
| Time | 25 minutes |
| Shop preset | `clean` |
| You need | Lab 0 done: the suite runs, and your agent starts in the repository |
| You start from | `main`, where `AGENTS.md` is deliberately short |

## Steps

1. **Record the "before".** Give your agent this prompt, and let it finish:

   > Write a Robot Framework test for criterion WEB-002_AC-5 of this repository and save it as
   > results/lab-02/before.robot. Do not run it, and do not change any other file.

   `results/` is ignored by git, so nothing here ends up in a commit.

2. **Read what you have.** Open `AGENTS.md`: under 30 lines, and nothing about how tests are written here. Then
   skim `docs/conventions.md` and the folder `openspec/specs/shop/`. These are what an agent should know about,
   and what it did not know in step 1.

3. **Write your `AGENTS.md`** with the checklist below. Add a short section for each point. Keep every line
   something an agent needs and cannot find out quickly on its own.

   **Put in:**
   - *Environment*: how to install, how to run the suite and one test, and that `-p shared` selects the shared
     instance;
   - *System under test*: what the shop is, where it runs, and that `uv run --no-sync python -m shop status` shows
     its state;
   - *Conventions*: one line that points to `docs/conventions.md`. Link it, don't copy it;
   - *Specifications*: that `openspec/specs/shop/` describes what the shop does, per criterion, and is the reference
     for expected behaviour;
   - *Boundaries*: what the agent must never do. For example: edit `resources/legacy.resource`, apply presets
     or reset the shop from a test, read or print `.env`, or install tools the repository does not pin.

   **Leave out:**
   - secrets, keys, tokens, or anything from `.env`;
   - what the agent can discover itself, such as lists of files, tests or keywords;
   - prose: history, motivation, long explanations.

4. **Move one section into its own file.** Pick the section that grew longest, for example *Environment*. Move it to
   `docs/agent-environment.md`, and leave one line in `AGENTS.md` that says when to read it:

   ```markdown
   Before installing anything or running tests, read docs/agent-environment.md.
   ```

   That is modular context: a short root file, and focused files the agent loads when a task needs them.

5. **Check that your agent loads it.** Start a new session, so that it reads the file fresh, then:

   | Claude Code | Codex | GitHub Copilot |
   |---|---|---|
   | `/memory` lists `AGENTS.md` through `CLAUDE.md` | reads `AGENTS.md` on start | `copilot instruction list` shows `AGENTS.md` |

   `CLAUDE.md` contains only `@AGENTS.md`. Keep it that way: one file, referenced by the others.

6. **Record the "after".** In the new session, the same prompt with a different file name:

   > Write a Robot Framework test for criterion WEB-002_AC-5 of this repository and save it as
   > results/lab-02/after.robot. Do not run it, and do not change any other file.

7. **Compare** the two files side by side, or with `diff results/lab-02/before.robot results/lab-02/after.robot`.
   Look for: the test's name, where its locators live, which keywords it uses, and whether the expected text
   matches `openspec/specs/shop/catalogue`. Note one difference your `AGENTS.md` made, and one it did not. You will
   compare notes in the debrief.

## Stretch

Give the API tests their own context. Create `tests/api/AGENTS.md` with what only API tests need: they use
`resources/api.resource` and its session `shop`, and they are tagged `api`. Then ask your agent to add an API test
for the health endpoint's version field, and see whether it followed the nested file. Delete the test afterwards.

## If your agent fails

Steps 2 to 4 need only an editor. For the before and after, follow
[the recorded walkthrough of this lab](../../transcripts/lab-02-context.md).
