# Agentic Engineering with Robot Framework

## Master Preparation Document

*World Wide Workshop Wednesday · Robot Framework Foundation*
*Full-day online workshop · 8 hours incl. breaks · Level: Intermediate*

This is the single source of truth for preparing and running the workshop: final timetable, curriculum, complete tool stack, the GitHub participation repository design, onboarding flow, and facilitator checklists. Companion documents: the proposal versions and the participant glossary.

---

# 1. Workshop Summary

**Title:** Agentic Engineering with Robot Framework: From a Markdown File to a Self-Healing Pipeline

**One-liner:** A full-day climb up the agentic maturity ladder — **Context → Skills → Tooling → Live Access → Orchestration** — where every rung works on its own and every participant leaves with a working, layered setup.

**Audience:** Test engineers and QA professionals with working Robot Framework knowledge. No prior agent experience required.

**Format:** Online, hands-on. Rhythm: short demo → guided lab → debrief. Labs outnumber lectures roughly 2:1.

**Standing rule of the day:** agents draft, humans decide.

---

# 2. Final Timetable

| Time (CET) | Module | Tier | Duration |
|---|---|---|---|
| 09:00 – 09:30 | 0 — Arrival & Environment Check | — | 30 min |
| 09:30 – 09:55 | 1 — Cold Open, the Agentic Shift & the Maturity Ladder | — | 25 min |
| 09:55 – 10:45 | 2 — Context Engineering: AGENTS.md, CLAUDE.md & Modular Markdown | Context | 50 min |
| 10:45 – 11:00 | ☕ Break | | 15 min |
| 11:00 – 11:50 | 3 — Agent Skills: Concept, Anatomy & Your First Custom Skill | Skills | 50 min |
| 11:50 – 12:35 | 4 — RobotCode for Agents: Discovery, Libdoc, Debugging & REPL | Tooling | 45 min |
| 12:35 – 13:20 | 🍽️ Lunch | | 45 min |
| 13:20 – 14:05 | 5 — Natural Prompt Automation & Debugging | Tiers 1–3 | 45 min |
| 14:05 – 14:50 | 6 — Robot Framework MCP: The Live-Access Upgrade | Live access | 45 min |
| 14:50 – 15:05 | ☕ Break | | 15 min |
| 15:05 – 15:45 | 7 — Hooks, Subagents & the CLI Toolbelt (gh, az, Jira skill) | Orchestration | 40 min |
| 15:45 – 16:15 | 8 — Self-Healing Tests | Orchestration | 30 min |
| 16:15 – 16:50 | 9 — CI & Toolchain Integration | Scale | 35 min |
| 16:50 – 17:00 | 10 — Wrap-Up, Roadmap & Q&A | — | 10 min |

**Engagement design baked into the order:**

- **Cold open (09:30):** the finished setup live — one prompt becomes a green test, the UI-drift script breaks the suite, it heals itself. Destination first, theory second.
- **First win before 10:30:** the `AGENTS.md` lab needs nothing but a text editor — everyone succeeds early.
- **Payoff lab in the post-lunch dip (13:20):** active typing plus a pair-review breakout beats introducing a new protocol at the day's lowest-energy hour.
- **MCP as a felt upgrade (14:05):** participants hit the ceiling of Tiers 1–3 in their own lab first, then get the tool that removes it.
- **Self-healing at 15:45:** the one demo that survives the late-afternoon slump.
- Buffer lives in debriefs and stretch goals — never in lab time.

---

# 3. Curriculum

## Module 0 — Arrival & Environment Check (30 min)

Everyone runs `setup-check`, clones the workshop repo, starts the demo shop, runs the suite once, watches some tests fail on purpose. Support co-host triages stragglers in a breakout. Poll: *what should an agent take off your plate first?*
**Outcome:** running environments, shared picture of the demo project.

## Module 1 — Cold Open, the Agentic Shift & the Maturity Ladder (25 min)

5-minute cold open (see above), then the essentials: what agentic engineering is and isn't; why agents fail on RF projects out of the box (suites, tags, and keywords resolve at *runtime* — file-reading gets half the story); the five-tier ladder; the standing rule.
**Outcome:** shared vocabulary and the map for the day. Pair with the glossary handout.

## Module 2 — Context Engineering (50 min · Demo 15 / Lab 25 / Debrief 10)

