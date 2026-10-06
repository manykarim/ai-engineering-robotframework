## Why

The glossary explains what skills, subagents, hooks and context files are, but rarely says where to read more. After
the day, that is the participant's next question.

Two terms the day relies on have no entry at all:
- *Context engineering* is the title of Module 2 and of Lab 2's header.
- *Spec-driven development* is the practice of Module 5. Only the tool, *OpenSpec*, is defined.

The glossary's own requirement asks for every term the labs use.

## What Changes

- **Links to primary sources** on existing entries. Every link names whose documentation it is: the workshop
  supports three agents, and four of these links are Claude Code's.

  | Entry | Links |
  |---|---|
  | *Skill* | Claude Code's [skills](https://code.claude.com/docs/en/skills); the [Agent Skills](https://agentskills.io/home) standard |
  | *Subagent* | Claude Code's [subagents](https://code.claude.com/docs/en/sub-agents) |
  | *Hook* | Claude Code's [hooks guide](https://code.claude.com/docs/en/hooks-guide) |
  | *Context file* | Claude Code's [CLAUDE.md files](https://code.claude.com/docs/en/memory#claude-md-files); the [AGENTS.md](https://agents.md/) standard |
  | *OpenSpec* | its [repository](https://github.com/Fission-AI/OpenSpec) |

- **Two new entries:**
  - *Context engineering*, under *Tier 1: Context*, links Martin Fowler's article
    [Context Engineering for Coding Agents](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html).
  - *Spec-driven development*, under *Spec-driven work*, links [OpenSpec](https://github.com/Fission-AI/OpenSpec).
- **The glossary requirement** gains this: entries for agent tooling and practices link the documentation a reader
  goes to next.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `workshop/facilitation`: *A glossary* defines context engineering and spec-driven development, and links the
  primary documentation of agent tooling and practices.

## Impact

- **Changed:** `GLOSSARY.md` only. The site renders it, and no lab text changes.
- **Size:** each existing entry grows by one line of links, and each new entry has at most three lines, so the
  glossary stays readable in about ten minutes.
- **Timing:** today is the workshop day. A merge updates the live glossary at once. The change adds text only and
  removes nothing a lab links to.
