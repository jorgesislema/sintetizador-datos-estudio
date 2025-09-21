"""Chunking stub."""
from __future__ import annotations
from typing import Iterator, Callable, Any

def chunk_generator(total: int, chunk_size: int, factory: Callable[[int, int], list[dict]]) -> Iterator[list[dict]]:
    offset = 0
    while offset < total:
        size = min(chunk_size, total - offset)
        yield factory(offset, size)
        offset += size
