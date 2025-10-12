# 📊 Guía Completa del Sintetizador de Datos - Entorno Completo de Ciencia de Datos

## 🎯 Visión General

Este proyecto proporciona un **ecosistema completo para practicar Data Science**, incluyendo:
- ✅ **ETL** (Extract, Transform, Load)
- ✅ **EDA** (Exploratory Data Analysis)
- ✅ **ML** (Machine Learning)
- ✅ **Automatizaciones**
- ✅ **Dashboards**
- ✅ **Análisis 360° de Negocios**

El sistema genera datos sintéticos realistas que simulan industrias completas con sus ecosistemas de negocio, permitiendo análisis de 360 grados.

---

## 📁 Estructura del Proyecto

```
sintetizador-datos-estudio/
├── core/                      # Motor principal
│   ├── generators.py          # Generación de datos
│   ├── ecosystems/            # 100+ ecosistemas de negocios
│   ├── engines/               # Motores de datos (Faker, etc.)
│   ├── dq/                    # Calidad de datos
│   ├── localization/          # Sistema multiidioma/país
│   └── writers/               # Exportadores
├── apps/
│   ├── ui_desktop/            # Interfaz gráfica (Tkinter)
│   └── cli/                   # Línea de comandos
├── schemas/                   # Definiciones YAML de tablas
│   ├── retail/                # Retail & E-commerce
│   ├── finance/               # Banca & Finanzas
│   ├── healthcare/            # Salud & Farmacia
│   ├── education/             # Educación
│   ├── creator_intelligence/  # Social Media & Content
│   ├── microbusiness/         # Micronegocios
│   └── enterprise/            # Empresas
├── outputs/                   # ⚠️ Salidas (NO versionado en Git)
└── docs/                      # Documentación
```

---

## 🚀 Inicio Rápido

### 1. Instalación

```bash
# Clonar repositorio
git clone https://github.com/jorgesislema/sintetizador-datos-estudio.git
cd sintetizador-datos-estudio

# Crear entorno virtual
python -m venv .venv

# Activar entorno (Windows)
.\.venv\Scripts\Activate.ps1

# Activar entorno (Linux/Mac)
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Uso - Interfaz Gráfica (Recomendado)

```bash
python launch_desktop.py
```

**Flujo en la UI:**
1. **Paso 1**: Seleccionar modo (Tabla Individual vs Ecosistema Completo)
2. **Paso 2**: Configurar parámetros (volumen, formato, localización)
3. **Paso 3**: Generar y revisar resultados

### 3. Uso - Línea de Comandos

```bash
# Listar dominios disponibles
python -m apps.cli.main list-domains

# Generar tabla individual
python -m apps.cli.main generate retail dim_product --rows 1000 --format csv

# Ver preview
python -m apps.cli.main preview finance dim_customer --rows 5
```

---

## 🏢 Ecosistemas de Negocios Completos

### ¿Qué son los Ecosistemas?

Los ecosistemas generan **conjuntos completos e interrelacionados** de datos que representan una industria completa. Cada ecosistema incluye:

- **Entidades maestras** (clientes, productos, empleados)
- **Tablas principales** (transacciones, ventas, órdenes)
- **Tablas de soporte** (direcciones, sesiones, pagos)
- **Tablas analíticas** (métricas, KPIs, reportes)

### Ecosistemas Disponibles (100+)

#### 🛒 Retail & E-commerce
- **retail_supermarket**: Cadena de supermercados
- **ecommerce_marketplace**: Marketplace multi-vendedor
- **ecommerce_fashion_boutique**: Boutique de moda online
- **retail_pharmacy**: Farmacia
- **retail_gas_station**: Gasolinera

#### 🏦 Banca & Finanzas
- **banking_digital**: Banco digital completo
- **fintech_digital_wallet**: Billetera digital
- **fintech_lending_platform**: Plataforma de préstamos

#### 🏥 Salud
- **healthcare_hospital**: Hospital completo
- **healthcare_dental_clinic**: Clínica dental
- **healthcare_veterinary_clinic**: Clínica veterinaria
- **healthcare_mental_health**: Centro de salud mental

#### 🎓 Educación
- **education_university**: Universidad completa
- **education_language_school**: Escuela de idiomas
- **education_cooking_school**: Escuela de cocina

#### 📱 Social Media & Contenido
- **social_media_influencer**: Influencer multi-plataforma
- **social_media_corporate**: Empresa multi-plataforma
- **social_media_gaming_streamer**: Streamer de gaming
- **social_media_beauty_influencer**: Influencer de belleza

#### 🏪 Micronegocios (40+)
- **microbusiness_bakery**: Panadería artesanal
- **microbusiness_coffee_shop**: Cafetería local
- **microbusiness_flower_shop**: Floristería
- **microbusiness_auto_repair**: Taller mecánico
- **microbusiness_yoga_studio**: Estudio de yoga
- Y muchos más...

### Ejemplo: Generar Ecosistema Completo

**Desde la UI:**
1. Seleccionar "Ecosistema Completo"
2. Elegir "Cadena de Supermercados"
3. Configurar volumen base: 1000
4. Click en "START"

**Desde CLI (Python):**
```python
from core.ecosystems import generate_ecosystem_data

