# Lab 9 - CI: the recorded walkthrough

*Recorded on 2026-09-26 in the workshop's own repository, following the lab's steps. The pull request came from a
branch of that repository instead of a fork; nothing else differs on a fork. Lab 9 needs no agent of your own, so
this transcript shows what the workflows produced. Results are shortened.*

## Step 1 - Enable Actions

Actions were already on in the workshop's repository. **The participant runs** `gh workflow list`:

```
Agent triage        active  367670936
Documentation site  active  367596625
Heal suggestions    active  367670939
Run tests           active  367596265
```

*Documentation site* is the fourth workflow the lab mentions. It runs only in the workshop's repository; on a fork,
it is skipped.

## Step 2 - The credential

The rehearsal started without any triage secret, to see what everyone gets. It added the `TRIAGE_*` secrets later,
in step 6.

## Step 3 - Break something

The rehearsal changed the expected status of `Health Reports Ok` in `tests/api/smoke.robot`:

```diff
 Health Reports Ok
     ${health}=    Get Shop Health
-    Should Be Equal    ${health}[status]    ok
+    Should Be Equal    ${health}[status]    okay
```

**The participant runs:**

```bash
git switch -c lab-09-break
git commit -am "Break a test on purpose"
git push -u origin lab-09-break
```

*Run tests* starts on the push and fails.

## Step 4 - Open a pull request

The rehearsal gave the pull request its own title and description instead of `--fill`, saying that it would be
closed, not merged. `gh pr create` answers with the pull request's address:

```
https://github.com/manykarim/ai-engineering-robotframework/pull/15
```

## Step 5 - Watch the checks

**The participant runs** `gh pr checks 15 --watch`. When they have finished:

```
Robot Framework suite  fail      54s   .../actions/runs/36241546620/job/108402894910
Robot Framework suite  fail      58s   .../actions/runs/36241548712/job/108402900459
Deploy to GitHub Pages skipping  0     .../actions/runs/36241548736/job/108403072416
Build the site         pass      1m8s  .../actions/runs/36241548736/job/108402900537
```

*Run tests* failed twice, once for the push and once for the pull request. The site's checks appear only in the
workshop's repository. *Agent triage* is no check of the pull request: it starts when *Run tests* has failed and
answers with a comment.

## Step 6 - Read the comment

**The participant runs** `gh pr view 15 --comments`. Without a credential, the comment lists the failed test and
names the secrets that would add an analysis:

> ### Test results: 10 passed, 1 failed
>
> | Test | Where | Message |
> |---|---|---|
> | Health Reports Ok | `smoke.robot:12` | ok != okay |
>
> *No analysis.* Add a Claude credential (`ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN`), or the `TRIAGE_MODEL`, `TRIAGE_BASE_URL` and `TRIAGE_API_KEY` secrets of any OpenAI-compatible endpoint, to get a root-cause analysis here. `SETUP.md` explains both; set a spending cap first.

Then the rehearsal set the three `TRIAGE_*` secrets for the maintainer's OpenAI-compatible endpoint (each
`gh secret set` asks for its value), with the model MiniMax-M3, and pushed a second break: the catalogue's expected
length changed from 12 to 13. *Run tests* failed again, and *Agent triage* **updated the same comment**; the pull
request still had one comment from `github-actions[bot]`:

