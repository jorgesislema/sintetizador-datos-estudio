#!/usr/bin/env python3
"""Script de prueba para verificar el funcionamiento del sintetizador de datos"""

import sys
sys.path.insert(0, '.')

from core.utils.schemas import list_domains, list_tables, load_table_schema
from core.generators import generate

def test_domains_and_tables():
    """Probar que los dominios y tablas se cargan correctamente"""
    print("=== Probando dominios y tablas ===")
    
    domains = list_domains()
    print(f"Dominios encontrados: {len(domains)}")
    
    for domain, tables in domains.items():
        print(f"\n{domain.upper()}:")
        print(f"  Tablas: {len(tables)}")
        for i, table in enumerate(tables[:5]):  # Mostrar solo las primeras 5
            print(f"    {i+1}. {table}")
        if len(tables) > 5:
            print(f"    ... y {len(tables) - 5} más")

def test_table_schema():
    """Probar la carga de esquemas de tabla"""
    print("\n=== Probando carga de esquemas ===")
    
    try:
        schema = load_table_schema('enterprise', 'dim_employee')
        fields = list(schema['fields'].keys())
        print(f"dim_employee tiene {len(fields)} campos")
        print(f"Primeros 10 campos: {fields[:10]}")
        return True
    except Exception as e:
        print(f"Error cargando esquema: {e}")
        return False

def test_data_generation():
    """Probar la generación de datos"""
    print("\n=== Probando generación de datos ===")
    
    try:
        data = generate('enterprise', 'dim_employee', 3)
        print(f"Generados {len(data)} registros")
        if data:
            first_record = data[0]
            print(f"Campos en primer registro: {len(first_record)}")
            print(f"ID: {first_record.get('id')}")
            print(f"Employee ID: {first_record.get('employee_id')}")
            print(f"Source System: {first_record.get('source_system')}")
        return True
    except Exception as e:
        print(f"Error generando datos: {e}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("🔬 Sintetizador de Datos - Pruebas de Funcionamiento")
    print("=" * 50)
    
    test_domains_and_tables()
    schema_ok = test_table_schema()
    generation_ok = test_data_generation()
    
    print("\n=== Resumen ===")
    print(f"✅ Carga de esquemas: {'OK' if schema_ok else 'ERROR'}")
    print(f"✅ Generación de datos: {'OK' if generation_ok else 'ERROR'}")
    
    if schema_ok and generation_ok:
        print("\n🎉 Todas las pruebas pasaron correctamente!")
        print("La aplicación está lista para usar.")
    else:
        print("\n❌ Algunas pruebas fallaron.")

if __name__ == "__main__":
    main()