"""Micro Retail Core generator stub."""
from __future__ import annotations
from typing import List, Dict, Any
from core.engines.faker_engine import generate_row

_FIELDS = ["first_name", "last_name", "email"]

def generate(rows: int) -> List[Dict[str, Any]]:
    return [generate_row(_FIELDS) for _ in range(rows)]
