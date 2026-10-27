"""Data models for marketboard observations and margin results."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class PriceObservation:
    """A single marketboard price observation recorded by the user."""

    item_name: str
    world: str
    price: int
    quantity: int = 1
    hq: bool = False
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    source: str = "manual"

    def to_dict(self) -> dict:
        return {
            "item_name": self.item_name,
            "world": self.world,
            "price": self.price,
            "quantity": self.quantity,
            "hq": self.hq,
            "timestamp": self.timestamp,
            "source": self.source,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PriceObservation":
        return cls(
            item_name=data["item_name"],
            world=data["world"],
            price=int(data["price"]),
            quantity=int(data.get("quantity", 1)),
            hq=bool(data.get("hq", False)),
            timestamp=str(data.get("timestamp", "")),
            source=str(data.get("source", "manual")),
        )


@dataclass
class MarginResult:
    """The computed margin between a buy and a sell observation."""

    item_name: str
    world: str
    buy_price: int
    sell_price: int
    quantity: int
    profit_per_unit: int
    total_profit: int
    margin_percent: float
    hq: bool = False

    def to_dict(self) -> dict:
        return {
            "item_name": self.item_name,
            "world": self.world,
            "buy_price": self.buy_price,
            "sell_price": self.sell_price,
            "quantity": self.quantity,
            "profit_per_unit": self.profit_per_unit,
            "total_profit": self.total_profit,
            "margin_percent": self.margin_percent,
            "hq": self.hq,
        }

    def is_profitable(self, min_margin_percent: float = 0.0) -> bool:
        return self.margin_percent >= min_margin_percent
