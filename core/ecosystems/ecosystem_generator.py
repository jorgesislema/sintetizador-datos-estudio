"""
Generador de Ecosistemas de Negocios Actualizado
Genera datasets completos e interconectados para ecosistemas de negocios específicos
usando dominios y tablas reales del sistema
"""
from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
from pathlib import Path
import json
from datetime import datetime
import uuid
import time

from .business_ecosystems import (
    BusinessEcosystem, 
    get_ecosystem_by_key,
    get_available_ecosystems,
    BusinessType
)
from ..generators import generate

# Intentar importar localización, fallar silenciosamente si no está disponible
try:
    from ..localization.i18n import translate_complete_dataset
    LOCALIZATION_AVAILABLE = True
except ImportError:
    LOCALIZATION_AVAILABLE = False

class EcosystemGenerator:
    """
    Generador de ecosistemas de negocios completos usando dominios y tablas reales
    """
    
    def __init__(self):
        self.ecosystem = None
        self.base_volume = 1000
        self.generated_data = {}
        self.id_mappings = {}  # Para mantener consistencia entre tablas
        
    def generate_complete_ecosystem(self, ecosystem_key: str, base_volume: int = 1000, 
                                  apply_translation: bool = False) -> Tuple[Dict[str, List[Dict]], Dict[str, Any]]:
        """
        Generar un ecosistema completo de negocio
        
        Args:
            ecosystem_key: Clave del ecosistema a generar
            base_volume: Volumen base para escalado
            apply_translation: Si aplicar traducción al español
            
        Returns:
            Tuple[generated_data, summary]
        """
        print(f"GENERANDO ECOSISTEMA COMPLETO: {ecosystem_key}")
        
        # Obtener definición del ecosistema
        self.ecosystem = get_ecosystem_by_key(ecosystem_key)
        if not self.ecosystem:
            raise ValueError(f"Ecosistema '{ecosystem_key}' no encontrado")
            
        self.base_volume = base_volume
        self.generated_data = {}
        self.id_mappings = {}
        
        print(f"Descripcion: {self.ecosystem.description}")
        print(f"Volumen base: {base_volume} registros")
        print("=" * 60)
        
        try:
            # Paso 1: Generar entidades maestras
            print(f"Generando entidades maestras para {self.ecosystem.display_name}...")
            
            # Paso 2: Generar tablas principales
            print("Generando tablas principales...")
            self._generate_tables_group(self.ecosystem.core_tables, "principales")
            
            # Paso 3: Generar tablas de soporte
            print("Generando tablas de soporte...")
            self._generate_tables_group(self.ecosystem.support_tables, "soporte")
            
            # Paso 4: Generar tablas de análisis
            print("Generando tablas de analisis...")
            self._generate_tables_group(self.ecosystem.analytics_tables, "análisis")
            
            # Paso 5: Aplicar traducciones si se solicita
            if apply_translation and LOCALIZATION_AVAILABLE:
                print("Aplicando traducciones...")
                self._apply_translations()
            
            print("\nEcosistema generado exitosamente!")
            
            # Crear resumen
            summary = self._create_summary()
            print(f"Total de tablas: {summary['total_tables']}")
            print(f"Total de registros: {summary['total_records']:,}")
            
            return self.generated_data, summary
            
        except Exception as e:
            print(f"Error generando ecosistema: {e}")
            raise
    
    def _generate_tables_group(self, tables_by_domain: Dict[str, List[str]], group_name: str):
        """Generar un grupo de tablas organizadas por dominio"""
        for domain, tables in tables_by_domain.items():
            for table in tables:
                try:
                    volume = self._calculate_table_volume(table)
                    if volume > 0:
                        print(f"   {table}: {volume:,} registros")
                        data = generate(domain, table, volume)
                        self.generated_data[table] = data
                    else:
                        print(f"   {table}: volumen calculado = 0, omitiendo")
                    # Micro-sleep para ceder control (evita UI aparente frozen en hilos únicos)
                    time.sleep(0.001)
                except Exception as e:
                    print(f"   Error generando {table}: {e}")
                    self.generated_data[table] = []
    
    def _calculate_table_volume(self, table: str) -> int:
        """Calcular el volumen de registros para una tabla específica"""
        ratio = self.ecosystem.volume_ratios.get(table, 1.0)
        return max(1, int(self.base_volume * ratio))
    
    def _apply_translations(self):
        """Aplicar traducciones a los datos generados"""
        translated_data = {}
        for table_name, data in self.generated_data.items():
            if data:  # Solo traducir si hay datos
                try:
                    translated_data[table_name] = translate_complete_dataset(data, "es")
                except Exception as e:
                    print(f"   ⚠️ Error traduciendo {table_name}: {e}")
                    translated_data[table_name] = data  # Mantener original si falla
            else:
                translated_data[table_name] = data
                
        self.generated_data = translated_data
    
    def _create_summary(self) -> Dict[str, Any]:
        """Crear resumen del ecosistema generado"""
        tables_summary = {}
        total_records = 0
        
        for table_name, data in self.generated_data.items():
            record_count = len(data) if data else 0
            tables_summary[table_name] = record_count
            total_records += record_count
        
        return {
            "ecosystem_key": self.ecosystem.key,
            "ecosystem_name": self.ecosystem.display_name,
            "description": self.ecosystem.description,
            "business_type": self.ecosystem.business_type.value,
            "total_tables": len(self.generated_data),
            "total_records": total_records,
            "base_volume": self.base_volume,
            "tables_summary": tables_summary,
            "master_entities": self.ecosystem.master_entities,
            "generation_timestamp": datetime.now().isoformat()
        }

# ===============================
# FUNCIONES DE UTILIDAD
# ===============================

def get_available_ecosystem_options():
    """Obtener opciones de ecosistemas para la UI"""
    ecosystems = get_available_ecosystems()
    return {key: ecosystem.display_name for key, ecosystem in ecosystems.items()}

def generate_ecosystem_data(ecosystem_key: str, volume: int = 1000, 
                          apply_translation: bool = False) -> Tuple[Dict[str, List[Dict]], Dict[str, Any]]:
    """
    Función de conveniencia para generar un ecosistema completo
    
    Returns:
        Tuple[generated_data, summary]
    """
    generator = EcosystemGenerator()
    data, summary = generator.generate_complete_ecosystem(ecosystem_key, volume, apply_translation)
    
    return data, summary