# Generar ecosistema completo
data, summary = generate_ecosystem_data(
    ecosystem_key='retail_supermarket',
    volume=1000,
    apply_translation=False
)

# El resultado incluye múltiples tablas
print(f"Tablas generadas: {len(data)}")
print(f"Total de registros: {summary['total_records']:,}")

# Tablas generadas (ejemplo):
# - dim_store: 3 registros
# - dim_product: 8,000 registros
# - dim_customer: 2,000 registros
# - fact_ticket_line: 20,000 registros
# - dim_cashier: 100 registros
# - fact_cash_drawer: 5,000 registros
# - fact_voids: 500 registros
# - fact_returns: 800 registros
```

---

## 🌍 Sistema de Localización

### Países Soportados (13)

**Latinoamérica:**
- Ecuador, Colombia, México, Argentina, Chile, Perú

**Europa:**
- España, Francia, Alemania, Italia

**Norteamérica:**
- USA, Canadá

**Global:**
- Contexto mundial genérico

### Configurar Localización

**En la UI:**
- Paso 2 → Selector de País
- Paso 2 → Selector de Idioma (Español/English)

**Por código:**
```python
from core.engines.faker_engine import set_geographic_context
from core.localization.i18n import translate_complete_dataset

# Configurar país
set_geographic_context('colombia')  # Teléfonos +57, COP

# Generar datos
data = generate('finance', 'dim_customer', 100)

# Traducir al español
data_es = translate_complete_dataset(data, "es")
```

### Datos Localizados

El sistema genera automáticamente:
- ✅ Ciudades reales del país
- ✅ Formatos de teléfono correctos
- ✅ Códigos postales válidos
- ✅ Monedas locales
- ✅ Direcciones auténticas

---

## 📊 Análisis 360° de Negocios

### Vista Completa del Negocio

Cada ecosistema proporciona datos para análisis multidimensional:

#### 1. **Dimensión Cliente**
- Demografía
- Comportamiento de compra
- Segmentación
- Lifetime value

#### 2. **Dimensión Producto**
- Catálogo completo
- Inventario
- Performance de ventas
- Rotación

#### 3. **Dimensión Operacional**
- Transacciones
- Empleados/Cajeros
- Turnos
- Cajas

#### 4. **Dimensión Financiera**
- Ventas
- Devoluciones
- Anulaciones
- Métricas de efectivo

#### 5. **Dimensión Temporal**
- Tendencias diarias
- Estacionalidad
- Patrones horarios
- Análisis de cohortes

### Ejemplo: Análisis Retail 360°

```python
import pandas as pd
from core.ecosystems import generate_ecosystem_data

# Generar datos completos
data, summary = generate_ecosystem_data('retail_supermarket', volume=1000)

# Convertir a DataFrames
df_sales = pd.DataFrame(data['fact_ticket_line'])
df_products = pd.DataFrame(data['dim_product'])
df_customers = pd.DataFrame(data['dim_customer'])
df_stores = pd.DataFrame(data['dim_store'])

# 1. Análisis de Ventas por Producto
sales_by_product = df_sales.groupby('product_id').agg({
    'quantity': 'sum',
    'amount': 'sum'
}).sort_values('amount', ascending=False)

# 2. Análisis de Clientes
customer_metrics = df_sales.groupby('customer_id').agg({
    'ticket_id': 'nunique',      # Número de compras
    'amount': ['sum', 'mean']     # Valor total y promedio
})

# 3. Performance por Tienda
store_performance = df_sales.merge(df_stores, on='store_id').groupby('store_name').agg({
    'amount': 'sum',
    'ticket_id': 'nunique'
})

# 4. Análisis Temporal
df_sales['sale_date'] = pd.to_datetime(df_sales['created_at_utc'])
daily_sales = df_sales.groupby(df_sales['sale_date'].dt.date)['amount'].sum()

# 5. Segmentación RFM (Recency, Frequency, Monetary)
# ... análisis avanzado
```

---

## 🔬 Práctica de ETL

### Pipeline ETL Completo

#### Extract (Extracción)

```python
from core.ecosystems import generate_ecosystem_data
import pandas as pd

# Generar datos raw
raw_data, summary = generate_ecosystem_data('banking_digital', volume=500)

# Simular múltiples fuentes
source_1 = pd.DataFrame(raw_data['dim_customer'])
source_2 = pd.DataFrame(raw_data['fact_transactions'])
source_3 = pd.DataFrame(raw_data['dim_account'])
```

#### Transform (Transformación)

```python
# 1. Limpieza de datos
def clean_data(df):
    # Eliminar duplicados
    df = df.drop_duplicates()
    
    # Manejar valores nulos
    df = df.fillna({
        'notes': 'N/A',
        'tags': ''
    })
    
    # Normalizar texto
    if 'email' in df.columns:
        df['email'] = df['email'].str.lower()
    
    return df

# 2. Transformaciones de negocio
def add_business_rules(df_transactions):
    # Clasificar transacciones
    df_transactions['transaction_type'] = df_transactions['amount'].apply(
        lambda x: 'DEBIT' if x < 0 else 'CREDIT'
    )
    
    # Calcular métricas derivadas
    df_transactions['is_large_transaction'] = df_transactions['amount'].abs() > 1000
    
    return df_transactions

