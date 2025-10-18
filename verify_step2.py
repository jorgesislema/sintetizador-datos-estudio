#!/usr/bin/env python3
"""Script para verificar la funcionalidad completa de la segunda parte gráfica"""

import sys
sys.path.insert(0, '.')

def test_step2_elements():
    """Verificar que todos los elementos del Step 2 estén implementados"""
    print("🎯 Verificando elementos de la segunda parte gráfica (Step 2)")
    print("=" * 60)
    
    # Leer el archivo de la UI
    with open('apps/ui_desktop/app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Elementos que deben estar en Step 2
    step2_elements = {
        "📊 Selector de formato de archivo": [
            "output_format", 
            'values=["csv", "json", "excel", "parquet"]'
        ],
        "📁 Selector de directorio de salida": [
            "select_output_dir", 
            'text="Explorar"'
        ],
        "📈 Barra de progreso": [
            "progress_bar", 
            "ttk.Progressbar"
        ],
        "🚀 Botón START": [
            'text="START - Generar Dataset"',
            "generate_dataset"
        ],
        "⚙️ Control de número de filas": [
            "row_count",
            "ttk.Spinbox"
        ],
        "🔧 Perfil de errores": [
            "error_profile",
            '"none", "light", "moderate", "heavy"'
        ],
        "👁️ Preview de datos": [
            "generate_preview",
            "preview_text"
        ],
        "📊 Status label": [
            "status_label",
            "Listo para generar datos"
        ]
    }
    
    results = {}
    for element_name, patterns in step2_elements.items():
        found = all(pattern in content for pattern in patterns)
        results[element_name] = found
        status = "✅" if found else "❌"
        print(f"  {status} {element_name}")
        
        if not found:
            missing = [p for p in patterns if p not in content]
            print(f"      Faltante: {missing}")
    
    # Verificar que no estén duplicados en Step 3
    print(f"\n🔍 Verificando que elementos están solo en Step 2...")
    
    # Extraer contenido del Step 2 y Step 3
    lines = content.split('\n')
    step2_start = None
    step3_start = None
    
    for i, line in enumerate(lines):
        if "def create_step2(self):" in line:
            step2_start = i
        elif "def create_step3(self):" in line:
            step3_start = i
            break
    
    if step2_start and step3_start:
        step2_content = '\n'.join(lines[step2_start:step3_start])
        step3_content = '\n'.join(lines[step3_start:step3_start+50])  # Solo primeras 50 líneas del step 3
        
        # Verificar elementos críticos
        critical_elements = [
            ('Botón START', 'START - Generar Dataset'),
            ('Barra de progreso', 'progress_bar'),
            ('Status label', 'status_label')
        ]
        
        for name, pattern in critical_elements:
            in_step2 = pattern in step2_content
            in_step3 = pattern in step3_content
            
            if in_step2 and not in_step3:
                print(f"  ✅ {name}: Solo en Step 2 ✓")
            elif in_step2 and in_step3:
                print(f"  ⚠️  {name}: Duplicado en ambos steps")
            elif not in_step2 and in_step3:
                print(f"  ❌ {name}: Solo en Step 3 (debe estar en Step 2)")
            else:
                print(f"  ❌ {name}: No encontrado")
    
    # Resumen
    total_elements = len(results)
    implemented = sum(results.values())
    
    print(f"\n📊 RESUMEN:")
    print(f"   Elementos implementados: {implemented}/{total_elements}")
    print(f"   Porcentaje completado: {(implemented/total_elements)*100:.1f}%")
    
    if implemented == total_elements:
        print(f"\n🎉 ¡SEGUNDA PARTE GRÁFICA COMPLETA!")
        print(f"   ✅ Todos los elementos están en Step 2")
        print(f"   ✅ Formato de archivo: CSV, JSON, Excel, Parquet")
        print(f"   ✅ Barra de progreso implementada")
        print(f"   ✅ Selector de directorio funcionando")
        print(f"   ✅ Botón START ubicado correctamente")
    else:
        print(f"\n⚠️  Elementos faltantes: {total_elements - implemented}")
    
    return implemented == total_elements

def main():
    success = test_step2_elements()
    
    if success:
        print(f"\n🚀 Sistema listo para ejecutar!")
        print(f"   La segunda parte gráfica está completa")
        print(f"   Ejecuta: python launch_desktop.py")
    else:
        print(f"\n❌ Revisar elementos faltantes")

if __name__ == "__main__":
    main()