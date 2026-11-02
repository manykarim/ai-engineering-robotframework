# Lab 7 - Done when

- [ ] Your agent's hook wiring file is in place.
- [ ] An edit that adds a locator literal to a test file was rejected.
- [ ] A misspelled keyword came back with the static check's finding.
- [ ] A test file edit came back with the result of the affected tests.
- [ ] A `git commit` after a red run was blocked.
- [ ] Your own hook is in your agent's hook file, next to the four provided ones.
- [ ] Your own hook refused or answered an action of your agent, the way you meant it to.
- [ ] `uv run --no-sync python hooks/no_inline_locators.py tests/` reports nothing.
- [ ] Under `buggy`, the suite had failures, and `results/issue.md` describes one of them with steps, expected,
      actual and evidence.
- [ ] `gh issue list --repo <your-handle>/ai-engineering-robotframework` shows the issue you filed.
- [ ] `uv run --no-sync python -m shop status` shows `clean`, and `uv run --no-sync python hooks/green_before_commit.py --check`
      says a commit may go ahead.
