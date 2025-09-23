# Organización de Archivos por Tabla

## 📁 Nueva Estructura de Carpetas

A partir de ahora, **cada tabla genera sus archivos en una carpeta separada** con el nombre de la tabla, evitando que se mezclen los archivos.

### 🎯 Estructura Anterior vs Nueva

#### ❌ Anterior (archivos mezclados)
```
outputs/
  ├── creator_intelligence__dim_channel.csv
  ├── creator_intelligence__dim_platform.csv
  ├── finance__dim_customer.csv
  ├── microbusiness__fact_sales.csv
  └── healthcare__dim_trial.csv
```

#### ✅ Nueva (carpetas separadas)
```
outputs/
  ├── dim_channel/
  │   ├── creator_intelligence__dim_channel.csv
  │   └── creator_intelligence__dim_channel_dq_report.json
  ├── dim_platform/
  │   ├── creator_intelligence__dim_platform.csv
  │   └── creator_intelligence__dim_platform_dq_report.json
  ├── dim_customer/
  │   └── finance__dim_customer.csv
  ├── fact_sales/
  │   └── microbusiness__fact_sales.csv
  └── dim_trial/
      └── healthcare__dim_trial.csv
```

## 🚀 Comandos Afectados

### Generación Simple
```bash
python -m apps.cli.main generate creator_intelligence dim_channel --rows 100 --format csv
```
**Resultado:** `outputs/dim_channel/creator_intelligence__dim_channel.csv`

### Generación con SCD2
```bash
python -m apps.cli.main generate-scd2 creator_intelligence dim_channel --rows 100
```
**Resultado:** `outputs/dim_channel/creator_intelligence__dim_channel_scd2.csv`

### Generación Multi-tabla
```bash
python -m apps.cli.main generate-multi finance dim_customer microbusiness dim_staff --primary-rows 50 --secondary-rows 200
```
**Resultado:** 
- `outputs/dim_customer/finance__dim_customer.csv`
- `outputs/dim_staff/finance__dim_staff.csv`

## 🔧 Aplicación de Escritorio

La aplicación de escritorio también usa la nueva estructura. Al generar una tabla desde la UI:
- Se crea automáticamente la carpeta con el nombre de la tabla
- Todos los archivos relacionados (datos + reporte DQ) van a esa carpeta

## 📦 Migración de Archivos Existentes

Si tienes archivos anteriores en la carpeta raíz de `outputs/`, puedes reorganizarlos usando:

```bash
python reorganize_outputs.py
```

Este script:
1. **Detecta** archivos con formato `domain__table.*`
2. **Crea** carpetas con el nombre de cada tabla
3. **Mueve** archivos a sus carpetas correspondientes
4. **Preserva** archivos que no coinciden con el patrón

## ✅ Beneficios

### 🎯 **Organización Clara**
- Cada tabla tiene su propio espacio
- Fácil navegación y búsqueda
- Eliminación de mezcla de archivos

### 📊 **Gestión de Proyectos**
- Datasets de diferentes dominios bien separados
- Facilita comparaciones entre versiones
- Mejor control de versiones

### 🔍 **Facilidad de Uso**
- Encuentra rápidamente archivos de una tabla específica
- Copia/mueve carpetas completas
- Análisis por tabla más sencillo

## 🎪 Ejemplos de Uso

### Generar múltiples tablas de Creator Intelligence
```bash
# Canales
python -m apps.cli.main generate creator_intelligence dim_channel --rows 200 --format csv

# Performance diario
python -m apps.cli.main generate creator_intelligence fact_content_performance_day --rows 1000 --format parquet

# Recomendaciones
python -m apps.cli.main generate creator_intelligence fact_recommendations --rows 500 --format csv
```

**Estructura resultante:**
```
outputs/
  ├── dim_channel/
  │   ├── creator_intelligence__dim_channel.csv
  │   └── creator_intelligence__dim_channel_dq_report.json
  ├── fact_content_performance_day/
  │   ├── creator_intelligence__fact_content_performance_day.parquet
  │   └── creator_intelligence__fact_content_performance_day_dq_report.json
  └── fact_recommendations/
      ├── creator_intelligence__fact_recommendations.csv
      └── creator_intelligence__fact_recommendations_dq_report.json
```

## 🔧 Configuración

No requiere configuración adicional. La funcionalidad está **activa automáticamente** en:

- ✅ CLI (`apps.cli.main`)
- ✅ Aplicación de Escritorio (`apps.ui_desktop.app`)
- ✅ Todos los comandos de generación

¡Tus datos ahora están perfectamente organizados! 🎉