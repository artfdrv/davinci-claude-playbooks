# davinci-claude-playbooks

*A scalable system of playbooks for Claude assisting with DaVinci Resolve editing workflows for filmmakers.*

You don't need to know how to code to use this. You need one repetitive editing
task you're tired of doing by hand.

## What this is

A small folder structure that turns "I do this same tedious thing every project"
into a documented, repeatable procedure Claude can run with you — and eventually
mostly without you.

It's built around **DaVinci Resolve** (via its scripting API / an MCP connector),
because that's free, scriptable, and most editors already have it. But the pattern
— playbook → knowledge → tool → skill — works for any repetitive creative task,
editing or not.

## Requirements

- [Claude Code](https://claude.com/claude-code) installed
- DaVinci Resolve (free or Studio) if you want Claude to drive the app directly,
  via a Resolve MCP connector (search "DaVinci Resolve MCP" for current options).
  Without it, you can still use this folder for anything text/file based —
  triage notes, shot logs, delivery checklists.

## First 10 minutes

1. Clone this repo, `cd` into it, run `claude`.
2. Read [`playbooks/example-single-take-video-edit/PLAYBOOK.md`](playbooks/example-single-take-video-edit/PLAYBOOK.md) —
   it's a worked example, not a template to follow literally. It shows what a
   finished playbook looks like after a few real runs.
3. Tell Claude about one boring, repeated task in your own workflow. For example:
   > "Every project I get a folder of clips and I have to watch each one and
   > sort the usable takes from the throwaways before I even start editing.
   > I want to figure out with you how to do that faster."
4. Do it together, once, slowly — you reviewing each step. Don't let Claude
   batch-process anything the first time through.
5. When it works, ask Claude to write down what you just did as a playbook
   (see [`playbooks/README.md`](playbooks/README.md) for the shape). That file
   is now yours to run again, faster, next time — and to hand to Claude cold
   in a new session.

## The loop

```
notice a repetitive task
        ↓
do it once, closely supervised  →  capture it as a playbook (playbooks/)
        ↓
run it again on the next project → note what changed, fix the playbook
        ↓
facts about your tools/footage that keep coming up → knowledge/
a step that's faster as a script than a prompt → tools/
        ↓
ran clean 2-3 times without changes → promote to a Claude Code skill
(.claude/skills/<name>/SKILL.md — same content, just copy it over)
```

## Map

| Path | What |
|---|---|
| `playbooks/` | One folder per recurring task, step by step. Draft → stable → skill |
| `knowledge/` | Facts verified about tools, footage, or process |
| `projects/` | One note per project: what was done, what's pending |
| `tools/` | Small scripts for steps that are faster as code than as a prompt |
| `CLAUDE.md` | What Claude reads automatically at the start of every session here |

## Ground rules worth keeping from day one

These came from real editing sessions where skipping them cost time:

- **Pilot on one clip before batching.** Let Claude show you the approach on
  a single item, review it, then say "do the rest."
- **Ask before anything destructive or hard to undo** — rendering, deleting
  files, overwriting an existing timeline or grade, installing software.
  Scripted changes to an app often don't undo cleanly with Cmd+Z.
- **Build new, don't modify existing** — new timelines/bins instead of editing
  the ones you already made, until you trust the process.
- **Read the current state before changing it**, and read it back after, so
  you (and Claude) can see exactly what changed.

## Making it yours

Everything in this kit is a starting point, not a standard. Delete the example
playbook once you've written your own. Rename `projects/` to whatever unit
your work comes in (shoots, clients, episodes). The only thing worth keeping
is the shape: a playbook per task, facts in `knowledge/`, one folder, growing
with you.

## Contributing

Have a playbook for a recurring editing task that isn't here yet (interview
cuts, wedding edits, podcast video, documentary assembly)? See
[`CONTRIBUTING.md`](CONTRIBUTING.md).
