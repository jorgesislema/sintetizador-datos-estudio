"""
Sistema de Ecosistemas de Negocios
Genera datos completos e interconectados para diferentes tipos de negocios
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import uuid

class BusinessType(Enum):
    """Tipos de negocios disponibles"""
    SOCIAL_MEDIA = "social_media"
    ECOMMERCE = "ecommerce"
    BANKING = "banking"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    RETAIL_PHYSICAL = "retail_physical"
    RESTAURANT = "restaurant"
    HOTEL = "hotel"
    STREAMING = "streaming"
    RIDE_SHARING = "ride_sharing"
    DELIVERY = "delivery"
    REAL_ESTATE = "real_estate"
    SAAS = "saas"
    GAMING = "gaming"
    FINTECH = "fintech"

@dataclass
class BusinessEcosystem:
    """Definición de un ecosistema de negocio"""
    business_type: BusinessType
    business_subtype: str
    display_name: str
    description: str
    master_entities: List[str]  # Entidades principales (usuarios, empresas, etc.)
    core_tables: List[str]      # Tablas principales del negocio
    support_tables: List[str]   # Tablas de soporte (catálogos, configuración)
    analytics_tables: List[str] # Tablas de métricas y análisis
    relationships: Dict[str, List[str]]  # Relaciones entre tablas
    required_volume: Dict[str, int]      # Volumen sugerido por tabla
    
# ===============================
# DEFINICIÓN DE ECOSISTEMAS
# ===============================

BUSINESS_ECOSYSTEMS: Dict[str, BusinessEcosystem] = {
    
    # ========== REDES SOCIALES ==========
    "social_media_influencer": BusinessEcosystem(
        business_type=BusinessType.SOCIAL_MEDIA,
        business_subtype="influencer",
        display_name="Influencer Multi-Plataforma",
        description="Creador de contenido con presencia en múltiples redes sociales",
        master_entities=["users", "brands", "content_base"],
        core_tables=[
            "dim_users",
            "dim_social_accounts", 
            "dim_content",
            "fact_posts",
            "fact_engagements",
            "fact_followers"
        ],
        support_tables=[
            "dim_platforms",
            "dim_content_types", 
            "dim_hashtags",
            "dim_demographics",
            "br_user_interests"
        ],
        analytics_tables=[
            "fact_daily_metrics",
            "fact_cross_platform_performance",
            "fact_audience_overlap",
            "fact_monetization"
        ],
        relationships={
            "dim_users": ["dim_social_accounts", "fact_posts", "fact_followers"],
            "dim_social_accounts": ["fact_posts", "fact_engagements"],
            "dim_content": ["fact_posts", "fact_engagements"],
            "fact_posts": ["fact_engagements", "fact_daily_metrics"]
        },
        required_volume={
            "dim_users": 10000,
            "dim_social_accounts": 35000,  # Cada user tiene ~3.5 cuentas
            "dim_content": 50000,
            "fact_posts": 200000,
            "fact_engagements": 2000000,
            "fact_followers": 500000
        }
    ),
    
    "social_media_corporate": BusinessEcosystem(
        business_type=BusinessType.SOCIAL_MEDIA,
        business_subtype="corporate",
        display_name="Empresa Multi-Plataforma",
        description="Empresa con estrategia de marketing digital en múltiples redes",
        master_entities=["companies", "employees", "campaigns"],
        core_tables=[
            "dim_companies",
            "dim_employees",
            "dim_corporate_accounts",
            "dim_campaigns", 
            "fact_corporate_posts",
            "fact_campaign_performance"
        ],
        support_tables=[
            "dim_departments",
            "dim_campaign_types",
            "dim_target_audiences",
            "br_employee_accounts"
        ],
        analytics_tables=[
            "fact_brand_mentions",
            "fact_competitor_analysis",
            "fact_roi_campaigns",
            "fact_customer_acquisition"
        ],
        relationships={
            "dim_companies": ["dim_employees", "dim_corporate_accounts", "dim_campaigns"],
            "dim_employees": ["br_employee_accounts", "fact_corporate_posts"],
            "dim_campaigns": ["fact_corporate_posts", "fact_campaign_performance"]
        },
        required_volume={
            "dim_companies": 1000,
            "dim_employees": 15000,
            "dim_corporate_accounts": 5000,
            "dim_campaigns": 8000,
            "fact_corporate_posts": 150000,
            "fact_campaign_performance": 50000
        }
    ),
    
    # ========== E-COMMERCE ==========
    "ecommerce_marketplace": BusinessEcosystem(
        business_type=BusinessType.ECOMMERCE,
        business_subtype="marketplace",
        display_name="Marketplace Multi-Vendedor",
        description="Plataforma de e-commerce con múltiples vendedores (Amazon, MercadoLibre)",
        master_entities=["customers", "sellers", "products"],
        core_tables=[
            "dim_customers",
            "dim_sellers", 
            "dim_products",
            "fact_orders",
            "fact_order_items",
            "fact_payments"
        ],
        support_tables=[
            "dim_categories",
            "dim_brands",
            "dim_shipping_methods",
            "dim_payment_methods",
            "dim_warehouses",
            "br_product_categories"
        ],
        analytics_tables=[
            "fact_customer_behavior",
            "fact_seller_performance",
            "fact_product_analytics", 
            "fact_recommendation_engine",
            "fact_inventory_movements"
        ],
        relationships={
            "dim_customers": ["fact_orders", "fact_payments", "fact_customer_behavior"],
            "dim_sellers": ["dim_products", "fact_seller_performance"],
            "dim_products": ["fact_order_items", "fact_product_analytics"],
            "fact_orders": ["fact_order_items", "fact_payments"]
        },
        required_volume={
            "dim_customers": 100000,
            "dim_sellers": 5000,
            "dim_products": 500000,
            "fact_orders": 2000000,
            "fact_order_items": 8000000,
            "fact_payments": 2200000
        }
    ),
    
    # ========== BANCA DIGITAL ==========
    "banking_digital": BusinessEcosystem(
        business_type=BusinessType.BANKING,
        business_subtype="digital",
        display_name="Banco Digital Completo",
        description="Banco con servicios digitales, cuentas, préstamos, inversiones",
        master_entities=["customers", "accounts", "products"],
        core_tables=[
            "dim_customers",
            "dim_accounts",
            "dim_bank_products",
            "fact_transactions",
            "fact_balances",
            "fact_loans"
        ],
        support_tables=[
            "dim_transaction_types",
            "dim_account_types", 
            "dim_branches",
            "dim_atms",
            "dim_currencies",
            "br_customer_products"
        ],
        analytics_tables=[
            "fact_risk_assessments",
            "fact_credit_scores",
            "fact_customer_lifetime_value",
            "fact_fraud_detection",
            "fact_regulatory_reports"
        ],
        relationships={
            "dim_customers": ["dim_accounts", "fact_loans", "fact_risk_assessments"],
            "dim_accounts": ["fact_transactions", "fact_balances"],
            "fact_transactions": ["fact_fraud_detection"]
        },
        required_volume={
            "dim_customers": 500000,
            "dim_accounts": 800000,
            "dim_bank_products": 50,
            "fact_transactions": 50000000,
            "fact_balances": 800000,
            "fact_loans": 150000
        }
    ),
    
    # ========== SALUD INTEGRAL ==========
    "healthcare_hospital": BusinessEcosystem(
        business_type=BusinessType.HEALTHCARE,
        business_subtype="hospital",
        display_name="Hospital Completo",
        description="Sistema hospitalario con pacientes, médicos, tratamientos, farmacia",
        master_entities=["patients", "doctors", "treatments"],
        core_tables=[
            "dim_patients",
            "dim_doctors",
            "dim_medical_staff",
            "fact_appointments",
            "fact_treatments",
            "fact_prescriptions"
        ],
        support_tables=[
            "dim_departments",
            "dim_specialties",
            "dim_medications",
            "dim_equipment",
            "dim_rooms",
            "br_doctor_specialties"
        ],
        analytics_tables=[
            "fact_patient_outcomes",
            "fact_resource_utilization", 
            "fact_quality_metrics",
            "fact_billing",
            "fact_insurance_claims"
        ],
        relationships={
            "dim_patients": ["fact_appointments", "fact_treatments", "fact_prescriptions"],
            "dim_doctors": ["fact_appointments", "fact_treatments"],
            "fact_treatments": ["fact_prescriptions", "fact_patient_outcomes"]
        },
        required_volume={
            "dim_patients": 200000,
            "dim_doctors": 2000,
            "dim_medical_staff": 8000,
            "fact_appointments": 1500000,
            "fact_treatments": 800000,
            "fact_prescriptions": 1200000
        }
    ),
    
    # ========== EDUCACIÓN UNIVERSITARIA ==========
    "education_university": BusinessEcosystem(
        business_type=BusinessType.EDUCATION,
        business_subtype="university",
        display_name="Universidad Completa",
        description="Sistema universitario con estudiantes, profesores, cursos, calificaciones",
        master_entities=["students", "professors", "courses"],
        core_tables=[
            "dim_students",
            "dim_professors", 
            "dim_courses",
            "fact_enrollments",
            "fact_grades",
            "fact_attendance"
        ],
        support_tables=[
            "dim_majors",
            "dim_departments",
            "dim_classrooms",
            "dim_semesters",
            "br_course_prerequisites"
        ],
        analytics_tables=[
            "fact_academic_performance",
            "fact_graduation_rates",
            "fact_employment_outcomes",
            "fact_tuition_payments",
            "fact_research_projects"
        ],
        relationships={
            "dim_students": ["fact_enrollments", "fact_grades", "fact_attendance"],
            "dim_professors": ["dim_courses", "fact_research_projects"],
            "dim_courses": ["fact_enrollments", "fact_grades"]
        },
        required_volume={
            "dim_students": 50000,
            "dim_professors": 3000,
            "dim_courses": 8000,
            "fact_enrollments": 400000,
            "fact_grades": 2000000,
            "fact_attendance": 8000000
        }
    ),
    
    # ========== RETAIL FÍSICO ==========
    "retail_supermarket": BusinessEcosystem(
        business_type=BusinessType.RETAIL_PHYSICAL,
        business_subtype="supermarket",
        display_name="Cadena de Supermercados",
        description="Cadena de supermercados con múltiples tiendas, inventario, empleados",
        master_entities=["customers", "stores", "products"],
        core_tables=[
            "dim_customers",
            "dim_stores",
            "dim_products",
            "fact_sales",
            "fact_inventory",
            "fact_employee_shifts"
        ],
        support_tables=[
            "dim_employees",
            "dim_suppliers",
            "dim_categories", 
            "dim_promotions",
            "br_loyalty_programs"
        ],
        analytics_tables=[
            "fact_customer_behavior",
            "fact_store_performance",
            "fact_supply_chain",
            "fact_seasonal_trends",
            "fact_competitor_pricing"
        ],
        relationships={
            "dim_customers": ["fact_sales", "fact_customer_behavior"],
            "dim_stores": ["fact_sales", "fact_inventory", "fact_employee_shifts"],
            "dim_products": ["fact_sales", "fact_inventory"]
        },
        required_volume={
            "dim_customers": 300000,
            "dim_stores": 150,
            "dim_products": 50000,
            "fact_sales": 10000000,
            "fact_inventory": 2000000,
            "fact_employee_shifts": 500000
        }
    ),
    
    # ========== STREAMING ==========
    "streaming_platform": BusinessEcosystem(
        business_type=BusinessType.STREAMING,
        business_subtype="video",
        display_name="Plataforma de Streaming",
        description="Servicio de streaming como Netflix con contenido, usuarios, visualizaciones",
        master_entities=["subscribers", "content", "viewing_sessions"],
        core_tables=[
            "dim_subscribers",
            "dim_content",
            "dim_actors_directors",
            "fact_viewing_sessions",
            "fact_ratings",
            "fact_subscriptions"
        ],
        support_tables=[
            "dim_genres",
            "dim_countries",
            "dim_languages",
            "dim_subscription_plans",
            "br_content_cast"
        ],
        analytics_tables=[
            "fact_content_performance",
            "fact_recommendation_accuracy",
            "fact_churn_analysis",
            "fact_content_costs",
            "fact_regional_preferences"
        ],
        relationships={
            "dim_subscribers": ["fact_viewing_sessions", "fact_ratings", "fact_subscriptions"],
            "dim_content": ["fact_viewing_sessions", "fact_ratings", "fact_content_performance"],
            "fact_viewing_sessions": ["fact_recommendation_accuracy"]
        },
        required_volume={
            "dim_subscribers": 10000000,
            "dim_content": 15000,
            "dim_actors_directors": 100000,
            "fact_viewing_sessions": 500000000,
            "fact_ratings": 50000000,
            "fact_subscriptions": 12000000
        }
    )
}

def get_available_ecosystems() -> Dict[str, BusinessEcosystem]:
    """Obtener todos los ecosistemas disponibles"""
    return BUSINESS_ECOSYSTEMS

def get_ecosystems_by_type(business_type: BusinessType) -> Dict[str, BusinessEcosystem]:
    """Obtener ecosistemas por tipo de negocio"""
    return {
        key: ecosystem for key, ecosystem in BUSINESS_ECOSYSTEMS.items()
        if ecosystem.business_type == business_type
    }

def get_ecosystem_by_key(ecosystem_key: str) -> Optional[BusinessEcosystem]:
    """Obtener un ecosistema específico por clave"""
    return BUSINESS_ECOSYSTEMS.get(ecosystem_key)

def get_business_types() -> List[BusinessType]:
    """Obtener todos los tipos de negocios disponibles"""
    return list(BusinessType)

def get_ecosystem_display_names() -> Dict[str, str]:
    """Obtener nombres para mostrar en UI"""
    return {
        key: ecosystem.display_name 
        for key, ecosystem in BUSINESS_ECOSYSTEMS.items()
    }