`AGENTS.md` as the cross-agent standard, `CLAUDE.md` and Copilot instructions as equivalents (one file, referenced by the others). What belongs in (environment, SUT, conventions, boundaries) and the harder discipline of what stays out (secrets, discoverables, prose). Modular context: a root file linking focused sub-files, loaded on demand; nested files for sub-projects. Context economics in one slide: minimal human-written context helps, bloated or auto-generated context measurably hurts.
**Lab:** write the demo project's `AGENTS.md` from a checklist; split one section into a referenced sub-file; before/after the same generation prompt. Stretch: nested `AGENTS.md` for the API subfolder.
**Outcome:** everyone can improve their real project tomorrow with a text editor.

## Module 3 — Agent Skills (50 min · 15/25/10)

`SKILL.md` anatomy: triggering description, instructions, optional bundled scripts. Decision rule: always relevant → `AGENTS.md`; task-class relevant → skill. The Robot Framework Agent Skills installed and inspected. Distribution via marketplaces and repos. Trigger discipline: skills load on relevance matching — vague prompts don't trigger them.
**Lab:** install RF Agent Skills, diff generation output; author a mini-skill enforcing one demo-project convention; verify trigger/no-trigger. Stretch: bundle a helper script.
**Outcome:** participants read, apply, and author skills — and know when a skill beats a context file.

## Module 4 — RobotCode for Agents (45 min · 15/25/5)

