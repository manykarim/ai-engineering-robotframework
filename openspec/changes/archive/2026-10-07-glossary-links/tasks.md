## 1. The glossary

- [x] 1.1 Add the links of the proposal to *Skill*, *Subagent*, *Hook*, *Context file* and *OpenSpec*, each labelled with whose documentation it is. Verify:
  - every link answers with HTTP 200, and the `#claude-md-files` anchor exists on its page;
  - each entry grew by one line at most;
  - no other entry changed.
- [x] 1.2 Add *Context engineering* under *Tier 1: Context*, linking Martin Fowler's article, and *Spec-driven development* under *Spec-driven work*, linking OpenSpec. Verify:
  - each new entry has at most three lines;
  - each defines the term, not the link;
  - `tools/check_labs.py` passes.

## 2. Close-out

- [x] 2.1 Run the checks and open the pull request. Verify:
  - `openspec validate --all --strict` passes;
  - the site builds, with the glossary's new anchors `#context-engineering` and `#spec-driven-development`.
- [x] 2.2 Archive after the merge. Verify: `workshop/facilitation`'s *A glossary* reads as in the change.
