#!/usr/bin/env python3
"""
Script de Verificación del Sistema Completo
Verifica que todos los componentes del sintetizador funcionen correctamente
"""
import sys
from pathlib import Path
from core.ecosystems import generate_ecosystem_data, get_available_ecosystem_options
from core.generators import generate
from core.utils.schemas import list_domains
import json

def print_section(title):
    """Imprimir sección con formato"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def check_ecosystems():
    """Verificar sistema de ecosistemas"""
    print_section("VERIFICANDO ECOSISTEMAS")
    
    try:
        ecosystems = get_available_ecosystem_options()
        print(f"✓ {len(ecosystems)} ecosistemas disponibles")
        
        # Listar por categoría
        categories = {}
        for key, name in ecosystems.items():
            category = key.split('_')[0]
            if category not in categories:
                categories[category] = []
            categories[category].append(name)
        
        print("\nEcosistemas por categoría:")
        for cat, items in sorted(categories.items()):
            print(f"  • {cat.capitalize()}: {len(items)} ecosistemas")
        
        return True
    except Exception as e:
        print(f"✗ Error en ecosistemas: {e}")
        return False

def check_generation():
    """Verificar generación de datos"""
    print_section("VERIFICANDO GENERACIÓN DE DATOS")
    
    try:
        # Test tabla individual
        print("Probando generación de tabla individual...")
        data = generate('retail', 'dim_product', 10)
        print(f"✓ Tabla individual: {len(data)} registros generados")
        
        # Test ecosistema
        print("\nProbando generación de ecosistema...")
        eco_data, summary = generate_ecosystem_data('retail_supermarket', volume=50)
        print(f"✓ Ecosistema generado:")
        print(f"  - Tablas: {summary['total_tables']}")
        print(f"  - Registros totales: {summary['total_records']:,}")
        
        # Verificar estructura de datos
        if eco_data:
            sample_table = list(eco_data.keys())[0]
            sample_record = eco_data[sample_table][0] if eco_data[sample_table] else {}
            print(f"  - Campos comunes presentes: {len(sample_record)} campos")
        
        return True
    except Exception as e:
        print(f"✗ Error en generación: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_localization():
    """Verificar sistema de localización"""
    print_section("VERIFICANDO LOCALIZACIÓN")
    
    try:
        from core.localization import (
            get_available_contexts, 
            get_available_languages
        )
        
        contexts = get_available_contexts()
        languages = get_available_languages()
        
        print(f"✓ {len(contexts)} contextos geográficos disponibles")
        print(f"✓ {len(languages)} idiomas disponibles")
        
        # Listar algunos contextos
        print("\nAlgunos contextos disponibles:")
        for ctx in list(contexts)[:5]:
            if isinstance(ctx, dict):
                print(f"  • {ctx.get('display_name', ctx)}")
            else:
                print(f"  • {ctx}")
        
        return True
    except ImportError:
        print("⚠ Sistema de localización no disponible (opcional)")
        return True
    except Exception as e:
        print(f"✗ Error en localización: {e}")
        return False

def check_data_quality():
    """Verificar sistema de calidad de datos"""
    print_section("VERIFICANDO CALIDAD DE DATOS")
    
    try:
        from core.dq.profiler import profile
        from core.errors.profiles import ERROR_PROFILES
        
        # Generar datos con diferentes perfiles
        data_clean = generate('finance', 'dim_customer', 100, error_profile='none')
        data_dirty = generate('finance', 'dim_customer', 100, error_profile='heavy')
        
        metrics_clean = profile(data_clean)
        metrics_dirty = profile(data_dirty)
        
        print(f"✓ Perfiles de error disponibles: {len(ERROR_PROFILES)}")
        print(f"✓ Análisis DQ funcionando")
        
        # Comparar calidad
        sample_field = list(metrics_clean.keys())[0]
        clean_completeness = metrics_clean[sample_field].get('completeness', 1.0)
        dirty_completeness = metrics_dirty[sample_field].get('completeness', 1.0)
        
        print(f"\nComparación de calidad (campo '{sample_field}'):")
        print(f"  - Datos limpios: {clean_completeness*100:.1f}% completitud")
        print(f"  - Datos con errores: {dirty_completeness*100:.1f}% completitud")
        
        return True
    except Exception as e:
        print(f"✗ Error en calidad de datos: {e}")
        return False

def check_domains():
    """Verificar dominios disponibles"""
    print_section("VERIFICANDO DOMINIOS")
    
    try:
        domains = list_domains()
        total_tables = sum(len(tables) for tables in domains.values())
        
        print(f"✓ {len(domains)} dominios disponibles")
        print(f"✓ {total_tables} tablas totales")
        
        print("\nDominios y tablas:")
        for domain, tables in sorted(domains.items()):
            print(f"  • {domain}: {len(tables)} tablas")
        
        return True
    except Exception as e:
        print(f"✗ Error en dominios: {e}")
        return False

def check_output_structure():
    """Verificar estructura de salida"""
    print_section("VERIFICANDO ESTRUCTURA DE SALIDA")
    
    try:
        # Verificar que outputs está en gitignore
        gitignore_path = Path('.gitignore')
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            if 'outputs/' in content:
                print("✓ outputs/ está en .gitignore")
            else:
                print("⚠ outputs/ NO está en .gitignore")
        
        # Crear directorio de salida de prueba
        test_output = Path('./outputs/test_verification')
        test_output.mkdir(parents=True, exist_ok=True)
        
        print(f"✓ Directorio de salida creado: {test_output}")
        
        # Verificar que pasos_a_paso está en gitignore
        if 'pasos_a_paso/' in content:
            print("✓ pasos_a_paso/ está en .gitignore")
        else:
            print("⚠ pasos_a_paso/ NO está en .gitignore")
        
        return True
    except Exception as e:
        print(f"✗ Error en estructura: {e}")
        return False

def check_documentation():
    """Verificar documentación"""
    print_section("VERIFICANDO DOCUMENTACIÓN")
    
    docs = {
        'GUIA_COMPLETA.md': 'Guía completa del sistema',
        'EJEMPLOS_PRACTICOS.md': 'Ejemplos prácticos',
        'README.md': 'Introducción',
        'LOCALIZATION_COMPLETE.md': 'Sistema de localización',
        'docs/ORGANIZACION_CARPETAS.md': 'Organización de archivos'
    }
    
    found = 0
    for doc, desc in docs.items():
        path = Path(doc)
        if path.exists():
            print(f"✓ {doc} - {desc}")
            found += 1
        else:
            print(f"⚠ {doc} - NO ENCONTRADO")
    
    print(f"\nDocumentación: {found}/{len(docs)} archivos encontrados")
    return found >= 3  # Al menos 3 documentos principales

def generate_summary_report():
    """Generar reporte resumen"""
    print_section("RESUMEN DEL SISTEMA")
    
    try:
        ecosystems = get_available_ecosystem_options()
        domains = list_domains()
        total_tables = sum(len(tables) for tables in domains.values())
        
        summary = f"""
