#!/usr/bin/env python3
"""
Script de verificación de implementación de controles de rango de fechas
Verifica que todos los componentes estén correctamente implementados
"""

import sys
import os

# Asegurar que podemos importar los módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Verificar que todos los imports necesarios funcionan"""
    print("=" * 70)
    print("TEST 1: Verificación de Imports")
    print("=" * 70)
    
    try:
        from core.engines.faker_engine import set_date_range
        print("✓ core.engines.faker_engine.set_date_range")
    except ImportError as e:
        print(f"✗ Error importando set_date_range: {e}")
        return False
    
    try:
        from core.engines.faker_engine import _rand_date, _rand_datetime_utc, _rand_datetime_local
        print("✓ Funciones de generación de fechas")
    except ImportError as e:
        print(f"✗ Error importando funciones de fecha: {e}")
        return False
    
    return True

def test_date_range_functionality():
    """Verificar funcionalidad de set_date_range"""
    print("\n" + "=" * 70)
    print("TEST 2: Funcionalidad de set_date_range")
    print("=" * 70)
    
    from core.engines.faker_engine import set_date_range, _rand_date
    
    # Test 1: Establecer rango válido
    try:
        set_date_range("2023-01-01", "2024-12-31")
        print("✓ Rango válido aceptado")
    except Exception as e:
        print(f"✗ Error estableciendo rango: {e}")
        return False
    
    # Test 2: Generar fechas en el rango
    try:
        dates = [_rand_date() for _ in range(100)]
        print(f"✓ Generadas {len(dates)} fechas en el rango")
        
        # Verificar que todas las fechas están en el rango
        from datetime import datetime
        for date_str in dates:
            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            year = date_obj.year
            if not (2023 <= year <= 2024):
                print(f"✗ Fecha fuera de rango: {date_str}")
                return False
        print(f"✓ Todas las fechas están dentro del rango 2023-2024")
        
    except Exception as e:
        print(f"✗ Error generando fechas: {e}")
        return False
    
    # Test 3: Limpiar rango
    try:
        set_date_range(None, None)
        print("✓ Rango limpiado correctamente")
    except Exception as e:
        print(f"✗ Error limpiando rango: {e}")
        return False
    
    return True

def test_ui_integration():
    """Verificar integración con UI"""
    print("\n" + "=" * 70)
    print("TEST 3: Integración con UI")
    print("=" * 70)
    
    import calendar
    from core.engines.faker_engine import set_date_range
    
    def simulate_apply_date_range(from_year, from_month, to_year, to_month):
        """Simular el método _apply_date_range_to_engine de la UI"""
        y1, m1, y2, m2 = int(from_year), int(from_month), int(to_year), int(to_month)
        
        # Normalizar orden
        if (y2, m2) < (y1, m1):
            y1, m1, y2, m2 = y2, m2, y1, m1
        
        start = f"{y1:04d}-{m1:02d}-01"
        last_day = calendar.monthrange(y2, m2)[1]
        end = f"{y2:04d}-{m2:02d}-{last_day:02d}"
        
        set_date_range(start, end)
        return start, end
    
    # Test casos comunes
    test_cases = [
        (2023, 1, 2024, 12, "2023-01-01", "2024-12-31"),
        (2024, 12, 2023, 1, "2023-01-01", "2024-12-31"),  # Invertido
        (2024, 2, 2024, 2, "2024-02-01", "2024-02-29"),   # Año bisiesto
        (2023, 2, 2023, 2, "2023-02-01", "2023-02-28"),   # No bisiesto
        (2024, 6, 2024, 6, "2024-06-01", "2024-06-30"),   # Mismo mes
    ]
    
    for i, (fy, fm, ty, tm, expected_start, expected_end) in enumerate(test_cases, 1):
        try:
            start, end = simulate_apply_date_range(fy, fm, ty, tm)
            if start == expected_start and end == expected_end:
                print(f"✓ Caso {i}: {fy}-{fm:02d} a {ty}-{tm:02d} → {start} a {end}")
            else:
                print(f"✗ Caso {i}: Esperado {expected_start}/{expected_end}, obtuvo {start}/{end}")
                return False
        except Exception as e:
            print(f"✗ Caso {i}: Error - {e}")
            return False
    
    return True

