"""Arrow writer stub."""
from __future__ import annotations
from pathlib import Path
from typing import Sequence, Mapping, Any

try:  # pragma: no cover
    import pyarrow as pa
    import pyarrow.feather as feather
except Exception:  # pragma: no cover
    pa = None  # type: ignore
    feather = None  # type: ignore


def write_rows(path: Path, rows: Sequence[Mapping[str, Any]]):
    if not rows or pa is None or feather is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    batch = pa.RecordBatch.from_pylist(list(rows))
    table = pa.Table.from_batches([batch])
    feather.write_feather(table, path)
