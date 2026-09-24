## Context

See `proposal.md` for the motivation. The source is demo-webshop tag `v0.3.0`, commit `6342d4b`. That commit's `main` run (`35862997690`) passed both conformance legs with `95 criteria: 95 pass, 0 fail, 0 error`, so every criterion in the story set holds for the image `0.3.0` in its clean state. Seven stories are in scope: WEB-002 to WEB-007 and API-005, **71 active criteria**. API-006 and API-007 are out of scope.

The story README sets two constraints that shape this design:

- **Binding interpretation rules** for downstream conversion: visible text, accessible names, error messages, non-normative examples.
- **A no-copy rule**: `CONFORMANCE.md` and the conformance tests are facilitator material.

The story files also carry a reason-writing rule, which the neutrality rule here extends from revision reasons to requirements.

## Goals / Non-Goals

**Goals:**
- An agent that reads `shop/*` can write a correct test for any in-scope criterion without seeing the live page. The spec supplies what the shop does and which visible texts and values prove it; locating the elements remains the agent's job.
- Every requirement traces to exactly one criterion, so a participant can scope a lab slice as "WEB-004_AC-1 to AC-3" and find it in the spec.
- The specs promise exactly what the criteria promise, and so inherit the conformance guarantee rather than asserting anything unverified.

**Non-Goals:**
- Specifying the workshop controls (spaces, presets, reset). Those are participant-side contracts in `workshop/shop-access`.
- Copying story files. The Module 5 lab copies its four stories in `workshop-labs`.
- Describing any page not covered by a criterion, such as the home page beyond its search form, the AI helper, or the order history page.

## Decisions

### D1. One requirement per active criterion

Each requirement is named `<Title> (<STORY>_<AC>)`. Its text restates that one criterion; its scenarios instantiate it. That gives 13 + 9 + 8 + 20 + 11 + 10 = **71 behaviour requirements**, plus the interpretation rules.

*Alternative:* grouping criteria into fewer, broader requirements, for example one "filters" requirement. It reads better but breaks the one-to-one trace that lab slices, test names and the coverage check all rely on.

### D2. The cart capability joins two stories

WEB-005 (the shopper's cart on the pages) and API-005 (the cart API) describe one cart. They share `shop/cart`, keeping their own criterion IDs. WEB-005_AC-10 and API-005_AC-9/10 overlap on session identification; both are kept, because each is a separate criterion with its own ID.

### D3. What counts as normative

The README's rules are followed literally:

- **Criteria are normative.** A test-data table counts only where a criterion refers to what it defines: the demo credentials (WEB-007_AC-4), the primary product and its rating (WEB-003_AC-2), the order number pattern (WEB-006_AC-7), and the edge-case IDs of an invalid product (WEB-003_AC-9).
- **Everything else is non-normative:** `e.g.` values, "or equivalent", example requests and responses, and every Notes section. Such values may appear in a scenario as a concrete instance that satisfies the criterion, never as the requirement itself.

### D4. Where a table contradicts its criterion, the criterion wins

Two contradictions exist in the source, and both are resolved in favour of the criterion:

| Story | Table says | Criterion says, and the spec follows |
|---|---|---|
| WEB-004 | `/api/search` takes `q` | `GET /api/search/` reads `query` (AC-9, the replacement for withdrawn AC-4) |
| WEB-005 | a `session_id` cookie identifies the API cart, "header wins" | the API reads only `X-Session-ID`; without it the session is `workshop-demo`, **even when a `session_id` cookie is sent**. On the pages, the cookie identifies the cart (AC-10) |

A converter that trusted either table would write a test that is wrong in the clean state, which is why these two cases are recorded here.

### D5. Neutral by construction

No requirement names a feature flag, a locator stage, a planted bug or a locator, or says why a check exists. Visible texts and accessible names are kept, because they are the shop's contract in every stage. One criterion needs care: WEB-003_AC-3 says the button "contains data attributes identifying the product (e.g., `data-product-id`)". The attribute name is an `e.g.` and therefore non-normative (D3), and it is a locator (D5). The requirement keeps the normative content - the button identifies the product it adds, and activating it adds that product - without naming the attribute.

### D6. Nothing beyond the criteria

A requirement never adds behaviour its criterion does not state, even behaviour that is true and tested elsewhere, such as the HTTP status of the not-found page or the tax rate. Only the criteria are covered by the conformance legs. Anything more would be a claim this repository cannot keep in step with the shop.

### D7. The interpretation rules as a capability

The README's rules - visible text versus accessible names, what counts as an error message, non-normative examples - plus the clean-state premise and the trace rule become `shop/interpretation-rules`. Its scenarios are the README's own examples: "Add to Cart" matches "Add to cart", "Tax" matches "Estimated tax", "Logout" does not match "Log out". Keeping the rules out of the six behaviour specs avoids six copies, and gives an agent one place to read how any of them is checked.

## Risks / Trade-offs

- [The workshop tag changes a story after `v0.3.0`, for example through the maintainer's decision-record review] → The workshop tag must be diffed against `v0.3.0` under `docs/user-stories/`. Any criterion change becomes a new change against these specs, never a silent edit. `workshop-labs`, whose dry-runs run against the workshop tag, owns the diff.
- [71 requirements are a lot of context] → Agents are pointed at `shop/*` capability by capability, not at the whole set. The Lab 2 `AGENTS.md` names the spec for the story being worked on, which is the context-economics point of Module 2.
- [A transcription error in a spec] → The coverage check maps every active criterion to exactly one requirement. A spot-check runs at least one scenario per capability against a `0.3.0` container.
- [Neutral wording can still leak intent] → A scan rejects the vocabulary that would leak it, such as `BUG_`, `LOCATOR_`, `stage`, `planted`, `data-`, `css` and `xpath`.

## Migration Plan

This is a spec-only change: nothing to deploy. Archiving syncs the seven delta specs into `openspec/specs/shop/`.
