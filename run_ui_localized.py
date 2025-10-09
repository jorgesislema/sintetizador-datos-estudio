#!/usr/bin/env python3
"""
Script para iniciar la aplicación de escritorio con sistema de localización
"""

import tkinter as tk
from apps.ui_desktop.app import DataSynthesizerApp

def main():
    """Iniciar la aplicación de escritorio"""
    try:
        print("🚀 Iniciando Sintetizador de Datos con Sistema de Localización...")
        print("=" * 60)
        print("✅ Sistema de localización disponible:")
        print("   🌍 13 contextos geográficos (Ecuador, España, USA, etc.)")
        print("   🗣️  Traducción al español de columnas y valores")
        print("   🔧 Interfaz integrada en Paso 2 de configuración")
        print("=" * 60)
        
        # Crear ventana principal
        root = tk.Tk()
        
        # Inicializar aplicación
        app = DataSynthesizerApp(root)
        
        print("📱 Aplicación iniciada. Verifica las opciones de localización en Paso 2.")
        print("💡 Puedes cambiar el idioma a 'Español' y seleccionar diferentes países.")
        
        # Ejecutar interfaz
        root.mainloop()
        
    except KeyboardInterrupt:
        print("\n👋 Aplicación cerrada por el usuario.")
    except Exception as e:
        print(f"\n❌ Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()