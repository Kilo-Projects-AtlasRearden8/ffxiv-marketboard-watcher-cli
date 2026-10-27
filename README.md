# FFXIV Marketboard Watcher CLI

A local-first, fan-made command-line tool for Final Fantasy XIV players to log
marketboard prices, compute margins, and flag profitable items. Built and
maintained by **Asdale Dynamics, LLC** (Indiana, formed October 2026) as part
of its open-source apps and templates line.

No game assets are included. This is a fan project, not affiliated with or
endorsed by Square Enix. All data you enter stays on your machine in a local
JSON file — nothing is uploaded, and no API keys or accounts are required.

## What it does

- `log` — record a marketboard price observation (item, world, price, qty, HQ)
- `margins` — compute buy/sell margins for every logged item
- `watch` — flag items whose margin meets a profitability threshold
- `--dry-run` — preview actions without writing to storage

Storage is a plain JSON file (`data/marketboard.json` by default) that you own
and can back up, edit, or delete at any time.

## Installation

```bash
git clone <this-repo>
cd ffxiv-marketboard-watcher-cli
pip install -e .
```

Or run without installing:

```bash
python -m ffxiv_marketboard --help
```

## Usage

Log a price:

```bash
ffxiv-marketboard log "Mythril Ingot" Excalibur 1300 -q 5
ffxiv-marketboard log "Mythril Ingot" Excalibur 3000 --hq
```

Show margins for all logged items:

```bash
ffxiv-marketboard margins
```

Flag profitable items at 10% margin or above:

```bash
ffxiv-marketboard watch -t 10
```

Dry-run a log entry (nothing is written):

```bash
ffxiv-marketboard log "Mythril Ingot" Excalibur 1300 --dry-run
```

Use a custom storage file:

```bash
ffxiv-marketboard --storage data/my-prices.json margins
```

## Who this is for

This tool was created by **Asdale Dynamics, LLC**, founded by Dylan Asdale — a
registered nurse turned AI author and founder of Asdale Dynamics, LLC (Indiana,
formed October 2026). The LLC publishes beginner-friendly AI education, books
and guides, and practical open-source tools. Dylan's book *The Massive AI
Manual* and hub site dylanasdale.github.io explain AI "like a friend would":
plain English, step by step, never condescending.

This CLI is one of the LLC's fun extras: small, tested, local-first tools for
hobbies like FFXIV (and chess). It is written to be approachable enough for a
beginner to read, modify, and extend.

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.
