"""Pricing math: margins, profits, and profitability flags."""

from __future__ import annotations

from typing import List, Optional

from .models import MarginResult, PriceObservation


def compute_margin(
    buy: PriceObservation,
    sell: PriceObservation,
    quantity: int = 1,
) -> MarginResult:
    """Compute the margin between a buy observation and a sell observation.

    Returns a MarginResult with profit per unit, total profit, and margin
    percent ((sell - buy) / buy * 100). A buy price of zero yields a margin
    of 0.0 to avoid division by zero.
    """
    buy_price = int(buy.price)
    sell_price = int(sell.price)
    profit_per_unit = sell_price - buy_price
    total_profit = profit_per_unit * int(quantity)
    if buy_price > 0:
        margin_percent = (profit_per_unit / buy_price) * 100.0
    else:
        margin_percent = 0.0
    return MarginResult(
        item_name=sell.item_name,
        world=sell.world,
        buy_price=buy_price,
        sell_price=sell_price,
        quantity=int(quantity),
        profit_per_unit=profit_per_unit,
        total_profit=total_profit,
        margin_percent=round(margin_percent, 2),
        hq=sell.hq,
    )


def flag_profitable(
    results: List[MarginResult],
    min_margin_percent: float = 10.0,
) -> List[MarginResult]:
    """Return results whose margin meets or exceeds the threshold."""
    return [result for result in results if result.is_profitable(min_margin_percent)]


def best_margin_for_item(
    observations: List[PriceObservation],
    item_name: str,
    world: Optional[str] = None,
) -> Optional[MarginResult]:
    """Pair the cheapest buy with the priciest sell for one item.

    Returns None when there are fewer than two usable observations.
    """
    matches = [
        obs
        for obs in observations
        if obs.item_name.lower() == item_name.lower()
        and (world is None or obs.world.lower() == world.lower())
    ]
    if len(matches) < 2:
        return None
    buys = [obs for obs in matches if obs.price > 0]
    if not buys:
        return None
    buy = min(buys, key=lambda obs: obs.price)
    sell = max(matches, key=lambda obs: obs.price)
    if sell.price <= buy.price:
        return compute_margin(buy, sell, quantity=1)
    return compute_margin(buy, sell, quantity=1)
