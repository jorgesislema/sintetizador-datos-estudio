# 💡 Ejemplos Prácticos - Sintetizador de Datos

Este documento incluye ejemplos completos paso a paso de cómo usar el sintetizador para diferentes escenarios de ciencia de datos.

## 🎯 Lista de Ejemplos

1. **Análisis Retail Completo** - ETL, EDA, visualizaciones
2. **Pipeline ETL Bancario** - Arquitectura Medallion (Bronze/Silver/Gold)
3. **Predicción de Churn** - Machine Learning end-to-end

---

## Ejemplo 1: Generar y Analizar Datos de Retail

```python
from core.ecosystems import generate_ecosystem_data
import pandas as pd

# Generar datos
data, summary = generate_ecosystem_data('retail_supermarket', volume=1000)

# Analizar
df_sales = pd.DataFrame(data['fact_ticket_line'])
print(f"Total ventas: ${df_sales['amount'].sum():,.2f}")
print(f"Transacciones: {len(df_sales):,}")
```

Para ejemplos completos y detallados, consulta **GUIA_COMPLETA.md**.