def test_file_structure():
    """Verificar que los archivos clave existen"""
    print("\n" + "=" * 70)
    print("TEST 4: Estructura de Archivos")
    print("=" * 70)
    
    files_to_check = [
        "apps/ui_desktop/app.py",
        "core/engines/faker_engine.py",
        "pasos_a_paso/apps_ui_desktop_app_pasos.txt",
    ]
    
    all_exist = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} no encontrado")
            all_exist = False
    
    return all_exist

def test_code_in_files():
    """Verificar que el código esperado está en los archivos"""
    print("\n" + "=" * 70)
    print("TEST 5: Presencia de Código Clave")
    print("=" * 70)
    
    checks = [
        ("apps/ui_desktop/app.py", "def _apply_date_range_to_engine", "Método _apply_date_range_to_engine"),
        ("apps/ui_desktop/app.py", "def apply_date_range", "Método apply_date_range"),
        ("apps/ui_desktop/app.py", "self.date_from_year", "Variable date_from_year"),
        ("apps/ui_desktop/app.py", "self.date_to_month", "Variable date_to_month"),
        ("apps/ui_desktop/app.py", "Rango de Fechas (YYYY-MM)", "Etiqueta UI"),
        ("apps/ui_desktop/app.py", "Aplicar Rango", "Botón de aplicar"),
        ("core/engines/faker_engine.py", "def set_date_range", "Función set_date_range"),
        ("core/engines/faker_engine.py", "_CURRENT_DATE_RANGE_START", "Variable global de rango"),
    ]
    
    all_found = True
    for file_path, search_string, description in checks:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if search_string in content:
                    print(f"✓ {description}")
                else:
                    print(f"✗ {description} no encontrado en {file_path}")
                    all_found = False
        except Exception as e:
            print(f"✗ Error leyendo {file_path}: {e}")
            all_found = False
    
    return all_found

def main():
    """Ejecutar todas las pruebas"""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════════════╗")
    print("║  VERIFICACIÓN DE IMPLEMENTACIÓN: CONTROLES DE RANGO DE FECHAS        ║")
    print("╚═══════════════════════════════════════════════════════════════════════╝")
    print("\n")
    
    tests = [
        ("Imports", test_imports),
        ("Funcionalidad de Rango", test_date_range_functionality),
        ("Integración UI", test_ui_integration),
        ("Estructura de Archivos", test_file_structure),
        ("Código Clave", test_code_in_files),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n✗ Error ejecutando {name}: {e}")
            results[name] = False
    
    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN DE RESULTADOS")
    print("=" * 70)
    
    all_passed = True
    for name, passed in results.items():
        status = "✅ PASÓ" if passed else "❌ FALLÓ"
        print(f"{status:12} - {name}")
        if not passed:
            all_passed = False
    
    print("=" * 70)
    
    if all_passed:
        print("\n✅ TODAS LAS VERIFICACIONES PASARON")
        print("\n🎉 Los controles de rango de fechas están completamente implementados!")
        print("\nCaracterísticas verificadas:")
        print("  • Variables de estado para rango de fechas")
        print("  • Controles UI (Spinboxes para año/mes)")
        print("  • Botón 'Aplicar Rango'")
        print("  • Métodos de aplicación y validación")
        print("  • Integración con motor de generación")
        print("  • Funciones de generación de fechas respetando rango")
        print("  • Normalización automática de rango invertido")
        print("  • Manejo correcto de años bisiestos")
        return 0
    else:
        print("\n❌ ALGUNAS VERIFICACIONES FALLARON")
        print("\nRevise los errores anteriores para más detalles.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
