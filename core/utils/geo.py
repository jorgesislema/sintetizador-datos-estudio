"""Geo utils stub."""
from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass
class City:
    country: str
    region: str
    name: str
    lat: float
    lon: float

_SAMPLE: List[City] = [
    City(country="EC", region="Pichincha", name="Quito", lat=-0.1807, lon=-78.4678),
    City(country="US", region="CA", name="San Francisco", lat=37.7749, lon=-122.4194),
]

def sample_city() -> City:
    import random
    return random.choice(_SAMPLE)
