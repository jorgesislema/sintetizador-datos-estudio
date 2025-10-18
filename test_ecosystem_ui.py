#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de ecosistemas en la UI
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

def test_ecosystem_imports():
    """Probar que las importaciones de ecosistemas funcionan"""
    print("🔍 Probando importaciones de ecosistemas...")
    
    try:
        from core.ecosystems import (
            get_available_ecosystem_options,
            generate_ecosystem_data,
            BUSINESS_ECOSYSTEMS
        )
        print("✅ Importaciones de ecosistemas exitosas")
        
        # Probar opciones disponibles
        options = get_available_ecosystem_options()
        print(f"📊 Ecosistemas disponibles: {len(options)}")
        for key, name in options.items():
            print(f"   - {key}: {name}")
            
        return True
        
    except ImportError as e:
        print(f"❌ Error en importaciones: {e}")
        return False

def test_ecosystem_generation():
    """Probar generación básica de ecosistema"""
    print("\n🏗️ Probando generación de ecosistema...")
    
    try:
        from core.ecosystems import generate_ecosystem_data
        
        # Generar un ecosistema pequeño
        data, summary = generate_ecosystem_data("social_media_influencer", 10, False)
        
        print("✅ Generación de ecosistema exitosa")
        print(f"📊 Tablas generadas: {len(data)}")
        print(f"📈 Total de registros: {summary.get('total_records', 'N/A')}")
        
        for table_name, table_data in data.items():
            print(f"   - {table_name}: {len(table_data)} registros")
            
        return True
        
    except Exception as e:
        print(f"❌ Error en generación: {e}")
        return False

def test_ui_compatibility():
    """Probar compatibilidad con el sistema UI"""
    print("\n🖥️ Probando compatibilidad con UI...")
    
    try:
        from apps.ui_desktop.app import DataSynthesizerApp
        import tkinter as tk
        
        # Crear instancia temporal de UI
        root = tk.Tk()
        app = DataSynthesizerApp(root)
        root.withdraw()  # Ocultar ventana
        
        # Verificar que tenga los métodos necesarios
        required_methods = [
            'create_ecosystem_mode_widgets',
            'generate_ecosystem_complete',
            'show_ecosystem_results'
        ]
        
        for method in required_methods:
            if hasattr(app, method):
                print(f"✅ Método {method} disponible")
            else:
                print(f"❌ Método {method} faltante")
                return False
        
        root.destroy()
        print("✅ UI compatible con ecosistemas")
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba UI: {e}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("🚀 INICIANDO PRUEBAS DE ECOSISTEMAS\n")
    
    tests = [
        test_ecosystem_imports,
        test_ecosystem_generation,
        test_ui_compatibility
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Error ejecutando {test.__name__}: {e}")
            results.append(False)
    
    print("\n📋 RESUMEN DE PRUEBAS:")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Pruebas exitosas: {passed}/{total}")
    print(f"❌ Pruebas fallidas: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron! El sistema está listo.")
    else:
        print("\n⚠️ Algunas pruebas fallaron. Revisar errores arriba.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)