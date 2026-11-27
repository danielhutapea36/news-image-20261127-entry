#!/usr/bin/env python3
"""news-image-20261127 entry program.

Reproduces the entry image: the repository holds the finished 1024x1024 PNG
(``entry.png``, drawn at build time), and this program copies it to the
output directory. Standard library only, no network, no clock, no randomness:
every run writes the same bytes.

Usage:
    MAKEFUN_OUTPUT_DIR=/tmp/ni27-out python3 main.py
    python3 main.py --out-dir /tmp/ni27-out
    python3 main.py --verify-only   # check the committed image, write nothing
"""

import argparse
import hashlib
import os
import struct
import sys
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1024 * 1024
IMAGE_NAME = "entry.png"


def source_path() -> Path:
    """Path of the committed image next to this program."""
    return Path(__file__).resolve().parent / IMAGE_NAME


def digest_of(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def inspect_png(data: bytes) -> tuple[int, int]:
    """Return (width, height) from the IHDR chunk, validating the container.

    Raises ValueError on anything that is not a well-formed PNG header.
    """
    if len(data) < 8 or data[:8] != PNG_SIGNATURE:
        raise ValueError("not a PNG file: bad signature")
    if len(data) < 33:
        raise ValueError("not a PNG file: too short for IHDR")
    chunk_len = struct.unpack(">I", data[8:12])[0]
    chunk_type = data[12:16]
    if chunk_type != b"IHDR" or chunk_len != 13:
        raise ValueError("not a PNG file: first chunk is not a 13-byte IHDR")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def load_committed_image() -> bytes:
    """Read the committed image and validate it before anything is written."""
    path = source_path()
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError(f"{IMAGE_NAME} is {len(data)} bytes, over the 1 MiB limit")
    width, height = inspect_png(data)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError(
            f"{IMAGE_NAME} is {width}x{height}, expected "
            f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )
    return data


def resolve_output_dir(cli_dir: str | None) -> Path:
    """--out-dir wins; then $MAKEFUN_OUTPUT_DIR; then /output.

    An explicitly set but empty $MAKEFUN_OUTPUT_DIR is an error.
    """
    if cli_dir:
        return Path(cli_dir)
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir is not None:
        if env_dir == "":
            raise ValueError("MAKEFUN_OUTPUT_DIR is set but empty")
        return Path(env_dir)
    return Path("/output")


def write_image(data: bytes, out_dir: Path) -> Path:
    """Copy the image bytes to out_dir and confirm the copy byte for byte."""
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / IMAGE_NAME
    with open(target, "wb") as handle:
        handle.write(data)
    written = target.read_bytes()
    if written != data:
        raise ValueError(f"wrote {target} but the bytes do not match the source")
    return target


def report(target: Path, data: bytes) -> str:
    """One-line summary of a successful write, with size and digest."""
    width, height = inspect_png(data)
    return (
        f"wrote {target}: {width}x{height}, {len(data)} bytes, "
        f"sha256={digest_of(data)}"
    )


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy the news-image-20261127 entry image to the output directory."
    )
    parser.add_argument("--out-dir", default=None,
                        help="output directory (overrides $MAKEFUN_OUTPUT_DIR)")
    parser.add_argument("--verify-only", action="store_true",
                        help="validate the committed image without writing anything")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        data = load_committed_image()
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if args.verify_only:
        print(
            f"verified {source_path()}: {len(data)} bytes, "
            f"sha256={digest_of(data)}"
        )
        return 0
    try:
        out_dir = resolve_output_dir(args.out_dir)
        target = write_image(data, out_dir)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(report(target, data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
