# Contributing

This repo is a starting shape, not a finished product. The most useful
contribution is a playbook for a recurring editing task this doesn't cover yet.

If you're an AI agent (Claude Code or otherwise) opening this repo on
someone's behalf, also read `CLAUDE.md` — it has the order of operations for
getting from "user has a repetitive task" to "PR worth reviewing."

## The bar: run it before you write it

A playbook is a record of something that actually happened, not a plan for
something that should work. Before opening a PR, you (human or agent) should
be able to say yes to all of these:

- [ ] **You ran the whole procedure**, start to finish, on real material —
      not a description of how you'd expect it to go.
- [ ] **You ran it more than once**, ideally on two different pieces of
      material, and the "Defaults" and "Known issues" sections reflect
      things that differed or broke between runs, not just the first pass.
- [ ] **There's at least one human checkpoint** in the procedure — a point
      where the person the playbook is for has to look at something before
      the next step happens (a render, a send, a delete). A playbook that's
      fully autonomous end to end is either trivial or hiding a risk.
- [ ] **Every number has a source.** A fade duration, a crop, a bitrate — say
      where it came from (a tool's default, a person's preference stated once,
      a measured accuracy). A defaults table with no source column is a guess
      dressed as a fact, and the next person can't tell which.
- [ ] **It's genericized.** No real names, real file paths, client or project
      identifiers. Read `example-single-take-video-edit/PLAYBOOK.md` for the
      shape this should take — specific enough to be useful, sanitized of
      whoever you built it for.
- [ ] **Status is honest.** `draft` if this is the first real run, `stable`
      only once it's survived 2-3 projects unchanged (see `playbooks/README.md`).
      Don't mark something `stable` to make the PR look more finished.

The PR template repeats this as a checklist — fill it in rather than deleting it.

## Adding a playbook

1. Copy [`playbooks/TEMPLATE/PLAYBOOK.md`](playbooks/TEMPLATE/PLAYBOOK.md) to
   `playbooks/<your-use-case>/PLAYBOOK.md` and fill it in as you go, not after.
2. Keep it tool-agnostic where you can, and call out clearly where it's
   Resolve-specific (an API call, a menu path) vs. generally true of any
   similar edit.
3. Check it against the bar above before opening the PR.

## Adding to `knowledge/`

Verified API behavior or a technique with numbers behind it is welcome,
independent of a full playbook. Say what's verified vs. still a guess, and
date it. The same "you actually ran this" bar applies.

## Adding a tool

Keep scripts narrow — one job, plain CLI arguments, no hardcoded paths. Note
platform requirements (the existing tools are macOS-only) at the top of the
file and in `tools/README.md`.

## What doesn't belong here

- Anything tied to a specific person, client, or shoot
- Personal preferences dressed up as defaults (a house style belongs in your
  own private workspace's `knowledge/conventions.md`, not here)
- Untested procedure — if you haven't run it, it's not a playbook yet

## Process

Open a PR against `main` from a fork. All PRs are reviewed and merged by the
maintainer by hand — expect questions if something in the checklist above
looks unverified, and don't take a merge delay personally; it just means the
queue is real.
