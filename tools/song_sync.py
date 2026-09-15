#!/usr/bin/env python3
"""Find where a reference song starts inside camera clips, by audio. No ffmpeg needed.

Decodes with macOS `afconvert` (works for camera proxies with AAC audio and .m4a/.mp3 songs;
does NOT open Sony raw MP4s with LPCM audio -- run it on the proxies, they have identical timing)
and cross-correlates with GCC-PHAT.

usage:
  tools/song_sync.py --song SONG.m4a CLIP [CLIP ...]      offsets for a known song
  tools/song_sync.py --library SONGS_DIR CLIP [CLIP ...]  identify each clip's song, then offsets
options:
  --fps 25   timeline/clip frame rate
  --json     machine-readable output

Output per clip:
  song_start_s / song_start_frame  clip time where the song's first sample plays (bias-corrected);
                                   use it as the clip in-point with the song in-point at 0
  conf        peak ratio vs next-best peak; true matches were 1.4-5.0, non-matches ~1.0-1.2
  2nd         best other song's conf (library mode); a match should clearly beat it
  song span   which part of the song the clip covers
"""
import argparse
import glob
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import wave

import numpy as np
from scipy.signal import decimate

# Raw GCC-PHAT lag lands 0.4-2.7 frames early vs hand sync (10 clips, 2 songs, Sept 2026).
BIAS_FRAMES = 1.6
SR = 16000
CACHE = os.path.join(tempfile.gettempdir(), "davinci-song-sync")
AUDIO_EXT = (".m4a", ".mp3", ".wav", ".aif", ".aiff")


def decode(path, sr=SR):
    os.makedirs(CACHE, exist_ok=True)
    st = os.stat(path)
    key = hashlib.md5(f"{path}|{st.st_size}|{st.st_mtime}|{sr}".encode()).hexdigest()
    out = os.path.join(CACHE, key + ".wav")
    if not os.path.exists(out):
        r = subprocess.run(["afconvert", "-f", "WAVE", "-d", f"LEI16@{sr}", "-c", "1", path, out], capture_output=True)
        if r.returncode:
            return None
    with wave.open(out) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)
    return x - x.mean()


def gcc_phat(clip, song, sr):
    """Return (seconds into clip where song sample 0 plays, peak ratio vs next-best peak >1 s away)."""
    n = 1 << int(np.ceil(np.log2(len(clip) + len(song))))
    X = np.fft.rfft(clip, n) * np.conj(np.fft.rfft(song, n))
    X /= np.abs(X) + 1e-9
    cc = np.fft.irfft(X, n)
    cc = np.concatenate([cc[-len(song):], cc[:len(clip)]])
    lags = np.arange(-len(song), len(clip))
    i = int(np.argmax(cc))
    frac = 0.0
    if 0 < i < len(cc) - 1:  # parabolic sub-sample peak
        y0, y1, y2 = cc[i - 1], cc[i], cc[i + 1]
        d = y0 - 2 * y1 + y2
        frac = 0.5 * (y0 - y2) / d if d else 0.0
    ratio = cc[i] / cc[np.abs(lags - lags[i]) > sr].max()
    return (lags[i] + frac) / sr, float(ratio)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--song")
    src.add_argument("--library")
    ap.add_argument("--fps", type=float, default=25)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("clips", nargs="+")
    a = ap.parse_args()

    songs = [a.song] if a.song else sorted(
        p for p in glob.glob(os.path.join(a.library, "*")) if p.lower().endswith(AUDIO_EXT))
    id_songs = {}
    rows = []
    for clip_path in sorted(a.clips):
        name = os.path.basename(clip_path)
        print(f"  {name}", file=sys.stderr)
        row = {"clip": name}
        rows.append(row)
        clip = decode(clip_path)
        if clip is None:
            row["verdict"] = "cannot decode (raw LPCM? use the proxy)"
            continue
        length = len(clip) / SR
        row["len_s"] = round(length, 2)
        if length < 2:
            row["verdict"] = "too short"
            continue

        runner_up = None
        best = songs[0]
        if len(songs) > 1:  # identify at 4 kHz, it is plenty for a yes/no
            c4 = decimate(clip, 4)
            scores = []
            for s in songs:
                if s not in id_songs:
                    x = decode(s)
                    id_songs[s] = None if x is None else decimate(x, 4)
                if id_songs[s] is not None:
                    scores.append((gcc_phat(c4, id_songs[s], SR // 4)[1], s))
            scores.sort(reverse=True)
            best = scores[0][1]
            runner_up = scores[1][0] if len(scores) > 1 else None

        song = decode(best)
        lag, conf = gcc_phat(clip, song, SR)
        start = lag + BIAS_FRAMES / a.fps
        song_len = len(song) / SR
        ok = conf >= 1.3 and (runner_up is None or conf >= 1.15 * runner_up)
        row.update(song=os.path.basename(best), song_start_s=round(start, 3), song_start_frame=int(round(start * a.fps)),
                   conf=round(conf, 2), runner_up_conf=None if runner_up is None else round(runner_up, 2),
                   song_from_s=round(max(0.0, -start), 1), song_to_s=round(min(song_len, length - start), 1),
                   verdict="match" if ok else "no clear match")

    if a.json:
        print(json.dumps(rows, indent=1, ensure_ascii=False))
        return
    print(f"{'clip':14} {'len':>6} {'conf':>5} {'2nd':>5} {'start_s':>8} {'frame':>6} {'song span':>13}  verdict")
    for r in rows:
        if "conf" not in r:
            print(f"{r['clip']:14} {r.get('len_s', ''):>6} {'':>5} {'':>5} {'':>8} {'':>6} {'':>13}  {r['verdict']}")
            continue
        span = f"{r['song_from_s']}-{r['song_to_s']}s"
        second = "" if r["runner_up_conf"] is None else r["runner_up_conf"]
        print(f"{r['clip']:14} {r['len_s']:6} {r['conf']:5} {second:>5} {r['song_start_s']:8} {r['song_start_frame']:6} "
              f"{span:>13}  {r['verdict']}: {r['song']}")


if __name__ == "__main__":
    main()
