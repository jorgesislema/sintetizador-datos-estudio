#!/usr/bin/env python3
"""
Script para reorganizar archivos existentes en outputs/ 
moviendo cada archivo a su carpeta correspondiente por tabla
"""
import os
import shutil
from pathlib import Path
import re

def reorganize_outputs():
    """Reorganizar archivos existentes en outputs/"""
    outputs_dir = Path("outputs")
    
    if not outputs_dir.exists():
        print("❌ Directorio outputs/ no encontrado")
        return
    
    # Patrón mejorado para detectar archivos con formato domain__table.*
    # Soporta nombres con guiones bajos múltiples
    pattern = re.compile(r'^(.+?)__(.+?)(?:_dq_report|_scd2)?\.(.+)$')
    
    files_moved = 0
    
    # Buscar archivos en la raíz de outputs/
    for file_path in outputs_dir.iterdir():
        if file_path.is_file():
            match = pattern.match(file_path.name)
            if match:
                domain, table, extension = match.groups()
                
                # Crear carpeta para la tabla si no existe
                table_dir = outputs_dir / table
                table_dir.mkdir(exist_ok=True)
                
                # Mover archivo a la carpeta de la tabla
                new_path = table_dir / file_path.name
                
                if new_path.exists():
                    print(f"⚠️  El archivo {new_path} ya existe, se sobrescribirá")
                
                shutil.move(str(file_path), str(new_path))
                print(f"📁 Movido: {file_path.name} → {table}/{file_path.name}")
                files_moved += 1
            else:
                print(f"⏭️  Ignorado (no coincide con patrón): {file_path.name}")
    
    print(f"\n✅ Reorganización completada: {files_moved} archivos movidos")
    
    # Mostrar estructura resultante
    print("\n📂 Nueva estructura de carpetas:")
    for item in sorted(outputs_dir.iterdir()):
        if item.is_dir():
            file_count = len(list(item.glob("*")))
            print(f"   📁 {item.name}/ ({file_count} archivos)")

if __name__ == "__main__":
    reorganize_outputs()