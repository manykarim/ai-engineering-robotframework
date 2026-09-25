# Lab 7 - Done when

- [ ] Your agent's hook wiring file is in place.
- [ ] An edit that adds a locator literal to a test file was rejected.
- [ ] A test file edit came back with the result of the affected tests.
- [ ] A `git commit` after a red run was blocked.
- [ ] `uv run --no-sync python hooks/no_inline_locators.py tests/` reports nothing.
- [ ] Under `buggy`, the suite had failures, and `results/issue.md` describes one of them with steps, expected,
      actual and evidence.
- [ ] `gh issue list --repo <your-handle>/ai-engineering-robotframework` shows the issue you filed.
- [ ] `uv run --no-sync python -m shop status` shows `clean`, and `uv run --no-sync python hooks/green_before_commit.py --check`
      says a commit may go ahead.
