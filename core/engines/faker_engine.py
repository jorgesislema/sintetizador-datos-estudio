"""Motor Faker mejorado con heurísticas simples.

El objetivo es evitar valores None masivos en previews y datasets cuando
los nombres de campo no están mapeados explícitamente. Se aplican reglas
por nombre y sufijos/prefijos frecuentes.
"""
from __future__ import annotations
from typing import Dict, Any, Callable
import random
from datetime import datetime, timedelta, UTC

try:  # pragma: no cover
    from faker import Faker
except ImportError:  # pragma: no cover
    Faker = None  # type: ignore

_FAKE = Faker() if Faker else None
if _FAKE:
    _FAKE.seed_instance(42)

def _fake_or(default: str, attr: str) -> str:
    if _FAKE and hasattr(_FAKE, attr):
        return getattr(_FAKE, attr)()
    return default

def _rand_choice(opts):
    return random.choice(opts)

def _rand_numeric(min_v=0, max_v=1000):
    return random.randint(min_v, max_v)

def _rand_float(min_v=0, max_v=1000, nd=2):
    return round(random.uniform(min_v, max_v), nd)

def _rand_date(days_back=365):
    base = datetime.now(UTC)
    return (base - timedelta(days=random.randint(0, days_back))).isoformat()

GENERAL_MAP: Dict[str, Callable[[], Any]] = {
    # Identificadores genéricos
    "id": lambda: _rand_numeric(1, 10_000_000),
    "*_id": lambda: _rand_numeric(1, 10_000_000),
    "*_id_hash": lambda: hashlib_sha("id" + str(_rand_numeric())),
    "*_code": lambda: f"C{_rand_numeric(100,999)}",
    "*_number": lambda: f"N{_rand_numeric(1000,9999)}",
    # Nombres y descripciones
    "first_name": lambda: _fake_or("Name", "first_name"),
    "last_name": lambda: _fake_or("Last", "last_name"),
    "provider_name": lambda: _fake_or("Clinic", "company"),
    "procedure_name": lambda: _fake_or("Procedure", "bs"),
    "diagnosis_name": lambda: _fake_or("Diagnosis", "catch_phrase"),
    "branch_name": lambda: _fake_or("Branch", "city"),
    "site_name": lambda: _fake_or("Site", "street_name"),
    "channel_name": lambda: _fake_or("Channel", "word"),
    "visit_name": lambda: f"Visit {_rand_numeric(1,20)}",
    "product_line": lambda: _fake_or("Product", "word"),
    "policy_id": lambda: f"POL{_rand_numeric(1000,9999)}",
    "risk_factors": lambda: _rand_choice(["LOW", "MED", "HIGH"]),
    "specialty": lambda: _rand_choice(["CARDIO", "DERMA", "GEN", "PED" ]),
    "department": lambda: _rand_choice(["HR","FIN","OPS","IT"]),
    "chronic_conditions": lambda: _rand_choice(["NONE","DM2","HTA","ASTHMA"]),
    # Categorías
    "procedure_category": lambda: _rand_choice(["LAB","IMG","CONSULT","SURG"]),
    "encounter_type": lambda: _rand_choice(["INPATIENT","OUTPATIENT","ER"]),
    "gender": lambda: _rand_choice(["M","F"]),
    "phase": lambda: _rand_choice(["I","II","III","IV"]),
    "arm": lambda: _rand_choice(["A","B","C"]),
    "channel_type": lambda: _rand_choice(["VIDEO","PHONE","CHAT"]),
    "severity_level": lambda: _rand_choice(["LOW","MED","HIGH"]),
    "chronic_flag": lambda: _rand_choice(["Y","N"]),
    "abnormal_flag": lambda: _rand_choice(["Y","N"]),
    "related_to_study": lambda: _rand_choice(["Y","N"]),
    "completion_status": lambda: _rand_choice(["DONE","CANCEL","NO_SHOW"]),
    "payment_status": lambda: _rand_choice(["PAID","PENDING","LATE"]),
    "claim_status": lambda: _rand_choice(["OPEN","CLOSED","IN_REVIEW"]),
    # Valores numéricos
    "base_cost": lambda: _rand_float(50, 5000, 2),
    "duration_min": lambda: _rand_numeric(5, 480),
    "loan_amount": lambda: _rand_float(1000, 50000, 2),
    "interest_rate": lambda: _rand_float(0, 0.25, 4),
    "interest_rate_apr": lambda: _rand_float(0, 0.35, 4),
    "premium_amount": lambda: _rand_float(10, 1000, 2),
    "claim_amount": lambda: _rand_float(10, 15000, 2),
    "paid_amount": lambda: _rand_float(0, 15000, 2),
    "reserve_amount": lambda: _rand_float(0, 20000, 2),
    "risk_score": lambda: _rand_float(0, 1, 3),
    "fraud_score": lambda: _rand_float(0, 1, 3),
    "credit_score": lambda: _rand_numeric(300, 850),
    "pd_score": lambda: _rand_float(0, 1, 3),
    "medication_taken_pct": lambda: _rand_float(0,100,2),
    "compliance_score": lambda: _rand_float(0,100,2),
    "dose_mg": lambda: _rand_numeric(1,1000),
    "duration_days": lambda: _rand_numeric(1,180),
    "quantity": lambda: _rand_numeric(1,60),
    "refills": lambda: _rand_numeric(0,5),
    "rating": lambda: _rand_numeric(1,5),
    "nps_score": lambda: _rand_numeric(0,10),
    # Fechas (ISO)
    "start_date": lambda: _rand_date(900),
    "end_date": lambda: _rand_date(700),
    "admission_date": lambda: _rand_date(400),
    "discharge_date": lambda: _rand_date(400),
    "score_date": lambda: _rand_date(180),
    "assessment_date": lambda: _rand_date(180),
    "loss_date": lambda: _rand_date(400),
    "claim_date": lambda: _rand_date(400),
    "reserve_date": lambda: _rand_date(200),
    "measurement_date": lambda: _rand_date(180),
    "randomization_date": lambda: _rand_date(180),
    "visit_window_start": lambda: _rand_date(90),
    "visit_window_end": lambda: _rand_date(90),
    "appointment_date": lambda: _rand_date(60),
}

import hashlib
def hashlib_sha(seed: str) -> str:
    return hashlib.sha256(seed.encode()).hexdigest()[:16]

def _resolve_field(name: str) -> Any:
    # Coincidencia exacta primero
    if name in GENERAL_MAP:
        return GENERAL_MAP[name]()
    # Coincidencia por sufijo *_id, *_code, etc.
    if name.endswith("_id") and "*_id" in GENERAL_MAP:
        return GENERAL_MAP["*_id"]()
    if name.endswith("_id_hash") and "*_id_hash" in GENERAL_MAP:
        return GENERAL_MAP["*_id_hash"]()
    if name.endswith("_code") and "*_code" in GENERAL_MAP:
        return GENERAL_MAP["*_code"]()
    if name.endswith("_number") and "*_number" in GENERAL_MAP:
        return GENERAL_MAP["*_number"]()
    return None

def generate_row(field_names: list[str]) -> Dict[str, Any]:
    row: Dict[str, Any] = {}
    for f in field_names:
        row[f] = _resolve_field(f)
    return row
