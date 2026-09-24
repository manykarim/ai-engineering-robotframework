# Suite outcomes

*Facilitator material.* What the shipped suite does under each preset, and why. The source of truth is
[`suite-outcomes.toml`](suite-outcomes.toml). This command checks it against the pinned shop, and exits non-zero on
any difference:

```bash
uv run --no-sync python tools/verify_outcomes.py          # all six presets, plain runs
uv run --no-sync python tools/verify_outcomes.py --heal   # drift_and_bug with healing, broken tests excluded (needs HEAL_* settings)
```

It uses `SHOP_URL` and `SHOP_SPACE` like everything else, so it works against the local shop and in a space on the
shared instance. It resets the space when it finishes.

## The tests and their locators

Each fragile test reaches one kind of element through a legacy locator (`resources/legacy.resource`). It fails in
exactly the stages that kind drifts in. Everything else in the suite uses the stable contract, and passes in every
stage.

Every legacy locator names a single element, because that is all `robotframework-heal` can repair: it accepts a
replacement only when it matches exactly one element. The two catalogue tests find the grid's container by its class,
and read the cards and prices inside it by the stable contract. A legacy locator for every card at once would heal to
the first card only.

| Test | Locator | Drifts in |
|---|---|---|
| `WEB-002_AC-1 Card Prices Are The Product Prices` | class (the grid) | stage 2, stage 4 |
| `WEB-002_AC-7 Audio Filter Shows Only Audio` | class (the grid) | stage 2, stage 4 |
| `WEB-006_AC-1 Order Total Adds Up` | `data-test` | stage 3, stage 4 |
| `WEB-006_AC-7 Successful Order` | form-field id | stage 2, stage 3, stage 4 |
| the other seven tests | stable contract | - |

## What fails, per preset

**Presets compose. Always apply `clean` first.** `buggy` switches only the bugs, and keeps whatever locator stage is active: `stage4` followed by `buggy` is stage 4 with every bug, and two more tests fail. Every row below starts from `clean`, and so does `verify_outcomes.py`.

The two tests broken on purpose fail everywhere and are left out below. Run with `--exclude broken` in Modules 7 and 8.

| Preset | Also fails |
|---|---|
| `clean` | - |
| `stage2` | card prices (class), audio filter (class), successful order (id) |
| `stage3` | order total (`data-test`), successful order (id) |
| `stage4` | card prices, audio filter, order total, successful order |
| `buggy` | every card offers "Add to cart", card prices, order total. Three planted defects: products 5 and 10 have no button, products 3, 6, 9 and 12 show 1.15 times their price, and the displayed total omits tax. The slow catalogue makes nothing fail. |
| `drift_and_bug` | card prices, audio filter, order total, successful order |

## Module 8: the triage answers

Run `uv run robotcode -p heal robot --exclude broken` under `drift_and_bug`, with a model configured. Healing repairs
every drifted locator. Four tests failed without healing. With it:

| Test | Heal | Verdict |
|---|---|---|
| `WEB-002_AC-7 Audio Filter Shows Only Audio` | the grid's class, reused from the card-price heal | **accept**: pure drift, the test now passes |
| `WEB-006_AC-7 Successful Order` | three form-field ids -> new locators | **accept**: pure drift, the test now passes |
| `WEB-002_AC-1 Card Prices Are The Product Prices` | the grid's class -> new locator | **reject the idea that it is fixed**: the locator healed, and the test still fails on the prices of products 3, 6, 9 and 12. That is a real defect |
| `WEB-006_AC-1 Order Total Adds Up` | the total's `data-test` hook -> new locator | **reject the idea that it is fixed**: the locator healed, and the total still omits tax. That is a real defect |

Healing never hides the two defects. The profile sets `HEAL_HEAL_ASSERTIONS=false`, so a failing expected value is
never "healed" into agreement.

The report in `results/heal/heal_report.html` lists one heal fewer than there are drifted tests. The audio-filter
test passes the same grid locator as the card-price test, so heal reuses the first repair without asking the model
again. The log says *"proactively replaced known-broken locator"*.

### Read the proposal, not only the result

heal accepts a model's locator when it matches exactly one visible element. It does not check that it is the element
the test meant. Worth showing from the report:

- **Where a heal lands.** In the maintainer's runs, the total healed onto its whole row, `css=div.payment-totals__total`,
  whose text is "Total due at payment $249.99". The test reads the amount out of it, so the heal works, but the
  proposed locator is a new class, which will drift again. The stable fix is the row's visible label. That is the
  contrast with the agentic path of Lab 8, which edits the keyword onto the stable contract.
- **A heal onto the wrong element.** Before the suite kept one fragile element per test, the attribute-less subtotal
  line healed onto the contact block in one run and onto the page heading in the next. The test then failed with
  *"No amount in ..."*. The verdict for such a heal is **reject**.
- **A heal that hides a broken test.** Run the healing profile *with* the broken tests and `WEB-002_AC-4 Rating Filter`
  usually passes: its only fault is a locator for the label "4 stars and up", which does not exist, and heal proposes
  `css=input[name="rating"]`. The test goes green, and no longer checks the label the criterion names, "4 stars & up".
  The verdict is **reject**: the fix is the label in the test, taken from `openspec/specs/shop/catalogue`. Whether a
  model makes this heal varies, so the matrix leaves the broken tests out of the healing check.

## Module 7: what to file

Under `buggy`, the three failing tests each point at an issue worth filing with `gh`: a missing button, a wrong
price and a wrong total. The broken card links, on products 4, 8 and 12, are checked by no shipped test. Participants
who automated WEB-003 in Module 5 find them with their own test.

## The two tests broken on purpose

- **`WEB-002_AC-12 Handpicked Highlights`**, for Module 4. The failure message says only that the highlights are
  wrong. At a breakpoint on its assertion, the debugger shows `@{expected} = ['899.0', '799.0', '389.0']` beside
  `@{shown} = ['$899.00', '$799.00', '$389.00']`. The expected values come from the API as unformatted numbers.
- **`WEB-002_AC-4 Rating Filter`**, for Module 5. It waits for a checkbox named "4 stars and up".
  `openspec/specs/shop/catalogue` quotes "4 stars & up". An agent with the specs but no live page can find it.

## The one inline locator

`tests/ui/catalogue.robot`, test `WEB-002_AC-10 Reset Filters`: `Click    role=link[name="Reset"]`. It is the only
locator written in a test file instead of a resource. It is the finding for the Lab 3 skill and the Lab 7 hook, and
no participant-facing document mentions it. It uses the stable contract, so it never drifts and never distracts
from Module 8.
