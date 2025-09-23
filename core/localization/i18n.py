"""
Sistema de Internacionalización (i18n) para Nombres de Columnas y Tablas
Soporta traducción de esquemas completos al español
"""
from typing import Dict, List, Any
import copy

# ===== TRADUCCIONES DE COLUMNAS =====

COLUMN_TRANSLATIONS = {
    # ===== CAMPOS COMUNES =====
    "id": "id",
    "natural_key": "clave_natural", 
    "tenant_id": "id_inquilino",
    "created_by": "creado_por",
    "updated_by": "actualizado_por",
    "batch_id": "id_lote",
    "geo_region": "region_geografica",
    "fx_rate_to_usd": "tasa_cambio_usd",
    "processing_status": "estado_procesamiento",
    "tags": "etiquetas",
    "notes": "notas",
    "currency_code": "codigo_moneda",
    
    # ===== CAMPOS DE CLIENTE =====
    "customer_id": "id_cliente",
    "first_name": "nombre",
    "last_name": "apellido", 
    "full_name": "nombre_completo",
    "email": "correo_electronico",
    "phone": "telefono",
    "address": "direccion",
    "city": "ciudad",
    "state": "provincia",
    "country": "pais",
    "postal_code": "codigo_postal",
    "birth_date": "fecha_nacimiento",
    "gender": "genero",
    "marital_status": "estado_civil",
    "income": "ingresos",
    "credit_score": "puntuacion_credito",
    "customer_type": "tipo_cliente",
    "registration_date": "fecha_registro",
    "last_login": "ultimo_acceso",
    "is_active": "esta_activo",
    "preferred_language": "idioma_preferido",
    
    # ===== CAMPOS DE PRODUCTOS =====
    "product_id": "id_producto",
    "product_name": "nombre_producto",
    "product_category": "categoria_producto",
    "product_subcategory": "subcategoria_producto",
    "brand": "marca",
    "model_number": "numero_modelo",
    "unit_price": "precio_unitario",
    "cost_price": "precio_costo",
    "selling_price": "precio_venta",
    "weight": "peso",
    "dimensions": "dimensiones",
    "color": "color",
    "size": "talla",
    "material": "material",
    "description": "descripcion",
    "manufacturer": "fabricante",
    "supplier_name": "nombre_proveedor",
    "stock_quantity": "cantidad_inventario",
    "reorder_level": "nivel_reorden",
    "is_discontinued": "esta_descontinuado",
    
    # ===== CAMPOS DE VENTAS =====
    "sale_id": "id_venta",
    "transaction_id": "id_transaccion", 
    "order_id": "id_pedido",
    "sale_date": "fecha_venta",
    "sale_time": "hora_venta",
    "quantity_sold": "cantidad_vendida",
    "quantity": "cantidad",
    "total_amount": "monto_total",
    "subtotal": "subtotal",
    "tax_amount": "monto_impuesto",
    "discount_amount": "monto_descuento",
    "discount_applied": "descuento_aplicado",
    "payment_method": "metodo_pago",
    "payment_status": "estado_pago",
    "sales_channel": "canal_venta",
    "sales_rep": "representante_ventas",
    "commission": "comision",
    "profit_margin": "margen_ganancia",
    
    # ===== CAMPOS DE EMPLEADOS =====
    "employee_id": "id_empleado",
    "staff_id": "id_personal",
    "employee_name": "nombre_empleado",
    "position": "cargo",
    "department": "departamento",
    "hire_date": "fecha_contratacion",
    "salary": "salario",
    "hourly_rate": "tarifa_hora",
    "supervisor_id": "id_supervisor",
    "employment_status": "estado_empleo",
    "performance_rating": "calificacion_desempeno",
    
    # ===== CAMPOS DE INVENTARIO =====
    "inventory_id": "id_inventario",
    "warehouse_id": "id_almacen",
    "location": "ubicacion",
    "bin_location": "ubicacion_contenedor",
    "transaction_type": "tipo_transaccion",
    "quantity_change": "cambio_cantidad",
    "current_stock": "inventario_actual",
    "available_stock": "inventario_disponible",
    "reserved_stock": "inventario_reservado",
    "minimum_stock": "inventario_minimo",
    "maximum_stock": "inventario_maximo",
    "last_counted": "ultimo_conteo",
    "expiry_date": "fecha_vencimiento",
    "lot_number": "numero_lote",
    "serial_number": "numero_serie",
    
    # ===== CAMPOS DE FECHAS Y TIEMPO =====
    "created_at": "creado_en",
    "updated_at": "actualizado_en",
    "deleted_at": "eliminado_en",
    "start_date": "fecha_inicio",
    "end_date": "fecha_fin",
    "due_date": "fecha_vencimiento",
    "completed_date": "fecha_completado",
    "timestamp": "marca_tiempo",
    "year": "ano",
    "month": "mes", 
    "day": "dia",
    "quarter": "trimestre",
    "week": "semana",
    "fiscal_year": "ano_fiscal",
    
    # ===== CAMPOS CREATOR INTELLIGENCE =====
    "platform_id": "id_plataforma",
    "platform_name": "nombre_plataforma",
    "channel_id": "id_canal",
    "channel_name": "nombre_canal",
    "handle": "usuario",
    "content_id": "id_contenido",
    "content_type": "tipo_contenido",
    "title": "titulo",
    "description": "descripcion",
    "views": "visualizaciones",
    "likes": "me_gusta",
    "comments": "comentarios",
    "shares": "compartidos",
    "subscribers": "suscriptores",
    "duration_s": "duracion_segundos",
    "ctr_pct": "ctr_porcentaje",
    "engagement_rate": "tasa_interaccion",
    "retention_pct": "retencion_porcentaje",
    "revenue_usd": "ingresos_usd",
    "rpm_usd": "rpm_usd",
    "cpm_usd": "cpm_usd",
    "watch_time_hours": "tiempo_visualizacion_horas",
    "impressions": "impresiones",
    "click_through_rate": "tasa_clics",
    "niche_topic": "tema_nicho",
    "hashtag_text": "texto_hashtag",
    "thumbnail_id": "id_miniatura",
    "experiment_id": "id_experimento",
    "test_variant": "variante_prueba",
    "conversion_rate": "tasa_conversion",
    
    # ===== CAMPOS DE SALUD/HEALTHCARE =====
    "patient_id": "id_paciente",
    "trial_id": "id_ensayo",
    "diagnosis": "diagnostico",
    "treatment": "tratamiento",
    "dosage": "dosis",
    "side_effects": "efectos_secundarios",
    "outcome": "resultado",
    "medical_history": "historial_medico",
    "allergies": "alergias",
    "medications": "medicamentos",
    "test_result": "resultado_prueba",
    "lab_value": "valor_laboratorio",
    "reference_range": "rango_referencia",
    "unit_of_measure": "unidad_medida",
    
    # ===== CAMPOS FINANCIEROS =====
    "account_id": "id_cuenta",
    "balance": "saldo",
    "credit_limit": "limite_credito",
    "interest_rate": "tasa_interes",
    "loan_amount": "monto_prestamo",
    "monthly_payment": "pago_mensual",
    "account_type": "tipo_cuenta",
    "transaction_type": "tipo_transaccion",
    "merchant": "comerciante",
    "category": "categoria",
    "risk_score": "puntuacion_riesgo",
    "annual_income": "ingresos_anuales"
}