SISTEMA DE SINTETIZADOR DE DATOS
=================================

📊 CAPACIDADES DEL SISTEMA
--------------------------
• Ecosistemas de negocio:     {len(ecosystems)}
• Dominios:                   {len(domains)}
• Tablas totales:             {total_tables}
• Perfiles de error:          4 (none, light, moderate, heavy)
• Formatos de salida:         CSV, Parquet, JSON, Excel
• Países soportados:          13 (América Latina, Europa, Norteamérica)
• Idiomas:                    2 (Español, English)

🎯 CASOS DE USO
---------------
✓ ETL (Extract, Transform, Load)
✓ EDA (Exploratory Data Analysis)
✓ Machine Learning
✓ Automatizaciones
✓ Dashboards
✓ Análisis 360° de Negocios

📁 ESTRUCTURA DE ARCHIVOS
-------------------------
• core/                       - Motor principal
• apps/                       - CLI y UI
• schemas/                    - Definiciones de tablas
• outputs/                    - Salidas (NO versionado)
• docs/                       - Documentación

📚 DOCUMENTACIÓN DISPONIBLE
---------------------------
• GUIA_COMPLETA.md           - Guía completa paso a paso
• EJEMPLOS_PRACTICOS.md      - Ejemplos de código
• README.md                  - Introducción y setup
• LOCALIZATION_COMPLETE.md   - Sistema de localización

🚀 CÓMO EMPEZAR
---------------
1. Interfaz Gráfica:    python launch_desktop.py
2. Línea de Comandos:   python -m apps.cli.main list-domains
3. Python directo:      Ver GUIA_COMPLETA.md

{'='*70}
Sistema verificado y listo para usar! 🎉
"""
        
        print(summary)
        
        # Guardar reporte
        report_path = Path('./SISTEMA_VERIFICADO.txt')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"\nReporte guardado en: {report_path}")
        
    except Exception as e:
        print(f"Error generando resumen: {e}")

def main():
    """Ejecutar todas las verificaciones"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║        VERIFICACIÓN DEL SISTEMA DE SINTETIZADOR DE DATOS            ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    results = {
        'Ecosistemas': check_ecosystems(),
        'Generación de Datos': check_generation(),
        'Localización': check_localization(),
        'Calidad de Datos': check_data_quality(),
        'Dominios': check_domains(),
        'Estructura de Salida': check_output_structure(),
        'Documentación': check_documentation()
    }
    
    # Resumen final
    print_section("RESULTADO DE VERIFICACIÓN")
    
    passed = sum(results.values())
    total = len(results)
    
    print("\nResultados por componente:")
    for component, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status:10s} {component}")
    
    print(f"\nTotal: {passed}/{total} componentes verificados correctamente")
    
    if passed == total:
        print("\n🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        generate_summary_report()
        return 0
    else:
        print("\n⚠ Algunos componentes requieren atención")
        return 1

if __name__ == '__main__':
    sys.exit(main())
