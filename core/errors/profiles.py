"""Error profiles for synthetic data generation.
Defines configurable error injection patterns: nulls, duplicates, typos, out_of_range.
"""
from __future__ import annotations
from typing import Dict, Any, List, Callable
import random
import string

# Perfiles predefinidos
ERROR_PROFILES = {
    "none": {
        "null_pct": 0.0,
        "duplicate_pct": 0.0,
        "typo_pct": 0.0,
        "out_of_range_pct": 0.0,
    },
    "light": {
        "null_pct": 0.05,
        "duplicate_pct": 0.02,
        "typo_pct": 0.03,
        "out_of_range_pct": 0.01,
    },
    "moderate": {
        "null_pct": 0.1,
        "duplicate_pct": 0.05,
        "typo_pct": 0.07,
        "out_of_range_pct": 0.03,
    },
    "heavy": {
        "null_pct": 0.2,
        "duplicate_pct": 0.1,
        "typo_pct": 0.15,
        "out_of_range_pct": 0.08,
    },
}

def get_profile(name: str) -> Dict[str, float]:
    """Get error profile by name."""
    return ERROR_PROFILES.get(name, ERROR_PROFILES["none"]).copy()

def apply_null_errors(rows: List[Dict[str, Any]], null_pct: float, exclude_fields: List[str] = None) -> List[Dict[str, Any]]:
    """Inject null errors randomly."""
    if exclude_fields is None:
        exclude_fields = ["id", "natural_key"]
    for row in rows:
        for field in row:
            if field not in exclude_fields and random.random() < null_pct:
                row[field] = None
    return rows

def apply_duplicate_errors(rows: List[Dict[str, Any]], duplicate_pct: float, key_fields: List[str] = None) -> List[Dict[str, Any]]:
    """Inject duplicate values in key fields."""
    if key_fields is None:
        key_fields = ["email_corp", "first_name", "last_name"]
    if not rows:
        return rows
    for field in key_fields:
        if field in rows[0]:
            values = [r[field] for r in rows if r[field] is not None]
            if values:
                for row in rows:
                    if random.random() < duplicate_pct and row[field] is not None:
                        row[field] = random.choice(values)
    return rows

def apply_typo_errors(rows: List[Dict[str, Any]], typo_pct: float, string_fields: List[str] = None) -> List[Dict[str, Any]]:
    """Inject typos in string fields."""
    if string_fields is None:
        string_fields = ["first_name", "last_name", "email_corp"]
    def add_typo(s: str) -> str:
        if len(s) < 2:
            return s
        pos = random.randint(0, len(s) - 1)
        typo_type = random.choice(["swap", "delete", "insert", "replace"])
        if typo_type == "swap" and pos < len(s) - 1:
            return s[:pos] + s[pos+1] + s[pos] + s[pos+2:]
        elif typo_type == "delete":
            return s[:pos] + s[pos+1:]
        elif typo_type == "insert":
            char = random.choice(string.ascii_lowercase)
            return s[:pos] + char + s[pos:]
        elif typo_type == "replace":
            char = random.choice(string.ascii_lowercase)
            return s[:pos] + char + s[pos+1:]
        return s
    for row in rows:
        for field in string_fields:
            if field in row and isinstance(row[field], str) and random.random() < typo_pct:
                row[field] = add_typo(row[field])
    return rows

def apply_out_of_range_errors(rows: List[Dict[str, Any]], out_of_range_pct: float, numeric_fields: List[str] = None) -> List[Dict[str, Any]]:
    """Inject out-of-range values in numeric fields."""
    if numeric_fields is None:
        numeric_fields = ["qty", "unit_price"]
    for row in rows:
        for field in numeric_fields:
            if field in row and isinstance(row[field], (int, float)) and random.random() < out_of_range_pct:
                # Make it out of range by multiplying by large factor or negative
                factor = random.choice([10, 100, -1, -10])
                row[field] = row[field] * factor
    return rows

def apply_error_profile(rows: List[Dict[str, Any]], profile_name: str) -> List[Dict[str, Any]]:
    """Apply a complete error profile to rows."""
    profile = get_profile(profile_name)
    rows = apply_null_errors(rows, profile["null_pct"])
    rows = apply_duplicate_errors(rows, profile["duplicate_pct"])
    rows = apply_typo_errors(rows, profile["typo_pct"])
    rows = apply_out_of_range_errors(rows, profile["out_of_range_pct"])
    return rows