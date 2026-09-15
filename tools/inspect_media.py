#!/usr/bin/env python3
"""Check a rendered MP4/MOV: size, duration, bitrates, codec profile, color tag, fast start. No ffmpeg needed.

usage: tools/inspect_media.py FILE [FILE ...]

Color tag = nclx primaries-transfer-matrix: 1-1-1 is Rec.709 with BT.709 transfer,
1-2-1 is Rec.709 with transfer "unspecified" (what Resolve writes for the "Gamma 2.4" tag).
Fast start = `moov` atom before `mdat` (Resolve's "Network optimization"): plays before fully downloaded.
"""
import os
import struct
import subprocess
import sys


def mdls(path, key):
    return subprocess.run(["mdls", "-raw", "-name", key, path], capture_output=True, text=True).stdout.strip()


def top_atoms(f, size):
    atoms, off = [], 0
    while off + 8 <= size:
        f.seek(off)
        hdr = f.read(16)
        n, typ = struct.unpack(">I4s", hdr[:8])
        if n == 1:
            n = struct.unpack(">Q", hdr[8:16])[0]
        elif n == 0:
            n = size - off
        atoms.append((typ.decode("latin1"), off, n))
        off += n
    return atoms


def inspect(path):
    size = os.path.getsize(path)
    print(f"== {os.path.basename(path)}")
    print(f"  size {size / 1e6:.1f} MB, duration {mdls(path, 'kMDItemDurationSeconds')} s, "
          f"{mdls(path, 'kMDItemPixelWidth')}x{mdls(path, 'kMDItemPixelHeight')}")
    print(f"  bitrate kbps: total {mdls(path, 'kMDItemTotalBitRate')}, video {mdls(path, 'kMDItemVideoBitRate')}, "
          f"audio {mdls(path, 'kMDItemAudioBitRate')}")
    with open(path, "rb") as f:
        atoms = top_atoms(f, size)
        names = [a[0] for a in atoms]
        fast = "moov" in names and "mdat" in names and names.index("moov") < names.index("mdat")
        print(f"  fast start: {'yes' if fast else 'no'}")
        moov = next((a for a in atoms if a[0] == "moov"), None)
        if moov is None:
            print("  no moov atom")
            return
        f.seek(moov[1])
        buf = f.read(moov[2])
    i = buf.find(b"colr")
    if i >= 0 and buf[i + 4:i + 8] in (b"nclx", b"nclc"):
        print("  color tag (primaries-transfer-matrix): %d-%d-%d" % struct.unpack(">HHH", buf[i + 8:i + 14]))
    else:
        print("  color tag: none")
    i = buf.find(b"avcC")
    if i >= 0:
        profile = {66: "Baseline", 77: "Main", 100: "High"}.get(buf[i + 5], buf[i + 5])
        print(f"  H.264 profile {profile}, level {buf[i + 7] / 10}")
    elif buf.find(b"hvcC") >= 0:
        print("  H.265")
    print(f"  audio: {'AAC' if buf.find(b'mp4a') >= 0 else 'no AAC track'}, {mdls(path, 'kMDItemAudioChannelCount')} ch")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for p in sys.argv[1:]:
        inspect(p)
