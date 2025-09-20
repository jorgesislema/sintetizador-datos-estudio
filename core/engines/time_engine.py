"""Time series engine stub."""
from __future__ import annotations
import numpy as np
from typing import Dict, Any


def generate_time_series(length: int = 100, seasonal: bool = True) -> Dict[str, Any]:
    idx = np.arange(length)
    base = np.sin(idx / 12 * 2 * np.pi) if seasonal else np.zeros_like(idx)
    noise = np.random.normal(0, 0.2, size=length)
    values = base + noise
    return {"t": idx.tolist(), "value": values.tolist()}
