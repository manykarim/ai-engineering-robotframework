## Context

See `proposal.md` for the motivation, and `specs/` for the requirements. The facts below were measured, not assumed, against demo-webshop `0.3.0` (its `docs/WORKSHOP-FEATURES.md` and the running shop) and `robotframework-heal` 0.4.0.

- **Each stage breaks a different kind of locator**, and the stable contract never drifts:

  | Kind (example) | Stage 1 | Stage 2 | Stage 3 | Stage 4 |
  |---|---|---|---|---|
  | covered form-field id (`id=checkout-email`) | pass | **fail** | **fail** | **fail** |
  | covered class (`.product-card__price`) | pass | **fail** | pass | **fail** |
  | `data-test` hook (`[data-test="product-price"]`) | pass | pass | **fail** | **fail** |
  | stable contract (role and name, text, label, field name, `href`, `data-category`) | pass | pass | pass | pass |

  The spike measured the first three rows. In stage 4 the class-exact rule falls back to the block rename, so `product-card__price` does drift.
- **Planted bugs are deterministic and stage-independent**:
  - the card button is missing on products 5 and 10;
  - the card price is ×1.15 on products 3, 6, 9 and 12, on the card only;
  - the checkout's displayed total omits tax;
  - the catalogue answers 1-3 s later;
  - broken card links, on products 4, 8 and 12, are checked by no WEB-002 or WEB-006 criterion.

  `drift_and_bug` is stage 4 plus the price and total defects.
- **`robotframework-heal` 0.4.0 heals nothing without a model.** It records the failure, classifies it `unknown`, and reports *"Healing skipped: No model configured for role 'locator'"*. `--listener Heal` attaches it without any change to a suite. It loads the nearest `.env` itself, and lets that file override the environment.
- **With a model, it heals one element at a time.** It accepts a replacement locator only when that locator matches exactly one visible element, and reruns the failed keyword with it. Within a run, it reuses a heal for a later call only when that call passes the identical locator string. Each failure has a budget of 60 s by default. The first healing run showed what that means for a suite. A legacy locator for a list, such as every card's price, was healed to its first element only. A `nth=0` wait that healed did nothing for the next call, which used a different string and matched nothing without failing. A wrong label, in the Module 5 broken test, was healed to the rating checkbox and passed.
- **`[name="email"]` matches two inputs on the checkout page**: the form's field and the sign-in dialog's.

## Goals / Non-Goals

**Goals:**
- Every test's behaviour under every preset is predictable from its declared locator kind and the defect table, and a script proves it.
- Module 8 shows healable drift healing and planted defects refusing to heal, in one run.
- The suite is the example participants and agents extend, so it follows the conventions it documents, with two deliberate exceptions.

**Non-Goals:**
- Participants' own tests, lab texts, skills, hooks and workflows (`workshop-labs`, `ci-and-site`).
- Deciding how participants obtain an LLM endpoint for Module 8. That decision belongs to `workshop-labs`; this change only makes the profile work once a model is configured.
- Covering broken card links. No WEB-002 or WEB-006 criterion checks them, so they remain the Module 7 find for participants who automate WEB-003.

## Decisions

### D1. The test inventory

| File | Test | Locator kind | Purpose |
|---|---|---|---|
| `tests/ui/catalogue.robot` | `WEB-002_AC-1 Every Card Offers Add To Cart` | stable (button by visible text) | fails under `buggy` |
| | `WEB-002_AC-1 Card Prices Are The Product Prices` | **class** (the grid) | drifts in 2 and 4; fails under `buggy` and `drift_and_bug` even when healed |
| | `WEB-002_AC-2 Categories Filter Group` | stable | the stable-contract example |
| | `WEB-002_AC-4 Rating Filter` | stable | **broken, Module 5** (D4) |
| | `WEB-002_AC-7 Audio Filter Shows Only Audio` | **class** (the grid) | drifts in 2 and 4; heals, no defect |
| | `WEB-002_AC-10 Reset Filters` | stable, with **the inline locator** (D5) | the Lab 3 / Lab 7 target |
| | `WEB-002_AC-12 Handpicked Highlights` | stable | **broken, Module 4** (D4) |
| `tests/ui/checkout.robot` | `WEB-006_AC-1 Order Total Adds Up` | **`data-test`** (the total) | drifts in 3 and 4; fails under `buggy` and `drift_and_bug` even when healed |
| | `WEB-006_AC-7 Successful Order` | **form-field id** | drifts in 2, 3 and 4; heals, no defect |
| | `WEB-006_AC-11 Validation Errors Next To Fields` | stable (labels, `aria-describedby`) | |
| | `WEB-006_AC-12 Cart Cleared After Order` | stable | |
| `tests/api/smoke.robot` | `Health Reports Ok` | API | smoke; Lab 2 nested-`AGENTS.md` target |
| | `Catalogue Lists Twelve Products` | API | smoke; the cart API stays untouched for the Module 5 stretch |

