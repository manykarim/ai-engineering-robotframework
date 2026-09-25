# Lab 8 - Healing

The shop's layout drifts under the tests. A healing listener repairs broken locators while the suite runs, and
records every repair as a proposal. Your job is the part no listener can do: decide, heal by heal, whether to trust
it.

| | |
|---|---|
| Module | 8 - Self-Healing Tests |
| Time | 12 minutes |
| Shop preset | `drift_and_bug`, applied in step 1 and reset in step 6 |
| You need | Lab 0 done. A healing model in `.env` if you have one ([SETUP.md](../../SETUP.md#healing-api-key)); without one, step 3 shows the other path |
| You start from | Your repository after the earlier labs, or `main` |

## Steps

1. **Let the layout drift:**

   ```bash
   uv run --no-sync python -m shop preset drift_and_bug
   ```

2. **Run the suite as it is**, without healing, and see what breaks:

   | Local shop | Shared instance |
   |---|---|
   | `uv run robotcode robot --exclude broken` | `uv run robotcode -p shared robot --exclude broken` |

   `uv run robotcode results show --failed` lists the failures. Their messages are mostly about elements that
   cannot be found.

3. **Run it again with healing.**

   - *With a healing model*, add the `heal` profile. It attaches the listener to the unchanged suite:

     | Local shop | Shared instance |
     |---|---|
     | `uv run robotcode -p heal robot --exclude broken` | `uv run robotcode -p shared -p heal robot --exclude broken` |

     The report is `results/heal/heal_report.html`. Open it in your browser. Every heal is a proposal: the old
     locator, the new one, and whether the step then passed. Your test files are not changed.

   - *Without a healing model*, use [the recorded healing report](../../transcripts/lab-08-healing/README.md) of the
     same preset. It lists the same information.

4. **Triage every heal.** For each one, decide, and write down why:

   - **accept**: the new locator finds the element the test meant, and the test is right to pass;
   - **reject**: it finds a different element, or makes a test pass that should not;
   - **investigate**: you cannot tell from the report.

   Ask of each: Is it the element the step meant? Is the new locator one that will drift again, like a new class
   name, or does it use the stable contract? `docs/conventions.md` says what that is.

5. **Look at what stayed red.** Some tests still fail with healing on. For each: did the heal work, and does the
   test now fail for another reason? The profile never heals an assertion, so an expected value that does not match
   stays red. Is that a broken locator, or a defect of the shop?

6. **Put the shop back:**

   ```bash
   uv run --no-sync python -m shop reset
   ```

## Stretch

The other way to heal: repair the test itself, with your agent. Apply `drift_and_bug` again, then:

> The test "WEB-006_AC-7 Successful Order" fails under the current shop layout. Use the RobotCode debugger and the
> robotframework MCP server to find which locator drifted, and repair its keyword onto the stable contract of
> docs/conventions.md, so that it works in every layout. Show me the change before you make it.

Run the test under `drift_and_bug` and under `clean`: it should pass in both. Reset the shop when you are done.

## If your agent fails

Steps 1 to 6 need no agent. For the stretch goal, follow
[the recorded walkthrough of this lab](../../transcripts/lab-08-healing.md).
