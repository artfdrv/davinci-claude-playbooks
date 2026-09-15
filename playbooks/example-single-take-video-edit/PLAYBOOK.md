---
name: example-single-take-video-edit
description: WORKED EXAMPLE — turn a folder of single-take performance clips (dance, a live take, a demo) plus one audio track into a synced, graded, delivered video per clip. Copy the pattern, not the specifics.
status: example
last_run: n/a — this is a sanitized worked example, not a live playbook
---

# Example: single-take video synced to a track

This is what a playbook looks like after several real runs: specific numbers,
a human checkpoint, and a "known issues" section that saves you from
re-discovering the same gotcha twice. It was built for dance videos —
performer does one take of a routine to a song, camera rolls the whole time —
but the shape (triage → sync → build → human review → deliver) applies to
any single-take-plus-track edit: a live music take, a spoken-word performance,
a demo reel.

Read this once for the pattern. Then delete it and write your own from the
`playbooks/README.md` template, based on a task you actually do.

## Inputs

- A folder of raw takes (camera files, ideally with a lower-res proxy alongside)
- The audio track the performer was working to, if there is one
- A Resolve project with a place to put the new bins/timelines
- Later: which take(s) to use, and any naming info for the delivered files

## Steps

### 1. Triage → shortlist (Claude alone, human sanity-checks the list)

1. If there's a track: identify which clips it appears in and where it starts
   in each (an audio cross-correlation script can do this in bulk — see
   `tools/song_sync.py` in this kit for a working example).
2. Generate a contact sheet (thumbnail grid) per clip instead of scrubbing
   full-res footage by hand — see `tools/contact_sheet.swift` for an example.
3. Classify each clip: full take / incomplete / false start / other. Write
   the rules you're actually using into `knowledge/` once they stabilize —
   they'll be specific to your footage (e.g. "under 10s = false start").
4. Tag the shortlisted files (Finder tags, a spreadsheet, whatever you already
   use) so the human step is "look at the tagged ones," not "look at all of them."
5. **Checkpoint**: human confirms the shortlist before anything gets imported.

### 2. Import (Claude alone)

1. Create a bin for this project if missing, import the chosen clips,
   link proxies if you shot with them.
2. Reuse the track from the media pool if it's already in the project.

### 3. Build the timeline (Claude alone)

**One standalone timeline per clip** — a single timeline with several clips
and gaps gets confusing fast once you're grading and delivering per-clip.

1. Create an empty timeline named `<project> <clip>`, add an audio track for
   the reference track if there isn't a second one already.
2. Place the clip: video + its own audio on their tracks, linked; the
   reference track on its own track, aligned to the sync point found in step 1.
3. Mute the camera audio track if the reference track is the one you're keeping.
4. Add short fades in/out on both video and the reference track (a few frames
   each — tune to taste).

### 4. Grade (Claude copies, human finishes)

1. Copy the grade from a clean reference clip shot under the same conditions,
   rather than building one from scratch every time.
2. First clip of a new lighting setup: human adjusts the base exposure/balance
   node, everything after copies from that.

### 5. Human review — STOP

Check sync, in/out points (did the performer actually finish?), fades, grade.
Cut changes usually mean rebuilding that clip rather than trimming in place —
check `knowledge/` for what your scripting API actually supports before
assuming trim-in-place works.

### 6. Deliver (Claude sets up; render only after a go-ahead)

1. Confirm folder and file names with the human.
2. Load (or build once, then reuse) a render preset for your delivery target.
3. One render job per clip, marks set to that clip's start/end.
4. Start only the jobs you just added — never the whole queue blind.
5. Verify each rendered file's actual specs (duration, resolution, bitrate) —
   don't assume the render settings applied the way you expect; check the file.

## Who does what

| Step | Who |
|---|---|
| Triage, sync, shortlist | Claude alone; human glances at the list |
| Which take to use | Human (or whoever the footage is for) |
| Import, timeline, sync, fades | Claude alone |
| End point | Claude proposes, human confirms in review |
| Grade | Claude copies a reference, human tweaks the base node |
| Review | Human |
| Render, file check | Claude, after the human's go-ahead |

## Known issues (illustrative — yours will differ)

- Some editing APIs have no trim/move on a placed clip: you rebuild the cut
  with exact frame numbers rather than dragging an edge. Worth checking early
  so you don't design a playbook around an operation that doesn't exist.
- Audio-only sync can't tell you when a performer *stops* — that end point
  usually still needs a human eye.
- A script that reads back "success" doesn't always mean the visible state
  matches — read back and check, don't trust the return value alone.

## Open questions

This section is where you park things you haven't nailed down yet, so the
next run picks them up instead of re-deciding from scratch each time.