Every fragile test reaches **only** its one fragile element through the fragile kind; everything else it does goes through stable keywords. Its behaviour in each stage is therefore the row of its kind in the table above, and nothing else. The fragile element is always a single element, because that is all a heal can repair (see Context). The two catalogue tests therefore find the grid's container by its class, and read the cards and prices inside it through the stable contract. When the grid heals once, the second test reuses the heal, since both pass the same locator string. Each checkout test adds Aurora Neural Headphones (product 1) in its own context. Product 1 is not affected by any card defect, so `buggy` breaks exactly the three intended tests.

*Alternative:* covering more criteria. Rejected: each extra test adds matrix entries and reading time without adding a new lesson.

### D2. Resources and the space

`resources/` holds:
- `shop.resource`: the browser, a context per test, pages;
- `catalogue.resource` and `checkout.resource`: stable-contract keywords;
- `legacy.resource`: the id, class and `data-test` keywords, the documented deviation;
- `api.resource`: a RequestsLibrary session.

`New Context` is opened with `baseURL=${SHOP_URL}` and, when `${SHOP_SPACE}` is set, `extraHTTPHeaders={"X-Workshop-Space": "${SHOP_SPACE}"}`. Playwright applies it to every page load, asset and XHR. The API session carries the same header. Both variables come from the foundation's variable file, so the local and shared profiles need nothing more. There is one browser per suite and one context per test: a fresh cookie jar means a fresh cart (convention "Isolated tests"). Browser keeps its default 10 s timeout, which absorbs the catalogue's planted 1-3 s delay; the matrix records that nothing fails because of it.

### D3. Field locators and checks

Checkout fields are scoped to `form[action="/checkout"]`, a stable-contract attribute, because `[name="email"]` alone is ambiguous. Card categories come from the card's `data-category`, which is a content attribute and not a lookup hook, so it is stable. Only the grid's container is located fragilely in the two catalogue tests, and only the displayed total in the checkout-total test: its subtotal, shipping and tax come from the summary's labelled lines. The price test compares every card's displayed price with the product's price from `GET /api/products/`, the "product's price" the clarified criterion speaks of.

### D4. The two tests broken on purpose

- **Module 4, `WEB-002_AC-12 Handpicked Highlights`.** It compares the three prices shown with the three highest prices from the API. It builds the expected list from the API's numbers (`899.0`) but reads the page's text (`$899.00`), so the lists never match. The cause is plain in the two variables at a breakpoint, `robotcode robot-debug`'s whole point, and invisible from the failure message's truncated lists alone.
- **Module 5, `WEB-002_AC-4 Rating Filter`.** It expects the checkbox "4 stars and up", while `shop/catalogue` quotes "4 stars & up". An agent limited to Tiers 1-3, with no live page, finds the mismatch by reading the spec. That is the point of shipping the specs.

Both carry the `broken` tag and fail under every preset, so the matrix lists them everywhere. Facilitators run with `--exclude broken` in Modules 7 and 8.

### D5. The one inline locator

`WEB-002_AC-10 Reset Filters` clicks the "Reset" link with a locator literal in the test body, written on the stable contract (by visible text), so it never drifts and never distracts from Module 8. It is recorded in `docs/facilitator/suite-outcomes.md` and in no participant-facing file, so that the Lab 3 skill and the Lab 7 hook have a real finding.

### D6. The matrix as data, and its verification

