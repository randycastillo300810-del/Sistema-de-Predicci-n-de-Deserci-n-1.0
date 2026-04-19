# interfaz_moderna.py
import customtkinter as ctk
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.generador_datos import GeneradorDatos
from models.sistema import SistemaPrediccionDesercion

# Configurar tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppModerna:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Sistema de Predicción de Deserción")
        self.root.geometry("900x700")
        
        self.sistema = None
        self.estudiantes = None
        self.generador = GeneradorDatos()
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(self.main_frame, text="SISTEMA DE PREDICCIÓN DE DESERCIÓN",
                              font=("Arial", 24, "bold"))
        titulo.pack(pady=10)
        
        subtitulo = ctk.CTkLabel(self.main_frame, text="Escala de notas: 0 a 20 (aprueba con 10)",
                                 font=("Arial", 12))
        subtitulo.pack()
        
        # Frame de botones
        frame_botones = ctk.CTkFrame(self.main_frame)
        frame_botones.pack(pady=20, fill="x")
        
        # Botones
        btn_entrenar = ctk.CTkButton(frame_botones, text="1. Entrenar Sistema", 
                                      command=self.entrenar,
                                      fg_color="green")
        btn_entrenar.pack(side="left", padx=10, expand=True, fill="x")
        
        btn_estadisticas = ctk.CTkButton(frame_botones, text="2. Estadísticas", 
                                          command=self.estadisticas,
                                          fg_color="blue")
        btn_estadisticas.pack(side="left", padx=10, expand=True, fill="x")
        
        btn_reglas = ctk.CTkButton(frame_botones, text="3. Ver Reglas", 
                                    command=self.reglas,
                                    fg_color="orange")
        btn_reglas.pack(side="left", padx=10, expand=True, fill="x")
        
        # Área de texto para resultados
        self.text_area = ctk.CTkTextbox(self.main_frame, height=300, font=("Courier", 11))
        self.text_area.pack(pady=20, fill="both", expand=True)
        
        # Frame de predicción
        frame_pred = ctk.CTkFrame(self.main_frame)
        frame_pred.pack(pady=10, fill="x")
        
        ctk.CTkLabel(frame_pred, text="ID del estudiante:").pack(side="left", padx=10)
        self.entry_id = ctk.CTkEntry(frame_pred, width=100)
        self.entry_id.pack(side="left", padx=10)
        
        btn_predecir = ctk.CTkButton(frame_pred, text="Predecir", 
                                      command=self.predecir,
                                      fg_color="purple")
        btn_predecir.pack(side="left", padx=10)
        
        # Label de estado
        self.label_estado = ctk.CTkLabel(self.main_frame, text="⚠️ Primero entrene el sistema",
                                         text_color="red")
        self.label_estado.pack(pady=10)
    
    def escribir(self, texto):
        self.text_area.insert("end", texto + "\n")
        self.text_area.see("end")
        self.root.update()
    
    def entrenar(self):
        self.text_area.delete("1.0", "end")
        self.escribir("🔄 Generando datos sintéticos...")
        
        self.estudiantes = self.generador.generar_dataset(n=500)
        self.escribir(f"✅ Generados {len(self.estudiantes)} estudiantes")
        
        self.sistema = SistemaPrediccionDesercion()
        self.sistema.entrenar(self.estudiantes)
        
        self.label_estado.configure(text="✅ Sistema entrenado", text_color="green")
        self.escribir("\n✅ SISTEMA LISTO PARA USAR")
    
    def estadisticas(self):
        if self.sistema is None:
            self.escribir("⚠️ Primero entrene el sistema")
            return
        
        self.text_area.delete("1.0", "end")
        
        total = len(self.estudiantes)
        desertores = sum(1 for e in self.estudiantes if e.deserto)
        
        self.escribir("="*50)
        self.escribir("ESTADÍSTICAS GENERALES")
        self.escribir("="*50)
        self.escribir(f"Total estudiantes: {total}")
        self.escribir(f"Desertores: {desertores} ({desertores/total*100:.1f}%)")
        
        notas = [e.promedio_primer_semestre for e in self.estudiantes]
        self.escribir(f"\nPromedio general: {sum(notas)/len(notas):.1f}/20")
    
    def reglas(self):
        if self.sistema is None:
            self.escribir("⚠️ Primero entrene el sistema")
            return
        
        self.text_area.delete("1.0", "end")
        self.escribir("="*50)
        self.escribir("REGLAS DE ASOCIACIÓN")
        self.escribir("="*50)
        
        reglas = self.sistema.apriori.obtener_reglas_desercion()
        for i, regla in enumerate(reglas[:10]):
            ant = " Y ".join(sorted(regla['antecedente']))
            self.escribir(f"\nRegla {i+1}:")
            self.escribir(f"  SI [{ant}]")
            self.escribir(f"  Confianza: {regla['confianza']*100:.1f}%")
    
    def predecir(self):
        if self.sistema is None:
            self.escribir("⚠️ Primero entrene el sistema")
            return
        
        try:
            id_buscar = int(self.entry_id.get())
            estudiante = next((e for e in self.estudiantes if e.id == id_buscar), None)
            
            if estudiante is None:
                self.escribir(f"❌ Estudiante ID {id_buscar} no encontrado")
                return
            
            self.text_area.delete("1.0", "end")
            self.escribir("-"*40)
            self.escribir(f"ESTUDIANTE ID: {estudiante.id}")
            self.escribir("-"*40)
            self.escribir(f"Promedio: {estudiante.promedio_primer_semestre}/20")
            self.escribir(f"Materias reprobadas: {estudiante.materias_reprobadas}")
            self.escribir(f"Asistencia: {estudiante.asistencia_promedio}%")
            
            prediccion = self.sistema.predecir(estudiante)
            self.escribir(f"\n🔮 RIESGO: {'ALTO' if prediccion['deserta'] else 'BAJO'}")
            
        except ValueError:
            self.escribir("❌ Ingrese un ID válido")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AppModerna()
    app.run()