The chat plugin teaches agents the `robotcode` CLI habits: **`discover`, never grep** (runtime resolution); **`libdoc` before generic knowledge** (installed versions, not training memories); **`robot-debug` for failing tests** (live breakpoint, real variables — not blind re-runs); **REPL only when no test exists yet** (the plugin's most common misfire — we trigger it on purpose); **`results`, not raw output.xml**. One `AGENTS.md` line ties Tier 1 to Tier 3.
**Lab:** install the plugin; discovery question; libdoc lookup; step-debug a pre-broken test; REPL-explore a new flow with visible browser. Stretch: results query by tag.
**Outcome:** an agent that behaves like an RF engineer who knows your setup — files and CLI only, no server required.

## Module 5 — Natural Prompt Automation & Debugging (45 min · 10/30/5)

The payoff, on Tiers 1–3 alone. User story → convention-following green suite; review discipline; conversational debugging end-to-end at a real breakpoint.
**Lab:** one of three user stories to green; pair-review in breakouts (like a junior engineer's PR); debug one pre-broken test purely through conversation. Stretch: API-level test via Requests keywords.
**Debrief:** group review checklist on a whiteboard — and note what was missing: the agent couldn't peek at the live page mid-draft. Hold that thought.
**Outcome:** a repeatable prompt → review → refine loop, plus a felt sense of the Tier 1–3 ceiling.

## Module 6 — Robot Framework MCP: The Live-Access Upgrade (45 min · 15/25/5)

The before/after on Module 5's own task: stepwise execution — run a step, inspect the live page, decide the next. Honest trade-off: MCP tools occupy context; CLIs and skills are cheaper — use MCP where live, stateful interaction earns its keep. Ecosystem note: tier boundaries are still moving; the tiers are complementary and skills transfer regardless of transport.
**Lab:** connect the RF MCP server; rebuild the Module 5 test stepwise; compare both versions — where did live access change the result? Stretch: change the page in the browser mid-session and ask the agent again.
**Outcome:** grounded live development and the judgement of when MCP is worth the setup.

## Module 7 — Hooks, Subagents & the CLI Toolbelt (40 min · 15/20/5)

Hooks as always-on guardrails (auto-run affected suite, reject inline locators — the Module 3 skill with teeth, block commits on red). Subagents: writer/reviewer/runner. The toolbelt pattern: check for a CLI before building an integration — `gh` for issues/PRs/checks, `az boards`/`az repos` for the enterprise crowd. Custom outward-facing skills: the Jira skill as worked example. Plus 10 minutes on prompt injection and constrained tool access — the security mindset in one segment.
**Lab:** two hooks; file a demo-project bug via `gh` with reproduction steps from a real run. Stretch A: writer → reviewer flow on a Module 5 task. Stretch B: the Jira skill against a free Jira Cloud instance.
**Outcome:** boundaries, divided responsibilities, hands on the real toolchain.

## Module 8 — Self-Healing Tests (30 min, demo-led · 15/12/3)

Listener-based healing: intercept the failure, inspect the live page, recover, keep running. Healing vs. hiding — assertions keep it honest. Every heal logged and reviewable; heals are *proposals*, never silent mutations. Live: UI-drift script mid-suite, then the healing report reviewed like adults.
**Lab (compact):** enable listener, run drift script, run suite, triage the report per heal: accept / reject / investigate.
**Outcome:** a working setup and the governance instinct to go with it.

## Module 9 — CI & Toolchain Integration (35 min · 15/15/5)

What belongs in CI (triage, healing suggestions, summaries) and what doesn't (unreviewed generation to main). Determinism and trust: pinned models, constrained tools, budgets, timeouts, every agent action a reviewable artifact. GitHub Actions hands-on: failure → agent analyses via `robotcode results` → root-cause PR comment; heals become suggestion PRs. Azure DevOps and Jira shown as the same pattern.
**Lab:** enable the provided workflow on your fork; push a breaking change; open a PR; watch the agent explain your mistake in public. Character-building. Stretch: heal-suggestion PR step.
**Outcome:** agents do the tedious parts; humans keep the merge button.

## Module 10 — Wrap-Up, Roadmap & Q&A (10 min)

The ladder once more; the honest advice (most teams should live on rungs 1–3 for a quarter); the Monday plan in ascending effort: (1) write your `AGENTS.md`, (2) install the RobotCode plugin + RF Agent Skills, (3) add one CI triage step. RF AI initiative, contributing skills back, open Q&A.

---

# 4. Tool Stack

Everything used during the day, what for, and when it first appears.

| Tool | Purpose in the workshop | First used | Install / access |
|---|---|---|---|
| Python 3.10+ | Runtime for everything | M0 | Participant machine |
| Robot Framework | The star of the show | M0 | `pip install robotframework` (pin version in repo) |
| Browser Library | UI automation against the demo shop | M0 | `pip install robotframework-browser` + `rfbrowser init` |
| Requests-based library | API-level tests (M5 stretch) | M5 | `pip install` per repo requirements |
| Docker + Compose | Runs the demo shop locally | M0 | Participant machine |
| **Demo shop app** | The system under test — small web shop with seeded data, stable IDs, and a UI-drift script | M0 | Ships in the workshop repo, `docker compose up` |
| Claude Code | Reference coding agent (Copilot CLI / Codex work too) | M1 | Per vendor docs; agent choice guide in repo |
| `AGENTS.md` / `CLAUDE.md` | Tier 1: standing project context | M2 | Text editor. That's the point. |
| Agent Skills / `SKILL.md` | Tier 2: on-demand expertise | M3 | Workshop repo `skills/` + marketplace |
| Robot Framework Agent Skills | Ready-made RF skills | M3 | Marketplace / repo install, per setup guide |
| RobotCode CLI + agent plugin | Tier 3: discover, libdoc, robot-debug, REPL, results | M4 | `pip install robotcode` **in the project venv** (not pipx/uvx); plugin via marketplace |
| Robot Framework MCP server | Tier 4: live stepwise execution | M6 | Per setup guide; config snippets for each agent in repo |
| Hooks (agent-native) | Guardrails | M7 | Provided configs in repo `hooks/` |
| Subagent definitions | Writer / reviewer / runner | M7 | Provided in repo `agents/` |
| `gh` CLI | GitHub reach: issues, PRs, checks | M7 | Installed + authenticated pre-workshop |
| `az` CLI | Azure DevOps reach (optional track) | M7 | Optional; demo covers it if few have it |
| Jira Cloud (free tier) | Custom-skill target (optional) | M7 | Optional; sign-up link in setup guide |
| Self-healing listener | Runtime locator recovery | M8 | Per setup guide; enabled via `--listener` |
| GitHub Actions | CI integration | M9 | Participant's fork; workflow ships in repo |
| Zoom/Teams + breakouts, `#help` channel, poll tool, shared whiteboard | Facilitation | All day | Organizer side |

**Pinning policy:** every Python dependency pinned in `requirements.txt`; agent plugin and skills versions named explicitly in the setup guide; demo shop image tagged. Version drift is the #1 cause of workshop-day chaos — a locked stack is non-negotiable.

---

# 5. GitHub Participation Repository

One public repository is the workshop's home before, during, and after. Suggested name: `agentic-engineering-workshop` (under the Foundation or MarketSquare org — decide early, the URL goes on every slide).

## 5.1 Repository layout

```
agentic-engineering-workshop/
├── README.md                  # What this is, quickstart, link to setup guide
├── AGENTS.md                  # Deliberately minimal at start — Lab 2 builds it out
├── SETUP.md                   # Full participant setup guide (sent T-1 week)
├── GLOSSARY.md                # The workshop glossary
├── requirements.txt           # Pinned. Everything.
├── setup-check/
│   └── check.py               # One command verifies the whole environment
├── demo-shop/                 # System under test
│   ├── docker-compose.yml
│   ├── app/                   # Small web shop, seeded data, stable IDs
│   └── drift.py               # The UI-drift script (renames IDs, shuffles attributes)
├── tests/                     # The deliberately imperfect RF suite
│   ├── ui/                    #   incl. the pre-broken tests (marked by tag: broken)
│   └── api/                   #   target of the nested-AGENTS.md stretch goal
├── labs/
│   ├── lab-02-context/        # One folder per lab:
│   │   ├── INSTRUCTIONS.md    #   numbered steps + stretch goal
│   │   └── checklist.md       #   what "done" looks like
│   ├── lab-03-skills/
│   ├── lab-04-robotcode/
│   ├── lab-05-prompt-to-green/
│   ├── lab-06-mcp/
│   ├── lab-07-hooks-toolbelt/
│   ├── lab-08-healing/
│   └── lab-09-ci/
├── skills/                    # Skill artifacts
│   ├── jira-ticket/           #   the provided Jira skill (Lab 7 stretch B)
│   └── template/              #   SKILL.md template for Lab 3
├── hooks/                     # Provided hook configs (run-suite-after-edit, no-inline-locators)
├── agents/                    # Subagent definitions (writer, reviewer, runner)
├── mcp/                       # RF MCP config snippets per agent
├── .github/
│   ├── workflows/
│   │   ├── run-tests.yml            # Plain suite run
│   │   ├── agent-triage.yml         # Lab 9: failure → root-cause PR comment
│   │   └── heal-suggestions.yml     # Lab 9 stretch: heals → suggestion PR
│   ├── ISSUE_TEMPLATE/
│   │   ├── setup-problem.yml        # Pre-workshop support funnel
│   │   └── bug-report.yml           # Target format for the Lab 7 gh exercise
│   └── DISCUSSIONS categories: Q&A, Show-your-setup, After-the-workshop
├── transcripts/               # Fallback: recorded agent interactions per lab
└── docs/
    ├── conventions.md         # Referenced from AGENTS.md (Lab 2 material)
    ├── environments.md
    └── facilitator/           # Everything from section 6–8 of this document
```

**Branches:** `main` is the participant starting state. `solutions` holds reference solutions per lab (same folder structure). Never merge `solutions` into `main` — participants fork `main`.

## 5.2 Participation model

- **Fork, don't clone-only:** each participant forks the repo. Lab 9 requires it (Actions run on their fork), and it means everyone leaves with their own working copy including their day's changes.
- **Issues as the support funnel:** setup problems before the workshop go through the `setup-problem` template — triaged async, common fixes promoted into `SETUP.md`. On the day, `#help` in the meeting chat takes over.
- **Discussions for the long tail:** Q&A during and after; a "Show your setup" category where participants post their `AGENTS.md`/skills after applying the material at work — this is where the community value compounds.
- **The Lab 7 loop-back:** the `bug-report.yml` issue template doubles as the target format for the `gh` exercise — participants file real issues against the demo shop's real (planted) bugs. The repo eats its own dog food.
- **After the day:** repo stays public and maintained; demo recordings linked from the README same-day; a `CONTRIBUTING.md` invites improved skills and additional labs. Good first issues: "add a lab for <suggested follow-up topic>".

## 5.3 Actions & secrets

- `agent-triage.yml` needs an LLM API key: stored as a repo/fork secret, documented in `SETUP.md`, with a **spending cap warning in bold**. Provide a no-key fallback: the workflow posts the `robotcode results` summary without agent analysis, so the lab degrades gracefully.
- All workflows pinned to specific action versions and model versions. Timeouts and token budgets set — the workshop should model the discipline it teaches.

---

# 6. Participant Onboarding Timeline

| When | What | Owner |
|---|---|---|
| T-4 weeks | Registration confirmation + save-the-date, glossary attached ("read in 10 min") | Organizer |
| T-2 weeks | Repo public; `SETUP.md` final; agent-choice guide (Claude Code / Copilot CLI / Codex) | Lead |
| T-1 week | Setup email: fork the repo, run `setup-check`, file issues if red. API-key and cost note. | Lead |
| T-2 days | **Optional drop-in setup call (45 min)** — historically the highest-ROI hour of prep | Co-host |
| T-1 day | Reminder: schedule, breaks, "two monitors help", link sheet | Organizer |
| Day, 08:45 | Room opens early; co-host on triage | Both |
| T+1 day | Follow-up: recordings, `solutions` branch pointer, feedback form, Discussions invite | Organizer |

---

# 7. Facilitator Preparation Checklist

**T-6 to T-4 weeks**
- [ ] Decide repo org + name; create repo from this structure
- [ ] Build/adapt demo shop; plant the broken tests and the bugs for Lab 7; verify `drift.py` produces *healable* drift (relabels) and *unhealable* drift (a real regression) — Module 8's honesty depends on both
- [ ] Pin the full dependency stack; write `setup-check`
- [ ] Dry-run Labs 2–6 end-to-end on a clean machine — **especially Lab 5 without MCP**: the whole afternoon dramaturgy depends on Tiers 1–3 carrying it
- [ ] Record fallback transcripts per lab (agent interaction walkthroughs)

**T-3 to T-1 weeks**
- [ ] Full dry-run of the cold open until it's boringly reliable — it's the first five minutes; it may not flake
- [ ] Test `agent-triage.yml` on a fresh fork with a fresh key; verify the no-key fallback
- [ ] Second-agent spot-check: run Labs 2–4 with Copilot CLI or Codex to know where instructions diverge
- [ ] Prepare polls, whiteboard template (review checklist skeleton), breakout plan
- [ ] Co-host walkthrough: triage playbook, solutions branch, where each fallback lives

**T-1 day / day-of**
- [ ] Freeze `main`; tag it (`workshop-2026-XX`)
- [ ] Verify demo shop image pulls cleanly; API keys valid; quotas sufficient
- [ ] Timer visible to lead; module-by-module run sheet printed (yes, printed)
- [ ] Open the room 15 min early

---

# 8. Risks & Fallbacks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Participant agent/API access fails mid-day | High (someone, always) | `transcripts/` walkthroughs per lab; rejoin at next module; Modules 2–4 need minimal cloud access — the safe harbour |
| Version drift breaks a lab | Medium | Everything pinned; `setup-check` validates versions, not just presence |
| Corporate proxy blocks agent or Docker | Medium | Named in T-1 week email with test command; drop-in call catches the rest; pairing as last resort |
| Cold open flakes live | Low (after dry-runs) | Recorded backup of the cold open, one keypress away. Never debug the opener on stage. |
| Lab 5 underdelivers without MCP | Low if rehearsed | Dry-run requirement above; if a story proves too hard for Tiers 1–3, swap it for an easier one — don't quietly enable MCP early |
| Non-determinism confuses ("mine looks different") | Certain | Framed in glossary + Module 1; debriefs *compare* outcomes — that comparison is the calibration skill |
| Timing overrun | Medium | Buffer in debriefs and stretch goals only; pre-agreed cut order: M8 lab → M9 stretch → M7 stretch B |
| Beginner-heavy audience | Known at registration | Drop M8 to demo-only, give its lab time to M2 |

---

# 9. What Participants Leave With

- Their fork: demo project, their own `AGENTS.md`, their authored skill, working hooks, MCP config, CI workflow — everything they built, in their account
- The `solutions` branch and same-day demo recordings
- The glossary, the group's review checklist, and the Monday plan: **(1) AGENTS.md, (2) RobotCode plugin + RF Agent Skills, (3) one CI triage step**
- A place to come back to: Discussions, `CONTRIBUTING.md`, and the RF AI initiative

---

*Built by the community, for the community. Fork it, break it, heal it.*
