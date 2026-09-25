# Lab 3 - Skills

Install ready-made Robot Framework [skills](../../GLOSSARY.md#skill), then write one of your own that enforces a
convention of this repository, and check that it loads when it should, and only then.

| | |
|---|---|
| Module | 3 - Agent Skills |
| Time | 25 minutes |
| Shop preset | `clean` |
| You need | Lab 0 done. Your `AGENTS.md` from Lab 2 helps, but this lab works without it |
| You start from | `main`, plus your work from Lab 2 if you have it |

A skill is a folder with a `SKILL.md`. The agent reads only its `description` until a task matches it; then it
loads the rest. Rule of thumb: what is *always* relevant goes into `AGENTS.md`; what is relevant for *one kind of
task* becomes a skill.

## Steps

1. **Install the Robot Framework Agent Skills** into this repository. The version is pinned in `SETUP.md`:

   | Claude Code | Codex | GitHub Copilot |
   |---|---|---|
   | `uvx rf-agentskills@0.6.0 install --agent claude-code --scope project --project . --what skills` | same, with `--agent codex` | same, with `--agent copilot` |
   | lands in `.claude/skills/` | lands in `.agents/skills/` | lands in `.claude/skills/`, which Copilot also reads |

2. **See what you got.** Start a new agent session and ask:

   > Which skills do you have for Robot Framework, and what is each one for? One line each.

3. **Rerun Lab 2's prompt**, now with the skills installed:

   > Write a Robot Framework test for criterion WEB-002_AC-5 of this repository and save it as
   > results/lab-03/with-skills.robot. Do not run it, and do not change any other file.

   Compare it with `results/lab-02/after.robot`, if you have it. Did a skill show up in the session? Did the
   keywords it chose change?

4. **Pick a convention** from `docs/conventions.md` for your own skill. A good first choice is convention 2,
   *Locators live in resources*. Any other works too.

5. **Copy the template** into your agent's skill folder, under a name for your convention, for example
   `locators-in-resources`:

   | Claude Code | Codex | GitHub Copilot |
   |---|---|---|
   | `cp -r skills/template .claude/skills/locators-in-resources` | `cp -r skills/template .agents/skills/locators-in-resources` | `cp -r skills/template .github/skills/locators-in-resources` |

   The template is a working skill for convention 1. Read it once as it is.

6. **Make it yours.** In the copied `SKILL.md`:
   - set `name` to the folder's name;
   - rewrite `description`: what the skill checks, and *when* to use it, in the words a prompt would contain;
   - replace the rule, the reason and the examples with your convention's;
   - delete the template's comment.

   Leave the script in `scripts/` alone for now; it belongs to the stretch goal.

7. **Check that it triggers.** New session, then a prompt that should load it:

   > Review tests/ui/catalogue.robot against the conventions of this repository.

   The session shows that your skill loaded:

   | Claude Code | Codex | GitHub Copilot |
   |---|---|---|
   | prints `Skill(<name>)` | reads your skill's `SKILL.md` | names the skill it invokes |

   Did the review find anything?

8. **Check that it stays quiet.** A prompt about something else:

   > What does `uv run --no-sync python -m shop reset` do? Answer in two sentences.

   Your skill must not load. If it does, your description is too broad: make it more specific and repeat steps 7
   and 8.

## Stretch

Give your skill teeth. Change `scripts/check.py` in your skill's folder so that it checks your convention instead of
convention 1. For convention 2, for example, report every argument in a test file that looks like a locator. Then tell
the agent in `SKILL.md` to run it, and repeat step 7.

If you let your agent make the change: the skill folders are agent configuration, and agents guard them. Claude Code
asks before it writes into `.claude/`, and Codex's sandbox keeps `.agents/` read-only until you approve the write.
Approve it, or edit the files yourself.

## If your agent fails

Steps 4 to 6 need only an editor. For the rest, follow
[the recorded walkthrough of this lab](../../transcripts/lab-03-skills.md).