`docs/facilitator/suite-outcomes.toml` (TOML rather than YAML: Python's standard `tomllib` reads it, where YAML would lean on PyYAML, present only as a transitive dependency) records each test's locator kind and lists, for each of `clean`, `stage2`, `stage3`, `stage4`, `buggy` and `drift_and_bug`, the failing tests with a reason code (`broken`, `drift:<kind>` or `defect:<criterion>`). `docs/facilitator/suite-outcomes.md` explains it for facilitators and the Module 8 triage.

`tools/verify_outcomes.py` does the following for each preset:
1. apply `clean` and then the preset through the `shop` helper, in the configured space. Presets compose - `buggy` keeps the current locator stage - so each preset is measured from `clean` (found when a run of `buggy` after `stage4` failed two drift-only tests);
2. run `uv run robotcode robot` into a temporary output directory;
3. read `output.xml`;
4. compare the failing set with the data.

It prints every difference with preset, test, expected and actual, exits non-zero on any, and always resets the space at the end. Because it runs through the foundation's settings, it works against the local shop and in a shared space alike.

The healing half of `drift_and_bug` - healable tests pass, defect tests stay red - needs a model. It is verified with `--heal`, which refuses to start without the `HEAL_*` settings. Like Module 8, it runs with `--exclude broken`: the Module 5 test fails only on a locator for a label that does not exist, and a model may well heal it. `suite-outcomes.md` turns that into a triage example rather than a matrix entry, because whether it happens depends on the model.

*Alternative:* a Markdown table only. Rejected: nothing would notice the day a new image changes an outcome.

### D7. The healing profile

`robot.toml` gains `paths = ["tests"]` and:

```toml
[profiles.heal]
description = "Attach robotframework-heal: heals become proposals in results/heal/."
extend-listeners = { "Heal" = [] }
extend-env = { HEAL_FIX_TIER = "report", HEAL_HEAL_ASSERTIONS = "false", HEAL_MAX_FAILURE_SECONDS = "120" }
```

It combines as `-p heal`, `-p local -p heal` or `-p shared -p heal`; without `local` or `shared`, the settings resolve to local as before. `HEAL_HEAL_ASSERTIONS=false` is written out even though it is the default, because "a defect is never healed away" is the lesson of Module 8 and must not depend on a default. `HEAL_MAX_FAILURE_SECONDS=120` doubles heal's budget per failure: in the first healing run, one heal took 57 s and the next was abandoned at 60 s, which turned a healable test red. A room of participants sharing one endpoint will be slower still. Reports land in `results/heal/`, which is git-ignored.

### D8. `docs/conventions.md`

It states the seven conventions of `workshop/test-conventions` with one reason each, the stable-contract list from demo-webshop, and a *Known deviation* section naming `resources/legacy.resource` as the legacy locators kept for Module 8. It does not mention the inline locator (D5).

### D9. Neutral test code

Test names describe the behaviour. `legacy.resource` is documented as "legacy locators, kept deliberately; see `docs/conventions.md`". No file under `tests/` or `resources/` names a flag, a planted bug, a defect preset or the reason a test fails under one.

## Risks / Trade-offs

- [The healing run cannot be verified without an LLM endpoint] → The `--heal` verification needs the maintainer's `HEAL_*` settings. Until it runs, the healing scenario of "Healing never hides a defect" is unverified, and the task stays open rather than being ticked on the plain run.
- [heal loads the whole nearest `.env` and lets it override the environment] → For participants, `.env` holds only `SHOP_*` and `HEAL_*`. A maintainer's `.env` also holds deployment tokens, which a healing run loads into the test process. Nothing in the suite logs the environment, and `SETUP.md` gains a line on the precedence.
- [A heal can pick the wrong element] → The model chooses among live elements, and heal verifies only that its choice exists, is unique and is visible. In two healing runs, the subtotal line, which has no attribute left in stage 4, healed onto the contact block and then onto the page heading. So each test keeps a single fragile element, and one the model can recognise: the total, which healed onto its labelled row both times. Amounts are read from whatever text the healed element has, so a labelled row still yields the amount, and an unrelated block fails with "No amount in ...", a triage case in itself. The matrix records which tests fail, not how a model heals.
- [The matrix goes stale with a new shop image] → `verify_outcomes.py` is the check. `workshop-labs` runs it against the workshop tag, and `ci-and-site` can run it too.
- [The Module 5 broken test may not be solvable on Tiers 1-3] → `workshop-labs`' dry-run of Lab 5 without MCP covers it, and its swap-in rule applies.
- [Runtime orders accumulate from the checkout tests] → They are harmless and space-scoped. `verify_outcomes.py` resets the space, and so does `python -m shop reset`.
- [The matrix is public] → It is facilitator material in a public repository, as the master document intends. Neutrality keeps participant-facing context from advertising answers; it is not secrecy.

## Migration Plan

This change adds files only. `robot.toml` gains `paths` and a profile; nothing existing changes behaviour.

## Open Questions

- **How Module 8 participants get a model** - a facilitator-provided capped key, their own, a local model, or the agentic path only - is decided in `workshop-labs`. The suite behaves identically in every case.
