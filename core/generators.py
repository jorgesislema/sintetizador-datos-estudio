"""Generic dataset generator based on schema definitions."""
from __future__ import annotations
from typing import List, Dict, Any
from datetime import datetime, UTC
import hashlib
import random

from core.utils.schemas import load_table_schema
from core.engines.faker_engine import generate_row
from core.utils.seed import set_seed
from core.utils.geo import sample_city
from core.utils.fx import get_fx_rate
from core.errors.profiles import apply_error_profile

_COMMON_EXCLUDE_HASH = {"record_hash", "dq_completeness_pct", "dq_validity_pct"}


def _compute_hash(row: Dict[str, Any]) -> str:
    h = hashlib.sha256()
    for k in sorted(row.keys()):
        if k in _COMMON_EXCLUDE_HASH:
            continue
        h.update(str(row[k]).encode())
    return h.hexdigest()


def generate(domain: str, table: str, rows: int, seed: int | None = None, error_profile: str = "none") -> List[Dict[str, Any]]:
    set_seed(seed)
    schema = load_table_schema(domain, table)
    fields = schema["fields"]

    out: List[Dict[str, Any]] = []
    batch_time = datetime.now(UTC).isoformat()
    city = sample_city()
    for i in range(rows):
        base = generate_row(fields)
        # Campos comunes completos (placeholder simple)
        if base.get("id") is None: base["id"] = i + 1
        if base.get("natural_key") is None:
            base["natural_key"] = base.get("employee_id") or base.get("transaction_id") or base.get("ticket_id") or base["id"]
        if base.get("tenant_id") is None: base["tenant_id"] = 1
        if base.get("source_system") is None: base["source_system"] = domain
        if base.get("source_table") is None: base["source_table"] = table
        if base.get("batch_id") is None: base["batch_id"] = 1
        if base.get("batch_time_utc") is None: base["batch_time_utc"] = batch_time
        if base.get("is_active") is None: base["is_active"] = True
        if base.get("valid_from_utc") is None: base["valid_from_utc"] = batch_time
        if base.get("valid_to_utc") is None: base["valid_to_utc"] = None
        if base.get("created_at_utc") is None: base["created_at_utc"] = batch_time
        if base.get("created_by") is None: base["created_by"] = "synthedata"
        if base.get("updated_at_utc") is None: base["updated_at_utc"] = batch_time
        if base.get("updated_by") is None: base["updated_by"] = "synthedata"
        if base.get("pii_sensitivity") is None: base["pii_sensitivity"] = "low"
        if base.get("geo_country") is None: base["geo_country"] = city.country
        if base.get("geo_region") is None: base["geo_region"] = city.region
        if base.get("geo_city") is None: base["geo_city"] = city.name
        if base.get("geo_lat") is None: base["geo_lat"] = city.lat
        if base.get("geo_lon") is None: base["geo_lon"] = city.lon
        if base.get("currency_code") is None: base["currency_code"] = "USD"
        fx = get_fx_rate("USD", "USD")
        if base.get("fx_rate_to_usd") is None: base["fx_rate_to_usd"] = fx.rate
        if base.get("processing_status") is None:
            base["processing_status"] = "ok"
        if base.get("tags") is None: base["tags"] = None
        if base.get("notes") is None: base["notes"] = None
        out.append(base)
    
    # Aplicar perfil de errores después de generar todas las filas
    if error_profile != "none":
        out = apply_error_profile(out, error_profile)
        # Actualizar processing_status para filas con errores
        for row in out:
            has_nulls = any(v is None for k, v in row.items() if k not in ["valid_to_utc", "tags", "notes"])
            if has_nulls:
                row["processing_status"] = "warn"
    
    # Calcular métricas DQ después de aplicar errores
    for row in out:
        non_null = sum(1 for f in fields if row.get(f) is not None)
        completeness = non_null / len(fields) if fields else 1.0
        row["dq_completeness_pct"] = round(completeness * 100, 2)
        row["dq_validity_pct"] = row["dq_completeness_pct"]  # placeholder
        row["record_hash"] = _compute_hash(row)
    
    return out
