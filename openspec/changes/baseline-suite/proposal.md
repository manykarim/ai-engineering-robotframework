## Why

The whole workshop day runs on one shipped test suite and a preset dial:

- M0: the suite runs once and some tests fail on purpose.
- M4: a pre-broken test is step-debugged.
- M7: the `buggy` preset turns up real failures to file as issues.
- M8: the `drift_and_bug` preset shows healable drift being healed while two genuine regressions stay red.
- M9: a pushed break is explained in CI.

That only works if the suite's imperfections are designed, documented and deterministic. It also has to cover catalogue prices (WEB-002) and the checkout total (WEB-006), because those are exactly what `drift_and_bug` breaks. If that coverage depended on which story a participant picked in Module 5, M7 and M8 would only land for part of the room.

## What Changes

- **`tests/ui/`** covering selected WEB-002 and WEB-006 criteria, and **`tests/api/`** with a minimal smoke. The minimal smoke is the target of the Lab 2 nested-`AGENTS.md` stretch. It deliberately does *not* cover API-005, which stays the Module 5 stretch goal.
- **`resources/`**: shared keywords that implement the `SHOP_URL`/`SHOP_SPACE` contract from `workshop-foundation`. Every browser context sends `X-Workshop-Space` when a space is set. Presets are applied outside the suite, so the same suite runs unchanged under any preset.
- **Designed imperfections, each documented with its purpose:**
  - two tests tagged `broken`, with distinct causes: one for Module 4's step-debugging, one for Module 5's conversational debugging;
  - a deliberate mix of drift-fragile locators and drift-robust ones. The fragile ones are stage-1 ids, classes and `data-test` hooks, each breaking in a different set of stages, and are Module 8's healing targets. The robust ones use visible text, roles and labels, and are the Lab 3 lesson;
  - exactly one inline-locator convention violation, the target of the Lab 3 skill and the Lab 7 hook. It is recorded for facilitators only, so participants have something real to find.
- **An expected-outcome matrix.** For each preset (`clean`, `stage2`-`stage4`, `buggy`, `drift_and_bug`) it lists which tests fail and why. It is kept as data, with a script that runs the suite under every preset against the pinned image and reports any difference, so the matrix stays true when the image changes. Facilitators use it, and so does the Module 8 heal triage (accept, reject or investigate) and CI. Under `drift_and_bug`, the WEB-002 price and WEB-006 total failures stay red however the locators heal.
- **Healing wiring**: a `heal` profile that attaches `robotframework-heal` as a listener to the unmodified suite, at `HEAL_FIX_TIER=report` and with assertion healing off, so every heal is a proposal and never a silent edit, and a planted bug can never be healed away.
- **The spike is answered: healing needs a model.** Run against stages 1-4 with no `HEAL_*` settings, `robotframework-heal` 0.4.0 attached, recorded every failure, and healed none: *"Healing skipped: No model configured for role 'locator'"*. Even classifying a failure needs the model. Module 8's listener path therefore needs an LLM endpoint; how participants get one is decided in `workshop-labs`. The spike also showed that `--listener Heal` works without touching a suite, and that `[name="email"]` alone is ambiguous: the sign-in dialog has one too.
- **`docs/conventions.md`**: the conventions the suite follows, and the legacy locators it keeps deliberately as Module 8's healing targets. The `AGENTS.md` from Lab 2 references it, and the Lab 3 skill enforces it.

## Capabilities

### New Capabilities
- `workshop/baseline-suite`: the shipped suite, its coverage, its designed imperfections, the preset-outcome matrix and the healing profile.
- `workshop/test-conventions`: the documented conventions the suite and the labs rely on.

### Modified Capabilities
None.

## Impact

- **New files**: `tests/ui/`, `tests/api/`, `resources/`, `docs/conventions.md`, `docs/facilitator/suite-outcomes.yaml` and `.md` (the matrix, in the facilitator folder `workshop-labs` fills), `tools/verify_outcomes.py`, and the `paths` setting and `heal` profile in `robot.toml`.
- **Depends on** `workshop-foundation` (profiles, shop contract, pinned stack) and `shop-specs` (the requirements the tests verify).
- **Consumed by** every lab from M0 to M9, and by `ci-and-site`.
- **Not in scope**: the participants' own Module 5 tests, lab instructions, skills, hooks and workflows.
