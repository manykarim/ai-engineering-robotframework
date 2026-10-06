# Bonus 1 - Done when

- [ ] The project lives next to the workshop clone, and your agent named the project's `AGENTS.md` as its
      instructions, and none of the clone's files.
- [ ] `AGENTS.md` has a section each for toolstack, references, concepts, examples and the specification, and
      `references/` holds the shop's `openapi.json`, AssertionEngine's README and code, and two Browser keywords.
- [ ] `openspec/config.yaml` has a `context:` with the same five points.
- [ ] The proposal passed your review of step 6 before it was applied.
- [ ] `uv run pytest` and `uv run robot --outputdir results atest` pass against your local shop in `clean`.
- [ ] `Get Product Price    1    ==    249.99` passes, and `Get Product Price    1    ==    1` fails with
      AssertionEngine's message.
- [ ] `docs/DemoShopLibrary.html` documents every keyword, and `uv build` wrote a wheel to `dist/`.
- [ ] You can name one thing the library gives you over `resources/api.resource`, and one thing it costs.
