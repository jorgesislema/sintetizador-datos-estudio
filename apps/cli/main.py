"""Typer CLI actualizado para generación dinámica."""
import typer
from pathlib import Path
import json
from typing import Optional

from core.utils import schemas as schema_utils
from core import generators as generic_gen
from core.dq import profiler, report
from core.writers import csv_writer, parquet_writer
from core.integrity.scd2 import scd2_version_rows
from core import multi as multi_gen

app = typer.Typer(help="SyntheData Suite CLI")

@app.command()
def list_domains():
    """Lista dominios disponibles."""
    typer.echo(json.dumps(schema_utils.list_domains(), indent=2))

@app.command()
def list_tables(domain: str):
    """Lista las tablas de un dominio."""
    typer.echo(json.dumps(schema_utils.list_tables(domain), indent=2))

@app.command()
def preview(domain: str, table: str, rows: int = 5, error_profile: str = "none"):
    """Previsualiza N filas con generación sintética."""
    data = generic_gen.generate(domain=domain, table=table, rows=rows, error_profile=error_profile)
    typer.echo(json.dumps(data, indent=2, ensure_ascii=False))

@app.command()
def generate(domain: str, table: str, rows: int = 1000, output: Path = Path("./outputs"), format: str = "parquet", error_profile: str = "none", dq_report: bool = True, seed: Optional[int] = None):
    """Genera dataset sintético basado en YAML schema."""
    data = generic_gen.generate(domain=domain, table=table, rows=rows, error_profile=error_profile, seed=seed)
    
    # Crear carpeta específica para la tabla
    table_output_dir = output / table
    table_output_dir.mkdir(parents=True, exist_ok=True)
    
    file_base = f"{domain}__{table}".lower()
    if format == "csv":
        csv_writer.write_rows(table_output_dir / f"{file_base}.csv", data)
    elif format == "parquet":
        parquet_writer.write_rows(table_output_dir / f"{file_base}.parquet", data)
    else:
        raise typer.BadParameter("Formato no soportado (csv|parquet)")
    if dq_report:
        metrics = profiler.profile(data)
        report.write_report(metrics, table_output_dir / f"{file_base}_dq_report.json")
    typer.echo(f"Generados {rows} registros en {table_output_dir} (formato={format})")

@app.command()
def generate_scd2(domain: str, table: str, rows: int = 100, change_prob: float = 0.2, output: Path = Path("./outputs"), error_profile: str = "none"):
    """Genera dataset con versiones SCD2 simples."""
    base = generic_gen.generate(domain=domain, table=table, rows=rows, error_profile=error_profile)
    versioned = scd2_version_rows(base, change_prob=change_prob)
    
    # Crear carpeta específica para la tabla
    table_output_dir = output / table
    table_output_dir.mkdir(parents=True, exist_ok=True)
    
    csv_writer.write_rows(table_output_dir / f"{domain}__{table}_scd2.csv", versioned)
    typer.echo(f"Generadas {len(versioned)} filas (incluyendo versiones) en {table_output_dir}")

@app.command()
def generate_multi(primary_domain: str, primary_table: str, secondary_domain: str, secondary_table: str, primary_rows: int = 50, secondary_rows: int = 200, scd2: bool=False, output: Path = Path("./outputs"), error_profile: str = "none"):
    """Genera dos tablas relacionadas (id -> FK)."""
    data = multi_gen.generate_two_tables(
        (primary_domain, primary_table, "id"),
        (secondary_domain, secondary_table, "employee_id" if secondary_table=="employees" else "customer_id"),
        primary_rows, secondary_rows, scd2=scd2, error_profile=error_profile
    )
    
    # Crear carpetas específicas para cada tabla
    for name, rows in data.items():
        table_output_dir = output / name
        table_output_dir.mkdir(parents=True, exist_ok=True)
        csv_writer.write_rows(table_output_dir / f"{primary_domain}__{name}.csv", rows)
    
    typer.echo(f"Generadas tablas: {', '.join(data.keys())} en carpetas separadas dentro de {output}")

if __name__ == "__main__":
    app()
