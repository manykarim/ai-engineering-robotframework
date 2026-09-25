# Lab 8 - the recorded healing report

For participants without a healing model. This is the healing run of Lab 8, step 3, recorded during the rehearsal:
the shipped suite, unchanged, with the shop in `drift_and_bug` and the `heal` profile on.

```bash
uv run --no-sync python -m shop preset drift_and_bug
uv run robotcode -p heal robot --exclude broken
```

The model was an OpenAI-compatible model with a spending cap. It made 5 heals and used about 17,000 tokens. Another
model, or another run, may choose different locators; which tests pass and fail stays the same.

## The result

11 tests ran: **9 passed, 2 failed.** Without healing, the same preset failed 4 of them.

## The heals

Each heal is a proposal: the listener found the element with a new locator, reran the keyword with it, and recorded
the change. No file was changed.

| # | Test | Keyword, in `resources/legacy.resource` | Old locator | New locator | Afterwards |
|---|---|---|---|---|---|
| 1 | `WEB-002_AC-1 Card Prices Are The Product Prices` | `Get Element`, in `Get Product Grid` | `section:has(h2:text-is("All products")):not(:has(section)) >> .product-grid` | `css=.catalog-content .tile-rack` | the step passed |
| 2 | `WEB-006_AC-1 Order Total Adds Up` | `Get Text`, in `Get Order Total` | `[data-test="checkout-total"]` | `css=div.payment-totals__total` | the step passed and read "Total due at payment $249.99" |
| 3 | `WEB-006_AC-7 Successful Order` | `Fill Text`, in `Fill Checkout Form By Field Ids` | `id=checkout-email` | `css=input#payment-email` | the step passed |
| 4 | `WEB-006_AC-7 Successful Order` | `Fill Text`, in `Fill Checkout Form By Field Ids` | `id=checkout-name` | `css=input#payment-name` | the step passed |
| 5 | `WEB-006_AC-7 Successful Order` | `Fill Text`, in `Fill Checkout Form By Field Ids` | `id=checkout-address` | `css=textarea#payment-address` | the step passed |

`WEB-002_AC-7 Audio Filter Shows Only Audio` passed without a heal of its own: it uses the same grid locator as heal 1,
and the listener reused that repair. Its log says *"proactively replaced known-broken locator"*.

## Still red with healing on

| Test | Failure |
|---|---|
| `WEB-002_AC-1 Card Prices Are The Product Prices` | `Cascade Water Bottle should cost $79.00.: $90.85 != $79.00` |
| `WEB-006_AC-1 Order Total Adds Up` | `The order total should be subtotal plus shipping plus tax.: 249.99 != 267.49` |

## Your triage

Copy this table and fill it in, as Lab 8's step 4 describes. For each heal: is the new locator the element the step
meant, and will it survive the next redesign? Then, for each test still red: did its heal work, and why does it
still fail?

| Heal | Verdict: accept, reject or investigate | Why |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |
