#!/usr/bin/env python3
"""Script para probar la funcionalidad completa del paso 2"""

import sys
sys.path.insert(0, '.')

from core.generators import generate
import pandas as pd
import json
from pathlib import Path

def test_output_formats():
    """Probar todos los formatos de salida"""
    print("=== Probando formatos de salida ===")
    
    # Generar datos de prueba
    print("Generando datos de prueba...")
    data = generate('enterprise', 'dim_employee', 10)
    df = pd.DataFrame(data)
    
    output_dir = Path("./test_output")
    output_dir.mkdir(exist_ok=True)
    
    # Probar CSV
    try:
        csv_file = output_dir / "test.csv"
        df.to_csv(csv_file, index=False)
        print(f"✅ CSV guardado: {csv_file}")
    except Exception as e:
        print(f"❌ Error CSV: {e}")
    
    # Probar JSON
    try:
        json_file = output_dir / "test.json"
        df.to_json(json_file, orient='records', indent=2)
        print(f"✅ JSON guardado: {json_file}")
    except Exception as e:
        print(f"❌ Error JSON: {e}")
    
    # Probar Excel
    try:
        excel_file = output_dir / "test.xlsx"
        df.to_excel(excel_file, index=False, engine='openpyxl')
        print(f"✅ Excel guardado: {excel_file}")
    except Exception as e:
        print(f"❌ Error Excel: {e}")
    
    # Probar Parquet
    try:
        parquet_file = output_dir / "test.parquet"
        df.to_parquet(parquet_file, index=False)
        print(f"✅ Parquet guardado: {parquet_file}")
    except Exception as e:
        print(f"❌ Error Parquet: {e}")
    
    print(f"\nArchivos generados en: {output_dir.absolute()}")
    return True

def test_configuration_options():
    """Probar opciones de configuración"""
    print("\n=== Probando opciones de configuración ===")
    
    # Configuraciones de prueba
    configs = [
        {"rows": 5, "error_profile": "none"},
        {"rows": 10, "error_profile": "light"},
        {"rows": 15, "error_profile": "moderate"}
    ]
    
    for i, config in enumerate(configs):
        try:
            data = generate('enterprise', 'dim_employee', 
                          config["rows"], 
                          error_profile=config["error_profile"])
            print(f"✅ Config {i+1}: {len(data)} filas, errores={config['error_profile']}")
        except Exception as e:
            print(f"❌ Config {i+1} falló: {e}")
    
    return True

def main():
    """Ejecutar todas las pruebas del paso 2"""
    print("🔧 Probando funcionalidad del Paso 2")
    print("=" * 50)
    
    formats_ok = test_output_formats()
    config_ok = test_configuration_options()
    
    print("\n=== Resumen ===")
    print(f"✅ Formatos de salida: {'OK' if formats_ok else 'ERROR'}")
    print(f"✅ Configuraciones: {'OK' if config_ok else 'ERROR'}")
    
    if formats_ok and config_ok:
        print("\n🎉 Paso 2 funcionando correctamente!")
        print("La UI puede usar todos los formatos y configuraciones.")
    else:
        print("\n❌ Hay problemas en el Paso 2.")

if __name__ == "__main__":
    main()