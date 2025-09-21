"""Constraints stub."""
from __future__ import annotations
from typing import Dict, Any, Callable, List

Validator = Callable[[Dict[str, Any]], bool]

class ConstraintSet:
    def __init__(self):
        self._validators: List[Validator] = []

    def add(self, fn: Validator):
        self._validators.append(fn)

    def validate(self, row: Dict[str, Any]) -> bool:
        return all(v(row) for v in self._validators)
