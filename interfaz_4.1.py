import customtkinter as ctk
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.generador_datos import GeneradorDatos
from models.sistema import SistemaPrediccionDesercion

# Configuración del tema
ctk.set_appearance_mode("dark")  # "dark" o "light"
ctk.set_default_color_theme("blue")

class AppModerna:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Sistema de Predicción de Deserción Universitaria")
        self.root.geometry("1100x800")
        self.root.minsize(900, 600)
        
        self.sistema = None
        self.estudiantes = None
        self.generador = GeneradorDatos()
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame principal con padding
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título principal
        titulo = ctk.CTkLabel(self.main_frame, text="📊 SISTEMA DE PREDICCIÓN DE DESERCIÓN",
                              font=ctk.CTkFont(size=28, weight="bold"))
        titulo.pack(pady=(10, 5))
        
        subtitulo = ctk.CTkLabel(self.main_frame, text="Escala de notas: 0 a 20 (aprueba con 10)",
                                 font=ctk.CTkFont(size=14))
        subtitulo.pack(pady=(0, 20))
        
        # Frame de botones principales (fila 1)
        frame_botones1 = ctk.CTkFrame(self.main_frame)
        frame_botones1.pack(pady=10, fill="x")
        
        btn_entrenar = ctk.CTkButton(frame_botones1, text="1. Entrenar Sistema", 
                                      command=self.entrenar,
                                      fg_color="#2E7D32", hover_color="#1B5E20",
                                      height=45, font=ctk.CTkFont(size=14, weight="bold"))
        btn_entrenar.pack(side="left", padx=10, expand=True, fill="x")
        
        btn_estadisticas = ctk.CTkButton(frame_botones1, text="2. Estadísticas", 
                                          command=self.mostrar_estadisticas,
                                          fg_color="#1565C0", hover_color="#0D47A1",
                                          height=45, font=ctk.CTkFont(size=14, weight="bold"))
        btn_estadisticas.pack(side="left", padx=10, expand=True, fill="x")
        #CODIGO DE RANDY CASTILLO 30727559
        btn_reglas = ctk.CTkButton(frame_botones1, text="3. Ver Reglas", 
                                    command=self.mostrar_reglas,
                                    fg_color="#E65100", hover_color="#BF360C",
                                    height=45, font=ctk.CTkFont(size=14, weight="bold"))
        btn_reglas.pack(side="left", padx=10, expand=True, fill="x")
        
        # Frame de botones principales (fila 2)
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
        
        # Frame de búsqueda rápida
        frame_buscar = ctk.CTkFrame(self.main_frame)
        frame_buscar.pack(pady=10, fill="x")
        
        ctk.CTkLabel(frame_buscar, text="Buscar estudiante por ID:", 
                     font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        self.entry_id = ctk.CTkEntry(frame_buscar, width=120, font=ctk.CTkFont(size=14))
        self.entry_id.pack(side="left", padx=5)
        
        btn_buscar = ctk.CTkButton(frame_buscar, text="🔍 Buscar y diagnosticar", 
                                    command=self.buscar_y_diagnosticar,
                                    fg_color="#455A64", hover_color="#37474F",
                                    height=35)
        btn_buscar.pack(side="left", padx=10)
        
        # Área de resultados con scroll (moderno)
        self.text_area = ctk.CTkTextbox(self.main_frame, height=450, 
                                        font=ctk.CTkFont(family="Consolas", size=11),
                                        wrap="word")
        self.text_area.pack(pady=15, fill="both", expand=True)
        
        # Label de estado
        self.label_estado = ctk.CTkLabel(self.main_frame, text="⚠️ Primero entrene el sistema (botón 1)",
                                         text_color="#FFB74D", font=ctk.CTkFont(size=12))
        self.label_estado.pack(pady=5)
    #CODIGO DE RANDY CASTILLO 30727559
    # ==================== MÉTODOS FUNCIONALES ====================
    
    def escribir(self, texto, color=None):
        """Escribe en el área de texto con opción de color (usando tags)"""
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
        self.label_estado.configure(text="✅ Sistema entrenado correctamente", text_color="#81C784")
        self.escribir("\n✅ SISTEMA LISTO PARA USAR")
    
    def mostrar_estadisticas(self):
        if not self.sistema:
            self.escribir("⚠️ Primero entrene el sistema")
            return
        self.limpiar()
        total = len(self.estudiantes)
        desertores = sum(1 for e in self.estudiantes if e.deserto)
        self.escribir("="*50)
        self.escribir("📊 ESTADÍSTICAS GENERALES")
        self.escribir("="*50)
        self.escribir(f"Total estudiantes: {total}")
        self.escribir(f"Desertores reales: {desertores} ({desertores/total*100:.1f}%)")
        notas = [e.promedio_primer_semestre for e in self.estudiantes]
        self.escribir(f"Promedio general: {sum(notas)/len(notas):.1f}/20")
        self.escribir(f"Nota mínima: {min(notas):.1f}  |  Nota máxima: {max(notas):.1f}")
        
        rangos = [(0,8),(8,10),(10,12),(12,14),(14,20)]
        self.escribir("\n📉 Deserción por rango de notas:")
        for bajo, alto in rangos:
            grupo = [e for e in self.estudiantes if bajo <= e.promedio_primer_semestre < alto]
            if grupo:
                des = sum(1 for e in grupo if e.deserto)
                self.escribir(f"  {bajo}-{alto}: {des}/{len(grupo)} ({des/len(grupo)*100:.1f}% desertan)")
    
    def mostrar_reglas(self):
        if not self.sistema:
            self.escribir("⚠️ Primero entrene")
            return
        self.limpiar()
        reglas = self.sistema.apriori.obtener_reglas_desercion()
        self.escribir("="*50)
        self.escribir("📜 REGLAS DE ASOCIACIÓN (deserción)")
        self.escribir("="*50)
        if not reglas:
            self.escribir("No se encontraron reglas. Ajuste soporte/confianza.")
            return
        for i, r in enumerate(reglas[:30], 1):
            ant = " Y ".join(sorted(r['antecedente']))
            self.escribir(f"{i}. SI [{ant}] → deserto  (confianza {r['confianza']*100:.1f}%)")
    
    def lista_completa_riesgo(self):
        if not self.sistema:
            self.escribir("⚠️ Primero entrene")
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
            self.escribir(f"{i}. ID: {a['estudiante_id']} | Nota: {a['nota_promedio']}/20 | Riesgo: {a['riesgo']}")
            if a['factores']:
                self.escribir(f"   Factores: {', '.join(a['factores'][:3])}")
            else:
                self.escribir(f"   Factores: (ninguno específico)")
            if a['recomendaciones']:
                self.escribir(f"   💡 {a['recomendaciones'][0]}")
            self.escribir("-"*50)
            self.text_area.see("end")
            self.root.update()
    
    def diagnostico_individual(self):
        """Muestra el diagnóstico completo de un estudiante a partir del ID ingresado"""
        if not self.sistema:
            self.escribir("⚠️ Primero entrene")
            return
        try:
            id_buscar = int(self.entry_id.get())
            estudiante = next((e for e in self.estudiantes if e.id == id_buscar), None)
            if not estudiante:
                self.escribir(f"❌ Estudiante con ID {id_buscar} no encontrado")
                return
            diag = self.sistema.diagnosticar_estudiante(estudiante)
            self.limpiar()
            self.escribir("="*50)
            self.escribir(f"🔬 DIAGNÓSTICO COMPLETO - ID {diag['id']}")
            self.escribir("="*50)
            self.escribir(f"Nota real: {diag['nota_real']}/20 → Categoría: {diag['nota_categoria']}")
            self.escribir(f"Asistencia categoría: {diag['asistencia_categoria']}")
            self.escribir(f"Materias reprobadas categoría: {diag['materias_categoria']}")
            self.escribir(f"Reprobó Matemáticas I: {diag['reprobo_mate']}")
            self.escribir(f"Reprobó Química I: {diag['reprobo_quimica']}")
            self.escribir(f"Trabaja: {diag['trabaja']} ({diag['horas_trabajo']}h)")
            self.escribir(f"Carga alta (trabajo>20h o hijos): {diag['carga_alta']}")
            self.escribir(f"Bajo rendimiento inicial: {diag['bajo_rendimiento']}")
            self.escribir(f"Rezago académico: {diag['rezago_academico']}")
            self.escribir(f"Baja asistencia (<70%): {diag['baja_asistencia']}")
            self.escribir("\n🔍 Factores de riesgo detectados:")
            if diag['factores']:
                for f in diag['factores']:
                    self.escribir(f"  • {f}")
            else:
                self.escribir("  • Ninguno específico")
            self.escribir(f"\n🎯 Predicción del árbol: {diag['prediccion']}")
            
            # Recomendaciones
            alerta = self.sistema.generar_alerta(estudiante)
            if alerta and alerta['recomendaciones']:
                self.escribir("\n📋 Recomendaciones:")
                for rec in alerta['recomendaciones']:
                    self.escribir(f"  • {rec}")
        except ValueError:
            self.escribir("❌ ID debe ser un número entero")
    
    def buscar_y_diagnosticar(self):
        """Alias de diagnóstico individual (para el botón de búsqueda)"""
        self.diagnostico_individual()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AppModerna()
    app.run()