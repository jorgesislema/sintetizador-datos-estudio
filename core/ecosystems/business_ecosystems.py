"""
Sistema de Ecosistemas de Negocios Actualizado
Genera datos completos e interconectados usando dominios y tablas reales del sistema
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
    RETAIL = "retail"
    MICROBUSINESS = "microbusiness"
    ENTERTAINMENT = "entertainment"

@dataclass
class BusinessEcosystem:
    """Definición de un ecosistema de negocio con dominios y tablas reales"""
    key: str
    name: str
    display_name: str
    description: str
    business_type: BusinessType
    master_entities: List[str]
    core_tables: Dict[str, List[str]]      # domain -> [tables]
    support_tables: Dict[str, List[str]]   # domain -> [tables] 
    analytics_tables: Dict[str, List[str]] # domain -> [tables]
    relationships: Dict[str, str]          # "table_a -> table_b": "foreign_key"
    volume_ratios: Dict[str, float]        # table -> ratio relative to base volume

# ===============================
# DEFINICIÓN DE ECOSISTEMAS REALES
# ===============================

BUSINESS_ECOSYSTEMS: Dict[str, BusinessEcosystem] = {
    
    # Ecosistemas Social Media / Creator Intelligence
    "social_media_influencer": BusinessEcosystem(
        key="social_media_influencer",
        name="Influencer Multi-Plataforma",
        display_name="Influencer Multi-Plataforma",
        description="Creador de contenido con presencia en múltiples redes sociales",
        business_type=BusinessType.SOCIAL_MEDIA,
        master_entities=["users", "content", "platforms"],
        core_tables={
            "creator_intelligence": [
                "dim_platform",
                "dim_channel", 
                "dim_content",
                "fact_content_performance_day",
                "fact_audience_day"
            ]
        },
        support_tables={
            "creator_intelligence": [
                "dim_hashtag",
                "br_content_hashtag",
                "dim_topic_taxonomy"
            ]
        },
        analytics_tables={
            "creator_intelligence": [
                "fact_traffic_source_day",
                "fact_retention_curve",
                "fact_comments_nlp"
            ]
        },
        relationships={
            "dim_platform -> dim_channel": "platform_id",
            "dim_content -> dim_platform": "platform_id", 
            "fact_content_performance_day -> dim_content": "content_id",
            "fact_audience_day -> dim_channel": "channel_id"
        },
        volume_ratios={
            "dim_platform": 0.05,      # 5% base platforms
            "dim_channel": 0.3,        # 30% channels
            "dim_content": 2.0,        # 200% content
            "fact_content_performance_day": 10.0,  # 1000% performance data
            "fact_audience_day": 3.0,  # 300% audience data
            "dim_hashtag": 0.5,        # 50% hashtags
            "br_content_hashtag": 5.0, # 500% content-hashtag relations
            "dim_topic_taxonomy": 0.2,  # 20% topic categories
            "fact_traffic_source_day": 8.0,  # 800% traffic data
            "fact_retention_curve": 6.0,     # 600% retention data
            "fact_comments_nlp": 15.0        # 1500% comment analysis
        }
    ),

    "social_media_corporate": BusinessEcosystem(
        key="social_media_corporate",
        name="Empresa Multi-Plataforma",
        display_name="Empresa Multi-Plataforma", 
        description="Empresa con presencia corporativa en redes sociales",
        business_type=BusinessType.SOCIAL_MEDIA,
        master_entities=["channels", "content", "campaigns"],
        core_tables={
            "creator_intelligence": [
                "dim_platform",
                "dim_channel",
                "dim_content", 
                "fact_content_performance_day",
                "fact_competitive_benchmark"
            ]
        },
        support_tables={
            "creator_intelligence": [
                "dim_project",
                "dim_experiment",
                "dim_schedule_slot"
            ]
        },
        analytics_tables={
            "creator_intelligence": [
                "fact_project_timeline",
                "fact_deliverables",
                "fact_posting_schedule_adherence"
            ]
        },
        relationships={
            "dim_channel -> dim_platform": "platform_id",
            "dim_content -> dim_channel": "channel_id",
            "fact_content_performance_day -> dim_content": "content_id",
            "dim_project -> dim_channel": "channel_id",
            "fact_competitive_benchmark -> dim_platform": "platform_id"
        },
        volume_ratios={
            "dim_platform": 0.08,      # 8% platforms
            "dim_channel": 0.2,        # 20% channels  
            "dim_content": 3.0,        # 300% content
            "fact_content_performance_day": 12.0,  # 1200% performance
            "fact_competitive_benchmark": 4.0,     # 400% competitive data
            "dim_project": 0.1,        # 10% projects
            "dim_experiment": 0.3,     # 30% experiments
            "dim_schedule_slot": 0.5,  # 50% schedule slots
            "fact_project_timeline": 2.0,          # 200% timeline data
            "fact_deliverables": 1.5,              # 150% deliverables
            "fact_posting_schedule_adherence": 8.0  # 800% schedule tracking
        }
    ),

    # Ecosistemas E-commerce
    "ecommerce_marketplace": BusinessEcosystem(
        key="ecommerce_marketplace",
        name="Marketplace Multi-Vendedor", 
        display_name="Marketplace Multi-Vendedor",
        description="Plataforma de comercio electrónico con múltiples vendedores",
        business_type=BusinessType.ECOMMERCE,
        master_entities=["stores", "products", "customers"],
        core_tables={
            "retail": [
                "dim_store",
                "dim_product", 
                "dim_customer",
                "fact_orders",
                "fact_order_items"
            ]
        },
        support_tables={
            "retail": [
                "dim_address",
                "dim_session",
                "fact_payments"
            ]
        },
        analytics_tables={
            "retail": [
                "fact_returns_rma"
            ]
        },
        relationships={
            "fact_orders -> dim_customer": "customer_id",
            "fact_orders -> dim_store": "store_id",
            "fact_order_items -> fact_orders": "order_id",
            "fact_order_items -> dim_product": "product_id",
            "fact_payments -> fact_orders": "order_id"
        },
        volume_ratios={
            "dim_store": 0.05,         # 5% stores
            "dim_product": 4.0,        # 400% products
            "dim_customer": 0.8,       # 80% customers
            "fact_orders": 2.0,        # 200% orders
            "fact_order_items": 5.0,   # 500% order items
            "dim_address": 1.2,        # 120% addresses
            "dim_session": 8.0,        # 800% sessions
            "fact_payments": 2.2,      # 220% payments
            "fact_returns_rma": 0.3    # 30% returns
        }
    ),

    # Ecosistemas Banking
    "banking_digital": BusinessEcosystem(
        key="banking_digital",
        name="Banco Digital Completo",
        display_name="Banco Digital Completo",
        description="Ecosistema bancario digital con productos financieros",
        business_type=BusinessType.BANKING,
        master_entities=["customers", "accounts", "branches"],
        core_tables={
            "finance": [
                "dim_customer",
                "dim_account",
                "dim_branch",
                "fact_transactions",
                "fact_loans"
            ]
        },
        support_tables={
            "finance": [
                "fact_collections",
                "fact_risk_scores"
            ]
        },
        analytics_tables={
            "finance": [
                "fact_risk"
            ]
        },
        relationships={
            "dim_account -> dim_customer": "customer_id",
            "dim_account -> dim_branch": "branch_id", 
            "fact_transactions -> dim_account": "account_id",
            "fact_loans -> dim_customer": "customer_id",
            "fact_collections -> fact_loans": "loan_id",
            "fact_risk_scores -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_customer": 1.0,       # 100% customers
            "dim_account": 2.5,        # 250% accounts
            "dim_branch": 0.02,        # 2% branches
            "fact_transactions": 15.0, # 1500% transactions
            "fact_loans": 0.3,         # 30% loans
            "fact_collections": 0.05,  # 5% collections
            "fact_risk_scores": 1.2,   # 120% risk scores
            "fact_risk": 0.8           # 80% risk assessments
        }
    ),

    # Ecosistemas Healthcare  
    "healthcare_hospital": BusinessEcosystem(
        key="healthcare_hospital",
        name="Hospital Completo",
        display_name="Hospital Completo",
        description="Sistema hospitalario con pacientes, procedimientos y resultados",
        business_type=BusinessType.HEALTHCARE,
        master_entities=["patients", "providers", "procedures"],
        core_tables={
            "healthcare": [
                "dim_patient_pseudo",
                "dim_provider",
                "dim_procedure",
                "fact_encounters",
                "fact_labs"
            ]
        },
        support_tables={
            "healthcare": [
                "dim_diagnosis",
                "fact_medications",
                "fact_appointments"
            ]
        },
        analytics_tables={
            "healthcare": [
                "fact_outcomes",
                "fact_csat"
            ]
        },
        relationships={
            "fact_encounters -> dim_patient_pseudo": "patient_id",
            "fact_encounters -> dim_provider": "provider_id",
            "fact_encounters -> dim_procedure": "procedure_id",
            "fact_labs -> dim_patient_pseudo": "patient_id",
            "fact_medications -> dim_patient_pseudo": "patient_id",
            "fact_appointments -> dim_patient_pseudo": "patient_id"
        },
        volume_ratios={
            "dim_patient_pseudo": 1.0,  # 100% patients
            "dim_provider": 0.08,       # 8% providers
            "dim_procedure": 0.5,       # 50% procedures
            "fact_encounters": 3.0,     # 300% encounters
            "fact_labs": 2.5,           # 250% lab tests
            "dim_diagnosis": 0.3,       # 30% diagnoses
            "fact_medications": 4.0,    # 400% medications
            "fact_appointments": 5.0,   # 500% appointments
            "fact_outcomes": 2.0,       # 200% outcomes
            "fact_csat": 1.5            # 150% satisfaction
        }
    ),

    # Ecosistemas Education
    "education_university": BusinessEcosystem(
        key="education_university", 
        name="Universidad Completa",
        display_name="Universidad Completa",
        description="Sistema universitario con estudiantes, cursos y calificaciones",
        business_type=BusinessType.EDUCATION,
        master_entities=["students", "courses", "faculty"],
        core_tables={
            "education": [
                "dim_student",
                "dim_course", 
                "dim_faculty",
                "fact_enrollment",
                "fact_grades"
            ]
        },
        support_tables={
            "education": [
                "dim_semester",
                "fact_student_financials"
            ]
        },
        analytics_tables={
            "education": [
                "fact_academic_performance",
                "fact_retention_metrics"
            ]
        },
        relationships={
            "fact_enrollment -> dim_student": "student_id",
            "fact_enrollment -> dim_course": "course_id",
            "fact_grades -> dim_student": "student_id",
            "fact_grades -> dim_course": "course_id",
            "fact_student_financials -> dim_student": "student_id"
        },
        volume_ratios={
            "dim_student": 1.0,         # 100% students
            "dim_course": 0.15,         # 15% courses
            "dim_faculty": 0.05,        # 5% faculty
            "fact_enrollment": 3.0,     # 300% enrollments
            "fact_grades": 8.0,         # 800% grades
            "dim_semester": 0.02,       # 2% semesters
            "fact_student_financials": 2.0,      # 200% financial records
            "fact_academic_performance": 4.0,    # 400% performance data
            "fact_retention_metrics": 1.0        # 100% retention data
        }
    ),

    # Ecosistemas Retail
    "retail_supermarket": BusinessEcosystem(
        key="retail_supermarket",
        name="Cadena de Supermercados",
        display_name="Cadena de Supermercados", 
        description="Cadena de supermercados con múltiples tiendas y operaciones",
        business_type=BusinessType.RETAIL,
        master_entities=["stores", "products", "customers"],
        core_tables={
            "retail": [
                "dim_store",
                "dim_product",
                "dim_customer", 
                "fact_ticket_line",
                "dim_cashier"
            ]
        },
        support_tables={
            "retail": [
                "fact_cash_drawer",
                "fact_voids",
                "fact_returns"
            ]
        },
        analytics_tables={
            "retail": [
                "fact_returns_rma"
            ]
        },
        relationships={
            "fact_ticket_line -> dim_store": "store_id",
            "fact_ticket_line -> dim_product": "product_id",
            "fact_ticket_line -> dim_customer": "customer_id",
            "fact_ticket_line -> dim_cashier": "cashier_id",
            "fact_cash_drawer -> dim_cashier": "cashier_id",
            "fact_voids -> fact_ticket_line": "ticket_line_id"
        },
        volume_ratios={
            "dim_store": 0.03,          # 3% stores
            "dim_product": 8.0,         # 800% products
            "dim_customer": 2.0,        # 200% customers
            "fact_ticket_line": 20.0,   # 2000% ticket lines
            "dim_cashier": 0.1,         # 10% cashiers
            "fact_cash_drawer": 5.0,    # 500% cash operations
            "fact_voids": 0.5,          # 50% voids
            "fact_returns": 0.8,        # 80% returns
            "fact_returns_rma": 0.3     # 30% RMA returns
        }
    ),

    # Ecosistemas Microbusiness
    "microbusiness_bakery": BusinessEcosystem(
        key="microbusiness_bakery",
        name="Panadería Artesanal",
        display_name="Panadería Artesanal",
        description="Panadería con producción artesanal y ventas locales",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["products", "ingredients", "customers"],
        core_tables={
            "microbusiness": [
                "dim_bakery_product",
                "dim_bakery_ingredient",
                "fact_bakery_production",
                "fact_bakery_sales",
                "dim_customer"
            ]
        },
        support_tables={
            "microbusiness": [
                "dim_store",
                "fact_pos_line"
            ]
        },
        analytics_tables={
            "microbusiness": [
                "fact_inventory"
            ]
        },
        relationships={
            "fact_bakery_production -> dim_bakery_product": "product_id",
            "fact_bakery_production -> dim_bakery_ingredient": "ingredient_id",
            "fact_bakery_sales -> dim_bakery_product": "product_id",
            "fact_bakery_sales -> dim_customer": "customer_id",
            "fact_pos_line -> dim_bakery_product": "product_id"
        },
        volume_ratios={
            "dim_bakery_product": 0.2,      # 20% products
            "dim_bakery_ingredient": 0.15,  # 15% ingredients
            "fact_bakery_production": 2.0,  # 200% production batches
            "fact_bakery_sales": 8.0,       # 800% sales transactions
            "dim_customer": 1.5,            # 150% customers
            "dim_store": 0.01,              # 1% stores (single location)
            "fact_pos_line": 12.0,          # 1200% POS transactions
            "fact_inventory": 3.0           # 300% inventory movements
        }
    ),

    # =================== NUEVOS ECOSISTEMAS (95 adicionales) ===================
    
    # SOCIAL MEDIA & CREATOR (10 ecosistemas)
    "social_media_gaming_streamer": BusinessEcosystem(
        key="social_media_gaming_streamer",
        name="Streamer de Gaming",
        display_name="Streamer de Gaming",
        description="Creador de contenido especializado en gaming y streaming en vivo",
        business_type=BusinessType.SOCIAL_MEDIA,
        master_entities=["streams", "games", "viewers"],
        core_tables={
            "creator_intelligence": [
                "dim_platform", "dim_channel", "dim_content",
                "fact_content_performance_day", "fact_audience_day"
            ]
        },
        support_tables={
            "creator_intelligence": [
                "dim_hashtag", "br_content_hashtag"
            ]
        },
        analytics_tables={
            "creator_intelligence": [
                "fact_traffic_source_day", "fact_retention_curve"
            ]
        },
        relationships={
            "dim_content -> dim_channel": "channel_id",
            "fact_content_performance_day -> dim_content": "content_id"
        },
        volume_ratios={
            "dim_platform": 0.03, "dim_channel": 0.1, "dim_content": 3.0,
            "fact_content_performance_day": 15.0, "fact_audience_day": 8.0,
            "dim_hashtag": 0.8, "br_content_hashtag": 6.0,
            "fact_traffic_source_day": 12.0, "fact_retention_curve": 9.0
        }
    ),

    "social_media_beauty_influencer": BusinessEcosystem(
        key="social_media_beauty_influencer",
        name="Beauty Influencer",
        display_name="Influencer de Belleza",
        description="Creador de contenido especializado en belleza y cosmética",
        business_type=BusinessType.SOCIAL_MEDIA,
        master_entities=["products", "tutorials", "brands"],
        core_tables={
            "creator_intelligence": [
                "dim_platform", "dim_channel", "dim_content",
                "fact_content_performance_day"
            ]
        },
        support_tables={
            "creator_intelligence": [
                "dim_hashtag", "dim_topic_taxonomy"
            ]
        },
        analytics_tables={
            "creator_intelligence": [
                "fact_comments_nlp", "fact_competitive_benchmark"
            ]
        },
        relationships={
            "dim_content -> dim_platform": "platform_id",
            "fact_content_performance_day -> dim_content": "content_id"
        },
        volume_ratios={
            "dim_platform": 0.06, "dim_channel": 0.25, "dim_content": 4.0,
            "fact_content_performance_day": 18.0, "dim_hashtag": 1.2,
            "dim_topic_taxonomy": 0.3, "fact_comments_nlp": 20.0,
            "fact_competitive_benchmark": 5.0
        }
    ),

    "social_media_fitness_coach": BusinessEcosystem(
        key="social_media_fitness_coach",
        name="Coach de Fitness",
        display_name="Coach de Fitness",
        description="Entrenador personal con presencia digital y programas online",
        business_type=BusinessType.SOCIAL_MEDIA,
        master_entities=["workouts", "clients", "programs"],
        core_tables={
            "creator_intelligence": [
                "dim_channel", "dim_content", "fact_content_performance_day"
            ]
        },
        support_tables={
            "creator_intelligence": [
                "dim_project", "fact_deliverables"
            ]
        },
        analytics_tables={
            "creator_intelligence": [
                "fact_audience_day"
            ]
        },
        relationships={
            "dim_content -> dim_channel": "channel_id",
            "fact_content_performance_day -> dim_content": "content_id"
        },
        volume_ratios={
            "dim_channel": 0.15, "dim_content": 2.5, "fact_content_performance_day": 12.0,
            "dim_project": 0.2, "fact_deliverables": 1.8, "fact_audience_day": 6.0
        }
    ),

    "social_media_food_blogger": BusinessEcosystem(
        key="social_media_food_blogger",
        name="Food Blogger",
        display_name="Blogger Gastronómico",
        description="Creador de contenido culinario con recetas y reseñas",
        business_type=BusinessType.SOCIAL_MEDIA,
        master_entities=["recipes", "restaurants", "ingredients"],
        core_tables={
            "creator_intelligence": [
                "dim_platform", "dim_content", "fact_content_performance_day"
            ]
        },
        support_tables={
            "creator_intelligence": [
                "dim_hashtag", "br_content_hashtag"
            ]
        },
        analytics_tables={
            "creator_intelligence": [
                "fact_comments_nlp"
            ]
        },
        relationships={
            "dim_content -> dim_platform": "platform_id",
            "fact_content_performance_day -> dim_content": "content_id"
        },
        volume_ratios={
            "dim_platform": 0.04, "dim_content": 3.5, "fact_content_performance_day": 14.0,
            "dim_hashtag": 0.7, "br_content_hashtag": 8.0, "fact_comments_nlp": 16.0
        }
    ),

    "social_media_travel_blogger": BusinessEcosystem(
        key="social_media_travel_blogger",
        name="Travel Blogger",
        display_name="Blogger de Viajes",
        description="Creador de contenido de viajes con guías y experiencias",
        business_type=BusinessType.SOCIAL_MEDIA,
        master_entities=["destinations", "hotels", "experiences"],
        core_tables={
            "creator_intelligence": [
                "dim_channel", "dim_content", "fact_content_performance_day"
            ]
        },
        support_tables={
            "creator_intelligence": [
                "dim_hashtag", "dim_topic_taxonomy"
            ]
        },
        analytics_tables={
            "creator_intelligence": [
                "fact_traffic_source_day"
            ]
        },
        relationships={
            "dim_content -> dim_channel": "channel_id",
            "fact_content_performance_day -> dim_content": "content_id"
        },
        volume_ratios={
            "dim_channel": 0.12, "dim_content": 5.0, "fact_content_performance_day": 20.0,
            "dim_hashtag": 1.5, "dim_topic_taxonomy": 0.4, "fact_traffic_source_day": 15.0
        }
    ),

    "social_media_tech_reviewer": BusinessEcosystem(
        key="social_media_tech_reviewer",
        name="Tech Reviewer",
        display_name="Revisor de Tecnología",
        description="Creador de contenido especializado en reviews tecnológicos",
        business_type=BusinessType.SOCIAL_MEDIA,
        master_entities=["devices", "reviews", "brands"],
        core_tables={
            "creator_intelligence": [
                "dim_platform", "dim_content", "fact_content_performance_day"
            ]
        },
        support_tables={
            "creator_intelligence": [
                "dim_experiment", "fact_deliverables"
            ]
        },
        analytics_tables={
            "creator_intelligence": [
                "fact_competitive_benchmark"
            ]
        },
        relationships={
            "dim_content -> dim_platform": "platform_id",
            "fact_content_performance_day -> dim_content": "content_id"
        },
        volume_ratios={
            "dim_platform": 0.05, "dim_content": 2.8, "fact_content_performance_day": 13.0,
            "dim_experiment": 0.4, "fact_deliverables": 2.2, "fact_competitive_benchmark": 6.0
        }
    ),

    "social_media_fashion_stylist": BusinessEcosystem(
        key="social_media_fashion_stylist",
        name="Fashion Stylist",
        display_name="Estilista de Moda",
        description="Creador de contenido de moda y estilo personal",
        business_type=BusinessType.SOCIAL_MEDIA,
        master_entities=["outfits", "brands", "trends"],
        core_tables={
            "creator_intelligence": [
                "dim_channel", "dim_content", "fact_content_performance_day"
            ]
        },
        support_tables={
            "creator_intelligence": [
                "dim_hashtag", "br_content_hashtag"
            ]
        },
        analytics_tables={
            "creator_intelligence": [
                "fact_audience_day"
            ]
        },
        relationships={
            "dim_content -> dim_channel": "channel_id",
            "fact_content_performance_day -> dim_content": "content_id"
        },
        volume_ratios={
            "dim_channel": 0.18, "dim_content": 4.5, "fact_content_performance_day": 17.0,
            "dim_hashtag": 2.0, "br_content_hashtag": 10.0, "fact_audience_day": 7.0
        }
    ),

    "social_media_diy_creator": BusinessEcosystem(
        key="social_media_diy_creator",
        name="DIY Creator",
        display_name="Creador DIY",
        description="Creador de contenido de manualidades y proyectos DIY",
        business_type=BusinessType.SOCIAL_MEDIA,
        master_entities=["projects", "materials", "tutorials"],
        core_tables={
            "creator_intelligence": [
                "dim_content", "fact_content_performance_day"
            ]
        },
        support_tables={
            "creator_intelligence": [
                "dim_project", "fact_project_timeline"
            ]
        },
        analytics_tables={
            "creator_intelligence": [
                "fact_comments_nlp"
            ]
        },
        relationships={
            "fact_content_performance_day -> dim_content": "content_id",
            "fact_project_timeline -> dim_project": "project_id"
        },
        volume_ratios={
            "dim_content": 3.2, "fact_content_performance_day": 11.0,
            "dim_project": 0.25, "fact_project_timeline": 2.5, "fact_comments_nlp": 14.0
        }
    ),

    "social_media_music_producer": BusinessEcosystem(
        key="social_media_music_producer",
        name="Music Producer",
        display_name="Productor Musical",
        description="Productor musical con contenido educativo y promocional",
        business_type=BusinessType.SOCIAL_MEDIA,
        master_entities=["tracks", "artists", "collaborations"],
        core_tables={
            "creator_intelligence": [
                "dim_platform", "dim_channel", "dim_content"
            ]
        },
        support_tables={
            "creator_intelligence": [
                "dim_hashtag", "dim_topic_taxonomy"
            ]
        },
        analytics_tables={
            "creator_intelligence": [
                "fact_content_performance_day"
            ]
        },
        relationships={
            "dim_channel -> dim_platform": "platform_id",
            "dim_content -> dim_channel": "channel_id"
        },
        volume_ratios={
            "dim_platform": 0.07, "dim_channel": 0.22, "dim_content": 2.0,
            "dim_hashtag": 0.9, "dim_topic_taxonomy": 0.15, "fact_content_performance_day": 9.0
        }
    ),

    "social_media_education_tutor": BusinessEcosystem(
        key="social_media_education_tutor",
        name="Education Tutor",
        display_name="Tutor Educativo",
        description="Educator que crea contenido académico y tutoriales educativos",
        business_type=BusinessType.SOCIAL_MEDIA,
        master_entities=["courses", "students", "subjects"],
        core_tables={
            "creator_intelligence": [
                "dim_content", "fact_content_performance_day", "fact_audience_day"
            ]
        },
        support_tables={
            "creator_intelligence": [
                "dim_project", "fact_deliverables"
            ]
        },
        analytics_tables={
            "creator_intelligence": [
                "fact_retention_curve"
            ]
        },
        relationships={
            "fact_content_performance_day -> dim_content": "content_id",
            "fact_deliverables -> dim_project": "project_id"
        },
        volume_ratios={
            "dim_content": 6.0, "fact_content_performance_day": 25.0, "fact_audience_day": 10.0,
            "dim_project": 0.3, "fact_deliverables": 3.0, "fact_retention_curve": 8.0
        }
    ),

    # E-COMMERCE & RETAIL (15 ecosistemas)
    "ecommerce_fashion_boutique": BusinessEcosystem(
        key="ecommerce_fashion_boutique",
        name="Boutique de Moda Online",
        display_name="Boutique de Moda Online",
        description="Tienda online especializada en moda y accesorios",
        business_type=BusinessType.ECOMMERCE,
        master_entities=["products", "customers", "orders"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_orders", "fact_order_items"]
        },
        support_tables={
            "retail": ["dim_address", "fact_payments"]
        },
        analytics_tables={
            "retail": ["fact_returns_rma"]
        },
        relationships={
            "fact_orders -> dim_customer": "customer_id",
            "fact_order_items -> fact_orders": "order_id"
        },
        volume_ratios={
            "dim_product": 3.0, "dim_customer": 0.6, "fact_orders": 1.8,
            "fact_order_items": 4.5, "dim_address": 0.8, "fact_payments": 2.0, "fact_returns_rma": 0.2
        }
    ),

    "ecommerce_electronics_store": BusinessEcosystem(
        key="ecommerce_electronics_store",
        name="Tienda de Electrónicos",
        display_name="Tienda de Electrónicos",
        description="E-commerce especializado en productos electrónicos y tecnología",
        business_type=BusinessType.ECOMMERCE,
        master_entities=["devices", "brands", "warranties"],
        core_tables={
            "retail": ["dim_store", "dim_product", "dim_customer", "fact_orders"]
        },
        support_tables={
            "retail": ["fact_payments", "dim_session"]
        },
        analytics_tables={
            "retail": ["fact_returns_rma"]
        },
        relationships={
            "fact_orders -> dim_customer": "customer_id",
            "fact_orders -> dim_store": "store_id"
        },
        volume_ratios={
            "dim_store": 0.02, "dim_product": 5.0, "dim_customer": 1.2,
            "fact_orders": 2.5, "fact_payments": 2.7, "dim_session": 12.0, "fact_returns_rma": 0.4
        }
    ),

    "ecommerce_home_decor": BusinessEcosystem(
        key="ecommerce_home_decor",
        name="Decoración del Hogar",
        display_name="Decoración del Hogar",
        description="Marketplace de productos para decoración y muebles",
        business_type=BusinessType.ECOMMERCE,
        master_entities=["furniture", "decor", "rooms"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_order_items"]
        },
        support_tables={
            "retail": ["fact_orders", "dim_address"]
        },
        analytics_tables={
            "retail": ["fact_returns_rma"]
        },
        relationships={
            "fact_order_items -> fact_orders": "order_id",
            "fact_orders -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 4.5, "dim_customer": 0.9, "fact_order_items": 6.0,
            "fact_orders": 1.5, "dim_address": 1.1, "fact_returns_rma": 0.3
        }
    ),

    "ecommerce_sports_equipment": BusinessEcosystem(
        key="ecommerce_sports_equipment",
        name="Equipamiento Deportivo",
        display_name="Equipamiento Deportivo",
        description="E-commerce de artículos y equipamiento deportivo",
        business_type=BusinessType.ECOMMERCE,
        master_entities=["equipment", "sports", "athletes"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_orders", "fact_payments"]
        },
        support_tables={
            "retail": ["dim_session", "fact_order_items"]
        },
        analytics_tables={
            "retail": ["fact_returns_rma"]
        },
        relationships={
            "fact_orders -> dim_customer": "customer_id",
            "fact_payments -> fact_orders": "order_id"
        },
        volume_ratios={
            "dim_product": 3.8, "dim_customer": 1.1, "fact_orders": 2.2,
            "fact_payments": 2.4, "dim_session": 8.0, "fact_order_items": 5.5, "fact_returns_rma": 0.25
        }
    ),

    "ecommerce_books_media": BusinessEcosystem(
        key="ecommerce_books_media",
        name="Librería Online",
        display_name="Librería Online",
        description="E-commerce de libros, ebooks y contenido multimedia",
        business_type=BusinessType.ECOMMERCE,
        master_entities=["books", "authors", "genres"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_orders"]
        },
        support_tables={
            "retail": ["fact_order_items", "fact_payments"]
        },
        analytics_tables={
            "retail": ["fact_returns_rma"]
        },
        relationships={
            "fact_orders -> dim_customer": "customer_id",
            "fact_order_items -> dim_product": "product_id"
        },
        volume_ratios={
            "dim_product": 8.0, "dim_customer": 1.5, "fact_orders": 3.0,
            "fact_order_items": 4.0, "fact_payments": 3.2, "fact_returns_rma": 0.1
        }
    ),

    # HEALTHCARE & WELLNESS (12 ecosistemas)
    "healthcare_dental_clinic": BusinessEcosystem(
        key="healthcare_dental_clinic",
        name="Clínica Dental",
        display_name="Clínica Dental",
        description="Clínica dental con servicios especializados y pacientes regulares",
        business_type=BusinessType.HEALTHCARE,
        master_entities=["patients", "dentists", "treatments"],
        core_tables={
            "healthcare": ["dim_patient_pseudo", "dim_provider", "fact_appointments"]
        },
        support_tables={
            "healthcare": ["dim_procedure", "fact_medications"]
        },
        analytics_tables={
            "healthcare": ["fact_csat", "fact_outcomes"]
        },
        relationships={
            "fact_appointments -> dim_patient_pseudo": "patient_id",
            "fact_appointments -> dim_provider": "provider_id"
        },
        volume_ratios={
            "dim_patient_pseudo": 1.0, "dim_provider": 0.05, "fact_appointments": 4.0,
            "dim_procedure": 0.2, "fact_medications": 2.0, "fact_csat": 1.2, "fact_outcomes": 1.8
        }
    ),

    "healthcare_veterinary_clinic": BusinessEcosystem(
        key="healthcare_veterinary_clinic",
        name="Clínica Veterinaria",
        display_name="Clínica Veterinaria",
        description="Clínica veterinaria con atención a mascotas y animales",
        business_type=BusinessType.HEALTHCARE,
        master_entities=["pets", "owners", "veterinarians"],
        core_tables={
            "healthcare": ["dim_patient_pseudo", "dim_provider", "fact_encounters"]
        },
        support_tables={
            "healthcare": ["fact_appointments", "fact_medications"]
        },
        analytics_tables={
            "healthcare": ["fact_outcomes"]
        },
        relationships={
            "fact_encounters -> dim_patient_pseudo": "patient_id",
            "fact_encounters -> dim_provider": "provider_id"
        },
        volume_ratios={
            "dim_patient_pseudo": 1.2, "dim_provider": 0.06, "fact_encounters": 3.5,
            "fact_appointments": 4.5, "fact_medications": 3.0, "fact_outcomes": 2.2
        }
    ),

    "healthcare_mental_health": BusinessEcosystem(
        key="healthcare_mental_health",
        name="Centro de Salud Mental",
        display_name="Centro de Salud Mental",
        description="Centro especializado en salud mental y terapias psicológicas",
        business_type=BusinessType.HEALTHCARE,
        master_entities=["patients", "therapists", "sessions"],
        core_tables={
            "healthcare": ["dim_patient_pseudo", "dim_provider", "fact_appointments"]
        },
        support_tables={
            "healthcare": ["dim_diagnosis", "fact_medications"]
        },
        analytics_tables={
            "healthcare": ["fact_outcomes", "fact_csat"]
        },
        relationships={
            "fact_appointments -> dim_patient_pseudo": "patient_id",
            "fact_appointments -> dim_provider": "provider_id"
        },
        volume_ratios={
            "dim_patient_pseudo": 0.8, "dim_provider": 0.04, "fact_appointments": 6.0,
            "dim_diagnosis": 0.25, "fact_medications": 2.5, "fact_outcomes": 3.0, "fact_csat": 1.8
        }
    ),

    # EDUCATION & TRAINING (12 ecosistemas)
    "education_language_school": BusinessEcosystem(
        key="education_language_school",
        name="Escuela de Idiomas",
        display_name="Escuela de Idiomas",
        description="Instituto de enseñanza de idiomas con cursos presenciales y online",
        business_type=BusinessType.EDUCATION,
        master_entities=["students", "teachers", "languages"],
        core_tables={
            "education": ["dim_student", "dim_faculty", "fact_enrollment"]
        },
        support_tables={
            "education": ["dim_course", "fact_grades"]
        },
        analytics_tables={
            "education": ["fact_academic_performance"]
        },
        relationships={
            "fact_enrollment -> dim_student": "student_id",
            "fact_grades -> dim_student": "student_id"
        },
        volume_ratios={
            "dim_student": 1.0, "dim_faculty": 0.08, "fact_enrollment": 2.5,
            "dim_course": 0.3, "fact_grades": 6.0, "fact_academic_performance": 4.0
        }
    ),

    "education_cooking_school": BusinessEcosystem(
        key="education_cooking_school",
        name="Escuela de Cocina",
        display_name="Escuela de Cocina",
        description="Instituto culinario con cursos de gastronomía y repostería",
        business_type=BusinessType.EDUCATION,
        master_entities=["students", "chefs", "recipes"],
        core_tables={
            "education": ["dim_student", "dim_faculty", "dim_course"]
        },
        support_tables={
            "education": ["fact_enrollment", "fact_grades"]
        },
        analytics_tables={
            "education": ["fact_academic_performance"]
        },
        relationships={
            "fact_enrollment -> dim_student": "student_id",
            "fact_enrollment -> dim_course": "course_id"
        },
        volume_ratios={
            "dim_student": 0.6, "dim_faculty": 0.04, "dim_course": 0.2,
            "fact_enrollment": 1.8, "fact_grades": 4.5, "fact_academic_performance": 2.8
        }
    ),

    # BANKING & FINTECH (10 ecosistemas)
    "fintech_digital_wallet": BusinessEcosystem(
        key="fintech_digital_wallet",
        name="Billetera Digital",
        display_name="Billetera Digital",
        description="Aplicación de pagos móviles y billetera digital",
        business_type=BusinessType.BANKING,
        master_entities=["users", "wallets", "transactions"],
        core_tables={
            "finance": ["dim_customer", "dim_account", "fact_transactions"]
        },
        support_tables={
            "finance": ["fact_risk_scores"]
        },
        analytics_tables={
            "finance": ["fact_risk"]
        },
        relationships={
            "dim_account -> dim_customer": "customer_id",
            "fact_transactions -> dim_account": "account_id"
        },
        volume_ratios={
            "dim_customer": 1.5, "dim_account": 2.0, "fact_transactions": 25.0,
            "fact_risk_scores": 1.8, "fact_risk": 1.2
        }
    ),

    "fintech_lending_platform": BusinessEcosystem(
        key="fintech_lending_platform",
        name="Plataforma de Préstamos",
        display_name="Plataforma de Préstamos",
        description="Plataforma digital de préstamos peer-to-peer",
        business_type=BusinessType.BANKING,
        master_entities=["borrowers", "lenders", "loans"],
        core_tables={
            "finance": ["dim_customer", "fact_loans", "fact_transactions"]
        },
        support_tables={
            "finance": ["fact_collections", "fact_risk_scores"]
        },
        analytics_tables={
            "finance": ["fact_risk"]
        },
        relationships={
            "fact_loans -> dim_customer": "customer_id",
            "fact_collections -> fact_loans": "loan_id"
        },
        volume_ratios={
            "dim_customer": 1.0, "fact_loans": 0.4, "fact_transactions": 8.0,
            "fact_collections": 0.08, "fact_risk_scores": 1.5, "fact_risk": 1.0
        }
    ),

    # MICROBUSINESS EXPANDED (20 ecosistemas)
    "microbusiness_coffee_shop": BusinessEcosystem(
        key="microbusiness_coffee_shop",
        name="Cafetería Local",
        display_name="Cafetería Local",
        description="Cafetería de barrio con productos artesanales",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["drinks", "pastries", "customers"],
        core_tables={
            "microbusiness": ["dim_product", "dim_customer", "fact_pos_line"]
        },
        support_tables={
            "microbusiness": ["dim_store", "fact_inventory"]
        },
        analytics_tables={
            "microbusiness": ["fact_cash_shift"]
        },
        relationships={
            "fact_pos_line -> dim_product": "product_id",
            "fact_pos_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 0.3, "dim_customer": 2.0, "fact_pos_line": 15.0,
            "dim_store": 0.005, "fact_inventory": 4.0, "fact_cash_shift": 2.0
        }
    ),

    "microbusiness_flower_shop": BusinessEcosystem(
        key="microbusiness_flower_shop",
        name="Floristería",
        display_name="Floristería",
        description="Floristería con arreglos personalizados y eventos",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["flowers", "arrangements", "events"],
        core_tables={
            "microbusiness": ["dim_product", "dim_customer", "fact_pos_line"]
        },
        support_tables={
            "microbusiness": ["fact_inventory", "fact_custom_orders"]
        },
        analytics_tables={
            "microbusiness": ["fact_cash_shift"]
        },
        relationships={
            "fact_pos_line -> dim_product": "product_id",
            "fact_custom_orders -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 0.8, "dim_customer": 1.2, "fact_pos_line": 8.0,
            "fact_inventory": 3.0, "fact_custom_orders": 1.5, "fact_cash_shift": 1.0
        }
    ),

    "microbusiness_auto_repair": BusinessEcosystem(
        key="microbusiness_auto_repair",
        name="Taller Mecánico",
        display_name="Taller Mecánico",
        description="Taller de reparación y mantenimiento automotriz",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["vehicles", "services", "parts"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_inventory"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_appointments -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.4, "dim_customer": 1.8, "fact_appointments": 3.0,
            "dim_staff": 0.03, "fact_inventory": 2.5, "fact_commissions": 1.5
        }
    ),

    "microbusiness_pet_grooming": BusinessEcosystem(
        key="microbusiness_pet_grooming",
        name="Peluquería Canina",
        display_name="Peluquería Canina",
        description="Salón de belleza y cuidado para mascotas",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["pets", "services", "owners"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_retail_sales"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_appointments -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.25, "dim_customer": 1.5, "fact_appointments": 4.0,
            "dim_staff": 0.02, "fact_retail_sales": 2.0, "fact_commissions": 1.2
        }
    ),

    "microbusiness_yoga_studio": BusinessEcosystem(
        key="microbusiness_yoga_studio",
        name="Estudio de Yoga",
        display_name="Estudio de Yoga",
        description="Estudio de yoga con clases grupales e individuales",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["classes", "instructors", "members"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_memberships"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_appointments"]
        },
        analytics_tables={
            "microbusiness": ["fact_retail_sales"]
        },
        relationships={
            "fact_memberships -> dim_customer": "customer_id",
            "fact_appointments -> dim_service": "service_id"
        },
        volume_ratios={
            "dim_service": 0.15, "dim_customer": 0.8, "fact_memberships": 1.0,
            "dim_staff": 0.04, "fact_appointments": 6.0, "fact_retail_sales": 1.5
        }
    ),

    # RETAIL SPECIALIZED (15 ecosistemas)
    "retail_pharmacy": BusinessEcosystem(
        key="retail_pharmacy",
        name="Farmacia",
        display_name="Farmacia",
        description="Farmacia con medicamentos y productos de salud",
        business_type=BusinessType.RETAIL,
        master_entities=["medicines", "customers", "prescriptions"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "retail": ["dim_cashier", "fact_cash_drawer"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_ticket_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 6.0, "dim_customer": 2.5, "fact_ticket_line": 20.0,
            "dim_cashier": 0.08, "fact_cash_drawer": 4.0, "fact_returns": 0.8
        }
    ),

    "retail_gas_station": BusinessEcosystem(
        key="retail_gas_station",
        name="Gasolinera",
        display_name="Gasolinera",
        description="Estación de servicio con combustibles y tienda de conveniencia",
        business_type=BusinessType.RETAIL,
        master_entities=["fuel", "convenience", "vehicles"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "retail": ["dim_store", "fact_cash_drawer"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_ticket_line -> dim_store": "store_id"
        },
        volume_ratios={
            "dim_product": 2.0, "dim_customer": 3.0, "fact_ticket_line": 25.0,
            "dim_store": 0.01, "fact_cash_drawer": 8.0, "fact_returns": 0.2
        }
    ),

    "retail_jewelry_store": BusinessEcosystem(
        key="retail_jewelry_store",
        name="Joyería",
        display_name="Joyería",
        description="Joyería con piezas exclusivas y servicios de reparación",
        business_type=BusinessType.RETAIL,
        master_entities=["jewelry", "precious_metals", "customers"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "retail": ["dim_cashier", "fact_returns"]
        },
        analytics_tables={
            "retail": ["fact_returns_rma"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_ticket_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 1.5, "dim_customer": 0.4, "fact_ticket_line": 2.0,
            "dim_cashier": 0.05, "fact_returns": 0.1, "fact_returns_rma": 0.05
        }
    ),

    # ENTERTAINMENT & MEDIA (10 ecosistemas)
    "entertainment_cinema": BusinessEcosystem(
        key="entertainment_cinema",
        name="Complejo Cinematográfico",
        display_name="Complejo Cinematográfico",
        description="Cine multiplex con múltiples salas y servicios",
        business_type=BusinessType.ENTERTAINMENT,
        master_entities=["movies", "screens", "customers"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "retail": ["dim_store", "fact_cash_drawer"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_ticket_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 0.8, "dim_customer": 1.8, "fact_ticket_line": 12.0,
            "dim_store": 0.05, "fact_cash_drawer": 3.0, "fact_returns": 0.3
        }
    ),

    "entertainment_arcade": BusinessEcosystem(
        key="entertainment_arcade",
        name="Sala de Juegos",
        display_name="Sala de Juegos",
        description="Centro de entretenimiento con videojuegos y diversiones",
        business_type=BusinessType.ENTERTAINMENT,
        master_entities=["games", "tokens", "players"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "retail": ["fact_cash_drawer"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_ticket_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 0.3, "dim_customer": 2.2, "fact_ticket_line": 18.0,
            "fact_cash_drawer": 6.0, "fact_returns": 0.1
        }
    ),

    # TECHNOLOGY & SERVICES (10 ecosistemas)
    "tech_computer_repair": BusinessEcosystem(
        key="tech_computer_repair",
        name="Reparación de Computadoras",
        display_name="Reparación de Computadoras",
        description="Servicio técnico especializado en reparación de equipos",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["devices", "repairs", "customers"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_inventory"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_appointments -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.6, "dim_customer": 1.5, "fact_appointments": 2.5,
            "dim_staff": 0.03, "fact_inventory": 3.0, "fact_commissions": 1.8
        }
    ),

    "tech_mobile_repair": BusinessEcosystem(
        key="tech_mobile_repair",
        name="Reparación de Celulares",
        display_name="Reparación de Celulares",
        description="Servicio técnico especializado en dispositivos móviles",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["phones", "parts", "warranties"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["fact_inventory", "fact_retail_sales"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_appointments -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.4, "dim_customer": 2.0, "fact_appointments": 8.0,
            "fact_inventory": 4.0, "fact_retail_sales": 3.0, "fact_commissions": 2.5
        }
    ),

    # FOOD & BEVERAGE (15 ecosistemas)
    "food_restaurant_fine": BusinessEcosystem(
        key="food_restaurant_fine",
        name="Restaurante Gourmet",
        display_name="Restaurante Gourmet",
        description="Restaurante de alta cocina con experiencia gastronómica premium",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["dishes", "wines", "reservations"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_inventory"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions", "fact_cash_shift"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_appointments -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 1.2, "dim_customer": 0.8, "fact_appointments": 4.0,
            "dim_staff": 0.08, "fact_inventory": 6.0, "fact_commissions": 2.0, "fact_cash_shift": 1.0
        }
    ),

    "food_pizza_delivery": BusinessEcosystem(
        key="food_pizza_delivery",
        name="Pizzería a Domicilio",
        display_name="Pizzería a Domicilio",
        description="Pizzería con servicio de entrega y pedidos en línea",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["pizzas", "delivery", "orders"],
        core_tables={
            "microbusiness": ["dim_product", "dim_customer", "fact_pos_line"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_inventory"]
        },
        analytics_tables={
            "microbusiness": ["fact_cash_shift"]
        },
        relationships={
            "fact_pos_line -> dim_product": "product_id",
            "fact_pos_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 0.8, "dim_customer": 2.5, "fact_pos_line": 12.0,
            "dim_staff": 0.06, "fact_inventory": 4.0, "fact_cash_shift": 2.0
        }
    ),

    "food_bakery": BusinessEcosystem(
        key="food_bakery",
        name="Panadería Artesanal",
        display_name="Panadería Artesanal",
        description="Panadería con productos frescos y repostería artesanal",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["bread", "pastries", "ingredients"],
        core_tables={
            "microbusiness": ["dim_product", "dim_customer", "fact_pos_line"]
        },
        support_tables={
            "microbusiness": ["fact_inventory", "fact_custom_orders"]
        },
        analytics_tables={
            "microbusiness": ["fact_cash_shift"]
        },
        relationships={
            "fact_pos_line -> dim_product": "product_id",
            "fact_pos_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 1.5, "dim_customer": 3.0, "fact_pos_line": 20.0,
            "fact_inventory": 8.0, "fact_custom_orders": 2.0, "fact_cash_shift": 2.5
        }
    ),

    "food_ice_cream": BusinessEcosystem(
        key="food_ice_cream",
        name="Heladería",
        display_name="Heladería",
        description="Heladería con sabores artesanales y productos únicos",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["flavors", "toppings", "customers"],
        core_tables={
            "microbusiness": ["dim_product", "dim_customer", "fact_pos_line"]
        },
        support_tables={
            "microbusiness": ["fact_inventory"]
        },
        analytics_tables={
            "microbusiness": ["fact_cash_shift"]
        },
        relationships={
            "fact_pos_line -> dim_product": "product_id",
            "fact_pos_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 0.6, "dim_customer": 2.8, "fact_pos_line": 15.0,
            "fact_inventory": 3.0, "fact_cash_shift": 1.8
        }
    ),

    # AUTOMOTIVE (8 ecosistemas)
    "auto_dealership": BusinessEcosystem(
        key="auto_dealership",
        name="Concesionario de Autos",
        display_name="Concesionario de Autos",
        description="Venta de vehículos nuevos y usados con financiamiento",
        business_type=BusinessType.RETAIL,
        master_entities=["vehicles", "sales", "financing"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "finance": ["dim_customer", "fact_loans"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_loans -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 2.0, "dim_customer": 0.8, "fact_ticket_line": 1.2,
            "fact_loans": 0.6, "fact_returns": 0.05
        }
    ),

    "auto_parts_store": BusinessEcosystem(
        key="auto_parts_store",
        name="Refaccionaria",
        display_name="Refaccionaria",
        description="Tienda especializada en refacciones y accesorios automotrices",
        business_type=BusinessType.RETAIL,
        master_entities=["parts", "brands", "vehicles"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "retail": ["dim_cashier", "fact_cash_drawer"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_ticket_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 8.0, "dim_customer": 1.5, "fact_ticket_line": 6.0,
            "dim_cashier": 0.04, "fact_cash_drawer": 2.0, "fact_returns": 0.3
        }
    ),

    # REAL ESTATE (5 ecosistemas)
    "realestate_agency": BusinessEcosystem(
        key="realestate_agency",
        name="Inmobiliaria",
        display_name="Inmobiliaria",
        description="Agencia inmobiliaria con ventas y rentas de propiedades",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["properties", "clients", "transactions"],
        core_tables={
            "microbusiness": ["dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_custom_orders"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_appointments -> dim_customer": "customer_id",
            "fact_commissions -> dim_staff": "staff_id"
        },
        volume_ratios={
            "dim_customer": 2.0, "fact_appointments": 3.0,
            "dim_staff": 0.05, "fact_custom_orders": 0.8, "fact_commissions": 1.2
        }
    ),

    # CONSULTING & PROFESSIONAL (8 ecosistemas)
    "consulting_legal": BusinessEcosystem(
        key="consulting_legal",
        name="Despacho Jurídico",
        display_name="Despacho Jurídico",
        description="Bufete de abogados con servicios legales especializados",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["cases", "clients", "documents"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["dim_staff"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_appointments -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.8, "dim_customer": 1.2, "fact_appointments": 2.0,
            "dim_staff": 0.08, "fact_commissions": 1.5
        }
    ),

    "consulting_accounting": BusinessEcosystem(
        key="consulting_accounting",
        name="Despacho Contable",
        display_name="Despacho Contable",
        description="Servicios contables y fiscales para empresas y personas",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["clients", "declarations", "documents"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["dim_staff"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_appointments -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.6, "dim_customer": 2.0, "fact_appointments": 4.0,
            "dim_staff": 0.06, "fact_commissions": 2.5
        }
    ),

    # AGRICULTURE & FARMING (5 ecosistemas)
    "agri_organic_farm": BusinessEcosystem(
        key="agri_organic_farm",
        name="Granja Orgánica",
        display_name="Granja Orgánica",
        description="Producción agrícola orgánica con venta directa",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["crops", "harvest", "customers"],
        core_tables={
            "microbusiness": ["dim_product", "dim_customer", "fact_pos_line"]
        },
        support_tables={
            "microbusiness": ["fact_inventory"]
        },
        analytics_tables={
            "microbusiness": ["fact_cash_shift"]
        },
        relationships={
            "fact_pos_line -> dim_product": "product_id",
            "fact_pos_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 2.0, "dim_customer": 1.0, "fact_pos_line": 5.0,
            "fact_inventory": 3.0, "fact_cash_shift": 1.0
        }
    ),

    # SPORTS & FITNESS (8 ecosistemas)
    "fitness_gym": BusinessEcosystem(
        key="fitness_gym",
        name="Gimnasio",
        display_name="Gimnasio",
        description="Centro de acondicionamiento físico con membresías",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["members", "equipment", "classes"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_memberships"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_retail_sales"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_memberships -> dim_customer": "customer_id",
            "fact_retail_sales -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.3, "dim_customer": 1.0, "fact_memberships": 1.2,
            "dim_staff": 0.05, "fact_retail_sales": 2.0, "fact_commissions": 0.8
        }
    ),

    "fitness_crossfit": BusinessEcosystem(
        key="fitness_crossfit",
        name="Box de CrossFit",
        display_name="Box de CrossFit",
        description="Centro especializado en entrenamiento funcional CrossFit",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["wods", "athletes", "competitions"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_memberships"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_appointments"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_memberships -> dim_customer": "customer_id",
            "fact_appointments -> dim_service": "service_id"
        },
        volume_ratios={
            "dim_service": 0.2, "dim_customer": 0.6, "fact_memberships": 0.8,
            "dim_staff": 0.03, "fact_appointments": 8.0, "fact_commissions": 1.0
        }
    ),

    # TRAVEL & HOSPITALITY (8 ecosistemas)
    "hotel_boutique": BusinessEcosystem(
        key="hotel_boutique",
        name="Hotel Boutique",
        display_name="Hotel Boutique",
        description="Hotel pequeño con servicios personalizados y experiencias únicas",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["rooms", "guests", "services"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_pos_line"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions", "fact_cash_shift"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_appointments -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.8, "dim_customer": 1.5, "fact_appointments": 3.0,
            "dim_staff": 0.12, "fact_pos_line": 8.0, "fact_commissions": 2.0, "fact_cash_shift": 1.0
        }
    ),

    "travel_agency": BusinessEcosystem(
        key="travel_agency",
        name="Agencia de Viajes",
        display_name="Agencia de Viajes",
        description="Agencia especializada en paquetes turísticos y viajes personalizados",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["packages", "destinations", "travelers"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_custom_orders"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_custom_orders -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 1.5, "dim_customer": 0.8, "fact_appointments": 2.0,
            "dim_staff": 0.04, "fact_custom_orders": 1.2, "fact_commissions": 1.8
        }
    ),

    # TRANSPORTATION (5 ecosistemas)
    "transport_taxi": BusinessEcosystem(
        key="transport_taxi",
        name="Servicio de Taxi",
        display_name="Servicio de Taxi",
        description="Servicio de transporte urbano con flota propia",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["vehicles", "drivers", "trips"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_pos_line"]
        },
        support_tables={
            "microbusiness": ["dim_staff"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_pos_line -> dim_service": "service_id",
            "fact_pos_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.1, "dim_customer": 5.0, "fact_pos_line": 30.0,
            "dim_staff": 0.08, "fact_commissions": 15.0
        }
    ),

    # PERSONAL CARE & BEAUTY (10 ecosistemas)
    "beauty_nail_salon": BusinessEcosystem(
        key="beauty_nail_salon",
        name="Salón de Uñas",
        display_name="Salón de Uñas",
        description="Salón especializado en manicure, pedicure y nail art",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["services", "clients", "products"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_retail_sales"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_appointments -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.3, "dim_customer": 1.8, "fact_appointments": 6.0,
            "dim_staff": 0.04, "fact_retail_sales": 3.0, "fact_commissions": 2.5
        }
    ),

    "beauty_barbershop": BusinessEcosystem(
        key="beauty_barbershop",
        name="Barbería",
        display_name="Barbería",
        description="Barbería tradicional con servicios de corte y arreglo masculino",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["cuts", "clients", "products"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_retail_sales"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_appointments -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.2, "dim_customer": 2.5, "fact_appointments": 10.0,
            "dim_staff": 0.05, "fact_retail_sales": 2.0, "fact_commissions": 3.0
        }
    ),

    "beauty_spa": BusinessEcosystem(
        key="beauty_spa",
        name="Spa y Relajación",
        display_name="Spa y Relajación",
        description="Centro de relajación con masajes y tratamientos corporales",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["treatments", "therapists", "packages"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_retail_sales"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_appointments -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.8, "dim_customer": 0.6, "fact_appointments": 2.0,
            "dim_staff": 0.06, "fact_retail_sales": 1.5, "fact_commissions": 1.8
        }
    ),

    # MANUFACTURING & CRAFTS (5 ecosistemas)
    "craft_jewelry_maker": BusinessEcosystem(
        key="craft_jewelry_maker",
        name="Joyería Artesanal",
        display_name="Joyería Artesanal",
        description="Taller de joyería con piezas únicas hechas a mano",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["pieces", "materials", "customers"],
        core_tables={
            "microbusiness": ["dim_product", "dim_customer", "fact_custom_orders"]
        },
        support_tables={
            "microbusiness": ["fact_inventory", "fact_pos_line"]
        },
        analytics_tables={
            "microbusiness": ["fact_cash_shift"]
        },
        relationships={
            "fact_custom_orders -> dim_product": "product_id",
            "fact_custom_orders -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 1.5, "dim_customer": 0.4, "fact_custom_orders": 0.8,
            "fact_inventory": 2.0, "fact_pos_line": 2.0, "fact_cash_shift": 0.5
        }
    ),

    "craft_furniture": BusinessEcosystem(
        key="craft_furniture",
        name="Carpintería",
        display_name="Carpintería",
        description="Taller de carpintería con muebles personalizados",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["furniture", "wood", "designs"],
        core_tables={
            "microbusiness": ["dim_product", "dim_customer", "fact_custom_orders"]
        },
        support_tables={
            "microbusiness": ["fact_inventory"]
        },
        analytics_tables={
            "microbusiness": ["fact_cash_shift"]
        },
        relationships={
            "fact_custom_orders -> dim_product": "product_id",
            "fact_custom_orders -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 2.0, "dim_customer": 0.3, "fact_custom_orders": 0.5,
            "fact_inventory": 5.0, "fact_cash_shift": 0.3
        }
    ),

    # PETS & VETERINARY (8 ecosistemas)
    "pets_veterinary": BusinessEcosystem(
        key="pets_veterinary",
        name="Clínica Veterinaria General",
        display_name="Clínica Veterinaria General",
        description="Clínica veterinaria con servicios generales para mascotas",
        business_type=BusinessType.HEALTHCARE,
        master_entities=["pets", "treatments", "owners"],
        core_tables={
            "healthcare": ["dim_patient", "dim_doctor", "fact_visits"]
        },
        support_tables={
            "healthcare": ["dim_medication", "fact_prescriptions"]
        },
        analytics_tables={
            "healthcare": ["fact_claims"]
        },
        relationships={
            "fact_visits -> dim_patient": "patient_id",
            "fact_prescriptions -> dim_medication": "medication_id"
        },
        volume_ratios={
            "dim_patient": 2.0, "dim_doctor": 0.06, "fact_visits": 4.0,
            "dim_medication": 1.5, "fact_prescriptions": 3.0, "fact_claims": 2.0
        }
    ),

    "pets_store": BusinessEcosystem(
        key="pets_store",
        name="Tienda de Mascotas",
        display_name="Tienda de Mascotas",
        description="Tienda especializada en productos y accesorios para mascotas",
        business_type=BusinessType.RETAIL,
        master_entities=["products", "pets", "owners"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "retail": ["dim_cashier", "fact_cash_drawer"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_ticket_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 4.0, "dim_customer": 1.8, "fact_ticket_line": 12.0,
            "dim_cashier": 0.04, "fact_cash_drawer": 3.0, "fact_returns": 0.6
        }
    ),

    # GAMING & ENTERTAINMENT (10 ecosistemas)
    "gaming_internet_cafe": BusinessEcosystem(
        key="gaming_internet_cafe",
        name="Ciber Café",
        display_name="Ciber Café",
        description="Centro de internet y gaming con equipos especializados",
        business_type=BusinessType.ENTERTAINMENT,
        master_entities=["computers", "games", "sessions"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "retail": ["fact_cash_drawer"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_ticket_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 0.2, "dim_customer": 3.0, "fact_ticket_line": 20.0,
            "fact_cash_drawer": 8.0, "fact_returns": 0.1
        }
    ),

    "gaming_board_games": BusinessEcosystem(
        key="gaming_board_games",
        name="Café de Juegos de Mesa",
        display_name="Café de Juegos de Mesa",
        description="Café temático con juegos de mesa y eventos sociales",
        business_type=BusinessType.ENTERTAINMENT,
        master_entities=["games", "events", "players"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "microbusiness": ["fact_appointments", "dim_service"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_appointments -> dim_service": "service_id"
        },
        volume_ratios={
            "dim_product": 0.8, "dim_customer": 1.5, "fact_ticket_line": 8.0,
            "fact_appointments": 4.0, "dim_service": 0.3, "fact_returns": 0.2
        }
    ),

    # FASHION & CLOTHING (8 ecosistemas)
    "fashion_boutique_luxury": BusinessEcosystem(
        key="fashion_boutique_luxury",
        name="Boutique de Lujo",
        display_name="Boutique de Lujo",
        description="Boutique exclusiva con marcas de alta gama",
        business_type=BusinessType.RETAIL,
        master_entities=["garments", "brands", "clients"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "retail": ["dim_cashier"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_ticket_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 2.5, "dim_customer": 0.4, "fact_ticket_line": 1.5,
            "dim_cashier": 0.03, "fact_returns": 0.2
        }
    ),

    "fashion_shoe_store": BusinessEcosystem(
        key="fashion_shoe_store",
        name="Zapatería",
        display_name="Zapatería",
        description="Tienda especializada en calzado para toda la familia",
        business_type=BusinessType.RETAIL,
        master_entities=["shoes", "brands", "sizes"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "retail": ["dim_cashier", "fact_cash_drawer"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_ticket_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 5.0, "dim_customer": 1.2, "fact_ticket_line": 4.0,
            "dim_cashier": 0.04, "fact_cash_drawer": 2.0, "fact_returns": 0.4
        }
    ),

    "fashion_tailoring": BusinessEcosystem(
        key="fashion_tailoring",
        name="Sastrería",
        display_name="Sastrería",
        description="Sastrería con confección a medida y ajustes",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["garments", "measurements", "clients"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["fact_custom_orders", "dim_staff"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_custom_orders -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.8, "dim_customer": 0.6, "fact_appointments": 1.5,
            "fact_custom_orders": 1.2, "dim_staff": 0.02, "fact_commissions": 1.0
        }
    ),

    # HOME & GARDEN (6 ecosistemas)
    "home_hardware_store": BusinessEcosystem(
        key="home_hardware_store",
        name="Ferretería",
        display_name="Ferretería",
        description="Ferretería con herramientas y materiales de construcción",
        business_type=BusinessType.RETAIL,
        master_entities=["tools", "materials", "contractors"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "retail": ["dim_cashier", "fact_cash_drawer"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_ticket_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 12.0, "dim_customer": 2.0, "fact_ticket_line": 8.0,
            "dim_cashier": 0.06, "fact_cash_drawer": 3.0, "fact_returns": 0.5
        }
    ),

    "home_garden_center": BusinessEcosystem(
        key="home_garden_center",
        name="Centro de Jardinería",
        display_name="Centro de Jardinería",
        description="Centro especializado en plantas y productos de jardinería",
        business_type=BusinessType.RETAIL,
        master_entities=["plants", "tools", "fertilizers"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "retail": ["fact_cash_drawer"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_ticket_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 8.0, "dim_customer": 1.0, "fact_ticket_line": 6.0,
            "fact_cash_drawer": 2.0, "fact_returns": 0.8
        }
    ),

    # ARTS & CULTURE (6 ecosistemas)
    "arts_music_store": BusinessEcosystem(
        key="arts_music_store",
        name="Tienda de Instrumentos",
        display_name="Tienda de Instrumentos",
        description="Tienda especializada en instrumentos musicales y accesorios",
        business_type=BusinessType.RETAIL,
        master_entities=["instruments", "accessories", "musicians"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "retail": ["dim_cashier"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_ticket_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 3.0, "dim_customer": 0.8, "fact_ticket_line": 2.0,
            "dim_cashier": 0.03, "fact_returns": 0.1
        }
    ),

    "arts_gallery": BusinessEcosystem(
        key="arts_gallery",
        name="Galería de Arte",
        display_name="Galería de Arte",
        description="Galería con obras de arte y eventos culturales",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["artworks", "artists", "collectors"],
        core_tables={
            "microbusiness": ["dim_product", "dim_customer", "fact_pos_line"]
        },
        support_tables={
            "microbusiness": ["fact_appointments", "dim_service"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_pos_line -> dim_product": "product_id",
            "fact_appointments -> dim_service": "service_id"
        },
        volume_ratios={
            "dim_product": 1.0, "dim_customer": 0.3, "fact_pos_line": 0.5,
            "fact_appointments": 1.0, "dim_service": 0.2, "fact_commissions": 0.4
        }
    ),

    # CLEANING & MAINTENANCE (4 ecosistemas)
    "cleaning_laundromat": BusinessEcosystem(
        key="cleaning_laundromat",
        name="Lavandería",
        display_name="Lavandería",
        description="Lavandería automática con servicios de limpieza",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["machines", "customers", "services"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_pos_line"]
        },
        support_tables={
            "microbusiness": ["fact_cash_shift"]
        },
        analytics_tables={
            "microbusiness": ["fact_inventory"]
        },
        relationships={
            "fact_pos_line -> dim_service": "service_id",
            "fact_pos_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.3, "dim_customer": 2.5, "fact_pos_line": 15.0,
            "fact_cash_shift": 3.0, "fact_inventory": 2.0
        }
    ),

    "cleaning_dry_cleaner": BusinessEcosystem(
        key="cleaning_dry_cleaner",
        name="Tintorería",
        display_name="Tintorería",
        description="Servicio de limpieza en seco y planchado profesional",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["garments", "treatments", "customers"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["fact_custom_orders"]
        },
        analytics_tables={
            "microbusiness": ["fact_cash_shift"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_custom_orders -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.6, "dim_customer": 1.8, "fact_appointments": 5.0,
            "fact_custom_orders": 4.0, "fact_cash_shift": 1.5
        }
    ),

    # SPECIALIZED RETAIL (10 ecosistemas)
    "retail_optical": BusinessEcosystem(
        key="retail_optical",
        name="Óptica",
        display_name="Óptica",
        description="Óptica con lentes, exámenes visuales y marcos especializados",
        business_type=BusinessType.RETAIL,
        master_entities=["glasses", "exams", "prescriptions"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "healthcare": ["dim_doctor", "fact_visits"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_visits -> dim_doctor": "doctor_id"
        },
        volume_ratios={
            "dim_product": 2.0, "dim_customer": 0.8, "fact_ticket_line": 2.5,
            "dim_doctor": 0.02, "fact_visits": 1.2, "fact_returns": 0.1
        }
    ),

    "retail_toy_store": BusinessEcosystem(
        key="retail_toy_store",
        name="Juguetería",
        display_name="Juguetería",
        description="Tienda especializada en juguetes y productos para niños",
        business_type=BusinessType.RETAIL,
        master_entities=["toys", "games", "children"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "retail": ["dim_cashier", "fact_cash_drawer"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_ticket_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 6.0, "dim_customer": 1.5, "fact_ticket_line": 8.0,
            "dim_cashier": 0.04, "fact_cash_drawer": 3.0, "fact_returns": 0.8
        }
    ),

    "retail_stationery": BusinessEcosystem(
        key="retail_stationery",
        name="Papelería",
        display_name="Papelería",
        description="Papelería con útiles escolares y materiales de oficina",
        business_type=BusinessType.RETAIL,
        master_entities=["supplies", "students", "offices"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "retail": ["dim_cashier", "fact_cash_drawer"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_ticket_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 4.0, "dim_customer": 2.0, "fact_ticket_line": 12.0,
            "dim_cashier": 0.03, "fact_cash_drawer": 4.0, "fact_returns": 0.4
        }
    ),

    "retail_bike_shop": BusinessEcosystem(
        key="retail_bike_shop",
        name="Tienda de Bicicletas",
        display_name="Tienda de Bicicletas",
        description="Tienda especializada en bicicletas y accesorios ciclísticos",
        business_type=BusinessType.RETAIL,
        master_entities=["bikes", "accessories", "cyclists"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "microbusiness": ["dim_service", "fact_appointments"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_appointments -> dim_service": "service_id"
        },
        volume_ratios={
            "dim_product": 3.0, "dim_customer": 0.6, "fact_ticket_line": 2.0,
            "dim_service": 0.3, "fact_appointments": 1.5, "fact_returns": 0.1
        }
    ),

    # SPECIALIZED SERVICES (8 ecosistemas)
    "service_locksmith": BusinessEcosystem(
        key="service_locksmith",
        name="Cerrajería",
        display_name="Cerrajería",
        description="Servicios de cerrajería y seguridad residencial y comercial",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["locks", "keys", "security"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_inventory"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_appointments -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.5, "dim_customer": 2.0, "fact_appointments": 3.0,
            "dim_staff": 0.03, "fact_inventory": 2.0, "fact_commissions": 1.8
        }
    ),

    "service_plumbing": BusinessEcosystem(
        key="service_plumbing",
        name="Plomería",
        display_name="Plomería",
        description="Servicios de plomería y reparaciones hidráulicas",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["pipes", "repairs", "installations"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_inventory"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_appointments -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.8, "dim_customer": 1.5, "fact_appointments": 2.5,
            "dim_staff": 0.04, "fact_inventory": 3.0, "fact_commissions": 2.0
        }
    ),

    "service_electrical": BusinessEcosystem(
        key="service_electrical",
        name="Electricidad",
        display_name="Electricidad",
        description="Servicios eléctricos e instalaciones para hogares y empresas",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["wiring", "installations", "repairs"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_inventory"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_appointments -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.6, "dim_customer": 1.2, "fact_appointments": 2.0,
            "dim_staff": 0.03, "fact_inventory": 4.0, "fact_commissions": 1.8
        }
    ),

    # WELLNESS & ALTERNATIVE MEDICINE (5 ecosistemas)
    "wellness_massage": BusinessEcosystem(
        key="wellness_massage",
        name="Centro de Masajes",
        display_name="Centro de Masajes",
        description="Centro especializado en masajes terapéuticos y relajantes",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["therapies", "clients", "therapists"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_retail_sales"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_appointments -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.4, "dim_customer": 0.8, "fact_appointments": 3.0,
            "dim_staff": 0.05, "fact_retail_sales": 1.0, "fact_commissions": 2.0
        }
    ),

    "wellness_acupuncture": BusinessEcosystem(
        key="wellness_acupuncture",
        name="Clínica de Acupuntura",
        display_name="Clínica de Acupuntura",
        description="Clínica de medicina alternativa y acupuntura",
        business_type=BusinessType.HEALTHCARE,
        master_entities=["treatments", "patients", "sessions"],
        core_tables={
            "healthcare": ["dim_patient", "dim_doctor", "fact_visits"]
        },
        support_tables={
            "healthcare": ["fact_prescriptions"]
        },
        analytics_tables={
            "healthcare": ["fact_claims"]
        },
        relationships={
            "fact_visits -> dim_patient": "patient_id",
            "fact_visits -> dim_doctor": "doctor_id"
        },
        volume_ratios={
            "dim_patient": 0.8, "dim_doctor": 0.02, "fact_visits": 2.5,
            "fact_prescriptions": 1.0, "fact_claims": 1.5
        }
    ),

    # FINAL SPECIALTY BUSINESSES (2 ecosistemas)
    "specialty_printing": BusinessEcosystem(
        key="specialty_printing",
        name="Imprenta Digital",
        display_name="Imprenta Digital",
        description="Servicios de impresión digital y diseño gráfico",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["prints", "designs", "clients"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_custom_orders"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_inventory"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_custom_orders -> dim_service": "service_id",
            "fact_custom_orders -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 1.2, "dim_customer": 1.5, "fact_custom_orders": 4.0,
            "dim_staff": 0.03, "fact_inventory": 5.0, "fact_commissions": 2.5
        }
    ),

    "specialty_wedding_planning": BusinessEcosystem(
        key="specialty_wedding_planning",
        name="Organización de Bodas",
        display_name="Organización de Bodas",
        description="Planificación y coordinación de eventos especiales y bodas",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["events", "couples", "vendors"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_custom_orders"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_custom_orders -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.8, "dim_customer": 0.2, "fact_appointments": 1.0,
            "dim_staff": 0.02, "fact_custom_orders": 0.5, "fact_commissions": 1.2
        }
    ),

    # FINAL ECOSYSTEMS TO REACH 100 (14 ecosistemas)
    "food_food_truck": BusinessEcosystem(
        key="food_food_truck",
        name="Food Truck",
        display_name="Food Truck",
        description="Camión de comida móvil con especialidades gastronómicas",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["menu", "locations", "events"],
        core_tables={
            "microbusiness": ["dim_product", "dim_customer", "fact_pos_line"]
        },
        support_tables={
            "microbusiness": ["fact_inventory"]
        },
        analytics_tables={
            "microbusiness": ["fact_cash_shift"]
        },
        relationships={
            "fact_pos_line -> dim_product": "product_id",
            "fact_pos_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 0.5, "dim_customer": 4.0, "fact_pos_line": 25.0,
            "fact_inventory": 2.0, "fact_cash_shift": 3.0
        }
    ),

    "retail_convenience_store": BusinessEcosystem(
        key="retail_convenience_store",
        name="Tienda de Conveniencia",
        display_name="Tienda de Conveniencia",
        description="Tienda de conveniencia 24 horas con productos esenciales",
        business_type=BusinessType.RETAIL,
        master_entities=["convenience", "24hours", "essentials"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "retail": ["dim_cashier", "fact_cash_drawer"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_ticket_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 3.0, "dim_customer": 6.0, "fact_ticket_line": 35.0,
            "dim_cashier": 0.08, "fact_cash_drawer": 8.0, "fact_returns": 0.5
        }
    ),

    "service_photography": BusinessEcosystem(
        key="service_photography",
        name="Estudio Fotográfico",
        display_name="Estudio Fotográfico",
        description="Estudio de fotografía profesional para eventos y retratos",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["sessions", "events", "portraits"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_custom_orders"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_custom_orders -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.6, "dim_customer": 0.5, "fact_appointments": 1.2,
            "dim_staff": 0.02, "fact_custom_orders": 1.0, "fact_commissions": 1.0
        }
    ),

    "transport_delivery": BusinessEcosystem(
        key="transport_delivery",
        name="Servicio de Delivery",
        display_name="Servicio de Delivery",
        description="Servicio de entrega a domicilio multi-restaurante",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["orders", "drivers", "restaurants"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_pos_line"]
        },
        support_tables={
            "microbusiness": ["dim_staff"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_pos_line -> dim_service": "service_id",
            "fact_pos_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.1, "dim_customer": 8.0, "fact_pos_line": 50.0,
            "dim_staff": 0.1, "fact_commissions": 25.0
        }
    ),

    "retail_wine_store": BusinessEcosystem(
        key="retail_wine_store",
        name="Vinoteca",
        display_name="Vinoteca",
        description="Tienda especializada en vinos y licores premium",
        business_type=BusinessType.RETAIL,
        master_entities=["wines", "spirits", "collectors"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "retail": ["dim_cashier"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_ticket_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 4.0, "dim_customer": 0.6, "fact_ticket_line": 2.5,
            "dim_cashier": 0.02, "fact_returns": 0.1
        }
    ),

    "service_tutoring": BusinessEcosystem(
        key="service_tutoring",
        name="Centro de Tutorías",
        display_name="Centro de Tutorías",
        description="Centro de tutorías académicas personalizadas",
        business_type=BusinessType.EDUCATION,
        master_entities=["subjects", "students", "tutors"],
        core_tables={
            "education": ["dim_course", "dim_student", "fact_enrollments"]
        },
        support_tables={
            "education": ["dim_instructor", "fact_grades"]
        },
        analytics_tables={
            "education": ["fact_course_evaluations"]
        },
        relationships={
            "fact_enrollments -> dim_course": "course_id",
            "fact_enrollments -> dim_student": "student_id"
        },
        volume_ratios={
            "dim_course": 0.8, "dim_student": 2.0, "fact_enrollments": 3.0,
            "dim_instructor": 0.08, "fact_grades": 12.0, "fact_course_evaluations": 2.5
        }
    ),

    "health_dentist_cosmetic": BusinessEcosystem(
        key="health_dentist_cosmetic",
        name="Dentista Cosmético",
        display_name="Dentista Cosmético",
        description="Clínica dental especializada en estética dental",
        business_type=BusinessType.HEALTHCARE,
        master_entities=["treatments", "aesthetics", "patients"],
        core_tables={
            "healthcare": ["dim_patient", "dim_doctor", "fact_visits"]
        },
        support_tables={
            "healthcare": ["dim_medication", "fact_prescriptions"]
        },
        analytics_tables={
            "healthcare": ["fact_claims"]
        },
        relationships={
            "fact_visits -> dim_patient": "patient_id",
            "fact_visits -> dim_doctor": "doctor_id"
        },
        volume_ratios={
            "dim_patient": 1.0, "dim_doctor": 0.02, "fact_visits": 2.5,
            "dim_medication": 0.5, "fact_prescriptions": 1.0, "fact_claims": 1.8
        }
    ),

    "entertainment_bowling": BusinessEcosystem(
        key="entertainment_bowling",
        name="Boliche",
        display_name="Boliche",
        description="Centro de boliche con pistas y servicios de entretenimiento",
        business_type=BusinessType.ENTERTAINMENT,
        master_entities=["lanes", "shoes", "leagues"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "retail": ["fact_cash_drawer"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_ticket_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 0.4, "dim_customer": 2.0, "fact_ticket_line": 10.0,
            "fact_cash_drawer": 4.0, "fact_returns": 0.2
        }
    ),

    "retail_electronics_repair": BusinessEcosystem(
        key="retail_electronics_repair",
        name="Reparación de Electrónicos",
        display_name="Reparación de Electrónicos",
        description="Taller de reparación de dispositivos electrónicos",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["devices", "repairs", "warranties"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["fact_inventory", "dim_staff"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_appointments -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.5, "dim_customer": 2.5, "fact_appointments": 4.0,
            "fact_inventory": 3.0, "dim_staff": 0.03, "fact_commissions": 2.0
        }
    ),

    "agri_farmers_market": BusinessEcosystem(
        key="agri_farmers_market",
        name="Mercado de Agricultores",
        display_name="Mercado de Agricultores",
        description="Puesto en mercado de agricultores con productos frescos",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["produce", "farmers", "markets"],
        core_tables={
            "microbusiness": ["dim_product", "dim_customer", "fact_pos_line"]
        },
        support_tables={
            "microbusiness": ["fact_inventory"]
        },
        analytics_tables={
            "microbusiness": ["fact_cash_shift"]
        },
        relationships={
            "fact_pos_line -> dim_product": "product_id",
            "fact_pos_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 1.5, "dim_customer": 3.0, "fact_pos_line": 15.0,
            "fact_inventory": 2.0, "fact_cash_shift": 2.0
        }
    ),

    "service_house_cleaning": BusinessEcosystem(
        key="service_house_cleaning",
        name="Limpieza Doméstica",
        display_name="Limpieza Doméstica",
        description="Servicio de limpieza residencial y comercial",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["clients", "schedules", "teams"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_appointments"]
        },
        support_tables={
            "microbusiness": ["dim_staff"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_appointments -> dim_service": "service_id",
            "fact_appointments -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 0.3, "dim_customer": 2.0, "fact_appointments": 8.0,
            "dim_staff": 0.1, "fact_commissions": 4.0
        }
    ),

    "retail_thrift_store": BusinessEcosystem(
        key="retail_thrift_store",
        name="Tienda de Segunda Mano",
        display_name="Tienda de Segunda Mano",
        description="Tienda de artículos usados y vintage",
        business_type=BusinessType.RETAIL,
        master_entities=["secondhand", "vintage", "donations"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "retail": ["fact_cash_drawer"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_ticket_line -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_product": 10.0, "dim_customer": 1.5, "fact_ticket_line": 8.0,
            "fact_cash_drawer": 3.0, "fact_returns": 0.2
        }
    ),

    "food_catering": BusinessEcosystem(
        key="food_catering",
        name="Servicio de Catering",
        display_name="Servicio de Catering",
        description="Servicio de catering para eventos y empresas",
        business_type=BusinessType.MICROBUSINESS,
        master_entities=["events", "menus", "clients"],
        core_tables={
            "microbusiness": ["dim_service", "dim_customer", "fact_custom_orders"]
        },
        support_tables={
            "microbusiness": ["dim_staff", "fact_inventory"]
        },
        analytics_tables={
            "microbusiness": ["fact_commissions"]
        },
        relationships={
            "fact_custom_orders -> dim_service": "service_id",
            "fact_custom_orders -> dim_customer": "customer_id"
        },
        volume_ratios={
            "dim_service": 1.0, "dim_customer": 0.4, "fact_custom_orders": 0.8,
            "dim_staff": 0.05, "fact_inventory": 5.0, "fact_commissions": 1.2
        }
    ),

    "specialty_escape_room": BusinessEcosystem(
        key="specialty_escape_room",
        name="Escape Room",
        display_name="Escape Room",
        description="Centro de entretenimiento con salas de escape temáticas",
        business_type=BusinessType.ENTERTAINMENT,
        master_entities=["rooms", "themes", "teams"],
        core_tables={
            "retail": ["dim_product", "dim_customer", "fact_ticket_line"]
        },
        support_tables={
            "microbusiness": ["fact_appointments", "dim_service"]
        },
        analytics_tables={
            "retail": ["fact_returns"]
        },
        relationships={
            "fact_ticket_line -> dim_product": "product_id",
            "fact_appointments -> dim_service": "service_id"
        },
        volume_ratios={
            "dim_product": 0.2, "dim_customer": 1.0, "fact_ticket_line": 4.0,
            "fact_appointments": 3.0, "dim_service": 0.15, "fact_returns": 0.1
        }
    )
}

# ===============================
# FUNCIONES DE UTILIDAD 
# ===============================

def get_available_ecosystems() -> Dict[str, BusinessEcosystem]:
    """Obtener todos los ecosistemas disponibles"""
    return BUSINESS_ECOSYSTEMS

def get_ecosystems_by_type(business_type: BusinessType) -> Dict[str, BusinessEcosystem]:
    """Obtener ecosistemas por tipo de negocio"""
    return {
        key: ecosystem for key, ecosystem in BUSINESS_ECOSYSTEMS.items()
        if ecosystem.business_type == business_type
    }

def get_ecosystem_by_key(key: str) -> Optional[BusinessEcosystem]:
    """Obtener un ecosistema específico por su clave"""
    return BUSINESS_ECOSYSTEMS.get(key)

def get_business_types() -> List[BusinessType]:
    """Obtener todos los tipos de negocio disponibles"""
    return list(set(ecosystem.business_type for ecosystem in BUSINESS_ECOSYSTEMS.values()))

def get_ecosystem_display_names() -> Dict[str, str]:
    """Obtener mapa de key -> display_name para la UI"""
    return {key: ecosystem.display_name for key, ecosystem in BUSINESS_ECOSYSTEMS.items()}