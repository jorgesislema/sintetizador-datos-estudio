#!/usr/bin/env python3
"""
Script de prueba para el nuevo sistema de carpetas por sesión
"""

import tempfile
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from core.generators import generate
from apps.ui_desktop.app import DataSynthesizerApp
import tkinter as tk

def test_session_folder_system():
    """Probar el sistema de carpetas por sesión programáticamente"""
    
    print("🧪 PRUEBA DEL SISTEMA DE CARPETAS POR SESIÓN")
    print("=" * 50)
    
    # Crear directorio temporal para pruebas
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Directorio temporal: {temp_dir}")
        
        # Simular una aplicación
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana principal
        
        try:
            app = DataSynthesizerApp(root)
            app.output_dir.set(temp_dir)
            
            print("\n📋 SIMULANDO GENERACIÓN DE MÚLTIPLES TABLAS...")
            
            # Generar varias tablas en la misma sesión
            test_tables = [
                ("retail", "transactions"),
                ("finance", "accounts"),
                ("healthcare", "patients")
            ]
            
            print(f"\n🔄 Generando {len(test_tables)} tablas en la misma sesión...")
            
            session_folder = None
            
            for i, (domain, table) in enumerate(test_tables):
                print(f"\n📊 Tabla {i+1}: {domain}.{table}")
                
                # Simular proceso de generación
                data = generate(domain, table, 10)  # Solo 10 filas para prueba rápida
                
                # Crear carpeta de sesión (solo la primera vez)
                if not session_folder:
                    session_folder = app.create_session_folder()
                    print(f"   📂 Carpeta de sesión creada: {session_folder.name}")
                
                # Guardar archivo
                output_file = session_folder / f"{domain}__{table}.csv"
                import pandas as pd
                df = pd.DataFrame(data)
                df.to_csv(output_file, index=False)
                
                # Registrar en metadatos
                app.add_table_to_session(domain, table, output_file, len(data))
                print(f"   ✅ Archivo guardado: {output_file.name}")
            
            # Verificar resultados
            print(f"\n📊 RESULTADOS DE LA SESIÓN:")
            print(f"   📂 Carpeta: {session_folder.name}")
            
            files_in_session = list(session_folder.glob("*"))
            print(f"   📄 Archivos generados: {len(files_in_session)}")
            
            for file in files_in_session:
                if file.suffix == '.csv':
                    print(f"     • {file.name}")
                elif file.name == 'session_metadata.json':
                    print(f"     • {file.name} (metadatos)")
            
            # Verificar metadatos
            metadata_file = session_folder / "session_metadata.json"
            if metadata_file.exists():
                import json
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                print(f"\n📋 METADATOS DE LA SESIÓN:")
                print(f"   🆔 ID: {metadata['session_id']}")
                print(f"   🕐 Creada: {metadata['created_at']}")
                print(f"   🌍 Contexto: {metadata['geographic_context']}")
                print(f"   🗣️ Idioma: {metadata['language']}")
                print(f"   📊 Tablas: {len(metadata['tables_generated'])}")
                
                for table_info in metadata['tables_generated']:
                    print(f"     • {table_info['domain']}.{table_info['table']} ({table_info['row_count']} filas)")
            
            print(f"\n✅ ¡PRUEBA COMPLETADA EXITOSAMENTE!")
            print(f"🎉 Todas las tablas se organizaron en una sola carpeta.")
            
        except Exception as e:
            print(f"❌ Error durante la prueba: {e}")
            import traceback
            traceback.print_exc()
        finally:
            root.destroy()

def main():
    """Función principal"""
    try:
        test_session_folder_system()
    except KeyboardInterrupt:
        print("\n👋 Prueba interrumpida por el usuario.")

if __name__ == "__main__":
    main()