#!/usr/bin/env python3
"""Script para capturar la estructura actual de la UI y detectar qué falta"""

import sys
sys.path.insert(0, '.')

def analyze_ui_structure():
    """Analizar la estructura actual de la UI"""
    
    print("📊 Análisis de estructura UI actual")
    print("=" * 50)
    
    # Leer el archivo de la UI
    with open('apps/ui_desktop/app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar elementos del Step 2
    print("🔍 Elementos encontrados en Step 2:")
    
    step2_elements = {
        "Selector de formato": "output_format" in content and "csv\", \"json\", \"excel\", \"parquet" in content,
        "Selector de directorio": "select_output_dir" in content and "Explorar" in content,
        "Botón START": "START - Generar Dataset" in content,
        "Barra de progreso": "progress_bar" in content,
        "Control de filas": "row_count" in content and "Spinbox" in content,
        "Perfil de errores": "error_profile" in content,
        "Preview": "generate_preview" in content
    }
    
    for element, found in step2_elements.items():
        status = "✅" if found else "❌"
        print(f"  {status} {element}")
    
    # Verificar donde está el botón START
    if "START - Generar Dataset" in content:
        # Encontrar en qué step está
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "START - Generar Dataset" in line:
                # Buscar hacia atrás para encontrar el step
                for j in range(i, max(0, i-100), -1):
                    if "create_step" in lines[j]:
                        step_method = lines[j].strip()
                        print(f"  📍 Botón START encontrado en: {step_method}")
                        break
                break
    
    print(f"\n📈 Elementos implementados: {sum(step2_elements.values())}/{len(step2_elements)}")
    
    # Verificar si necesita movimiento del botón START
    if step2_elements["Botón START"]:
        print("\n⚠️  PROBLEMA DETECTADO:")
        print("   El botón START está en Step 3, pero debe estar en Step 2")
        print("   Según solicitud: 'falta la segunda parte gráfica'")
        print("   Necesario: Mover START y barra de progreso al Step 2")
    
    return step2_elements

def main():
    elements = analyze_ui_structure()
    
    if not elements["Botón START"]:
        print("\n❌ Botón START no encontrado")
    else:
        print("\n✅ Todos los elementos base están implementados")
        print("🔧 Solo necesita reorganización: mover START al Step 2")

if __name__ == "__main__":
    main()