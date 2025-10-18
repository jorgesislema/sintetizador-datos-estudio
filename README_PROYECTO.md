Proyecto de Datos: Prácticas ETL → EDA → ML → Dashboard

Objetivo: practicar extremo a extremo con datos sintéticos realistas.

Pasos rápidos (Windows PowerShell):

1) Crear entorno y activar
   python -m venv .venv_sintetizador
   .\.venv_sintetizador\Scripts\Activate

2) Instalar dependencias mínimas
   pip install -r requirements.txt
   # Opcional (ML/duckdb/etc.)
   pip install -r requirements-optional.txt

3) Generar datos con la app de escritorio (opcional)
   python run_ui_localized.py

4) Ejecutar pruebas rápidas
   pytest -q

Estructura sugerida de entregables:
- data/raw, data/processed, data/errors
- reports/etl_report.md, reports/eda_report.md, reports/ml_report.md
- logs/etl_*.log, logs/eda_*.log, logs/ml_*.log
- models/model.pkl
- dashboards/ (si aplica)

Utilidades:
- src/utils/reporting.py: utilidades de reporte/logs/errores.

Notas:
- Usar la app para generar una sesión con parámetros (rango de fechas, sucursales, volumen).
- No se cambia el esquema sin aprobación; vistas KPI se propondrán en sql/.
