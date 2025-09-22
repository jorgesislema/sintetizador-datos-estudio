"""DuckDB writer stub."""
from __future__ import annotations
from pathlib import Path
from typing import Sequence, Mapping, Any

try:  # pragma: no cover
    import duckdb
except Exception:  # pragma: no cover
    duckdb = None  # type: ignore


def write_rows(db_path: Path, table: str, rows: Sequence[Mapping[str, Any]]):
    if duckdb is None or not rows:
        return
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(db_path))
    try:
        import pandas as pd  # local import
        df = pd.DataFrame(rows)
        con.register("tmp", df)
        con.execute(f"CREATE TABLE IF NOT EXISTS {table} AS SELECT * FROM tmp LIMIT 0;")
        con.execute(f"INSERT INTO {table} SELECT * FROM tmp;")
    finally:
        con.close()
