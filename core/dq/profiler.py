"""Simple DQ profiler stub."""
from __future__ import annotations
from typing import Sequence, Mapping, Any, Dict
from collections import Counter


def profile(rows: Sequence[Mapping[str, Any]]) -> Dict[str, Dict[str, float]]:
    if not rows:
        return {}
    columns = rows[0].keys()
    total = len(rows)
    result: Dict[str, Dict[str, float]] = {}
    for c in columns:
        values = [r[c] for r in rows if r[c] is not None]
        non_null = len(values)
        completeness = non_null / total
        cnt = Counter(values)
        unique_non_null = sum(1 for v, k in cnt.items() if k == 1)
        duplicates = sum(k for k in cnt.values() if k > 1) - (len([k for k in cnt.values() if k > 1]))
        uniqueness_ratio = unique_non_null / non_null if non_null else 0.0
        # Validity simplificada = completeness (placeholder)
        result[c] = {
            "completeness": completeness,
            "validity": completeness,
            "duplicates_count": float(duplicates),
            "uniqueness_ratio": uniqueness_ratio,
        }
    return result
