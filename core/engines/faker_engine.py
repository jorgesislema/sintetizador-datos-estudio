"""Motor Faker mejorado con heurísticas simples y soporte de localización.

El objetivo es evitar valores None masivos en previews y datasets cuando
los nombres de campo no están mapeados explícitamente. Se aplican reglas
por nombre y sufijos/prefijos frecuentes.

Soporta contextos geográficos y localización de datos por país/región.
"""
from __future__ import annotations
from typing import Dict, Any, Callable
import random
from datetime import datetime, timedelta, UTC

try:  # pragma: no cover
    from faker import Faker
except ImportError:  # pragma: no cover
    Faker = None  # type: ignore

# Importar sistemas de localización
try:
    from core.localization.geographic_contexts import (
        get_context_data, get_random_city, get_random_province, 
        get_phone_format, get_currency
    )
    LOCALIZATION_AVAILABLE = True
except ImportError:
    LOCALIZATION_AVAILABLE = False

_FAKE = Faker() if Faker else None
if _FAKE:
    _FAKE.seed_instance(42)

# ===== CONFIGURACIÓN GLOBAL DE LOCALIZACIÓN =====
_CURRENT_GEOGRAPHIC_CONTEXT = "global"
_CURRENT_LANGUAGE = "en"
_CURRENT_DATE_RANGE_START = None  # type: datetime | None
_CURRENT_DATE_RANGE_END = None    # type: datetime | None

def set_geographic_context(context_name: str):
    """Establecer el contexto geográfico global para la generación"""
    global _CURRENT_GEOGRAPHIC_CONTEXT
    _CURRENT_GEOGRAPHIC_CONTEXT = context_name

def set_language_context(language: str):
    """Establecer el idioma para la generación"""
    global _CURRENT_LANGUAGE
    _CURRENT_LANGUAGE = language

def get_current_geographic_context() -> str:
    """Obtener el contexto geográfico actual"""
    return _CURRENT_GEOGRAPHIC_CONTEXT

def get_current_language() -> str:
    """Obtener el idioma actual"""
    return _CURRENT_LANGUAGE

def set_date_range(start_ym: str | None, end_ym: str | None):
    """Establecer un rango global de fechas para la generación de campos de fecha/hora.

    Args:
        start_ym: Cadena en formato 'YYYY-MM' o 'YYYY-MM-DD' (inicio inclusive) o None para limpiar.
        end_ym: Cadena en formato 'YYYY-MM' o 'YYYY-MM-DD' (fin inclusive) o None para limpiar.
    """
    global _CURRENT_DATE_RANGE_START, _CURRENT_DATE_RANGE_END
    if not start_ym or not end_ym:
        _CURRENT_DATE_RANGE_START = None
        _CURRENT_DATE_RANGE_END = None
        return

    def _parse(s: str) -> datetime:
        s = s.strip()
        try:
            # Intentar YYYY-MM-DD
            return datetime.fromisoformat(s).replace(tzinfo=UTC) if 'T' not in s else datetime.fromisoformat(s)
        except Exception:
            # Intentar YYYY-MM
            try:
                year, month = map(int, s.split('-')[:2])
                return datetime(year, month, 1, tzinfo=UTC)
            except Exception as e:  # pragma: no cover
                raise ValueError(f"Fecha inválida para rango: {s}") from e

    start_dt = _parse(start_ym)
    end_dt = _parse(end_ym)
    # Normalizar orden
    if end_dt < start_dt:
        start_dt, end_dt = end_dt, start_dt
    _CURRENT_DATE_RANGE_START = start_dt
    _CURRENT_DATE_RANGE_END = end_dt

def _fake_or(default: str, attr: str) -> str:
    if _FAKE and hasattr(_FAKE, attr):
        return getattr(_FAKE, attr)()
    return default

def _rand_choice(opts):
    return random.choice(opts)

def _rand_numeric(min_v=0, max_v=1000):
    return random.randint(min_v, max_v)

def _rand_float(min_v=0, max_v=1000, nd=2):
    return round(random.uniform(min_v, max_v), nd)

def _rand_date(days_back=365):
    """Genera una fecha ISO. Si hay rango global, usarlo; si no, usar days_back relativo al ahora."""
    if _CURRENT_DATE_RANGE_START and _CURRENT_DATE_RANGE_END:
        start = _CURRENT_DATE_RANGE_START
        end = _CURRENT_DATE_RANGE_END
        # número de días entre ambos (inclusivo)
        delta_days = max(0, (end.date() - start.date()).days)
        pick = start + timedelta(days=random.randint(0, delta_days))
        return pick.isoformat()
    base = datetime.now(UTC)
    return (base - timedelta(days=random.randint(0, days_back))).isoformat()

def _rand_datetime_utc(days_back=365):
    """Genera una fecha/hora UTC aleatoria respetando el rango global si está definido."""
    if _CURRENT_DATE_RANGE_START and _CURRENT_DATE_RANGE_END:
        start = _CURRENT_DATE_RANGE_START
        end = _CURRENT_DATE_RANGE_END
        total_seconds = max(0, int((end - start).total_seconds()))
        # evitar cero segundos
        offset = 0 if total_seconds == 0 else random.randint(0, total_seconds)
        result = start + timedelta(seconds=offset)
        return result.isoformat()
    base = datetime.now(UTC)
    delta_days = random.randint(-abs(days_back), abs(days_back))
    result = base + timedelta(days=delta_days, hours=random.randint(0, 23), minutes=random.randint(0, 59))
    return result.isoformat()

def _rand_datetime_local():
    """Genera una fecha/hora local aleatoria respetando el rango global si está definido."""
    if _CURRENT_DATE_RANGE_START and _CURRENT_DATE_RANGE_END:
        # Convertir a naive local de ser necesario
        start = _CURRENT_DATE_RANGE_START
        end = _CURRENT_DATE_RANGE_END
        total_seconds = max(0, int((end - start).total_seconds()))
        offset = 0 if total_seconds == 0 else random.randint(0, total_seconds)
        result = (start + timedelta(seconds=offset)).replace(tzinfo=None)
        return result.isoformat()
    base = datetime.now()
    delta_days = random.randint(-30, 30)
    result = base + timedelta(days=delta_days, hours=random.randint(0, 23), minutes=random.randint(0, 59))
    return result.isoformat()

# ===== FUNCIONES LOCALIZADAS POR CONTEXTO GEOGRÁFICO =====

def _localized_city():
    """Genera una ciudad según el contexto geográfico actual"""
    if LOCALIZATION_AVAILABLE:
        return get_random_city(_CURRENT_GEOGRAPHIC_CONTEXT)
    return _fake_or("City", "city")

def _localized_province():
    """Genera una provincia/estado según el contexto geográfico actual"""
    if LOCALIZATION_AVAILABLE:
        return get_random_province(_CURRENT_GEOGRAPHIC_CONTEXT)
    return _fake_or("State", "state")

def _localized_phone():
    """Genera un teléfono con formato del contexto geográfico actual"""
    if LOCALIZATION_AVAILABLE:
        phone_format = get_phone_format(_CURRENT_GEOGRAPHIC_CONTEXT)
        if phone_format != "MIXED":
            # Generar número según formato del país
            if phone_format == "+593":  # Ecuador
                return f"+593-{random.randint(90,99)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
            elif phone_format == "+57":  # Colombia
                return f"+57-{random.randint(300,350)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
            elif phone_format == "+52":  # México
                return f"+52-{random.randint(55,99)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}"
            elif phone_format == "+34":  # España
                return f"+34-{random.randint(600,799)}-{random.randint(100,999)}-{random.randint(100,999)}"
            elif phone_format == "+1":  # USA/Canadá
                return f"+1-{random.randint(200,999)}-{random.randint(200,999)}-{random.randint(1000,9999)}"
            else:
                return f"{phone_format}-{random.randint(100000,999999999)}"
    return _fake_or("+1-555-0000", "phone_number")

def _localized_currency():
    """Obtiene la moneda del contexto geográfico actual"""
    if LOCALIZATION_AVAILABLE:
        return get_currency(_CURRENT_GEOGRAPHIC_CONTEXT)
    return "USD"

def _localized_address():
    """Genera una dirección localizada según el contexto geográfico"""
    if LOCALIZATION_AVAILABLE:
        context = get_context_data(_CURRENT_GEOGRAPHIC_CONTEXT)
        if "streets" in context:
            street = random.choice(context["streets"])
            number = random.randint(1, 999)
            return f"{street} {number}"
    return _fake_or("123 Main St", "address")

def _localized_postal_code():
    """Genera código postal según formato del país"""
    if LOCALIZATION_AVAILABLE:
        context = get_context_data(_CURRENT_GEOGRAPHIC_CONTEXT)
        postal_format = context.get("postal_code_format", "#####")
        
        # Generar según formato específico
        if postal_format == "EC######":  # Ecuador
            return f"EC{random.randint(100000,999999)}"
        elif postal_format == "######":  # Colombia
            return f"{random.randint(100000,999999)}"
        elif postal_format == "#####":  # México, España, USA
            return f"{random.randint(10000,99999)}"
        elif postal_format == "A####AAA":  # Argentina
            return f"{random.choice('ABCDEFG')}{random.randint(1000,9999)}{random.choice('ABC')}{random.choice('ABC')}{random.choice('ABC')}"
        elif postal_format == "A#A #A#":  # Canadá
            return f"{random.choice('ABCDEFG')}{random.randint(0,9)}{random.choice('ABCDEFG')} {random.randint(0,9)}{random.choice('ABCDEFG')}{random.randint(0,9)}"
    return f"{random.randint(10000,99999)}"

def _localized_country():
    """Obtiene el país del contexto geográfico actual"""
    if LOCALIZATION_AVAILABLE:
        context = get_context_data(_CURRENT_GEOGRAPHIC_CONTEXT)
        if _CURRENT_GEOGRAPHIC_CONTEXT == "global":
            return random.choice(context.get("countries", ["Global"]))
        else:
            # Mapear código de país a nombre
            country_names = {
                "ecuador": "Ecuador",
                "colombia": "Colombia", 
                "mexico": "México",
                "argentina": "Argentina",
                "chile": "Chile",
                "peru": "Perú",
                "espana": "España",
                "francia": "Francia",
                "alemania": "Alemania",
                "italia": "Italia",
                "usa": "Estados Unidos",
                "canada": "Canadá"
            }
            return country_names.get(_CURRENT_GEOGRAPHIC_CONTEXT, "Global")
    return _fake_or("Country", "country")

