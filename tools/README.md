# Tools

Small scripts for one step that's faster as code than as a back-and-forth
prompt — usually because it's repetitive, needs to run over many files at
once, or does numeric work (correlation, image thumbnails) a chat turn isn't
suited for.

## Included examples

These four back the example playbook (`playbooks/example-single-take-video-edit/`).
They're real, runnable scripts — not pseudocode — so you can see what a
"tool" in this kit actually looks like, then delete them once you've got
your own.

| Script | What it does |
|---|---|
| `song_sync.py` | Finds which audio track a clip matches and the exact frame it starts at, via cross-correlation. Needs `afconvert` (macOS) and numpy/scipy |
| `contact_sheet.swift` | Thumbnail grid per clip, so you can eyeball a folder of footage without scrubbing each file. No ffmpeg needed |
| `finder_tag.py` | Add/remove/list macOS Finder tags from the command line, for building a shortlist |
| `inspect_media.py` | Checks a rendered file's actual bitrate, codec profile, color tag, and fast-start flag — for verifying a render did what you asked, not just that the job said "Complete" |

Run any of them with no arguments to see usage.

## Writing your own

Ask Claude to write it as part of doing the task, not as a separate step —
"can you turn that last loop into a script I can reuse" once you've done
something manually once or twice and it's clearly going to happen again.
Keep them narrow: one job, callable with plain arguments, no assumptions
about paths outside what you pass in.
