"""Foreign key manager stub."""
from __future__ import annotations
from typing import Dict, List

class FKRegistry:
    def __init__(self):
        self._keys: Dict[str, List[str]] = {}

    def register(self, table: str, keys: List[str]):
        self._keys[table] = keys

    def get(self, table: str) -> List[str]:
        return self._keys.get(table, [])

REGISTRY = FKRegistry()
