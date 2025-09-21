"""PII hashing stub."""
from __future__ import annotations
import hashlib, os

def hash_value(value: str, salt_env: str = "SYNTHE_PII_SALT") -> str:
    salt = os.getenv(salt_env, "default_salt")
    h = hashlib.sha256()
    h.update(salt.encode())
    h.update(str(value).encode())
    return h.hexdigest()
