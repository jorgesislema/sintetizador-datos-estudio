# Controles de Rango de Fechas - Documentación de Implementación

## Resumen

Los controles de rango de fechas han sido implementados completamente en la interfaz de usuario del Sintetizador de Datos. Esta funcionalidad permite a los usuarios especificar un rango temporal (año-mes) para la generación de datos sintéticos.

## Características Implementadas

### 1. Variables de Estado (app.py, líneas 63-76)

Se agregaron variables para mantener el rango de fechas:
- `self.date_from_year`: Año de inicio
- `self.date_from_month`: Mes de inicio
- `self.date_to_year`: Año de fin
- `self.date_to_month`: Mes de fin

**Valores por defecto**: Últimos 12 meses desde la fecha actual

### 2. Controles de UI en Paso 2 (app.py, líneas 417-437)

Se agregó una fila completa en la configuración con:
- **Etiqueta**: "Rango de Fechas (YYYY-MM)"
- **Control "Desde"**: 
  - Spinbox para año (1970-2100)
  - Spinbox para mes (1-12)
- **Control "Hasta"**:
  - Spinbox para año (1970-2100)
  - Spinbox para mes (1-12)
- **Botón**: "Aplicar Rango" para validar y aplicar la configuración

### 3. Lógica de Aplicación

#### Método `_apply_date_range_to_engine()` (app.py, líneas 525-541)

Este método interno:
1. Obtiene los valores de año y mes de los controles
2. Normaliza el orden (intercambia si "hasta" < "desde")
3. Construye fechas ISO:
   - Fecha inicio: `YYYY-MM-01`
   - Fecha fin: `YYYY-MM-DD` (último día del mes usando `calendar.monthrange`)
4. Llama a `core.engines.faker_engine.set_date_range(start, end)`

#### Método `apply_date_range()` (app.py, líneas 543-554)

Método público que:
1. Valida que los meses estén en rango 1-12
2. Muestra mensaje de error si la validación falla
3. Llama al método interno `_apply_date_range_to_engine()`
4. Muestra confirmación al usuario

### 4. Integración con Generación de Datos

El método `_apply_date_range_to_engine()` se invoca antes de cada generación:

- **`generate_preview()`** (línea 897): Aplica rango antes de generar preview
- **`generate_single_table()`** (línea 995): Aplica rango antes de generar tabla individual
- **`generate_ecosystem_complete()`** (línea 1152): Aplica rango antes de generar ecosistema

### 5. Motor de Generación (faker_engine.py)

#### Función `set_date_range()` (líneas 57-89)

Establece variables globales que controlan la generación de fechas:
- Acepta formatos `YYYY-MM` o `YYYY-MM-DD`
- Normaliza el orden automáticamente
- Permite limpiar el rango con valores `None`

#### Funciones de Generación de Fechas

Las siguientes funciones respetan el rango global cuando está definido:

1. **`_rand_date()`** (líneas 105-115): Genera fechas ISO aleatorias
2. **`_rand_datetime_utc()`** (líneas 117-130): Genera fechas/horas UTC
3. **`_rand_datetime_local()`** (líneas 132-145): Genera fechas/horas locales

### 6. Persistencia en Metadatos

El rango de fechas se guarda en `session_metadata.json` (app.py, líneas 1266-1268):

```json
{
  "date_range": {
    "from": "YYYY-MM",
    "to": "YYYY-MM"
  }
}
```

## Flujo de Uso

1. Usuario abre la aplicación
2. En Paso 2, configura el rango de fechas usando los spinboxes
3. (Opcional) Hace clic en "Aplicar Rango" para validar
4. Genera datos (preview, tabla individual o ecosistema)
5. El sistema automáticamente aplica el rango configurado
6. Todas las fechas generadas caen dentro del rango especificado

## Validaciones Implementadas

1. **Validación de meses**: Asegura que los meses estén entre 1-12
2. **Normalización automática**: Intercambia "desde" y "hasta" si están invertidos
3. **Último día del mes**: Calcula correctamente usando `calendar.monthrange()`
4. **Años bisiestos**: Maneja correctamente febrero (28 o 29 días)

## Casos de Prueba Verificados

✅ Rango normal (desde < hasta)
✅ Rango invertido (desde > hasta) - auto-swap
✅ Mismo mes
✅ Febrero en año bisiesto (29 días)
✅ Febrero en año no bisiesto (28 días)
✅ Generación de fechas dentro del rango
✅ Limpieza del rango (None, None)

## Ubicación de Archivos Modificados

- `apps/ui_desktop/app.py`: Interfaz de usuario y lógica de aplicación
- `core/engines/faker_engine.py`: Motor de generación de datos con soporte de rango
- `pasos_a_paso/apps_ui_desktop_app_pasos.txt`: Documentación del proceso de implementación

## Próximas Mejoras (Opcional)

- Añadir indicador visual cuando el rango no incluye la fecha actual
- Agregar presets comunes (último mes, último trimestre, último año)
- Validación adicional de rangos muy amplios o muy pequeños
- Selector de fecha con calendario visual

## Estado de Implementación

✅ **COMPLETADO** - La funcionalidad está totalmente implementada y probada.
