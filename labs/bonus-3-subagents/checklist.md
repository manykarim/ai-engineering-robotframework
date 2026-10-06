# Bonus 3 - Done when

- [ ] After step 1, `git diff upstream/main --stat -- tests resources` printed nothing.
- [ ] Your agent's subagent folder holds `debugger` and `analyzer`, and your agent lists both or starts them by name.
- [ ] The analyzer has no tool that edits files. With Codex, its instructions forbid hand edits.
- [ ] Each of the four failed tests got its own report from the debugger, with the cause, the evidence, the change
      and the result.
- [ ] `git diff -- tests resources` shows no changed expected value, assertion or tag.
- [ ] Under `drift_and_bug`, the tests the debugger repaired passed, and the ones it reported failed. Under
      `clean`, all of them passed.
- [ ] In step 8, the analyzer gave every finding a verdict, and `git status` showed no new change.
- [ ] `uv run robocop check --select replace-set-variable-with-var --select replace-create-with-var tests resources`
      reports no issues, and the suite under `clean` has the same result as at the end of step 7.
- [ ] Asked for a hand edit in step 10, the analyzer left the file unchanged.
- [ ] `uv run --no-sync python -m shop status` shows `clean`.
