"""FX utils stub."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

@dataclass
class FXRate:
    base: str
    quote: str
    rate: float

_SAMPLE = {"USD": 1.0, "EUR": 1.08, "MXN": 18.0, "COP": 4000.0}

def get_fx_rate(base: str, quote: str) -> FXRate:
    if base not in _SAMPLE or quote not in _SAMPLE:
        raise ValueError("Moneda no soportada en stub")
    rate = _SAMPLE[quote] / _SAMPLE[base]
    return FXRate(base=base, quote=quote, rate=rate)
