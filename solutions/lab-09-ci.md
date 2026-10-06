# Lab 9 - CI: the reference

[Lab 9](../labs/lab-09-ci/INSTRUCTIONS.md) produces no files in your repository: its result is a pull request on
your fork with a triage comment. The [transcript](../transcripts/lab-09-ci.md) records one, with both kinds of
comment.

## What done looks like

- *Run tests* fails on your push and again on the pull request.
- *Agent triage* comments once on the pull request. A second failing push updates that comment instead of adding
  one.
- Without a credential, the comment lists the failed tests and names the secrets that would add an analysis. With
  one, a root cause per test follows the list.
- The pull request is closed, not merged, and `main` on your fork is unchanged.

## Why it is a good result

- **The workflow, not the agent, posts the comment,** so the agent needs no permission to write to your repository.
- **One comment per pull request,** which later failures update, so the pull request stays readable.
- **The summary comes first and works without a key;** the analysis is an addition, and its last line names the
  model that wrote it.

## What to debrief

- **Does the root cause match the break?** In the rehearsal it did, for both tests, with the diff's hunks as
  evidence. But each fix offered two ways out: change the test back, or change the shop to match the test. Only
  someone who knows why the test changed can choose.
- **The heal suggestion** (stretch goal). The rehearsal's run healed the five drifted locators of
  `resources/legacy.resource` onto a branch. Review it as in Lab 8: one heal no longer used the keyword's `${GRID}`
  variable, and a second run proposed a different locator for the same line.

## Compare yours

Compare your comment with the two versions in the [transcript](../transcripts/lab-09-ci.md): the one without a
credential, and the one with an analysis.
