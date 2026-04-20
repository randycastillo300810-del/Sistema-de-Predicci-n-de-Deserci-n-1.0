import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.generador_datos import GeneradorDatos
from models.sistema import SistemaPrediccionDesercion

class AppDesercion:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Predicción de Deserción Universitaria")
        self.root.geometry("950x750")
        self.root.configure(bg='#f0f0f0')
        
        self.sistema = None
        self.estudiantes = None
        self.generador = GeneradorDatos()
        
        self.crear_menu()
        self.crear_area_principal()
    
    def crear_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        archivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)
        archivo_menu.add_command(label="Salir", command=self.root.quit)
        
        datos_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Datos", menu=datos_menu)
        datos_menu.add_command(label="Generar datos y entrenar", command=self.generar_entrenar)
        
        ayuda_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=ayuda_menu)
        ayuda_menu.add_command(label="Acerca de", command=self.acerca_de)
    
    def crear_area_principal(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        titulo = tk.Label(self.main_frame, text="SISTEMA DE PREDICCIÓN DE DESERCIÓN",
                          font=("Arial", 16, "bold"), bg='#f0f0f0')
        titulo.pack(pady=10)
        
        subtitulo = tk.Label(self.main_frame, text="Escala de notas: 0 a 20 (aprueba con 10)",
                             font=("Arial", 10), bg='#f0f0f0', fg='gray')
        subtitulo.pack(pady=5)
        
        # Frame para botones principales
        frame_botones = ttk.Frame(self.main_frame)
        frame_botones.pack(pady=10)
        
        btn_entrenar = tk.Button(frame_botones, text="1. Entrenar Sistema",
                                  command=self.generar_entrenar,
                                  bg='#4CAF50', fg='white', font=("Arial", 11),
                                  padx=15, pady=8)
        btn_entrenar.grid(row=0, column=0, padx=5)
        
        btn_estadisticas = tk.Button(frame_botones, text="2. Estadísticas",
                                      command=self.mostrar_estadisticas,
                                      bg='#2196F3', fg='white', font=("Arial", 11),
                                      padx=15, pady=8)
        btn_estadisticas.grid(row=0, column=1, padx=5)
        
        btn_reglas = tk.Button(frame_botones, text="3. Ver Reglas",
                                command=self.mostrar_reglas,
                                bg='#FF9800', fg='white', font=("Arial", 11),
                                padx=15, pady=8)
        btn_reglas.grid(row=0, column=2, padx=5)
        
        btn_riesgo = tk.Button(frame_botones, text="4. Lista completa en riesgo",
                                command=self.mostrar_todos_riesgo,
                                bg='#9C27B0', fg='white', font=("Arial", 11),
                                padx=15, pady=8)
        btn_riesgo.grid(row=0, column=3, padx=5)
        
        # Frame para predicción y búsqueda
        frame_busqueda = ttk.LabelFrame(self.main_frame, text="Predecir / Diagnosticar estudiante")
        frame_busqueda.pack(fill=tk.X, pady=10, padx=5)
        
        ttk.Label(frame_busqueda, text="ID del estudiante:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = ttk.Entry(frame_busqueda, width=10)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)
        
        btn_predecir = tk.Button(frame_busqueda, text="Predecir y diagnosticar", 
                                  command=self.predecir_y_diagnosticar,
                                  bg='#3F51B5', fg='white', font=("Arial", 10),
                                  padx=10, pady=3)
        btn_predecir.grid(row=0, column=2, padx=5)
        
        btn_buscar = tk.Button(frame_busqueda, text="Buscar en lista de riesgo",
                                command=self.buscar_y_mostrar,
                                bg='#607D8B', fg='white', font=("Arial", 10),
                                padx=10, pady=3)
        btn_buscar.grid(row=0, column=3, padx=5)
        
        # Área de resultados con scroll
        self.area_resultados = scrolledtext.ScrolledText(self.main_frame, height=28, width=110,
                                                          font=("Courier", 9), wrap=tk.WORD)
        self.area_resultados.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Label de estado
        self.label_estado = tk.Label(self.main_frame, text="⚠️ Primero debe entrenar el sistema (opción 1)",
                                      font=("Arial", 9), bg='#f0f0f0', fg='red')
        self.label_estado.pack(pady=5)
    
    def generar_entrenar(self):
        self.area_resultados.delete(1.0, tk.END)
        self.area_resultados.insert(tk.END, "🔄 Generando datos sintéticos...\n")
        self.root.update()
        
        self.estudiantes = self.generador.generar_dataset(n=500)
        self.area_resultados.insert(tk.END, f"✅ Generados {len(self.estudiantes)} estudiantes\n\n")
        
        self.sistema = SistemaPrediccionDesercion()
        self.sistema.entrenar(self.estudiantes)
        
        self.label_estado.config(text="✅ Sistema entrenado correctamente", fg='green')
        self.area_resultados.insert(tk.END, "\n✅ SISTEMA LISTO PARA USAR\n")
    
    def mostrar_estadisticas(self):
        if self.sistema is None or self.estudiantes is None:
            messagebox.showwarning("Error", "Primero debe entrenar el sistema (opción 1)")
            return
        
        self.area_resultados.delete(1.0, tk.END)
        total = len(self.estudiantes)
        desertores = sum(1 for e in self.estudiantes if e.deserto)
        
        self.area_resultados.insert(tk.END, "="*50 + "\n")
        self.area_resultados.insert(tk.END, "ESTADÍSTICAS GENERALES (Escala 0-20)\n")
        self.area_resultados.insert(tk.END, "="*50 + "\n\n")
        self.area_resultados.insert(tk.END, f"Total estudiantes: {total}\n")
        self.area_resultados.insert(tk.END, f"Desertores reales: {desertores} ({desertores/total*100:.1f}%)\n")
        self.area_resultados.insert(tk.END, f"No desertores: {total - desertores}\n\n")
        
        notas = [e.promedio_primer_semestre for e in self.estudiantes]
        self.area_resultados.insert(tk.END, f"📊 Promedio general: {sum(notas)/len(notas):.1f}/20\n")
        self.area_resultados.insert(tk.END, f"   Nota mínima: {min(notas):.1f}/20\n")
        self.area_resultados.insert(tk.END, f"   Nota máxima: {max(notas):.1f}/20\n\n")
        
        rangos = [(0,8),(8,10),(10,12),(12,14),(14,20)]
        self.area_resultados.insert(tk.END, "📊 Deserción por rango de notas:\n")
        for bajo, alto in rangos:
            grupo = [e for e in self.estudiantes if bajo <= e.promedio_primer_semestre < alto]
            if grupo:
                des = sum(1 for e in grupo if e.deserto)
                self.area_resultados.insert(tk.END, f"   {bajo}-{alto}: {des}/{len(grupo)} ({des/len(grupo)*100:.1f}% desertan)\n")
    
    def mostrar_reglas(self):
        if self.sistema is None:
            messagebox.showwarning("Error", "Primero entrene el sistema")
            return
        self.area_resultados.delete(1.0, tk.END)
        self.area_resultados.insert(tk.END, "="*50 + "\nREGLAS DE ASOCIACIÓN\n" + "="*50 + "\n\n")
        reglas = self.sistema.apriori.obtener_reglas_desercion()
        if not reglas:
            self.area_resultados.insert(tk.END, "No se encontraron reglas de deserción. Intente ajustar soporte/confianza.\n")
            return
        for i, r in enumerate(reglas[:30], 1):
            ant = " Y ".join(sorted(r['antecedente']))
            self.area_resultados.insert(tk.END, f"{i}. SI [{ant}] → deserto\n   Confianza: {r['confianza']*100:.1f}%\n\n")
    
    def mostrar_todos_riesgo(self):
        """Muestra la lista COMPLETA de estudiantes en riesgo (sin límite) con factores"""
        if self.sistema is None or self.estudiantes is None:
            messagebox.showwarning("Error", "Primero entrene el sistema")
            return
        self.area_resultados.delete(1.0, tk.END)
        alertas = self.sistema.generar_reporte(self.estudiantes, top_n=None)  # TODOS
        if not alertas:
            self.area_resultados.insert(tk.END, "✅ No hay estudiantes en riesgo.\n")
            return
        self.area_resultados.insert(tk.END, f"{'='*60}\nLISTA COMPLETA DE ESTUDIANTES EN RIESGO ({len(alertas)} en total)\n{'='*60}\n\n")
        for i, a in enumerate(alertas, 1):
            self.area_resultados.insert(tk.END, f"{i}. ID: {a['estudiante_id']} | Nota: {a['nota_promedio']}/20 | Riesgo: {a['riesgo']}\n")
            if a['factores']:
                self.area_resultados.insert(tk.END, f"   Factores: {', '.join(a['factores'][:3])}\n")
            else:
                self.area_resultados.insert(tk.END, f"   Factores: (ninguno específico)\n")
            if a['recomendaciones']:
                self.area_resultados.insert(tk.END, f"   💡 {a['recomendaciones'][0]}\n")
            self.area_resultados.insert(tk.END, "-"*50 + "\n")
            self.area_resultados.see(tk.END)
            self.root.update()
    
    def predecir_y_diagnosticar(self):
        """Usa diagnosticar_estudiante para mostrar el estado completo del estudiante"""
        if self.sistema is None or self.estudiantes is None:
            messagebox.showwarning("Error", "Primero entrene el sistema")
            return
        try:
            id_buscar = int(self.entry_id.get())
            estudiante = next((e for e in self.estudiantes if e.id == id_buscar), None)
            if not estudiante:
                messagebox.showwarning("No encontrado", f"ID {id_buscar} no existe")
                return
            
            # Obtener diagnóstico detallado
            diag = self.sistema.diagnosticar_estudiante(estudiante)
            
            self.area_resultados.delete(1.0, tk.END)
            self.area_resultados.insert(tk.END, f"{'='*50}\nDIAGNÓSTICO COMPLETO DEL ESTUDIANTE\n{'='*50}\n")
            self.area_resultados.insert(tk.END, f"ID: {diag['id']}\n")
            self.area_resultados.insert(tk.END, f"Nota real: {diag['nota_real']}/20\n")
            self.area_resultados.insert(tk.END, f"Categoría de nota: {diag['nota_categoria']} (bajo<10, medio=10-14, alto>14)\n")
            self.area_resultados.insert(tk.END, f"Categoría de asistencia: {diag['asistencia_categoria']}\n")
            self.area_resultados.insert(tk.END, f"Categoría de materias reprobadas: {diag['materias_categoria']}\n")
            self.area_resultados.insert(tk.END, f"Reprobó Matemáticas I: {diag['reprobo_mate']}\n")
            self.area_resultados.insert(tk.END, f"Reprobó Química I: {diag['reprobo_quimica']}\n")
            self.area_resultados.insert(tk.END, f"Trabaja: {diag['trabaja']} ({diag['horas_trabajo']}h)\n")
            self.area_resultados.insert(tk.END, f"Carga alta (trabajo>20h o hijos): {diag['carga_alta']}\n")
            self.area_resultados.insert(tk.END, f"Bajo rendimiento inicial (nota<10): {diag['bajo_rendimiento']}\n")
            self.area_resultados.insert(tk.END, f"Rezago académico (>2 materias reprobadas): {diag['rezago_academico']}\n")
            self.area_resultados.insert(tk.END, f"Baja asistencia (<70%): {diag['baja_asistencia']}\n")
            self.area_resultados.insert(tk.END, f"\n🔍 Factores de riesgo identificados: {', '.join(diag['factores']) if diag['factores'] else 'NINGUNO'}\n")
            self.area_resultados.insert(tk.END, f"\n🎯 Predicción del árbol de decisión: {diag['prediccion']}\n")
            
            # Mostrar también recomendaciones si las hay
            alerta = self.sistema.generar_alerta(estudiante)
            if alerta and alerta['recomendaciones']:
                self.area_resultados.insert(tk.END, "\n📋 Recomendaciones:\n")
                for rec in alerta['recomendaciones']:
                    self.area_resultados.insert(tk.END, f"   {rec}\n")
                    
        except ValueError:
            messagebox.showwarning("Error", "Ingrese un ID numérico")
    
    def buscar_y_mostrar(self):
        """Busca un estudiante por ID y si está en riesgo, lo muestra en la lista"""
        if self.sistema is None or self.estudiantes is None:
            messagebox.showwarning("Error", "Primero entrene el sistema")
            return
        try:
            id_buscar = int(self.entry_id.get())
            estudiante = next((e for e in self.estudiantes if e.id == id_buscar), None)
            if not estudiante:
                messagebox.showwarning("No encontrado", f"ID {id_buscar} no existe")
                return
            pred = self.sistema.predecir(estudiante)
            if not pred['deserta']:
                messagebox.showinfo("Sin riesgo", f"El estudiante {id_buscar} NO está en riesgo.")
                return
            alerta = self.sistema.generar_alerta(estudiante)
            self.area_resultados.insert(tk.END, f"\n🔍 Estudiante {id_buscar} EN RIESGO:\n")
            self.area_resultados.insert(tk.END, f"   Nota: {alerta['nota_promedio']}/20\n")
            self.area_resultados.insert(tk.END, f"   Factores: {', '.join(alerta['factores']) if alerta['factores'] else 'No especificados'}\n")
            self.area_resultados.insert(tk.END, f"   Recomendación: {alerta['recomendaciones'][0] if alerta['recomendaciones'] else 'Ninguna'}\n")
            self.area_resultados.see(tk.END)
        except ValueError:
            messagebox.showwarning("Error", "ID inválido")
    
    def acerca_de(self):
        messagebox.showinfo("Acerca de", "Sistema de Predicción de Deserción\nEscala 0-20\nAlgoritmos: ID3 y Apriori\nVersión con diagnóstico completo")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppDesercion(root)
    root.mainloop()