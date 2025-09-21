"""Generación multi-tabla sencilla con soporte opcional SCD2 para tabla primaria."""
from __future__ import annotations
from typing import Dict, Any, List, Tuple
from core.generators import generate
from core.integrity.scd2 import scd2_version_rows

def generate_two_tables(primary: Tuple[str,str,str], secondary: Tuple[str,str,str], primary_rows: int, secondary_rows: int, scd2: bool=False, error_profile: str = "none") -> Dict[str,List[Dict[str,Any]]]:
    p_domain, p_table, p_fk_field = primary
    s_domain, s_table, s_ref_field = secondary
    prim = generate(p_domain, p_table, primary_rows, error_profile=error_profile)
    if scd2:
        prim = scd2_version_rows(prim)
    # crear índice de ids primarios
    prim_ids = [r["id"] for r in prim if r.get("id") is not None]
    sec = generate(s_domain, s_table, secondary_rows, error_profile=error_profile)
    # asignar FK simple round-robin
    for i, r in enumerate(sec):
        if prim_ids:
            r[s_ref_field] = prim_ids[i % len(prim_ids)]
    return {p_table: prim, s_table: sec}
