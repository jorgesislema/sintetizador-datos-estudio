"""Seed utilities."""
from __future__ import annotations
import os, random
from typing import Optional

import numpy as np

_DEFAULT_ENV = "SYNTHE_SEED"

def set_seed(seed: Optional[int] = None) -> int:
    if seed is None:
        env_val = os.getenv(_DEFAULT_ENV)
        seed = int(env_val) if env_val is not None else 42
    random.seed(seed)
    np.random.seed(seed)
    return seed
