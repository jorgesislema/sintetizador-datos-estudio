"""CSV writer stub."""
from __future__ import annotations
from pathlib import Path
from typing import Sequence, Mapping, Any
import csv


def write_rows(path: Path, rows: Sequence[Mapping[str, Any]]):
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
