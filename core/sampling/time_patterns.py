"""Time pattern sampling stub."""
from __future__ import annotations
import numpy as np


def daily_seasonality(days: int = 30):
    idx = np.arange(days)
    return (np.sin(idx / 7 * 2 * np.pi) + 1) / 2
