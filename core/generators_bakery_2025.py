"""Generadores determinísticos para tablas del Informe Panadería-Cafetería 2025.

Estas tablas no escalan con volume; se generan con registros fijos basados en el documento.
"""
from __future__ import annotations

from typing import List, Dict


def generate_catalogo_productos_2025() -> List[Dict]:
    rows = [
        {"product_id": "P001", "category": "Panadería", "product_name": "Pan de Agua", "description": "Pan de textura suave, elaborado con masa con 0% grasa.", "base_price_usd": 0.21, "iva_rate": 0.15, "final_price_usd": 0.24},
        {"product_id": "P002", "category": "Panadería", "product_name": "Pan de Ambato", "description": "Pan tradicional de la sierra ecuatoriana.", "base_price_usd": 0.27, "iva_rate": 0.15, "final_price_usd": 0.31},
        {"product_id": "P003", "category": "Panadería", "product_name": "Pan de Chocolate", "description": "Pan especial enrollado y relleno de chocolate.", "base_price_usd": 0.78, "iva_rate": 0.15, "final_price_usd": 0.90},
        {"product_id": "P004", "category": "Panadería", "product_name": "Molde Integral", "description": "Pan de molde elaborado con masa integral.", "base_price_usd": 1.52, "iva_rate": 0.15, "final_price_usd": 1.75},
        {"product_id": "P005", "category": "Panadería", "product_name": "Guagua de Pan (Tradicional)", "description": "Masa especial rellena de mermelada de frutas, decorada con glaseado.", "base_price_usd": 0.87, "iva_rate": 0.15, "final_price_usd": 1.00},
        {"product_id": "T001", "category": "Pastelería", "product_name": "Tartaleta de Frambuesa", "description": "Masa quebrada dulce con crema mousseline y frambuesas.", "base_price_usd": 4.66, "iva_rate": 0.15, "final_price_usd": 5.36},
        {"product_id": "T002", "category": "Pastelería", "product_name": "Cheesecake de Frutos Rojos (Porción)", "description": "Cheesecake de vainilla con cubierta de fresas y moras.", "base_price_usd": 3.91, "iva_rate": 0.15, "final_price_usd": 4.50},
        {"product_id": "T003", "category": "Pastelería", "product_name": "Pastel Mediano (8-15 porciones)", "description": "Bizcochuelo de vainilla relleno de crema y mermelada.", "base_price_usd": 10.87, "iva_rate": 0.15, "final_price_usd": 12.50},
        {"product_id": "T004", "category": "Pastelería", "product_name": "Torta de Chocolate (12 porciones)", "description": "Torta húmeda de masa de chocolate con relleno y cobertura de ganache.", "base_price_usd": 18.48, "iva_rate": 0.15, "final_price_usd": 21.25},
        {"product_id": "C001", "category": "Cafetería", "product_name": "Americano (150 ml)", "description": "Espresso diluido en agua caliente.", "base_price_usd": 3.08, "iva_rate": 0.15, "final_price_usd": 3.54},
        {"product_id": "C002", "category": "Cafetería", "product_name": "Cappuccino (150 ml)", "description": "Espresso, leche vaporizada y espuma de leche.", "base_price_usd": 3.57, "iva_rate": 0.15, "final_price_usd": 4.11},
        {"product_id": "C003", "category": "Cafetería", "product_name": "Latte (300 ml)", "description": "Espresso con una mayor proporción de leche vaporizada.", "base_price_usd": 3.97, "iva_rate": 0.15, "final_price_usd": 4.57},
        {"product_id": "C004", "category": "Cafetería", "product_name": "Chocolate Caliente", "description": "A base de chocolate 80%.", "base_price_usd": 3.22, "iva_rate": 0.15, "final_price_usd": 3.70},
    ]
    return rows


def generate_costos_insumos_2025() -> List[Dict]:
    return [
        {"ingredient_id": "ING001", "ingredient_name": "Harina de Trigo (Superior)", "supplier_unit_size": "50 kg", "supplier_unit_cost_usd": 42.71, "cost_per_gram_usd": 0.00085},
        {"ingredient_id": "ING002", "ingredient_name": "Azúcar Blanca (Granel)", "supplier_unit_size": "50 kg", "supplier_unit_cost_usd": 40.12, "cost_per_gram_usd": 0.00080},
        {"ingredient_id": "ING003", "ingredient_name": "Manteca Vegetal (Panificación)", "supplier_unit_size": "15 kg", "supplier_unit_cost_usd": 26.70, "cost_per_gram_usd": 0.00178},
        {"ingredient_id": "ING004", "ingredient_name": "Levadura Fresca", "supplier_unit_size": "500 g", "supplier_unit_cost_usd": 1.78, "cost_per_gram_usd": 0.00356},
        {"ingredient_id": "ING005", "ingredient_name": "Sal Refinada", "supplier_unit_size": "1 kg", "supplier_unit_cost_usd": 0.53, "cost_per_gram_usd": 0.00053},
        {"ingredient_id": "ING006", "ingredient_name": "Huevo (Tipo A)", "supplier_unit_size": "30 unidades", "supplier_unit_cost_usd": 3.80, "cost_per_gram_usd": 0.12667},
        {"ingredient_id": "ING007", "ingredient_name": "Leche UHT", "supplier_unit_size": "1 L", "supplier_unit_cost_usd": 0.96, "cost_per_gram_usd": 0.00096},
        {"ingredient_id": "ING008", "ingredient_name": "Café de Especialidad (Grano)", "supplier_unit_size": "1 kg", "supplier_unit_cost_usd": 21.65, "cost_per_gram_usd": 0.02165},
        {"ingredient_id": "ING009", "ingredient_name": "Cobertura de Chocolate (Semiamargo)", "supplier_unit_size": "1 kg", "supplier_unit_cost_usd": 9.00, "cost_per_gram_usd": 0.00900},
    ]


