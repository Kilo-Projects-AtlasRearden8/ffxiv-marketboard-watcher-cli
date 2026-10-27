"""Local JSON storage for marketboard price observations."""

from __future__ import annotations

import json
import os
from typing import List, Optional

from .models import PriceObservation


class Storage:
    """Reads and writes price observations to a local JSON file."""

    def __init__(self, path: str) -> None:
        self.path = path

    def _ensure_parent(self) -> None:
        parent = os.path.dirname(os.path.abspath(self.path))
        if parent and not os.path.isdir(parent):
            os.makedirs(parent, exist_ok=True)

    def load(self) -> List[PriceObservation]:
        """Load all observations from the JSON file."""
        if not os.path.exists(self.path):
            return []
        try:
            with open(self.path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (json.JSONDecodeError, OSError):
            return []
        if not isinstance(data, list):
            return []
        observations: List[PriceObservation] = []
        for entry in data:
            try:
                observations.append(PriceObservation.from_dict(entry))
            except (KeyError, TypeError, ValueError):
                continue
        return observations

    def save(self, observations: List[PriceObservation]) -> None:
        """Write all observations to the JSON file."""
        self._ensure_parent()
        payload = [obs.to_dict() for obs in observations]
        tmp_path = self.path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(tmp_path, self.path)

    def add(self, observation: PriceObservation) -> List[PriceObservation]:
        """Append one observation and persist the full list."""
        observations = self.load()
        observations.append(observation)
        self.save(observations)
        return observations

    def latest_for_item(
        self, item_name: str, world: Optional[str] = None
    ) -> List[PriceObservation]:
        """Return observations for an item, newest first."""
        observations = self.load()
        matches = [
            obs
            for obs in observations
            if obs.item_name.lower() == item_name.lower()
            and (world is None or obs.world.lower() == world.lower())
        ]
        matches.sort(key=lambda obs: obs.timestamp, reverse=True)
        return matches
