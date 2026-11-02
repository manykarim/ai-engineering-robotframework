# Proposal

## Why

Lab 3 and the setup guide pin the Robot Framework Agent Skills installer at `rf-agentskills` 0.6.0. 0.7.0 is out
(2026-10-06) and is the latest stable release. Participants should install the current skills, and the reference
result on the `solutions` branch should show what that install produces.

## What Changes

- `labs/lab-03-skills/INSTRUCTIONS.md`, step 1: `uvx rf-agentskills@0.6.0` becomes `uvx rf-agentskills@0.7.0`. The
  rest of the command and the install folders stay: the 0.7.0 installer accepts the same flags and writes to the same
  places (`.claude/skills/`, `.agents/skills/`).
- `SETUP.md`, *Agent plugins and skills*: the installer becomes 0.7.0, both in the version column and in the command.
  The content version becomes 2.0.0, the content that 0.7.0 bundles (it was `v1.2.0`).
- **BREAKING** for anyone who already installed the skills: content 2.0.0 renames every skill to `rf-*` (12 skills).
  `rf-libdoc` replaces `libdoc-search` and `libdoc-explain`. The keyword, test-case and resource generator skills are
  retired, and the `rf-tools` MCP server is gone. Re-running the install upgrades in place and prunes files the bundle
  no longer ships. Lab 3's text names no skill, so its steps still hold.
- On the `solutions` branch, Lab 3's result is regenerated with 0.7.0. Its commit gets the files the 0.7.0 installer
  writes instead of the 0.6.0 ones. The participant's own skill, `locators-in-resources`, stays unchanged.
- The Lab 3 reference page lists the 0.7.0 skill names, and corrects where GitHub Copilot's skills land. It also says
  that the transcript was recorded with 0.6.0.
- Not changed: transcripts stay as recorded, and so do archived OpenSpec changes.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. `workshop/lab-assets` (*Third-party agent plugins are pinned*) requires the version that `SETUP.md` names and an
install into the project. Both still hold with 0.7.0, and no spec names the version. The change sets
`skip_specs: true`.

## Impact

- `main`: `labs/lab-03-skills/INSTRUCTIONS.md` and `SETUP.md`. The docs site renders both, so it picks up the change
  after the merge.
- `solutions`: the `lab-03-skills` commit (the installed skill files under `.claude/` and `.rf-agentskills/`) and the
  `reference` commit holding `solutions/lab-03-skills.md`. The branch is rebased and force-pushed, as
  `workshop/solutions` requires after a change to `main`.
- Participants: anyone who installed 0.6.0 for a rehearsal re-runs the install command. Their own skills stay.
- No Python dependency changes: `rf-agentskills` runs through `uvx` and is not in `pyproject.toml` or `uv.lock`.