# 3. Agregaciones
def create_customer_summary(df_transactions):
    return df_transactions.groupby('customer_id').agg({
        'id': 'count',                # Número de transacciones
        'amount': ['sum', 'mean'],    # Total y promedio
        'created_at_utc': ['min', 'max']  # Primera y última transacción
    }).reset_index()

# Aplicar transformaciones
cleaned_customers = clean_data(source_1)
transformed_transactions = add_business_rules(clean_data(source_2))
customer_summary = create_customer_summary(transformed_transactions)
```

#### Load (Carga)

```python
from pathlib import Path

# Crear estructura de data warehouse
output_dir = Path('./outputs/data_warehouse')
output_dir.mkdir(parents=True, exist_ok=True)

# Capa Bronze (Raw)
bronze_dir = output_dir / 'bronze'
bronze_dir.mkdir(exist_ok=True)
source_1.to_parquet(bronze_dir / 'raw_customers.parquet')
source_2.to_parquet(bronze_dir / 'raw_transactions.parquet')

# Capa Silver (Cleaned)
silver_dir = output_dir / 'silver'
silver_dir.mkdir(exist_ok=True)
cleaned_customers.to_parquet(silver_dir / 'customers.parquet')
transformed_transactions.to_parquet(silver_dir / 'transactions.parquet')

# Capa Gold (Business)
gold_dir = output_dir / 'gold'
gold_dir.mkdir(exist_ok=True)
customer_summary.to_parquet(gold_dir / 'customer_metrics.parquet')
```

---

## 📈 Práctica de EDA (Exploratory Data Analysis)

### Análisis Exploratorio Completo

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from core.ecosystems import generate_ecosystem_data

# Generar datos
data, _ = generate_ecosystem_data('ecommerce_marketplace', volume=1000)

# DataFrames
df_orders = pd.DataFrame(data['fact_orders'])
df_products = pd.DataFrame(data['dim_product'])
df_customers = pd.DataFrame(data['dim_customer'])

# ====== 1. ESTADÍSTICAS DESCRIPTIVAS ======
print("=== Estadísticas de Órdenes ===")
print(df_orders.describe())

print("\n=== Información del Dataset ===")
print(df_orders.info())

# ====== 2. ANÁLISIS DE DISTRIBUCIONES ======
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
df_orders['order_amount'].hist(bins=50)
plt.title('Distribución de Montos de Órdenes')
plt.xlabel('Monto')
plt.ylabel('Frecuencia')

plt.subplot(1, 3, 2)
df_orders['order_amount'].plot(kind='box')
plt.title('Box Plot - Montos')

plt.subplot(1, 3, 3)
df_orders.groupby('customer_id').size().hist(bins=30)
plt.title('Órdenes por Cliente')
plt.xlabel('Número de Órdenes')

plt.tight_layout()
plt.savefig('outputs/eda_distributions.png')

# ====== 3. ANÁLISIS TEMPORAL ======
df_orders['order_date'] = pd.to_datetime(df_orders['created_at_utc'])
df_orders['month'] = df_orders['order_date'].dt.month
df_orders['day_of_week'] = df_orders['order_date'].dt.dayofweek

monthly_sales = df_orders.groupby('month')['order_amount'].sum()
daily_sales = df_orders.groupby('day_of_week')['order_amount'].mean()

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
monthly_sales.plot(kind='bar')
plt.title('Ventas Mensuales')

plt.subplot(1, 2, 2)
daily_sales.plot(kind='bar')
plt.title('Ventas Promedio por Día de la Semana')
plt.xticks(range(7), ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'])

plt.tight_layout()
plt.savefig('outputs/eda_temporal.png')

# ====== 4. CORRELACIONES ======
# Seleccionar columnas numéricas
numeric_cols = df_orders.select_dtypes(include=[np.number]).columns
correlation_matrix = df_orders[numeric_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Matriz de Correlación')
plt.savefig('outputs/eda_correlation.png')

# ====== 5. ANÁLISIS DE VALORES FALTANTES ======
missing_data = df_orders.isnull().sum()
missing_pct = (missing_data / len(df_orders)) * 100
missing_df = pd.DataFrame({
    'Missing_Count': missing_data,
    'Percentage': missing_pct
}).sort_values('Percentage', ascending=False)

print("\n=== Valores Faltantes ===")
print(missing_df[missing_df['Missing_Count'] > 0])

# ====== 6. OUTLIERS ======
def detect_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df[column] < Q1 - 1.5*IQR) | (df[column] > Q3 + 1.5*IQR)]
    return outliers

amount_outliers = detect_outliers_iqr(df_orders, 'order_amount')
print(f"\n=== Outliers en Montos ===")
print(f"Número de outliers: {len(amount_outliers)}")
print(f"Porcentaje: {(len(amount_outliers)/len(df_orders))*100:.2f}%")
```

---

## 🤖 Práctica de Machine Learning

### Casos de Uso ML

#### 1. Clasificación: Predicción de Churn

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from core.ecosystems import generate_ecosystem_data

# Generar datos
data, _ = generate_ecosystem_data('banking_digital', volume=2000)

