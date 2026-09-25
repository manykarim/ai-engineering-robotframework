---
name: resource-architect
description: Design Robot Framework resource and variables layout for maintainable suites. Use when asked to create resource files, variable files, or propose project structure with shared keywords and environment-specific data.
---

# Robot Framework Resource Architect

Create resource file templates and directory layout proposals. Output JSON only.

## Input (JSON)

Provide input via `--input` or stdin. Example:

```json
{
  "project_root": ".",
  "domains": ["auth", "orders"],
  "libraries": ["BuiltIn", "OperatingSystem"],
  "environments": ["dev", "qa"],
  "resource_naming": "by-domain",
  "variables_format": "resource"
}
```

## Command

```bash
python3 "/tmp/claude-1000/-mnt-c-workspace-ai-engineering-robotframework/6fe17ce9-00bd-4179-bc22-dbf725b60a81/scratchpad/rehearsal/repo/.claude/rf-agentskills-files/scripts/resource_architect.py" --input plan.json
```

Write files (optional):

```bash
python3 "/tmp/claude-1000/-mnt-c-workspace-ai-engineering-robotframework/6fe17ce9-00bd-4179-bc22-dbf725b60a81/scratchpad/rehearsal/repo/.claude/rf-agentskills-files/scripts/resource_architect.py" --input plan.json --write
```

Overwrite existing files (by default existing files are skipped):

```bash
python3 "/tmp/claude-1000/-mnt-c-workspace-ai-engineering-robotframework/6fe17ce9-00bd-4179-bc22-dbf725b60a81/scratchpad/rehearsal/repo/.claude/rf-agentskills-files/scripts/resource_architect.py" --input plan.json --write --overwrite
```

## Output (JSON)
- `directories`: planned directory list
- `files`: list of file paths + contents
- `warnings` and `suggestions`
