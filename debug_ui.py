#!/usr/bin/env python3
"""Script para depurar problemas en la UI"""

import sys
sys.path.insert(0, '.')

import tkinter as tk
from pathlib import Path

def test_ui_import():
    """Probar importación de la UI"""
    try:
        from apps.ui_desktop.app import DataSynthesizerApp
        print("✅ UI se importa correctamente")
        return True
    except Exception as e:
        print(f"❌ Error importando UI: {e}")
        return False

def test_ui_creation():
    """Probar creación de la aplicación UI"""
    try:
        from apps.ui_desktop.app import DataSynthesizerApp
        
        # Crear root window sin mostrarla
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana
        
        # Crear aplicación
        app = DataSynthesizerApp(root)
        print("✅ UI se crea correctamente")
        
        # Probar cargar dominios
        app.load_domains()
        print("✅ Dominios se cargan en UI")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Error creando UI: {e}")
        return False

def test_domain_loading():
    """Probar carga específica de dominios"""
    try:
        from core.utils.schemas import list_domains
        domains = list_domains()
        print(f"✅ Dominios disponibles: {list(domains.keys())}")
        
        for domain, tables in domains.items():
            print(f"  {domain}: {len(tables)} tablas")
            if len(tables) > 0:
                print(f"    Ejemplo: {tables[0]}")
        
        return True
    except Exception as e:
        print(f"❌ Error cargando dominios: {e}")
        return False

def test_table_schema_loading():
    """Probar carga de esquemas de tabla"""
    try:
        from core.utils.schemas import load_table_schema
        
        # Probar varias tablas
        test_cases = [
            ("enterprise", "dim_employee"),
            ("microbusiness", "dim_product"),
            ("retail", "dim_store"),
        ]
        
        for domain, table in test_cases:
            try:
                schema = load_table_schema(domain, table)
                fields_count = len(schema.get("fields", {}))
                print(f"✅ {domain}.{table}: {fields_count} campos")
            except Exception as e:
                print(f"❌ Error en {domain}.{table}: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Error general en esquemas: {e}")
        return False

def main():
    """Ejecutar todas las pruebas de depuración"""
    print("🔍 Depuración de problemas en UI")
    print("=" * 50)
    
    import_ok = test_ui_import()
    domain_ok = test_domain_loading()
    schema_ok = test_table_schema_loading()
    ui_ok = test_ui_creation()
    
    print("\n=== Resumen ===")
    print(f"✅ Importación UI: {'OK' if import_ok else 'ERROR'}")
    print(f"✅ Carga dominios: {'OK' if domain_ok else 'ERROR'}")
    print(f"✅ Carga esquemas: {'OK' if schema_ok else 'ERROR'}")
    print(f"✅ Creación UI: {'OK' if ui_ok else 'ERROR'}")
    
    if all([import_ok, domain_ok, schema_ok, ui_ok]):
        print("\n🎉 Todos los tests pasaron!")
        print("La UI debería funcionar correctamente.")
    else:
        print("\n❌ Hay problemas detectados.")

if __name__ == "__main__":
    main()