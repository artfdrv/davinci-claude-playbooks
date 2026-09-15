# Video editing workspace

Home base for editing with Claude driving DaVinci Resolve through a Resolve MCP
connector. There's no app code here: this is the operating manual (playbooks +
knowledge) for recurring editing work, plus notes on individual projects.

New here? Read `README.md` first.

## Map

| Path | What |
|---|---|
| `playbooks/` | One folder per recurring task, step by step. Draft → stable → skill (see `playbooks/README.md`) |
| `knowledge/` | Facts about your tools, footage, and process, verified in practice. Read the relevant file before scripting something new |
| `projects/` | One note per project: results, decisions, status |
| `tools/` | Small scripts for steps that are faster as code than as a prompt |

## Environment

<!-- Fill in once you've set these up:
- Resolve MCP connector name and any quirks (e.g. multiple connectors reaching the same app — pick one and stick to it)
- Where run_script is sandboxed (no OS/file access) vs. run_script_unsafe (needs OS access)
- Any local tools you have available (ffmpeg or not, what Python packages, etc.)
- Your media layout: raw footage, proxies, music/assets, delivery folders
- Your Resolve project structure: one project per period? one bin per shoot/client?
-->

- API stubs: `get_scripting_api(as_file=true)` then grep the file — cheaper than pulling full docs into context.
- `get_whats_new` is worth calling once in a while: Resolve adds features often, faster than any model's training cutoff.

## Ground rules

- Read state before writing; read back after every write and report what actually changed.
- Build new timelines/bins; don't modify existing timelines, grades, gallery or render queue without asking.
- Pilot on one clip, let the user review, then batch.
- Ask before rendering, deleting anything (in the app or on disk), or installing tools.
- Scripted changes may not undo cleanly with Cmd+Z.

## Keep the knowledge current

Write down what you learn in the same session, dated (YYYY-MM-DD), marking anything unverified:

- API behavior, bug or workaround → `knowledge/resolve-api-gotchas.md`
- A technique that works (with numbers) → matching `knowledge/` file, or a new one
- A preference or workflow change → the playbook, and a `knowledge/conventions.md` if you start one
- Project-specific results and status → `projects/<project>.md`
- A new recurring task → new `playbooks/<use-case>/PLAYBOOK.md` from the template in `playbooks/README.md`

## If you're an agent working toward a contribution

Someone opened Claude Code in this repo because they want to add a playbook.
Here's the order that actually produces something worth merging:

1. **Do the task first, don't write the playbook first.** Help with the real,
   repeated task on real material, the way any session in this repo would.
   Draft the procedure as you go, but treat it as scratch notes, not a
   deliverable yet.
2. **Run it more than once.** A procedure that worked once is an anecdote. It
   needs to survive a second project with different material before its
   "defaults" and "known issues" sections mean anything — see the
   `draft → stable` distinction in `playbooks/README.md`.
3. **Only then** copy `playbooks/TEMPLATE/PLAYBOOK.md`, fill it in from what
   actually happened, and check it against `CONTRIBUTING.md`'s checklist
   before opening a PR.
4. Strip anything specific to the person or project you were helping — names,
   paths, client identifiers — the way `example-single-take-video-edit` was
   genericized from a real one. If unsure whether something is too specific,
   leave it out and generalize the number or example instead.
5. Tell the user plainly what you're about to make public before opening a
   PR. This repo is reviewed by one maintainer; a low-effort or never-run
   submission just costs them time to reject.
