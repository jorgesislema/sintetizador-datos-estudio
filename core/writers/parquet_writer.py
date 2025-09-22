"""Parquet writer stub."""
from __future__ import annotations
from pathlib import Path
from typing import Sequence, Mapping, Any

try:  # pragma: no cover
    import pandas as pd
except ImportError:  # pragma: no cover
    pd = None  # type: ignore


def write_rows(path: Path, rows: Sequence[Mapping[str, Any]]):
    if not rows or pd is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_parquet(path, index=False)
