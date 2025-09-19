from __future__ import annotations
from typing import Dict, List, Any
import numpy as np

ERROR_TYPES = {"nulls", "outliers", "typo", "duplicate"}

class ErrorProfile:
    def __init__(self, global_error_pct: float, mode: str = "cell", type_weights: Dict[str, float] | None = None):
        self.global_error_pct = global_error_pct
        self.mode = mode  # "cell" o "row"
        self.type_weights = type_weights or {t: 1 for t in ERROR_TYPES}

    def sample_error_types(self, n: int) -> List[str]:
        keys = list(self.type_weights.keys())
        weights = np.array([self.type_weights[k] for k in keys], dtype=float)
        weights = weights / weights.sum()
        return np.random.choice(keys, size=n, p=weights).tolist()

def inject_errors(data: Dict[str, List[Any]], profile: ErrorProfile) -> Dict[str, List[Any]]:
    if profile.global_error_pct <= 0:
        return data
    rows = len(next(iter(data.values()))) if data else 0
    cols = list(data.keys())
    total_cells = rows * len(cols)
    rng = np.random.default_rng()
    out = {k: list(v) for k, v in data.items()}

    if profile.mode == "cell":
        n_errors = int(total_cells * (profile.global_error_pct / 100.0))
        cell_indices = rng.choice(total_cells, size=n_errors, replace=False)
        err_types = profile.sample_error_types(n_errors)
        for idx, etype in zip(cell_indices, err_types):
            r = idx // len(cols)
            c = idx % len(cols)
            col = cols[c]
            out[col][r] = _mutate(out[col][r], etype)
    else:  # row mode
        n_rows_err = int(rows * (profile.global_error_pct / 100.0))
        row_indices = rng.choice(rows, size=n_rows_err, replace=False)
        err_types = profile.sample_error_types(n_rows_err)
        for r, etype in zip(row_indices, err_types):
            col = rng.choice(cols)
            out[col][r] = _mutate(out[col][r], etype)
    return out

def _mutate(value: Any, etype: str):
    if etype == "nulls":
        return None
    if etype == "outliers":
        if isinstance(value, (int, float)):
            return value * 10 if value not in (0, None) else 999999
        return value
    if etype == "typo":
        if isinstance(value, str) and value:
            pos = np.random.randint(0, len(value))
            return value[:pos] + "#" + value[pos + 1 :]
        return value
    if etype == "duplicate":
        return value  # duplicado se implementaría a nivel dataset
    return value
