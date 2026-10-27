"""Command-line interface for the FFXIV Marketboard Watcher."""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from .models import MarginResult
from .pricing import best_margin_for_item, compute_margin, flag_profitable
from .storage import Storage


def _fmt_gil(amount: int) -> str:
    return f"{amount:,} gil"


def cmd_log(args: argparse.Namespace) -> int:
    storage = Storage(args.storage)
    from .models import PriceObservation

    observation = PriceObservation(
        item_name=args.item,
        world=args.world,
        price=args.price,
        quantity=args.quantity,
        hq=args.hq,
        source="dry-run" if args.dry_run else "manual",
    )
    if args.dry_run:
        print(f"[dry-run] would log: {observation.item_name} on {observation.world}")
        print(f"[dry-run] {_fmt_gil(observation.price)} x {observation.quantity}")
        print(f"[dry-run] storage path: {storage.path} (not written)")
        return 0
    storage.add(observation)
    print(f"Logged {_fmt_gil(observation.price)} for {observation.item_name} on {observation.world}")
    return 0


def cmd_margins(args: argparse.Namespace) -> int:
    storage = Storage(args.storage)
    observations = storage.load()
    if not observations:
        print("No observations stored yet. Use 'log' to record prices first.")
        return 0

    items: dict = {}
    for obs in observations:
        items.setdefault(obs.item_name.lower(), []).append(obs)

    results: List[MarginResult] = []
    for item_name, obs_list in items.items():
        result = best_margin_for_item(
            obs_list, item_name, world=args.world if args.world else None
        )
        if result is not None:
            results.append(result)

    results.sort(key=lambda r: r.margin_percent, reverse=True)

    print(f"{'Item':<30} {'World':<18} {'Buy':>9} {'Sell':>9} {'Profit':>10} {'Margin':>8}")
    print("-" * 88)
    for result in results:
        print(
            f"{result.item_name:<30} {result.world:<18} "
            f"{_fmt_gil(result.buy_price):>9} {_fmt_gil(result.sell_price):>9} "
            f"{_fmt_gil(result.profit_per_unit):>10} {result.margin_percent:>7.2f}%"
        )
    return 0


def cmd_watch(args: argparse.Namespace) -> int:
    storage = Storage(args.storage)
    observations = storage.load()
    if not observations:
        print("No observations stored yet. Use 'log' to record prices first.")
        return 0

    items: dict = {}
    for obs in observations:
        items.setdefault(obs.item_name.lower(), []).append(obs)

    results: List[MarginResult] = []
    for item_name, obs_list in items.items():
        result = best_margin_for_item(
            obs_list, item_name, world=args.world if args.world else None
        )
        if result is not None:
            results.append(result)

    profitable = flag_profitable(results, min_margin_percent=args.threshold)
    profitable.sort(key=lambda r: r.margin_percent, reverse=True)

    if not profitable:
        print(f"No items flagged profitable at {args.threshold}% margin or above.")
        return 0

    print(f"Profitable items (>= {args.threshold}% margin):")
    print(f"{'Item':<30} {'World':<18} {'Buy':>9} {'Sell':>9} {'Profit':>10} {'Margin':>8}")
    print("-" * 88)
    for result in profitable:
        print(
            f"{result.item_name:<30} {result.world:<18} "
            f"{_fmt_gil(result.buy_price):>9} {_fmt_gil(result.sell_price):>9} "
            f"{_fmt_gil(result.profit_per_unit):>10} {result.margin_percent:>7.2f}%"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ffxiv-marketboard",
        description="Log FFXIV marketboard prices, compute margins, flag profitable items.",
    )
    parser.add_argument(
        "--storage",
        default="data/marketboard.json",
        help="Path to the local JSON storage file (default: data/marketboard.json)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without writing to storage",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    log_parser = subparsers.add_parser("log", help="Record a price observation")
    log_parser.add_argument("item", help="Item name")
    log_parser.add_argument("world", help="World / datacenter name")
    log_parser.add_argument("price", type=int, help="Price in gil")
    log_parser.add_argument(
        "-q", "--quantity", type=int, default=1, help="Quantity (default: 1)"
    )
    log_parser.add_argument(
        "--hq", action="store_true", help="Mark the observation as high quality"
    )
    log_parser.set_defaults(func=cmd_log)

    margins_parser = subparsers.add_parser(
        "margins", help="Show computed margins for logged items"
    )
    margins_parser.add_argument(
        "-w", "--world", help="Filter results to a specific world"
    )
    margins_parser.set_defaults(func=cmd_margins)

    watch_parser = subparsers.add_parser(
        "watch", help="Flag profitable items above a margin threshold"
    )
    watch_parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=10.0,
        help="Minimum margin percent to flag (default: 10.0)",
    )
    watch_parser.add_argument(
        "-w", "--world", help="Filter results to a specific world"
    )
    watch_parser.set_defaults(func=cmd_watch)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
