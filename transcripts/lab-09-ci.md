# Lab 9 - CI: what to expect

*The recorded walkthrough of this lab follows once the workflows have run in the workshop's repository. Until then,
this page shows what Lab 9 produces, so that you can follow along if Actions will not run on your fork.*

## The steps, and what you see

1. **Enable Actions** on your fork. The *Actions* tab lists three workflows: *Run tests*, *Agent triage* and
   *Heal suggestions*.
2. **Push a branch that breaks a test**, for example the expected status of `Health Reports Ok` in
   `tests/api/smoke.robot` changed from `ok` to `okay`. *Run tests* fails on the push, and again on the pull request.
3. **Open the pull request on your fork.** When *Run tests* has failed, *Agent triage* starts and comments.

## The comment without a key

With no secret set, the comment holds the failed tests from the run. This one was produced by the same script the
workflow uses, from a run with exactly that break:

> ### Test results: 1 passed, 1 failed
>
> | Test | Where | Message |
> |---|---|---|
> | Health Reports Ok | `smoke.robot:12` | ok != okay |
>
> *No analysis.* Add a Claude credential (`ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN`), or the `TRIAGE_MODEL`, `TRIAGE_BASE_URL` and `TRIAGE_API_KEY` secrets of any OpenAI-compatible endpoint, to get a root-cause analysis here. `SETUP.md` explains both; set a spending cap first.

With a Claude credential or the `TRIAGE_*` settings, a *Root cause* section follows the table: which change in the
pull request broke which test, the evidence from the failure message, and what to fix. Its last line names who
wrote it. An agent drafted it, so check it before you act on it.
