from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
import json
import math


# Mapeo simple de dtypes a descripciones en español
_DTYPE_ES = {
    "int64": "entero",
    "Int64": "entero (nullable)",
    "float64": "decimal",
    "Float64": "decimal (nullable)",
    "bool": "booleano",
    "boolean": "booleano (nullable)",
    "datetime64[ns]": "fecha/hora",
    "string": "texto",
    "object": "texto",
}

# Descripciones conocidas de campos comunes (inglés y español)
_COMMON_FIELD_DESCRIPTIONS = {
    # Inglés
    "id": "Identificador interno del registro",
    "natural_key": "Llave natural del registro (clave de negocio)",
    "tenant_id": "Identificador del inquilino/tenant",
    "source_system": "Nombre del sistema fuente del que proviene el registro",
    "source_table": "Nombre de la tabla fuente",
    "batch_id": "Identificador del lote/proceso de carga",
    "batch_time_utc": "Fecha/hora en UTC del lote de procesamiento",
    "record_hash": "Hash del registro para control de cambios/duplicados",
    "is_active": "Indicador de versión activa (SCD2)",
    "valid_from_utc": "Inicio de vigencia de la versión (UTC)",
    "valid_to_utc": "Fin de vigencia de la versión (UTC)",
    "created_at_utc": "Fecha/hora de creación del registro (UTC)",
    "created_by": "Usuario/proceso que creó el registro",
    "updated_at_utc": "Fecha/hora de última actualización (UTC)",
    "updated_by": "Usuario/proceso que actualizó el registro",
    "pii_sensitivity": "Nivel de sensibilidad de datos personales (PII)",
    "geo_country": "País (contexto geográfico)",
    "geo_region": "Región/estado (contexto geográfico)",
    "geo_city": "Ciudad (contexto geográfico)",
    "geo_lat": "Latitud",
    "geo_lon": "Longitud",
    "currency_code": "Código de moneda (ISO 4217)",
    "fx_rate_to_usd": "Tasa de cambio con respecto a USD",
    "processing_status": "Estado de procesamiento",
    "dq_completeness_pct": "Porcentaje de completitud (calidad de datos)",
    "dq_validity_pct": "Porcentaje de validez (calidad de datos)",
    "tags": "Etiquetas/metadata libre",
    "notes": "Notas/observaciones",

    # Español equivalentes frecuentes
    "esta_activo": "Indicador de versión activa (SCD2)",
    "valido_desde_utc": "Inicio de vigencia de la versión (UTC)",
    "valido_hasta_utc": "Fin de vigencia de la versión (UTC)",
    "moneda": "Código de moneda (ISO 4217)",
    "tasa_cambio_usd": "Tasa de cambio con respecto a USD",
    "estado_procesamiento": "Estado de procesamiento",
    "pii_sensibilidad": "Nivel de sensibilidad de datos personales (PII)",
}


def _format_percent(x: float | int | None) -> str:
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return "-"
    try:
        return f"{float(x) * 100:.2f}%" if x <= 1 else f"{float(x):.2f}%"
    except Exception:
        return "-"


def _read_table(path: Path, nrows: Optional[int] = None) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path, nrows=nrows)
    if suffix == ".json":
        return pd.read_json(path)
    if suffix == ".parquet":
        return pd.read_parquet(path)
    if suffix in (".xlsx", ".xls"): 
        return pd.read_excel(path)
    # Fallback: intentar CSV
    return pd.read_csv(path, nrows=nrows)


def _infer_dtype_es(series: pd.Series) -> str:
    dtype = str(series.dtype)
    # Detección básica de fechas si vienen como texto pero parecen ISO/fecha
    if dtype in ("object", "string"):
        sample = series.dropna().astype(str).head(20)
        if not sample.empty:
            if sample.str.match(r"\d{4}-\d{2}-\d{2}(?:[ T]\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?)?").mean() > 0.6:
                return "fecha/hora"
    return _DTYPE_ES.get(dtype, dtype)


def _first_non_null(series: pd.Series):
    try:
        val = series.dropna().iloc[0]
        if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
            return ""
        if isinstance(val, (dict, list)):
            return json.dumps(val, ensure_ascii=False)
        return str(val)
    except Exception:
        return ""


def _column_description(col: str) -> str:
    key = col.strip()
    return _COMMON_FIELD_DESCRIPTIONS.get(key, "")


def generate_data_dictionary_es(
    saved_files: Dict[str, Path],
    session_folder: Path,
    sample_rows: int = 1000
) -> Path:
    """Genera un diccionario de datos en español para los archivos guardados.

    Crea un índice global y un archivo por tabla en formato Markdown.

    Args:
        saved_files: Mapa {nombre_tabla: ruta_archivo}
        session_folder: Carpeta de la sesión en outputs
        sample_rows: Número máximo de filas a leer para inferencia de tipos/estadísticos

    Returns:
        Ruta de la carpeta creada con el diccionario
    """
    out_dir = Path(session_folder) / "data_dictionary_es"
    out_dir.mkdir(parents=True, exist_ok=True)

    index_lines: List[str] = ["# Diccionario de Datos (ES)", "", f"Carpeta de sesión: {Path(session_folder).name}", ""]
    index_lines += ["| Tabla | Registros | Archivo |", "|---|---:|---|"]

    for table_name, file_path in saved_files.items():
        file_path = Path(file_path)
        try:
            df = _read_table(file_path)
        except Exception as e:
            # Registrar fallo mínimo y continuar
            md_path = out_dir / f"{table_name}.md"
            md = [f"# {table_name}", "", f"No se pudo leer el archivo: {file_path}", f"Error: {e}"]
            md_path.write_text("\n".join(md), encoding="utf-8")
            index_lines.append(f"| {table_name} | - | {file_path.name} |")
            continue

        row_count = len(df)
        index_lines.append(f"| {table_name} | {row_count:,} | {file_path.name} |")

        # Reducir para muestreo y estadísticas ligeras
        df_sample = df.head(sample_rows)

        # Construir markdown por tabla
        lines: List[str] = [f"# {table_name}", "", f"Archivo: `{file_path.name}`", f"Registros: {row_count:,}", "", "## Columnas", ""]
        lines += ["| Columna | Tipo | Nulos % | Únicos | Ejemplo | Descripción |", "|---|---|---:|---:|---|---|"]

        for col in df_sample.columns:
            series = df_sample[col]
            tipo = _infer_dtype_es(series)
            null_pct = float(series.isna().mean()) if len(series) else 0.0
            nunique = int(series.nunique(dropna=True)) if len(series) else 0
            ejemplo = _first_non_null(series)
            desc = _column_description(str(col))
            lines.append(
                f"| {col} | {tipo} | {_format_percent(null_pct)} | {nunique:,} | {ejemplo} | {desc} |"
            )

        # Guardar archivo de la tabla
        out_file = out_dir / f"{table_name}.md"
        out_file.write_text("\n".join(lines), encoding="utf-8")

    # Guardar índice
    index_path = out_dir / "INDEX.md"
    index_path.write_text("\n".join(index_lines), encoding="utf-8")

    # Resumen JSON opcional para automatización
    summary = {
        "tables": [
            {"table": t, "file": str(Path(p).name)} for t, p in saved_files.items()
        ],
        "output_dir": str(out_dir),
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    return out_dir
