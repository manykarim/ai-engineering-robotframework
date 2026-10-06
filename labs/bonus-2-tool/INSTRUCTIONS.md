# Bonus 2 - A tool

Build a Robot Framework tool with your agent: a listener that turns failed tests into GitHub issues. Before the
first prompt, you give the agent what it cannot guess: the toolstack, GitHub's API description, the listener
interface of Robot Framework 7.5, the rules a reporter must keep, and a listener to imitate. Then it works from a
specification, slice by slice, as in Lab 5. The method is in
[Building libraries and tools with an agent](../../docs/building-with-agents.md).

| | |
|---|---|
| Module | Bonus 2 - Building a tool with an agent |
| Time | about 60 minutes, self-paced |
| Shop preset | `clean` |
| You need | The workshop's clone with its environment, OpenSpec (Lab 5), and `gh auth status` signed in (Lab 0) |
| You start from | A new folder next to your workshop clone |

## Steps

1. **Start the project next to the clone,** not inside it: the clone's `AGENTS.md` and `openspec/` would otherwise
   become the agent's context too.

   ```bash
   cd ..                                   # the folder that holds ai-engineering-robotframework
   uv init --lib robotframework-github-reporter
   cd robotframework-github-reporter
   uv add "robotframework==7.5"
   uv add --dev pytest
   ```

2. **Save the references** the agent needs into the project:

   ```bash
   mkdir references
   # GitHub's issue endpoints, from its own API description: listing, opening and commenting on issues
   uv run --no-project python -c "
   import json, urllib.request
   url = 'https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/dereferenced/api.github.com.deref.json'
   spec = json.load(urllib.request.urlopen(url))
   keep = ['/repos/{owner}/{repo}/issues', '/repos/{owner}/{repo}/issues/{issue_number}/comments']
   json.dump({path: spec['paths'][path] for path in keep}, open('references/github-issues.json', 'w'), indent=1)
   "
   # A listener to imitate: robotframework-heal's, from the workshop's environment
   uv run --project ../ai-engineering-robotframework --no-sync python -c "import shutil, heal.rf.listener as m; shutil.copy(m.__file__, 'references/example-listener.py')"
   ```

3. **Write `AGENTS.md`** yourself, from the skeleton in the
   [guide](../../docs/building-with-agents.md#2-five-kinds-of-context). For this project, it says:
   - **Toolstack:**
     - Python 3.12 with uv; Robot Framework 7.5 is the only dependency at run time;
     - HTTP goes through `urllib.request` from the standard library, so that the listener runs in any project's
       environment;
     - unit tests run with `uv run pytest`, Robot tests with `uv run robot --outputdir results atest`;
     - packaging with `uv build`.
   - **References:**
     - `references/github-issues.json`;
     - the User Guide's
       [listener interface](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#listener-interface)
       and its [version 3](https://robotframework.org/robotframework/7.5/RobotFrameworkUserGuide.html#listener-version-3);
     - [`ListenerV3`](https://robot-framework.readthedocs.io/en/v7.5/autodoc/robot.api.html#robot.api.interfaces.ListenerV3)
       in the Robot API, whose code is `robot/api/interfaces.py` in the project's `.venv`.
   - **Concepts:**
     - a listener, version 3, registered with `--listener module.Class:name=value`;
     - a reporter never fails or changes a test: every error of its own becomes a warning;
     - the token comes from `GITHUB_TOKEN` or `GH_TOKEN`, never from an argument or a file;
     - the dry run is the default.
   - **Examples:** `references/example-listener.py`.
   - **Specification:** OpenSpec, under `openspec/changes/`.

4. **Set up OpenSpec** for your agent, and give it the same context:

   | Claude Code | Codex | GitHub Copilot |
   |---|---|---|
   | `openspec init --tools claude` | `openspec init --tools codex` | `openspec init --tools github-copilot` |

   Uncomment `context:` in `openspec/config.yaml`, and write the five points of step 3 there in a few lines each.
   Start your agent in the project's folder, and ask it which instruction files it loaded: the project's, and none
   of the clone's.

5. **Propose the first slice** (`/opsx:propose` in Claude Code, `$openspec-propose` in Codex, `/opsx-propose` in
   GitHub Copilot):

   > A listener, version 3, importable as `robotframework_github_reporter.GitHubIssues`, with the arguments `repo`
   > (owner/name), `dry_run` (true by default) and `label` (`robot-failure` by default). For every failed test, it
   > opens an issue in `repo` titled "Failing test: <the test's full name>", with the label, the failure message,
   > the test's source and line, and the run's URL when it runs in GitHub Actions. If an open issue with that title
   > and label exists, it adds a comment instead. In a dry run it sends nothing: it prints each request it would
   > send, and writes them to `github-requests.json` in the output directory. Live, it reads the token from
   > `GITHUB_TOKEN` or `GH_TOKEN`, and falls back to a dry run with a warning when there is none. Unit tests replace
   > `urllib.request.urlopen`; Robot tests in `atest/` run a failing suite with the listener in a dry run.

6. **Review the proposal** before anything is built, as in Lab 5:
   - Does it use only the standard library for HTTP, and add no dependency at run time?
   - Can no error of the listener fail, skip or change a test?
   - Is the token read from the environment only, and is the dry run the default?
   - Do the unit tests cover a new issue, a comment on an open one, a dry run, a missing token and an API error?

   Ask for changes until the answer to each is yes.

7. **Apply it** (`/opsx:apply`, `$openspec-apply-change` or `/opsx-apply`), then run the checks yourself:

   ```bash
   uv run pytest
   uv run robot --outputdir results atest
   uv build
   ```

8. **Point it at the workshop's suite,** in a dry run. From the clone:

   ```bash
   cd ../ai-engineering-robotframework
   uv run robotcode robot --pythonpath ../robotframework-github-reporter/src \
     --listener "robotframework_github_reporter.GitHubIssues:repo=<your-handle>/ai-engineering-robotframework" \
     tests/ui/catalogue.robot
   ```

   It lists one issue for each test that fails, sends nothing, and the run fails exactly the tests it fails without
   the listener.

## Stretch

Run it live against your fork, then close what it opened:

```bash
GH_TOKEN=$(gh auth token) uv run robotcode robot --pythonpath ../robotframework-github-reporter/src \
  --listener "robotframework_github_reporter.GitHubIssues:repo=<your-handle>/ai-engineering-robotframework:dry_run=False" \
  tests/ui/catalogue.robot
gh issue list --repo <your-handle>/ai-engineering-robotframework --label robot-failure
```

Run it a second time: the issues get a comment each, and no new ones. In PowerShell, set the token first with
`$env:GH_TOKEN = gh auth token`.

## Compare with the reference

When you are done, compare your result with [the reference](https://manykarim.github.io/ai-engineering-robotframework/solutions/bonus-2-tool): what the
rehearsal produced, why it is a good result, and the answers the debrief covers. Open it after the lab: it
gives the answers away.

## If your agent fails

Follow
[the recorded walkthrough of this lab](https://manykarim.github.io/ai-engineering-robotframework/transcripts/bonus-2-tool).
