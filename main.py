#!/usr/bin/env python3
"""World News, Friday 27 November 2026 — entry program.

The finished newspaper image ships in this repository as ``entry.png``
(1024 by 1024 pixels, drawn offline while the entry was built). Running
this program copies that image into the output directory, after checking
that it is a well-formed PNG of the required size. Only the Python
standard library is used: nothing is fetched from the network, and no
clock or random source is consulted, so repeated runs produce identical
bytes.

Run it with an output directory:

    MAKEFUN_OUTPUT_DIR=/tmp/ni27-out python3 main.py
    python3 main.py --out-dir /tmp/ni27-out

Or inspect the committed image without writing anything:

    python3 main.py --verify-only

A bad image, a missing file, or an unwritable output directory makes the
program print an error and exit non-zero instead of writing anything.
"""

import argparse
import hashlib
import os
import struct
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
WANT_WIDTH = 1024
WANT_HEIGHT = 1024
BYTE_LIMIT = 1024 * 1024
IMAGE_FILE = "entry.png"


def bundled_image_path() -> Path:
    """Where the committed image lives, beside this program."""
    return Path(__file__).resolve().parent / IMAGE_FILE


def sha256_hex(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def png_dimensions(blob: bytes) -> tuple[int, int]:
    """Read (width, height) out of the IHDR chunk of a PNG byte string.

    The first eight bytes must be the PNG signature and the first chunk
    must be a 13-byte IHDR; anything else raises ValueError.
    """
    if len(blob) < 8 or blob[:8] != PNG_MAGIC:
        raise ValueError("not a PNG: wrong magic bytes")
    if len(blob) < 33:
        raise ValueError("not a PNG: too short to hold an IHDR chunk")
    first_len = struct.unpack(">I", blob[8:12])[0]
    first_kind = blob[12:16]
    if first_kind != b"IHDR" or first_len != 13:
        raise ValueError("not a PNG: first chunk is not a 13-byte IHDR")
    width, height = struct.unpack(">II", blob[16:24])
    return width, height


def read_bundled_image() -> bytes:
    """Load the committed image, refusing anything outside the gate."""
    blob = bundled_image_path().read_bytes()
    if len(blob) > BYTE_LIMIT:
        raise ValueError(
            f"{IMAGE_FILE} is {len(blob)} bytes, above the 1 MiB limit"
        )
    width, height = png_dimensions(blob)
    if (width, height) != (WANT_WIDTH, WANT_HEIGHT):
        raise ValueError(
            f"{IMAGE_FILE} is {width}x{height}, "
            f"expected {WANT_WIDTH}x{WANT_HEIGHT}"
        )
    return blob


def pick_output_folder(cli_folder: str | None) -> Path:
    """Decide where the image goes.

    The --out-dir flag wins. Otherwise $MAKEFUN_OUTPUT_DIR is used, and
    when that is unset the program writes to /output. An explicitly set
    but empty $MAKEFUN_OUTPUT_DIR is an error, not a silent default.
    """
    if cli_folder:
        return Path(cli_folder)
    env_folder = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_folder is not None:
        if not env_folder:
            raise ValueError("MAKEFUN_OUTPUT_DIR is set but empty")
        return Path(env_folder)
    return Path("/output")


def store_image(blob: bytes, folder: Path) -> Path:
    """Write the image bytes out and read them back to prove the copy."""
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / IMAGE_FILE
    with open(destination, "wb") as handle:
        handle.write(blob)
    if destination.read_bytes() != blob:
        raise ValueError(f"wrote {destination} but the bytes differ")
    return destination


def describe_write(destination: Path, blob: bytes) -> str:
    """One-line summary of a successful run: path, size and digest."""
    width, height = png_dimensions(blob)
    return (
        f"wrote {destination}: {width}x{height}, {len(blob)} bytes, "
        f"sha256={sha256_hex(blob)}"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Copy the news-image-20261127 entry image to the output directory."
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="output directory (overrides $MAKEFUN_OUTPUT_DIR)",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="validate the committed image without writing anything",
    )
    return parser


def run(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        blob = read_bundled_image()
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if args.verify_only:
        print(
            f"verified {bundled_image_path()}: {len(blob)} bytes, "
            f"sha256={sha256_hex(blob)}"
        )
        return 0
    try:
        folder = pick_output_folder(args.out_dir)
        destination = store_image(blob, folder)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(describe_write(destination, blob))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
