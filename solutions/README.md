# Reference solutions

What each lab produced when the facilitators rehearsed it with Claude Code, why that is a good result, and the
answers the debrief covers. **Read a page after you have done its lab:** it gives the answers away.

Your result will differ in wording and sometimes in approach, and can be just as good. Compare it with the lab's
checklist first, and with the reference second.

| Lab | Reference | Recorded walkthrough |
|---|---|---|
| Lab 0 - Arrival | [lab-00-arrival.md](lab-00-arrival.md) | [transcript](../transcripts/lab-00-arrival.md) |
| Lab 2 - Context | [lab-02-context.md](lab-02-context.md) | [transcript](../transcripts/lab-02-context.md) |
| Lab 3 - Skills | [lab-03-skills.md](lab-03-skills.md) | [transcript](../transcripts/lab-03-skills.md) |
| Lab 4 - RobotCode | [lab-04-robotcode.md](lab-04-robotcode.md) | [transcript](../transcripts/lab-04-robotcode.md) |
| Lab 5 - Prompt to green | [lab-05-prompt-to-green.md](lab-05-prompt-to-green.md) | [transcript](../transcripts/lab-05-prompt-to-green.md) |
| Lab 6 - MCP | [lab-06-mcp.md](lab-06-mcp.md) | [transcript](../transcripts/lab-06-mcp.md) |
| Lab 7 - Hooks and the toolbelt | [lab-07-hooks-toolbelt.md](lab-07-hooks-toolbelt.md) | [transcript](../transcripts/lab-07-hooks-toolbelt.md) |
| Lab 8 - Healing | [lab-08-healing.md](lab-08-healing.md) | [transcript](../transcripts/lab-08-healing.md) |
| Lab 9 - CI | [lab-09-ci.md](lab-09-ci.md) | [transcript](../transcripts/lab-09-ci.md) |
| Bonus 1 - A library | [bonus-1-library.md](bonus-1-library.md) | [transcript](../transcripts/bonus-1-library.md) |
| Bonus 2 - A tool | [bonus-2-tool.md](bonus-2-tool.md) | [transcript](../transcripts/bonus-2-tool.md) |

## Where the reference lives

On the `solutions` branch of the workshop's repository: `main`, then one commit per lab that produces files, then
these pages, the transcripts and the facilitators' answer sheet. Nothing of it is on `main`, so your fork, and the
agent working in it, never sees it unless you fetch it.

## Compare your files with the reference

Fetch the branch once, after the lab:

```bash
git remote add upstream https://github.com/manykarim/ai-engineering-robotframework.git   # only once
git fetch upstream solutions
git log --oneline main..upstream/solutions
```

Then compare a file with the result of the lab that produced it, for example Lab 2's `AGENTS.md`:

```bash
REF=$(git log -1 --format=%H --grep '^lab-02-context' upstream/solutions)
git diff "$REF" -- AGENTS.md
```

Once fetched, the reference sits in your clone's git history, where an agent can read it when it goes looking.
Fetch it after the labs whose answers it holds, not before. The commands are for bash, zsh or Git Bash. In
PowerShell, write `$REF = git log ...` instead of `REF=$(...)`.
