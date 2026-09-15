# Resolve scripting API: verified behavior

Starter set, carried over from real sessions. Dated entries; "verified" =
actually observed, not read in docs. Add your own as you find them — this
file is the whole point of the pattern: stop re-discovering the same bug.

## Connector and tooling

- If more than one MCP connector can reach the same running Resolve instance,
  pick one for a given session and stick to it — mixing them against the same
  app invites confusion about which call actually landed.
- A sandboxed `run_script` typically has no OS/file access (no `os`, `sys`,
  file writes); use an "unsafe"/OS-access variant only when you actually need
  it. Resolve itself can still write files (exports, stills, renders) even
  from the sandboxed path.
- Pull API stubs to a local file and grep them rather than asking for docs in
  every message — much cheaper on context, and exact for your Resolve version.
- Call whatever "what's new" tool your connector exposes now and then: Resolve
  ships major features often, faster than any model's training cutoff.

## Media pool

- Media pool operations (create timeline, import) typically act on the
  **current folder** — set it explicitly before calling them, don't assume.
- Proxy linking works from a plain path once the naming convention matches
  your camera's proxy output.

## Timelines

- A new empty timeline starts with 1 video + 1 audio track, and its timeline
  origin is usually not frame 0 (often 1 hour in, i.e. frame 90000 at 25fps) —
  check yours before doing frame math.
- Appending to a timeline acts on the **current timeline** — set it first.
- `endFrame` in an append call is commonly **exclusive** (duration = end − start).
  Appending linked video+audio in a single call, then deleting and
  re-appending, has been observed to silently drop the video track — append
  video and audio separately, verify each landed, then link them explicitly.
- **No trim, move, or slip on a placed timeline item** is common in these
  APIs — to change a cut you delete the item and re-append with new numbers,
  rather than dragging an edge.
- A "mute" call on a track is usually the same mute a human sees in the UI —
  read it back to confirm rather than trusting the call succeeded.

## Color

- Grade-copy calls often work **across timelines**, not just within one —
  useful for reusing a grade from a previous project without a full manual copy.
- Many scripting APIs expose **no node delete and no OFX parameter access**
  (e.g. can't set a Color Space Transform's parameters via script). Practical
  workaround: pick a reference clip/grade that already has the node structure
  you want, and copy grades onto new clips from it, rather than building the
  node tree via script.
- Scopes (waveform/vectorscope/histogram) are typically not exposed via the
  scripting API at all — if you need pixel data, look for a "grab a still" or
  "export current frame" call instead.

## Render

- A render job list read back via the API may not include everything you set
  (e.g. exact bitrate or color tags) — verify the actual rendered file
  (bitrate, resolution, color tag) rather than trusting the job list.
- Starting rendering by job ID starts only those jobs — don't call the
  "start whole queue" variant unless you mean to touch every job in it,
  including ones you didn't add this session.
- The render queue accumulates old jobs across sessions; don't clear it
  without asking, since some of those jobs may be someone else's work.
