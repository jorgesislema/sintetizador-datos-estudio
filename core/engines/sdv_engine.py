"""SDV engine stub (documentación placeholder)."""
from __future__ import annotations

class SDVNotInstalled(Exception):
    pass

try:  # pragma: no cover
    import sdv  # noqa: F401
    SDV_AVAILABLE = True
except Exception:  # pragma: no cover
    SDV_AVAILABLE = False


def train_model(tables: dict):  # placeholder
    if not SDV_AVAILABLE:
        raise SDVNotInstalled("SDV no instalado. Use extra [engines-ml].")
    # TODO: implementar entrenamiento multi-tabla
    return None
