"""Multiprocessing stub."""
from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor
from typing import Callable, Any, Iterable, List


def parallel_map(fn: Callable[[Any], Any], items: Iterable[Any], workers: int = 2) -> List[Any]:
    with ProcessPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(fn, items))
