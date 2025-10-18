#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de la interfaz Tkinter
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Probar importaciones"""
    try:
        import apps.ui_desktop.app as app
        print("✅ Módulo app importado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error importando app: {e}")
        return False

def test_domains():
    """Probar carga de dominios"""
    try:
        from pathlib import Path
        schemas_dir = Path("schemas")
        if schemas_dir.exists():
            domains = [d.name for d in schemas_dir.iterdir() if d.is_dir()]
            print(f"✅ Dominios encontrados: {domains}")
            return domains
        else:
            print("❌ Directorio schemas no encontrado")
            return []
    except Exception as e:
        print(f"❌ Error cargando dominios: {e}")
        return []

def test_schema_loading():
    """Probar carga de esquemas"""
    try:
        from core.utils.schemas import load_table_schema, list_tables
        
        # Obtener las tablas disponibles en enterprise
        tables = list_tables("enterprise")
        if tables:
            table_name = tables[0]  # Usar la primera tabla disponible
            schema = load_table_schema("enterprise", table_name)
            print(f"✅ Esquema {table_name} cargado correctamente")
            return True
        else:
            print("❌ No hay tablas disponibles en enterprise")
            return False
    except Exception as e:
        print(f"❌ Error cargando esquema: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🧪 Ejecutando pruebas de la interfaz Tkinter...")
    print("=" * 50)

    # Prueba 1: Importaciones
    print("\n1. Probando importaciones...")
    import_ok = test_imports()

    # Prueba 2: Dominios
    print("\n2. Probando carga de dominios...")
    domains = test_domains()

    # Prueba 3: Esquemas
    print("\n3. Probando carga de esquemas...")
    schema_ok = test_schema_loading()

    print("\n" + "=" * 50)
    if import_ok and domains and schema_ok:
        print("🎉 Todas las pruebas pasaron correctamente!")
        print("\n💡 Para ejecutar la interfaz gráfica:")
        print("   python launch_desktop.py")
        print("   # o")
        print("   python -c \"import sys; sys.path.insert(0, '.'); import apps.ui_desktop.app as app; app.main()\"")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    main()