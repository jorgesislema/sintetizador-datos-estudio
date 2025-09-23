"""
Sistema de Contextos Geográficos para Generación de Datos Sintéticos
Soporta múltiples países y regiones con datos específicos locales
"""
from typing import Dict, List, Any
import random

# ===== CONTEXTOS GEOGRÁFICOS COMPLETOS =====

GEOGRAPHIC_CONTEXTS: Dict[str, Dict[str, Any]] = {
    # ========== LATINOAMÉRICA ==========
    "ecuador": {
        "region": "Latinoamérica",
        "country_code": "EC",
        "currency": "USD",
        "timezone": "America/Guayaquil",
        "phone_format": "+593",
        "postal_code_format": "EC######",
        "cities": [
            "Quito", "Guayaquil", "Cuenca", "Santo Domingo", "Ambato",
            "Portoviejo", "Durán", "Machala", "Loja", "Manta",
            "Riobamba", "Esmeraldas", "Milagro", "Ibarra", "La Libertad"
        ],
        "provinces": [
            "Pichincha", "Guayas", "Azuay", "Manabí", "Tungurahua",
            "Los Ríos", "El Oro", "Loja", "Imbabura", "Chimborazo",
            "Esmeraldas", "Cañar", "Carchi", "Bolivar", "Santa Elena"
        ],
        "streets": [
            "Av. Amazonas", "Av. 10 de Agosto", "Av. Shyris", "Calle Sucre",
            "Av. Naciones Unidas", "Av. República", "Calle Bolívar", "Av. Patria"
        ]
    },
    
    "colombia": {
        "region": "Latinoamérica", 
        "country_code": "CO",
        "currency": "COP",
        "timezone": "America/Bogota",
        "phone_format": "+57",
        "postal_code_format": "######",
        "cities": [
            "Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena",
            "Cúcuta", "Bucaramanga", "Pereira", "Santa Marta", "Ibagué",
            "Pasto", "Manizales", "Neiva", "Villavicencio", "Armenia"
        ],
        "provinces": [
            "Cundinamarca", "Antioquia", "Valle del Cauca", "Atlántico",
            "Bolívar", "Norte de Santander", "Santander", "Risaralda",
            "Magdalena", "Tolima", "Nariño", "Caldas", "Huila"
        ],
        "streets": [
            "Carrera 7", "Avenida Caracas", "Calle 72", "Carrera 15",
            "Avenida Boyacá", "Calle 26", "Carrera 13", "Avenida Chile"
        ]
    },
    
    "mexico": {
        "region": "Latinoamérica",
        "country_code": "MX", 
        "currency": "MXN",
        "timezone": "America/Mexico_City",
        "phone_format": "+52",
        "postal_code_format": "#####",
        "cities": [
            "Ciudad de México", "Guadalajara", "Monterrey", "Puebla", "Tijuana",
            "León", "Juárez", "Torreón", "Querétaro", "San Luis Potosí",
            "Mérida", "Mexicali", "Aguascalientes", "Chihuahua", "Cuernavaca"
        ],
        "provinces": [
            "Ciudad de México", "Jalisco", "Nuevo León", "Puebla", "Baja California",
            "Guanajuato", "Chihuahua", "Coahuila", "Querétaro", "San Luis Potosí",
            "Yucatán", "Aguascalientes", "Morelos", "Veracruz", "Tamaulipas"
        ]
    },
    
    "argentina": {
        "region": "Latinoamérica",
        "country_code": "AR",
        "currency": "ARS", 
        "timezone": "America/Argentina/Buenos_Aires",
        "phone_format": "+54",
        "postal_code_format": "A####AAA",
        "cities": [
            "Buenos Aires", "Córdoba", "Rosario", "Mendoza", "La Plata",
            "Tucumán", "Mar del Plata", "Salta", "Santa Fe", "San Juan",
            "Resistencia", "Neuquén", "Santiago del Estero", "Corrientes", "Posadas"
        ],
        "provinces": [
            "Buenos Aires", "Córdoba", "Santa Fe", "Mendoza", "Tucumán",
            "Entre Ríos", "Salta", "Misiones", "Chaco", "San Juan",
            "Jujuy", "Río Negro", "Formosa", "Neuquén", "Chubut"
        ]
    },
    
    "chile": {
        "region": "Latinoamérica",
        "country_code": "CL",
        "currency": "CLP",
        "timezone": "America/Santiago", 
        "phone_format": "+56",
        "postal_code_format": "#######",
        "cities": [
            "Santiago", "Valparaíso", "Concepción", "La Serena", "Antofagasta",
            "Temuco", "Rancagua", "Talca", "Arica", "Chillán",
            "Iquique", "Los Ángeles", "Puerto Montt", "Valdivia", "Osorno"
        ],
        "provinces": [
            "Santiago", "Valparaíso", "Biobío", "Coquimbo", "Antofagasta",
            "Araucanía", "O'Higgins", "Maule", "Arica y Parinacota", "Ñuble",
            "Tarapacá", "Los Lagos", "Los Ríos", "Atacama", "Aysén"
        ]
    },
    
    "peru": {
        "region": "Latinoamérica",
        "country_code": "PE",
        "currency": "PEN",
        "timezone": "America/Lima",
        "phone_format": "+51", 
        "postal_code_format": "PE#####",
        "cities": [
            "Lima", "Arequipa", "Trujillo", "Chiclayo", "Piura",
            "Iquitos", "Cusco", "Chimbote", "Huancayo", "Tacna",
            "Ica", "Juliaca", "Sullana", "Ayacucho", "Chincha Alta"
        ],
        "provinces": [
            "Lima", "Arequipa", "La Libertad", "Lambayeque", "Piura",
            "Loreto", "Cusco", "Áncash", "Junín", "Tacna",
            "Ica", "Puno", "Ayacucho", "Cajamarca", "Huánuco"
        ]
    },
    
    # ========== EUROPA ==========
    "espana": {
        "region": "Europa",
        "country_code": "ES",
        "currency": "EUR",
        "timezone": "Europe/Madrid",
        "phone_format": "+34",
        "postal_code_format": "#####",
        "cities": [
            "Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza",
            "Málaga", "Murcia", "Palma", "Las Palmas", "Bilbao",
            "Alicante", "Córdoba", "Valladolid", "Vigo", "Gijón"
        ],
        "provinces": [
            "Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza",
            "Málaga", "Murcia", "Baleares", "Las Palmas", "Vizcaya",
            "Alicante", "Córdoba", "Valladolid", "Pontevedra", "Asturias"
        ]
    },
    
    "francia": {
        "region": "Europa",
        "country_code": "FR", 
        "currency": "EUR",
        "timezone": "Europe/Paris",
        "phone_format": "+33",
        "postal_code_format": "#####",
        "cities": [
            "París", "Marsella", "Lyon", "Toulouse", "Niza",
            "Nantes", "Montpellier", "Estrasburgo", "Burdeos", "Lille",
            "Rennes", "Reims", "Saint-Étienne", "Le Havre", "Toulon"
        ],
        "provinces": [
            "Île-de-France", "Provence-Alpes-Côte d'Azur", "Auvergne-Rhône-Alpes",
            "Occitanie", "Nouvelle-Aquitaine", "Pays de la Loire", "Hauts-de-France",
            "Normandie", "Grand Est", "Bretagne", "Bourgogne-Franche-Comté"
        ]
    },
    
    "alemania": {
        "region": "Europa",
        "country_code": "DE",
        "currency": "EUR", 
        "timezone": "Europe/Berlin",
        "phone_format": "+49",
        "postal_code_format": "#####",
        "cities": [
            "Berlín", "Hamburgo", "Múnich", "Colonia", "Frankfurt",
            "Stuttgart", "Düsseldorf", "Leipzig", "Dortmund", "Essen",
            "Bremen", "Dresden", "Hannover", "Núremberg", "Duisburg"
        ],
        "provinces": [
            "Berlín", "Hamburgo", "Baviera", "Renania del Norte-Westfalia",
            "Hesse", "Baden-Württemberg", "Sajonia", "Baja Sajonia",
            "Renania-Palatinado", "Turingia", "Brandemburgo", "Bremen"
        ]
    },
    
    "italia": {
        "region": "Europa",
        "country_code": "IT",
        "currency": "EUR",
        "timezone": "Europe/Rome", 
        "phone_format": "+39",
        "postal_code_format": "#####",
        "cities": [
            "Roma", "Milán", "Nápoles", "Turín", "Palermo",
            "Génova", "Bolonia", "Florencia", "Bari", "Catania",
            "Venecia", "Verona", "Messina", "Padua", "Trieste"
        ],
        "provinces": [
            "Lazio", "Lombardía", "Campania", "Piamonte", "Sicilia",
            "Liguria", "Emilia-Romaña", "Toscana", "Puglia", "Véneto",
            "Calabria", "Cerdeña", "Marche", "Abruzzo", "Friuli"
        ]
    },
    
    # ========== NORTEAMÉRICA ==========
    "usa": {
        "region": "Norteamérica",
        "country_code": "US",
        "currency": "USD",
        "timezone": "America/New_York",
        "phone_format": "+1", 
        "postal_code_format": "#####",
        "cities": [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
            "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
            "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte"
        ],
        "provinces": [
            "New York", "California", "Illinois", "Texas", "Arizona",
            "Pennsylvania", "Florida", "Ohio", "North Carolina", "Georgia",
            "Michigan", "New Jersey", "Virginia", "Washington", "Massachusetts"
        ]
    },
    
    "canada": {
        "region": "Norteamérica", 
        "country_code": "CA",
        "currency": "CAD",
        "timezone": "America/Toronto",
        "phone_format": "+1",
        "postal_code_format": "A#A #A#",
        "cities": [
            "Toronto", "Montreal", "Vancouver", "Calgary", "Edmonton",
            "Ottawa", "Winnipeg", "Quebec City", "Hamilton", "Kitchener",
            "London", "Victoria", "Halifax", "Oshawa", "Windsor"
        ],
        "provinces": [
            "Ontario", "Quebec", "British Columbia", "Alberta", "Manitoba",
            "Saskatchewan", "Nova Scotia", "New Brunswick", "Newfoundland",
            "Prince Edward Island", "Northwest Territories", "Yukon", "Nunavut"
        ]
    },
    
    # ========== GLOBAL (MEZCLA) ==========
    "global": {
        "region": "Global",
        "country_code": "GLOBAL",
        "currency": "MIXED",
        "timezone": "UTC",
        "phone_format": "MIXED", 
        "postal_code_format": "MIXED",
        "cities": [
            # Mezcla de todas las ciudades principales
            "New York", "London", "Tokyo", "Paris", "Madrid", "Mexico City",
            "Buenos Aires", "São Paulo", "Berlin", "Rome", "Moscow",
            "Sydney", "Toronto", "Amsterdam", "Stockholm", "Zurich",
            "Bogotá", "Lima", "Santiago", "Quito", "Caracas", "Barcelona"
        ],
        "countries": [
            "Estados Unidos", "Reino Unido", "España", "Francia", "Alemania",
            "Italia", "México", "Colombia", "Argentina", "Chile", "Perú",
            "Ecuador", "Brasil", "Canadá", "Australia", "Japón", "China"
        ]
    }
}

