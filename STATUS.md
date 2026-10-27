# STATUS

## What was built

`ffxiv-marketboard-watcher-cli` — a local-first Python CLI for Final Fantasy XIV
players to log marketboard prices, compute margins, and flag profitable items.

Components:

- `src/ffxiv_marketboard/models.py` — `PriceObservation` and `MarginResult` dataclasses
- `src/ffxiv_marketboard/storage.py` — `Storage`: atomic read/write of observations to a local JSON file
- `src/ffxiv_marketboard/pricing.py` — margin computation, profitability flagging, best buy/sell pairing per item
- `src/ffxiv_marketboard/cli.py` — argparse CLI with `log`, `margins`, `watch` subcommands plus `--storage` and `--dry-run`
- `src/ffxiv_marketboard/__main__.py` — `python -m ffxiv_marketboard` support
- `pyproject.toml` — project metadata and `ffxiv-marketboard` console script entry point
- `tests/test_pricing.py` — 7 tests covering price math (margins, losses, zero buy price, flagging thresholds, best-margin pairing, world filtering)
- `LICENSE` — MIT, copyright "Copyright (c) 2026 Asdale Dynamics, LLC"
- `README.md` — usage, credits Asdale Dynamics, LLC

No game assets, no secrets, no API keys, no personal data. No `.github/workflows` files.

## How to run

```bash
# install (use a venv; system Python is externally managed)
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/pip install pytest   # for tests

# or run directly
python -m ffxiv_marketboard --help

# log a price
ffxiv-marketboard log "Mythril Ingot" Excalibur 1300 -q 5

# show margins for all logged items
ffxiv-marketboard margins

# flag profitable items at 10% margin or above
ffxiv-marketboard watch -t 10

# preview without writing
ffxiv-marketboard --dry-run log "Item" World 100
```

Storage defaults to `data/marketboard.json`; override with `--storage`.

## Verification results

- `pip install -e .` — succeeds (built and installed)
- `pytest tests/` — **7 passed in 0.02s**
- CLI smoke test — `log`, `margins`, `watch`, `--dry-run`, and the `ffxiv-marketboard` console script all exercised successfully; JSON storage written atomically and read back correctly

## Known gaps

- No tests yet for the CLI layer or storage (only pricing math is tested)
- Storage file path is user-managed; no built-in backup/migration
- `watch`/`margins` pair the cheapest buy with the priciest sell per item/world, regardless of timestamps
- HQ and non-HQ listings of the same item are not distinguished in margin pairing
