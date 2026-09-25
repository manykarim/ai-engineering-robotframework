# Lab 5 - Done when

## Plan review (step 3, with your partner)

- [ ] The change covers exactly your slice: no criterion missing, none added.
- [ ] Its specs live under `specs/suite/<area>/` in the change, not under `shop/` or `workshop/`.
- [ ] Every requirement names the criterion it verifies, as `<STORY>_<AC>`, and says what is checked.
- [ ] The tasks name one test per criterion (or more), each named `<STORY>_<AC> <behaviour>`.
- [ ] The tasks put every locator into a keyword under `resources/`, built from roles, labels or visible text.
- [ ] Quoted texts from the specification appear as they are, not paraphrased.
- [ ] Every test creates its own state (for example its own cart), and nothing applies a preset or resets the shop.
- [ ] The last task runs the new tests.

## Result (step 5)

- [ ] `uv run robotcode robot tests/ui/<your file>.robot` passes.
- [ ] `hooks/no_inline_locators.py` reports nothing for your file.
- [ ] Each test carries its story tag and `ui`.
- [ ] Each test passes on its own: `uv run robotcode robot --test "<one test name>"`.
- [ ] Every expected text in your tests can be found in `openspec/specs/shop/<area>`.

## Debugging (step 6)

- [ ] Your agent explained the cause of the failing rating-filter test from the repository's files alone.
- [ ] `uv run robotcode robot --test "WEB-002_AC-4 Rating Filter"` passes, and the test no longer carries the tag
      `broken`.
