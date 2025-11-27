import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
from generator import GrammarParser, TestCaseGenerator


class Application(tk.Tk):
    """Interfaz gráfica mejorada de la aplicación"""
    
    def __init__(self):
        super().__init__()
        
        self.title("Generador Automático de Casos de Prueba - GLC")
        self.geometry("1600x900")
        self.configure(bg='#f5f5f5')
        
        # Centrar ventana
        self.center_window()
        
        self.grammar_text = ""
        self.generator = None
        
        self.create_widgets()
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = 1600
        height = 900
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        # Título principal con estilo mejorado
        title_frame = tk.Frame(self, bg='#2c3e50', height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, 
                              text="🔧 Generador Automático de Casos de Prueba",
                              font=('Segoe UI', 18, 'bold'),
                              bg='#2c3e50',
                              fg='white')
        title_label.pack(pady=(15, 5))
        
        subtitle_label = tk.Label(title_frame,
                                 text="Gramáticas Libres de Contexto (GLC) • INFO1148",
                                 font=('Segoe UI', 10),
                                 bg='#2c3e50',
                                 fg='#95a5a6')
        subtitle_label.pack()
        
        # Frame principal con padding
        main_container = tk.Frame(self, bg='#f5f5f5')
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Frame principal
        main_frame = tk.Frame(main_container, bg='#f5f5f5')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configurar grid weights
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=2)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Panel izquierdo: Gramática
        left_container = tk.Frame(main_frame, bg='white', relief=tk.SOLID, bd=1)
        left_container.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 8))
        
        # Encabezado del panel izquierdo
        left_header = tk.Frame(left_container, bg='#ecf0f1', height=45)
        left_header.pack(fill=tk.X)
        left_header.pack_propagate(False)
        
        tk.Label(left_header, text="📝 Definición de Gramática (GLC)",
                font=('Segoe UI', 11, 'bold'),
                bg='#ecf0f1', fg='#2c3e50').pack(side=tk.LEFT, padx=15, pady=10)
        
        left_frame = tk.Frame(left_container, bg='white')
        left_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Botones de acción con mejor diseño
        btn_frame = tk.Frame(left_frame, bg='white')
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        btn_style = {
            'font': ('Segoe UI', 9),
            'relief': tk.FLAT,
            'bd': 0,
            'padx': 15,
            'pady': 8,
            'cursor': 'hand2'
        }
        
        btn_load = tk.Button(btn_frame, text="📁 Cargar Archivo", 
                            command=self.load_grammar,
                            bg='#3498db', fg='white',
                            activebackground='#2980b9',
                            **btn_style)
        btn_load.pack(side=tk.LEFT, padx=(0, 5))
        
        btn_example = tk.Button(btn_frame, text="📄 Ejemplo", 
                               command=self.load_example,
                               bg='#9b59b6', fg='white',
                               activebackground='#8e44ad',
                               **btn_style)
        btn_example.pack(side=tk.LEFT, padx=5)
        
        btn_clear_grammar = tk.Button(btn_frame, text="🗑️ Limpiar", 
                                      command=self.clear_grammar,
                                      bg='#e74c3c', fg='white',
                                      activebackground='#c0392b',
                                      **btn_style)
        btn_clear_grammar.pack(side=tk.LEFT, padx=5)
        
        # Instrucciones con mejor formato
        inst_frame = tk.Frame(left_frame, bg='#fff3cd', relief=tk.SOLID, bd=1)
        inst_frame.pack(fill=tk.X, pady=(0, 10))
        
        inst_label = tk.Label(inst_frame, 
                             text="💡 Formato: No-Terminal -> producción | producción\n"
                                  "   Ejemplo: E -> E + T | T",
                             font=('Segoe UI', 9),
                             justify=tk.LEFT,
                             bg='#fff3cd',
                             fg='#856404',
                             padx=10,
                             pady=8)
        inst_label.pack(fill=tk.X)
        
        # Text area para gramática con mejor estilo
        text_frame = tk.Frame(left_frame, bg='white', relief=tk.SOLID, bd=1)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.grammar_text_widget = scrolledtext.ScrolledText(text_frame, 
                                                             height=18, 
                                                             width=55,
                                                             font=('Consolas', 11),
                                                             wrap=tk.WORD,
                                                             relief=tk.FLAT,
                                                             padx=10,
                                                             pady=10,
                                                             bg='white',
                                                             fg='#2c3e50',
                                                             insertbackground='#3498db',
                                                             selectbackground='#3498db',
                                                             selectforeground='white')
        self.grammar_text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Panel derecho: Configuración
        right_container = tk.Frame(main_frame, bg='white', relief=tk.SOLID, bd=1)
        right_container.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=(0, 8))
        
        # Encabezado del panel derecho
        right_header = tk.Frame(right_container, bg='#ecf0f1', height=45)
        right_header.pack(fill=tk.X)
        right_header.pack_propagate(False)
        
        tk.Label(right_header, text="⚙️ Configuración de Generación",
                font=('Segoe UI', 11, 'bold'),
                bg='#ecf0f1', fg='#2c3e50').pack(side=tk.LEFT, padx=15, pady=10)
        
        right_frame = tk.Frame(right_container, bg='white')
        right_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Frame de 2 columnas
        columns_frame = tk.Frame(right_frame, bg='white')
        columns_frame.pack(fill=tk.BOTH, expand=True)
        
        # Columna izquierda: Configuraciones
        left_col = tk.Frame(columns_frame, bg='white')
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Columna derecha: Botones
        right_col = tk.Frame(columns_frame, bg='white')
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        
        # Sección: Cantidad de casos con mejor diseño
        section1 = tk.LabelFrame(left_col, text="  Cantidad de Casos  ", 
                                font=('Segoe UI', 10, 'bold'),
                                bg='white', fg='#2c3e50',
                                relief=tk.SOLID, bd=1,
                                padx=15, pady=8)
        section1.pack(fill=tk.X, pady=(0, 10))
        
        # Labels y spinboxes con mejor espaciado
        configs = [
            ("Casos Válidos:", 'valid_count', 10, '#27ae60'),
            ("Casos Inválidos:", 'invalid_count', 5, '#e67e22'),
            ("Casos Extremos:", 'extreme_count', 5, '#9b59b6')
        ]
        
        for label_text, attr_name, default_val, color in configs:
            row_frame = tk.Frame(section1, bg='white')
            row_frame.pack(fill=tk.X, pady=5)
            
            label = tk.Label(row_frame, text=label_text, 
                           font=('Segoe UI', 10),
                           bg='white', fg='#34495e',
                           width=15, anchor='w')
            label.pack(side=tk.LEFT)
            
            spinbox = ttk.Spinbox(row_frame, from_=1, to=100, width=12,
                                font=('Segoe UI', 10))
            spinbox.set(default_val)
            spinbox.pack(side=tk.LEFT, padx=(10, 0))
            setattr(self, attr_name, spinbox)
            
            # Indicador de color
            indicator = tk.Label(row_frame, text="●", font=('Arial', 12),
                               bg='white', fg=color)
            indicator.pack(side=tk.LEFT, padx=(10, 0))
        
        # Sección: Parámetros de generación
        section2 = tk.LabelFrame(left_col, text="  Parámetros de Generación  ",
                                font=('Segoe UI', 10, 'bold'),
                                bg='white', fg='#2c3e50',
                                relief=tk.SOLID, bd=1,
                                padx=15, pady=8)
        section2.pack(fill=tk.X, pady=(0, 10))
        
        params = [
            ("Profundidad Máxima:", 'max_depth', 5, 1, 15),
            ("Longitud Máxima:", 'max_length', 50, 10, 500)
        ]
        
        for label_text, attr_name, default_val, from_val, to_val in params:
            row_frame = tk.Frame(section2, bg='white')
            row_frame.pack(fill=tk.X, pady=5)
            
            label = tk.Label(row_frame, text=label_text,
                           font=('Segoe UI', 10),
                           bg='white', fg='#34495e',
                           width=15, anchor='w')
            label.pack(side=tk.LEFT)
            
            spinbox = ttk.Spinbox(row_frame, from_=from_val, to=to_val, width=12,
                                font=('Segoe UI', 10))
            spinbox.set(default_val)
            spinbox.pack(side=tk.LEFT, padx=(10, 0))
            setattr(self, attr_name, spinbox)
        
        # Información total con diseño mejorado
        total_frame = tk.Frame(left_col, bg='#e8f5e9', relief=tk.SOLID, bd=1)
        total_frame.pack(fill=tk.X, pady=(0, 0))
        
        self.total_label = tk.Label(total_frame,
                                    text="📊 Total a generar: 20 casos",
                                    font=('Segoe UI', 11, 'bold'),
                                    bg='#e8f5e9',
                                    fg='#2e7d32',
                                    padx=15,
                                    pady=12)
        self.total_label.pack(fill=tk.X)
        
        # Vincular eventos para actualizar total
        for widget in [self.valid_count, self.invalid_count, self.extreme_count]:
            widget.bind('<KeyRelease>', self.update_total)
            widget.bind('<<Increment>>', self.update_total)
            widget.bind('<<Decrement>>', self.update_total)
        
        # BOTONES EN LA COLUMNA DERECHA
        # Botón principal GENERAR con diseño destacado
        btn_generate = tk.Button(right_col,
                                text="🚀 GENERAR\nCASOS DE\nPRUEBA",
                                command=self.generate_cases,
                                bg='#27ae60',
                                fg='white',
                                font=('Segoe UI', 11, 'bold'),
                                relief=tk.FLAT,
                                bd=0,
                                padx=20,
                                pady=25,
                                cursor='hand2',
                                activebackground='#229954',
                                activeforeground='white',
                                width=12,
                                height=5)
        btn_generate.pack(pady=(0, 10))
        
        # Botón exportar
        btn_export = tk.Button(right_col,
                              text="💾 Exportar\na JSON",
                              command=self.export_json,
                              bg='#3498db',
                              fg='white',
                              font=('Segoe UI', 9),
                              relief=tk.FLAT,
                              bd=0,
                              padx=15,
                              pady=15,
                              cursor='hand2',
                              activebackground='#2980b9',
                              activeforeground='white',
                              width=12,
                              height=3)
        btn_export.pack(pady=(0, 10))
        
        # Botón limpiar
        btn_clear = tk.Button(right_col,
                             text="🔄 Limpiar\nResultados",
                             command=self.clear_results,
                             bg='#e67e22',
                             fg='white',
                             font=('Segoe UI', 9),
                             relief=tk.FLAT,
                             bd=0,
                             padx=15,
                             pady=15,
                             cursor='hand2',
                             activebackground='#d35400',
                             activeforeground='white',
                             width=12,
                             height=3)
        btn_clear.pack(pady=0)
        
        # Panel inferior: Resultados con más espacio
        bottom_container = tk.Frame(main_frame, bg='white', relief=tk.SOLID, bd=1)
        bottom_container.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(8, 0))
        
        # Encabezado del panel inferior
        bottom_header = tk.Frame(bottom_container, bg='#ecf0f1', height=45)
        bottom_header.pack(fill=tk.X)
        bottom_header.pack_propagate(False)
        
        tk.Label(bottom_header, text="📊 Resultados de Generación",
                font=('Segoe UI', 11, 'bold'),
                bg='#ecf0f1', fg='#2c3e50').pack(side=tk.LEFT, padx=15, pady=10)
        
        bottom_frame = tk.Frame(bottom_container, bg='white')
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Notebook para métricas y casos con estilo
        style = ttk.Style()
        style.configure('Custom.TNotebook', background='white', borderwidth=0)
        style.configure('Custom.TNotebook.Tab', padding=[20, 10], font=('Segoe UI', 10))
        
        self.notebook = ttk.Notebook(bottom_frame, style='Custom.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab de métricas
        metrics_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(metrics_frame, text="📈 Métricas y Estadísticas")
        
        self.metrics_text = scrolledtext.ScrolledText(metrics_frame, 
                                                      height=25,
                                                      font=('Consolas', 10),
                                                      wrap=tk.WORD,
                                                      relief=tk.FLAT,
                                                      padx=15,
                                                      pady=15,
                                                      bg='#fafafa',
                                                      fg='#2c3e50',
                                                      insertbackground='#3498db',
                                                      selectbackground='#3498db',
                                                      selectforeground='white')
        self.metrics_text.pack(fill=tk.BOTH, expand=True)
        
        # Tab de casos de prueba
        cases_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(cases_frame, text="📋 Casos de Prueba Generados")
        
        # Frame con búsqueda mejorado
        search_frame = tk.Frame(cases_frame, bg='#ecf0f1', relief=tk.FLAT)
        search_frame.pack(fill=tk.X)
        
        search_inner = tk.Frame(search_frame, bg='#ecf0f1')
        search_inner.pack(pady=12, padx=15)
        
        tk.Label(search_inner, text="🔍 Filtrar por tipo:", 
                font=('Segoe UI', 10, 'bold'),
                bg='#ecf0f1', fg='#2c3e50').pack(side=tk.LEFT, padx=(0, 10))
        
        self.filter_var = tk.StringVar(value="Todos")
        filter_combo = ttk.Combobox(search_inner, 
                                    textvariable=self.filter_var,
                                    values=["Todos", "válida", "inválida", "extrema"],
                                    state="readonly",
                                    font=('Segoe UI', 10),
                                    width=15)
        filter_combo.pack(side=tk.LEFT, padx=(0, 10))
        filter_combo.bind('<<ComboboxSelected>>', self.filter_cases)
        
        btn_filter = tk.Button(search_inner, text="Aplicar Filtro", 
                              command=self.filter_cases,
                              bg='#3498db', fg='white',
                              font=('Segoe UI', 9, 'bold'),
                              relief=tk.FLAT, bd=0,
                              padx=15, pady=6,
                              cursor='hand2',
                              activebackground='#2980b9',
                              activeforeground='white')
        btn_filter.pack(side=tk.LEFT)
        
        self.cases_text = scrolledtext.ScrolledText(cases_frame, 
                                                    height=25,
                                                    font=('Consolas', 10),
                                                    wrap=tk.WORD,
                                                    relief=tk.FLAT,
                                                    padx=15,
                                                    pady=15,
                                                    bg='#fafafa',
                                                    fg='#2c3e50',
                                                    insertbackground='#3498db',
                                                    selectbackground='#3498db',
                                                    selectforeground='white')
        self.cases_text.pack(fill=tk.BOTH, expand=True)
        
        # Barra de estado mejorada
        status_frame = tk.Frame(self, bg='#34495e', height=35)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame,
                                     text="⚡ Estado: Listo para generar casos de prueba",
                                     relief=tk.FLAT,
                                     anchor=tk.W,
                                     font=('Segoe UI', 9),
                                     bg='#34495e',
                                     fg='#ecf0f1',
                                     padx=15)
        self.status_label.pack(fill=tk.BOTH, expand=True)
        
        # Configurar grid weights para mejor distribución
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=2)
        main_frame.rowconfigure(1, weight=3)
    
    def update_total(self, event=None):
        """Actualiza el total de casos a generar"""
        try:
            valid = int(self.valid_count.get())
            invalid = int(self.invalid_count.get())
            extreme = int(self.extreme_count.get())
            total = valid + invalid + extreme
            self.total_label.config(text=f"📊 Total a generar: {total} casos")
        except:
            pass
    
    def clear_grammar(self):
        """Limpia el área de gramática"""
        self.grammar_text_widget.delete(1.0, tk.END)
        self.status_label.config(text="⚡ Estado: Gramática limpiada")
    
    def clear_results(self):
        """Limpia los resultados"""
        self.metrics_text.delete(1.0, tk.END)
        self.cases_text.delete(1.0, tk.END)
        self.generator = None
        self.status_label.config(text="⚡ Estado: Resultados limpiados")
    
    def filter_cases(self, event=None):
        """Filtra casos por tipo"""
        if not self.generator:
            return
        
        filter_type = self.filter_var.get()
        self.cases_text.delete(1.0, tk.END)
        
        cases_str = "=== CASOS DE PRUEBA GENERADOS ===\n\n"
        
        filtered_cases = self.generator.test_cases
        if filter_type != "Todos":
            filtered_cases = [c for c in self.generator.test_cases if c['type'] == filter_type]
        
        cases_str += f"Mostrando {len(filtered_cases)} de {len(self.generator.test_cases)} casos\n"
        cases_str += "=" * 80 + "\n\n"
        
        for case in filtered_cases:
            cases_str += f"ID: {case['id']} | Tipo: {case['type'].upper()}\n"
            cases_str += f"Expresión: {case['expression']}\n"
            
            if 'depth' in case:
                cases_str += f"Profundidad: {case['depth']}\n"
            if 'mutation' in case:
                cases_str += f"Mutación aplicada: {case['mutation']}\n"
            if 'extreme_type' in case:
                cases_str += f"Tipo extremo: {case['extreme_type']}\n"
            
            cases_str += "-" * 80 + "\n\n"
        
        self.cases_text.insert(1.0, cases_str)
    
    def load_grammar(self):
        """Carga gramática desde archivo"""
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de gramática",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.grammar_text_widget.delete(1.0, tk.END)
                    self.grammar_text_widget.insert(1.0, content)
                self.status_label.config(text=f"⚡ Estado: Gramática cargada desde {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")
                self.status_label.config(text="⚡ Estado: Error al cargar gramática")
    
    def load_example(self):
        """Carga gramática de ejemplo"""
        example = """E -> E + T | E - T | T
T -> T * F | T / F | T % F | F
F -> ( E ) | num"""
        
        self.grammar_text_widget.delete(1.0, tk.END)
        self.grammar_text_widget.insert(1.0, example)
        self.status_label.config(text="⚡ Estado: Gramática de ejemplo cargada")
    
    def generate_cases(self):
        """Genera casos de prueba"""
        grammar_text = self.grammar_text_widget.get(1.0, tk.END).strip()
        
        if not grammar_text:
            messagebox.showwarning("Advertencia", "Por favor ingrese una gramática")
            self.status_label.config(text="⚡ Estado: No hay gramática definida")
            return
        
        try:
            self.status_label.config(text="⏳ Estado: Generando casos de prueba...")
            self.update()
            
            # Parsear gramática
            grammar = GrammarParser(grammar_text)
            
            # Crear generador
            self.generator = TestCaseGenerator(grammar)
            
            # Obtener configuración
            valid = int(self.valid_count.get())
            invalid = int(self.invalid_count.get())
            extreme = int(self.extreme_count.get())
            depth = int(self.max_depth.get())
            length = int(self.max_length.get())
            
            # Generar casos
            self.generator.generate_all(valid, invalid, extreme, depth, length)
            
            # Mostrar resultados
            self.display_results()
            
            total = len(self.generator.test_cases)
            exec_time = self.generator.metrics['execution_time']
            
            messagebox.showinfo("✅ Generación Exitosa", 
                              f"Se generaron {total} casos de prueba\n" + 
                              f"Tiempo de ejecución: {exec_time}")
            
            self.status_label.config(text=f"✅ Estado: {total} casos generados exitosamente en {exec_time}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar casos:\n{str(e)}")
            self.status_label.config(text="❌ Estado: Error en la generación")
    
    def display_results(self):
        """Muestra los resultados en la interfaz"""
        if not self.generator:
            return
        
        # Mostrar métricas
        self.metrics_text.delete(1.0, tk.END)
        
        metrics_str = "╔" + "═" * 78 + "╗\n"
        metrics_str += "║" + " " * 25 + "REPORTE DE MÉTRICAS" + " " * 34 + "║\n"
        metrics_str += "╚" + "═" * 78 + "╝\n\n"
        
        metrics_str += f"📊 Total de casos generados: {self.generator.metrics['total_cases']}\n\n"
        
        metrics_str += "📈 Distribución por categoría:\n"
        metrics_str += "   ├─ Válidas:   " + f"{self.generator.metrics['distribution']['valid']:>8}\n"
        metrics_str += "   ├─ Inválidas: " + f"{self.generator.metrics['distribution']['invalid']:>8}\n"
        metrics_str += "   └─ Extremas:  " + f"{self.generator.metrics['distribution']['extreme']:>8}\n\n"
        
        metrics_str += f"📏 Longitud promedio: {self.generator.metrics['avg_length']} símbolos\n"
        metrics_str += f"🌳 Profundidad máxima: {self.generator.metrics['max_depth']}\n\n"
        
        metrics_str += "🔢 Operadores generados:\n"
        for op, count in self.generator.metrics['operators'].items():
            if count > 0:
                bar = "█" * min(count, 50)
                metrics_str += f"   {op:>3} │ {bar} ({count})\n"
        
        metrics_str += f"\n⏱️  Tiempo de ejecución: {self.generator.metrics['execution_time']}\n"
        metrics_str += f"📅 Generado: {self.generator.metrics['generated_at']}\n"
        
        metrics_str += "\n" + "─" * 80 + "\n"
        metrics_str += "✅ Generación completada exitosamente\n"
        
        self.metrics_text.insert(1.0, metrics_str)
        
        # Mostrar casos de prueba
        self.filter_cases()
        
        # Cambiar a la pestaña de métricas
        self.notebook.select(0)
    
    def export_json(self):
        """Exporta resultados a JSON"""
        if not self.generator or not self.generator.test_cases:
            messagebox.showwarning("Advertencia", "No hay casos de prueba para exportar")
            self.status_label.config(text="⚡ Estado: No hay datos para exportar")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Guardar como",
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
            initialfile=f"casos_prueba_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        if filename:
            try:
                self.generator.export_json(filename)
                messagebox.showinfo("✅ Exportación Exitosa", 
                                  f"Resultados exportados correctamente a:\n{filename}")
                self.status_label.config(text=f"✅ Estado: Datos exportados a {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar:\n{str(e)}")
                self.status_label.config(text="❌ Estado: Error al exportar")


def main():
    """Función principal"""
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
