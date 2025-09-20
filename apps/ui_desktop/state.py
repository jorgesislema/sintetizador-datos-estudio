"""State management stub for Streamlit wizard."""
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class UIState:
    step: int = 1
    selected_domain: str | None = None
    selected_tables: List[str] = field(default_factory=list)
    row_count: int = 1000
    error_profile: str = "none"
    engine: str = "faker"
    output_format: List[str] = field(default_factory=lambda: ["parquet"])
    output_dir: str = "outputs"
    generation_progress: float = 0.0
    last_run_report: Dict[str, Any] = field(default_factory=dict)

GLOBAL_STATE = UIState()
