# Lab 5 - Prompt to green

Turn a user story into a green, convention-following test suite, the way you would with a junior engineer: agree on a
plan first, review it with a colleague, then let the work happen, run it, and refine. The vehicle is
[OpenSpec](../../GLOSSARY.md#openspec): a propose step that writes the plan down before any code exists. You finish
by debugging a broken test in conversation, without looking at the live page.

| | |
|---|---|
| Module | 5 - Natural Prompt Automation & Debugging |
| Time | 30 minutes |
| Shop preset | `clean` |
| You need | Labs 0 and 2 done; OpenSpec installed ([SETUP.md](../../SETUP.md#nodejs-and-openspec)); a partner for the review |
| You start from | `main`, plus your `AGENTS.md` from Lab 2 (step 0 says how to catch up) |

Everything in this lab works with files and the command line alone. Don't connect an MCP server yet: Module 6 is
about what it adds.

## Steps

0. **Missed Lab 2?** Take the reference `AGENTS.md`:

   ```bash
   git remote add upstream https://github.com/manykarim/ai-engineering-robotframework.git
   git fetch upstream solutions
   git checkout upstream/solutions -- AGENTS.md docs/agent-environment.md
   ```

1. **Pick a story** (2 minutes). Each comes with a slice of criteria. Automate the slice, not the whole story:

   | Story | Difficulty | Slice | Story file | Specification |
   |---|---|---|---|---|
   | WEB-004 search | easier | AC-1, AC-3, AC-6, AC-7 | [WEB-004](stories/WEB-004_search_products.md) | `openspec/specs/shop/search` |
   | WEB-003 product detail | medium | AC-1, AC-3, AC-8, AC-9 | [WEB-003](stories/WEB-003_view_product_detail.md) | `openspec/specs/shop/product-detail` |
   | WEB-005 cart | harder | AC-2, AC-3, AC-4, AC-9 | [WEB-005](stories/WEB-005_manage_cart.md) | `openspec/specs/shop/cart` |

   If the facilitator announces the swap-in, WEB-007 sign-in replaces one of them: AC-2, AC-3, AC-4 and AC-8 of
   [WEB-007](stories/WEB-007_user_authentication.md), specified in `openspec/specs/shop/authentication`.

   The story is how a product owner wrote it. The specification is the same behaviour, stated precisely enough to
   test. When they differ, the specification wins.

   Short on time, or told so by the facilitator? Take only the first two criteria of your slice.

2. **Propose** (10 minutes). Start the propose workflow with your slice. For WEB-004:

   | Claude Code | Codex | GitHub Copilot |
   |---|---|---|
   | `/opsx:propose` | `$openspec-propose` | `/opsx-propose` |

   > /opsx:propose Automate WEB-004_AC-1, WEB-004_AC-3, WEB-004_AC-6 and WEB-004_AC-7 from
   > labs/lab-05-prompt-to-green/stories/WEB-004_search_products.md as Robot Framework UI tests. The expected
   > behaviour is in openspec/specs/shop/search.

   It creates a change in `openspec/changes/<name>/`: a proposal, specs, a design and tasks. No test yet. The agent
   reads the specification and the suite first, so this takes several minutes: read your story meanwhile.

3. **Pair review the plan** (6 minutes, in your breakout). Share your screen with your partner and go through the
   change together, with the *Plan review* list in [checklist.md](checklist.md). Review it like a junior engineer's
   plan: is this what we want built? Fix what you find, by editing the files or by telling your agent, before
   anything is built. Then swap.

4. **Apply** (7 minutes). Let the agent build what the plan says:

   | Claude Code | Codex | GitHub Copilot |
   |---|---|---|
   | `/opsx:apply` | `$openspec-apply-change` | `/opsx-apply` |

5. **Run and refine** (2 minutes). Run your new tests yourself:

   ```bash
   uv run robotcode robot tests/ui/<your file>.robot
   ```

   Green? Check them against the conventions with the *Result* list in [checklist.md](checklist.md). Red? Ask your
   agent why, and to show you the evidence before it changes anything. Check for inline locators with:

   ```bash
   uv run --no-sync python hooks/no_inline_locators.py tests/ui/<your file>.robot
   ```

6. **Debug in conversation** (3 minutes). One of the two tests that fail on purpose is this lab's:

   > The test "WEB-002_AC-4 Rating Filter" fails. Find the cause using only the files of this repository, including
   > its specifications. Do not open a browser and do not use an MCP server. Explain the cause and your evidence
   > before you change anything.

   When the explanation holds up against the specification:

   > Fix it, remove its broken tag, and run it.

7. **Archive** the change if you have a minute left: `/opsx:archive` (Claude Code), `$openspec-archive-change`
   (Codex) or `/opsx-archive` (GitHub Copilot). Your specs move to `openspec/specs/suite/`, the record of what your
   tests verify.

## Stretch

Add API tests for API-005, the cart API: AC-1, AC-2, AC-4 and AC-7 of
[API-005](stories/API-005_cart_operations.md), specified in `openspec/specs/shop/cart`. Propose them the same way.
They go into `tests/api/`, with the keywords they need in `resources/api.resource`, tagged `api`. If you wrote
`tests/api/AGENTS.md` in Lab 2, check whether the agent followed it.

## If your agent fails

Follow [the recorded walkthrough of this lab](../../transcripts/lab-05-prompt-to-green.md), which does the WEB-004
slice. You can still do the pair review with its proposal: it is in the walkthrough.
