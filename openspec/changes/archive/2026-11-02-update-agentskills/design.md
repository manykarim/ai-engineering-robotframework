# Design

## Context

See proposal.md for why. The installer version lives in two places on `main`: Lab 3's step 1 and the table in
`SETUP.md`. `workshop/lab-assets` makes `SETUP.md` the place that names it. `rf-agentskills` is not a Python
dependency of the project: it runs through `uvx`, so `uv.lock` does not record it.

What 0.7.0 does, checked on 2026-11-02 with `install --help` and `--dry-run`:
- It takes the same flags as 0.6.0 (`--agent`, `--scope project`, `--project .`, `--what skills`). `--what mcp` is
  accepted and ignored.
- It writes to the same folders: `.claude/skills/` for Claude Code and GitHub Copilot, `.agents/skills/` for Codex,
  plus support files under `.claude/rf-agentskills-files/` or `.codex/rf-agentskills-files/`.
- It installs 12 skills: `rf-appium`, `rf-browser`, `rf-language`, `rf-libdoc`, `rf-platynui`, `rf-python-library`,
  `rf-requests`, `rf-restinstance`, `rf-results`, `rf-robotcode`, `rf-selenium` and `rf-setup`.
- Re-running `install` over an older install upgrades it. Files the bundle no longer ships are pruned when their
  hash is unchanged, and user-modified files are kept.
- It still writes absolute paths into some installed files (`transform=plugin_root_substitution`), as 0.6.0 did.

On `solutions`, the commit `lab-03-skills: the Robot Framework Agent Skills and a skill for convention 2` holds 79
files. 76 come from the 0.6.0 installer, 2 are the participant's skill (`.claude/skills/locators-in-resources/`), and
one is `.rf-agentskills/installed.json`. The 0.6.0 install ran under WSL, so its absolute paths start with
`/tmp/claude-1000/...`. No later commit touches those files; Lab 6 adds `.mcp.json`, which is a different file. The
reference page `solutions/lab-03-skills.md` names the 0.6.0 skills in one sentence. That sentence also says Copilot
keeps them in `.github/skills/`, which contradicts Lab 3 and both installers: Copilot's skills land in
`.claude/skills/`.

## Goals / Non-Goals

**Goals:**
- Every instruction a participant follows names `rf-agentskills@0.7.0`, and `SETUP.md` names the content it brings.
- `solutions` shows what installing 0.7.0 in Lab 3 produces, and its reference page describes that result.

**Non-Goals:**
- Changing transcripts or archived changes. They record what happened with 0.6.0.
- Changing Lab 3's steps, its skill template, or the participant's `locators-in-resources` skill.
- Adopting 0.7.0's new options (`--agents`, `claude-desktop`) or installing more than `--what skills`.

## Decisions

### D1. Change the version string only on `main`
Lab 3 names no skill, so its steps, prompts and folder table stay true for 0.7.0. Only the version in the command
changes. In `SETUP.md` the content column changes from `v1.2.0` to `2.0.0`. Upstream calls it "plugin 2.0.0" and has
no content tag for it, so there is nothing to put a `v` in front of. Alternative: drop the content version from the
table. Rejected, because the table exists so that "everyone gets the same versions", and the content is what
participants see.

### D2. Regenerate Lab 3's result by running the 0.7.0 installer inside that commit
When `solutions` is rebased onto the new `main`, the rebase stops at `lab-03-skills` (a sequence editor marks it
`edit`). The installer runs there with the exact command from Lab 3, over the 0.6.0 install, as a participant
upgrading would run it. The result is amended into the commit, and the rebase continues. The commit's message and
position stay the same, so `git log main..origin/solutions` still shows one commit per lab. Then:
- `git show --stat` of the commit shows the 0.7.0 skill folders, `locators-in-resources`, and `installed.json` with
  `bundle_version` 0.7.0;
- any 0.6.0 skill folder the installer kept, because its hash no longer matched, is removed by hand, so that the
  commit holds exactly what a fresh 0.7.0 install plus the participant's skill would hold.

Alternatives:
- A new commit on top of `solutions`. Rejected: `workshop/solutions` wants one commit per lab, and the reference page's
  "Compare yours" command looks for the commit that starts with `lab-03-skills`.
- Leave the 0.6.0 result. Rejected by the user: the reference would not match what participants install.

### D3. Run the installer under WSL, in a checkout below `/tmp`
The installer writes the checkout's absolute path into installed files. The 0.6.0 install ran under WSL below `/tmp`.
Running 0.7.0 the same way keeps that shape, and keeps a Windows user profile path out of the branch.

### D4. The reference page changes in its own commit, by the same rebase
The rebase also stops at `reference: one page per lab ...`, where `solutions/lab-03-skills.md` gets:
- the 12 `rf-*` names in place of the 0.6.0 list;
- Codex's `.agents/skills/` and Copilot's `.claude/skills/`, matching Lab 3;
- one sentence saying the transcript was recorded with 0.6.0, whose skills had other names.

Its *What to debrief* claims are checked again against 0.7.0 (task 4.2) and stay only if they still hold.

## Risks / Trade-offs

- [0.7.0's new `rf-language` skill also covers reviewing Robot Framework code, and may compete with
  `locators-in-resources` on the review prompt] → Task 4.2 runs both debrief prompts in a fresh Claude Code session on
  the rebased branch. If the participant's skill no longer loads, stop and decide with the user. The fix would be a
  change to Lab 3, which is a different change.
- [The installer keeps a 0.6.0 file it considers user-modified] → D2's check removes the leftovers, and the commit's
  file list is compared with a fresh 0.7.0 dry run.
- [Rewriting a lab commit changes its hash; a participant who saved the old hash for "Compare yours" gets an old
  diff] → The page looks the commit up by message, not by hash, so the documented command keeps working.
- [The force-push races another push to `solutions`] → `--force-with-lease` on the tip that was rebased.

## Migration Plan

1. On a branch from `main`, change the version in Lab 3 and `SETUP.md`. Open a pull request, let the site build pass,
   and merge it.
2. Rebase `solutions` onto the new `main`, stopping at `lab-03-skills` and at the reference commit (D2, D4).
3. Check the debrief prompts, run the suite, and force-push with a lease.
4. Rollback: revert the merge on `main`, then rebase `solutions` again, or force-push its previous tip, which the pull
   request records.

## Open Questions

- `update-dependencies` is archived only on the local branch `archive-update-dependencies`, which is not pushed. If it
  merges first, this change rebases `solutions` onto a `main` that already includes it. Either order works; the lease
  uses whatever tip `solutions` has when task 4 starts.