def generate_costos_indirectos_2025() -> List[Dict]:
    return [
        {"cost_id": "CI01", "cost_category": "Inmuebles", "cost_item": "Alquiler de Local Comercial", "estimated_monthly_cost_usd": 1200.00, "notes": "Basado en 100 m² a un promedio de $12/m²."},
        {"cost_id": "CI02", "cost_category": "Servicios Básicos", "cost_item": "Electricidad", "estimated_monthly_cost_usd": 291.00, "notes": "2,500 kWh a $0.1164/kWh."},
        {"cost_id": "CI03", "cost_category": "Servicios Básicos", "cost_item": "Agua Potable", "estimated_monthly_cost_usd": 50.00, "notes": "Estimación fija mensual."},
        {"cost_id": "CI04", "cost_category": "Servicios Básicos", "cost_item": "Gas Industrial", "estimated_monthly_cost_usd": 41.35, "notes": "50 kg a $0.82694/kg."},
        {"cost_id": "CI05", "cost_category": "Tecnología", "cost_item": "Suscripción Sistema POS", "estimated_monthly_cost_usd": 75.00, "notes": "Software POS y gestión."},
        {"cost_id": "CI06", "cost_category": "Seguridad", "cost_item": "Monitoreo y Alarma", "estimated_monthly_cost_usd": 150.00, "notes": "Servicio de seguridad mensual."},
        {"cost_id": "CI07", "cost_category": "Licencias", "cost_item": "Provisión Permisos Anuales", "estimated_monthly_cost_usd": 21.47, "notes": "Prorrateo Patente+ARCSA+Min.Gobierno."},
        {"cost_id": "CI-TOTAL", "cost_category": "Total", "cost_item": "Costo Indirecto Total Mensual", "estimated_monthly_cost_usd": 1828.82, "notes": "Suma de costos mensuales estimados."},
    ]


def generate_costos_rrhh_2025() -> List[Dict]:
    return [
        {"role": "Pastelero/a", "base_salary_usd": 514.00, "iess_employer_contribution_usd": 57.31, "decimo_tercero_provision_usd": 42.83, "decimo_cuarto_provision_usd": 39.17, "vacation_provision_usd": 21.42, "reserve_fund_provision_usd": 42.83, "total_monthly_cost_per_employee_usd": 717.56},
        {"role": "Panadero/a", "base_salary_usd": 470.00, "iess_employer_contribution_usd": 52.41, "decimo_tercero_provision_usd": 39.17, "decimo_cuarto_provision_usd": 39.17, "vacation_provision_usd": 19.58, "reserve_fund_provision_usd": 39.17, "total_monthly_cost_per_employee_usd": 659.50},
        {"role": "Barista/Vendedor", "base_salary_usd": 470.00, "iess_employer_contribution_usd": 52.41, "decimo_tercero_provision_usd": 39.17, "decimo_cuarto_provision_usd": 39.17, "vacation_provision_usd": 19.58, "reserve_fund_provision_usd": 39.17, "total_monthly_cost_per_employee_usd": 659.50},
        {"role": "Ayudante Polifuncional", "base_salary_usd": 470.00, "iess_employer_contribution_usd": 52.41, "decimo_tercero_provision_usd": 39.17, "decimo_cuarto_provision_usd": 39.17, "vacation_provision_usd": 19.58, "reserve_fund_provision_usd": 39.17, "total_monthly_cost_per_employee_usd": 659.50},
    ]


GEN_FIXED_TABLES = {
    "catalogo_productos_2025": generate_catalogo_productos_2025,
    "costos_insumos_2025": generate_costos_insumos_2025,
    "costos_indirectos_2025": generate_costos_indirectos_2025,
    "costos_rrhh_2025": generate_costos_rrhh_2025,
}


def generate_fixed_table(table: str):
    fn = GEN_FIXED_TABLES.get(table)
    if not fn:
        raise ValueError(f"Tabla fija 2025 no soportada: {table}")
    return fn()
