import typer
from rich import print
from core.utils.schema_loader import SchemaLoader
from core.engines.vector_engine import VectorEngine
from core.engines.faker_engine import FakerEngine
from core.dq.error_injection import ErrorProfile, inject_errors
import pandas as pd
from generators.enterprise.hr_core import generate_hr_core

app = typer.Typer(help="CLI para generación de datos sintéticos")
loader = SchemaLoader()

@app.command()
def list_domains():
    print(loader.list_domains())

@app.command()
def list_tables(domain: str, category: str = "enterprise"):
    schema = loader.load_domain(domain, category)
    print(list(schema.get("entities", {}).keys()))

@app.command()
def preview(domain: str = "hr_core", rows: int = 5, engine: str = "vector"):
    if domain == "hr_core":
        tables = generate_hr_core(rows=rows, engine_name=engine)
        for name, df in tables.items():
            print(f"[bold]{name}[/bold]")
            print(df.head())

@app.command()
def generate(domain: str = "hr_core", rows: int = 1000, output: str = "outputs", engine: str = "vector", error_pct: float = 0.0):
    tables = generate_hr_core(rows=rows, engine_name=engine)
    if error_pct > 0:
        profile = ErrorProfile(global_error_pct=error_pct)
        # aplicar a cada tabla
        for tname, df in tables.items():
            mutated = inject_errors(df.to_dict(orient="list"), profile)
            tables[tname] = pd.DataFrame(mutated)
    # escritura simple CSV
    for name, df in tables.items():
        df.to_csv(f"{output}/{name}.csv", index=False)
    print(f"Generadas tablas: {list(tables.keys())} en {output}")

if __name__ == "__main__":
    app()
