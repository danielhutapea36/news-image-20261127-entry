# World News — Friday 27 November 2026

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/danielhutapea36/news-image-20261127-entry/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/danielhutapea36/news-image-20261127-entry/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

An entry for the [news-image-20261127](https://make.fun/bounty/news-image-20261127) bounty on make.fun: a single 1024×1024 news image summarising the day's world headlines, built to be read at a glance.

## The six stories

1. **Thanksgiving storms black out 900,000+ in the US** — BBC / Reuters
2. **Zelensky: US too focused on Middle East** — BBC
3. **Two Italians killed in strike on Kuwait site** — BBC / Reuters
4. **Guinea-Bissau delays elections by two years** — Reuters
5. **Asia's big AI bet on Nvidia wobbles** — BBC
6. **Also today:** Hamas official among eight killed in Gaza strikes; pregnant US inmate escapes in prison vehicle; Norse Atlantic suspends all flights; Depardieu to stand trial — BBC / Reuters

## The image

- File: `entry.png`
- Dimensions: 1024×1024
- Size: 134833 bytes
- SHA-256: `cab0b43636961816b51529cfac8027c3364715e8a47ae8ff6f6632f1f725f83d`

## How it works

The PNG was drawn during the build (Pillow, offline) and committed to this repository. The entry program itself (`main.py`) is standard-library-only: it simply copies the committed `entry.png` to the output directory — the pattern the competition's own starter uses ("the simplest program copies an image the repository holds").

This matters because the grader runs the program in an environment where "standard library only: nothing is installed before it runs". A program that imports Pillow would fail there with `ModuleNotFoundError` even though it works locally. This entry program imports only `argparse`, `hashlib`, `os`, `struct`, `sys`, and `pathlib`, makes no network calls, and is fully deterministic: the same committed bytes are copied every run.

Before writing, the program verifies the image: PNG magic bytes, a 13-byte IHDR chunk, 1024×1024 dimensions, and size at most 1 MiB. After copying, it reads the output back and checks the bytes match the committed image exactly.

## Run it

```bash
MAKEFUN_OUTPUT_DIR=/tmp/ni27-out python3 main.py
```

Or check the committed image without writing anything:

```bash
python3 main.py --verify-only
```

`--out-dir` overrides `$MAKEFUN_OUTPUT_DIR`; if neither is set, the program writes to `/output`. An explicitly set but empty `$MAKEFUN_OUTPUT_DIR` is an error.

## Verification

A successful run exits 0 and prints the output path, byte count, and digest, for example:

```
wrote /tmp/ni27-out/entry.png: 134833 bytes, sha256=cab0b43636961816b51529cfac8027c3364715e8a47ae8ff6f6632f1f725f83d
```

`--verify-only` exits 0 and prints the same size and digest for the committed image. Re-running into a fresh directory produces byte-identical output.

## About make.fun

Built for the make.fun bounty platform — [make.fun](https://make.fun/?ref=danielhutapea36&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127).
