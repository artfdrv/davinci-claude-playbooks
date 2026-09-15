# Playbooks

A playbook is the written procedure for one recurring task (a triage pass, a
type of edit, a delivery checklist). It starts rough after the first real run
and gets sharper every time you use it. Once it stops changing, it becomes a
Claude Code skill.

## Layout

```
playbooks/<use-case>/PLAYBOOK.md   the procedure
playbooks/<use-case>/...           optional: templates or scripts only this use case needs
```

Shared scripts live in `/tools`, shared facts in `/knowledge`, per-project notes in `/projects`.

## Lifecycle

1. **draft**: written after the first real run; expect edits.
2. **stable**: ran on 2-3 projects without procedure changes.
3. **skill**: copy to `.claude/skills/<use-case>/SKILL.md` (the frontmatter already fits) and reference tools by path.

## Index

| Playbook | Status | Notes |
|---|---|---|
| [example-single-take-video-edit](example-single-take-video-edit/PLAYBOOK.md) | example | Worked example included in this kit — delete once you've written your own |

## Template

```markdown
---
name: <use-case>
description: <one line: when to use it>
status: draft
last_run: YYYY-MM-DD (<project>)
---

# <Title>

## Inputs          what the user provides
## Steps           numbered; each says who: Claude alone / Claude + user check / user
## Checkpoints     where to stop for human review
## Defaults        numbers and settings
## Known issues    and workarounds
## Open questions
```
