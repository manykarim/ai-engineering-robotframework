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
