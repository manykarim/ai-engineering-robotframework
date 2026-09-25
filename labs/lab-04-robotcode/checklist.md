# Lab 4 - Done when

- [ ] Your agent lists the `robotcode` plugin (Claude Code: `claude plugin list`).
- [ ] `AGENTS.md` has one line that points the agent to RobotCode through uv.
- [ ] The discovery answer came from `uv run robotcode discover`, visible in the session.
- [ ] The library answer came from `uv run robotcode libdoc`, visible in the session.
- [ ] The agent stopped at a breakpoint with `uv run robotcode robot-debug` and explained the cause from the
      variables it saw.
- [ ] `uv run robotcode robot --test "WEB-002_AC-12 Handpicked Highlights"` passes, and the test no longer carries
      the tag `broken`.
- [ ] `git diff --stat` shows changes only in `tests/ui/catalogue.robot`, `resources/catalogue.resource` and
      `AGENTS.md`.
- [ ] The agent explored the price range filter in the REPL, with a visible browser, without writing a test file.
