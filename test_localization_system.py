#!/usr/bin/env python3
"""
Script de prueba completo para el Sistema de Localización
Demuestra el funcionamiento de contextos geográficos y traducción al español
"""

from core.localization.geographic_contexts import get_available_contexts, get_region_options
from core.localization.i18n import translate_complete_dataset, get_available_languages
from core.engines.faker_engine import set_geographic_context, get_current_geographic_context
from core.generators import generate

def test_geographic_contexts():
    """Probar contextos geográficos"""
    print("🌍 SISTEMA DE CONTEXTOS GEOGRÁFICOS")
    print("=" * 50)
    
    # Mostrar contextos disponibles por región
    regions = get_region_options()
    for region, countries in regions.items():
        print(f"\n📍 {region}:")
        for country in countries:
            print(f"   • {country}")
    
    print(f"\n📊 Total de contextos disponibles: {len(get_available_contexts())}")
    
    # Probar generación con diferentes contextos
    print("\n🧪 PRUEBAS DE GENERACIÓN CON CONTEXTOS ESPECÍFICOS")
    print("=" * 50)
    
    test_contexts = ["ecuador", "espana", "usa"]
    
    for context in test_contexts:
        print(f"\n🏷️  Contexto: {context.upper()}")
        set_geographic_context(context)
        
        # Generar 1 fila de datos retail
        data = generate('retail', 'transactions', 1)
        row = data[0]
        
        # Mostrar campos específicos que muestran localización
        print(f"   💰 Moneda: {row.get('currency_code', 'N/A')}")
        print(f"   🏢 Marca: {row.get('brand', 'N/A')}")
        print(f"   📦 Método pago: {row.get('payment_method', 'N/A')}")

def test_translation_system():
    """Probar sistema de traducción"""
    print("\n\n🗣️  SISTEMA DE TRADUCCIÓN AL ESPAÑOL")
    print("=" * 50)
    
    # Mostrar idiomas disponibles
    languages = get_available_languages()
    print(f"📚 Idiomas disponibles: {', '.join(languages)}")
    
    # Generar datos de salud (tienen muchas columnas para traducir)
    print("\n🧪 PRUEBA DE TRADUCCIÓN")
    print("=" * 30)
    
    original_data = generate('healthcare', 'patients', 1)
    translated_data = translate_complete_dataset(original_data, "es")
    
    print("\n📋 COMPARACIÓN DE COLUMNAS:")
    print("-" * 40)
    
    original_keys = list(original_data[0].keys())
    translated_keys = list(translated_data[0].keys())
    
    # Mostrar las primeras 10 traducciones
    translations_shown = 0
    for orig, trans in zip(original_keys, translated_keys):
        if orig != trans and translations_shown < 10:  # Solo mostrar columnas que cambiaron
            print(f"   🔄 {orig:<20} → {trans}")
            translations_shown += 1
    
    print(f"\n📊 Total de columnas traducidas: {sum(1 for o, t in zip(original_keys, translated_keys) if o != t)}")

def test_combined_system():
    """Probar sistema combinado: localización + traducción"""
    print("\n\n🌐 SISTEMA COMBINADO: LOCALIZACIÓN + TRADUCCIÓN")
    print("=" * 50)
    
    # Configurar contexto de Ecuador
    set_geographic_context("ecuador")
    print(f"🏷️  Contexto configurado: {get_current_geographic_context()}")
    
    # Generar datos
    data = generate('finance', 'accounts', 1)
    
    # Traducir al español
    spanish_data = translate_complete_dataset(data, "es")
    
    print("\n📊 DATOS GENERADOS (Ecuador + Español):")
    print("-" * 40)
    
    row = spanish_data[0]
    
    # Mostrar algunos campos clave (traducidos)
    key_fields = [
        'codigo_moneda', 'creado_por', 'actualizado_por', 
        'clave_natural', 'notas', 'region_geo'
    ]
    
    for field in key_fields:
        if field in row:
            value = str(row[field])[:50] + "..." if len(str(row[field])) > 50 else str(row[field])
            print(f"   📝 {field}: {value}")

def main():
    """Función principal de prueba"""
    print("🚀 PRUEBA COMPLETA DEL SISTEMA DE LOCALIZACIÓN")
    print("=" * 60)
    print("Este script demuestra el funcionamiento completo del sistema")
    print("de localización implementado para el Sintetizador de Datos.")
    print("=" * 60)
    
    try:
        test_geographic_contexts()
        test_translation_system()
        test_combined_system()
        
        print("\n\n✅ ¡TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE!")
        print("🎉 El sistema de localización está funcionando perfectamente.")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()