"""Distribution sampling stub."""
from __future__ import annotations
import numpy as np
from typing import Sequence


def normal(mean: float, std: float, n: int) -> Sequence[float]:
    return np.random.normal(mean, std, size=n)


def categorical(choices: Sequence[str], n: int):
    import random
    return [random.choice(choices) for _ in range(n)]
