"""PII tagging stub."""
from __future__ import annotations
from typing import Dict
import re

_PATTERNS = {
    "email": re.compile(r"@"),
    "phone": re.compile(r"\d{7,}"),
}

def tag_field(name: str, sample_value: str | None) -> str | None:
    if sample_value is None:
        return None
    for tag, pattern in _PATTERNS.items():
        if pattern.search(sample_value):
            return tag
    return None
