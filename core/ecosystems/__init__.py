"""
Módulo de Ecosistemas de Negocios
Sistema para generar datasets completos e interconectados
"""

from .business_ecosystems import (
    BusinessEcosystem,
    BusinessType, 
    BUSINESS_ECOSYSTEMS,
    get_available_ecosystems,
    get_ecosystems_by_type,
    get_ecosystem_by_key,
    get_business_types,
    get_ecosystem_display_names
)

from .ecosystem_generator import (
    EcosystemGenerator,
    get_available_ecosystem_options,
    generate_ecosystem_data
)

__all__ = [
    # Clases principales
    "BusinessEcosystem",
    "BusinessType",
    "EcosystemGenerator",
    
    # Datos
    "BUSINESS_ECOSYSTEMS",
    
    # Funciones de acceso
    "get_available_ecosystems",
    "get_ecosystems_by_type", 
    "get_ecosystem_by_key",
    "get_business_types",
    "get_ecosystem_display_names",
    "get_available_ecosystem_options",
    
    # Funciones de generación
    "generate_ecosystem_data"
]