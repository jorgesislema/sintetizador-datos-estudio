"""Schema loading and resolution utilities."""
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
import yaml

SCHEMAS_ROOT = Path("schemas")
_COMMON_FILE = SCHEMAS_ROOT / "_common.yml"

class SchemaError(Exception):
    pass

def _load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as e:  # pragma: no cover
        raise SchemaError(f"Archivo no encontrado: {path}") from e

def load_common_fields() -> List[str]:
    data = _load_yaml(_COMMON_FILE)
    return data.get("common_fields", [])

_DEF_CACHE: Dict[str, Any] = {}


def list_domains() -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {}
    if SCHEMAS_ROOT.exists():
        for domain_dir in SCHEMAS_ROOT.iterdir():
            if domain_dir.is_dir() and not domain_dir.name.startswith("_"):
                domain_name = domain_dir.name
                try:
                    tables = list_tables(domain_name)
                    if tables:  # Solo incluir dominios que tengan tablas
                        result[domain_name] = tables
                except:
                    # Si hay error cargando tablas, continuar con el siguiente dominio
                    continue
    return result


def list_tables(domain: str) -> List[str]:
    domain_path = SCHEMAS_ROOT / domain
    if not domain_path.exists() or not domain_path.is_dir():
        raise SchemaError(f"Dominio {domain} no encontrado")
    
    tables = []
    
    # Buscar primero en el archivo principal del dominio
    main_file = domain_path / f"{domain}.yml"
    if main_file.exists():
        try:
            data = _load_yaml(main_file)
            if "tables" in data:
                tables.extend(list(data["tables"].keys()))
                return tables  # Si encontramos el archivo principal, usamos solo ese
        except:
            pass
    
    # Si no hay archivo principal, buscar en archivos individuales
    for yaml_file in domain_path.glob("*.yml"):
        if yaml_file.name.startswith("_"):
            continue
        try:
            data = _load_yaml(yaml_file)
            if "tables" in data:
                tables.extend(list(data["tables"].keys()))
        except:
            continue
    
    return tables


def load_table_schema(domain: str, table: str) -> Dict[str, Any]:
    domain_path = SCHEMAS_ROOT / domain
    if not domain_path.exists() or not domain_path.is_dir():
        raise SchemaError(f"Dominio {domain} no encontrado")
    
    # Buscar primero en el archivo principal del dominio
    main_file = domain_path / f"{domain}.yml"
    if main_file.exists():
        try:
            data = _load_yaml(main_file)
            if "tables" in data and table in data["tables"]:
                table_def = data["tables"][table]
                fields = _expand_fields(table_def.get("fields", []))
                return {"fields": {field: {"type": "string", "description": ""} for field in fields}}
        except:
            pass
    
    # Si no se encuentra en el archivo principal, buscar en archivos individuales
    for yaml_file in domain_path.glob("*.yml"):
        if yaml_file.name.startswith("_") or yaml_file.name == f"{domain}.yml":
            continue
        try:
            data = _load_yaml(yaml_file)
            if "tables" in data and table in data["tables"]:
                table_def = data["tables"][table]
                fields = _expand_fields(table_def.get("fields", []))
                return {"fields": {field: {"type": "string", "description": ""} for field in fields}}
        except:
            continue
    
    raise SchemaError(f"Tabla {table} no encontrada en dominio {domain}")


def _expand_fields(raw_fields: List[Any]) -> List[str]:
    # Flatten anchor expansion: currently *common_fields stored as literal if unresolved
    common = set(load_common_fields())
    out: List[str] = []
    for item in raw_fields:
        if isinstance(item, str) and item.strip() in ("*common_fields", "'*common_fields'", '"*common_fields"'):
            # expand manual anchor token
            out.extend(common)
        elif isinstance(item, str):
            out.append(item)
    # deduplicate preserving order
    seen = set()
    dedup: List[str] = []
    for f in out:
        if f not in seen:
            seen.add(f)
            dedup.append(f)
    return dedup


def _resolve_domain_path(domain: str) -> Path:
    # Buscar en todos los dominios disponibles
    if SCHEMAS_ROOT.exists():
        for domain_dir in SCHEMAS_ROOT.iterdir():
            if domain_dir.is_dir() and domain_dir.name == domain:
                domain_file = domain_dir / f"{domain}.yml"
                if domain_file.exists():
                    return domain_file
                # Si no hay archivo de dominio general, buscar archivos de tabla individuales
                table_files = list(domain_dir.glob("*.yml"))
                if table_files:
                    # Usar el primer archivo encontrado como archivo de dominio
                    return table_files[0]
    raise SchemaError(f"Dominio {domain} no encontrado")
