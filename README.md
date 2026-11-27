# World News — Friday 27 November 2026

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/danielhutapea36/news-image-20261127-entry/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/danielhutapea36/news-image-20261127-entry/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

One 1024×1024 newspaper-style image that sums up Friday 27 November 2026's world news at a glance. This is my entry for the [news-image-20261127](https://make.fun/bounty/news-image-20261127) bounty on make.fun.

## What happened that day

1. **Thanksgiving storms black out 900,000+ in the US** — a nor'easter lashed the East Coast, cutting power and grounding flights; the Macy's parade was postponed for the first time in a century. BBC / Reuters
2. **Zelensky: US too focused on Middle East** — Ukraine's president told the BBC that delays to Patriot missile deliveries cost lives, and called Trump's friendship with Putin "strange". BBC
3. **Two Italians killed in strike on Kuwait site** — Rome and Kuwait blamed Iran for a drone attack on an air-defence station; Tehran denied any role. BBC / Reuters
4. **Guinea-Bissau delays elections by two years** — the military rulers extended the transition a year after the coup, pushing the polls to November 2028. Reuters
5. **Asia's big AI bet on Nvidia wobbles** — Asian chip stocks slid as Nvidia's boss returned as CEO and investors questioned AI valuations. BBC
6. **Also today:** a Hamas official was among eight killed in Gaza strikes; a pregnant US inmate escaped in a prison vehicle; Norse Atlantic suspended all flights; Depardieu is to stand trial. BBC / Reuters

## The image

- File: `entry.png`
- Dimensions: 1024×1024
- Size: 134833 bytes
- SHA-256: `cab0b43636961816b51529cfac8027c3364715e8a47ae8ff6f6632f1f725f83d`

## What the program does

The image was drawn offline during the build (Pillow) and committed here. `main.py` is deliberately boring: it copies the committed `entry.png` to the output directory — the approach the competition's own starter recommends ("the simplest program copies an image the repository holds").

That simplicity is the point. The grader runs the program in an environment where "standard library only: nothing is installed before it runs", so a program importing Pillow would fail there with `ModuleNotFoundError` even though it works on my machine. This program imports only `argparse`, `hashlib`, `os`, `struct`, `sys`, and `pathlib`, never touches the network, and is deterministic: the same committed bytes are copied on every run.

Before writing anything it checks the image: the PNG magic bytes, a 13-byte IHDR chunk, 1024×1024 dimensions, and a size of at most 1 MiB. After writing, it reads the output back and confirms the bytes match the committed image exactly.

## Running it

```bash
MAKEFUN_OUTPUT_DIR=/tmp/ni27-out python3 main.py
```

To inspect the committed image without writing anything:

```bash
python3 main.py --verify-only
```

`--out-dir` overrides `$MAKEFUN_OUTPUT_DIR`; with neither set, the program writes to `/output`. An explicitly set but empty `$MAKEFUN_OUTPUT_DIR` is an error.

## What a good run looks like

A successful run exits 0 and prints the path, size, and digest, for example:

```
wrote /tmp/ni27-out/entry.png: 1024x1024, 134833 bytes, sha256=cab0b43636961816b51529cfac8027c3364715e8a47ae8ff6f6632f1f725f83d
```

`--verify-only` exits 0 and prints the same size and digest for the committed image. Running again into a fresh directory produces byte-identical output.

## About make.fun

Built for the make.fun bounty platform — [make.fun](https://make.fun/?ref=danielhutapea36&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127).
