# Bonus 2 - Done when

- [ ] The project lives next to the workshop clone, and your agent named the project's `AGENTS.md` as its
      instructions, and none of the clone's files.
- [ ] `AGENTS.md` has a section each for toolstack, references, concepts, examples and the specification, and
      `references/` holds `github-issues.json` and `example-listener.py`.
- [ ] `openspec/config.yaml` has a `context:` with the same five points.
- [ ] The proposal passed your review of step 6 before it was applied.
- [ ] `uv run pytest` and `uv run robot --outputdir results atest` pass, and `uv build` wrote a wheel to `dist/`.
- [ ] `pyproject.toml` names Robot Framework as the only dependency at run time.
- [ ] On the workshop's suite in a dry run, the listener listed one issue per failed test, sent nothing, and the
      run failed the same tests as without it.
