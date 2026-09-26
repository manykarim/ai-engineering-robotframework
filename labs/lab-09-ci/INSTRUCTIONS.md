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
   | `agent-triage.yml` | when a pull request's tests fail | posts one comment with the failed tests and, with a credential, an agent's root cause |
   | `heal-suggestions.yml` | when you start it | turns heals into a suggestion pull request (the stretch goal) |

   A fourth workflow builds this workshop's website. It runs only in the workshop's own repository, never on your
   fork.

2. **Optionally give the triage agent a credential.** Without one, the lab still works: the comment then lists
   the failed tests, without an analysis. With one, an agent adds the root cause. **Set a spending cap on any key
   first.**

   | You have | Set these secrets on your fork | The analysis comes from |
   |---|---|---|
   | a Claude subscription | `CLAUDE_CODE_OAUTH_TOKEN`, from `claude setup-token` | the Claude Code Action |
   | an Anthropic API key | `ANTHROPIC_API_KEY` | the Claude Code Action |
   | a key for any OpenAI-compatible endpoint, for example your healing key | `TRIAGE_MODEL`, `TRIAGE_BASE_URL`, `TRIAGE_API_KEY` | one call to that model |

   ```bash
   gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo <your-handle>/ai-engineering-robotframework
   ```

   `gh secret set` asks for the value, so it never lands in your shell history.

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
Lab 8: merge nothing you would reject. It needs your healing model as the secrets `HEAL_MODEL`, `HEAL_BASE_URL` and
`HEAL_API_KEY`; without them, it ends with a notice and changes nothing.

## If your agent fails

This lab needs no agent of your own: the agent runs in CI. If Actions will not run on your fork, follow
[the recorded walkthrough of this lab](../../transcripts/lab-09-ci.md).
