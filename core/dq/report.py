"""DQ report writer stub."""
from __future__ import annotations
from pathlib import Path
from typing import Any, Dict
import json


def write_report(metrics: Dict[str, Any], path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metrics, indent=2))
