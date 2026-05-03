import customtkinter as ctk
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.generador_datos import GeneradorDatos
from models.sistema import SistemaPrediccionDesercion
from models.lector_excel import LectorExcel

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppMejorada:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Sistema de Predicción de Deserción Universitaria")
        self.root.geometry("1200x850")
        self.root.minsize(1100, 700)
        
        self.sistema = None
        self.estudiantes = None
        self.generador = GeneradorDatos()
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(self.main_frame, text="📊 SISTEMA DE PREDICCIÓN DE DESERCIÓN",
                              font=ctk.CTkFont(size=30, weight="bold"))
        titulo.pack(pady=(10, 5))
        
        subtitulo = ctk.CTkLabel(self.main_frame, text="Escala de notas: 0 a 20 (aprueba con 10)",
                                 font=ctk.CTkFont(size=14))
        subtitulo.pack(pady=(0, 20))
        
        # Fila 1: Botones principales
        frame_botones1 = ctk.CTkFrame(self.main_frame)
        frame_botones1.pack(pady=10, fill="x")
        
        btn_entrenar = ctk.CTkButton(frame_botones1, text="1. Generar Datos Sintéticos", 
                                      command=self.entrenar,
                                      fg_color="#2E7D32", hover_color="#1B5E20",
                                      height=45, font=ctk.CTkFont(size=14, weight="bold"))
        btn_entrenar.pack(side="left", padx=10, expand=True, fill="x")
        
        btn_cargar_excel = ctk.CTkButton(frame_botones1, text="📁 2. Cargar Excel Real", 
                                          command=self.cargar_excel,
                                          fg_color="#00695C", hover_color="#004D40",
                                          height=45, font=ctk.CTkFont(size=14, weight="bold"))
        btn_cargar_excel.pack(side="left", padx=10, expand=True, fill="x")
        
        btn_estadisticas = ctk.CTkButton(frame_botones1, text="3. Dashboard Estadísticas", 
                                          command=self.mostrar_estadisticas,
                                          fg_color="#1565C0", hover_color="#0D47A1",
                                          height=45, font=ctk.CTkFont(size=14, weight="bold"))
        btn_estadisticas.pack(side="left", padx=10, expand=True, fill="x")
        
        # Fila 2
        frame_botones2 = ctk.CTkFrame(self.main_frame)
        frame_botones2.pack(pady=10, fill="x")
        
        btn_riesgo = ctk.CTkButton(frame_botones2, text="4. Lista completa en riesgo", 
                                    command=self.lista_completa_riesgo,
                                    fg_color="#6A1B9A", hover_color="#4A148C",
                                    height=45, font=ctk.CTkFont(size=14, weight="bold"))
        btn_riesgo.pack(side="left", padx=10, expand=True, fill="x")
        
        btn_diagnostico = ctk.CTkButton(frame_botones2, text="5. Diagnóstico individual", 
                                         command=self.diagnostico_individual,
                                         fg_color="#00838F", hover_color="#006064",
                                         height=45, font=ctk.CTkFont(size=14, weight="bold"))
        btn_diagnostico.pack(side="left", padx=10, expand=True, fill="x")
        
        # Búsqueda por nombre/cédula
        frame_buscar = ctk.CTkFrame(self.main_frame)
        frame_buscar.pack(pady=10, fill="x")
        
        ctk.CTkLabel(frame_buscar, text="🔎 Buscar por Nombre o Cédula:", 
                     font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        self.entry_buscar = ctk.CTkEntry(frame_buscar, width=250, font=ctk.CTkFont(size=14))
        self.entry_buscar.pack(side="left", padx=5)
        
        btn_buscar = ctk.CTkButton(frame_buscar, text="Buscar y diagnosticar", 
                                    command=self.buscar_y_diagnosticar,
                                    fg_color="#9C27B0", hover_color="#7B1FA2",
                                    height=35)
        btn_buscar.pack(side="left", padx=10)
        
        # Área de resultados
        self.text_area = ctk.CTkTextbox(self.main_frame, height=350, 
                                        font=ctk.CTkFont(family="Consolas", size=12),
                                        wrap="word")
        self.text_area.pack(pady=15, fill="both", expand=True)
        
        self.label_estado = ctk.CTkLabel(self.main_frame, text="⚠️ Cargue un Excel o genere datos (opción 1 o 2)",
                                         text_color="#FFB74D", font=ctk.CTkFont(size=12))
        self.label_estado.pack(pady=5)
    
    # ==================== MÉTODOS BASE ====================
    def escribir(self, texto):
        self.text_area.insert("end", texto + "\n")
        self.text_area.see("end")
        self.root.update()
    
    def limpiar(self):
        self.text_area.delete("1.0", "end")
    
    def entrenar(self):
        self.limpiar()
        self.escribir("🔄 Generando datos sintéticos...")
        self.estudiantes = self.generador.generar_dataset(n=500)
        self.escribir(f"✅ Generados {len(self.estudiantes)} estudiantes")
        self.sistema = SistemaPrediccionDesercion()
        self.sistema.entrenar(self.estudiantes)
        self.label_estado.configure(text="✅ Sistema entrenado con datos SINTÉTICOS", text_color="#81C784")
        self.escribir("\n✅ SISTEMA LISTO PARA USAR")
    
    def cargar_excel(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
        )
        if not archivo:
            return
        self.limpiar()
        self.escribir(f"📂 Cargando archivo: {os.path.basename(archivo)}")
        lector = LectorExcel()
        lector.cargar_datos(archivo)
        self.estudiantes = lector.convertir_a_estudiantes()
        if not self.estudiantes:
            self.escribir("❌ No se pudieron cargar estudiantes")
            return
        desertores = sum(1 for e in self.estudiantes if e.deserto)
        self.escribir(f"\n📊 Estadísticas del Excel cargado:")
        self.escribir(f"   Total: {len(self.estudiantes)} estudiantes")
        self.escribir(f"   Desertores: {desertores} ({desertores/len(self.estudiantes)*100:.1f}%)")
        self.escribir("\n🔄 Entrenando el sistema con datos reales...")
        self.sistema = SistemaPrediccionDesercion()
        self.sistema.entrenar(self.estudiantes)
        self.label_estado.configure(text=f"✅ Cargados {len(self.estudiantes)} estudiantes desde Excel", text_color="#81C784")
        self.escribir("\n✅ SISTEMA ENTRENADO CON DATOS REALES")
    
    def mostrar_estadisticas(self):
        if not self.sistema:
            self.escribir("⚠️ Primero cargue un Excel o genere datos")
            return
        self.limpiar()
        self.escribir("📊 Abriendo Dashboard Visual...")
        dashboard = ctk.CTkToplevel(self.root)
        dashboard.title("Dashboard - Estadísticas de Deserción")
        dashboard.geometry("1000x650")
        dashboard.attributes("-topmost", True)
        
        total = len(self.estudiantes)
        desertores = sum(1 for e in self.estudiantes if e.deserto)
        tasa = (desertores / total) * 100 if total > 0 else 0
        notas = [e.promedio_primer_semestre for e in self.estudiantes]
        promedio_gen = sum(notas) / len(notas) if notas else 0
        
        frame_kpis = ctk.CTkFrame(dashboard)
        frame_kpis.pack(fill="x", padx=20, pady=20)
        info = f"👥 Total: {total}   |   ⚠️ En Riesgo: {desertores} ({tasa:.1f}%)   |   📝 Promedio Global: {promedio_gen:.1f}/20"
        ctk.CTkLabel(frame_kpis, text=info, font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)
        
        frame_graficos = ctk.CTkFrame(dashboard)
        frame_graficos.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), facecolor='#2B2B2B')
        ax1.pie([desertores, total - desertores], labels=['En Riesgo', 'Seguros'],
                colors=['#EF5350', '#66BB6A'], autopct='%1.1f%%', startangle=140)
        ax1.set_title('Distribución Global de Riesgo', color='white', pad=15, weight='bold')
        
        rangos = [(0,8),(8,10),(10,12),(12,14),(14,21)]
        etiquetas = ['0-8', '8-10', '10-12', '12-14', '14-20']
        valores = []
        for bajo, alto in rangos:
            grupo = [e for e in self.estudiantes if bajo <= e.promedio_primer_semestre < alto]
            valores.append(sum(1 for e in grupo if e.deserto))
        bars = ax2.bar(etiquetas, valores, color='#42A5F5')
        ax2.set_title('Estudiantes en Riesgo por Rango de Notas', color='white', pad=15, weight='bold')
        ax2.tick_params(colors='white')
        ax2.set_ylabel('Cantidad', color='white')
        for spine in ax2.spines.values():
            spine.set_edgecolor('white')
        for bar in bars:
            y = bar.get_height()
            if y > 0:
                ax2.text(bar.get_x() + bar.get_width()/2, y + 0.5, int(y), ha='center', va='bottom', color='white', weight='bold')
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=frame_graficos)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def lista_completa_riesgo(self):
        if not self.sistema:
            self.escribir("⚠️ Primero cargue un Excel o genere datos")
            return
        self.limpiar()
        alertas = self.sistema.generar_reporte(self.estudiantes, top_n=None)
        if not alertas:
            self.escribir("✅ No hay estudiantes en riesgo.")
            return
        self.escribir(f"{'='*60}")
        self.escribir(f"⚠️ LISTA COMPLETA DE ESTUDIANTES EN RIESGO ({len(alertas)} total)")
        self.escribir("="*60)
        for i, a in enumerate(alertas, 1):
            est = next((e for e in self.estudiantes if e.id == a['estudiante_id']), None)
            nombre = getattr(est, 'nombre_completo', f"ID {a['estudiante_id']}") if est else f"ID {a['estudiante_id']}"
            cedula = getattr(est, 'cedula', '') if est else ''
            self.escribir(f"{i}. {nombre}")
            if cedula:
                self.escribir(f"   Cédula: {cedula}")
            self.escribir(f"   Nota: {a['nota_promedio']}/20 | Riesgo: {a['riesgo']}")
            if a.get('factores'):
                self.escribir(f"   Factores: {', '.join(a['factores'][:3])}")
            if a.get('recomendaciones'):
                self.escribir(f"   💡 {a['recomendaciones'][0]}")
            self.escribir("-"*50)
            self.text_area.see("end")
            self.root.update()
    
    def diagnostico_individual(self):
        if not self.sistema:
            self.escribir("⚠️ Primero cargue un Excel o genere datos")
            return
        dialog = ctk.CTkInputDialog(text="Ingrese el ID del estudiante:", title="Diagnóstico individual")
        id_text = dialog.get_input()
        if not id_text:
            return
        try:
            id_int = int(id_text)
            estudiante = next((e for e in self.estudiantes if e.id == id_int), None)
            if not estudiante:
                self.escribir(f"❌ Estudiante con ID {id_int} no encontrado")
                return
            diag = self.sistema.diagnosticar_estudiante(estudiante)
            alerta = self.sistema.generar_alerta(estudiante)
            self.mostrar_perfil_mejorado(estudiante, diag, alerta)
        except ValueError:
            self.escribir("❌ El ID debe ser un número entero")
    
    def buscar_y_diagnosticar(self):
        if not self.sistema:
            self.escribir("⚠️ Primero cargue un Excel o genere datos")
            return
        texto = self.entry_buscar.get().strip()
        if not texto:
            self.escribir("⚠️ Ingrese un nombre, apellido o cedula para buscar")
            return
        self.limpiar()
        texto_low = texto.lower()
        resultados = []
        for e in self.estudiante:
            nombre = getattr(e, 'nombre_completo', '').lower()
            cedula = str(getattr(e, 'cedula', '')).lower()
            if texto_low in nombre or texto_low in cedula:
                resultados.append(e)
        if not resultados:
            self.escribir(f"❌ No se encontraron estudiantes con: '{texto}'")
            return
        self.escribir(f"🔍 RESULTADOS DE BÚSQUEDA: '{texto}' ({len(resultados)} encontrados)")
        self.escribir("="*60)        
        for idx, e in enumerate(resultados, 1):
            nombre = getattr(e, 'nombre_completo', f"Estudiante ID {e.id}")
            cedula = getattr(e, 'cedula', 'N/A')
            prom = e.promedio_primer_semestre
            riesgo_txt = "⚠️ ALTO RIESGO" if e.deserto else "✅ BAJO RIESGO"
            self.escribir(f"{idx}. {nombre}")
            self.escribir(f"   ID: {e.id} | Cédula: {cedula} | Nota: {prom}/20 | {riesgo_txt}")
            self.escribir("-"*50)
        if len(resultados) == 1:
            self.escribir("\n🔍 Abriendo diagnóstico automático...")
            est = resultados[0]
            diag = self.sistema.diagnosticar_estudiante(est)
            alerta = self.sistema.generar_alerta(est)
            # Verificar si hay materias reprobadas para mostrar advertencia
            materias_reprobadas = []
            if hasattr(est, 'notas') and est.notas:
                materias_reprobadas = [m for m, n in est.notas.items() if n < 10]
            self.mostrar_perfil_mejorado(est, diag, alerta, materias_reprobadas)
        else:
            self.escribir("\n💡 Para diagnosticar a uno, anote su ID y use el botón 'Diagnóstico individua")
            
    # ==================== PERFIL MEJORADO ====================
    def mostrar_perfil_mejorado(self, estudiante, diag, alerta):
        """Ventana con diseño mejorado: notas por materia y recomendaciones"""
        perfil = ctk.CTkToplevel(self.root)
        titulo = getattr(estudiante, 'nombre_completo', f"ID {estudiante.id}")
        perfil.title(f"Perfil del Estudiante - {titulo}")
        perfil.geometry("980x750")
        perfil.attributes("-topmost", True)
        
        # ========== ENCABEZADO ==========
        header = ctk.CTkFrame(perfil, fg_color="#1a1a1a", corner_radius=15)
        header.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(header, text="👤", font=ctk.CTkFont(size=48)).pack(side="left", padx=25, pady=10)
        col_nom = ctk.CTkFrame(header, fg_color="transparent")
        col_nom.pack(side="left", fill="both", expand=True, padx=10)
        ctk.CTkLabel(col_nom, text=titulo, font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w")
        if hasattr(estudiante, 'cedula') and estudiante.cedula:
            texto_ced = f"Cédula: {estudiante.cedula}"
            if hasattr(estudiante, 'carrera') and estudiante.carrera:
                texto_ced += f"  |  Carrera: {estudiante.carrera}"
            ctk.CTkLabel(col_nom, text=texto_ced, font=ctk.CTkFont(size=13)).pack(anchor="w")
        if hasattr(estudiante, 'turno') and estudiante.turno:
            texto_turno = f"Turno: {estudiante.turno}"
            if hasattr(estudiante, 'seccion') and estudiante.seccion:
                texto_turno += f"  |  Sección: {estudiante.seccion}"
            ctk.CTkLabel(col_nom, text=texto_turno, font=ctk.CTkFont(size=13)).pack(anchor="w")
        
        color_riesgo = "#EF5350" if diag.get('prediccion') == "ALTO" else "#66BB6A"
        texto_riesgo = f"⚠️ {diag.get('prediccion', 'BAJO')} RIESGO" if diag.get('prediccion') == "ALTO" else f"✅ {diag.get('prediccion', 'BAJO')} RIESGO"
        ctk.CTkLabel(header, text=texto_riesgo, text_color=color_riesgo, font=ctk.CTkFont(size=20, weight="bold")).pack(side="right", padx=30)
        
        # ========== NOTAS POR MATERIA ==========
        frame_notas = ctk.CTkFrame(perfil, corner_radius=15)
        frame_notas.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(frame_notas, text="📚 NOTAS POR MATERIA", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=15, pady=(10,5))
        
        if hasattr(estudiante, 'notas') and estudiante.notas:
            materias = list(estudiante.notas.keys())
            col1 = ctk.CTkFrame(frame_notas, fg_color="transparent")
            col1.pack(side="left", fill="both", expand=True, padx=10, pady=5)
            col2 = ctk.CTkFrame(frame_notas, fg_color="transparent")
            col2.pack(side="left", fill="both", expand=True, padx=10, pady=5)
            for i, (mat, nota) in enumerate(estudiante.notas.items()):
                parent = col1 if i % 2 == 0 else col2
                color_nota = "#EF5350" if nota < 10 else ("#FFA726" if nota < 14 else "#66BB6A")
                frame_materia = ctk.CTkFrame(parent, fg_color="#2b2b2b", corner_radius=10)
                frame_materia.pack(fill="x", pady=4)
                ctk.CTkLabel(frame_materia, text=f"{mat}:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10, pady=5)
                ctk.CTkLabel(frame_materia, text=f"{nota} / 20", text_color=color_nota, font=ctk.CTkFont(weight="bold")).pack(side="right", padx=10, pady=5)
        else:
            ctk.CTkLabel(frame_notas, text="No hay notas disponibles", text_color="gray").pack(pady=10)
        
        promedio = diag['nota_real']
        color_prom = "#EF5350" if promedio < 10 else ("#FFA726" if promedio < 14 else "#66BB6A")
        frame_prom = ctk.CTkFrame(frame_notas, fg_color="transparent")
        frame_prom.pack(fill="x", pady=10)
        ctk.CTkLabel(frame_prom, text=f"⭐ PROMEDIO FINAL: {promedio} / 20", text_color=color_prom, font=ctk.CTkFont(size=18, weight="bold")).pack()
        
        # ========== FACTORES DE RIESGO ==========
        frame_factores = ctk.CTkFrame(perfil, corner_radius=15)
        frame_factores.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(frame_factores, text="⚠️ FACTORES DE RIESGO DETECTADOS", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(10,5))
        if diag.get('factores'):
            for factor in diag['factores']:
                ctk.CTkLabel(frame_factores, text=f"• {factor}", text_color="#FFB74D", wraplength=800, justify="left").pack(anchor="w", padx=25, pady=2)
        else:
            ctk.CTkLabel(frame_factores, text="• No se detectaron factores de riesgo", text_color="#A5D6A7").pack(anchor="w", padx=25, pady=2)
        
        # ========== RECOMENDACIONES ==========
        frame_rec = ctk.CTkFrame(perfil, corner_radius=15)
        frame_rec.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(frame_rec, text="💡 RECOMENDACIONES PARA MEJORAR", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(10,5))
        if alerta and alerta.get('recomendaciones'):
            for rec in alerta['recomendaciones']:
                ctk.CTkLabel(frame_rec, text=f"• {rec}", text_color="#FFF59D", wraplength=850, justify="left").pack(anchor="w", padx=25, pady=3)
        else:
            ctk.CTkLabel(frame_rec, text="• Mantener el rendimiento actual. No se requieren intervenciones urgentes.", text_color="#A5D6A7").pack(anchor="w", padx=25, pady=3)
        
        # ========== GRÁFICO ==========
        frame_graf = ctk.CTkFrame(perfil, corner_radius=15)
        frame_graf.pack(fill="both", expand=True, padx=20, pady=10)
        ctk.CTkLabel(frame_graf, text="📈 ANÁLISIS VISUAL", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=15, pady=(10,0))
        
        fig, ax = plt.subplots(figsize=(5, 2), facecolor='#2B2B2B')
        if hasattr(estudiante, 'notas') and estudiante.notas:
            materias = list(estudiante.notas.keys())
            notas = list(estudiante.notas.values())
            colores = ['#EF5350' if n < 10 else ('#FFA726' if n < 14 else '#66BB6A') for n in notas]
            ax.barh(materias, notas, color=colores)
            ax.axvline(x=10, color='white', linestyle='--', alpha=0.7)
            ax.set_xlim(0, 20)
            ax.set_title("Notas por Materia", color='white')
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_edgecolor('white')
        else:
            ax.text(0.5, 0.5, "Sin datos de materias", ha='center', va='center', color='white', transform=ax.transAxes)
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=frame_graf)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # ========== MENSAJE FINAL Y ADVERTENCIA ==========
        frame_msg = ctk.CTkFrame(perfil, fg_color="transparent")
        frame_msg.pack(fill="x", padx=20, pady=10)
        
        # Advertencia adicional si el árbol dice BAJO pero hay materias reprobadas
        materias_reprobadas = []
        if hasattr(estudiante, 'notas') and estudiante.notas:
            materias_reprobadas = [m for m, n in estudiante.notas.items() if n < 10]
        if diag.get('prediccion') == "BAJO" and materias_reprobadas:
            ctk.CTkLabel(frame_msg, text="⚠️ ATENCIÓN: Aunque el sistema indica bajo riesgo, el estudiante tiene materias reprobadas. Se recomienda seguimiento personalizado.", text_color="#FF9800", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=2)
        
        if diag.get('prediccion') == "ALTO":
            ctk.CTkLabel(frame_msg, text="⚠️ El estudiante requiere intervención temprana. Siga las recomendaciones.", text_color="#EF5350", font=ctk.CTkFont(size=13, weight="bold")).pack(pady=5)
        else:
            ctk.CTkLabel(frame_msg, text="✅ El estudiante está en buen camino. Continúe con el seguimiento normal.", text_color="#66BB6A", font=ctk.CTkFont(size=13, weight="bold")).pack(pady=5)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AppMejorada()
    app.run()