"""
Aplicación de escritorio nativa para el Sintetizador de Datos
Usando Tkinter para interfaz gráfica local
"""
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
import threading
import json

from core.generators import generate
from core.dq.profiler import profile
from core.integrity.scd2 import scd2_version_rows


class DataSynthesizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sintetizador de Datos - Estudio")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)

        # Variables de estado
        self.current_step = 1
        self.selected_domain = tk.StringVar()
        self.selected_table = tk.StringVar()
        self.row_count = tk.IntVar(value=1000)
        self.error_profile = tk.StringVar(value="none")
        self.output_dir = tk.StringVar(value="./outputs")
        self.output_format = tk.StringVar(value="csv")
        self.scd2_enabled = tk.BooleanVar(value=False)
        self.preview_data = None
        self.generated_data = None
        self.dq_report = None
        # Mapa dinámico descripcion -> nombre técnico de tabla (se recalcula al cambiar dominio)
        self.table_description_map = {}

        # Configurar estilos
        self.setup_styles()

        # Crear interfaz
        self.create_widgets()

        # Cargar dominios disponibles
        self.load_domains()

    def setup_styles(self):
        """Configurar estilos de la aplicación"""
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10, "bold"))
        style.configure("TLabel", font=("Arial", 10))
        style.configure("Header.TLabel", font=("Arial", 16, "bold"), foreground="#1f77b4")
        style.configure("Step.TLabel", font=("Arial", 14, "bold"), foreground="#2ca02c")

    def create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = ttk.Label(main_frame, text="Sintetizador de Datos - Estudio",
                               style="Header.TLabel")
        title_label.pack(pady=(0, 20))

        # Información del proyecto
        info_frame = ttk.LabelFrame(main_frame, text="Informacion del Proyecto", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 20))

        info_text = """
Versión: 1.0.0
Arquitectura: Modular Python
Motores: Faker + SDV/CTGAN
Características: Generación híbrida, SCD2 automático, Perfiles de error, DQ integrada, Multi-formato output
        """
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.pack(anchor=tk.W)

        # Contenedor de pasos
        self.steps_container = ttk.Frame(main_frame)
        self.steps_container.pack(fill=tk.BOTH, expand=True)

        # Crear los 3 pasos
        self.create_step1()
        self.create_step2()
        self.create_step3()

        # Mostrar paso inicial
        self.show_step(1)

    def create_step1(self):
        """Crear el Paso 1: Selección de Dominio y Tabla"""
        self.step1_frame = ttk.Frame(self.steps_container)

        step_label = ttk.Label(self.step1_frame, text="Paso 1: Seleccion de Dominio y Tabla",
                              style="Step.TLabel")
        step_label.pack(pady=(0, 20))

        # Frame de selección
        selection_frame = ttk.LabelFrame(self.step1_frame, text="Selección", padding="10")
        selection_frame.pack(fill=tk.X, pady=(0, 20))

        # Dominio
        ttk.Label(selection_frame, text="Dominio:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.domain_combo = ttk.Combobox(selection_frame, textvariable=self.selected_domain,
                                        state="readonly", width=30)
        self.domain_combo.grid(row=0, column=1, padx=(10, 0), pady=5)
        self.domain_combo.bind("<<ComboboxSelected>>", self.on_domain_selected)

        # Tabla
        ttk.Label(selection_frame, text="Tabla:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.table_combo = ttk.Combobox(selection_frame, textvariable=self.selected_table,
                                       state="readonly", width=30)
        self.table_combo.grid(row=1, column=1, padx=(10, 0), pady=5)
        self.table_combo.bind("<<ComboboxSelected>>", self.on_table_selected)

        # Sección de columnas disponibles
        columns_frame = ttk.LabelFrame(self.step1_frame, text="Columnas Disponibles", padding="10")
        columns_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        # Área de texto para mostrar columnas
        # Altura reducida para que el botón Continuar siempre quede visible incluso en pantallas pequeñas
        self.columns_text = scrolledtext.ScrolledText(columns_frame, height=12, width=80, wrap=tk.WORD)
        self.columns_text.pack(fill=tk.BOTH, expand=True)
        self.columns_text.insert(tk.END, "Selecciona un dominio y tabla para ver las columnas disponibles...")

        # Botón continuar
        continue_btn = ttk.Button(self.step1_frame, text="Continuar al Paso 2",
                                  command=lambda: self.show_step(2))
        continue_btn.pack(pady=10)

        # Barra de progreso pasiva (informativa) para que el usuario sepa que existe
        passive_frame = ttk.Frame(self.step1_frame)
        passive_frame.pack(fill=tk.X, pady=(5, 10))
        ttk.Label(passive_frame, text="Progreso (aparece activo en Paso 2):").pack(anchor=tk.W)
        self.passive_progress = ttk.Progressbar(passive_frame, maximum=100, value=0)
        self.passive_progress.pack(fill=tk.X)

    def create_step2(self):
        """Crear el Paso 2: Configuración de Parámetros"""
        self.step2_frame = ttk.Frame(self.steps_container)

        step_label = ttk.Label(self.step2_frame, text="Paso 2: Configuracion de Parametros",
                              style="Step.TLabel")
        step_label.pack(pady=(0, 20))

        # Mostrar selección actual
        self.selection_info = ttk.Label(self.step2_frame, text="")
        self.selection_info.pack(pady=(0, 20))

        # Configuración
        config_frame = ttk.LabelFrame(self.step2_frame, text="Configuración", padding="10")
        config_frame.pack(fill=tk.X, pady=(0, 20))

        # Fila 1: Tamaño del dataset y perfil de errores
        ttk.Label(config_frame, text="Numero de Filas:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Spinbox(config_frame, from_=100, to=100000, textvariable=self.row_count,
                    width=10).grid(row=0, column=1, padx=(10, 20), pady=5)

        ttk.Label(config_frame, text="Perfil de Errores:").grid(row=0, column=2, sticky=tk.W, pady=5)
        error_combo = ttk.Combobox(config_frame, textvariable=self.error_profile,
                                  values=["none", "light", "moderate", "heavy"], state="readonly", width=15)
        error_combo.grid(row=0, column=3, padx=(10, 0), pady=5)

        # Fila 2: Directorio de salida y formato
        ttk.Label(config_frame, text="Directorio de Salida:").grid(row=1, column=0, sticky=tk.W, pady=5)
        output_entry = ttk.Entry(config_frame, textvariable=self.output_dir, width=30)
        output_entry.grid(row=1, column=1, padx=(10, 5), pady=5)
        ttk.Button(config_frame, text="Explorar", width=8,
                  command=self.select_output_dir).grid(row=1, column=2, padx=(5, 20), pady=5)

        ttk.Label(config_frame, text="Formato de Archivo:").grid(row=1, column=3, sticky=tk.W, pady=5)
        format_combo = ttk.Combobox(config_frame, textvariable=self.output_format,
                                   values=["csv", "json", "excel", "parquet"], state="readonly", width=15)
        format_combo.grid(row=1, column=4, padx=(10, 0), pady=5)

        # Preview
        preview_frame = ttk.LabelFrame(self.step2_frame, text="Preview (Opcional)", padding="10")
        preview_frame.pack(fill=tk.X, pady=(0, 20))

        self.preview_enabled = tk.BooleanVar(value=False)
        ttk.Checkbutton(preview_frame, text="Generar preview",
                       variable=self.preview_enabled).pack(anchor=tk.W)

        self.preview_rows = tk.IntVar(value=10)
        preview_controls = ttk.Frame(preview_frame)
        preview_controls.pack(fill=tk.X, pady=(10, 0))

        ttk.Label(preview_controls, text="Filas de preview:").pack(side=tk.LEFT)
        ttk.Spinbox(preview_controls, from_=5, to=50, textvariable=self.preview_rows,
                    width=5).pack(side=tk.LEFT, padx=(10, 0))

        ttk.Button(preview_controls, text="Generar Preview",
                  command=self.generate_preview).pack(side=tk.RIGHT)

        # Área de preview
        self.preview_text = scrolledtext.ScrolledText(preview_frame, height=10, width=80)
        self.preview_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # Sección de Generación
        generation_frame = ttk.LabelFrame(self.step2_frame, text="Generacion de Dataset", padding="10")
        generation_frame.pack(fill=tk.X, pady=(20, 0))

        # Controles de generación
        gen_controls_frame = ttk.Frame(generation_frame)
        gen_controls_frame.pack(fill=tk.X, pady=(0, 10))

        # SCD2 option
        ttk.Checkbutton(gen_controls_frame, text="Aplicar SCD2 en generacion",
                       variable=self.scd2_enabled).pack(side=tk.LEFT, padx=(0, 20))

        # Botón START prominente
        start_button = ttk.Button(gen_controls_frame, text="START - Generar Dataset",
                  command=self.generate_dataset)
        start_button.pack(side=tk.RIGHT)
        start_button.configure(style="Accent.TButton")

        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(generation_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(10, 0))

        self.status_label = ttk.Label(generation_frame, text="Listo para generar datos")
        self.status_label.pack(pady=(5, 0))

        # Navegación
        nav_frame = ttk.Frame(self.step2_frame)
        nav_frame.pack(fill=tk.X, pady=20)

        ttk.Button(nav_frame, text="Volver al Paso 1",
                  command=lambda: self.show_step(1)).pack(side=tk.LEFT)
        ttk.Button(nav_frame, text="Ver Resultados",
                  command=lambda: self.show_step(3)).pack(side=tk.RIGHT)

    def create_step3(self):
        """Crear el Paso 3: Resultados"""
        self.step3_frame = ttk.Frame(self.steps_container)

        step_label = ttk.Label(self.step3_frame, text="Paso 3: Resultados y Metricas",
                              style="Step.TLabel")
        step_label.pack(pady=(0, 20))

        # Configuración final utilizada
        self.final_config = ttk.Label(self.step3_frame, text="")
        self.final_config.pack(pady=(0, 20))

        # Resultados
        results_frame = ttk.LabelFrame(self.step3_frame, text="Resultados de Generacion", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Métricas DQ
        metrics_frame = ttk.Frame(results_frame)
        metrics_frame.pack(fill=tk.X, pady=(0, 10))

        self.metrics_labels = {}
        metrics = ["Completitud", "Duplicados", "Unicidad", "Validez"]
        for i, metric in enumerate(metrics):
            ttk.Label(metrics_frame, text=f"{metric}:").grid(row=0, column=i*2, sticky=tk.W, padx=(0, 5))
            self.metrics_labels[metric] = ttk.Label(metrics_frame, text="-", font=("Arial", 10, "bold"))
            self.metrics_labels[metric].grid(row=0, column=i*2+1, sticky=tk.W)

        # Botón de descarga
        ttk.Button(results_frame, text="Abrir Carpeta de Resultados",
                  command=self.open_results_folder).pack(pady=10)

        # Área de resultados detallados
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=80)
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # Navegación
        ttk.Button(self.step3_frame, text="Volver al Paso 2",
                  command=lambda: self.show_step(2)).pack(pady=20)

    def load_domains(self):
        """Cargar dominios disponibles"""
        try:
            from core.utils.schemas import list_domains
            domains_dict = list_domains()

            # Lista simple de dominios (solo nombres)
            available_domains = list(domains_dict.keys())
            self.domain_combo['values'] = sorted(available_domains)

            # Si hay dominios disponibles, seleccionar el primero
            if available_domains:
                self.domain_combo.set(available_domains[0])
                # Trigger manual del evento de selección
                self.on_domain_selected(None)
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando dominios: {str(e)}")

    def get_selected_table(self):
        """Obtener nombre técnico de la tabla seleccionada usando el mapa dinámico."""
        desc = self.selected_table.get()
        if not desc:
            return ""
        # Buscar en el mapa cargado en la selección de dominio
        return self.table_description_map.get(desc, desc)

    def get_selected_domain(self):
        """Obtener el dominio seleccionado"""
        return self.selected_domain.get()

    def on_domain_selected(self, event):
        """Manejador de selección de dominio"""
        domain = self.get_selected_domain()

        try:
            from core.utils.schemas import list_tables
            tables = list_tables(domain)

            # Mapeo de nombres técnicos a descripciones legibles
            table_descriptions = {
                "enterprise": {
                    "dim_employee": "RR.HH. - Empleados",
                    "dim_org_unit": "RR.HH. - Unidades Organizacionales", 
                    "dim_job": "RR.HH. - Puestos",
                    "fact_headcount_daily": "RR.HH. - Plantilla Diaria",
                    "fact_attrition": "RR.HH. - Rotación",
                    "fact_overtime": "RR.HH. - Horas Extra",
                    "fact_pto": "RR.HH. - Vacaciones",
                    "dim_job_req": "Reclutamiento - Requisiciones",
                    "dim_candidate": "Reclutamiento - Candidatos",
                    "fact_pipeline_events": "Reclutamiento - Pipeline",
                    "fact_interviews": "Reclutamiento - Entrevistas",
                    "fact_offers": "Reclutamiento - Ofertas",
                    "dim_payroll_cycle": "Nómina - Ciclos",
                    "dim_benefit": "Nómina - Beneficios",
                    "fact_pay_slip": "Nómina - Recibos",
                    "fact_deductions": "Nómina - Deducciones",
                    "fact_taxes": "Nómina - Impuestos",
                    "dim_customer": "Ventas - Clientes",
                    "dim_store": "Ventas - Tiendas",
                    "dim_product": "Ventas - Productos", 
                    "dim_salesperson": "Ventas - Vendedores",
                    "fact_sales_line": "Ventas - Líneas",
                    "fact_returns": "Ventas - Devoluciones",
                    "fact_margins": "Ventas - Márgenes"
                },
                "microbusiness": {
                    "dim_product": "Productos",
                    "dim_supplier": "Proveedores",
                    "dim_store": "Tienda",
                    "dim_customer": "Clientes",
                    "fact_pos_line": "Ventas POS",
                    "fact_cash_shift": "Turnos de Caja",
                    "fact_inventory": "Inventario",
                    "fact_po": "Órdenes de Compra",
                    "dim_perishables_batch": "Lotes Perecederos",
                    "fact_perishables_waste": "Mermas",
                    "fact_local_promos": "Promociones",
                    "fact_distributor_credit": "Crédito Distribuidor",
                    "dim_recipe": "Recetas",
                    "dim_ingredient": "Ingredientes",
                    "fact_daily_production": "Producción Diaria",
                    "fact_mermas": "Mermas Producción",
                    "fact_custom_orders": "Pedidos Especiales",
                    "dim_book_title": "Libros",
                    "dim_publisher": "Editoriales",
                    "fact_books_sales": "Ventas Libros",
                    "fact_consignment": "Consignación",
                    "fact_copy_services": "Servicios Copia",
                    "dim_service": "Servicios",
                    "dim_staff": "Personal",
                    "fact_appointments": "Citas",
                    "fact_commissions": "Comisiones",
                    "fact_memberships": "Membresías",
                    "fact_retail_sales": "Ventas Retail"
                },
                "retail": {
                    "dim_store": "Tiendas",
                    "dim_cashier": "Cajeros",
                    "dim_product": "Productos",
                    "dim_customer": "Clientes",
                    "fact_ticket_line": "Líneas Ticket",
                    "fact_voids": "Anulaciones",
                    "fact_returns": "Devoluciones",
                    "fact_cash_drawer": "Caja Registradora",
                    "dim_session": "Sesiones Web",
                    "dim_address": "Direcciones",
                    "fact_orders": "Pedidos",
                    "fact_order_items": "Items Pedido",
                    "fact_payments": "Pagos",
                    "fact_returns_rma": "Devoluciones RMA"
                },
                "finance": {
                    "dim_customer": "Clientes",
                    "dim_account": "Cuentas",
                    "dim_branch": "Sucursales",
                    "fact_transactions": "Transacciones",
                    "fact_loans": "Préstamos",
                    "fact_collections": "Cobranzas",
                    "fact_risk_scores": "Scores de Riesgo",
                    "dim_policy": "Pólizas",
                    "dim_insured_party": "Asegurados",
                    "dim_broker": "Corredores",
                    "fact_premiums": "Primas",
                    "fact_claims": "Siniestros",
                    "fact_reserves": "Reservas",
                    "fact_risk": "Riesgo"
                },
                "healthcare": {
                    "dim_patient_pseudo": "Pacientes",
                    "dim_provider": "Prestadores",
                    "dim_procedure": "Procedimientos",
                    "dim_diagnosis": "Diagnósticos",
                    "fact_encounters": "Encuentros",
                    "fact_labs": "Laboratorios",
                    "fact_medications": "Medicamentos",
                    "fact_outcomes": "Resultados",
                    "dim_trial": "Ensayos",
                    "dim_site": "Sitios",
                    "dim_subject_pseudo": "Sujetos",
                    "dim_visit": "Visitas",
                    "fact_aes": "Eventos Adversos",
                    "fact_biomarkers": "Biomarcadores",
                    "fact_adherence": "Adherencia",
                    "dim_channel": "Canales",
                    "fact_appointments": "Citas",
                    "fact_prescriptions": "Prescripciones",
                    "fact_csat": "Satisfacción"
                }
            }

            # Crear lista con descripciones
            table_options = []
            domain_tables = table_descriptions.get(domain, {})
            for table in tables:
                description = domain_tables.get(table, f"Tabla {table}")
                table_options.append(description)

            # Guardar mapa descripcion -> nombre técnico para este dominio
            self.table_description_map = {domain_tables.get(t, f"Tabla {t}"): t for t in tables}
            self.table_combo['values'] = table_options
            self.selected_table.set("")  # Limpiar selección anterior
            self.columns_text.delete(1.0, tk.END)
            self.columns_text.insert(tk.END, f"Selecciona una tabla del dominio '{domain}' para ver las columnas disponibles...")
        except Exception as e:
            self.table_combo['values'] = []
            self.columns_text.delete(1.0, tk.END)
            self.columns_text.insert(tk.END, f"Error cargando tablas del dominio '{domain}': {str(e)}")
            messagebox.showwarning("Advertencia", f"Error cargando tablas del dominio {domain}: {str(e)}")

    def on_table_selected(self, event):
        """Manejador de selección de tabla"""
        domain = self.get_selected_domain()
        desc = self.selected_table.get()
        table = self.get_selected_table()

        # Fallback: si no se resolvió el nombre técnico intenta inferirlo por coincidencia parcial
        if desc and (not table or table.startswith("Tabla ")):
            # intentar normalizar
            import unicodedata
            norm = unicodedata.normalize('NFKD', desc).encode('ascii','ignore').decode('ascii')
            norm = norm.lower().replace(' ', '_').replace('-', '_')
            from core.utils.schemas import list_tables
            try:
                candidates = list_tables(domain)
                for c in candidates:
                    if c in norm or norm in c:
                        table = c
                        break
            except Exception:
                pass

        # Debug logging (consola)
        try:
            print(f"[DEBUG] Seleccion tabla desc='{desc}' -> tecnico='{table}' dominio='{domain}'")
        except Exception:
            pass

        if domain and table:
            self.show_table_columns(domain, table)
            try:
                self.show_step(2)
            except Exception:
                pass

    def show_table_columns(self, domain: str, table: str):
        """Mostrar las columnas disponibles para la tabla seleccionada"""
        try:
            from core.utils.schemas import load_table_schema

            schema = load_table_schema(domain, table)
            fields = schema.get("fields", {})

            # Limpiar área de texto
            self.columns_text.delete(1.0, tk.END)

            # Título
            self.columns_text.insert(tk.END, f"Dominio: {domain.upper()}\n", "title")
            self.columns_text.insert(tk.END, f"Tabla: {table}\n\n", "title")

            # Campos comunes (siempre presentes)
            common_fields = [
                "id (PK técnica)", "natural_key (BK si aplica)",
                "tenant_id/org_id", "source_system", "source_table",
                "batch_id", "batch_time_utc", "record_hash (dedupe)",
                "is_active", "valid_from_utc", "valid_to_utc (SCD2)",
                "created_at_utc", "created_by", "updated_at_utc", "updated_by",
                "pii_sensitivity (none/low/med/high)",
                "geo_country", "geo_region", "geo_city", "geo_lat", "geo_lon",
                "currency_code", "fx_rate_to_usd",
                "processing_status (ok/warn/error)", "dq_completeness_pct", "dq_validity_pct",
                "tags", "notes"
            ]

            self.columns_text.insert(tk.END, "CAMPOS COMUNES (siempre incluidos):\n", "header")
            for field in common_fields:
                self.columns_text.insert(tk.END, f"• {field}\n")
            self.columns_text.insert(tk.END, "\n")

            # Campos específicos de la tabla
            if fields:
                self.columns_text.insert(tk.END, "CAMPOS ESPECIFICOS DE LA TABLA:\n", "header")
                for field_name, field_config in fields.items():
                    field_type = field_config.get("type", "string")
                    description = field_config.get("description", "")
                    if description:
                        self.columns_text.insert(tk.END, f"• {field_name} ({field_type}): {description}\n")
                    else:
                        self.columns_text.insert(tk.END, f"• {field_name} ({field_type})\n")
            else:
                self.columns_text.insert(tk.END, "No hay campos específicos definidos para esta tabla.\n")

            # Configurar tags para formato
            self.columns_text.tag_configure("title", font=("Arial", 12, "bold"), foreground="#1f77b4")
            self.columns_text.tag_configure("header", font=("Arial", 10, "bold"), foreground="#2ca02c")

        except Exception as e:
            self.columns_text.delete(1.0, tk.END)
            self.columns_text.insert(tk.END, f"Error cargando esquema: {str(e)}")
            messagebox.showerror("Error", f"Error cargando esquema de la tabla: {str(e)}")

    def select_output_dir(self):
        """Seleccionar directorio de salida"""
        dir_path = filedialog.askdirectory(title="Seleccionar directorio de salida")
        if dir_path:
            self.output_dir.set(dir_path)

    def generate_preview(self):
        """Generar preview de datos"""
        if not self.get_selected_domain() or not self.get_selected_table():
            messagebox.showerror("Error", "Selecciona un dominio y tabla primero")
            return

        if not self.preview_enabled.get():
            return

        # Deshabilitar botón durante generación
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, "Generando preview...\n")

        # Generar en thread separado para no bloquear UI
        def generate_thread():
            try:
                domain = self.get_selected_domain()
                table = self.get_selected_table()
                rows = self.preview_rows.get()

                data = generate(domain, table, rows, error_profile=self.error_profile.get())

                # Mostrar resultados
                self.root.after(0, lambda: self.show_preview_results(data))

            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Error generando preview: {str(e)}"))

        threading.Thread(target=generate_thread, daemon=True).start()

    def show_preview_results(self, data):
        """Mostrar resultados del preview"""
        if data:
            # Convertir a DataFrame para mejor visualización
            df = pd.DataFrame(data)

            # Mostrar información básica
            info_text = f"Preview generado: {len(data)} filas, {len(df.columns)} columnas\n\n"
            info_text += "Primeras filas:\n" + "="*50 + "\n"

            # Mostrar primeras 5 filas
            preview_df = df.head(5)
            info_text += str(preview_df.to_string(index=False))

            # Métricas DQ
            if data:
                metrics = profile(data)
                sample_metric = next(iter(metrics.values()), {})

                info_text += "\n\n" + "="*50 + "\n"
                info_text += "Metricas de Calidad (Preview):\n"
                info_text += f"Completitud: {sample_metric.get('completeness', 0)*100:.1f}%\n"
                info_text += f"Duplicados: {sample_metric.get('duplicates_count', 0):.0f}\n"
                info_text += f"Unicidad: {sample_metric.get('uniqueness_ratio', 0):.2f}\n"
                info_text += f"Validez: {sample_metric.get('validity', 0)*100:.1f}%\n"

            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, info_text)

            self.preview_data = data
        else:
            self.preview_text.insert(tk.END, "No se generaron datos")

    def generate_dataset(self):
        """Generar dataset completo"""
        if not self.get_selected_domain() or not self.get_selected_table():
            messagebox.showerror("Error", "Selecciona un dominio y tabla primero")
            return

        # Actualizar barra de progreso
        self.progress_var.set(0)
        self.status_label.config(text="Iniciando generación...")

        def generate_thread():
            try:
                domain = self.get_selected_domain()
                table = self.get_selected_table()
                rows = self.row_count.get()

                # Paso 1: Generar datos
                self.root.after(0, lambda: self.status_label.config(text="Generando datos..."))
                self.root.after(0, lambda: self.progress_var.set(20))

                data = generate(domain, table, rows, error_profile=self.error_profile.get())

                # Paso 2: Aplicar SCD2 si está habilitado
                if self.scd2_enabled.get():
                    self.root.after(0, lambda: self.status_label.config(text="Aplicando SCD2..."))
                    self.root.after(0, lambda: self.progress_var.set(40))
                    data = scd2_version_rows(data, change_prob=0.2)

                # Paso 3: Guardar archivo
                self.root.after(0, lambda: self.status_label.config(text="Guardando archivo..."))
                self.root.after(0, lambda: self.progress_var.set(60))

                # Crear carpeta específica para la tabla
                base_out_dir = Path(self.output_dir.get())
                table_out_dir = base_out_dir / table
                table_out_dir.mkdir(parents=True, exist_ok=True)
                
                format_ext = self.output_format.get()
                out_file = table_out_dir / f"{domain}__{table}.{format_ext}"

                # Guardar según el formato seleccionado
                df = pd.DataFrame(data)
                
                if format_ext == "csv":
                    df.to_csv(out_file, index=False)
                elif format_ext == "json":
                    df.to_json(out_file, orient='records', indent=2)
                elif format_ext == "excel":
                    df.to_excel(out_file, index=False, engine='openpyxl')
                elif format_ext == "parquet":
                    df.to_parquet(out_file, index=False)
                else:
                    # Default to CSV
                    df.to_csv(out_file, index=False)

                # Paso 4: Calcular métricas DQ
                self.root.after(0, lambda: self.status_label.config(text="Calculando métricas DQ..."))
                self.root.after(0, lambda: self.progress_var.set(80))

                dq_metrics = profile(data)

                # Paso 5: Finalizar
                self.root.after(0, lambda: self.progress_var.set(100))
                self.root.after(0, lambda: self.status_label.config(text="¡Generación completada!"))

                # Mostrar resultados
                self.root.after(0, lambda: self.show_generation_results(data, dq_metrics, out_file))

            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Error generando dataset: {str(e)}"))
                self.root.after(0, lambda: self.status_label.config(text="Error en generación"))

        threading.Thread(target=generate_thread, daemon=True).start()

    def show_generation_results(self, data, dq_metrics, out_file):
        """Mostrar resultados de la generación"""
        # Actualizar métricas en la UI
        sample_metric = next(iter(dq_metrics.values()), {})
        self.metrics_labels["Completitud"].config(text=f"{sample_metric.get('completeness', 0)*100:.1f}%")
        self.metrics_labels["Duplicados"].config(text=f"{sample_metric.get('duplicates_count', 0):.0f}")
        self.metrics_labels["Unicidad"].config(text=f"{sample_metric.get('uniqueness_ratio', 0):.2f}")
        self.metrics_labels["Validez"].config(text=f"{sample_metric.get('validity', 0)*100:.1f}%")

        # Mostrar información en el área de resultados
        result_text = f"Dataset generado exitosamente!\n\n"
        result_text += f"Archivo: {out_file}\n"
        result_text += f"Filas generadas: {len(data)}\n"
        result_text += f"Columnas: {len(data[0]) if data else 0}\n\n"

        result_text += "Reporte de Calidad de Datos:\n"
        result_text += "="*40 + "\n"
        result_text += f"Completitud Promedio: {sample_metric.get('completeness', 0)*100:.1f}%\n"
        result_text += f"Total Duplicados: {sample_metric.get('duplicates_count', 0):.0f}\n"
        result_text += f"Ratio Unicidad: {sample_metric.get('uniqueness_ratio', 0):.2f}\n"
        result_text += f"Validez: {sample_metric.get('validity', 0)*100:.1f}%\n\n"

        result_text += "Primeras filas del dataset:\n"
        result_text += "="*40 + "\n"

        if data:
            df = pd.DataFrame(data[:5])  # Primeras 5 filas
            result_text += str(df.to_string(index=False))

        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, result_text)

        # Guardar datos generados para descarga
        self.generated_data = data
        self.dq_report = dq_metrics

        messagebox.showinfo("Éxito", f"Dataset generado correctamente!\nArchivo guardado en: {out_file}")

    def open_results_folder(self):
        """Abrir la carpeta de resultados"""
        output_dir = self.output_dir.get()
        if not output_dir or not os.path.exists(output_dir):
            messagebox.showwarning("Advertencia", "No hay carpeta de resultados válida")
            return
            
        try:
            import subprocess
            import sys
            
            if sys.platform == "win32":
                os.startfile(output_dir)
            elif sys.platform == "darwin":
                subprocess.call(["open", output_dir])
            else:
                subprocess.call(["xdg-open", output_dir])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la carpeta: {str(e)}")

    def download_dataset(self):
        """Descargar dataset generado"""
        if not self.generated_data:
            messagebox.showwarning("Advertencia", "No hay datos generados para descargar")
            return

        # Pedir ubicación de guardado
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Parquet files", "*.parquet"), ("All files", "*.*")],
            title="Guardar Dataset"
        )

        if file_path:
            try:
                df = pd.DataFrame(self.generated_data)

                if file_path.endswith('.csv'):
                    df.to_csv(file_path, index=False)
                elif file_path.endswith('.parquet'):
                    df.to_parquet(file_path, index=False)
                else:
                    # Default to CSV
                    df.to_csv(file_path, index=False)

                messagebox.showinfo("Éxito", f"Archivo guardado correctamente:\n{file_path}")

            except Exception as e:
                messagebox.showerror("Error", f"Error guardando archivo: {str(e)}")

    def show_step(self, step_num):
        """Mostrar el paso especificado"""
        # Ocultar todos los pasos
        self.step1_frame.pack_forget()
        self.step2_frame.pack_forget()
        self.step3_frame.pack_forget()

        # Actualizar estado
        self.current_step = step_num

        # Mostrar el paso correspondiente
        if step_num == 1:
            self.step1_frame.pack(fill=tk.BOTH, expand=True)
        elif step_num == 2:
            # Actualizar información de selección
            domain = self.get_selected_domain()
            table = self.get_selected_table()
            if domain and table:
                self.selection_info.config(text=f"Dominio: {domain} | Tabla: {table}")
            else:
                self.selection_info.config(text="Selecciona un dominio y tabla en el Paso 1")

            self.step2_frame.pack(fill=tk.BOTH, expand=True)
        elif step_num == 3:
            # Actualizar configuración final
            config_text = f"Dominio: {self.get_selected_domain()} | Tabla: {self.get_selected_table()}\n"
            config_text += f"Filas: {self.row_count.get()} | Errores: {self.error_profile.get()}\n"
            config_text += f"Salida: {self.output_dir.get()} | Formato: {self.output_format.get()}"
            self.final_config.config(text=config_text)

            self.step3_frame.pack(fill=tk.BOTH, expand=True)


def main():
    """Función principal"""
    root = tk.Tk()
    app = DataSynthesizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
