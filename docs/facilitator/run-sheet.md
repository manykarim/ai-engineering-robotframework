# Run sheet

*Facilitator material.* The day, module by module: what the shop must be in, what you show, what participants do,
and what to do when it goes wrong or runs late. Print it. Times are CET, as in the master preparation document.

## The day

| Time | Module | Shop preset | You demonstrate | Participants do | Fallback | When it runs late |
|---|---|---|---|---|---|---|
| 09:00-09:30 | 0 - Arrival & Environment Check (30 min) | `clean` | Nothing yet: welcome, the poll *"what should an agent take off your plate first?"* | [Lab 0](../../labs/lab-00-arrival/INSTRUCTIONS.md) | Co-host breakout with the [triage playbook](triage-playbook.md); shared instance; pairing | Stragglers continue in the breakout during Module 1 |
| 09:30-09:55 | 1 - Cold Open, the Agentic Shift & the Maturity Ladder (25 min) | `clean` on your machine; the cold open switches it | The [cold open](cold-open.md), then the ladder and the standing rule | Listen; glossary at hand | The recorded cold open, `transcripts/cold-open.md` | Shorten the talk, never the cold open |
| 09:55-10:45 | 2 - Context Engineering (50 min: 15 / 25 / 10) | `clean` | An `AGENTS.md` written live; the same prompt before and after | [Lab 2](../../labs/lab-02-context/INSTRUCTIONS.md) | Steps 2-4 need only an editor; transcript | Debrief down to 5 minutes |
| 10:45-11:00 | Break | | | | | |
| 11:00-11:50 | 3 - Agent Skills (50 min: 15 / 25 / 10) | `clean` | A `SKILL.md` taken apart; trigger and no-trigger | [Lab 3](../../labs/lab-03-skills/INSTRUCTIONS.md) | Transcript | Skip the stretch; debrief 5 minutes |
| 11:50-12:35 | 4 - RobotCode for Agents (45 min: 15 / 25 / 5) | `clean` | `discover`, `libdoc`, `robot-debug` on a test you break live, the REPL misfire | [Lab 4](../../labs/lab-04-robotcode/INSTRUCTIONS.md) | Steps 3-4 run by hand; transcript | Skip the REPL step (6) |
| 12:35-13:20 | Lunch | | | | | |
| 13:20-14:05 | 5 - Natural Prompt Automation & Debugging (45 min: 10 / 30 / 5) | `clean` | `/opsx:propose` on a slice outside the lab (WEB-002_AC-8, the price range) | [Lab 5](../../labs/lab-05-prompt-to-green/INSTRUCTIONS.md), pair review in breakouts | Transcript; the pair review works on its proposal | Skip the archive step (7) |
| 14:05-14:50 | 6 - Robot Framework MCP (45 min: 15 / 25 / 5) | `clean` | Your Module 5 demo test rebuilt stepwise | [Lab 6](../../labs/lab-06-mcp/INSTRUCTIONS.md) | Transcript | Skip the cost step (6) |
| 14:50-15:05 | Break | | | | | |
| 15:05-15:45 | 7 - Hooks, Subagents & the CLI Toolbelt (40 min: 15 / 20 / 5) | `buggy`, applied by each participant in step 4 | Hooks firing; `gh issue create` from a real run; 10 minutes on prompt injection | [Lab 7](../../labs/lab-07-hooks-toolbelt/INSTRUCTIONS.md) | Steps 3-5, 7-8 need no agent; transcript | Cut stretch B (Jira) |
| 15:45-16:15 | 8 - Self-Healing Tests (30 min: 15 / 12 / 3) | `drift_and_bug`, applied by each participant in step 1 | A live healing run, and its report triaged ([answers](suite-outcomes.md#module-8-the-triage-answers)) | [Lab 8](../../labs/lab-08-healing/INSTRUCTIONS.md) | The recorded report in `transcripts/lab-08-healing/` | **First cut:** demo only, skip the lab |
| 16:15-16:50 | 9 - CI & Toolchain Integration (35 min: 15 / 15 / 5) | `clean` (CI starts its own shop) | A pushed break explained in a pull request on your fork | [Lab 9](../../labs/lab-09-ci/INSTRUCTIONS.md) | Transcript | Cut the stretch (heal suggestions) |
| 16:50-17:00 | 10 - Wrap-Up, Roadmap & Q&A (10 min) | - | The ladder once more; the Monday plan: `AGENTS.md`, then the RobotCode plugin and RF Agent Skills, then one CI triage step | Questions | - | - |

Buffer lives in debriefs and stretch goals, never in lab time.

## Cuts

When the day runs late, cut in this order, and only as far as needed:
1. the Module 8 lab: show Module 8 as a demo;
2. the Module 9 stretch goal;
3. Module 7's stretch B, the Jira skill.

**A beginner-heavy room** (you know at registration): run Module 8 as a demo only from the start, and give its 12
lab minutes to Module 2.

## Presets for the room

Every participant switches their own shop, local or in their own space, with the shop helper. Say the command out
loud and put it in the chat at the start of Modules 7 and 8, and the reset at their end:

```bash
uv run --no-sync python -m shop preset buggy          # Module 7, step 4
uv run --no-sync python -m shop preset drift_and_bug  # Module 8, step 1
uv run --no-sync python -m shop reset                 # the end of Modules 7 and 8
uv run --no-sync python -m shop status                # what holds right now
```

Presets compose: `buggy` keeps a drifted layout if one is active. The reset always returns to `clean`. A participant
whose suite fails more than the two `broken` tests outside Modules 7 and 8 has a preset left on: `status`, then
`reset`.

## Healing keys (Module 8)

Decide before the setup email whether this workshop hands out healing keys. Without keys, Module 8 works with the
recorded report and the agentic stretch goal, and nobody needs anything extra.

If you hand them out:
1. Create **one key per participant** at an OpenAI-compatible provider, each with a **hard spending cap** and an
   expiry at the end of the day. One healing run under `drift_and_bug` takes about 20,000 tokens; a cap for ten runs
   is plenty.
2. Send each key in a private chat message on the day. Never in a shared document, a slide or the repository.
3. Participants put `HEAL_MODEL`, `HEAL_BASE_URL` and `HEAL_API_KEY` into `.env` (`SETUP.md`, *Healing API key*).
   `setup-check` then shows *Healing endpoint* as passed.
4. Revoke all keys after the workshop.

Never one shared key for the whole room: it cannot be capped per person, and it leaks the moment someone pastes it.

## Module 5: the whiteboard

During the debrief, build the group's review checklist on the shared whiteboard. Participants leave with it. Start
from this skeleton, and let the room fill in what their pair reviews found:

| Question to ask of an agent's plan | Found in our reviews |
|---|---|
| Does it cover exactly the slice, no more? | |
| Are its specs in `suite/*`, naming each criterion? | |
| Does every test name start with its criterion? | |
| Do locators live in resources, built on the stable contract? | |
| Are quoted texts from the spec used as they are? | |
| Does every test create its own state? | |
| What could the agent not know without seeing the page? | |

The last row is the bridge to Module 6.
