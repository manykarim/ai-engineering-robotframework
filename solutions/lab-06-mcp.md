# Lab 6 - MCP: the reference

[Lab 6](../labs/lab-06-mcp/INSTRUCTIONS.md) connects the Robot Framework MCP server, has your agent rebuild a Lab 5
test step by step on the live page, and compares the two. [Transcript](../transcripts/lab-06-mcp.md).

## The reference

The server's configuration for Claude Code, `.mcp.json`. The other agents' files are in `mcp/`.

```json
{
  "mcpServers": {
    "robotframework": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "--no-sync",
        "rf-mcp"
      ],
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

The stepwise rebuild of `WEB-004_AC-3` lost the comparison, so the reference keeps the Lab 5 test and has no stepwise
file.

## Why it is a good result

- **The server runs from the project's environment** at the pinned version, with `PYTHONPATH=.`, so it finds the
  shop's settings.
- **The comparison was decided on the conventions,** not on which version is newer, and one test per criterion is
  left.

## What to debrief

What live access changed in the rehearsal, and what it did not:
- **Changed:** it pinned what the shop happens to show. The stepwise version found the search input by its
  accessible name, "Search products".
- **Not changed:** every assumption of the Lab 5 version held: one search box, the results region, one card with its
  image and price. Neither version can tell whether Enter produced the results, because the shop also searches by
  itself shortly after typing stops.
- **Why the Lab 5 version won:** "Search products" comes from the shop, not from the specification, and the
  conventions allow accessible names only where the specification speaks of a label. The stepwise heading check was
  case-sensitive, and the stepwise tests covered one of AC-3's two ways of searching.

## Compare yours

```bash
git fetch upstream solutions
REF=$(git log -1 --format=%H --grep '^lab-06-mcp' upstream/solutions)
git diff "$REF" -- .mcp.json
```

The lines marked `-` are the reference's, the lines marked `+` yours. No `upstream` remote yet? [Add it first](README.md#compare-your-files-with-the-reference).

Your stepwise test is the result to compare: with the [conventions](../docs/conventions.md) and with your Lab 5
test, as the lab's comparison step does.