# Preparar datos
df_customers = pd.DataFrame(data['dim_customer'])
df_transactions = pd.DataFrame(data['fact_transactions'])

# Feature engineering
customer_features = df_transactions.groupby('customer_id').agg({
    'id': 'count',                    # Número de transacciones
    'amount': ['sum', 'mean', 'std'], # Métricas de monto
    'created_at_utc': lambda x: (pd.Timestamp.now() - pd.to_datetime(x).max()).days  # Recency
}).reset_index()

customer_features.columns = ['customer_id', 'num_transactions', 'total_amount', 
                              'avg_amount', 'std_amount', 'days_since_last']

# Crear target (simulado): churn si no hay transacciones recientes
customer_features['churned'] = (customer_features['days_since_last'] > 90).astype(int)

# Preparar features
X = customer_features[['num_transactions', 'total_amount', 'avg_amount', 
                        'std_amount', 'days_since_last']]
y = customer_features['churned']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluar
y_pred = model.predict(X_test)
print("=== Predicción de Churn ===")
print(classification_report(y_test, y_pred))
print("\nMatriz de Confusión:")
print(confusion_matrix(y_test, y_pred))

# Feature importance
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
print("\nImportancia de Features:")
print(feature_importance)
```

#### 2. Regresión: Predicción de Ventas

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Generar datos
data, _ = generate_ecosystem_data('retail_supermarket', volume=1000)

df_sales = pd.DataFrame(data['fact_ticket_line'])

# Preparar datos temporales
df_sales['sale_date'] = pd.to_datetime(df_sales['created_at_utc'])
df_sales['day_of_week'] = df_sales['sale_date'].dt.dayofweek
df_sales['hour'] = df_sales['sale_date'].dt.hour
df_sales['month'] = df_sales['sale_date'].dt.month

# Agregación diaria
daily_sales = df_sales.groupby(df_sales['sale_date'].dt.date).agg({
    'amount': 'sum',
    'quantity': 'sum',
    'ticket_id': 'nunique'
}).reset_index()

daily_sales.columns = ['date', 'total_sales', 'total_quantity', 'num_tickets']
daily_sales['date'] = pd.to_datetime(daily_sales['date'])
daily_sales['day_num'] = (daily_sales['date'] - daily_sales['date'].min()).dt.days

# Features y target
X = daily_sales[['day_num', 'total_quantity', 'num_tickets']]
y = daily_sales['total_sales']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelo
model = LinearRegression()
model.fit(X_train, y_train)

# Predicciones
y_pred = model.predict(X_test)

print("=== Predicción de Ventas ===")
print(f"R² Score: {r2_score(y_test, y_pred):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")
```

#### 3. Clustering: Segmentación de Clientes

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Generar datos
data, _ = generate_ecosystem_data('ecommerce_marketplace', volume=1500)

df_orders = pd.DataFrame(data['fact_orders'])

# RFM Features
current_date = pd.Timestamp.now()
df_orders['order_date'] = pd.to_datetime(df_orders['created_at_utc'])

rfm = df_orders.groupby('customer_id').agg({
    'order_date': lambda x: (current_date - x.max()).days,  # Recency
    'order_id': 'count',                                      # Frequency
    'order_amount': 'sum'                                     # Monetary
}).reset_index()

rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']

# Escalar features
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[['recency', 'frequency', 'monetary']])

# K-Means Clustering
kmeans = KMeans(n_clusters=4, random_state=42)
rfm['cluster'] = kmeans.fit_predict(rfm_scaled)

# Análisis de clusters
cluster_summary = rfm.groupby('cluster').agg({
    'recency': 'mean',
    'frequency': 'mean',
    'monetary': 'mean',
    'customer_id': 'count'
}).round(2)

cluster_summary.columns = ['Avg_Recency', 'Avg_Frequency', 'Avg_Monetary', 'Customer_Count']

print("=== Segmentación de Clientes ===")
print(cluster_summary)

# Visualización
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(rfm['recency'], rfm['frequency'], rfm['monetary'], 
                     c=rfm['cluster'], cmap='viridis')
