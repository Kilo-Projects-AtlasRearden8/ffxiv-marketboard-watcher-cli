"""Tests for price math in ffxiv_marketboard.pricing."""

import pytest

from ffxiv_marketboard.models import PriceObservation
from ffxiv_marketboard.pricing import (
    best_margin_for_item,
    compute_margin,
    flag_profitable,
)


def _obs(item, world, price, hq=False):
    return PriceObservation(item_name=item, world=world, price=price, hq=hq)


def test_compute_margin_profitable():
    buy = _obs("Mythril Ingot", "Excalibur", 1000)
    sell = _obs("Mythril Ingot", "Excalibur", 1300)
    result = compute_margin(buy, sell, quantity=5)
    assert result.profit_per_unit == 300
    assert result.total_profit == 1500
    assert result.margin_percent == 30.0
    assert result.is_profitable(10.0) is True
    assert result.is_profitable(50.0) is False


def test_compute_margin_loss():
    buy = _obs("Mythril Ingot", "Excalibur", 1000)
    sell = _obs("Mythril Ingot", "Excalibur", 900)
    result = compute_margin(buy, sell, quantity=1)
    assert result.profit_per_unit == -100
    assert result.margin_percent == -10.0


def test_compute_margin_zero_buy_price():
    buy = _obs("Mythril Ingot", "Excalibur", 0)
    sell = _obs("Mythril Ingot", "Excalibur", 500)
    result = compute_margin(buy, sell)
    assert result.margin_percent == 0.0
    assert result.profit_per_unit == 500


def test_flag_profitable_threshold():
    results = [
        compute_margin(_obs("A", "W", 100), _obs("A", "W", 150)),  # 50%
        compute_margin(_obs("B", "W", 100), _obs("B", "W", 110)),  # 10%
        compute_margin(_obs("C", "W", 100), _obs("C", "W", 90)),   # -10%
    ]
    flagged = flag_profitable(results, min_margin_percent=10.0)
    assert len(flagged) == 2
    assert flagged[0].item_name == "A"
    assert flagged[1].item_name == "B"


def test_best_margin_for_item_picks_cheapest_buy_priciest_sell():
    observations = [
        _obs("Item X", "Excalibur", 5000),
        _obs("Item X", "Excalibur", 3000),
        _obs("Item X", "Excalibur", 8000),
        _obs("Item X", "Excalibur", 4000),
    ]
    result = best_margin_for_item(observations, "Item X", world="Excalibur")
    assert result is not None
    assert result.buy_price == 3000
    assert result.sell_price == 8000
    assert result.profit_per_unit == 5000


def test_best_margin_for_item_insufficient_data():
    observations = [_obs("Item X", "Excalibur", 5000)]
    assert best_margin_for_item(observations, "Item X") is None
    assert best_margin_for_item([], "Item X") is None


def test_best_margin_for_item_world_filter():
    observations = [
        _obs("Item X", "Excalibur", 1000),
        _obs("Item X", "Balmung", 9000),
        _obs("Item X", "Balmung", 10000),
    ]
    result = best_margin_for_item(observations, "Item X", world="Balmung")
    assert result is not None
    assert result.world == "Balmung"
    assert result.buy_price == 9000
    assert result.sell_price == 10000