# ===== TRADUCCIONES DE NOMBRES DE TABLAS =====

TABLE_TRANSLATIONS = {
    # ===== DIMENSIONES =====
    "dim_customer": "dim_cliente",
    "dim_product": "dim_producto", 
    "dim_employee": "dim_empleado",
    "dim_supplier": "dim_proveedor",
    "dim_store": "dim_tienda",
    "dim_date": "dim_fecha",
    "dim_time": "dim_tiempo",
    "dim_geography": "dim_geografia",
    "dim_channel": "dim_canal",
    "dim_platform": "dim_plataforma",
    "dim_content": "dim_contenido",
    "dim_trial": "dim_ensayo",
    "dim_patient": "dim_paciente",
    
    # ===== HECHOS =====
    "fact_sales": "hecho_ventas",
    "fact_inventory": "hecho_inventario", 
    "fact_orders": "hecho_pedidos",
    "fact_transactions": "hecho_transacciones",
    "fact_performance": "hecho_rendimiento",
    "fact_revenue": "hecho_ingresos",
    "fact_expenses": "hecho_gastos",
    "fact_productivity": "hecho_productividad",
    "fact_quality": "hecho_calidad",
    "fact_customer_activity": "hecho_actividad_cliente",
    "fact_content_performance": "hecho_rendimiento_contenido",
    "fact_retention_curve": "hecho_curva_retencion",
    "fact_recommendations": "hecho_recomendaciones",
    "fact_competitive_benchmark": "hecho_benchmark_competitivo",
    "fact_lab_results": "hecho_resultados_laboratorio",
    "fact_clinical_outcomes": "hecho_resultados_clinicos",
    
    # ===== ESPECIALIZADOS =====
    "fact_pos_line": "hecho_linea_pdv",
    "fact_cash_shift": "hecho_turno_caja",
    "fact_bakery_sales": "hecho_ventas_panaderia",
    "fact_hardware_sales": "hecho_ventas_ferreteria",
    "fact_soap_production": "hecho_produccion_jabon",
    "fact_lab_operations": "hecho_operaciones_laboratorio",
    
    # ===== DIMENSIONES ESPECIALIZADAS =====
    "dim_bakery_product": "dim_producto_panaderia",
    "dim_hardware_product": "dim_producto_ferreteria", 
    "dim_soap_product": "dim_producto_jabon",
    "dim_lab_test": "dim_prueba_laboratorio",
    "dim_equipment": "dim_equipo",
    "dim_ingredient": "dim_ingrediente",
    "dim_recipe": "dim_receta",
    "dim_hashtag": "dim_hashtag",
    "dim_experiment": "dim_experimento",
    "dim_schedule_slot": "dim_franja_horaria",
    
    # ===== BRIDGING TABLES =====
    "br_content_hashtag": "br_contenido_hashtag",
    "br_product_category": "br_producto_categoria",
    "br_customer_segment": "br_cliente_segmento"
}

