# World News — Friday 27 November 2026

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/danielhutapea36/news-image-20261127-entry/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/danielhutapea36/news-image-20261127-entry/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

A newspaper front page for one day: Friday 27 November 2026, in a single 1024×1024 picture. My entry for the [news-image-20261127](https://make.fun/bounty/news-image-20261127) bounty on make.fun.

## The day in six stories

1. **Thanksgiving storms black out 900,000+ in the US** — a nor'easter battered the East Coast, knocking out power and grounding flights, and the Macy's parade was postponed for the first time in a century. (BBC / Reuters)
2. **Zelensky: US too focused on Middle East** — Ukraine's president told the BBC that hold-ups to Patriot missile deliveries are costing lives, and called Trump's friendship with Putin "strange". (BBC)
3. **Two Italians killed in strike on Kuwait site** — Rome and Kuwait blamed Iran for a drone attack on an air-defence station; Tehran denied any involvement. (BBC / Reuters)
4. **Guinea-Bissau delays elections by two years** — the military rulers stretched the transition a year after the coup, moving the polls to November 2028. (Reuters)
5. **Asia's big AI bet on Nvidia wobbles** — Asian chip stocks fell as Nvidia's boss came back as CEO and investors questioned AI valuations. (BBC)
6. **Also today:** a Hamas official was among eight people killed in Gaza strikes; a pregnant US inmate got away in a prison vehicle; Norse Atlantic grounded its fleet; Depardieu faces trial. (BBC / Reuters)

## The picture itself

The committed file is `entry.png`: a 1024×1024 PNG of 134833 bytes, SHA-256 `cab0b43636961816b51529cfac8027c3364715e8a47ae8ff6f6632f1f725f83d`.

## How the entry works

The picture was drawn offline while the entry was being built (Pillow) and committed here. `main.py` then does the simplest honest thing: it copies that committed `entry.png` to the output directory — the approach the competition's own starter suggests ("the simplest program copies an image the repository holds").

Keeping it that simple is deliberate. The grader runs the program where "standard library only: nothing is installed before it runs", so a program that imported Pillow would die there with `ModuleNotFoundError` even though it runs fine on my machine. This one imports only `hashlib`, `os`, and `sys`, makes no network calls, and is deterministic: the same committed bytes go out on every run.

Before it writes, it checks the picture: the PNG magic bytes, a 13-byte IHDR chunk, 1024×1024 dimensions, and at most 1 MiB. After it writes, it reads the output back and makes sure the bytes match the committed image exactly.

## Trying it out

```bash
MAKEFUN_OUTPUT_DIR=/tmp/ni27-check python3 main.py
```

To look at the committed image without writing anything:

```bash
python3 main.py --verify-only
```

`--out-dir` beats `$MAKEFUN_OUTPUT_DIR`; with neither set, the program writes to `/output`. An explicitly set but empty `$MAKEFUN_OUTPUT_DIR` is treated as an error.

## A good run

A good run exits 0 and prints where it wrote, how big the file is, and its digest:

```
wrote /tmp/ni27-check/entry.png: 1024x1024, 134833 bytes, sha256=cab0b43636961816b51529cfac8027c3364715e8a47ae8ff6f6632f1f725f83d
```

`--verify-only` exits 0 and prints the same size and digest for the committed image. Run it again somewhere else and the output is byte-identical.

## make.fun

Built for the make.fun bounty platform — [make.fun](https://make.fun/?ref=danielhutapea36&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127).
