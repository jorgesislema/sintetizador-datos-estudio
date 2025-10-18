# 📁 Sistema de Carpetas por Sesión - Sintetizador de Datos

## ✅ Implementación Completada

El sistema de organización por sesión ha sido implementado exitosamente, permitiendo que **todas las tablas generadas en una petición estén dentro de una sola carpeta**.

## 🏗️ Cómo Funciona

### 1. **Carpetas Únicas por Sesión**
Cada vez que generas datos, el sistema crea una carpeta única con formato:
```
session_YYYYMMDD_HHMMSS_[UUID]
```

**Ejemplo**: `session_20250922_110022_47455a41`

### 2. **Organización Automática**
- **Una sesión = Una carpeta**
- **Todas las tablas** de esa sesión van en la misma carpeta
- **Sin carpetas por tabla** - organización por petición/sesión

### 3. **Estructura de Carpeta de Sesión**
```
outputs/
└── session_20250922_110022_47455a41/
    ├── retail__transactions.csv      # Tabla 1
    ├── finance__accounts.csv         # Tabla 2
    ├── healthcare__patients.csv      # Tabla 3
    └── session_metadata.json         # Metadatos de la sesión
```

## 🎮 Controles en la UI

### **Botón "Nueva Sesión"**
- Ubicado en **Paso 2** junto al botón "START"
- Inicia una nueva sesión de trabajo
- Todas las generaciones siguientes van a la nueva carpeta

### **Información de Sesión Activa**
- Se muestra debajo de la barra de progreso
- Indica qué sesión está activa: `"Sesión activa: session_YYYYMMDD_HHMMSS_UUID"`
- Muestra `"Sin sesión activa"` cuando no hay sesión

### **Botón "Abrir Carpeta"**
- Abre directamente la carpeta de la sesión activa
- Si no hay sesión activa, abre la carpeta de outputs general

## 📋 Metadatos de Sesión

Cada sesión incluye un archivo `session_metadata.json` con:

```json
{
  "session_id": "session_20250922_110022_47455a41",
  "created_at": "2025-09-22T11:00:22.758231",
  "language": "Español",
  "geographic_context": "Global",
  "tables_generated": [
    {
      "domain": "retail",
      "table": "transactions", 
      "file_path": "outputs\\session_...\\retail__transactions.csv",
      "row_count": 50,
      "generated_at": "2025-09-22T11:00:22.738795"
    }
  ]
}
```

## 🚀 Flujo de Trabajo

### **Opción 1: Sesión Automática**
1. Ve al **Paso 2**
2. Configura dominio, tabla, etc.
3. Presiona **"START - Generar Dataset"**
4. El sistema crea automáticamente una carpeta de sesión
5. Todas las tablas van a esa carpeta

### **Opción 2: Nueva Sesión Manual**
1. Ve al **Paso 2**
2. Presiona **"Nueva Sesión"** para empezar desde cero
3. Genera múltiples tablas
4. Todas van a la nueva carpeta de sesión

### **Opción 3: Continuar Sesión**
1. Si ya hay una sesión activa, las nuevas tablas se agregan
2. La información de sesión se actualiza automáticamente
3. Los metadatos se mantienen actualizados

## 📊 Ventajas del Sistema

### ✅ **Organización por Petición**
- Todas las tablas relacionadas juntas
- Fácil identificación por timestamp
- Sin mezcla de diferentes trabajos

### ✅ **Trazabilidad Completa**
- Metadatos de configuración usada
- Registro de todas las tablas generadas
- Timestamps de cada generación

### ✅ **Facilidad de Uso**
- Abrir carpeta va directo a la sesión activa
- Controles claros en la UI
- Información visual del estado

### ✅ **Flexibilidad**
- Puedes iniciar nueva sesión cuando quieras
- Continuar sesión existente automáticamente
- Compatible con localización (idioma + geografía)

## 🧪 Ejemplos de Uso

### **Caso 1: Proyecto de Retail**
```
session_20250922_140000_abc123/
├── retail__transactions.csv     # Transacciones
├── retail__products.csv         # Productos  
├── finance__accounts.csv        # Cuentas relacionadas
└── session_metadata.json
```

### **Caso 2: Análisis de Salud** 
```
session_20250922_150000_def456/
├── healthcare__patients.csv     # Pacientes
├── healthcare__lab_results.csv  # Resultados lab
├── healthcare__appointments.csv # Citas
└── session_metadata.json
```

### **Caso 3: Desarrollo Multi-dominio**
```
session_20250922_160000_ghi789/
├── enterprise__hr_core.csv      # RRHH
├── finance__accounts.csv        # Finanzas
├── education__students.csv      # Educación
└── session_metadata.json
```

## 🔧 Implementación Técnica

### **Archivos Modificados**
- `apps/ui_desktop/app.py` - UI y lógica de sesiones
- Nuevos imports: `datetime`, `uuid`
- Nuevos métodos: `create_session_folder()`, `add_table_to_session()`, etc.

### **Variables de Sesión**
```python
self.current_session_id = None    # ID de sesión activa
self.session_folder = None        # Path de carpeta activa
```

### **Generación de ID Únicos**
```python
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
session_uuid = str(uuid.uuid4())[:8]
session_id = f"session_{timestamp}_{session_uuid}"
```

## ✅ Estado Actual

🎯 **Completamente Funcional**:
- ✅ Carpetas únicas por sesión
- ✅ Metadatos automáticos  
- ✅ Controles de UI integrados
- ✅ Apertura directa de carpetas
- ✅ Compatibilidad con localización
- ✅ Pruebas exitosas confirmadas

## 🎉 Resultado Final

El sistema ahora organiza perfectamente todas las tablas generadas en una petición dentro de una sola carpeta, facilitando la gestión y organización de los datos sintéticos generados. 

**¡Ya no más carpetas dispersas por tabla - ahora todo está agrupado por sesión de trabajo!** 🚀