from __future__ import annotations
from pathlib import Path
import json
from datetime import datetime


def write_report(path: str | Path, title: str, summary: dict | None = None, details: str | None = None):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}", "", f"Fecha: {datetime.now().isoformat()}"]
    if summary:
        lines += ["", "## Resumen", "", json.dumps(summary, indent=2, ensure_ascii=False)]
    if details:
        lines += ["", "## Detalles", "", details]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def log_line(path: str | Path, message: str):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {message}\n")


def save_error_rows(path: str | Path, rows: list[dict]):
    import pandas as pd
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    return path
