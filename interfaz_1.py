# interfaz_tkinter.py
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.generador_datos import GeneradorDatos
from models.sistema import SistemaPrediccionDesercion

class AppDesercion:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Predicción de Deserción Universitaria")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        self.sistema = None
        self.estudiantes = None
        self.generador = GeneradorDatos()
        
        self.crear_menu()
        self.crear_area_principal()
    
    def crear_menu(self):
        # Barra de menú
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        archivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)
        archivo_menu.add_command(label="Salir", command=self.root.quit)
        
        # Menú Datos
        datos_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Datos", menu=datos_menu)
        datos_menu.add_command(label="Generar datos y entrenar", command=self.generar_entrenar)
        
        # Menú Ayuda
        ayuda_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=ayuda_menu)
        ayuda_menu.add_command(label="Acerca de", command=self.acerca_de)
    
    def crear_area_principal(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = tk.Label(self.main_frame, text="SISTEMA DE PREDICCIÓN DE DESERCIÓN", 
                          font=("Arial", 16, "bold"), bg='#f0f0f0')
        titulo.pack(pady=10)
        
        # Subtítulo
        subtitulo = tk.Label(self.main_frame, text="Escala de notas: 0 a 20 (aprueba con 10)",
                             font=("Arial", 10), bg='#f0f0f0', fg='gray')
        subtitulo.pack(pady=5)
        
        # Frame para botones
        frame_botones = ttk.Frame(self.main_frame)
        frame_botones.pack(pady=20)
        
        # Botones principales
        btn_entrenar = tk.Button(frame_botones, text="1. Entrenar Sistema", 
                                  command=self.generar_entrenar,
                                  bg='#4CAF50', fg='white', font=("Arial", 12),
                                  padx=20, pady=10)
        btn_entrenar.grid(row=0, column=0, padx=10)
        
        btn_estadisticas = tk.Button(frame_botones, text="2. Estadísticas", 
                                      command=self.mostrar_estadisticas,
                                      bg='#2196F3', fg='white', font=("Arial", 12),
                                      padx=20, pady=10)
        btn_estadisticas.grid(row=0, column=1, padx=10)
        
        btn_reglas = tk.Button(frame_botones, text="3. Ver Reglas", 
                                command=self.mostrar_reglas,
                                bg='#FF9800', fg='white', font=("Arial", 12),
                                padx=20, pady=10)
        btn_reglas.grid(row=0, column=2, padx=10)
        
        # Área de resultados (Text widget)
        self.area_resultados = tk.Text(self.main_frame, height=20, width=80, 
                                        font=("Courier", 10))
        self.area_resultados.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(self.area_resultados)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.area_resultados.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.area_resultados.yview)
        
        # Frame para predicción individual
        frame_prediccion = ttk.LabelFrame(self.main_frame, text="Predecir estudiante individual")
        frame_prediccion.pack(fill=tk.X, pady=10)
        
        # Entrada de ID
        ttk.Label(frame_prediccion, text="ID del estudiante:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = ttk.Entry(frame_prediccion, width=10)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)
        
        btn_predecir = tk.Button(frame_prediccion, text="Predecir", 
                                  command=self.predecir_estudiante,
                                  bg='#9C27B0', fg='white', font=("Arial", 10),
                                  padx=10, pady=5)
        btn_predecir.grid(row=0, column=2, padx=10, pady=5)
        
        # Label de estado
        self.label_estado = tk.Label(self.main_frame, text="⚠️ Primero debe entrenar el sistema (opción 1)",
                                      font=("Arial", 10), bg='#f0f0f0', fg='red')
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
        self.area_resultados.insert(tk.END, f"Desertores: {desertores} ({desertores/total*100:.1f}%)\n")
        self.area_resultados.insert(tk.END, f"No desertores: {total - desertores}\n\n")
        
        # Distribución de notas
        notas = [e.promedio_primer_semestre for e in self.estudiantes]
        self.area_resultados.insert(tk.END, "📊 Distribución de notas:\n")
        self.area_resultados.insert(tk.END, f"   Promedio general: {sum(notas)/len(notas):.1f}/20\n")
        self.area_resultados.insert(tk.END, f"   Nota mínima: {min(notas):.1f}/20\n")
        self.area_resultados.insert(tk.END, f"   Nota máxima: {max(notas):.1f}/20\n\n")
        
        # Por rango de notas
        self.area_resultados.insert(tk.END, "📊 Deserción por rango de notas:\n")
        rangos = [(0, 8), (8, 10), (10, 12), (12, 14), (14, 20)]
        for bajo, alto in rangos:
            grupo = [e for e in self.estudiantes if bajo <= e.promedio_primer_semestre < alto]
            if grupo:
                des = sum(1 for e in grupo if e.deserto)
                self.area_resultados.insert(tk.END, f"   Notas {bajo}-{alto}: {des}/{len(grupo)} ({des/len(grupo)*100:.1f}% desertan)\n")
    
    def mostrar_reglas(self):
        if self.sistema is None:
            messagebox.showwarning("Error", "Primero debe entrenar el sistema (opción 1)")
            return
        
        self.area_resultados.delete(1.0, tk.END)
        self.area_resultados.insert(tk.END, "="*50 + "\n")
        self.area_resultados.insert(tk.END, "REGLAS DE ASOCIACIÓN\n")
        self.area_resultados.insert(tk.END, "="*50 + "\n\n")
        
        reglas = self.sistema.apriori.obtener_reglas_desercion()
        
        for i, regla in enumerate(reglas[:10]):
            ant = " Y ".join(sorted(regla['antecedente']))
            self.area_resultados.insert(tk.END, f"\nRegla {i+1}:\n")
            self.area_resultados.insert(tk.END, f"  SI [{ant}]\n")
            self.area_resultados.insert(tk.END, f"  ENTONCES [deserto]\n")
            self.area_resultados.insert(tk.END, f"  Confianza: {regla['confianza']*100:.1f}%\n")
    
    def predecir_estudiante(self):
        if self.sistema is None or self.estudiantes is None:
            messagebox.showwarning("Error", "Primero debe entrenar el sistema (opción 1)")
            return
        
        try:
            id_buscar = int(self.entry_id.get())
            estudiante = None
            for e in self.estudiantes:
                if e.id == id_buscar:
                    estudiante = e
                    break
            
            if estudiante is None:
                messagebox.showwarning("Error", f"No se encontró estudiante con ID {id_buscar}")
                return
            
            self.area_resultados.delete(1.0, tk.END)
            self.area_resultados.insert(tk.END, "-"*40 + "\n")
            self.area_resultados.insert(tk.END, f"ESTUDIANTE ID: {estudiante.id}\n")
            self.area_resultados.insert(tk.END, "-"*40 + "\n\n")
            self.area_resultados.insert(tk.END, f"📊 Promedio: {estudiante.promedio_primer_semestre}/20\n")
            self.area_resultados.insert(tk.END, f"📚 Materias reprobadas: {estudiante.materias_reprobadas}\n")
            self.area_resultados.insert(tk.END, f"📅 Asistencia: {estudiante.asistencia_promedio}%\n")
            self.area_resultados.insert(tk.END, f"💼 Trabaja: {'Sí' if estudiante.trabaja else 'No'} ({estudiante.horas_trabajo}h)\n")
            self.area_resultados.insert(tk.END, f"📐 Reprobó Matemáticas: {'Sí' if estudiante.reprobo_matematicas_I else 'No'}\n")
            self.area_resultados.insert(tk.END, f"🧪 Reprobó Química: {'Sí' if estudiante.reprobo_quimica_I else 'No'}\n")
            self.area_resultados.insert(tk.END, f"📖 Realidad: {'DESERTÓ' if estudiante.deserto else 'NO DESERTÓ'}\n\n")
            
            # Predicción
            prediccion = self.sistema.predecir(estudiante)
            self.area_resultados.insert(tk.END, "🔮 PREDICCIÓN DEL SISTEMA:\n")
            if prediccion['deserta']:
                self.area_resultados.insert(tk.END, "   ⚠️ RIESGO ALTO DE DESERCIÓN\n\n")
            else:
                self.area_resultados.insert(tk.END, "   ✅ RIESGO BAJO DE DESERCIÓN\n\n")
            
            # Recomendaciones
            alerta = self.sistema.generar_alerta(estudiante)
            if alerta:
                self.area_resultados.insert(tk.END, "📋 RECOMENDACIONES:\n")
                for rec in alerta['recomendaciones']:
                    self.area_resultados.insert(tk.END, f"   {rec}\n")
                    
        except ValueError:
            messagebox.showwarning("Error", "Ingrese un ID válido (número)")
    
    def acerca_de(self):
        messagebox.showinfo("Acerca de", 
                           "Sistema de Predicción de Deserción Universitaria\n"
                           "Versión 1.0\n\n"
                           "Escala de notas: 0 a 20\n"
                           "Algoritmos: ID3 y Apriori")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppDesercion(root)
    root.mainloop()