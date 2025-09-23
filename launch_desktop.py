#!/usr/bin/env python3
"""
Script de lanzamiento para la aplicación de escritorio del Sintetizador de Datos
Ejecuta la interfaz gráfica nativa usando Tkinter
"""

import os
import sys

def main():
    """Función principal de lanzamiento"""
    print("🚀 Iniciando Sintetizador de Datos - Interfaz de Escritorio")
    print("🔬 Versión: 1.0.0")
    print("📱 UI: Tkinter (Nativa)")
    print("=" * 50)
    print("💡 Si la aplicación no se abre, ejecuta manualmente:")
    print("   python -c \"import sys; sys.path.insert(0, '.'); import apps.ui_desktop.app as app; app.main()\"")
    print("=" * 50)

    # Ejecutar con comando del sistema
    try:
        os.system('python -c "import sys; sys.path.insert(0, \'.\'); import apps.ui_desktop.app as app; app.main()"')
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()