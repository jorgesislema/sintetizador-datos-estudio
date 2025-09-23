"""
Generador de Ecosistemas de Negocios
Genera datasets completos e interconectados para ecosistemas de negocios específicos
"""
from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
from pathlib import Path
import json
from datetime import datetime
import uuid

from .business_ecosystems import (
    BusinessEcosystem, 
    get_ecosystem_by_key,
    get_available_ecosystems,
    BusinessType
)
from ..generators import generate
from ..localization.i18n import translate_complete_dataset


class EcosystemGenerator:
    """Generador de ecosistemas completos de negocios"""
    
    def __init__(self, ecosystem_key: str, base_volume: int = 1000):
        """
        Inicializar generador de ecosistema
        
        Args:
            ecosystem_key: Clave del ecosistema a generar
            base_volume: Volumen base para escalar las tablas
        """
        self.ecosystem_key = ecosystem_key
        self.ecosystem = get_ecosystem_by_key(ecosystem_key)
        self.base_volume = base_volume
        self.generated_data: Dict[str, List[Dict]] = {}
        self.relationships_map: Dict[str, Dict[str, List[Any]]] = {}
        
        if not self.ecosystem:
            raise ValueError(f"Ecosistema '{ecosystem_key}' no encontrado")
    
    def calculate_table_volumes(self) -> Dict[str, int]:
        """Calcular volúmenes de datos por tabla basado en el volumen base"""
        volumes = {}
        
        # Obtener el volumen de referencia (primera entidad maestra)
        ref_volume = self.ecosystem.required_volume.get(
            self.ecosystem.master_entities[0], 1000
        )
        
        # Calcular factor de escala
        scale_factor = self.base_volume / ref_volume
        
        # Aplicar escala a todas las tablas
        for table, suggested_volume in self.ecosystem.required_volume.items():
            volumes[table] = max(1, int(suggested_volume * scale_factor))
            
        return volumes
    
    def generate_master_entities(self, volumes: Dict[str, int]) -> Dict[str, List[Dict]]:
        """Generar entidades maestras del ecosistema"""
        master_data = {}
        
        print(f"🔄 Generando entidades maestras para {self.ecosystem.display_name}...")
        
        for entity in self.ecosystem.master_entities:
            if entity in volumes:
                volume = volumes[entity]
                print(f"   📊 {entity}: {volume:,} registros")
                
                # Mapear nombre de entidad a dominio/tabla
                domain, table = self._map_entity_to_schema(entity)
                
                try:
                    data = generate(domain, table, volume)
                    master_data[entity] = data
                    
                    # Extraer IDs para relaciones
                    self._extract_relationship_ids(entity, data)
                    
                except Exception as e:
                    print(f"   ⚠️ Error generando {entity}: {e}")
                    master_data[entity] = []
        
        return master_data
    
    def generate_core_tables(self, volumes: Dict[str, int]) -> Dict[str, List[Dict]]:
        """Generar tablas principales del ecosistema"""
        core_data = {}
        
        print(f"🔄 Generando tablas principales...")
        
        for table in self.ecosystem.core_tables:
            if table in volumes:
                volume = volumes[table]
                print(f"   📊 {table}: {volume:,} registros")
                
                domain, table_name = self._map_table_to_schema(table)
                
                try:
                    data = generate(domain, table_name, volume)
                    
                    # Aplicar relaciones si es necesario
                    data = self._apply_relationships(table, data)
                    
                    core_data[table] = data
                    
                except Exception as e:
                    print(f"   ⚠️ Error generando {table}: {e}")
                    core_data[table] = []
        
        return core_data
    
    def generate_support_tables(self, volumes: Dict[str, int]) -> Dict[str, List[Dict]]:
        """Generar tablas de soporte (catálogos, configuración)"""
        support_data = {}
        
        print(f"🔄 Generando tablas de soporte...")
        
        for table in self.ecosystem.support_tables:
            # Las tablas de soporte suelen ser más pequeñas
            volume = min(volumes.get(table, 100), 1000)
            print(f"   📊 {table}: {volume:,} registros")
            
            domain, table_name = self._map_table_to_schema(table)
            
            try:
                data = generate(domain, table_name, volume)
                support_data[table] = data
                
            except Exception as e:
                print(f"   ⚠️ Error generando {table}: {e}")
                support_data[table] = []
        
        return support_data
    
    def generate_analytics_tables(self, volumes: Dict[str, int]) -> Dict[str, List[Dict]]:
        """Generar tablas de métricas y análisis"""
        analytics_data = {}
        
        print(f"🔄 Generando tablas de análisis...")
        
        for table in self.ecosystem.analytics_tables:
            if table in volumes:
                volume = volumes[table]
                print(f"   📊 {table}: {volume:,} registros")
                
                domain, table_name = self._map_table_to_schema(table)
                
                try:
                    data = generate(domain, table_name, volume)
                    
                    # Aplicar relaciones con datos maestros
                    data = self._apply_relationships(table, data)
                    
                    analytics_data[table] = data
                    
                except Exception as e:
                    print(f"   ⚠️ Error generando {table}: {e}")
                    analytics_data[table] = []
        
        return analytics_data
    
    def generate_complete_ecosystem(self, apply_translation: bool = False) -> Dict[str, List[Dict]]:
        """Generar ecosistema completo de negocios"""
        print(f"🚀 GENERANDO ECOSISTEMA COMPLETO: {self.ecosystem.display_name}")
        print(f"📋 Descripción: {self.ecosystem.description}")
        print(f"📊 Volumen base: {self.base_volume:,} registros")
        print("=" * 60)
        
        # Calcular volúmenes por tabla
        volumes = self.calculate_table_volumes()
        
        # Generar datos por categorías
        master_data = self.generate_master_entities(volumes)
        core_data = self.generate_core_tables(volumes)
        support_data = self.generate_support_tables(volumes)
        analytics_data = self.generate_analytics_tables(volumes)
        
        # Combinar todos los datos
        all_data = {
            **master_data,
            **core_data, 
            **support_data,
            **analytics_data
        }
        
        # Aplicar traducción si se solicita
        if apply_translation:
            print(f"🌐 Aplicando traducción al español...")
            for table_name, data in all_data.items():
                if data:  # Solo si hay datos
                    try:
                        all_data[table_name] = translate_complete_dataset(data, "es")
                    except Exception as e:
                        print(f"   ⚠️ Error traduciendo {table_name}: {e}")
        
        self.generated_data = all_data
        
        print(f"\n✅ Ecosistema generado exitosamente!")
        print(f"📊 Total de tablas: {len(all_data)}")
        print(f"📈 Total de registros: {sum(len(data) for data in all_data.values()):,}")
        
        return all_data
    
    def _map_entity_to_schema(self, entity: str) -> Tuple[str, str]:
        """Mapear entidad a dominio/tabla existente"""
        # Mapeo básico - esto se puede expandir
        entity_mapping = {
            "users": ("creator_intelligence", "creator_intelligence"),
            "customers": ("retail", "retail"),
            "patients": ("healthcare", "patients"),
            "students": ("education", "education"),
            "products": ("retail", "retail"),
            "sellers": ("enterprise", "enterprise"),
            "employees": ("enterprise", "enterprise"),
            "accounts": ("finance", "accounts"),
            "stores": ("retail", "retail"),
            "content": ("creator_intelligence", "creator_intelligence")
        }
        
        return entity_mapping.get(entity, ("retail", "retail"))
    
    def _map_table_to_schema(self, table: str) -> Tuple[str, str]:
        """Mapear tabla a dominio/tabla existente"""
        # Mapeo inteligente basado en prefijos y nombres
        if "social" in table or "content" in table or "platform" in table:
            return ("creator_intelligence", "creator_intelligence")
        elif "customer" in table or "retail" in table or "product" in table:
            return ("retail", "retail")
        elif "patient" in table or "doctor" in table or "medical" in table:
            return ("healthcare", "patients")
        elif "student" in table or "professor" in table or "course" in table:
            return ("education", "education")
        elif "account" in table or "transaction" in table or "bank" in table:
            return ("finance", "accounts")
        elif "employee" in table or "enterprise" in table or "company" in table:
            return ("enterprise", "enterprise")
        else:
            # Default fallback
            return ("retail", "retail")
    
    def _extract_relationship_ids(self, entity: str, data: List[Dict]):
        """Extraer IDs para usar en relaciones"""
        if not data:
            return
            
        # Buscar campo ID principal
        id_fields = [key for key in data[0].keys() if 'id' in key.lower()]
        
        if id_fields:
            primary_id = id_fields[0]  # Usar el primer campo ID encontrado
            ids = [record[primary_id] for record in data if primary_id in record]
            
            if entity not in self.relationships_map:
                self.relationships_map[entity] = {}
            self.relationships_map[entity]['ids'] = ids
    
    def _apply_relationships(self, table: str, data: List[Dict]) -> List[Dict]:
        """Aplicar relaciones entre tablas usando IDs de entidades maestras"""
        # Esta es una implementación básica
        # En un sistema completo, esto sería más sofisticado
        
        if not data or not self.relationships_map:
            return data
        
        # Buscar campos de relación en los datos
        for record in data:
            for field, value in record.items():
                if 'user_id' in field and 'users' in self.relationships_map:
                    # Reemplazar con ID real de usuario generado
                    user_ids = self.relationships_map['users'].get('ids', [])
                    if user_ids:
                        import random
                        record[field] = random.choice(user_ids)
        
        return data
    
    def get_ecosystem_summary(self) -> Dict[str, Any]:
        """Obtener resumen del ecosistema generado"""
        if not self.generated_data:
            return {}
            
        return {
            "ecosystem_key": self.ecosystem_key,
            "ecosystem_name": self.ecosystem.display_name,
            "description": self.ecosystem.description,
            "business_type": self.ecosystem.business_type.value,
            "base_volume": self.base_volume,
            "total_tables": len(self.generated_data),
            "total_records": sum(len(data) for data in self.generated_data.values()),
            "tables_summary": {
                table: len(data) for table, data in self.generated_data.items()
            },
            "generation_timestamp": datetime.now().isoformat()
        }


def get_available_ecosystem_options() -> Dict[str, str]:
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
    generator = EcosystemGenerator(ecosystem_key, volume)
    data = generator.generate_complete_ecosystem(apply_translation)
    summary = generator.get_ecosystem_summary()
    
    return data, summary