# ===== TRADUCCIONES DE VALORES CATEGÓRICOS =====

CATEGORICAL_VALUE_TRANSLATIONS = {
    # Estados generales
    "Active": "Activo",
    "Inactive": "Inactivo", 
    "Pending": "Pendiente",
    "Completed": "Completado",
    "Cancelled": "Cancelado",
    "Processing": "Procesando",
    "Draft": "Borrador",
    "Published": "Publicado",
    "Archived": "Archivado",
    
    # Tipos de cliente
    "Individual": "Individual",
    "Business": "Empresa",
    "Premium": "Premium",
    "Standard": "Estándar",
    "VIP": "VIP",
    
    # Métodos de pago
    "Cash": "Efectivo",
    "Credit Card": "Tarjeta de Crédito",
    "Debit Card": "Tarjeta de Débito", 
    "Bank Transfer": "Transferencia Bancaria",
    "PayPal": "PayPal",
    "Mobile Payment": "Pago Móvil",
    
    # Géneros
    "Male": "Masculino",
    "Female": "Femenino",
    "Other": "Otro",
    "Prefer not to say": "Prefiero no decir",
    
    # Estados civiles
    "Single": "Soltero",
    "Married": "Casado",
    "Divorced": "Divorciado",
    "Widowed": "Viudo",
    
    # Regiones geográficas
    "North": "Norte",
    "South": "Sur", 
    "East": "Este",
    "West": "Oeste",
    "Central": "Central",
    "Northeast": "Noreste",
    "Southeast": "Sureste",
    "Northwest": "Noroeste",
    "Southwest": "Suroeste",
    
    # Plataformas de contenido
    "YouTube": "YouTube",
    "TikTok": "TikTok", 
    "Instagram": "Instagram",
    "Facebook": "Facebook",
    "Twitter": "Twitter",
    
    # Tipos de contenido
    "Video": "Video",
    "Short": "Corto",
    "Reel": "Reel",
    "Story": "Historia",
    "Live": "En Vivo",
    "Post": "Publicación"
}

# ===== FUNCIONES DE TRADUCCIÓN =====

def translate_column_name(column_name: str, target_language: str = "es") -> str:
    """Traducir nombre de columna al idioma objetivo"""
    if target_language == "es":
        return COLUMN_TRANSLATIONS.get(column_name, column_name)
    return column_name

def translate_table_name(table_name: str, target_language: str = "es") -> str:
    """Traducir nombre de tabla al idioma objetivo"""
    if target_language == "es":
        return TABLE_TRANSLATIONS.get(table_name, table_name)
    return table_name

def translate_categorical_value(value: str, target_language: str = "es") -> str:
    """Traducir valor categórico al idioma objetivo"""
    if target_language == "es" and isinstance(value, str):
        return CATEGORICAL_VALUE_TRANSLATIONS.get(value, value)
    return value

def translate_schema_fields(fields: List[str], target_language: str = "es") -> List[str]:
    """Traducir lista completa de campos de esquema"""
    if target_language == "es":
        return [translate_column_name(field, target_language) for field in fields]
    return fields

def translate_data_row(row: Dict[str, Any], target_language: str = "es") -> Dict[str, Any]:
    """Traducir una fila de datos completa (nombres de columnas y valores categóricos)"""
    if target_language != "es":
        return row
        
    translated_row = {}
    for key, value in row.items():
        # Traducir nombre de columna
        new_key = translate_column_name(key, target_language)
        
        # Traducir valor si es categórico string
        if isinstance(value, str):
            new_value = translate_categorical_value(value, target_language)
        else:
            new_value = value
            
        translated_row[new_key] = new_value
    
    return translated_row

def translate_complete_dataset(data: List[Dict[str, Any]], target_language: str = "es") -> List[Dict[str, Any]]:
    """Traducir dataset completo (todos los registros)"""
    if target_language != "es":
        return data
        
    return [translate_data_row(row, target_language) for row in data]

def get_available_languages() -> List[str]:
    """Obtener lista de idiomas disponibles"""
    return ["en", "es"]

def get_language_display_names() -> Dict[str, str]:
    """Obtener nombres de idiomas para mostrar en UI"""
    return {
        "en": "English",
        "es": "Español"
    }