ax.set_xlabel('Recency')
ax.set_ylabel('Frequency')
ax.set_zlabel('Monetary')
plt.colorbar(scatter)
plt.title('Segmentación RFM')
plt.savefig('outputs/customer_segmentation.png')
```

---

## ⚙️ Automatizaciones

### Script de ETL Automatizado

```python
#!/usr/bin/env python3
"""
Script de automatización ETL
Ejecutar diariamente para actualizar data warehouse
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
from core.ecosystems import generate_ecosystem_data

def etl_pipeline(ecosystem_key, volume, output_base_dir='./outputs/warehouse'):
    """Pipeline ETL automatizado"""
    
    print(f"[{datetime.now()}] Iniciando ETL para {ecosystem_key}")
    
    # 1. Extract
    print("  [Extract] Generando datos...")
    data, summary = generate_ecosystem_data(ecosystem_key, volume)
    
    # 2. Transform
    print("  [Transform] Procesando datos...")
    transformed_data = {}
    for table_name, records in data.items():
        df = pd.DataFrame(records)
        
        # Limpiar
        df = df.drop_duplicates()
        
        # Agregar timestamp de procesamiento
        df['etl_processed_at'] = datetime.now()
        
        transformed_data[table_name] = df
    
    # 3. Load
    print("  [Load] Guardando datos...")
    output_dir = Path(output_base_dir) / ecosystem_key / datetime.now().strftime('%Y%m%d')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for table_name, df in transformed_data.items():
        output_file = output_dir / f"{table_name}.parquet"
        df.to_parquet(output_file, index=False)
        print(f"    ✓ {table_name}: {len(df)} registros → {output_file}")
    
    # Generar reporte
    report = {
        'ecosystem': ecosystem_key,
        'execution_time': datetime.now().isoformat(),
        'tables_processed': len(transformed_data),
        'total_records': sum(len(df) for df in transformed_data.values()),
        'summary': summary
    }
    
    report_file = output_dir / '_etl_report.json'
    import json
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"[{datetime.now()}] ETL completado. Reporte: {report_file}")
    return report

if __name__ == '__main__':
    # Ejecutar para múltiples ecosistemas
    ecosystems = [
        ('retail_supermarket', 500),
        ('banking_digital', 300),
        ('healthcare_hospital', 400)
    ]
    
    for eco_key, vol in ecosystems:
        etl_pipeline(eco_key, vol)
```

### Automatización con Cron/Task Scheduler

**Linux/Mac (Crontab):**
```bash
# Editar crontab
crontab -e

# Ejecutar diariamente a las 2 AM
0 2 * * * cd /path/to/project && /path/to/.venv/bin/python etl_automation.py
```

**Windows (Task Scheduler):**
```powershell
# Crear tarea programada
$action = New-ScheduledTaskAction -Execute "python" -Argument "etl_automation.py" -WorkingDirectory "C:\path\to\project"
$trigger = New-ScheduledTaskTrigger -Daily -At 2am
Register-ScheduledTask -TaskName "ETL_Daily" -Action $action -Trigger $trigger
```

---

## 📊 Dashboards

### Dashboard con Pandas + Matplotlib

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from core.ecosystems import generate_ecosystem_data

class BusinessDashboard:
    def __init__(self, ecosystem_key, volume=1000):
        # Generar datos
        self.data, self.summary = generate_ecosystem_data(ecosystem_key, volume)
        self.ecosystem_key = ecosystem_key
        
    def create_sales_dashboard(self):
        """Dashboard de ventas retail"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle(f'Dashboard de Ventas - {self.ecosystem_key}', fontsize=16)
        
        # Datos
        df_sales = pd.DataFrame(self.data.get('fact_ticket_line', []))
        df_products = pd.DataFrame(self.data.get('dim_product', []))
        
        if df_sales.empty:
            print("No hay datos de ventas")
            return
        
        # 1. Ventas totales por día
        df_sales['date'] = pd.to_datetime(df_sales['created_at_utc']).dt.date
        daily_sales = df_sales.groupby('date')['amount'].sum()
        axes[0, 0].plot(daily_sales.index, daily_sales.values)
        axes[0, 0].set_title('Ventas Diarias')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # 2. Distribución de montos
        axes[0, 1].hist(df_sales['amount'], bins=50, edgecolor='black')
        axes[0, 1].set_title('Distribución de Montos')
        axes[0, 1].set_xlabel('Monto')
        
        # 3. Top 10 productos
        top_products = df_sales.groupby('product_id')['amount'].sum().nlargest(10)
        axes[0, 2].barh(range(len(top_products)), top_products.values)
        axes[0, 2].set_title('Top 10 Productos')
        axes[0, 2].set_yticks(range(len(top_products)))
        axes[0, 2].set_yticklabels([f'Prod {pid}' for pid in top_products.index])
        
        # 4. Transacciones por hora
        df_sales['hour'] = pd.to_datetime(df_sales['created_at_utc']).dt.hour
        hourly = df_sales.groupby('hour').size()
        axes[1, 0].bar(hourly.index, hourly.values)
        axes[1, 0].set_title('Transacciones por Hora')
        axes[1, 0].set_xlabel('Hora')
        
        # 5. Métricas clave
        total_sales = df_sales['amount'].sum()
        avg_ticket = df_sales['amount'].mean()
        num_transactions = len(df_sales)
        
        metrics_text = f"Total Ventas: ${total_sales:,.2f}\n"
        metrics_text += f"Ticket Promedio: ${avg_ticket:,.2f}\n"
        metrics_text += f"Transacciones: {num_transactions:,}"
        
        axes[1, 1].text(0.1, 0.5, metrics_text, fontsize=14, 
                        verticalalignment='center', family='monospace')
        axes[1, 1].axis('off')
        axes[1, 1].set_title('Métricas Clave')
        
        # 6. Performance por tienda (si existe)
        if 'store_id' in df_sales.columns:
            store_sales = df_sales.groupby('store_id')['amount'].sum()
            axes[1, 2].pie(store_sales.values, labels=[f'Store {sid}' for sid in store_sales.index],
                          autopct='%1.1f%%')
            axes[1, 2].set_title('Ventas por Tienda')
        
        plt.tight_layout()
        plt.savefig(f'outputs/dashboard_{self.ecosystem_key}.png', dpi=150)
        print(f"Dashboard guardado en outputs/dashboard_{self.ecosystem_key}.png")
        
        return fig

