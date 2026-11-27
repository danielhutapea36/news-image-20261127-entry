#!/usr/bin/env python3
"""One picture of Friday 27 November 2026's world news.

``entry.png`` — a 1024 by 1024 newspaper page drawn offline while this
entry was built — ships in this repository. This program copies it to
the output directory. It uses only the standard library, reads nothing
from the network, and consults neither the clock nor any random source,
so every run writes the same bytes.

    MAKEFUN_OUTPUT_DIR=/tmp/ni27-out python3 main.py
    python3 main.py --out-dir /tmp/ni27-out
    python3 main.py --verify-only

A bad image, a missing file, or an unwritable folder prints an error
and exits non-zero; a good run exits zero and prints where it wrote.
"""

import hashlib
import os
import sys

MAGIC = bytes((0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A))
SIDE = 1024
LIMIT = 1 << 20
NAME = "entry.png"


def die(message):
    sys.stderr.write("error: %s\n" % message)
    return 1


def picture_size(blob):
    """Width and height from the IHDR chunk, or ValueError."""
    if len(blob) < 33 or blob[:8] != MAGIC:
        raise ValueError("not a PNG file")
    if int.from_bytes(blob[8:12], "big") != 13 or blob[12:16] != b"IHDR":
        raise ValueError("first chunk is not a 13-byte IHDR")
    return (int.from_bytes(blob[16:20], "big"),
            int.from_bytes(blob[20:24], "big"))


def load_picture():
    """Read the bundled image and check it against the gate."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), NAME)
    with open(path, "rb") as handle:
        blob = handle.read()
    if len(blob) > LIMIT:
        raise ValueError("%s is %d bytes, over the 1 MiB limit" % (NAME, len(blob)))
    width, height = picture_size(blob)
    if (width, height) != (SIDE, SIDE):
        raise ValueError("%s is %dx%d, expected %dx%d"
                         % (NAME, width, height, SIDE, SIDE))
    return path, blob


def parse_flags(argv):
    """Return (out_dir, verify_only) for --out-dir and --verify-only."""
    out_dir = None
    verify_only = False
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--verify-only":
            verify_only = True
        elif arg == "--out-dir":
            i += 1
            if i >= len(argv):
                raise ValueError("--out-dir needs a directory after it")
            out_dir = argv[i]
        elif arg.startswith("--out-dir="):
            out_dir = arg.split("=", 1)[1]
            if out_dir == "":
                raise ValueError("--out-dir needs a non-empty directory")
        elif arg in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        else:
            raise ValueError("unknown argument: %s" % arg)
        i += 1
    return out_dir, verify_only


def target_folder(flag_dir):
    """--out-dir wins, then $MAKEFUN_OUTPUT_DIR, then /output."""
    if flag_dir:
        return flag_dir
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir is not None:
        if env_dir == "":
            raise ValueError("MAKEFUN_OUTPUT_DIR is set but empty")
        return env_dir
    return "/output"


def main(argv):
    try:
        out_dir, verify_only = parse_flags(argv)
        path, blob = load_picture()
    except (OSError, ValueError) as exc:
        return die(str(exc))
    digest = hashlib.sha256(blob).hexdigest()
    if verify_only:
        print("verified %s: %d bytes, sha256=%s" % (path, len(blob), digest))
        return 0
    try:
        folder = target_folder(out_dir)
        os.makedirs(folder, exist_ok=True)
        destination = os.path.join(folder, NAME)
        with open(destination, "wb") as handle:
            handle.write(blob)
        with open(destination, "rb") as handle:
            if handle.read() != blob:
                raise ValueError("wrote %s but the bytes differ" % destination)
    except (OSError, ValueError) as exc:
        return die(str(exc))
    width, height = picture_size(blob)
    print("wrote %s: %dx%d, %d bytes, sha256=%s"
          % (destination, width, height, len(blob), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
