# Lab 8 - Healing: the reference

[Lab 8](../labs/lab-08-healing/INSTRUCTIONS.md) drifts the shop, runs the suite with `robotframework-heal`, and has
you triage every heal. Its stretch goal repairs a test with your agent instead. [Transcript](../transcripts/lab-08-healing.md),
and the [recorded healing report](../transcripts/lab-08-healing-report.md) for runs without a model.

## The triage

Under `drift_and_bug`, four tests failed without healing. With it:

| Test | Heal | Verdict |
|---|---|---|
| `WEB-002_AC-7 Audio Filter Shows Only Audio` | the grid's class, reused from the card-price heal | **accept**: pure drift, and the test passes |
| `WEB-006_AC-7 Successful Order` | three form-field ids, replaced | **accept**: pure drift, and the test passes |
| `WEB-002_AC-1 Card Prices Are The Product Prices` | the grid's class, replaced | **the locator is fixed, the test is not**: it still fails on the prices of products 3, 6, 9 and 12, a real defect |
| `WEB-006_AC-1 Order Total Adds Up` | the total's `data-test` hook, replaced | **the locator is fixed, the test is not**: the total still omits tax, a real defect |

## Why these verdicts

- **Healing repairs locators, never assertions.** The profile sets `HEAL_HEAL_ASSERTIONS=false`, so a defect stays
  red with healing on.
- **A heal is a proposal.** heal accepts a locator that matches exactly one element. Whether it is the element the
  test meant is your call. In the facilitators' runs, the total healed onto its whole row, `css=div.payment-totals__total`:
  it works, and it is a new class that will drift again.

## The stretch goal

```diff
--- a/tests/ui/checkout.robot
+++ b/tests/ui/checkout.robot
@@ -26,7 +26,7 @@ WEB-006_AC-1 Order Total Adds Up
 
 WEB-006_AC-7 Successful Order
     [Documentation]    A valid order shows a confirmation with an order number ORD- plus 8 hex characters.
-    Fill Checkout Form By Field Ids    test@example.com    Test User    123 Test Street, City
+    Fill Checkout Form    test@example.com    Test User    123 Test Street, City
     Place Order
     ${message}=    Get Order Confirmation
     ${numbers}=    Get Regexp Matches    ${message}    \\bORD-[0-9A-F]{8}\\b
```

The test now fills the form through `Fill Checkout Form`, which finds the fields by their labels, the stable
contract, instead of the field ids of `resources/legacy.resource`. It passes under `drift_and_bug` and under `clean`.

## What to debrief

- **A heal that hides a broken test.** With the broken tests included, `WEB-002_AC-4 Rating Filter` can pass: heal
  proposes `css=input[name="rating"]` for a label that does not exist, and the test no longer checks the label the
  criterion names. The verdict is reject.

## Compare yours

```bash
git fetch upstream solutions
REF=$(git log -1 --format=%H --grep '^lab-08-healing' upstream/solutions)
git diff "$REF" -- tests/ui/checkout.robot
```

The lines marked `-` are the reference's, the lines marked `+` yours. No `upstream` remote yet? [Add it first](README.md#compare-your-files-with-the-reference).