# Usar dashboard
dashboard = BusinessDashboard('retail_supermarket', volume=1000)
dashboard.create_sales_dashboard()
```

### Dashboard Interactivo (Bonus: Streamlit)

```python
# dashboard_streamlit.py
import streamlit as st
import pandas as pd
import plotly.express as px
from core.ecosystems import generate_ecosystem_data

st.set_page_config(page_title="Dashboard de Negocios", layout="wide")

st.title("📊 Dashboard Interactivo de Análisis de Negocios")

# Sidebar
ecosystem = st.sidebar.selectbox(
    "Seleccionar Ecosistema",
    ['retail_supermarket', 'banking_digital', 'healthcare_hospital']
)

volume = st.sidebar.slider("Volumen de Datos", 100, 5000, 1000)

if st.sidebar.button("Generar Datos"):
    with st.spinner("Generando datos..."):
        data, summary = generate_ecosystem_data(ecosystem, volume)
        st.session_state['data'] = data
        st.session_state['summary'] = summary

if 'data' in st.session_state:
    # Métricas principales
    col1, col2, col3 = st.columns(3)
    summary = st.session_state['summary']
    
    col1.metric("Total Tablas", summary['total_tables'])
    col2.metric("Total Registros", f"{summary['total_records']:,}")
    col3.metric("Volumen Base", summary['base_volume'])
    
    # Tablas generadas
    st.subheader("Tablas Generadas")
    tables_df = pd.DataFrame(list(summary['tables_summary'].items()), 
                              columns=['Tabla', 'Registros'])
    
    fig = px.bar(tables_df, x='Tabla', y='Registros', 
                 title="Registros por Tabla")
    st.plotly_chart(fig, use_container_width=True)
    
    # Vista de datos
    st.subheader("Vista de Datos")
    selected_table = st.selectbox("Seleccionar Tabla", 
                                   list(st.session_state['data'].keys()))
    
    if selected_table:
        df = pd.DataFrame(st.session_state['data'][selected_table])
        st.dataframe(df.head(100))
        
        # Estadísticas
        st.subheader("Estadísticas")
        st.write(df.describe())
```

**Ejecutar:**
```bash
pip install streamlit plotly
streamlit run dashboard_streamlit.py
```

---

## 🎓 Calidad de Datos (DQ)

### Perfiles de Error

El sistema incluye 4 perfiles de error para simular datos reales:

| Perfil | Nulls | Duplicados | Typos | Out-of-Range |
|--------|-------|------------|-------|--------------|
| **none** | 0% | 0% | 0% | 0% |
| **light** | 5% | 2% | 3% | 1% |
| **moderate** | 10% | 5% | 7% | 3% |
| **heavy** | 20% | 10% | 15% | 8% |

### Análisis de Calidad

```python
from core.dq.profiler import profile
from core.generators import generate

# Generar datos con errores
data_clean = generate('finance', 'dim_customer', 1000, error_profile='none')
data_dirty = generate('finance', 'dim_customer', 1000, error_profile='heavy')

# Analizar calidad
metrics_clean = profile(data_clean)
metrics_dirty = profile(data_dirty)

# Comparar
import pandas as pd
comparison = pd.DataFrame({
    'Métrica': ['Completitud', 'Unicidad', 'Validez'],
    'Clean': [
        metrics_clean['email']['completeness'],
        metrics_clean['email']['uniqueness_ratio'],
        metrics_clean['email']['validity']
    ],
    'Dirty': [
        metrics_dirty['email']['completeness'],
        metrics_dirty['email']['uniqueness_ratio'],
        metrics_dirty['email']['validity']
    ]
})

print(comparison)
```

---

## 📝 Casos de Uso Completos

### Caso 1: Análisis de Retail Completo

```python
"""
Análisis completo de una cadena de supermercados
Incluye: ETL, EDA, ML, Dashboard
"""
from core.ecosystems import generate_ecosystem_data
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

# 1. GENERAR DATOS
print("1. Generando ecosistema retail...")
data, summary = generate_ecosystem_data('retail_supermarket', volume=2000)

# 2. ETL - PREPARACIÓN
print("2. Preparando datos...")
df_sales = pd.DataFrame(data['fact_ticket_line'])
df_products = pd.DataFrame(data['dim_product'])
df_customers = pd.DataFrame(data['dim_customer'])
df_stores = pd.DataFrame(data['dim_store'])

# Limpiar y enriquecer
df_sales['sale_date'] = pd.to_datetime(df_sales['created_at_utc'])
df_sales['day_of_week'] = df_sales['sale_date'].dt.dayofweek
df_sales['hour'] = df_sales['sale_date'].dt.hour
df_sales['month'] = df_sales['sale_date'].dt.month

# Join con productos
df_enriched = df_sales.merge(df_products[['id', 'product_name']], 
                              left_on='product_id', right_on='id', 
                              suffixes=('', '_product'))

# 3. EDA - EXPLORACIÓN
print("3. Análisis exploratorio...")

# Ventas por tienda
store_sales = df_enriched.groupby('store_id').agg({
    'amount': 'sum',
    'quantity': 'sum',
    'ticket_id': 'nunique'
})

