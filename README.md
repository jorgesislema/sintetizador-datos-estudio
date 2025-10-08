# 🔬 Sintetizador de Datos - Estudio

Generador de datos sintéticos híbrido para analítica, ML y pruebas de ingeniería de datos.

## ✨ Características

- **Arquitectura Modular**: Core dividido en submódulos (engines, dq, integrity, errors, multi, writers, utils)
- **Motores Híbridos**: Faker principal + SDV/CTGAN stubs + time_engine
- **Interfaz Nativa**: Aplicación de escritorio con Tkinter (sin dependencias web)
- **Wizard Interactivo**: Proceso de 3 pasos para configuración fácil
- **Calidad de Datos**: Perfiles de error configurables (none/light/moderate/heavy)
- **SCD2 Automático**: Versionado con cambio probabilístico de campos
- **DQ Integrada**: Métricas en tiempo real (completitud, duplicados, unicidad, validez)
- **Multi-formato**: CSV, Parquet, Arrow, DuckDB
- **Preview Interactivo**: Vista previa antes de generar datasets grandes

## 🚀 Instalación

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno (Windows)
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
pip install -e .
```

### 📦 Dependencias Opcionales

```bash
# Para motores ML avanzados
pip install -r requirements-optional.txt
```

## 🎯 Uso - Interfaz de Escritorio (Recomendado)

La interfaz nativa de escritorio es la forma más fácil de usar el generador:

```bash
# Ejecutar aplicación de escritorio
python launch_desktop.py
```

**Proceso de 3 pasos:**
1. **Selección**: Elige dominio y tabla de los esquemas disponibles
2. **Configuración**: Define tamaño del dataset, perfil de errores, formato de salida
3. **Generación**: Preview opcional + generación completa con métricas en tiempo real

### Características de la UI:
- ✅ Wizard intuitivo de 3 pasos
- ✅ Preview interactivo antes de generar
- ✅ Barra de progreso en tiempo real
- ✅ Métricas DQ automáticas
- ✅ Descarga directa de archivos
- ✅ Interfaz nativa (sin navegador web)

## 💻 Uso - CLI (Avanzado)

Para uso programático o automatización:

```bash
# Listar dominios disponibles
synthedata list-domains

# Listar tablas de un dominio
synthedata list-tables hr_core

# Preview de datos
synthedata preview hr_core employees --rows 5 --error-profile light

# Generar dataset completo
synthedata generate hr_core employees --rows 1000 --format parquet --error-profile moderate --output outputs

# Generar con SCD2
synthedata generate-scd2 hr_core employees --rows 50 --change-prob 0.3

# Generar multi-tabla
synthedata generate-multi hr_core employees sales transactions --primary-rows 20 --secondary-rows 80
```

## 📊 Campos Comunes Incluidos

El generador agrega automáticamente campos comunes a todos los datasets:

```
id, natural_key, tenant_id, source_system, source_table,
batch_id, batch_time_utc,
record_hash,
is_active, valid_from_utc, valid_to_utc,
created_at_utc, created_by, updated_at_utc, updated_by,
pii_sensitivity,
geo_country, geo_region, geo_city, geo_lat, geo_lon,
currency_code, fx_rate_to_usd,
processing_status,
dq_completeness_pct, dq_validity_pct,
tags, notes
```

Notas:
- `natural_key` se infiere heurísticamente: employee_id | transaction_id | ticket_id | id.
- `valid_to_utc` permanece `null` (placeholder SCD2) hasta implementar versionado.
- `geo_*` y `currency_code` son constantes por lote (mejorable con variabilidad configurable).
- `fx_rate_to_usd` placeholder (1.0 para USD→USD).
- `processing_status` pasa a `warn` si se inyectan errores por perfil de error.

## Perfiles de Error
Perfiles predefinidos para simular diferentes niveles de calidad de datos:

- `none`: Sin errores (100% calidad)
- `light`: Errores leves (5% nulls, 2% duplicados, 3% typos, 1% out-of-range)
- `moderate`: Errores moderados (10% nulls, 5% duplicados, 7% typos, 3% out-of-range)
- `heavy`: Errores severos (20% nulls, 10% duplicados, 15% typos, 8% out-of-range)

Los errores incluyen:
- **Nulls**: Valores faltantes en campos no clave
- **Duplicados**: Repetición de valores en campos clave (email, nombre)
- **Typos**: Errores tipográficos en strings (swap, delete, insert, replace)
- **Out-of-range**: Valores numéricos fuera de rango (multiplicados por factores grandes)

## 🎯 Estado Actual

✅ **Completado:**
- Arquitectura modular completa
- Generación dinámica con campos comunes (25+ campos)
- DQ extendida (completitud, duplicados, unicidad, validez)
- SCD2 básico con versionado probabilístico
- Perfiles de error configurables (4 niveles)
- Multi-tabla simple con FKs
- **UI de escritorio nativa con Tkinter** ✅ FUNCIONANDO
- CLI completa con todos los comandos
- Tests funcionales
- **Dominios expandidos**: Enterprise, Microbusiness, Retail, Finance, Healthcare
- **Visualización de columnas**: Muestra campos comunes + específicos por tabla

## 🎉 ¡Interfaz de Escritorio Lista!

La aplicación de escritorio nativa con Tkinter está **completamente funcional**:

```bash
# Ejecutar interfaz gráfica
python -c "import sys; sys.path.insert(0, '.'); import apps.ui_desktop.app as app; app.main()"

# O usar el script de lanzamiento
python launch_desktop.py
```

**Características de la UI nativa:**
- ✅ Wizard de 3 pasos intuitivo
- ✅ Selección de dominio/tabla con descripciones
- ✅ **Visualización completa de columnas disponibles**
- ✅ Preview interactivo de datos
- ✅ Barra de progreso en tiempo real
- ✅ Métricas DQ automáticas
- ✅ Descarga directa de archivos
- ✅ Interfaz nativa (sin navegador)
- ✅ Sin dependencias externas (Tkinter incluido en Python)

## 📋 Arquitectura

```
sintetizador-datos-estudio/
├── core/                    # Núcleo del generador
│   ├── engines/            # Motores de datos (faker, sdv, time)
│   ├── dq/                 # Calidad de datos (profiler)
│   ├── integrity/          # SCD2 y constraints
│   ├── errors/             # Perfiles de error
│   ├── multi/              # Generación multi-tabla
│   ├── writers/            # Exportadores (csv, parquet, etc.)
│   └── utils/              # Utilidades (schemas, seed, geo, fx)
├── apps/
│   ├── cli/                # Interfaz de línea de comandos
│   └── ui-desktop/         # Interfaz gráfica nativa (Tkinter)
├── schemas/                # Definiciones YAML de datos
├── tests/                  # Tests unitarios
└── launch_desktop.py       # Script de lanzamiento UI
```

## Licencia
MIT
