# Tutorial: Uso de la Interfaz Tkinter
## Archivo: tutorial_ui_tkinter.md

## 🎯 Guía Rápida de Uso

### Paso 1: Lanzar la Aplicación
```bash
# Opción recomendada
python launch_desktop.py

# O directamente
python -c "import sys; sys.path.insert(0, '.'); import apps.ui_desktop.app as app; app.main()"
```

### Paso 2: Seleccionar Dominio y Tabla
1. **Dominio**: Elige "enterprise" del menú desplegable
2. **Tabla**: Selecciona "hr_core" o "sales"
3. **Haz clic en "Siguiente"**

### Paso 3: Configurar Parámetros
1. **Número de registros**: 1000 (por defecto)
2. **Perfil de errores**: "none" (sin errores), "light" (errores leves)
3. **Directorio de salida**: Haz clic en "Explorar" para elegir carpeta
4. **Formato**: CSV (recomendado)
5. **Preview**: Activar para ver muestra antes de generar
6. **Haz clic en "Siguiente"**

### Paso 4: Generar y Descargar
1. **Generar datos**: Haz clic en "Generar Datos"
2. **Ver progreso**: Observa la barra de progreso
3. **Revisar métricas**: Ver completitud, duplicados, unicidad
4. **Descargar**: Haz clic en "Descargar Archivo" para guardar

## 💡 Consejos de Uso

### Para Datasets Grandes
- Desactiva preview para mejor rendimiento
- Usa formato Parquet para archivos grandes
- Monitorea el progreso en la barra

### Perfiles de Error
- **none**: Datos perfectos (para testing)
- **light**: Errores realistas leves
- **moderate**: Errores moderados
- **heavy**: Muchos errores (para testing DQ)

### Formatos de Salida
- **CSV**: Compatible con Excel, fácil de leer
- **Parquet**: Comprimido, rápido para big data

## 🔧 Solución de Problemas

### Error de Importación
```bash
# Verificar módulos
python -c "import apps.ui_desktop; print('OK')"
```

### UI No Responde
- La aplicación usa threading, debería mantenerse responsiva
- Si se congela, reinicia la aplicación

### Archivos No se Generan
- Verifica permisos de escritura en el directorio seleccionado
- Revisa que el directorio existe

## 📊 Métricas de Calidad de Datos

La aplicación calcula automáticamente:
- **Completitud**: % de campos no nulos
- **Duplicados**: Número de filas duplicadas
- **Unicidad**: % de valores únicos
- **Validez**: % de datos en rangos esperados

## 🎉 ¡Listo para Usar!

La interfaz está completamente funcional y lista para generar datos sintéticos de calidad con una experiencia nativa de escritorio.