# Productos top
top_products = df_enriched.groupby('product_name')['amount'].sum().nlargest(20)

# Patrones temporales
hourly_pattern = df_enriched.groupby('hour')['amount'].mean()
daily_pattern = df_enriched.groupby('day_of_week')['amount'].mean()

# 4. ML - PREDICCIÓN
print("4. Modelo de predicción de ventas...")

# Preparar features para predicción diaria
daily_agg = df_enriched.groupby(df_enriched['sale_date'].dt.date).agg({
    'amount': 'sum',
    'quantity': 'sum',
    'ticket_id': 'nunique'
}).reset_index()

daily_agg.columns = ['date', 'total_sales', 'total_quantity', 'num_tickets']
daily_agg['date'] = pd.to_datetime(daily_agg['date'])
daily_agg['day_of_week'] = daily_agg['date'].dt.dayofweek
daily_agg['day_num'] = (daily_agg['date'] - daily_agg['date'].min()).dt.days

# Features
X = daily_agg[['day_num', 'day_of_week', 'total_quantity', 'num_tickets']]
y = daily_agg['total_sales']

# Modelo
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

score = model.score(X_test, y_test)
print(f"  R² Score: {score:.4f}")

# 5. DASHBOARD
print("5. Generando dashboard...")

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Dashboard Completo - Análisis Retail', fontsize=16)

# Gráficos
axes[0, 0].bar(range(len(top_products)), top_products.values)
axes[0, 0].set_title('Top 20 Productos')
axes[0, 0].set_xlabel('Producto')

axes[0, 1].plot(hourly_pattern.index, hourly_pattern.values)
axes[0, 1].set_title('Patrón de Ventas por Hora')
axes[0, 1].set_xlabel('Hora del Día')

axes[0, 2].bar(daily_pattern.index, daily_pattern.values)
axes[0, 2].set_title('Ventas por Día de la Semana')
axes[0, 2].set_xticks(range(7))
axes[0, 2].set_xticklabels(['L', 'M', 'X', 'J', 'V', 'S', 'D'])

axes[1, 0].bar(range(len(store_sales)), store_sales['amount'].values)
axes[1, 0].set_title('Ventas por Tienda')

axes[1, 1].scatter(y_test, model.predict(X_test), alpha=0.5)
axes[1, 1].plot([y_test.min(), y_test.max()], 
                [y_test.min(), y_test.max()], 'r--')
axes[1, 1].set_title(f'Predicción vs Real (R²={score:.3f})')
axes[1, 1].set_xlabel('Real')
axes[1, 1].set_ylabel('Predicción')

# Métricas
metrics_text = f"""
MÉTRICAS CLAVE
================
Total Ventas: ${df_enriched['amount'].sum():,.2f}
Ticket Promedio: ${df_enriched['amount'].mean():,.2f}
Transacciones: {len(df_enriched):,}
Productos Únicos: {df_enriched['product_id'].nunique()}
Clientes: {df_enriched['customer_id'].nunique()}
Tiendas: {df_enriched['store_id'].nunique()}
"""

axes[1, 2].text(0.1, 0.5, metrics_text, fontsize=10,
                verticalalignment='center', family='monospace')
axes[1, 2].axis('off')

plt.tight_layout()
plt.savefig('outputs/caso_uso_retail_completo.png', dpi=150)
print("\n✅ Análisis completo. Dashboard guardado en outputs/")
```

### Caso 2: Pipeline ML en Banca

```python
"""
Pipeline completo de ML para detección de fraude en banca
"""
from core.ecosystems import generate_ecosystem_data
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Generar datos bancarios
data, _ = generate_ecosystem_data('banking_digital', volume=3000)

df_transactions = pd.DataFrame(data['fact_transactions'])
df_accounts = pd.DataFrame(data['dim_account'])

# Feature engineering para detección de anomalías
df_transactions['hour'] = pd.to_datetime(df_transactions['created_at_utc']).dt.hour
df_transactions['day_of_week'] = pd.to_datetime(df_transactions['created_at_utc']).dt.dayofweek

# Características por cuenta
account_features = df_transactions.groupby('account_id').agg({
    'amount': ['mean', 'std', 'min', 'max'],
    'id': 'count',
    'hour': lambda x: x.mode()[0] if len(x.mode()) > 0 else 0
}).reset_index()

account_features.columns = ['account_id', 'avg_amount', 'std_amount', 
                             'min_amount', 'max_amount', 'num_transactions', 
                             'most_common_hour']

# Preparar features
features = account_features[['avg_amount', 'std_amount', 'num_transactions', 
                              'most_common_hour']].fillna(0)

# Escalar
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Modelo de detección de anomalías
iso_forest = IsolationForest(contamination=0.1, random_state=42)
anomaly_predictions = iso_forest.fit_predict(features_scaled)

# Resultados
account_features['is_anomaly'] = anomaly_predictions == -1

print("=== Detección de Anomalías ===")
print(f"Total cuentas: {len(account_features)}")
print(f"Anomalías detectadas: {account_features['is_anomaly'].sum()}")
print(f"Porcentaje: {(account_features['is_anomaly'].sum()/len(account_features))*100:.2f}%")

