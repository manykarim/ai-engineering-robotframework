## Why

Module 5's payoff lab asks an agent to turn a user story into a green suite on Tiers 1-3 alone, without any live view of the page. The master document names this as the day's riskiest lab. Today the shop's behaviour is only described in demo-webshop's story files, and most of those do not ship to participants. Its conformance record must not be copied at all, per the demo-webshop handoff. Agents writing tests here would be guessing. Specs derived from the stories give them structured, neutral reference context: what the shop does, in the shop's own visible terms.

## What Changes

- `openspec/specs/shop/*`: one capability spec per area of the shop that the workshop day touches, derived from the demo-webshop stories at tag `v0.3.0` (commit `6342d4b`), where both conformance legs verified all 95 criteria:
  - catalogue (WEB-002), product detail (WEB-003), search (WEB-004)
  - cart (WEB-005 and API-005), checkout (WEB-006), authentication (WEB-007)
- **The interpretation rules travel with the specs.** The story README makes its rules binding for downstream conversion: quoted UI text means an element's *visible* text, matched as a phrase regardless of case and whitespace runs; accessible names count only where a criterion speaks of a label or name. These rules decide whether an agent's locator is right, so they become a capability of their own.
- **Traceable to the source.** Each requirement names the acceptance criteria it derives from (for example `WEB-004_AC-3`), and the design records the demo-webshop tag and story commit used. A shop release with changed stories becomes a new change here, never a silent edit.
- **Neutral by rule.** The behaviour specs describe *correct* behaviour only. They never name a feature flag, a locator stage, a planted bug, a locator (ids, classes, `data-test` hooks) or the purpose of a check. The Module 7 bug hunt only works if participants are not told which behaviours break. Visible text and accessible names are allowed: they are the shop's stable contract across every stage, and exactly what good tests should use. The rule holds for every `shop/*` spec without exception, which is why the shop's workshop controls - spaces, presets, reset - are not specified here: participants reach them through the `shop` helper, already specified in `workshop/shop-access`, and the controls necessarily name the locator stages.
- **Not copied from demo-webshop**: `CONFORMANCE.md`, `backend/tests/conformance/`, story revision history, withdrawn criteria. The story files for the Module 5 lab are copied by `workshop-labs`, not here.
- API-006 (checkout API) and API-007 (login API) are out of scope: nothing on the day uses them.

## Capabilities

### New Capabilities
- `shop/catalogue`: browsing, filtering and resetting the product grid.
- `shop/product-detail`: the product page, its related products and the not-found page.
- `shop/search`: search input, suggestions, results and clearing.
- `shop/cart`: cart contents in the UI and through the cart API.
- `shop/checkout`: the checkout form, validation, order confirmation and order documents.
- `shop/authentication`: signing in with a demo account and signing out.
- `shop/interpretation-rules`: how every `shop/*` requirement is read and checked - visible text, accessible names, error messages, examples - and how each requirement traces to its criterion.

### Modified Capabilities
None.

## Impact

- **New files**: `openspec/specs/shop/**/spec.md` through this change's delta specs, synced on archive.
- **Depends on** `workshop-foundation`, whose `openspec/config.yaml` defines the `shop/*` namespace and carries the neutrality rule as an artifact rule. Also depends on the demo-webshop handoff issue (its `workshop-rollout` task 5.3), which names the story path, corrections and withdrawn IDs.
- **Consumed by** `baseline-suite` (its tests verify these requirements), `workshop-labs` (the `AGENTS.md` participants write in Lab 2 points agents here) and every participant agent in Module 5.
- **Not in scope**: any test, story file copy or lab text.
