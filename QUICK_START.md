# 🚀 Quick Start - Sintetizador de Datos

## ¡Bienvenido!

Este sistema te permite **generar datos sintéticos realistas** para practicar todo el flujo de trabajo de un científico de datos: ETL, EDA, ML, automatizaciones y dashboards.

---

## ⚡ Inicio Rápido (5 minutos)

### 1. Instalación

```bash
# Clonar repositorio
git clone https://github.com/jorgesislema/sintetizador-datos-estudio.git
cd sintetizador-datos-estudio

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Primera Generación - Interfaz Gráfica

```bash
python launch_desktop.py
```

1. Selecciona "Ecosistema Completo"
2. Elige "Cadena de Supermercados"
3. Volumen: 1000
4. Click "START"

**¡Ya tienes datos para analizar!** Los archivos están en `./outputs/`

### 3. Primera Generación - Python

```python
from core.ecosystems import generate_ecosystem_data
import pandas as pd

# Generar datos
data, summary = generate_ecosystem_data('retail_supermarket', volume=1000)

# Ver resumen
print(f"Tablas: {summary['total_tables']}")
print(f"Registros: {summary['total_records']:,}")

# Analizar ventas
df_sales = pd.DataFrame(data['fact_ticket_line'])
print(f"Total ventas: ${df_sales['amount'].sum():,.2f}")
```

---

## 📚 ¿Qué sigue?

### Para aprender el sistema completo:
👉 **[GUIA_COMPLETA.md](GUIA_COMPLETA.md)** - Tutorial completo con todos los detalles

### Para ver ejemplos de código:
👉 **[EJEMPLOS_PRACTICOS.md](EJEMPLOS_PRACTICOS.md)** - Ejemplos paso a paso

### Para verificar el sistema:
```bash
python verificar_sistema.py
```

---

## 🎯 100+ Ecosistemas Disponibles

### Retail & E-commerce
- `retail_supermarket` - Cadena de supermercados
- `ecommerce_marketplace` - Marketplace multi-vendedor
- `retail_pharmacy` - Farmacia

### Banca & Finanzas
- `banking_digital` - Banco digital completo
- `fintech_digital_wallet` - Billetera digital
- `fintech_lending_platform` - Préstamos P2P

### Salud
- `healthcare_hospital` - Hospital completo
- `healthcare_dental_clinic` - Clínica dental
- `healthcare_veterinary_clinic` - Veterinaria

### Social Media
- `social_media_influencer` - Influencer multi-plataforma
- `social_media_gaming_streamer` - Streamer de gaming
- `social_media_beauty_influencer` - Influencer de belleza

### Micronegocios (40+)
- `microbusiness_coffee_shop` - Cafetería
- `microbusiness_bakery` - Panadería
- `microbusiness_yoga_studio` - Estudio de yoga
- Y muchos más...

**Ver lista completa en:** [GUIA_COMPLETA.md](GUIA_COMPLETA.md#ecosistemas-de-negocios-completos)

---

## 💡 Casos de Uso Comunes

### 1. Practicar ETL
```python
# Generar datos → Limpiar → Cargar en Data Warehouse
# Ver ejemplo completo en GUIA_COMPLETA.md - Sección ETL
```

### 2. Análisis Exploratorio (EDA)
```python
# Generar datos → Estadísticas → Visualizaciones
# Ver ejemplo completo en GUIA_COMPLETA.md - Sección EDA
```

### 3. Machine Learning
```python
# Generar datos → Features → Entrenar modelo → Evaluar
# Ver ejemplo completo en GUIA_COMPLETA.md - Sección ML
```

### 4. Dashboards
```python
# Generar datos → Agregaciones → Visualizaciones interactivas
# Ver ejemplo completo en GUIA_COMPLETA.md - Sección Dashboards
```

---

## 🌍 Localización

Genera datos localizados para 13 países:

```python
from core.engines.faker_engine import set_geographic_context

# Configurar país
set_geographic_context('colombia')  # +57, COP, ciudades de Colombia

# Generar datos
data = generate('finance', 'dim_customer', 100)
```

**Países disponibles:**
- **América Latina:** Ecuador, Colombia, México, Argentina, Chile, Perú
- **Europa:** España, Francia, Alemania, Italia
- **Norteamérica:** USA, Canadá

---

## 📊 Análisis 360° de Negocios

Cada ecosistema proporciona datos para análisis completo:

✅ **Dimensión Cliente** - Demografía, comportamiento, segmentación  
✅ **Dimensión Producto** - Catálogo, inventario, performance  
✅ **Dimensión Operacional** - Transacciones, empleados, turnos  
✅ **Dimensión Financiera** - Ventas, costos, márgenes  
✅ **Dimensión Temporal** - Tendencias, estacionalidad, patrones  

---

## 🎓 Calidad de Datos

4 perfiles de error para simular datos reales:

| Perfil | Descripción | Uso |
|--------|-------------|-----|
| `none` | Datos perfectos | Baseline, ML training |
| `light` | Errores leves (5%) | Datos production normales |
| `moderate` | Errores moderados (10%) | Practicar limpieza |
| `heavy` | Errores severos (20%) | Practicar DQ avanzado |

```python
# Generar con errores
data = generate('finance', 'customers', 1000, error_profile='moderate')
```

---

## 📁 Estructura de Salidas

Los datos se guardan automáticamente en `./outputs/` (excluido de Git):

```
outputs/
├── retail_supermarket_20251012_143022/
│   ├── dim_store.parquet
│   ├── dim_product.parquet
│   ├── fact_ticket_line.parquet
│   └── summary.json
└── banking_digital_20251012_150134/
    ├── dim_customer.parquet
    ├── fact_transactions.parquet
    └── summary.json
```

---

## 🆘 Ayuda

### Verificar que todo funciona:
```bash
python verificar_sistema.py
```

### Ver ecosistemas disponibles:
```bash
python -m apps.cli.main list-domains
```

### Ver tablas de un dominio:
```bash
python -m apps.cli.main list-tables retail
```

### Documentación completa:
- **GUIA_COMPLETA.md** - Tutorial completo
- **EJEMPLOS_PRACTICOS.md** - Código de ejemplos
- **README.md** - Introducción general

---

## 🎉 ¡Comienza Ahora!

```bash
# Opción 1: Interfaz Gráfica
python launch_desktop.py

# Opción 2: Python directo
python -c "from core.ecosystems import generate_ecosystem_data; data, s = generate_ecosystem_data('retail_supermarket', 100); print(f'✓ {s[\"total_records\"]} registros generados')"

# Opción 3: Verificar sistema
python verificar_sistema.py
```

---

**¡A practicar Data Science! 🚀📊🤖**

*Para más información, consulta [GUIA_COMPLETA.md](GUIA_COMPLETA.md)*
