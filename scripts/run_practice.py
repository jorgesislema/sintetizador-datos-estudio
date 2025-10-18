from __future__ import annotations
"""Runner de práctica: ejecuta flujo ETL→EDA→ML con una sesión reciente.
Requisitos: haber generado una sesión con la app (outputs/session_*)."""
import subprocess
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'


def _run(cmd: list[str]):
    print('>',' '.join(cmd))
    res = subprocess.run(cmd, cwd=ROOT)
    if res.returncode != 0:
        sys.exit(res.returncode)


def main():
    # Verificar que hay datos
    out = ROOT / 'outputs'
    sessions = sorted([p for p in out.glob('session_*') if p.is_dir()])
    if not sessions:
        print('No hay sesiones en outputs/. Generar datos con la app primero.')
        sys.exit(1)
    print('Usando sesión:', sessions[-1].name)
    # Ejecutar notebooks en orden
    _run([sys.executable, '-m', 'jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', str(SRC/'etl.ipynb')])
    _run([sys.executable, '-m', 'jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', str(SRC/'eda.ipynb')])
    _run([sys.executable, '-m', 'jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace', str(SRC/'ml.ipynb')])
    print('Flujo completado. Revisar reports/ y models/.')


if __name__ == '__main__':
    main()
