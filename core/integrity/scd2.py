"""SCD2 helper stub."""
from __future__ import annotations
from datetime import datetime, timedelta, UTC
from typing import Iterable, Dict, Any, List
import random

def scd2_version_rows(base_rows: Iterable[Dict[str, Any]], change_prob: float = 0.1) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for r in base_rows:
        current = r.copy()
        current["valid_from_utc"] = datetime.now(UTC).isoformat()
        current["valid_to_utc"] = None
        current["is_active"] = True
        out.append(current)
        if random.random() < change_prob:
            # Cerrar versión actual
            current["is_active"] = False
            current["valid_to_utc"] = datetime.now(UTC).isoformat()
            # Nueva versión
            new_version = current.copy()
            new_version["is_active"] = True
            new_version["valid_from_utc"] = datetime.now(UTC).isoformat()
            new_version["valid_to_utc"] = None
            # Intentar mutar un campo string no común
            for field, value in list(new_version.items()):
                if field in ("id","natural_key","created_at_utc","updated_at_utc","record_hash"):
                    continue
                if isinstance(value, str) and value and field.startswith("last_"):
                    new_version[field] = value + "_v2"
                    break
            out.append(new_version)
    return out
