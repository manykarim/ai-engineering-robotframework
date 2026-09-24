<!--
  Maintainers: this lab uses the workflows run-tests.yml, agent-triage.yml and heal-suggestions.yml, which arrive
  with the OpenSpec change ci-and-site. Until that change is applied, this lab cannot run, and its walkthrough is
  recorded there.
-->

# Lab 9 - CI

Put an agent where it helps most and risks least: in CI, explaining failures. Push a change that breaks a test,
open a pull request on your fork, and watch an agent explain your mistake in public. You keep the merge button.

| | |
|---|---|
| Module | 9 - CI & Toolchain Integration |
| Time | 15 minutes |
| Shop preset | `clean`: CI starts its own shop from the pinned image, whatever your local shop does |
| You need | Lab 0 done: your fork, and `gh auth status` signed in |
| You start from | Your fork, with your work of the day committed |

## Steps

1. **Enable Actions** on your fork: open its *Actions* tab on GitHub and confirm that you want to run its workflows.
   Three are provided in `.github/workflows/`:

   | Workflow | Runs | Does |
   |---|---|---|
   | `run-tests.yml` | on every push and pull request | runs the suite against the pinned shop and uploads the results |
   | `agent-triage.yml` | when a pull request's tests fail | posts a root-cause comment, written by an agent from `robotcode results` |
   | `heal-suggestions.yml` | when you start it | turns heals into a suggestion pull request (the stretch goal) |

2. **Optionally give the triage agent a key.** The header of `.github/workflows/agent-triage.yml` names the secret
   it reads. **Set a spending cap on the key first**, then:

   ```bash
   gh secret set <SECRET_NAME> --repo <your-handle>/ai-engineering-robotframework
   ```

   Without a key, the lab still works: the comment then holds the `robotcode results` summary, without the agent's
   analysis.

3. **Make a branch and break something.** For example, change an expected value in a test you wrote today, or in
   `tests/api/smoke.robot`. Commit it yourself, in the terminal:

   ```bash
   git switch -c lab-09-break
   git commit -am "Break a test on purpose"
   git push -u origin lab-09-break
   ```

4. **Open a pull request** on your fork, not on the workshop's repository:

   ```bash
   gh pr create --repo <your-handle>/ai-engineering-robotframework --base main --head lab-09-break --fill
   ```

5. **Watch the checks** until they finish:

   ```bash
   gh pr checks --repo <your-handle>/ai-engineering-robotframework --watch
   ```

6. **Read the comment:**

   ```bash
   gh pr view --repo <your-handle>/ai-engineering-robotframework --comments
   ```

   Does the root cause it names match what you broke? What evidence does it give? Would you trust it on a change
   you had not made yourself?

7. **Close the pull request** without merging:

   ```bash
   gh pr close --repo <your-handle>/ai-engineering-robotframework lab-09-break
   ```

## Stretch

Start the heal-suggestion workflow from the *Actions* tab (*Run workflow*). It runs the suite against a drifted shop
with healing on, and opens a pull request that proposes the heals as changes. Review it the way you triaged heals in
Lab 8: merge nothing you would reject.

## If your agent fails

This lab needs no agent of your own: the agent runs in CI. If Actions will not run on your fork, follow
[the recorded walkthrough of this lab](../../transcripts/lab-09-ci.md).
