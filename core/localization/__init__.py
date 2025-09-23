"""
Módulo de Localización para el Sintetizador de Datos

Proporciona:
- Contextos geográficos para múltiples países
- Sistema de internacionalización (i18n)
- Localización de datos sintéticos
"""

from .geographic_contexts import (
    GEOGRAPHIC_CONTEXTS,
    get_available_contexts,
    get_context_data,
    get_random_city,
    get_random_province,
    get_phone_format,
    get_currency,
    get_contexts_by_region,
    get_region_options
)

from .i18n import (
    translate_column_name,
    translate_table_name,
    translate_categorical_value,
    translate_schema_fields,
    translate_data_row,
    translate_complete_dataset,
    get_available_languages,
    get_language_display_names,
    COLUMN_TRANSLATIONS,
    TABLE_TRANSLATIONS,
    CATEGORICAL_VALUE_TRANSLATIONS
)

__all__ = [
    # Geographic contexts
    "GEOGRAPHIC_CONTEXTS",
    "get_available_contexts",
    "get_context_data", 
    "get_random_city",
    "get_random_province",
    "get_phone_format",
    "get_currency",
    "get_contexts_by_region",
    "get_region_options",
    
    # Internationalization
    "translate_column_name",
    "translate_table_name", 
    "translate_categorical_value",
    "translate_schema_fields",
    "translate_data_row",
    "translate_complete_dataset",
    "get_available_languages",
    "get_language_display_names",
    "COLUMN_TRANSLATIONS",
    "TABLE_TRANSLATIONS", 
    "CATEGORICAL_VALUE_TRANSLATIONS"
]