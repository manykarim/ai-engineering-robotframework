# Glossary

The words of the day, in about ten minutes. They are grouped by the rung of the maturity ladder where you first
meet them, then the words of spec-driven work and of this repository.

## The ladder

### Agentic engineering

Working with a coding agent that reads your project, runs commands, edits files and checks its own results, while
you set the direction and review the outcome. It is not autocomplete, and it is not handing over the keys.

### Coding agent

A program that drives a large language model in a loop with tools: reading and writing files, running shell
commands, calling servers. The workshop demonstrates Claude Code; Codex and GitHub Copilot work for every lab.

### Maturity ladder

The five rungs the day climbs, each useful on its own:
1. **Context**: standing knowledge in a [context file](#context-file).
2. **Skills**: expertise loaded when a task needs it.
3. **Tooling**: command-line tools the agent runs, such as [RobotCode](#robotcode).
4. **Live access**: a running session that stays open between the agent's steps, over [MCP](#mcp).
5. **Orchestration**: [hooks](#hook), [subagents](#subagent), CI and healing around the agent.

Most teams get the most from rungs 1 to 3 first.

### Tier

One rung of the ladder. "Tiers 1 to 3" means context, skills and tooling, without a session that stays open
between the agent's steps.

### Non-determinism

The same prompt gives different answers, run to run and agent to agent. Your result will differ from your
neighbour's. Comparing the two is how you learn what the agent relies on.

### Agents draft, humans decide

The standing rule of the day. An agent may propose tests, fixes, issues and heals; a person accepts or rejects them.

## Tier 1: Context

### Context engineering

Deciding what an agent sees, and when: what it always loads, what it loads for a task, and what stays out.
Read more: Martin Fowler's [Context Engineering for Coding Agents](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html).

### Context file

A Markdown file every session loads before your first prompt. `AGENTS.md` is the cross-agent standard; `CLAUDE.md`
here only imports it. It holds what is always relevant: how to build and run, where the system under test is, the
conventions, the boundaries. It never holds secrets, and nothing the agent can find out quickly by itself.
Read more: Claude Code's [CLAUDE.md files](https://code.claude.com/docs/en/memory#claude-md-files); the [AGENTS.md](https://agents.md/) standard.

### Modular context

A short root context file that points to focused files the agent reads only when a task needs them. A folder can
have its own `AGENTS.md` for what only applies there.

### Context window

What the model can see at once: your prompts, the context files, tool definitions and results. Everything loaded
into it costs space and attention, which is why less, well-chosen context works better.

## Tier 2: Skills

### Skill

A folder with a `SKILL.md`: a name, a description, instructions, and optionally scripts and reference files. The
agent reads only the description until a task matches it, then loads the rest. Always relevant: context file.
Relevant for one kind of task: skill.
Read more: Claude Code's [skills](https://code.claude.com/docs/en/skills); the [Agent Skills](https://agentskills.io/home) standard.

### Trigger

The moment a skill's description matches the task and the agent loads it. A vague description triggers too often or
never. Test both: a prompt that should load the skill, and one that should not.

### Plugin

A package of skills, and sometimes hooks, subagents or MCP servers, installed from a marketplace: a repository that
lists plugins. The RobotCode plugin is one.

## Tier 3: Tooling

### RobotCode

The Robot Framework toolkit behind the VS Code extension, with a command line agents can use: `uv run robotcode`.
Run through uv, it sees this project's libraries at their pinned versions. Commands, agent use and traps:
[the RobotCode cheat sheet](docs/robotcode.md).

### Discover

`robotcode discover`: asks the project which tests, suites and tags exist, resolved the way Robot Framework resolves
them at run time. More reliable than searching files, because tags and names can come from settings and options.

### Libdoc

`robotcode libdoc`: the documentation of a library as installed here, with every keyword and its arguments. Look a
keyword up instead of trusting what a model remembers from another version.

### Debugger

`robotcode robot-debug`: runs a real test and stops at a breakpoint, so that you, or the agent, can read the actual
variables. The alternative to guessing from a failure message.

### REPL

`robotcode repl`: runs keywords one at a time, interactively. The right tool for exploring a flow no test covers yet;
the wrong one for debugging a test that exists.

### Results

`robotcode results`: summaries, failures and statistics of the last run, without reading `output.xml` by hand.

### Static analysis

Checking test files without running them. `robotcode analyze code` finds keywords and variables that do not exist;
Robocop finds style issues and outdated syntax, and fixes some of them.
Read more: RobotCode's [analyzing code](https://robotcode.io/03_reference/analyzing-code); Robocop's [rules](https://robocop.dev/stable/rules/rules_list/).

## Tier 4: Live access

### MCP

The Model Context Protocol: a standard way for an agent to use tools a separate program offers. That program is an
*MCP server*. The Robot Framework MCP server runs keywords in a session that stays open, and shows the agent the page
after each step. RobotCode's [REPL](#repl) and [debugger](#debugger) reach the page too, but only while one command
runs. The MCP tools take room in the [context window](#context-window), so use them where live, stateful work pays
for that.

### Stepwise execution

Building a test one step at a time against the live system: run a step, look at the result, decide the next.

## Tier 5: Orchestration

### Hook

A command the agent runs automatically, before or after it uses a tool, and cannot skip. It can reject the action or
report back. Hooks turn conventions into guardrails.
Read more: Claude Code's [hooks guide](https://code.claude.com/docs/en/hooks-guide).

### Subagent

A separate agent with its own instructions and a limited set of tools, which the main agent hands a task to. A
reviewer that cannot edit files is one.
Read more: Claude Code's [subagents](https://code.claude.com/docs/en/sub-agents).

### Toolbelt

The command-line tools you already have, such as `gh` or `az`. Before building an integration for an agent, check
whether a tool it can run already does the job.

### Prompt injection

Text that an agent reads, from a web page, an issue or a tool's output, written to look like an instruction. An agent
with tools can be steered by it. Treat what agents read as data, and keep outward actions behind a human decision.

### Heal

A repair of a broken locator at run time: a healing listener notices that an element cannot be found, finds the one
the step meant, and continues. Here every heal is recorded as a proposal and never written into a file by itself.
Assertions are never healed, so a wrong value stays a failure.

### Healing report

The record of a healing run: for each heal, the old and new locator, and whether the step then passed. You triage it
heal by heal.

### Triage

Deciding what each finding is worth: *accept*, *reject* or *investigate*.

## Spec-driven work

### Spec-driven development

Agreeing on what a change must do, as a specification, before an agent builds it, and checking the result against
it. Read more: [OpenSpec](https://github.com/Fission-AI/OpenSpec), the tool this workshop uses.

### OpenSpec

A tool for agreeing on a change before building it. `/opsx:propose` writes a proposal, specs, a design and tasks;
you review them; `/opsx:apply` builds the change; `/opsx:archive` moves its specs into `openspec/specs/`.
Read more: OpenSpec's [repository](https://github.com/Fission-AI/OpenSpec).

### Specification

In this repository, `openspec/specs/shop/` describes what the shop does, criterion by criterion. It is the reference
for expected behaviour. The specs your own changes write go to `openspec/specs/suite/`.

### User story

A requirement as a product owner writes it, with acceptance criteria such as `WEB-004_AC-3`. Tests name the criterion
they verify.

## Building libraries and tools

### Assertion engine

The assertion operators of Browser's `Get` keywords (`Get Text    h1    ==    Welcome`), as a library of its own
that other libraries use for their keywords: [AssertionEngine](https://github.com/MarketSquare/AssertionEngine).

### PythonLibCore

The structure Browser and other libraries are built on: keywords in several classes, one library to Robot
Framework. [PythonLibCore](https://github.com/robotframework/PythonLibCore).

### Listener

Python code Robot Framework calls during a run: when a suite, test or keyword starts and ends. The heal profile is
one. [Bonus 2](labs/bonus-2-tool/INSTRUCTIONS.md) builds one.

## This repository

### Shop

The system under test: a small web shop that runs from a published container image, on your machine or on the shared
instance.

### Preset

A named state of the shop, applied with `uv run --no-sync python -m shop preset <name>`. `clean` is the normal state;
other presets drift the layout or switch on planted defects. Labs tell you when to apply one, and reset afterwards.

### Space

Your own copy of the shop's state on the shared instance, named after your GitHub handle. Presets you apply in your
space affect nobody else.

### Stable contract

What stays the same when the shop's markup changes: roles and accessible names, visible text, labels, form-field
names and link targets. Locators built on it survive layout drift. Ids, classes and `data-test` hooks do not.

### Drift

A change of the page's markup that leaves its behaviour intact: renamed ids and classes, removed hooks. It breaks
fragile locators and nothing else.

### Planted defect

A deliberate bug a preset switches on, for the labs to find. Which ones exist is part of the exercise.

### Broken test

A test that fails on purpose, tagged `broken`, for a debugging lab. There are two.

### Transcript

A recorded walkthrough of a lab by an agent, on [the site](https://manykarim.github.io/ai-engineering-robotframework/transcripts). If your agent fails, follow it and
rejoin at the next module.

### Fork

Your own copy of this repository on GitHub. You work in it all day, Lab 9 runs its CI on it, and you keep it.
