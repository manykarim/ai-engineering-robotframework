# Bonus 2 - A tool: the reference

[Bonus 2](../labs/bonus-2-tool/INSTRUCTIONS.md) has you build a listener that turns failed tests into GitHub issues,
with your agent, from a context you write before the first prompt. The reference is the rehearsal's result, with
Claude Code, recorded in the [transcript](../transcripts/bonus-2-tool.md). Its project is on this branch, under
`bonus/bonus-2-tool/`.

## The reference

`AGENTS.md`, written from the lab's list in step 3:

```markdown
## Toolstack

- Python 3.12 with uv; Robot Framework 7.5 is the only dependency at run time.
- HTTP goes through `urllib.request` from the standard library, so that the listener runs in any project's
  environment.
- Unit tests run with `uv run pytest`, Robot tests with `uv run robot --outputdir results atest`.
- Packaging with `uv build`.

## References

- `references/github-issues.json`.
- The User Guide's
  [listener interface](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#listener-interface)
  and its [version 3](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#listener-version-3).
- [`ListenerV3`](https://robot-framework.readthedocs.io/en/v7.5/autodoc/robot.api.html#robot.api.interfaces.ListenerV3)
  in the Robot API, whose code is `robot/api/interfaces.py` in the project's `.venv`.

## Concepts

- A listener, version 3, registered with `--listener module.Class:name=value`.
- A reporter never fails or changes a test: every error of its own becomes a warning.
- The token comes from `GITHUB_TOKEN` or `GH_TOKEN`, never from an argument or a file.
- The dry run is the default.
- It imports from its source folder alone, as step 8 runs it with `--pythonpath`: it reads nothing about
  itself from installed package metadata.

## Examples

- `references/example-listener.py`.

## Specification

- OpenSpec, under `openspec/changes/`.
```

The listener, `robotframework_github_reporter.GitHubIssues`, in about 360 lines over three modules: `listener.py`
(the Robot Framework side), `github.py` (the requests, through `urllib.request`) and `content.py` (titles and
bodies). It starts like this:

```python
class GitHubIssues:
    """Opens a GitHub issue for each failed test, or comments on its open issue.

    Use as `--listener robotframework_github_reporter.GitHubIssues:repo=owner/name[:dry_run=false][:label=...]`.
    """

    ROBOT_LISTENER_API_VERSION = 3
```

Robot Framework 7.5 is its only dependency at run time. 76 unit tests replace `urllib.request.urlopen`, and 5 Robot
tests run a failing suite with the listener in a dry run.

On the workshop's `tests/ui/catalogue.robot`, the dry run recorded three requests in `results/github-requests.json`,
and sent none:

```text
GET  /repos/your-handle/ai-engineering-robotframework/issues?state=open&labels=robot-failure&per_page=100
POST /repos/your-handle/ai-engineering-robotframework/issues   Failing test: Catalogue.WEB-002_AC-4 Rating Filter
POST /repos/your-handle/ai-engineering-robotframework/issues   Failing test: Catalogue.WEB-002_AC-12 Handpicked Highlights
```

The run failed the same two tests as without the listener.

## Why it is a good result

- **The context came first.** `AGENTS.md` names the toolstack, the saved GitHub endpoints, the listener chapter and
  the `ListenerV3` entry for 7.5, the rules a reporter must keep, and a listener to imitate. The proposal, design
  and tasks the agent wrote all follow from it.
- **A reporter that cannot break the run.** Every argument has a default, and every error of its own becomes a
  warning: a failing reporter never fails a test.
- **No dependency at run time beyond Robot Framework,** so it runs in the workshop's environment with `--pythonpath`,
  without being installed there.
- **The token is read from the environment only,** and the dry run is the default: nothing reaches GitHub until you
  ask for it.

## What to debrief

- **What the agent could not guess.** In the first rehearsal, the lab did not yet say that the listener must import
  from its source folder alone. The agent's package read its own version from installed package metadata, a normal
  choice for a library. Run with `--pythonpath` from another project, the import failed, Robot Framework skipped the
  listener with an error, and the run went on as if nothing were wrong. One line in `AGENTS.md` fixed it: an
  integration constraint is context the agent needs, however obvious it seems to you.
- **The size of the slice.** For one listener event, the agent planned 17 tasks and wrote 76 unit tests. Review the
  tasks before you apply, as you review the specs: a slice you would not build in an afternoon is too big.

## Compare yours

The reference is on the `solutions` branch, which your fork does not have. From your workshop clone:

```bash
git fetch upstream solutions
mkdir -p ../reference && git archive upstream/solutions bonus/bonus-2-tool | tar -x -C ../reference
diff ../reference/bonus/bonus-2-tool/AGENTS.md ../robotframework-github-reporter/AGENTS.md
```

No `upstream` remote yet? [Add it first](README.md#compare-your-files-with-the-reference).