GENERAL_MAP: Dict[str, Callable[[], Any]] = {
    # Identificadores genéricos
    "id": lambda: _rand_numeric(1, 10_000_000),
    "*_id": lambda: _rand_numeric(1, 10_000_000),
    "*_id_hash": lambda: hashlib_sha("id" + str(_rand_numeric())),
    "*_code": lambda: f"C{_rand_numeric(100,999)}",
    "*_number": lambda: f"N{_rand_numeric(1000,9999)}",
    
    # Nombres y descripciones - Base
    "first_name": lambda: _fake_or("Name", "first_name"),
    "last_name": lambda: _fake_or("Last", "last_name"),
    "provider_name": lambda: _fake_or("Clinic", "company"),
    "procedure_name": lambda: _fake_or("Procedure", "bs"),
    "diagnosis_name": lambda: _fake_or("Diagnosis", "catch_phrase"),
    "branch_name": lambda: _fake_or("Branch", "city"),
    "site_name": lambda: _fake_or("Site", "street_name"),
    "channel_name": lambda: _fake_or("Channel", "word"),
    "visit_name": lambda: f"Visit {_rand_numeric(1,20)}",
    "product_line": lambda: _fake_or("Product", "word"),
    "policy_id": lambda: f"POL{_rand_numeric(1000,9999)}",
    "coverage_limit": lambda: _rand_float(10000, 1000000, 2),
    "deductible": lambda: _rand_float(500, 5000, 2),
    "premium_amount": lambda: _rand_float(100, 2000, 2),
    "claim_amount": lambda: _rand_float(100, 50000, 2),
    "approval_amount": lambda: _rand_float(100, 45000, 2),
    "outstanding_balance": lambda: _rand_float(0, 10000, 2),
    "credit_limit": lambda: _rand_float(1000, 50000, 2),
    "interest_rate": lambda: _rand_float(0.01, 0.25, 4),
    "loan_id": lambda: _rand_numeric(1000000, 9999999),
    "account_id": lambda: _rand_numeric(100000, 999999),
    "transaction_amount": lambda: _rand_float(1, 10000, 2),
    "fee_amount": lambda: _rand_float(0, 100, 2),
    
    # ===== CAMPOS GEOGRÁFICOS LOCALIZADOS =====
    "city": lambda: _localized_city(),
    "city_name": lambda: _localized_city(),
    "state": lambda: _localized_province(),
    "province": lambda: _localized_province(),
    "state_province": lambda: _localized_province(),
    "country": lambda: _localized_country(),
    "country_name": lambda: _localized_country(),
    "address": lambda: _localized_address(),
    "street_address": lambda: _localized_address(),
    "postal_code": lambda: _localized_postal_code(),
    "zip_code": lambda: _localized_postal_code(),
    "currency_code": lambda: _localized_currency(),
    "phone_number": lambda: _localized_phone(),
    
    # Enterprise - HR/RR.HH.
    "employee_id": lambda: _rand_numeric(10000, 99999),
    "email_corp": lambda: _fake_or("john.doe@company.com", "company_email"),
    "email_personal": lambda: _fake_or("john@gmail.com", "email"),
    "job_title": lambda: _rand_choice(["Analyst", "Manager", "Director", "Specialist", "Coordinator"]),
    "job_family": lambda: _rand_choice(["Engineering", "Sales", "Marketing", "HR", "Finance"]),
    "job_level": lambda: _rand_choice(["Junior", "Mid", "Senior", "Lead", "Principal"]),
    "grade": lambda: _rand_choice(["A", "B", "C", "D", "E"]),
    "salary_base_annual": lambda: _rand_float(30000, 150000, 2),
    "org_unit_name": lambda: _rand_choice(["Engineering", "Sales", "Marketing", "HR", "Finance", "Operations"]),
    "manager_employee_id": lambda: _rand_numeric(10000, 99999),
    "parent_org_unit_id": lambda: _rand_numeric(100, 999),
    "headcount_date": lambda: _rand_date(365),
    "active_flag": lambda: _rand_choice([True, False]),
    "termination_reason": lambda: _rand_choice(["Resignation", "Layoff", "Performance", "Retirement"]),
    "voluntary_flag": lambda: _rand_choice([True, False]),
    "hours_overtime": lambda: _rand_float(0, 20, 2),
    "overtime_rate": lambda: _rand_float(1.5, 2.0, 2),
    "pto_type": lambda: _rand_choice(["Vacation", "Sick", "Personal", "Holiday"]),
    "hours_pto": lambda: _rand_float(1, 8, 2),
    "approval_status": lambda: _rand_choice(["Approved", "Pending", "Rejected"]),
    
    # Microbusiness/Retail - Productos y Ventas  
    "sku": lambda: f"SKU{_rand_numeric(10000,99999)}",
    "product_name": lambda: _fake_or("Product Name", "word"),
    "category": lambda: _rand_choice(["Electronics", "Clothing", "Food", "Books", "Home"]),
    "brand": lambda: _fake_or("Brand Name", "company"),
    "unit_size": lambda: f"{_rand_numeric(1,1000)}{_rand_choice(['ml', 'g', 'kg', 'L', 'units'])}",
    "uom": lambda: _rand_choice(["each", "kg", "liter", "box", "pack"]),
    "list_price": lambda: _rand_float(5, 500, 2),
    "cost_unit": lambda: _rand_float(1, 250, 2),
    "unit_price": lambda: _rand_float(1, 500, 2),
    "supplier_name": lambda: _fake_or("Supplier Corp", "company"),
    "contact_phone": lambda: _localized_phone(),
    "credit_terms_days": lambda: _rand_numeric(15, 90),
    "lead_time_days": lambda: _rand_numeric(1, 30),
    "store_name": lambda: _fake_or("Store Name", "street_name"),
    "store_type": lambda: _rand_choice(["Convenience", "Grocery", "Specialty", "Department"]),
    "owner_name": lambda: _fake_or("Owner Name", "name"),
    "customer_name": lambda: _fake_or("Customer Name", "name"),
    "phone": lambda: _localized_phone(),
    "loyalty_points": lambda: _rand_numeric(0, 10000),
    "loyalty_tier": lambda: _rand_choice(["Bronze", "Silver", "Gold", "Platinum"]),
    "loyalty_points_balance": lambda: _rand_numeric(0, 50000),
    "registration_date": lambda: _rand_date(1000),
    "opening_date": lambda: _rand_date(2000),
    "ticket_id": lambda: _rand_numeric(100000, 999999),
    "line_total": lambda: _rand_float(1, 1000, 2),
    "payment_method": lambda: _rand_choice(["Cash", "Credit", "Debit", "Mobile"]),
    "tax_amount": lambda: _rand_float(0, 50, 2),
    "discount_amount": lambda: _rand_float(0, 100, 2),
    "void_reason": lambda: _rand_choice(["Customer Request", "Wrong Item", "Price Error"]),
    "return_reason": lambda: _rand_choice(["Defective", "Wrong Size", "Customer Change"]),
    "cashier_id": lambda: _rand_numeric(1000, 9999),
    "shift_type": lambda: _rand_choice(["Morning", "Afternoon", "Night"]),
    "ean_upc": lambda: f"{_rand_numeric(100000000000, 999999999999)}",
    
    # Education - K-12, EdTech B2B, Higher Education
    "lead_id": lambda: _rand_numeric(100000, 999999),
    "student_id": lambda: _rand_numeric(100000, 999999),
    "parent_id": lambda: _rand_numeric(100000, 999999),
    "faculty_id": lambda: _rand_numeric(10000, 99999),
    "course_id": lambda: _rand_numeric(1000, 9999),
    "account_id": lambda: _rand_numeric(10000, 99999),
    "program_id": lambda: _rand_numeric(1000, 9999),
    "enrollment_id": lambda: _rand_numeric(1000000, 9999999),
    "grade_id": lambda: _rand_numeric(1000000, 9999999),
    "parent_first_name": lambda: _fake_or("Parent Name", "first_name"),
    "parent_last_name": lambda: _fake_or("Parent Surname", "last_name"),
    "parent_email": lambda: _fake_or("parent@email.com", "email"),
    "parent_phone": lambda: _fake_or("+1234567890", "phone_number"),
    "student_first_name": lambda: _fake_or("Student Name", "first_name"),
    "student_last_name": lambda: _fake_or("Student Surname", "last_name"),
    "student_birth_date": lambda: _rand_date(6570),  # Niños de ~18 años atrás
    "grade_level": lambda: _rand_choice(["Pre-K", "K", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th"]),
    "school_interest": lambda: _rand_choice(["Public", "Private", "Charter", "Magnet", "Homeschool"]),
    "lead_source": lambda: _rand_choice(["Website", "Referral", "Social Media", "Advertisement", "Event", "Cold Call"]),
    "lead_status": lambda: _rand_choice(["New", "Contacted", "Qualified", "Proposal", "Enrolled", "Lost"]),
    "inquiry_date": lambda: _rand_date(365),
    "follow_up_date": lambda: _rand_date(30),
    "assigned_counselor": lambda: _fake_or("Counselor Name", "name"),
    "location_preference": lambda: _rand_choice(["Main Campus", "North Campus", "South Campus", "Online", "Hybrid"]),
    "budget_range": lambda: _rand_choice(["$0-5k", "$5-10k", "$10-15k", "$15-20k", "$20k+"]),
    "special_needs": lambda: _rand_choice([True, False]),
    "languages_spoken": lambda: _rand_choice(["English", "Spanish", "French", "Mandarin", "Bilingual"]),
    "previous_school_type": lambda: _rand_choice(["Public", "Private", "Charter", "Homeschool", "International"]),
    "program_name": lambda: _rand_choice(["Elementary Program", "Middle School", "High School", "IB Program", "AP Program"]),
    "program_type": lambda: _rand_choice(["Traditional", "Montessori", "Waldorf", "IB", "STEM", "Arts"]),
    "grade_levels_served": lambda: _rand_choice(["K-5", "6-8", "9-12", "K-12", "Pre-K-12"]),
    "curriculum_type": lambda: _rand_choice(["Common Core", "IB", "AP", "Montessori", "Custom"]),
    "language_instruction": lambda: _rand_choice(["English", "Spanish", "French", "Bilingual", "Immersion"]),
    "tuition_annual": lambda: _rand_float(5000, 50000, 2),
    "application_fee": lambda: _rand_float(50, 500, 2),
    "program_capacity": lambda: _rand_numeric(20, 500),
    "current_enrollment": lambda: _rand_numeric(15, 450),
    "waiting_list_count": lambda: _rand_numeric(0, 50),
    "accreditation_status": lambda: _rand_choice(["Accredited", "Pending", "Not Accredited"]),
    "facilities_included": lambda: _rand_choice(["Library", "Lab", "Gym", "Cafeteria", "Pool", "Theater"]),
    "extracurricular_options": lambda: _rand_choice(["Sports", "Arts", "Music", "Drama", "Robotics", "Debate"]),
    "occupation": lambda: _rand_choice(["Engineer", "Doctor", "Teacher", "Lawyer", "Business", "Other"]),
    "employer": lambda: _fake_or("Company Name", "company"),
    "income_range": lambda: _rand_choice(["$0-50k", "$50-100k", "$100-150k", "$150-200k", "$200k+"]),
    "education_level": lambda: _rand_choice(["High School", "Bachelor's", "Master's", "PhD", "Professional"]),
    "marital_status": lambda: _rand_choice(["Single", "Married", "Divorced", "Widowed"]),
    "number_of_children": lambda: _rand_numeric(1, 5),
    "preferred_communication": lambda: _rand_choice(["Email", "Phone", "Text", "Mail"]),
    "emergency_contact_name": lambda: _fake_or("Emergency Contact", "name"),
    "emergency_contact_phone": lambda: _fake_or("+1234567890", "phone_number"),
    "application_status": lambda: _rand_choice(["Submitted", "Under Review", "Accepted", "Rejected", "Waitlisted"]),
    "admission_test_score": lambda: _rand_numeric(200, 800),
    "interview_score": lambda: _rand_numeric(1, 10),
    "recommendation_score": lambda: _rand_numeric(1, 10),
    "financial_aid_requested": lambda: _rand_choice([True, False]),
    "financial_aid_approved": lambda: _rand_choice([True, False]),
    "scholarship_amount": lambda: _rand_float(0, 10000, 2),
    "deposit_paid": lambda: _rand_choice([True, False]),
    "tuition_balance": lambda: _rand_float(0, 50000, 2),
    "payment_plan_selected": lambda: _rand_choice(["Annual", "Semester", "Monthly", "Quarterly"]),
    "school_name": lambda: _fake_or("Educational Institution", "company"),
    "school_type": lambda: _rand_choice(["Public", "Private", "Charter", "Magnet", "Religious"]),
    "district_name": lambda: _fake_or("School District", "city"),
    "school_level": lambda: _rand_choice(["Elementary", "Middle", "High", "K-12", "PreK-12"]),
    "total_students": lambda: _rand_numeric(100, 5000),
    "total_teachers": lambda: _rand_numeric(10, 300),
    "total_staff": lambda: _rand_numeric(5, 150),
    "principal_name": lambda: _fake_or("Principal Name", "name"),
    "principal_email": lambda: _fake_or("principal@school.edu", "email"),
    "tech_coordinator_name": lambda: _fake_or("Tech Coordinator", "name"),
    "tech_coordinator_email": lambda: _fake_or("tech@school.edu", "email"),
    "procurement_contact_name": lambda: _fake_or("Procurement Contact", "name"),
    "procurement_contact_email": lambda: _fake_or("procurement@school.edu", "email"),
    "annual_budget_technology": lambda: _rand_float(10000, 500000, 2),
    "current_lms_platform": lambda: _rand_choice(["Canvas", "Blackboard", "Moodle", "Google Classroom", "Schoology"]),
    "internet_bandwidth": lambda: _rand_choice(["100Mbps", "500Mbps", "1Gbps", "10Gbps"]),
    "device_inventory_count": lambda: _rand_numeric(50, 2000),
    "contract_start_date": lambda: _rand_date(730),
    "contract_end_date": lambda: _rand_date(365),
    "sales_rep_assigned": lambda: _fake_or("Sales Rep", "name"),
    "product_category": lambda: _rand_choice(["LMS", "Assessment", "Content", "Analytics", "Communication"]),
    "target_age_group": lambda: _rand_choice(["K-5", "6-8", "9-12", "K-12", "Adult"]),
    "subject_areas": lambda: _rand_choice(["Math", "Science", "ELA", "Social Studies", "All Subjects"]),
    "license_type": lambda: _rand_choice(["Site", "Concurrent", "Named User", "Floating"]),
    "pricing_model": lambda: _rand_choice(["Per Student", "Per Teacher", "Site License", "Concurrent Users"]),
    "price_per_license": lambda: _rand_float(5, 100, 2),
    "minimum_licenses": lambda: _rand_numeric(10, 100),
    "maximum_licenses": lambda: _rand_numeric(1000, 10000),
    "integration_capabilities": lambda: _rand_choice(["SIS", "LMS", "Google", "Microsoft", "All"]),
    "training_included": lambda: _rand_choice([True, False]),
    "support_level": lambda: _rand_choice(["Basic", "Standard", "Premium", "Enterprise"]),
    "trial_period_days": lambda: _rand_numeric(7, 90),
    "implementation_time": lambda: _rand_choice(["1 week", "2 weeks", "1 month", "3 months"]),
    "certification_offered": lambda: _rand_choice([True, False]),
    "license_id": lambda: _rand_numeric(1000000, 9999999),
    "user_type": lambda: _rand_choice(["Student", "Teacher", "Administrator", "Parent"]),
    "session_duration_minutes": lambda: _rand_numeric(5, 240),
    "features_accessed": lambda: _rand_choice(["Assignments", "Gradebook", "Communication", "Reports", "Analytics"]),
    "activities_completed": lambda: _rand_numeric(0, 50),
    "assessments_taken": lambda: _rand_numeric(0, 20),
    "content_created": lambda: _rand_numeric(0, 100),
    "content_shared": lambda: _rand_numeric(0, 50),
    "login_method": lambda: _rand_choice(["SSO", "Direct", "Google", "Microsoft"]),
    "device_type": lambda: _rand_choice(["Desktop", "Tablet", "Mobile", "Chromebook"]),
    "browser_type": lambda: _rand_choice(["Chrome", "Safari", "Firefox", "Edge"]),
    "location_accessed": lambda: _rand_choice(["School", "Home", "Library", "Other"]),
    "peak_concurrent_users": lambda: _rand_numeric(1, 500),
    "data_exported": lambda: _rand_choice([True, False]),
    "support_tickets_created": lambda: _rand_numeric(0, 10),
    "opportunity_stage": lambda: _rand_choice(["Lead", "Qualified", "Demo", "Trial", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]),
    "probability_percentage": lambda: _rand_numeric(0, 100),
    "deal_value": lambda: _rand_float(1000, 100000, 2),
    "license_quantity": lambda: _rand_numeric(10, 1000),
    "contract_length_months": lambda: _rand_choice([12, 24, 36]),
    "decision_maker_name": lambda: _fake_or("Decision Maker", "name"),
    "decision_maker_role": lambda: _rand_choice(["Principal", "Superintendent", "Tech Director", "Curriculum Director"]),
    "demo_date": lambda: _rand_date(30),
    "trial_start_date": lambda: _rand_date(60),
    "trial_end_date": lambda: _rand_date(30),
    "proposal_sent_date": lambda: _rand_date(45),
    "negotiation_start_date": lambda: _rand_date(30),
    "close_date": lambda: _rand_date(90),
    "won_lost_reason": lambda: _rand_choice(["Price", "Features", "Timeline", "Budget", "Competitor"]),
    "competitor_involved": lambda: _rand_choice(["Google", "Microsoft", "Canvas", "Blackboard", "Other"]),
    "sales_rep_id": lambda: _rand_numeric(1000, 9999),
    "sales_cycle_days": lambda: _rand_numeric(30, 365),
    "ethnicity": lambda: _rand_choice(["Caucasian", "Hispanic", "African American", "Asian", "Native American", "Other"]),
    "citizenship_status": lambda: _rand_choice(["Citizen", "Permanent Resident", "International", "Other"]),
    "student_status": lambda: _rand_choice(["Active", "Inactive", "Graduated", "Withdrawn", "Transfer"]),
    "enrollment_type": lambda: _rand_choice(["Full-time", "Part-time", "Audit", "Non-degree"]),
    "academic_level": lambda: _rand_choice(["Freshman", "Sophomore", "Junior", "Senior", "Graduate"]),
    "major_primary": lambda: _rand_choice(["Business", "Engineering", "Education", "Arts", "Science", "Medicine"]),
    "major_secondary": lambda: _rand_choice(["Business", "Engineering", "Education", "Arts", "Science", "None"]),
    "minor_field": lambda: _rand_choice(["Psychology", "Mathematics", "History", "English", "Computer Science", "None"]),
    "advisor_faculty_id": lambda: _rand_numeric(10000, 99999),
    "cumulative_gpa": lambda: _rand_float(0.0, 4.0, 2),
    "credit_hours_completed": lambda: _rand_numeric(0, 180),
    "credit_hours_attempted": lambda: _rand_numeric(0, 200),
    "financial_aid_status": lambda: _rand_choice(["Eligible", "Not Eligible", "Pending", "Denied"]),
    "work_study_eligible": lambda: _rand_choice([True, False]),
    "housing_status": lambda: _rand_choice(["On-campus", "Off-campus", "Commuter", "Family Housing"]),
    "meal_plan_type": lambda: _rand_choice(["Full", "Partial", "Commuter", "None"]),
    "course_code": lambda: f"{_rand_choice(['MATH', 'ENG', 'SCI', 'HIST', 'ART'])}{_rand_numeric(100, 499)}",
    "course_title": lambda: _rand_choice(["Introduction to", "Advanced", "Principles of", "Applied", "Contemporary"]) + " " + _rand_choice(["Mathematics", "Science", "Literature", "History", "Art"]),
    "course_description": lambda: _fake_or("Course description content", "paragraph"),
    "school_college": lambda: _rand_choice(["Arts & Sciences", "Engineering", "Business", "Education", "Medicine"]),
    "credit_hours": lambda: _rand_choice([1, 2, 3, 4, 6]),
    "course_level": lambda: _rand_choice(["Undergraduate", "Graduate", "Doctoral"]),
    "prerequisites": lambda: _rand_choice(["None", "MATH101", "ENG101", "SCI101", "Multiple"]),
    "corequisites": lambda: _rand_choice(["None", "Lab Component", "Discussion Section"]),
    "course_format": lambda: _rand_choice(["Lecture", "Lab", "Seminar", "Independent Study", "Hybrid"]),
    "instruction_method": lambda: _rand_choice(["In-person", "Online", "Hybrid", "Synchronous", "Asynchronous"]),
    "max_enrollment": lambda: _rand_numeric(15, 300),
    "lab_required": lambda: _rand_choice([True, False]),
    "field_work_required": lambda: _rand_choice([True, False]),
    "internship_component": lambda: _rand_choice([True, False]),
    "certification_prep": lambda: _rand_choice([True, False]),
    "transferable_credits": lambda: _rand_choice([True, False]),
    "repeatable": lambda: _rand_choice([True, False]),
    "pass_fail_option": lambda: _rand_choice([True, False]),
    "honors_section": lambda: _rand_choice([True, False]),
    "writing_intensive": lambda: _rand_choice([True, False]),
    "title_rank": lambda: _rand_choice(["Instructor", "Assistant Professor", "Associate Professor", "Professor", "Adjunct"]),
    "employment_status": lambda: _rand_choice(["Full-time", "Part-time", "Adjunct", "Visiting", "Emeritus"]),
    "tenure_status": lambda: _rand_choice(["Tenured", "Tenure-track", "Non-tenure", "Clinical"]),
    "highest_degree": lambda: _rand_choice(["PhD", "Master's", "Professional", "Bachelor's"]),
    "specialization_area": lambda: _rand_choice(["Research", "Teaching", "Clinical", "Applied", "Theoretical"]),
    "research_interests": lambda: _fake_or("Research focus area", "catch_phrase"),
    "office_hours": lambda: _rand_choice(["MWF 2-4pm", "TTh 1-3pm", "By Appointment", "Online Only"]),
    "teaching_load": lambda: _rand_numeric(2, 8),
    "administrative_roles": lambda: _rand_choice(["Department Chair", "Committee Member", "Advisor", "Coordinator", "None"]),
    "committee_memberships": lambda: _rand_numeric(0, 5),
    "publication_count": lambda: _rand_numeric(0, 100),
    "grant_funding_total": lambda: _rand_float(0, 500000, 2),
    "sabbatical_eligible": lambda: _rand_choice([True, False]),
    "semester_id": lambda: _rand_numeric(1000, 9999),
    "academic_year": lambda: _rand_choice(["2023-24", "2024-25", "2025-26"]),
    "term_name": lambda: _rand_choice(["Fall", "Spring", "Summer", "Winter"]),
    "term_code": lambda: _rand_choice(["F24", "S25", "U25", "W25"]),
    "registration_start_date": lambda: _rand_date(120),
    "registration_end_date": lambda: _rand_date(90),
    "add_drop_deadline": lambda: _rand_date(75),
    "withdrawal_deadline": lambda: _rand_date(45),
    "final_exam_start": lambda: _rand_date(20),
    "final_exam_end": lambda: _rand_date(15),
    "graduation_date": lambda: _rand_date(30),
    "term_status": lambda: _rand_choice(["Active", "Completed", "Future", "Cancelled"]),
    "credit_hour_limit": lambda: _rand_numeric(18, 24),
    "part_time_threshold": lambda: _rand_numeric(6, 11),
    "full_time_threshold": lambda: _rand_numeric(12, 15),
    "section_number": lambda: _rand_numeric(1, 20),
    "grade_letter": lambda: _rand_choice(["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F", "W", "I"]),
    "grade_points": lambda: _rand_float(0.0, 4.0, 2),
    "grade_status": lambda: _rand_choice(["Final", "Temporary", "Incomplete", "Withdrawn"]),
    "attempt_number": lambda: _rand_numeric(1, 3),
    "withdrawal_date": lambda: _rand_date(60) if _rand_choice([True, False, False]) else None,
    "incomplete_date": lambda: _rand_date(30) if _rand_choice([True, False, False, False]) else None,
    "grade_change_date": lambda: _rand_date(30) if _rand_choice([True, False, False, False]) else None,
    "grade_change_reason": lambda: _rand_choice(["Calculation Error", "Late Submission", "Grade Appeal", "Administrative"]),
    "midterm_grade": lambda: _rand_choice(["A", "B", "C", "D", "F", "S", "U"]),
    "final_exam_score": lambda: _rand_numeric(0, 100),
    "final_project_score": lambda: _rand_numeric(0, 100),
    "participation_score": lambda: _rand_numeric(0, 100),
    "attendance_percentage": lambda: _rand_float(0, 100, 1),
    "enrollment_status": lambda: _rand_choice(["Enrolled", "Withdrawn", "Completed", "In Progress"]),
    "enrollment_method": lambda: _rand_choice(["Online", "In-person", "Phone", "Advisor", "Auto-registration"]),
    "waitlist_position": lambda: _rand_numeric(1, 50) if _rand_choice([True, False, False]) else None,
    "registration_priority": lambda: _rand_numeric(1, 9),
    "fees_amount": lambda: _rand_float(100, 2000, 2),
    "financial_aid_applied": lambda: _rand_float(0, 10000, 2),
    "add_drop_count": lambda: _rand_numeric(0, 5),
    "last_attendance_date": lambda: _rand_date(30),
    "financial_record_id": lambda: _rand_numeric(1000000, 9999999),
    "transaction_category": lambda: _rand_choice(["Tuition", "Fees", "Housing", "Meals", "Books", "Miscellaneous"]),
    "room_board_amount": lambda: _rand_float(2000, 15000, 2),
    "work_study_amount": lambda: _rand_float(0, 3000, 2),
    "payment_plan_id": lambda: _rand_numeric(1000, 9999),
    "balance_forward": lambda: _rand_float(0, 5000, 2),
    "current_balance": lambda: _rand_float(0, 10000, 2),
    "performance_id": lambda: _rand_numeric(1000000, 9999999),
    "gpa_semester": lambda: _rand_float(0.0, 4.0, 2),
    "gpa_cumulative": lambda: _rand_float(0.0, 4.0, 2),
    "credit_hours_passed": lambda: _rand_numeric(0, 18),
    "courses_withdrawn": lambda: _rand_numeric(0, 3),
    "courses_incomplete": lambda: _rand_numeric(0, 2),
    "academic_standing": lambda: _rand_choice(["Good Standing", "Academic Probation", "Academic Suspension", "Dean's List"]),
    "probation_status": lambda: _rand_choice(["None", "Academic", "Financial", "Disciplinary"]),
    "honors_achievement": lambda: _rand_choice(["None", "Dean's List", "President's List", "Magna Cum Laude", "Summa Cum Laude"]),
    "dean_list_status": lambda: _rand_choice([True, False]),
    "graduation_progress_percentage": lambda: _rand_float(0, 100, 1),
    "major_change_count": lambda: _rand_numeric(0, 3),
    "advisor_meetings_count": lambda: _rand_numeric(0, 10),
    "retention_id": lambda: _rand_numeric(1000000, 9999999),
    "cohort_year": lambda: _rand_choice([2020, 2021, 2022, 2023, 2024]),
    "retention_risk_score": lambda: _rand_float(0, 100, 1),
    "attendance_rate": lambda: _rand_float(0, 100, 1),
    "course_completion_rate": lambda: _rand_float(0, 100, 1),
    "support_services_used": lambda: _rand_choice(["Tutoring", "Counseling", "Career Services", "Financial Aid", "Multiple", "None"]),
    "housing_changes": lambda: _rand_numeric(0, 3),
    "major_changes": lambda: _rand_numeric(0, 2),
    "advisor_changes": lambda: _rand_numeric(0, 2),
    "academic_interventions": lambda: _rand_choice(["None", "Early Alert", "Academic Coaching", "Tutoring", "Counseling"]),
    "social_engagement_score": lambda: _rand_float(0, 100, 1),
    "early_alert_flags": lambda: _rand_numeric(0, 5),
    "graduation_likelihood": lambda: _rand_float(0, 100, 1),
    
    # Finance - Campos específicos ya cubiertos
    "risk_factors": lambda: _rand_choice(["LOW", "MED", "HIGH"]),
    "specialty": lambda: _rand_choice(["CARDIO", "DERMA", "GEN", "PED"]),
    "department": lambda: _rand_choice(["HR","FIN","OPS","IT"]),
    "chronic_conditions": lambda: _rand_choice(["NONE","DM2","HTA","ASTHMA"]),
    
    # Healthcare - Campos específicos ya cubiertos
    "procedure_category": lambda: _rand_choice(["LAB","IMG","CONSULT","SURG"]),
    "encounter_type": lambda: _rand_choice(["INPATIENT","OUTPATIENT","ER"]),
    "gender": lambda: _rand_choice(["M","F"]),
    "phase": lambda: _rand_choice(["I","II","III","IV"]),
    "arm": lambda: _rand_choice(["A","B","C"]),
    "channel_type": lambda: _rand_choice(["VIDEO","PHONE","CHAT"]),
    "severity_level": lambda: _rand_choice(["LOW","MED","HIGH"]),
    "chronic_flag": lambda: _rand_choice(["Y","N"]),
    "abnormal_flag": lambda: _rand_choice(["Y","N"]),
    "related_to_study": lambda: _rand_choice(["Y","N"]),
    "completion_status": lambda: _rand_choice(["DONE","CANCEL","NO_SHOW"]),
    "payment_status": lambda: _rand_choice(["PAID","PENDING","LATE"]),
    "claim_status": lambda: _rand_choice(["OPEN","CLOSED","IN_REVIEW"]),
    
    # Valores numéricos - Ampliados
    "base_cost": lambda: _rand_float(50, 5000, 2),
    "duration_min": lambda: _rand_numeric(5, 480),
    "loan_amount": lambda: _rand_float(1000, 50000, 2),
    "interest_rate": lambda: _rand_float(0, 0.25, 4),
    "interest_rate_apr": lambda: _rand_float(0, 0.35, 4),
    "premium_amount": lambda: _rand_float(10, 1000, 2),
    "claim_amount": lambda: _rand_float(10, 15000, 2),
    "paid_amount": lambda: _rand_float(0, 15000, 2),
    "reserve_amount": lambda: _rand_float(0, 20000, 2),
    "risk_score": lambda: _rand_float(0, 1, 3),
    "fraud_score": lambda: _rand_float(0, 1, 3),
    "credit_score": lambda: _rand_numeric(300, 850),
    "pd_score": lambda: _rand_float(0, 1, 3),
    "medication_taken_pct": lambda: _rand_float(0,100,2),
    "compliance_score": lambda: _rand_float(0,100,2),
    "dose_mg": lambda: _rand_numeric(1,1000),
    "duration_days": lambda: _rand_numeric(1,180),
    "quantity": lambda: _rand_numeric(1,60),
    "refills": lambda: _rand_numeric(0,5),
    "rating": lambda: _rand_numeric(1,5),
    "nps_score": lambda: _rand_numeric(0,10),
    
    # Fechas (ISO) - Ampliadas
    "start_date": lambda: _rand_date(900),
    "end_date": lambda: _rand_date(700),
    "hire_date": lambda: _rand_date(1500),
    "termination_date": lambda: _rand_date(365) if _rand_choice([True, False, False]) else None,
    "admission_date": lambda: _rand_date(400),
    "discharge_date": lambda: _rand_date(400),
    "score_date": lambda: _rand_date(180),
    "assessment_date": lambda: _rand_date(180),
    "loss_date": lambda: _rand_date(400),
    "claim_date": lambda: _rand_date(400),
    "reserve_date": lambda: _rand_date(200),
    "measurement_date": lambda: _rand_date(180),
    "randomization_date": lambda: _rand_date(180),
    "visit_window_start": lambda: _rand_date(90),
    "visit_window_end": lambda: _rand_date(90),
    "appointment_date": lambda: _rand_date(60),
    "due_date": lambda: _rand_date(90),
    "paid_date": lambda: _rand_date(30),
    "disbursement_date": lambda: _rand_date(500),
    
    # Micronegocios Especializados - Panadería
    "recipe_id": lambda: _rand_numeric(1000, 9999),
    "product_name": lambda: _rand_choice([
        "Pan de Molde", "Croissant", "Baguette", "Pan Integral", "Torta de Chocolate", 
        "Empanadas", "Galletas de Avena", "Muffins de Arándanos", "Pan Dulce", "Facturas",
        "Medialunas", "Pan de Centeno", "Torta Tres Leches", "Cupcakes", "Pan Francés",
        "Rosca de Reyes", "Donas Glaseadas", "Pan de Ajo", "Tartaletas", "Bizcochuelo"
    ]),
    "ingredients_main": lambda: _rand_choice([
        "Harina, Agua, Levadura, Sal", "Huevos, Azúcar, Mantequilla, Harina", 
        "Chocolate, Crema, Vainilla, Azúcar", "Masa Hojaldre, Mantequilla", 
        "Harina Integral, Semillas, Miel", "Queso, Jamón, Masa", "Avena, Miel, Nueces"
    ]),
    "preparation_time_hours": lambda: _rand_float(0.5, 6.0, 1),
    "baking_time_minutes": lambda: _rand_numeric(15, 180),
    "shelf_life_days": lambda: _rand_numeric(1, 14),
    "storage_requirements": lambda: _rand_choice(["Temperatura ambiente", "Refrigerado", "Congelado", "Lugar seco"]),
    "allergen_info": lambda: _rand_choice(["Gluten", "Lactosa", "Huevos", "Frutos secos", "Sin alérgenos"]),
    "weight_grams": lambda: _rand_numeric(50, 2000),
    "profit_margin_pct": lambda: _rand_float(20, 80, 1),
    "seasonal_item": lambda: _rand_choice([True, False]),
    "custom_order_available": lambda: _rand_choice([True, False]),
    "decoration_level": lambda: _rand_choice(["Básico", "Intermedio", "Avanzado", "Personalizado"]),
    "difficulty_level": lambda: _rand_choice(["Fácil", "Medio", "Difícil", "Experto"]),
    "equipment_required": lambda: _rand_choice(["Horno básico", "Batidora", "Moldes especiales", "Equipo decoración", "Horno especializado"]),
    "ingredient_category": lambda: _rand_choice(["Harinas", "Azúcares", "Grasas", "Lácteos", "Conservantes", "Saborizantes"]),
    "ingredient_name": lambda: _rand_choice([
        "Harina 000", "Harina Leudante", "Azúcar Blanca", "Mantequilla", "Huevos", 
        "Levadura Fresca", "Sal Fina", "Vainilla", "Chocolate", "Crema de Leche",
        "Queso Crema", "Nueces", "Almendras", "Coco Rallado", "Miel"
    ]),
    "unit_of_measure": lambda: _rand_choice(["kg", "litros", "unidades", "gramos", "ml"]),
    "minimum_stock_level": lambda: _rand_numeric(5, 50),
    "maximum_stock_level": lambda: _rand_numeric(100, 500),
    "current_stock_quantity": lambda: _rand_numeric(10, 300),
    "expiration_tracking_required": lambda: _rand_choice([True, False]),
    "storage_temperature": lambda: _rand_choice(["Ambiente", "2-8°C", "-18°C", "Seco"]),
    "organic_certified": lambda: _rand_choice([True, False]),
    "allergen_category": lambda: _rand_choice(["Gluten", "Lactosa", "Huevos", "Frutos secos", "Ninguno"]),
    "substitution_available": lambda: _rand_choice([True, False]),
    "seasonal_availability": lambda: _rand_choice([True, False]),
    "import_domestic": lambda: _rand_choice(["Importado", "Nacional", "Local"]),
    "quality_grade": lambda: _rand_choice(["Premium", "Estándar", "Económico"]),
    "batch_number": lambda: f"LOTE{_rand_numeric(1000, 9999)}",
    "quantity_produced": lambda: _rand_numeric(10, 500),
    "quantity_sold": lambda: _rand_numeric(5, 450),
    "quantity_waste": lambda: _rand_numeric(0, 50),
    "production_start_time": lambda: f"{_rand_numeric(6, 18)}:{_rand_numeric(0, 59):02d}",
    "production_end_time": lambda: f"{_rand_numeric(7, 22)}:{_rand_numeric(0, 59):02d}",
    "baker_staff_id": lambda: _rand_numeric(100, 999),
    "oven_used": lambda: _rand_choice(["Horno 1", "Horno 2", "Horno Industrial", "Horno Especializado"]),
    "temperature_celsius": lambda: _rand_numeric(150, 250),
    "humidity_percentage": lambda: _rand_float(40, 80, 1),
    "quality_score": lambda: _rand_numeric(1, 10),
    "cost_materials": lambda: _rand_float(5, 100, 2),
    "cost_labor": lambda: _rand_float(10, 200, 2),
    "energy_cost": lambda: _rand_float(2, 50, 2),
    "total_production_cost": lambda: _rand_float(20, 400, 2),
    "revenue_generated": lambda: _rand_float(30, 800, 2),
    "profit_loss": lambda: _rand_float(-50, 400, 2),
    "customer_type": lambda: _rand_choice(["Minorista", "Mayorista", "Institucional", "Individual"]),
    "sale_time": lambda: f"{_rand_numeric(7, 20)}:{_rand_numeric(0, 59):02d}",
    "delivery_pickup": lambda: _rand_choice(["Entrega", "Recogida", "En tienda"]),
    "special_occasion": lambda: _rand_choice(["Cumpleaños", "Boda", "Graduación", "Ninguna", "Corporativo"]),
    "customer_satisfaction": lambda: _rand_numeric(1, 10),
    "repeat_customer": lambda: _rand_choice([True, False]),
    "promotional_sale": lambda: _rand_choice([True, False]),
    
    # Micronegocios Especializados - Ferretería
    "product_subcategory": lambda: _rand_choice(["Tornillería", "Electricidad", "Plomería", "Jardinería", "Pintura"]),
    "hardware_product_name": lambda: _rand_choice([
        "Tornillos Autorroscantes", "Cable Eléctrico", "Tubería PVC", "Martillo", "Destornillador",
        "Pintura Látex", "Cemento Contacto", "Lija", "Candado", "Bisagras",
        "Interruptor", "Llave Inglesa", "Manguera", "Taladro", "Clavos"
    ]),
    "model_number": lambda: f"MOD-{_rand_numeric(1000, 9999)}",
    "markup_percentage": lambda: _rand_float(20, 100, 1),
    "reorder_point": lambda: _rand_numeric(10, 100),
    "lead_time_days": lambda: _rand_numeric(1, 30),
    "warranty_months": lambda: _rand_choice([0, 6, 12, 24, 36]),
    "weight_kg": lambda: _rand_float(0.1, 50.0, 2),
    "dimensions_cm": lambda: f"{_rand_numeric(5, 100)}x{_rand_numeric(5, 100)}x{_rand_numeric(5, 100)}",
    "material_type": lambda: _rand_choice(["Metal", "Plástico", "Madera", "Cerámica", "Compuesto"]),
    "usage_category": lambda: _rand_choice(["Profesional", "Doméstico", "Industrial", "Especializado"]),
    "safety_certification": lambda: _rand_choice(["CE", "ISO", "UL", "ANSI", "Ninguna"]),
    "environmental_rating": lambda: _rand_choice(["A", "B", "C", "D", "No aplica"]),
    "bulk_discount_available": lambda: _rand_choice([True, False]),
    "supplier_name": lambda: _rand_choice([
        "Ferretería Central", "Distribuidora Norte", "Suministros Sur", "Importadora Este",
        "Comercial Oeste", "Proveedora Nacional", "Distribuciones Locales"
    ]),
    "contact_person": lambda: _fake_or("Contacto Proveedor", "name"),
    "payment_terms": lambda: _rand_choice(["30 días", "60 días", "Contado", "15 días"]),
    "credit_limit": lambda: _rand_float(1000, 50000, 2),
    "delivery_frequency": lambda: _rand_choice(["Semanal", "Quincenal", "Mensual", "Bajo demanda"]),
    "minimum_order_amount": lambda: _rand_float(100, 5000, 2),
    "discount_percentage": lambda: _rand_float(5, 25, 1),
    "reliability_score": lambda: _rand_numeric(1, 10),
    "quality_rating": lambda: _rand_numeric(1, 10),
    "delivery_performance": lambda: _rand_float(70, 100, 1),
    "product_categories_supplied": lambda: _rand_choice(["Herramientas", "Electricidad", "Plomería", "Múltiples"]),
    "contract_expiry_date": lambda: _rand_date(365),
    "transaction_type": lambda: _rand_choice(["Entrada", "Salida", "Ajuste", "Devolución"]),
    "quantity_change": lambda: _rand_numeric(-100, 100),
    "reason_code": lambda: _rand_choice(["Compra", "Venta", "Ajuste", "Devolución", "Merma"]),
    "purchase_order_id": lambda: _rand_numeric(10000, 99999),
    "lot_batch_number": lambda: f"LOTE{_rand_numeric(1000, 9999)}",
    "location_warehouse": lambda: _rand_choice(["Almacén A", "Almacén B", "Mostrador", "Bodega"]),
    "inventory_status": lambda: _rand_choice(["Disponible", "Reservado", "Dañado", "Obsoleto"]),
    "quality_check_passed": lambda: _rand_choice([True, False]),
    "project_type": lambda: _rand_choice(["Construcción", "Reparación", "Mantenimiento", "Jardinería"]),
    "delivery_required": lambda: _rand_choice([True, False]),
    "installation_service": lambda: _rand_choice([True, False]),
    "warranty_sold": lambda: _rand_choice([True, False]),
    "referral_source": lambda: _rand_choice(["Recomendación", "Internet", "Publicidad", "Cliente habitual"]),
    
    # Micronegocios Especializados - Laboratorio
    "test_name": lambda: _rand_choice([
        "Hemograma Completo", "Glucosa", "Colesterol Total", "Creatinina", "Urea",
        "Triglicéridos", "TSH", "PSA", "Examen de Orina", "Hepatitis B",
        "VIH", "Cultivo de Garganta", "Perfil Lipídico", "HbA1c", "Vitamina D"
    ]),
    "test_category": lambda: _rand_choice(["Hematología", "Química clínica", "Microbiología", "Inmunología", "Urianálisis"]),
    "test_type": lambda: _rand_choice(["Rutina", "Urgente", "Especializado", "Perfil"]),
    "specimen_type": lambda: _rand_choice(["Sangre", "Orina", "Heces", "Saliva", "Tejido"]),
    "collection_method": lambda: _rand_choice(["Venopunción", "Punción capilar", "Muestra espontánea", "Biopsia"]),
    "processing_time_hours": lambda: _rand_float(0.5, 72.0, 1),
    "reference_range_min": lambda: _rand_float(0, 100, 2),
    "reference_range_max": lambda: _rand_float(100, 500, 2),
    "units_measurement": lambda: _rand_choice(["mg/dL", "g/L", "UI/L", "mmol/L", "células/μL"]),
    "equipment_name": lambda: _rand_choice([
        "Analizador Hematológico", "Microscopio", "Centrífuga", "Incubadora", 
        "Espectrofotómetro", "Analizador Químico", "Contador de Células"
    ]),
    "equipment_required": lambda: _rand_choice(["Analizador", "Microscopio", "Centrífuga", "Incubadora", "Espectrofotómetro"]),
    "reagent_required": lambda: _rand_choice(["Kit específico", "Reactivos múltiples", "Colorante", "Buffer"]),
    "certification_level": lambda: _rand_choice(["Básico", "Intermedio", "Avanzado", "Especialista"]),
    "fasting_required": lambda: _rand_choice([True, False]),
    "special_preparation": lambda: _rand_choice(["Ayuno 12h", "Dieta especial", "Suspender medicamentos", "Ninguna"]),
    "critical_value_low": lambda: _rand_float(0, 50, 2),
    "critical_value_high": lambda: _rand_float(200, 1000, 2),
    "turnaround_time_hours": lambda: _rand_numeric(1, 48),
    "quality_control_frequency": lambda: _rand_choice(["Diario", "Por lote", "Semanal", "Mensual"]),
    "equipment_type": lambda: _rand_choice(["Analizador automático", "Manual", "Semi-automático", "Especializado"]),
    "manufacturer": lambda: _rand_choice(["Roche", "Abbott", "Siemens", "Beckman", "Sysmex"]),
    "serial_number": lambda: f"SN{_rand_numeric(100000, 999999)}",
    "purchase_date": lambda: _rand_date(1825),
    "warranty_expiry": lambda: _rand_date(365),
    "last_calibration_date": lambda: _rand_date(90),
    "next_calibration_due": lambda: _rand_date(30),
    "maintenance_frequency": lambda: _rand_choice(["Diario", "Semanal", "Mensual", "Trimestral"]),
    "operational_status": lambda: _rand_choice(["Operativo", "Mantenimiento", "Fuera de servicio", "Calibración"]),
    "location_lab": lambda: _rand_choice(["Lab 1", "Lab 2", "Urgencias", "Especialidades"]),
    "cost_per_hour": lambda: _rand_float(10, 200, 2),
    "technician_certification_required": lambda: _rand_choice([True, False]),
    "daily_capacity": lambda: _rand_numeric(50, 1000),
    "accuracy_percentage": lambda: _rand_float(95, 99.9, 1),
    "precision_level": lambda: _rand_choice(["Alta", "Media", "Estándar"]),
    "patient_id": lambda: _rand_numeric(100000, 999999),
    "order_date": lambda: _rand_date(30),
    "collection_date": lambda: _rand_date(7),
    "processing_date": lambda: _rand_date(3),
    "report_date": lambda: _rand_date(1),
    "technician_id": lambda: _rand_numeric(1000, 9999),
    "specimen_quality": lambda: _rand_choice(["Excelente", "Buena", "Aceptable", "Rechazada"]),
    "test_result_value": lambda: _rand_float(1, 500, 2),
    "test_result_status": lambda: _rand_choice(["Normal", "Anormal", "Crítico", "Indeterminado"]),
    "reference_range_status": lambda: _rand_choice(["Dentro", "Bajo", "Alto", "Crítico"]),
    "critical_value_flag": lambda: _rand_choice([True, False]),
    "repeat_required": lambda: _rand_choice([True, False]),
    "quality_control_passed": lambda: _rand_choice([True, False]),
    "processing_time_actual": lambda: _rand_float(0.5, 24.0, 1),
    "cost_actual": lambda: _rand_float(5, 200, 2),
    "patient_satisfaction": lambda: _rand_numeric(1, 10),
    "doctor_feedback": lambda: _rand_choice(["Excelente", "Bueno", "Regular", "Malo"]),
    "shift_type": lambda: _rand_choice(["Mañana", "Tarde", "Noche", "24 horas"]),
    "staff_count": lambda: _rand_numeric(2, 15),
    "tests_processed": lambda: _rand_numeric(50, 500),
    "specimens_received": lambda: _rand_numeric(60, 600),
    "specimens_rejected": lambda: _rand_numeric(0, 50),
    "equipment_downtime_minutes": lambda: _rand_numeric(0, 480),
    "quality_control_tests": lambda: _rand_numeric(5, 50),
    "turnaround_time_avg": lambda: _rand_float(2, 24, 1),
    "customer_complaints": lambda: _rand_numeric(0, 10),
    "revenue_daily": lambda: _rand_float(1000, 20000, 2),
    "costs_daily": lambda: _rand_float(500, 15000, 2),
    "efficiency_score": lambda: _rand_float(70, 100, 1),
    
    # Micronegocios Especializados - Jabonería
    "soap_product_name": lambda: _rand_choice([
        "Jabón de Lavanda", "Jabón de Rosa", "Jabón de Miel", "Jabón de Avena",
        "Jabón Artesanal", "Jabón de Coco", "Jabón Exfoliante", "Jabón Hidratante",
        "Jabón Antibacterial", "Jabón de Glicerina", "Jabón de Carbón", "Jabón de Té Verde"
    ]),
    "fragrance_type": lambda: _rand_choice(["Lavanda", "Rosa", "Cítrico", "Menta", "Vainilla", "Sin fragancia"]),
    "skin_type_target": lambda: _rand_choice(["Todo tipo", "Piel seca", "Piel grasa", "Piel sensible", "Piel mixta"]),
    "ingredients_natural_pct": lambda: _rand_float(50, 100, 1),
    "cruelty_free": lambda: _rand_choice([True, False]),
    "ph_level": lambda: _rand_float(5.5, 9.0, 1),
    "packaging_type": lambda: _rand_choice(["Barra", "Líquido", "Espuma", "Gel", "Polvo"]),
    "shelf_life_months": lambda: _rand_numeric(6, 36),
    "seasonal_demand": lambda: _rand_choice([True, False]),
    "custom_formulation": lambda: _rand_choice([True, False]),
    "gift_packaging_available": lambda: _rand_choice([True, False]),
    "wholesale_available": lambda: _rand_choice([True, False]),
    "retail_channel": lambda: _rand_choice(["Tienda física", "Online", "Mayorista", "Ferias"]),
    "age_group_target": lambda: _rand_choice(["Niños", "Adolescentes", "Adultos", "Tercera edad", "Todas las edades"]),
    "ingredient_type": lambda: _rand_choice(["Base", "Fragancia", "Colorante", "Conservante", "Activo"]),
    "origin_country": lambda: _rand_choice(["Local", "Francia", "España", "Brasil", "India"]),
    "fair_trade_certified": lambda: _rand_choice([True, False]),
    "cost_per_kg": lambda: _rand_float(10, 500, 2),
    "minimum_order_kg": lambda: _rand_numeric(1, 50),
    "concentration_percentage": lambda: _rand_float(0.1, 50.0, 2),
    "sustainability_rating": lambda: _rand_choice(["A", "B", "C", "D", "No calificado"]),
    "alternative_available": lambda: _rand_choice([True, False]),
    "batch_size_units": lambda: _rand_numeric(50, 1000),
    "curing_time_days": lambda: _rand_numeric(7, 60),
    "ph_test_result": lambda: _rand_float(5.0, 9.5, 1),
    "hardness_test_result": lambda: _rand_choice(["Suave", "Medio", "Duro", "Muy duro"]),
    "fragrance_intensity": lambda: _rand_choice(["Suave", "Medio", "Intenso", "Muy intenso"]),
    "color_consistency": lambda: _rand_choice(["Uniforme", "Ligeramente irregular", "Irregular"]),
    "production_time_hours": lambda: _rand_float(2, 12, 1),
    "yield_percentage": lambda: _rand_float(85, 98, 1),
    "waste_percentage": lambda: _rand_float(2, 15, 1),
    "defect_count": lambda: _rand_numeric(0, 50),
    "approved_units": lambda: _rand_numeric(40, 950),
    "sale_channel": lambda: _rand_choice(["Tienda", "Online", "Feria", "Mayorista", "Catálogo"]),
    "shipping_cost": lambda: _rand_float(0, 50, 2),
    "gift_purchase": lambda: _rand_choice([True, False]),
    "seasonal_promotion": lambda: _rand_choice([True, False]),
    "packaging_preference": lambda: _rand_choice(["Estándar", "Eco-friendly", "De lujo", "Minimalista"]),
    "delivery_method": lambda: _rand_choice(["Domicilio", "Punto de recogida", "Tienda", "Correo"]),
    "customer_feedback_score": lambda: _rand_numeric(1, 10),
    
    # Creator Intelligence - Plataformas y Canales
    "platform_name": lambda: _rand_choice(["YouTube", "TikTok", "Instagram", "Twitter", "Facebook", "LinkedIn"]),
    "api_source": lambda: _rand_choice(["YouTube Data API v3", "TikTok Business API", "Instagram Basic Display API", "Meta Graph API"]),
    "url_base": lambda: _rand_choice(["https://www.googleapis.com/youtube/v3", "https://open-api.tiktok.com", "https://graph.instagram.com"]),
    "tz_default": lambda: _rand_choice(["UTC", "America/New_York", "America/Los_Angeles", "Europe/London", "America/Mexico_City"]),
    "data_freshness_sla": lambda: _rand_choice(["24h", "12h", "6h", "1h", "real-time"]),
    "handle": lambda: f"@{_fake_or('handle', 'user_name').lower().replace('.', '').replace(' ', '')}",
    "channel_name": lambda: _rand_choice([
        "Tech Reviews Pro", "Daily Life Vlogs", "Gaming Central", "Beauty Secrets", "Fitness Journey",
        "Cooking Adventures", "Travel Diaries", "Music Covers", "Comedy Sketches", "Educational Hub",
        "Art Tutorials", "Business Tips", "Health & Wellness", "Fashion Forward", "DIY Projects"
    ]),
    "niche_topic": lambda: _rand_choice([
        "Technology", "Lifestyle", "Gaming", "Beauty", "Fitness", "Food", "Travel", "Music", 
        "Comedy", "Education", "Art", "Business", "Health", "Fashion", "DIY", "Science", "Sports"
    ]),
    "lang": lambda: _rand_choice(["es", "en", "pt", "fr", "de", "it", "ja", "ko"]),
    "subs_current": lambda: _rand_numeric(100, 10000000),
    "join_date": lambda: _rand_date(2000),
    
    # Creator Intelligence - Contenido
    "content_type": lambda: _rand_choice(["video", "short", "reel", "post", "story", "live"]),
    "title": lambda: _rand_choice([
        "10 Tips que CAMBIARÁN tu vida", "El SECRETO que nadie te cuenta", "Reaccionando a...", 
        "Tutorial COMPLETO paso a paso", "Mi RUTINA diaria REAL", "Lo que NADIE esperaba",
        "PROBANDO productos VIRALES", "La VERDAD sobre...", "Cómo conseguir... en 30 días",
        "EPIC FAIL compilación", "Antes vs Después INCREÍBLE", "Top 5 mejores...",
        "RESPONDIENDO a sus preguntas", "Detrás de cámaras", "Mi mayor ERROR"
    ]),
    "title_tokens_json": lambda: _rand_choice([
        '["tips", "cambiarán", "vida"]', '["secreto", "nadie", "cuenta"]', 
        '["tutorial", "completo", "paso"]', '["rutina", "diaria", "real"]'
    ]),
    "description_len": lambda: _rand_numeric(50, 5000),
    "duration_s": lambda: _rand_numeric(15, 3600),
    "aspect_ratio": lambda: _rand_choice(["16:9", "9:16", "1:1", "4:3", "21:9"]),
    "hashtags_json": lambda: _rand_choice([
        '["#viral", "#trending", "#fyp"]', '["#tutorial", "#howto", "#tips"]',
        '["#lifestyle", "#daily", "#vlog"]', '["#gaming", "#gameplay", "#gamer"]',
        '["#beauty", "#makeup", "#skincare"]', '["#food", "#recipe", "#cooking"]'
    ]),
    "tags_json": lambda: _rand_choice([
        '["entertainment", "trending"]', '["educational", "tutorial"]',
        '["lifestyle", "personal"]', '["technology", "review"]'
    ]),
    "publish_ts_utc": lambda: _rand_datetime_utc(365),
    "collab_flag": lambda: _rand_choice([True, False]),
    "series_id": lambda: _rand_numeric(1000, 9999) if _rand_choice([True, False]) else None,
    "evergreen_flag": lambda: _rand_choice([True, False]),
    
    # Creator Intelligence - Taxonomía y Hashtags
    "level1": lambda: _rand_choice(["Entertainment", "Education", "Technology", "Lifestyle", "Business", "Arts", "Sports"]),
    "level2": lambda: _rand_choice(["Gaming", "Comedy", "Music", "Tutorials", "Reviews", "Vlogs", "News"]),
    "level3": lambda: _rand_choice(["Mobile Games", "PC Gaming", "Stand-up", "Music Covers", "Tech Reviews", "Daily Life"]),
    "keywords_json": lambda: _rand_choice([
        '["gaming", "gameplay", "review"]', '["tutorial", "howto", "guide"]',
        '["comedy", "funny", "humor"]', '["music", "cover", "song"]'
    ]),
    "hashtag_text": lambda: _rand_choice([
        "#fyp", "#viral", "#trending", "#foryou", "#explore", "#reels", "#shorts",
        "#tutorial", "#tips", "#howto", "#diy", "#lifestyle", "#daily", "#vlog",
        "#gaming", "#gamer", "#gameplay", "#streamer", "#esports",
        "#beauty", "#makeup", "#skincare", "#fashion", "#style",
        "#food", "#recipe", "#cooking", "#foodie", "#delicious",
        "#fitness", "#workout", "#health", "#gym", "#motivation",
        "#travel", "#adventure", "#explore", "#nature", "#photography"
    ]),
    
    # Creator Intelligence - Thumbnails y Títulos
    "variant_code": lambda: _rand_choice(["A", "B", "C", "D", "E"]),
    "style": lambda: _rand_choice(["meme", "clean", "face", "object", "text", "dramatic", "minimal"]),
    "main_color": lambda: _rand_choice(["red", "blue", "yellow", "green", "orange", "purple", "black", "white"]),
    "text_len": lambda: _rand_numeric(0, 100),
    "face_detected_flag": lambda: _rand_choice([True, False]),
    "sentiment": lambda: _rand_choice(["positive", "negative", "neutral", "excited", "curious", "urgent"]),
    "word_count": lambda: _rand_numeric(3, 20),
    "clickbait_score": lambda: _rand_float(0, 100, 1),
    
    # Creator Intelligence - Experimentos
    "objective": lambda: _rand_choice(["CTR", "retention", "conversion", "engagement", "watch_time", "subscribers"]),
    "hypothesis": lambda: _rand_choice([
        "Thumbnails con caras aumentan CTR en 15%",
        "Títulos con números mejoran clicks en 20%",
        "Videos de 8-12 min tienen mejor retención",
        "Publicar en horarios peak aumenta views",
        "Colaboraciones incrementan suscriptores"
    ]),
    "start_ts_utc": lambda: _rand_datetime_utc(30),
    "end_ts_utc": lambda: _rand_datetime_utc(-30),
    "owner": lambda: _fake_or("owner", "name"),
    
    # Creator Intelligence - Scheduling
    "dow": lambda: _rand_choice(["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]),
    "hour_local": lambda: _rand_numeric(0, 23),
    "is_peak_flag": lambda: _rand_choice([True, False]),
    "historical_avg_ctr_pct": lambda: _rand_float(2, 15, 2),
    "historical_watch_time_s": lambda: _rand_numeric(30, 600),
    
    # Creator Intelligence - Métricas de Performance
    "impressions": lambda: _rand_numeric(1000, 10000000),
    "views": lambda: _rand_numeric(100, 5000000),
    "unique_viewers": lambda: _rand_numeric(80, 3000000),
    "avg_view_duration_s": lambda: _rand_numeric(15, 600),
    "avg_percentage_viewed_pct": lambda: _rand_float(20, 80, 1),
    "retention_30s_pct": lambda: _rand_float(40, 90, 1),
    "retention_60s_pct": lambda: _rand_float(20, 70, 1),
    "retention_50pct_mark_s": lambda: _rand_numeric(30, 300),
    "watch_time_min": lambda: _rand_numeric(10, 100000),
    "likes": lambda: _rand_numeric(10, 500000),
    "comments": lambda: _rand_numeric(5, 50000),
    "shares": lambda: _rand_numeric(2, 25000),
    "saves": lambda: _rand_numeric(1, 10000),
    "dislikes": lambda: _rand_numeric(0, 5000),
    "ctr_thumb_pct": lambda: _rand_float(2, 15, 2),
    "end_screen_clicks": lambda: _rand_numeric(0, 5000),
    "card_clicks": lambda: _rand_numeric(0, 2000),
    "subs_gained": lambda: _rand_numeric(0, 10000),
    "subs_lost": lambda: _rand_numeric(0, 1000),
    "revenue_ad_usd": lambda: _rand_float(0.5, 5000, 2),
    "rpm_usd": lambda: _rand_float(0.5, 10, 2),
    "cpm_usd": lambda: _rand_float(0.1, 5, 2),
    
    # Creator Intelligence - Retención y Fuentes
    "second_mark": lambda: _rand_numeric(0, 600),
    "viewers_remaining_pct": lambda: _rand_float(10, 100, 1),
    "drop_delta_pct": lambda: _rand_float(-20, 5, 1),
    "key_moment_flag": lambda: _rand_choice(["hook", "valley", "peak", "normal"]),
    "source": lambda: _rand_choice(["search", "home", "suggested", "shorts", "external", "playlist", "browse", "notifications"]),
    "ctr_pct": lambda: _rand_float(1, 20, 2),
    
    # Creator Intelligence - Audiencia
    "subs_total": lambda: _rand_numeric(100, 10000000),
    "returning_viewers": lambda: _rand_numeric(50, 1000000),
    "new_viewers": lambda: _rand_numeric(20, 500000),
    "gender_mix_json": lambda: _rand_choice([
        '{"male": 65, "female": 35}', '{"male": 45, "female": 55}',
        '{"male": 50, "female": 50}', '{"male": 40, "female": 60}'
    ]),
    "age_brackets_json": lambda: _rand_choice([
        '{"13-17": 15, "18-24": 35, "25-34": 30, "35-44": 15, "45+": 5}',
        '{"13-17": 25, "18-24": 40, "25-34": 25, "35-44": 8, "45+": 2}',
        '{"13-17": 5, "18-24": 20, "25-34": 40, "35-44": 25, "45+": 10}'
    ]),
    "geo_top_json": lambda: _rand_choice([
        '{"US": 35, "MX": 25, "ES": 15, "AR": 10, "CO": 8, "other": 7}',
        '{"MX": 40, "US": 20, "ES": 15, "AR": 12, "PE": 8, "other": 5}',
        '{"ES": 45, "MX": 20, "AR": 15, "US": 10, "CO": 5, "other": 5}'
    ]),
    "device_mix_json": lambda: _rand_choice([
        '{"mobile": 75, "desktop": 20, "tablet": 5}',
        '{"mobile": 85, "desktop": 12, "tablet": 3}',
        '{"mobile": 65, "desktop": 30, "tablet": 5}'
    ]),
    
    # Creator Intelligence - Testing y Pacing
    "hour_since_publish": lambda: _rand_numeric(0, 48),
    "uplift_ctr_pct": lambda: _rand_float(-10, 50, 1),
    "winner_flag": lambda: _rand_choice([True, False]),
    
    # Creator Intelligence - NLP y Comentarios
    "comments_count": lambda: _rand_numeric(5, 50000),
    "sentiment_avg": lambda: _rand_float(-1, 1, 2),
    "topics_json": lambda: _rand_choice([
        '["positive_feedback", "requests", "questions"]',
        '["criticism", "suggestions", "praise"]',
        '["funny_reactions", "memes", "appreciation"]'
    ]),
    "toxicity_rate_pct": lambda: _rand_float(0, 15, 1),
    "questions_count": lambda: _rand_numeric(0, 500),
    "suggestions_count": lambda: _rand_numeric(0, 200),
    
    # Creator Intelligence - Scheduling y Competencia
    "posted_ts_local": lambda: _rand_datetime_local(),
    "delay_min": lambda: _rand_numeric(-30, 120),
    "within_peak_flag": lambda: _rand_choice([True, False]),
    "competitor_content_id": lambda: _rand_numeric(100000, 999999),
    "competitor_channel": lambda: _rand_choice([
        "TechReviewer", "LifestyleGuru", "GamingPro", "BeautyExpert", "FoodieChannel",
        "TravelAddict", "FitnessCoach", "MusicMaker", "ComedyCentral", "EducationHub"
    ]),
    "velocity_views_24h": lambda: _rand_numeric(1000, 1000000),
    "ctr_proxy_pct": lambda: _rand_float(2, 12, 1),
    "avg_duration_proxy_s": lambda: _rand_numeric(30, 900),
    
    # Creator Intelligence - Recomendaciones y Reportes
    "category": lambda: _rand_choice(["hook", "title", "thumbnail", "format", "length", "hashtag", "schedule", "content"]),
    "action_text": lambda: _rand_choice([
        "Mejorar hook en primeros 5 segundos",
        "Usar thumbnails con caras expresivas",
        "Optimizar títulos con números específicos",
        "Reducir duración a 8-12 minutos",
        "Publicar en horarios de mayor audiencia",
        "Incluir hashtags trending del nicho",
        "Agregar llamadas a acción más claras"
    ]),
    "expected_uplift_metric": lambda: _rand_choice(["CTR", "watch_time", "retention", "engagement", "subscribers"]),
    "expected_uplift_pct": lambda: _rand_float(5, 50, 1),
    "priority": lambda: _rand_choice(["high", "medium", "low", "critical"]),
    "due_date": lambda: _rand_date(30),
    "report_type": lambda: _rand_choice(["diagnosis", "guide", "recommendations", "experiment_results", "monthly_review"]),
    "storage_uri": lambda: f"s3://creator-intelligence/reports/{_rand_numeric(1000, 9999)}.pdf",
    "summary_md": lambda: "## Resumen Ejecutivo\n\nAnálisis de performance del canal...",
    
    # Creator Intelligence - Gestión de Proyectos
    "client_id": lambda: _rand_numeric(1000, 9999),
    "scope": lambda: _rand_choice(["diagnosis", "retainer", "audit", "optimization", "strategy"]),
    "pricing_model": lambda: _rand_choice(["hourly", "monthly", "project", "performance"]),
    "milestone_date": lambda: _rand_date(90),
    "milestone_name": lambda: _rand_choice([
        "Initial Assessment", "Strategy Development", "Implementation Phase 1", 
        "Mid-point Review", "Optimization Round", "Final Delivery"
    ]),
    "deliverable_type": lambda: _rand_choice(["diagnosis", "guide", "recommendations", "report", "strategy"]),
    "delivered_date": lambda: _rand_date(30),
    "acceptance_status": lambda: _rand_choice(["pending", "accepted", "revision_requested", "approved"]),
    "meeting_ts_utc": lambda: _rand_datetime_utc(7),
    "attendees_json": lambda: '["client_lead", "creator_manager", "analyst", "strategist"]',
    "agenda_md": lambda: "## Agenda\n1. Review metrics\n2. Discuss recommendations\n3. Plan next steps",
    "outcomes_md": lambda: "## Outcomes\n- Agreed on CTR optimization strategy\n- Set targets for next month",
    "next_actions_json": lambda: '["Implement new thumbnail strategy", "A/B test titles", "Schedule follow-up"]',
    
    # Creator Intelligence - Raw Data
    "payload_json": lambda: '{"metrics": {"views": 12500, "ctr": 8.5}, "timestamp": "2024-01-01T12:00:00Z"}',
    "pulled_ts_utc": lambda: _rand_datetime_utc(1),
    "api_endpoint": lambda: _rand_choice([
        "/youtube/v3/analytics", "/tiktok/v1/business/insights", 
        "/instagram/v1/insights", "/facebook/v12.0/insights"
    ]),
    "rate_limit_ms": lambda: _rand_numeric(100, 5000),
    "schema_version": lambda: _rand_choice(["v1.0", "v1.1", "v2.0", "v2.1"]),
    
    # Campos common/metadata 
    "pii_sensitivity": lambda: _rand_choice(["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"]),
    "source_table": lambda: f"table_{_rand_numeric(100, 999)}",
    "source_system": lambda: f"SYS_{_rand_choice(['PROD', 'STG', 'DEV'])}",
    "geo_region": lambda: _rand_choice(["North", "South", "East", "West", "Central"]),
    "geo_lat": lambda: _rand_float(-90, 90, 6),
    "geo_lon": lambda: _rand_float(-180, 180, 6),
    "fx_rate_to_usd": lambda: _rand_float(0.5, 2.0, 4),
    "notes": lambda: _fake_or("System generated note", "sentence"),
    "valid_from_utc": lambda: _rand_date(1000),
    "valid_to_utc": lambda: _rand_date(200),
    "created_at_utc": lambda: _rand_date(800),
}

import hashlib
def hashlib_sha(seed: str) -> str:
    return hashlib.sha256(seed.encode()).hexdigest()[:16]

# Variable global para contexto de tabla
_CURRENT_TABLE_CONTEXT = None

def set_table_context(table_name: str):
    """Establece el contexto de la tabla actual para generación específica."""
    global _CURRENT_TABLE_CONTEXT
    _CURRENT_TABLE_CONTEXT = table_name

def _resolve_field(name: str) -> Any:
    global _CURRENT_TABLE_CONTEXT
    
    # Resolución específica por contexto de tabla
    if _CURRENT_TABLE_CONTEXT and name == "product_name":
        if "bakery" in _CURRENT_TABLE_CONTEXT:
            return _rand_choice([
                "Pan de Molde", "Croissant", "Baguette", "Pan Integral", "Torta de Chocolate", 
                "Empanadas", "Galletas de Avena", "Muffins de Arándanos", "Pan Dulce", "Facturas",
                "Medialunas", "Pan de Centeno", "Torta Tres Leches", "Cupcakes", "Pan Francés",
                "Rosca de Reyes", "Donas Glaseadas", "Pan de Ajo", "Tartaletas", "Bizcochuelo"
            ])
        elif "hardware" in _CURRENT_TABLE_CONTEXT:
            return _rand_choice([
                "Tornillos Autorroscantes", "Cable Eléctrico", "Tubería PVC", "Martillo", "Destornillador",
                "Pintura Látex", "Cemento Contacto", "Lija", "Candado", "Bisagras",
                "Interruptor", "Llave Inglesa", "Manguera", "Taladro", "Clavos"
            ])
        elif "soap" in _CURRENT_TABLE_CONTEXT:
            return _rand_choice([
                "Jabón de Lavanda", "Jabón de Rosa", "Jabón de Miel", "Jabón de Avena",
                "Jabón Artesanal", "Jabón de Coco", "Jabón Exfoliante", "Jabón Hidratante",
                "Jabón Antibacterial", "Jabón de Glicerina", "Jabón de Carbón", "Jabón de Té Verde"
            ])
    
    if _CURRENT_TABLE_CONTEXT and name == "test_name" and "lab" in _CURRENT_TABLE_CONTEXT:
        return _rand_choice([
            "Hemograma Completo", "Glucosa", "Colesterol Total", "Creatinina", "Urea",
            "Triglicéridos", "TSH", "PSA", "Examen de Orina", "Hepatitis B",
            "VIH", "Cultivo de Garganta", "Perfil Lipídico", "HbA1c", "Vitamina D"
        ])
    
    if _CURRENT_TABLE_CONTEXT and name == "equipment_name" and "lab" in _CURRENT_TABLE_CONTEXT:
        return _rand_choice([
            "Analizador Hematológico", "Microscopio", "Centrífuga", "Incubadora", 
            "Espectrofotómetro", "Analizador Químico", "Contador de Células"
        ])
    
    if _CURRENT_TABLE_CONTEXT and name == "equipment_required":
        if "bakery" in _CURRENT_TABLE_CONTEXT:
            return _rand_choice(["Horno básico", "Batidora", "Moldes especiales", "Equipo decoración", "Horno especializado"])
        elif "hardware" in _CURRENT_TABLE_CONTEXT:
            return _rand_choice(["Herramientas básicas", "Equipo especializado", "Maquinaria pesada", "Instrumentos medición"])
        elif "lab" in _CURRENT_TABLE_CONTEXT:
            return _rand_choice(["Analizador", "Microscopio", "Centrífuga", "Incubadora", "Espectrofotómetro"])
        elif "soap" in _CURRENT_TABLE_CONTEXT:
            return _rand_choice(["Mezcladora", "Moldes", "Caldero", "Prensa", "Equipo curado"])
    
    # Coincidencia exacta primero
    if name in GENERAL_MAP:
        return GENERAL_MAP[name]()
    
    # Coincidencia por sufijos comunes
    if name.endswith("_id") and "*_id" in GENERAL_MAP:
        return GENERAL_MAP["*_id"]()
    if name.endswith("_id_hash") and "*_id_hash" in GENERAL_MAP:
        return GENERAL_MAP["*_id_hash"]()
    if name.endswith("_code") and "*_code" in GENERAL_MAP:
        return GENERAL_MAP["*_code"]()
    if name.endswith("_number") and "*_number" in GENERAL_MAP:
        return GENERAL_MAP["*_number"]()
    
    # Heurísticas por contenido de nombre (palabras clave)
    name_lower = name.lower()
    
    # Fechas
    if any(kw in name_lower for kw in ["date", "time", "timestamp"]):
        return _rand_date(365)
    
    # Precios y cantidades
    if any(kw in name_lower for kw in ["price", "cost", "amount", "total", "balance", "salary"]):
        return _rand_float(1, 1000, 2)
    
    # Cantidades enteras
    if any(kw in name_lower for kw in ["quantity", "qty", "count", "hours", "days", "points"]):
        return _rand_numeric(1, 100)
    
    # Nombres
    if any(kw in name_lower for kw in ["name", "title", "description"]):
        return _fake_or(f"Generic {name}", "word")
    
    # Flags y booleanos
    if any(kw in name_lower for kw in ["flag", "active", "enabled", "voluntary"]):
        return _rand_choice([True, False])
    
    # Status y tipos
    if any(kw in name_lower for kw in ["status", "type", "category", "method", "reason"]):
        return _rand_choice(["Active", "Pending", "Closed", "Type_A", "Category_1"])
    
    # Emails
    if "email" in name_lower:
        return _fake_or("example@company.com", "email")
    
    # Teléfonos
    if "phone" in name_lower:
        return _fake_or("+1234567890", "phone_number")
    
    # Fallback para evitar None
    return f"value_{_rand_numeric(1, 9999)}"

def generate_row(field_names: list[str]) -> Dict[str, Any]:
    row: Dict[str, Any] = {}
    for f in field_names:
        row[f] = _resolve_field(f)
    return row
