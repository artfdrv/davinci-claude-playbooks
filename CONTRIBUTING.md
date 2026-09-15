# Contributing

This repo is a starting shape, not a finished product. The most useful
contribution is a playbook for a recurring editing task this doesn't cover yet.

## Adding a playbook

1. Copy the template in [`playbooks/README.md`](playbooks/README.md) into
   `playbooks/<your-use-case>/PLAYBOOK.md`.
2. Base it on a task you've actually done with Claude more than once — not a
   hypothetical. Real frame numbers, real settings, real "here's what broke"
   beat generic advice.
3. Keep it tool-agnostic where you can, and call out clearly where it's
   Resolve-specific (an API call, a menu path) vs. generally true of any
   single-take/multi-take edit.
4. No personal data: no real client names, real file paths outside the repo,
   or anything that identifies a specific shoot or person. Genericize numbers
   and examples the way [`example-single-take-video-edit`](playbooks/example-single-take-video-edit/PLAYBOOK.md) does.

## Adding to `knowledge/`

Verified API behavior or a technique with numbers behind it is welcome,
independent of a full playbook. Say what's verified vs. still a guess, and date it.

## Adding a tool

Keep scripts narrow — one job, plain CLI arguments, no hardcoded paths. Note
platform requirements (the existing tools are macOS-only) at the top of the
file and in `tools/README.md`.

## What doesn't belong here

- Anything tied to a specific person, client, or shoot
- Personal preferences dressed up as defaults (a house style belongs in your
  own private workspace's `knowledge/conventions.md`, not here)
- Untested procedure — if you haven't run it, say so in the playbook's status

## Process

Open a PR. For a new playbook, a short description of the recurring task it
solves is enough context to review it.