# ===== FUNCIONES DE UTILIDAD =====

def get_available_contexts() -> List[str]:
    """Obtener lista de contextos geográficos disponibles"""
    return list(GEOGRAPHIC_CONTEXTS.keys())

def get_context_data(context_name: str) -> Dict[str, Any]:
    """Obtener datos de un contexto geográfico específico"""
    return GEOGRAPHIC_CONTEXTS.get(context_name, GEOGRAPHIC_CONTEXTS["global"])

def get_random_city(context_name: str = "global") -> str:
    """Obtener ciudad aleatoria del contexto especificado"""
    context = get_context_data(context_name)
    return random.choice(context["cities"])

def get_random_province(context_name: str = "global") -> str:
    """Obtener provincia/estado aleatorio del contexto especificado"""
    context = get_context_data(context_name)
    if "provinces" in context:
        return random.choice(context["provinces"])
    return "N/A"

def get_phone_format(context_name: str = "global") -> str:
    """Obtener formato de teléfono del contexto especificado"""
    context = get_context_data(context_name)
    return context.get("phone_format", "+1")

def get_currency(context_name: str = "global") -> str:
    """Obtener moneda del contexto especificado"""
    context = get_context_data(context_name)
    return context.get("currency", "USD")

def get_contexts_by_region(region: str) -> List[str]:
    """Obtener contextos de una región específica"""
    return [
        name for name, data in GEOGRAPHIC_CONTEXTS.items()
        if data.get("region", "").lower() == region.lower()
    ]

# ===== CONFIGURACIÓN REGIONAL =====

REGIONS = {
    "Latinoamérica": ["ecuador", "colombia", "mexico", "argentina", "chile", "peru"],
    "Europa": ["espana", "francia", "alemania", "italia"],
    "Norteamérica": ["usa", "canada"],
    "Global": ["global"]
}

def get_region_options() -> Dict[str, List[str]]:
    """Obtener opciones organizadas por región para la UI"""
    return REGIONS