# Exportar cuentas sospechosas
suspicious_accounts = account_features[account_features['is_anomaly']]
suspicious_accounts.to_csv('outputs/suspicious_accounts.csv', index=False)
print("\n✅ Cuentas sospechosas exportadas a outputs/suspicious_accounts.csv")
```

---

## 🔧 Mejores Prácticas

### 1. Organización de Proyectos

```
mi_proyecto_analisis/
├── data/
│   ├── raw/              # Datos sin procesar
│   ├── processed/        # Datos limpios
│   └── final/            # Datasets finales
├── notebooks/
│   ├── 01_exploracion.ipynb
│   ├── 02_limpieza.ipynb
│   └── 03_modelado.ipynb
├── scripts/
│   ├── etl.py
│   ├── generate_data.py
│   └── train_model.py
├── models/               # Modelos entrenados
├── reports/              # Reportes y visualizaciones
└── README.md
```

### 2. Versionamiento de Datos

```python
from pathlib import Path
from datetime import datetime

def save_versioned_data(df, base_name):
    """Guardar datos con versión"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    version_dir = Path('data/versions')
    version_dir.mkdir(exist_ok=True)
    
    filename = version_dir / f"{base_name}_{timestamp}.parquet"
    df.to_parquet(filename)
    
    # Symlink a la versión actual
    current_link = Path('data') / f"{base_name}_current.parquet"
    if current_link.exists():
        current_link.unlink()
    current_link.symlink_to(filename)
    
    return filename
```

### 3. Logging

```python
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/pipeline_{datetime.now():%Y%m%d}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Usar en código
logger.info("Iniciando generación de datos")
logger.warning("Volumen alto detectado")
logger.error("Error en procesamiento")
```

### 4. Configuración Centralizada

```python
# config.py
from pathlib import Path

class Config:
    # Paths
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / 'data'
    OUTPUT_DIR = BASE_DIR / 'outputs'
    
    # Parámetros de generación
    DEFAULT_VOLUME = 1000
    DEFAULT_ECOSYSTEM = 'retail_supermarket'
    
    # Localización
    DEFAULT_COUNTRY = 'ecuador'
    DEFAULT_LANGUAGE = 'es'
    
    # ML
    RANDOM_SEED = 42
    TEST_SIZE = 0.2
    
    # DQ
    ERROR_PROFILE = 'light'

# Usar en scripts
from config import Config

data_path = Config.DATA_DIR / 'raw'
```

---

## ❓ Troubleshooting

### Problema: Memoria insuficiente

```python
# Solución: Procesar en lotes
def generate_large_dataset(ecosystem, total_volume, batch_size=1000):
    """Generar dataset grande en lotes"""
    all_data = {}
    
    num_batches = total_volume // batch_size
    for i in range(num_batches):
        print(f"Procesando lote {i+1}/{num_batches}")
        batch_data, _ = generate_ecosystem_data(ecosystem, batch_size)
        
        # Combinar con lotes anteriores
        for table, records in batch_data.items():
            if table not in all_data:
                all_data[table] = []
            all_data[table].extend(records)
    
    return all_data
```

### Problema: Generación lenta

```python
# Solución: Usar multiprocesamiento
from multiprocessing import Pool

def generate_table_wrapper(args):
    domain, table, rows = args
    return generate(domain, table, rows)

def parallel_generation(tables_config):
    """Generar múltiples tablas en paralelo"""
    with Pool(processes=4) as pool:
        results = pool.map(generate_table_wrapper, tables_config)
    return results
```

### Problema: Datos no realistas

```python
# Solución: Aplicar localización y semilla
from core.engines.faker_engine import set_geographic_context

set_geographic_context('colombia')  # Datos localizados
data = generate('retail', 'customers', 1000, seed=42)  # Reproducible
```

---

## 📚 Recursos Adicionales

### Documentación
- `README.md` - Introducción y setup
- `LOCALIZATION_COMPLETE.md` - Sistema de localización
- `docs/ORGANIZACION_CARPETAS.md` - Estructura de archivos
- `tutorial_ui_tkinter.md` - Guía de UI

### Ejemplos
- `test_system.py` - Tests del sistema
- `test_ecosystem_ui.py` - Tests de ecosistemas
- `test_localization_system.py` - Tests de localización

### Scripts Útiles
- `launch_desktop.py` - Lanzador de UI
- `reorganize_outputs.py` - Organizar archivos de salida

---

## 🎯 Roadmap y Futuras Mejoras

### Corto Plazo
- [ ] Integración con DuckDB para queries SQL
- [ ] Dashboard en tiempo real con WebSocket
- [ ] API REST para generación remota

### Medio Plazo
- [ ] Soporte para más formatos (Avro, ORC)
- [ ] Integración con Apache Airflow
- [ ] Templates de notebooks Jupyter

### Largo Plazo
- [ ] ML AutoML integration
- [ ] Data versioning con DVC
- [ ] Deployment en cloud (AWS/Azure/GCP)

---

## 📞 Soporte

Para preguntas o issues:
1. Revisar esta documentación
2. Consultar los archivos en `docs/`
3. Revisar el código en `core/` y `apps/`

---

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles

---

**Última actualización:** Octubre 2025
**Versión:** 2.0
**Autor:** Sistema de Sintetizador de Datos
