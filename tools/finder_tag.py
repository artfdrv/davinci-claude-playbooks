#!/usr/bin/env python3
"""Add, remove or list macOS Finder tags, no extra tools needed.

usage:
  tools/finder_tag.py list FILE [FILE ...]
  tools/finder_tag.py add TAG FILE [FILE ...]      keeps existing tags; reuses TAG's color from a file already tagged
  tools/finder_tag.py remove TAG FILE [FILE ...]

Tags live in the `com.apple.metadata:_kMDItemUserTags` xattr: a binary plist list of
"Name" or "Name\\n<color index>" strings. Finder shows the color from that suffix.
"""
import plistlib
import subprocess
import sys

ATTR = "com.apple.metadata:_kMDItemUserTags"


def read_tags(path):
    r = subprocess.run(["xattr", "-px", ATTR, path], capture_output=True, text=True)
    if r.returncode:
        return []
    return plistlib.loads(bytes.fromhex("".join(r.stdout.split())))


def write_tags(path, tags):
    if not tags:
        subprocess.run(["xattr", "-d", ATTR, path], capture_output=True)
        return
    subprocess.run(["xattr", "-wx", ATTR, plistlib.dumps(tags, fmt=plistlib.FMT_BINARY).hex(), path], check=True)


def tag_name(tag):
    return tag.split("\n")[0]


def stored_form(tag):
    """The "Name\\n<color>" form used on any file that already carries this tag (keeps Finder's color)."""
    r = subprocess.run(["mdfind", f"kMDItemUserTags == '{tag}'"], capture_output=True, text=True)
    for f in r.stdout.splitlines():
        for t in read_tags(f):
            if tag_name(t) == tag:
                return t
    return tag


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("list", "add", "remove"):
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "list":
        for f in sys.argv[2:]:
            print(f"{f}: {[tag_name(t) for t in read_tags(f)]}")
        return
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    tag, files = sys.argv[2], sys.argv[3:]
    stored = stored_form(tag) if cmd == "add" else tag
    for f in files:
        tags = read_tags(f)
        if cmd == "add" and not any(tag_name(t) == tag for t in tags):
            tags.append(stored)
        elif cmd == "remove":
            tags = [t for t in tags if tag_name(t) != tag]
        write_tags(f, tags)
        print(f"{f}: {[tag_name(t) for t in read_tags(f)]}")


if __name__ == "__main__":
    main()
