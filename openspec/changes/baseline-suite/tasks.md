## 1. Wiring

- [ ] 1.1 Add `paths = ["tests"]` and the `heal` profile to `robot.toml` (design D7). Verify:
  - `uv run robotcode profiles list` shows `local`, `shared` and `heal`;
  - `uv run robotcode -p shared -p heal config show` contains both the heal listener and `SHOP_PROFILE=shared`;
  - `uv run robotcode -p heal config show` sets `HEAL_FIX_TIER=report` and `HEAL_HEAL_ASSERTIONS=false`.
- [ ] 1.2 Write `resources/` per design D2: `shop.resource`, `api.resource`, `catalogue.resource`, `checkout.resource` and `legacy.resource`. Verify:
  - `uv run robotcode analyze code resources` reports no errors;
  - opening a page through `shop.resource` with the shared profile in a throwaway space shows that space in the page's `data-workshop-space`;
  - a scan of `catalogue.resource`, `checkout.resource`, `shop.resource` and `api.resource` finds no `id=`, `#`, `.class`, `data-test` or `xpath` locator. Those appear only in `legacy.resource`.

## 2. Tests

- [ ] 2.1 Write `tests/ui/catalogue.robot` with the seven tests of design D1, including the two tests broken on purpose (D4) and the one inline locator (D5). Verify:
  - after `python -m shop reset`, `uv run robotcode robot --exclude broken tests/ui/catalogue.robot` passes locally;
  - with `--include broken`, exactly the two D4 tests run and fail;
  - under `robotcode robot-debug`, a breakpoint in `WEB-002_AC-12` shows the API's `899.0` beside the page's `$899.00`;
  - the `WEB-002_AC-4` failure message contains "4 stars and up".
- [ ] 2.2 Write `tests/ui/checkout.robot` with the four tests of design D1. Verify: after a reset, the file passes locally, and each test starts with an empty cart. Running the file twice in a row passes both times.
- [ ] 2.3 Write `tests/api/smoke.robot` with the two smoke tests of design D1. Verify: it passes against the local shop and in a shared space, and no file under `tests/api/` or `resources/api.resource` refers to `/api/cart`.
- [ ] 2.4 Check the suite against its own conventions. Verify:
  - every test name starts with `<STORY>_<AC>` or the test carries `smoke`;
  - every test carries a story or `smoke` tag and exactly one of `ui` or `api`;
  - exactly two tests carry `broken`;
  - exactly one locator literal occurs in `tests/`, the D5 one;
  - searching `tests/` and `resources/` for `BUG_`, `LOCATOR_`, `buggy` and `drift_and_bug` finds nothing.

## 3. Conventions document

- [ ] 3.1 Write `docs/conventions.md` per design D8. Verify: it states the seven conventions of `workshop/test-conventions`, each with a reason; it names `resources/legacy.resource` as the known deviation; it does not mention the inline locator; and every example locator in it follows its own rules.

## 4. The expected-outcome matrix

- [ ] 4.1 Write `docs/facilitator/suite-outcomes.yaml` and `suite-outcomes.md` per design D6, derived from the D1 inventory and the drift and defect tables before anything is run. Verify: every test of the suite appears in the data, every reason uses the vocabulary `broken`, `drift:<kind>` or `defect:<criterion>`, and the Markdown names the D5 inline locator.
- [ ] 4.2 Write `tools/verify_outcomes.py` per design D6. Verify:
  - run against the local `0.3.0` shop, it applies all six presets and reports no difference;
  - on a copy of the data with one expected outcome changed, it names that test and preset and exits non-zero;
  - afterwards the space status names `clean`.
- [ ] 4.3 Verify the matrix on the shared instance. Verify: `verify_outcomes.py` with the shared profile in a throwaway space reports no difference, the space reads `clean` afterwards, and the status of `default` is unchanged.

## 5. Healing

- [ ] 5.1 Check the healing profile without a model. Verify:
  - under `stage4`, `uv run robotcode -p heal robot` produces the same passed and failed tests as a plain run;
  - `results/heal/summary.json` records every failure as suppressed, with the reason that no model is configured;
  - `git status -- tests resources` is clean.
- [ ] 5.2 Check the healing profile with a model, which needs the maintainer's `HEAL_*` settings. Verify:
  - `verify_outcomes.py --heal` under `drift_and_bug` shows `WEB-002_AC-7 Audio Filter Shows Only Audio` and `WEB-006_AC-7 Successful Order` passing through healed locators;
  - `WEB-002_AC-1 Card Prices Are The Product Prices` and `WEB-006_AC-1 Order Total Adds Up` fail on their expected values;
  - `heal_report.html` lists each heal as a proposal;
  - `tests/` and `resources/` are unchanged;
  - the model and the tokens used are recorded in the pull request.
- [ ] 5.3 Add the precedence note to the "Healing API key" section of `SETUP.md`: `robotframework-heal` loads the nearest `.env` itself and lets it override the environment for its settings, the opposite of `SHOP_*`. Verify: the note is present, and every `setup-check` guide reference still resolves.

## 6. Close-out

- [ ] 6.1 Validate and archive. Verify: `openspec validate baseline-suite --strict` passes. After the merge, `openspec archive baseline-suite -y` creates `openspec/specs/workshop/baseline-suite` and `workshop/test-conventions`, each with its Purpose.
