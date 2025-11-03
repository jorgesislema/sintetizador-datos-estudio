"""
Aplicación de escritorio nativa para el Sintetizador de Datos
Usando Tkinter para interfaz gráfica local
"""
import os
import calendar
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
import threading
import json
from datetime import datetime
import uuid

from core.generators import generate
from core.dq.profiler import profile
from core.integrity.scd2 import scd2_version_rows

# Importar sistema de localización
try:
    from core.localization import (
        get_available_contexts, get_region_options, 
        get_available_languages, get_language_display_names
    )
    LOCALIZATION_AVAILABLE = True
except ImportError:
    LOCALIZATION_AVAILABLE = False

# Importar sistema de ecosistemas
try:
    from core.ecosystems import (
        get_available_ecosystem_options,
        generate_ecosystem_data
    )
    ECOSYSTEMS_AVAILABLE = True
except ImportError:
    ECOSYSTEMS_AVAILABLE = False


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
        
        # ===== NUEVAS VARIABLES DE LOCALIZACIÓN =====
        self.language = tk.StringVar(value="Español")
        self.geographic_context = tk.StringVar(value="Global")
        
        # ===== RANGO DE FECHAS GLOBAL (YYYY-MM) =====
        # Por defecto: últimos 12 meses
        try:
            now = datetime.now()
            self.date_from_year = tk.IntVar(value=now.year - 1)
            self.date_from_month = tk.IntVar(value=now.month)
            self.date_to_year = tk.IntVar(value=now.year)
            self.date_to_month = tk.IntVar(value=now.month)
        except Exception:
            # Fallback conservador
            self.date_from_year = tk.IntVar(value=2023)
            self.date_from_month = tk.IntVar(value=1)
            self.date_to_year = tk.IntVar(value=2024)
            self.date_to_month = tk.IntVar(value=12)
        
        # Mapa de nombres de meses para UI mejorada
        self.month_names = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }
        self.month_display_to_num = {v: k for k, v in self.month_names.items()}
        
        # ===== VARIABLES DE SESIÓN =====
        self.current_session_id = None
        self.session_folder = None
        
        # ===== VARIABLES DE ECOSISTEMAS =====
        self.mode = tk.StringVar(value="single")  # "single" o "ecosystem"
        self.selected_ecosystem = tk.StringVar()
        self.ecosystem_volume = tk.IntVar(value=1000)
        # Auto-recalculo de descripción al cambiar volumen base
        try:
            self.ecosystem_volume.trace_add('write', lambda *args: self.update_ecosystem_mode_info())
        except Exception:
            pass
        
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
        """Crear el Paso 1: Selección de Modo y Datos"""
        self.step1_frame = ttk.Frame(self.steps_container)

        step_label = ttk.Label(self.step1_frame, text="Paso 1: Selección de Modo y Datos",
                              style="Step.TLabel")
        step_label.pack(pady=(0, 20))

        # Frame de selección de modo
        mode_frame = ttk.LabelFrame(self.step1_frame, text="Modo de Generación", padding="10")
        mode_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Radio buttons para seleccionar modo
        ttk.Radiobutton(mode_frame, text="📊 Tabla Individual", 
                       variable=self.mode, value="single",
                       command=self.on_mode_changed).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(mode_frame, text="🏢 Ecosistema de Negocio Completo", 
                       variable=self.mode, value="ecosystem",
                       command=self.on_mode_changed).pack(anchor=tk.W, pady=2)

        # Frame de selección (cambia según el modo)
        self.selection_frame = ttk.LabelFrame(self.step1_frame, text="Selección", padding="10")
        self.selection_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Contenido dinámico según el modo
        self.single_mode_frame = ttk.Frame(self.selection_frame)
        self.ecosystem_mode_frame = ttk.Frame(self.selection_frame)
        
        self.create_single_mode_widgets()
        self.create_ecosystem_mode_widgets()

        # Navegación temprana (el botón estaba arriba para mayor visibilidad)
        nav_step1 = ttk.Frame(self.step1_frame)
        nav_step1.pack(fill=tk.X, pady=(10, 5))
        self.continue_btn = ttk.Button(nav_step1, text="Continuar al Paso 2", command=lambda: self.show_step(2), state='disabled')
        self.continue_btn.pack(side=tk.RIGHT)

        self.info_frame = ttk.LabelFrame(self.step1_frame, text="Descripción / Información", padding="10")
        self.info_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        # Área de texto para mostrar información (altura mayor porque el botón está separado)
        self.info_text = scrolledtext.ScrolledText(self.info_frame, height=14, width=80, wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        self.info_text.insert(tk.END, "Selecciona un modo de generación para comenzar...")

        # Mostrar modo por defecto
        self.on_mode_changed()

        # Barra de progreso pasiva (informativa) una sola vez
        passive_frame = ttk.Frame(self.step1_frame)
        passive_frame.pack(fill=tk.X, pady=(5, 10))
        ttk.Label(passive_frame, text="Progreso (se activa en Paso 2):").pack(anchor=tk.W)
        self.passive_progress = ttk.Progressbar(passive_frame, maximum=100, value=0)
        self.passive_progress.pack(fill=tk.X)

    def create_single_mode_widgets(self):
        """Crear widgets para modo tabla individual"""
        # Dominio
        ttk.Label(self.single_mode_frame, text="Dominio:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.domain_combo = ttk.Combobox(self.single_mode_frame, textvariable=self.selected_domain,
                                        state="readonly", width=30)
        self.domain_combo.grid(row=0, column=1, padx=(10, 0), pady=5)
        self.domain_combo.bind("<<ComboboxSelected>>", self.on_domain_selected)

        # Tabla
        ttk.Label(self.single_mode_frame, text="Tabla:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.table_combo = ttk.Combobox(self.single_mode_frame, textvariable=self.selected_table,
                                       state="readonly", width=30)
        self.table_combo.grid(row=1, column=1, padx=(10, 0), pady=5)
        self.table_combo.bind("<<ComboboxSelected>>", self.on_table_selected)

    def create_ecosystem_mode_widgets(self):
        """Crear widgets para modo ecosistema"""
        # Ecosistema
        ttk.Label(self.ecosystem_mode_frame, text="Tipo de Negocio:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ecosystem_combo = ttk.Combobox(self.ecosystem_mode_frame, textvariable=self.selected_ecosystem,
                                           state="readonly", width=50)
        self.ecosystem_combo.grid(row=0, column=1, padx=(10, 0), pady=5)
        self.ecosystem_combo.bind("<<ComboboxSelected>>", self.on_ecosystem_selected)
        
        # Volumen base
        ttk.Label(self.ecosystem_mode_frame, text="Volumen Base:").grid(row=1, column=0, sticky=tk.W, pady=5)
        volume_frame = ttk.Frame(self.ecosystem_mode_frame)
        volume_frame.grid(row=1, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        ttk.Entry(volume_frame, textvariable=self.ecosystem_volume, width=10).pack(side=tk.LEFT)
        ttk.Label(volume_frame, text="registros (se escala automáticamente)").pack(side=tk.LEFT, padx=(5, 0))

    def on_mode_changed(self):
        """Manejar cambio de modo"""
        # Ocultar ambos frames
        self.single_mode_frame.pack_forget()
        self.ecosystem_mode_frame.pack_forget()
        
        if self.mode.get() == "single":
            # Mostrar modo tabla individual
            self.single_mode_frame.pack(fill=tk.X, expand=True)
            self.info_frame.config(text="Columnas Disponibles")
            self.update_single_mode_info()
            # Estado del botón continuar depende de selección
            if self.get_selected_domain() and self.get_selected_table():
                self.continue_btn.configure(state='normal')
            else:
                self.continue_btn.configure(state='disabled')
        else:
            # Mostrar modo ecosistema
            self.ecosystem_mode_frame.pack(fill=tk.X, expand=True)
            self.info_frame.config(text="Descripción del Ecosistema")
            self.load_ecosystems()
            self.update_ecosystem_mode_info()
            # Habilitar sólo si hay ecosistema seleccionado
            if self.selected_ecosystem.get():
                self.continue_btn.configure(state='normal')
            else:
                self.continue_btn.configure(state='disabled')
        # Guardar preferencia de modo
        try:
            self._save_preferences()
        except Exception:
            pass
        # Si el usuario ya está en Paso 2, refrescar etiqueta
        if self.current_step == 2 and hasattr(self, 'selection_info'):
            if self.mode.get() == 'single':
                domain = self.get_selected_domain()
                table = self.get_selected_table()
                if domain and table:
                    self.selection_info.config(text=f"Dominio: {domain} | Tabla: {table}")
                else:
                    self.selection_info.config(text="Selecciona un dominio y tabla en el Paso 1")
            else:
                eco = self.selected_ecosystem.get() or '—'
                self.selection_info.config(text=f"Ecosistema seleccionado: {eco}")

    def load_ecosystems(self):
        """Cargar ecosistemas disponibles"""
        if ECOSYSTEMS_AVAILABLE:
            try:
                ecosystems = get_available_ecosystem_options()
                self.ecosystem_combo['values'] = list(ecosystems.values())
                
                # Mapear display name a key
                self.ecosystem_display_map = {v: k for k, v in ecosystems.items()}
                
            except Exception as e:
                self.ecosystem_combo['values'] = ["Error cargando ecosistemas"]
                print(f"Error cargando ecosistemas: {e}")
        else:
            self.ecosystem_combo['values'] = ["Sistema de ecosistemas no disponible"]

    def on_ecosystem_selected(self, event=None):
        """Manejar selección de ecosistema"""
        self.update_ecosystem_mode_info()
        if self.selected_ecosystem.get():
            self.continue_btn.configure(state='normal')
        else:
            self.continue_btn.configure(state='disabled')

    def update_single_mode_info(self):
        """Actualizar información del modo tabla individual"""
        self.info_text.delete(1.0, tk.END)
        
        if self.get_selected_domain() and self.get_selected_table():
            # Mostrar información de columnas como antes
            self.on_table_selected()
        else:
            self.info_text.insert(tk.END, "Selecciona un dominio y tabla para ver las columnas disponibles...")

    def update_ecosystem_mode_info(self):
        """Actualizar información del modo ecosistema"""
        self.info_text.delete(1.0, tk.END)
        
        selected_display = self.selected_ecosystem.get()
        if not selected_display or not ECOSYSTEMS_AVAILABLE:
            self.info_text.insert(tk.END, "Selecciona un tipo de negocio para ver la descripción del ecosistema...")
            return
            
        try:
            # Obtener la clave del ecosistema
            ecosystem_key = self.ecosystem_display_map.get(selected_display)
            if not ecosystem_key:
                return
                
            from core.ecosystems import get_ecosystem_by_key
            ecosystem = get_ecosystem_by_key(ecosystem_key)
            
            if ecosystem:
                info_text = f"🏢 {ecosystem.display_name}\n\n"
                info_text += f"📋 Descripción:\n{ecosystem.description}\n\n"
                info_text += f"📊 Entidades Maestras:\n"
                for entity in ecosystem.master_entities:
                    info_text += f"   • {entity}\n"
                info_text += f"\n🗃️ Tablas Principales:\n"
                for domain, tables in ecosystem.core_tables.items():
                    for table in tables:
                        info_text += f"   • {table} ({domain})\n"
                info_text += f"\n🔧 Tablas de Soporte:\n"
                for domain, tables in ecosystem.support_tables.items():
                    for table in tables:
                        info_text += f"   • {table} ({domain})\n"
                info_text += f"\n📈 Tablas de Análisis:\n"
                for domain, tables in ecosystem.analytics_tables.items():
                    for table in tables:
                        info_text += f"   • {table} ({domain})\n"
                
                # Calcular volumen estimado basado en volume_ratios
                # Usar volumen específico del ecosistema; fallback al de tabla individual si existiera
                try:
                    base_volume = int(self.ecosystem_volume.get() or 1000)
                except Exception:
                    # Fallback defensivo: variable original para tablas individuales
                    try:
                        base_volume = int(self.row_count.get() or 1000)
                    except Exception:
                        base_volume = 1000
                total_estimated_records = 0
                table_volume_lines = []
                for table, ratio in ecosystem.volume_ratios.items():
                    table_volume = int(base_volume * ratio)
                    total_estimated_records += table_volume
                    table_volume_lines.append(f"   • {table}: {table_volume:,}")
                info_text += f"\n💾 Volumen Total Estimado: {total_estimated_records:,} registros"
                info_text += "\n📊 Distribución Estimada por Tabla:\n" + "\n".join(table_volume_lines)
                
                self.info_text.insert(tk.END, info_text)
                
        except Exception as e:
            self.info_text.insert(tk.END, f"Error cargando información del ecosistema: {e}")

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

        # Fila 2b: Número de sucursales (si aplica)
        ttk.Label(config_frame, text="Número de Sucursales:").grid(row=1, column=5, sticky=tk.W, pady=5)
        if not hasattr(self, 'branch_count'):
            self.branch_count = tk.IntVar(value=10)
        ttk.Spinbox(config_frame, from_=1, to=10000, textvariable=self.branch_count,
                    width=8).grid(row=1, column=6, padx=(10, 0), pady=5)

        # Fila 3: Rango de fechas global
        ttk.Label(config_frame, text="Rango de Fechas (YYYY-MM):").grid(row=2, column=0, sticky=tk.W, pady=10)
        date_range_frame = ttk.Frame(config_frame)
        date_range_frame.grid(row=2, column=1, columnspan=4, sticky=tk.W)
        
        # Desde
        ttk.Label(date_range_frame, text="Desde:").pack(side=tk.LEFT)
        from_year = ttk.Spinbox(date_range_frame, from_=1970, to=2100, textvariable=self.date_from_year, width=6)
        from_year.pack(side=tk.LEFT, padx=(5, 2))
        
        # Combobox para mes con nombres
        self.date_from_month_display = tk.StringVar(value=self.month_names[self.date_from_month.get()])
        from_month = ttk.Combobox(date_range_frame, textvariable=self.date_from_month_display,
                                  values=list(self.month_names.values()), state="readonly", width=12)
        from_month.pack(side=tk.LEFT, padx=(2, 10))
        from_month.bind('<<ComboboxSelected>>', lambda e: self._update_month_from_display('from'))
        
        # Hasta
        ttk.Label(date_range_frame, text="Hasta:").pack(side=tk.LEFT)
        to_year = ttk.Spinbox(date_range_frame, from_=1970, to=2100, textvariable=self.date_to_year, width=6)
        to_year.pack(side=tk.LEFT, padx=(5, 2))
        
        # Combobox para mes con nombres
        self.date_to_month_display = tk.StringVar(value=self.month_names[self.date_to_month.get()])
        to_month = ttk.Combobox(date_range_frame, textvariable=self.date_to_month_display,
                                values=list(self.month_names.values()), state="readonly", width=12)
        to_month.pack(side=tk.LEFT, padx=(2, 10))
        to_month.bind('<<ComboboxSelected>>', lambda e: self._update_month_from_display('to'))
        
        apply_date_btn = ttk.Button(date_range_frame, text="Aplicar Rango", command=self.apply_date_range)
        apply_date_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Atajos rápidos para rangos comunes
        ttk.Label(date_range_frame, text="│").pack(side=tk.LEFT, padx=(15, 5))
        ttk.Button(date_range_frame, text="Último Mes", width=10,
                  command=lambda: self._set_quick_range('last_month')).pack(side=tk.LEFT, padx=2)
        ttk.Button(date_range_frame, text="Último Año", width=10,
                  command=lambda: self._set_quick_range('last_year')).pack(side=tk.LEFT, padx=2)
        ttk.Button(date_range_frame, text="Este Año", width=10,
                  command=lambda: self._set_quick_range('this_year')).pack(side=tk.LEFT, padx=2)

        # ===== NUEVA SECCIÓN DE LOCALIZACIÓN =====
        if LOCALIZATION_AVAILABLE:
            localization_frame = ttk.LabelFrame(self.step2_frame, text="Configuración Regional", padding="10")
            localization_frame.pack(fill=tk.X, pady=(20, 0))

            # Fila 1: Idioma y Contexto Geográfico
            ttk.Label(localization_frame, text="Idioma de Columnas:").grid(row=0, column=0, sticky=tk.W, pady=5)
            language_combo = ttk.Combobox(localization_frame, textvariable=self.language,
                                        values=["English", "Español"], state="readonly", width=12)
            language_combo.grid(row=0, column=1, padx=(10, 20), pady=5)

            ttk.Label(localization_frame, text="Referencia Geográfica:").grid(row=0, column=2, sticky=tk.W, pady=5)
            
            # Crear lista de opciones geográficas organizadas
            geo_options = self._get_geographic_options()
            geo_combo = ttk.Combobox(localization_frame, textvariable=self.geographic_context,
                                    values=geo_options, state="readonly", width=20)
            geo_combo.grid(row=0, column=3, padx=(10, 0), pady=5)

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

        # Botón Nueva Sesión
        new_session_button = ttk.Button(gen_controls_frame, text="Nueva Sesión",
                  command=self.start_new_session_ui)
        new_session_button.pack(side=tk.RIGHT, padx=(0, 10))

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

        # Información de sesión
        self.session_info_label = ttk.Label(generation_frame, text="Sin sesión activa", foreground="gray")
        self.session_info_label.pack(pady=(2, 0))

        # Navegación
        nav_frame = ttk.Frame(self.step2_frame)
        nav_frame.pack(fill=tk.X, pady=20)

        ttk.Button(nav_frame, text="Volver al Paso 1",
                  command=lambda: self.show_step(1)).pack(side=tk.LEFT)
        ttk.Button(nav_frame, text="Ver Resultados",
                  command=lambda: self.show_step(3)).pack(side=tk.RIGHT)

    def _apply_date_range_to_engine(self):
        """Aplicar el rango de fechas global al motor faker_engine."""
        try:
            from core.engines.faker_engine import set_date_range
        except ImportError:
            return
        y1 = int(self.date_from_year.get())
        m1 = int(self.date_from_month.get())
        y2 = int(self.date_to_year.get())
        m2 = int(self.date_to_month.get())
        # Normalizar y construir YYYY-MM-01 y fin de mes
        if (y2, m2) < (y1, m1):
            y1, m1, y2, m2 = y2, m2, y1, m1
        start = f"{y1:04d}-{m1:02d}-01"
        last_day = calendar.monthrange(y2, m2)[1]
        end = f"{y2:04d}-{m2:02d}-{last_day:02d}"
        set_date_range(start, end)

    def _update_month_from_display(self, which):
        """Sincronizar el valor numérico del mes desde el nombre mostrado."""
        if which == 'from':
            month_name = self.date_from_month_display.get()
            if month_name in self.month_display_to_num:
                self.date_from_month.set(self.month_display_to_num[month_name])
        else:  # 'to'
            month_name = self.date_to_month_display.get()
            if month_name in self.month_display_to_num:
                self.date_to_month.set(self.month_display_to_num[month_name])
    
    def _set_quick_range(self, range_type):
        """Establecer un rango de fechas predefinido."""
        now = datetime.now()
        
        if range_type == 'last_month':
            # Mes pasado
            if now.month == 1:
                from_year, from_month = now.year - 1, 12
            else:
                from_year, from_month = now.year, now.month - 1
            to_year, to_month = from_year, from_month
            
        elif range_type == 'last_year':
            # Últimos 12 meses
            from_year = now.year - 1 if now.month == 1 else now.year
            from_month = now.month
            to_year, to_month = now.year, now.month
            
        elif range_type == 'this_year':
            # Este año (enero hasta hoy)
            from_year, from_month = now.year, 1
            to_year, to_month = now.year, now.month
        else:
            return
        
        # Actualizar valores
        self.date_from_year.set(from_year)
        self.date_from_month.set(from_month)
        self.date_to_year.set(to_year)
        self.date_to_month.set(to_month)
        
        # Actualizar displays de meses
        self.date_from_month_display.set(self.month_names[from_month])
        self.date_to_month_display.set(self.month_names[to_month])
        
        # Aplicar automáticamente
        self._apply_date_range_to_engine()
        
        # Mostrar confirmación
        range_desc = {
            'last_month': 'Último Mes',
            'last_year': 'Últimos 12 Meses',
            'this_year': 'Este Año'
        }
        messagebox.showinfo("Rango Rápido", 
                          f"Rango '{range_desc[range_type]}' aplicado:\n"
                          f"{from_year}-{from_month:02d} a {to_year}-{to_month:02d}")

    def apply_date_range(self):
        """Validar y aplicar el rango de fechas desde la UI."""
        try:
            y1 = int(self.date_from_year.get()); m1 = int(self.date_from_month.get())
            y2 = int(self.date_to_year.get()); m2 = int(self.date_to_month.get())
            if not (1 <= m1 <= 12 and 1 <= m2 <= 12):
                raise ValueError("Mes fuera de rango")
        except Exception:
            messagebox.showerror("Error", "Rango de fechas inválido. Use años válidos y meses 1-12.")
            return
        self._apply_date_range_to_engine()
        messagebox.showinfo("Rango aplicado", "El rango de fechas ha sido aplicado para la generación.")

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
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"Selecciona una tabla del dominio '{domain}' para ver las columnas disponibles...")
        except Exception as e:
            self.table_combo['values'] = []
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"Error cargando tablas del dominio '{domain}': {str(e)}")
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
            self.continue_btn.configure(state='normal')
        else:
            self.continue_btn.configure(state='disabled')

    def show_table_columns(self, domain: str, table: str):
        """Mostrar las columnas disponibles para la tabla seleccionada"""
        try:
            from core.utils.schemas import load_table_schema

            schema = load_table_schema(domain, table)
            fields = schema.get("fields", {})

            # Limpiar área de texto
            self.info_text.delete(1.0, tk.END)

            # Título
            self.info_text.insert(tk.END, f"Dominio: {domain.upper()}\n", "title")
            self.info_text.insert(tk.END, f"Tabla: {table}\n\n", "title")

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

            self.info_text.insert(tk.END, "CAMPOS COMUNES (siempre incluidos):\n", "header")
            for field in common_fields:
                self.info_text.insert(tk.END, f"• {field}\n")
            self.info_text.insert(tk.END, "\n")

            # Campos específicos de la tabla
            if fields:
                self.info_text.insert(tk.END, "CAMPOS ESPECIFICOS DE LA TABLA:\n", "header")
                for field_name, field_config in fields.items():
                    field_type = field_config.get("type", "string")
                    description = field_config.get("description", "")
                    if description:
                        self.info_text.insert(tk.END, f"• {field_name} ({field_type}): {description}\n")
                    else:
                        self.info_text.insert(tk.END, f"• {field_name} ({field_type})\n")
            else:
                self.info_text.insert(tk.END, "No hay campos específicos definidos para esta tabla.\n")

            # Configurar tags para formato
            self.info_text.tag_configure("title", font=("Arial", 12, "bold"), foreground="#1f77b4")
            self.info_text.tag_configure("header", font=("Arial", 10, "bold"), foreground="#2ca02c")

        except Exception as e:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"Error cargando esquema: {str(e)}")
            messagebox.showerror("Error", f"Error cargando esquema de la tabla: {str(e)}")

    def select_output_dir(self):
        """Seleccionar directorio de salida"""
        dir_path = filedialog.askdirectory(title="Seleccionar directorio de salida")
        if dir_path:
            self.output_dir.set(dir_path)

    def generate_preview(self):
        """Generar preview de datos"""
        # En modo ecosistema no se muestra popup: simplemente salir silenciosamente
        if self.mode.get() == 'ecosystem':
            return
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

                # Configurar contexto de localización si está disponible
                if LOCALIZATION_AVAILABLE and hasattr(self, 'geographic_context') and self.geographic_context.get() != "Global":
                    try:
                        from core.engines.faker_engine import set_geographic_context
                        context_key = self._get_context_key_from_display(self.geographic_context.get())
                        set_geographic_context(context_key)
                    except ImportError:
                        pass  # Fallar silenciosamente si no está disponible
                # Aplicar rango de fechas global
                self._apply_date_range_to_engine()
                
                # Generar datos
                data = generate(domain, table, rows, error_profile=self.error_profile.get())
                
                # Aplicar traducciones si se seleccionó español y está disponible
                if LOCALIZATION_AVAILABLE and hasattr(self, 'language') and self.language.get() == "Español":
                    try:
                        from core.localization.i18n import translate_complete_dataset
                        data = translate_complete_dataset(data, "es")
                    except ImportError:
                        pass  # Fallar silenciosamente si no está disponible

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
        """Generar dataset completo (tabla individual o ecosistema)"""
        mode = self.mode.get()
        
        if mode == "single":
            return self.generate_single_table()
        elif mode == "ecosystem":
            return self.generate_ecosystem_complete()
        else:
            messagebox.showerror("Error", "Modo de generación no válido")

    def generate_single_table(self):
        """Generar tabla individual"""
        if not self.get_selected_domain() or not self.get_selected_table():
            messagebox.showerror("Error", "Selecciona un dominio y tabla primero")
            return

        # Actualizar barra de progreso
        self.progress_var.set(0)
        self.status_label.config(text="Iniciando generación de tabla individual...")

        def generate_thread():
            try:
                domain = self.get_selected_domain()
                table = self.get_selected_table()
                rows = self.row_count.get()
                # Si es tabla de sucursales/tiendas, sobreescribir con branch_count
                try:
                    tname = (table or "").lower()
                    if tname in ("dim_store", "dim_branch") or any(x in tname for x in ["store", "branch"]):
                        rows = int(self.branch_count.get())
                except Exception:
                    pass

                # Paso 1: Configurar localización
                self.root.after(0, lambda: self.status_label.config(text="Configurando localización..."))
                self.root.after(0, lambda: self.progress_var.set(10))
                
                # Configurar contexto geográfico si está disponible
                if LOCALIZATION_AVAILABLE and hasattr(self, 'geographic_context') and self.geographic_context.get() != "Global":
                    try:
                        from core.engines.faker_engine import set_geographic_context
                        context_key = self._get_context_key_from_display(self.geographic_context.get())
                        set_geographic_context(context_key)
                    except ImportError:
                        pass  # Fallar silenciosamente si no está disponible

                self.root.after(0, lambda: self.status_label.config(text="Generando datos..."))
                self.root.after(0, lambda: self.progress_var.set(20))

                # Aplicar rango de fechas global
                self._apply_date_range_to_engine()

                data = generate(domain, table, rows, error_profile=self.error_profile.get())
                
                # Aplicar traducciones si se seleccionó español y está disponible
                if LOCALIZATION_AVAILABLE and hasattr(self, 'language') and self.language.get() == "Español":
                    try:
                        from core.localization.i18n import translate_complete_dataset
                        data = translate_complete_dataset(data, "es")
                    except ImportError:
                        pass  # Fallar silenciosamente si no está disponible

                # Paso 2: Aplicar SCD2 si está habilitado
                if self.scd2_enabled.get():
                    self.root.after(0, lambda: self.status_label.config(text="Aplicando SCD2..."))
                    self.root.after(0, lambda: self.progress_var.set(40))
                    data = scd2_version_rows(data, change_prob=0.2)

                # Paso 3: Guardar archivo
                self.root.after(0, lambda: self.status_label.config(text="Guardando archivo..."))
                self.root.after(0, lambda: self.progress_var.set(60))

                # Crear carpeta de sesión
                session_folder = self.create_session_folder()
                
                format_ext = self.output_format.get()
                out_file = session_folder / f"{domain}__{table}.{format_ext}"

                # Guardar archivo
                df = pd.DataFrame(data)
                saved_path = self._save_dataframe(df, out_file, format_ext)

                # Registrar tabla en la sesión con la ruta efectiva
                self.add_table_to_session(domain, table, saved_path, len(data))

                # Paso 4: Calcular métricas DQ
                self.root.after(0, lambda: self.status_label.config(text="Calculando métricas DQ..."))
                self.root.after(0, lambda: self.progress_var.set(80))

                dq_metrics = profile(data)

                # Paso 5: Finalizar
                self.root.after(0, lambda: self.progress_var.set(100))
                self.root.after(0, lambda: self.status_label.config(text="¡Tabla generada exitosamente!"))

                # Mostrar resultados usando la ruta efectiva
                self.root.after(0, lambda: self.show_generation_results(data, dq_metrics, saved_path))

            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Error generando tabla: {str(e)}"))
                self.root.after(0, lambda: self.status_label.config(text="Error en generación"))

        threading.Thread(target=generate_thread, daemon=True).start()

    # ================= Preferencias de Usuario =================
    def _preferences_path(self) -> Path:
        try:
            return Path.home() / '.sintetizador_settings.json'
        except Exception:
            return Path('.') / '.sintetizador_settings.json'

    def _load_preferences(self):  # ya definida más arriba en parche anterior, proteger duplicado
        if hasattr(self, '_prefs_loaded_marker'):
            return
        self._prefs_loaded_marker = True
        path = self._preferences_path()
        if not path.exists():
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            saved_mode = data.get('last_mode')
            if saved_mode in ('single','ecosystem'):
                self.mode.set(saved_mode)
            saved_ecosystem_key = data.get('last_ecosystem_key')
            if saved_ecosystem_key:
                from core.ecosystems import get_available_ecosystem_options
                ecosystems = get_available_ecosystem_options()
                display_name = ecosystems.get(saved_ecosystem_key)
                if display_name:
                    self.selected_ecosystem.set(display_name)
            self.on_mode_changed()
        except Exception:
            pass

    def _save_preferences(self):  # redefinida para asegurar existencia
        data = {
            'last_mode': self.mode.get(),
            'last_ecosystem_key': None
        }
        if hasattr(self, 'ecosystem_display_map') and self.selected_ecosystem.get():
            data['last_ecosystem_key'] = self.ecosystem_display_map.get(self.selected_ecosystem.get())
        try:
            with open(self._preferences_path(), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def generate_ecosystem_complete(self):
        """Generar ecosistema completo de negocio"""
        selected_display = self.selected_ecosystem.get()
        if not selected_display:
            messagebox.showerror("Error", "Selecciona un tipo de negocio primero")
            return

        if not ECOSYSTEMS_AVAILABLE:
            messagebox.showerror("Error", "Sistema de ecosistemas no disponible")
            return

        # Actualizar barra de progreso
        self.progress_var.set(0)
        self.status_label.config(text="Iniciando generación de ecosistema...")

        def generate_thread():
            try:
                # Obtener configuración
                ecosystem_key = self.ecosystem_display_map.get(selected_display)
                volume = self.ecosystem_volume.get()
                apply_translation = (LOCALIZATION_AVAILABLE and 
                                   hasattr(self, 'language') and 
                                   self.language.get() == "Español")

                # Estimar volumen total antes de generar para advertir
                from core.ecosystems import get_ecosystem_by_key
                eco_def = get_ecosystem_by_key(ecosystem_key)
                est_total = 0
                for t, r in eco_def.volume_ratios.items():
                    try:
                        est_total += int(volume * r)
                    except Exception:
                        pass
                if est_total > 2_000_000:
                    proceed = messagebox.askyesno(
                        "Confirmación de Volumen",
                        f"El volumen estimado es {est_total:,} registros (alto).\n\n¿Deseas continuar?"
                    )
                    if not proceed:
                        self.root.after(0, lambda: self.status_label.config(text="Generación cancelada por el usuario"))
                        return

                # Paso 1: Configurar localización
                self.root.after(0, lambda: self.status_label.config(text="Configurando localización..."))
                self.root.after(0, lambda: self.progress_var.set(5))
                
                if LOCALIZATION_AVAILABLE and hasattr(self, 'geographic_context') and self.geographic_context.get() != "Global":
                    try:
                        from core.engines.faker_engine import set_geographic_context
                        context_key = self._get_context_key_from_display(self.geographic_context.get())
                        set_geographic_context(context_key)
                    except ImportError:
                        pass

                # Paso 2: Generar ecosistema completo
                self.root.after(0, lambda: self.status_label.config(text="Generando ecosistema completo..."))
                self.root.after(0, lambda: self.progress_var.set(10))

                # Aplicar rango de fechas global
                self._apply_date_range_to_engine()

                # Pasar número de sucursales si está configurado
                branch_count = None
                try:
                    branch_count = int(self.branch_count.get()) if hasattr(self, 'branch_count') else None
                except Exception:
                    branch_count = None

                ecosystem_data, summary = generate_ecosystem_data(
                    ecosystem_key,
                    volume,
                    apply_translation,
                    branch_count=branch_count
                )

                # Paso 3: Crear carpeta de sesión
                self.root.after(0, lambda: self.status_label.config(text="Organizando archivos..."))
                self.root.after(0, lambda: self.progress_var.set(70))

                session_folder = self.create_session_folder()
                
                # Guardar todas las tablas del ecosistema
                format_ext = self.output_format.get()
                saved_files = {}
                
                total_tables = len(ecosystem_data)
                for i, (table_name, data) in enumerate(ecosystem_data.items()):
                    if data:  # Solo guardar si hay datos
                        progress = 70 + (i / max(total_tables,1)) * 20
                        self.root.after(0, lambda p=progress, t=table_name: (
                            self.progress_var.set(p),
                            self.status_label.config(text=f"Guardando {t}...")
                        ))
                        
                        out_file = session_folder / f"ecosystem__{table_name}.{format_ext}"
                        df = pd.DataFrame(data)
                        saved_path = self._save_dataframe(df, out_file, format_ext)
                        
                        # Registrar en sesión con la ruta efectiva
                        self.add_table_to_session("ecosystem", table_name, saved_path, len(data))
                        saved_files[table_name] = saved_path

                # Paso 4: Generar diccionario de datos en Español
                try:
                    from src.utils.data_dictionary_es import generate_data_dictionary_es
                    self.root.after(0, lambda: self.status_label.config(text="Creando diccionario de datos (ES)..."))
                    self.root.after(0, lambda: self.progress_var.set(92))
                    dicc_dir = generate_data_dictionary_es(saved_files, session_folder)
                except Exception as e:
                    # No bloquear la generación si falla el diccionario
                    dicc_dir = None
                    try:
                        self.root.after(0, lambda: messagebox.showwarning(
                            "Diccionario no generado",
                            f"Ocurrió un problema generando el diccionario de datos (ES).\nDetalle: {e}"
                        ))
                    except Exception:
                        pass

                # Paso 5: Guardar resumen del ecosistema
                self.root.after(0, lambda: self.status_label.config(text="Guardando metadatos..."))
                self.root.after(0, lambda: self.progress_var.set(95))

                summary_file = session_folder / "ecosystem_summary.json"
                with open(summary_file, 'w', encoding='utf-8') as f:
                    json.dump(summary, f, indent=2, ensure_ascii=False)

                # Paso 6: Finalizar
                self.root.after(0, lambda: self.progress_var.set(100))
                self.root.after(0, lambda: self.status_label.config(text="¡Ecosistema generado exitosamente!"))

                # Mostrar resultados del ecosistema
                self.root.after(0, lambda: self.show_ecosystem_results(ecosystem_data, summary, saved_files))

            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Error generando ecosistema: {str(e)}"))
                self.root.after(0, lambda: self.status_label.config(text="Error en generación"))

        threading.Thread(target=generate_thread, daemon=True).start()

    def _save_dataframe(self, df: pd.DataFrame, out_file: Path, format_ext: str) -> Path:
        """Guardar DataFrame en el formato especificado.
        Retorna la ruta efectiva del archivo guardado. Realiza fallback a CSV si el formato falla.
        """
        try:
            if format_ext == "csv":
                df.to_csv(out_file, index=False)
                return out_file
            elif format_ext == "json":
                df.to_json(out_file, orient='records', indent=2)
                return out_file
            elif format_ext == "excel":
                try:
                    import openpyxl  # type: ignore  # noqa: F401
                except Exception:
                    # Fallback: guardar como CSV si no hay engine Excel
                    fallback = out_file.with_suffix('.csv')
                    df.to_csv(fallback, index=False)
                    # Avisar al usuario de la degradación de formato
                    try:
                        self.root.after(0, lambda: messagebox.showwarning(
                            "Excel no disponible",
                            f"No se encontró openpyxl. Archivo guardado como CSV:\n{fallback}"
                        ))
                    except Exception:
                        pass
                    return fallback
                # Si openpyxl existe, proceder
                df.to_excel(out_file, index=False, engine='openpyxl')
                return out_file
            elif format_ext == "parquet":
                df.to_parquet(out_file, index=False)
                return out_file
            else:
                # Default to CSV
                df.to_csv(out_file, index=False)
                return out_file
        except Exception as e:
            # Fallback final a CSV con notificación
            try:
                fallback = out_file.with_suffix('.csv')
                df.to_csv(fallback, index=False)
                self.root.after(0, lambda: messagebox.showwarning(
                    "Error al guardar",
                    f"Se produjo un error guardando en formato '{format_ext}'.\n"
                    f"Se guardó como CSV: {fallback}\n\nDetalle: {e}"
                ))
                return fallback
            except Exception:
                # Re-lanzar si el fallback también falla
                raise

    def show_ecosystem_results(self, ecosystem_data: Dict, summary: Dict, saved_files: Dict):
        """Mostrar resultados de la generación de ecosistema"""
        # Resetear métricas (ya que son múltiples tablas)
        self.metrics_labels["Completitud"].config(text="N/A")
        self.metrics_labels["Duplicados"].config(text="N/A") 
        self.metrics_labels["Unicidad"].config(text="N/A")
        self.metrics_labels["Validez"].config(text="N/A")

        # Mostrar información del ecosistema
        result_text = f"🏢 ECOSISTEMA GENERADO EXITOSAMENTE!\n\n"
        result_text += f"📋 Tipo: {summary['ecosystem_name']}\n"
        result_text += f"📊 Total de tablas: {summary['total_tables']}\n"
        result_text += f"📈 Total de registros: {summary['total_records']:,}\n"
        result_text += f"📁 Carpeta: {self.session_folder.name if self.session_folder else 'N/A'}\n\n"

        result_text += "📊 TABLAS GENERADAS:\n"
        result_text += "="*50 + "\n"
        
        for table_name, record_count in summary['tables_summary'].items():
            result_text += f"   📄 {table_name}: {record_count:,} registros\n"

        result_text += f"\n🌐 Configuración:\n"
        result_text += f"   🗣️ Idioma: {self.language.get() if hasattr(self, 'language') else 'N/A'}\n"
        result_text += f"   🌍 Región: {self.geographic_context.get() if hasattr(self, 'geographic_context') else 'N/A'}\n"
        result_text += f"   📊 Volumen base: {self.ecosystem_volume.get():,}\n"
        try:
            result_text += f"   🏬 Sucursales: {int(self.branch_count.get())}\n"
        except Exception:
            pass
        result_text += f"   📆 Rango de fechas: {int(self.date_from_year.get()):04d}-{int(self.date_from_month.get()):02d} a {int(self.date_to_year.get()):04d}-{int(self.date_to_month.get()):02d}\n"

        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, result_text)

        # Guardar datos para descarga (usar la primera tabla como referencia)
        first_table_data = next(iter(ecosystem_data.values()), [])
        self.generated_data = first_table_data
        
        messagebox.showinfo("Éxito", 
                          f"¡Ecosistema '{summary['ecosystem_name']}' generado!\n\n"
                          f"📊 {summary['total_tables']} tablas creadas\n"
                          f"📈 {summary['total_records']:,} registros totales\n"
                          f"📁 Ubicación: {self.session_folder}")

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
        result_text += f"Configuración temporal: {int(self.date_from_year.get()):04d}-{int(self.date_from_month.get()):02d} a {int(self.date_to_year.get()):04d}-{int(self.date_to_month.get()):02d}\n\n"

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

    def create_session_folder(self):
        """Crear carpeta única para la sesión actual"""
        if not self.current_session_id:
            # Generar ID único para la sesión
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_uuid = str(uuid.uuid4())[:8]
            self.current_session_id = f"session_{timestamp}_{session_uuid}"
            
            # Actualizar UI
            self.session_info_label.config(text=f"Sesión activa: {self.current_session_id}")
        
        # Crear carpeta de sesión
        base_out_dir = Path(self.output_dir.get())
        self.session_folder = base_out_dir / self.current_session_id
        self.session_folder.mkdir(parents=True, exist_ok=True)
        
        # Crear archivo de metadatos de la sesión
        session_metadata = {
            "session_id": self.current_session_id,
            "created_at": datetime.now().isoformat(),
            "language": self.language.get(),
            "geographic_context": self.geographic_context.get(),
            # Persistir número de sucursales para auditoría de sesiones
            "branch_count": (int(self.branch_count.get()) if hasattr(self, 'branch_count') else None),
            "date_range": {
                "from": f"{int(self.date_from_year.get()):04d}-{int(self.date_from_month.get()):02d}",
                "to": f"{int(self.date_to_year.get()):04d}-{int(self.date_to_month.get()):02d}"
            },
            "tables_generated": []
        }
        
        metadata_file = self.session_folder / "session_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(session_metadata, f, indent=2, ensure_ascii=False)
        
        return self.session_folder

    def add_table_to_session(self, domain: str, table: str, file_path: str, row_count: int):
        """Agregar información de tabla generada a la sesión"""
        if not self.session_folder:
            return
            
        metadata_file = self.session_folder / "session_metadata.json"
        
        # Leer metadatos existentes
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Agregar nueva tabla
        table_info = {
            "domain": domain,
            "table": table,
            "file_path": str(file_path),
            "row_count": row_count,
            "generated_at": datetime.now().isoformat()
        }
        
        metadata["tables_generated"].append(table_info)
        
        # Guardar metadatos actualizados
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

    def start_new_session(self):
        """Iniciar una nueva sesión de generación"""
        self.current_session_id = None
        self.session_folder = None

    def start_new_session_ui(self):
        """Iniciar nueva sesión desde la UI"""
        self.start_new_session()
        
        # Actualizar UI
        self.session_info_label.config(text="Sin sesión activa")
        
        # Mostrar información sobre la nueva sesión
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        messagebox.showinfo("Nueva Sesión", 
                          f"Nueva sesión iniciada.\n\n"
                          f"Todas las tablas generadas a partir de ahora\n"
                          f"se guardarán en una carpeta única.\n\n"
                          f"Hora de inicio: {timestamp}")

    def open_results_folder(self):
        """Abrir la carpeta de resultados"""
        # Si hay una sesión activa, abrir esa carpeta específica
        if self.session_folder and self.session_folder.exists():
            target_dir = str(self.session_folder)
        else:
            target_dir = self.output_dir.get()
            
        if not target_dir or not os.path.exists(target_dir):
            messagebox.showwarning("Advertencia", "No hay carpeta de resultados válida")
            return
            
        try:
            import subprocess
            import sys
            
            if sys.platform == "win32":
                os.startfile(target_dir)
            elif sys.platform == "darwin":
                subprocess.call(["open", target_dir])
            else:
                subprocess.call(["xdg-open", target_dir])
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
            if self.mode.get() == 'single':
                domain = self.get_selected_domain()
                table = self.get_selected_table()
                if domain and table:
                    self.selection_info.config(text=f"Dominio: {domain} | Tabla: {table}")
                else:
                    self.selection_info.config(text="Selecciona un dominio y tabla en el Paso 1")
                # Asegurar que el frame de preview esté visible
                try:
                    if hasattr(self, 'preview_text'):
                        self.preview_text.master.master.pack(fill=tk.X, pady=(0, 20))
                except Exception:
                    pass
            else:
                eco = self.selected_ecosystem.get() or '—'
                self.selection_info.config(text=f"Ecosistema seleccionado: {eco} (preview deshabilitado)")
                # Ocultar frame de preview si existe
                try:
                    if hasattr(self, 'preview_text'):
                        self.preview_text.master.master.pack_forget()
                except Exception:
                    pass

            self.step2_frame.pack(fill=tk.BOTH, expand=True)
        elif step_num == 3:
            # Actualizar configuración final
            config_text = f"Dominio: {self.get_selected_domain()} | Tabla: {self.get_selected_table()}\n"
            config_text += f"Filas: {self.row_count.get()} | Errores: {self.error_profile.get()}\n"
            config_text += f"Salida: {self.output_dir.get()} | Formato: {self.output_format.get()}\n"
            config_text += f"Rango de fechas: {int(self.date_from_year.get()):04d}-{int(self.date_from_month.get()):02d} a {int(self.date_to_year.get()):04d}-{int(self.date_to_month.get()):02d}\n"
            try:
                config_text += f"Sucursales: {int(self.branch_count.get())}"
            except Exception:
                pass
            self.final_config.config(text=config_text)

            self.step3_frame.pack(fill=tk.BOTH, expand=True)

    def _get_geographic_options(self) -> List[str]:
        """Obtener opciones geográficas organizadas para el combobox"""
        if not LOCALIZATION_AVAILABLE:
            return ["Global"]
        
        try:
            from core.localization.geographic_contexts import get_region_options
            regions = get_region_options()
            
            options = []
            
            # Añadir Global primero
            options.append("Global")
            
            # Añadir Latinoamérica
            if "Latinoamérica" in regions:
                options.append("--- Latinoamérica ---")
                for country in regions["Latinoamérica"]:
                    country_display = {
                        "ecuador": "Ecuador",
                        "colombia": "Colombia", 
                        "mexico": "México",
                        "argentina": "Argentina",
                        "chile": "Chile",
                        "peru": "Perú"
                    }.get(country, country.title())
                    options.append(country_display)
            
            # Añadir Europa
            if "Europa" in regions:
                options.append("--- Europa ---")
                for country in regions["Europa"]:
                    country_display = {
                        "espana": "España",
                        "francia": "Francia",
                        "alemania": "Alemania", 
                        "italia": "Italia"
                    }.get(country, country.title())
                    options.append(country_display)
            
            # Añadir Norteamérica
            if "Norteamérica" in regions:
                options.append("--- Norteamérica ---")
                for country in regions["Norteamérica"]:
                    country_display = {
                        "usa": "Estados Unidos",
                        "canada": "Canadá"
                    }.get(country, country.title())
                    options.append(country_display)
                    
            return options
            
        except Exception:
            return ["Global", "Ecuador", "Colombia", "México", "España", "Estados Unidos"]

    def _get_context_key_from_display(self, display_name: str) -> str:
        """Convertir nombre mostrado a clave de contexto"""
        mapping = {
            "Global": "global",
            "Ecuador": "ecuador",
            "Colombia": "colombia", 
            "México": "mexico",
            "Argentina": "argentina",
            "Chile": "chile",
            "Perú": "peru",
            "España": "espana",
            "Francia": "francia",
            "Alemania": "alemania",
            "Italia": "italia", 
            "Estados Unidos": "usa",
            "Canadá": "canada"
        }
        return mapping.get(display_name, "global")

    def _get_language_key_from_display(self, display_name: str) -> str:
        """Convertir nombre de idioma mostrado a clave"""
        mapping = {
            "English": "en",
            "Español": "es"
        }
        return mapping.get(display_name, "en")


def main():
    """Función principal"""
    root = tk.Tk()
    app = DataSynthesizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