> ### Test results: 9 passed, 2 failed
>
> | Test | Where | Message |
> |---|---|---|
> | Health Reports Ok | `smoke.robot:12` | ok != okay |
> | Catalogue Lists Twelve Products | `smoke.robot:16` | Length of '[{'id': 5, 'name': 'Atlas Standing Desk', 'sku': 'ATL-DSK-005', 'price': 799.0, 'description': 'Programmable standing desk with posture coa ... : '/static/img/velocity-backpack.jpg', 'category': 'Travel', 'inventory': 110, 'rating': 4.4, 'review_count': 205}]' should be 13 but is 12. |
>
> ### Root cause
>
> Triage Report
>
> ### 1. Health Reports Ok
> **Cause:** `tests/api/smoke.robot` line 14 was changed to expect `okay` instead of `ok`.
>
> **Evidence:** Failure message `ok != okay` — the API still returns the string `"ok"`, but the assertion now compares it against `"okay"`.
>
> **Fix:** Either update the health endpoint to return `"okay"` (likely in the shop service's health handler) so the API matches the new expectation, or revert the test back to `ok` if the API contract shouldn't change. The latter is more likely correct unless the response string was intentionally reworded elsewhere in the change.
>
> ### 2. Catalogue Lists Twelve Products
> **Cause:** `tests/api/smoke.robot` line 18 was changed from `12` to `13`.
>
> **Evidence:** The Robot Framework message states the list length `"should be 13 but is 12"`. The response payload shown contains exactly 12 product dictionaries, so the catalogue endpoint still returns 12 items.
>
> **Fix:** Add the missing 13th product to the catalogue seed/fixture (and to any static catalogue served by the shop API), or revert the expected length to `12` if the test was bumped prematurely. A new fixture entry matching the existing schema (`id`, `name`, `sku`, `price`, …) is needed.
>
> ### Other diff hunks
> The changes in `openspec/changes/ci-and-site/tasks.md` (checkbox ticks) and `tools/triage.py` (thinking-block stripping, longer message rendering) are unrelated to these two failures — they don't touch the API response or the catalogue data.
>
> **Summary:** Both failures are direct consequences of the test-side expectations in `smoke.robot` being raised without the corresponding API/data changes landing.
>
> ---
> <sub>Triage by one call to MiniMax-M3 through an OpenAI-compatible endpoint. A model drafted this; check it before you act on it.</sub>

The rehearsal branch also carried two fixes to `tools/triage.py` that the rehearsal itself had found, which the
comment rightly calls unrelated. Your comment will not mention them.

The lab's questions, answered for this comment:
- **Does the root cause match what was broken?** Yes, for both tests, with the right lines of `smoke.robot`.
- **What evidence does it give?** The failure messages and the diff's hunks.
- **Would you trust it on a change you had not made?** Each *Fix* offers two ways out: change the test back, or
  change the shop to match the test. Only someone who knows why the test changed can choose. Here the test was
  wrong, and following the first suggestion would have meant changing a working shop.

The Claude tier was not recorded: no Claude credential was set. With one, the Claude Code Action writes the
*Root cause*, and the comment's last line names it.

## Step 7 - Close the pull request

**The participant runs** `gh pr close lab-09-break`:

```
✓ Closed pull request manykarim/ai-engineering-robotframework#15 (Lab 9 rehearsal: a break on purpose)
```

## Stretch - Heal suggestions

Without the `HEAL_*` secrets, *Run workflow* on *Heal suggestions* ends successfully with the notice *No healing
model configured*, and nothing changes.

With the healing model's three secrets set, **the participant runs**
`gh workflow run heal-suggestions.yml -f preset=stage4`. The run drifts the shop, runs the suite with healing, and
reports in its summary:

```
Heals against `stage4`
- healed: 5, unhealed: 0, tokens: 11984
```

The repository does not let GitHub Actions open pull requests, which is also how every fork starts. The run's last
step therefore pushed the heals to a branch and left a notice:

```
Open the pull request yourself
https://github.com/manykarim/ai-engineering-robotframework/pull/new/heal-suggestions/36241288079
```

The branch changes five lines of `resources/legacy.resource`, and nothing else:

```diff
-    ${grid}=    Get Element    ${GRID} >> .product-grid
+    ${grid}=    Get Element    css=section:has(h2:text-is("All products")) >> .tile-rack
-    ${text}=    Get Text    [data-test="checkout-total"]
+    ${text}=    Get Text    css=div.payment-totals__total
-    Fill Text    id=checkout-email    ${email}
-    Fill Text    id=checkout-name    ${full_name}
-    Fill Text    id=checkout-address    ${address}
+    Fill Text    css=input#payment-email    ${email}
+    Fill Text    css=input#payment-name    ${full_name}
+    Fill Text    css=textarea#payment-address    ${address}
```

Review it as you triaged heals in Lab 8. The first line no longer uses the keyword's `${GRID}` variable, and a run
before this one proposed a different locator for the same line: heals are suggestions, not answers. The rehearsal
merged nothing and deleted the branch.
