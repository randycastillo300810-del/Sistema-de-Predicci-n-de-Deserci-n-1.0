# main.py

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.generador_datos import GeneradorDatos
from models.sistema import SistemaPrediccionDesercion

def mostrar_menu():
    print("\n" + "="*60)
    print("SISTEMA DE PREDICCIÓN DE DESERCIÓN UNIVERSITARIA")
    print("ESCALA DE NOTAS: 0 a 20 (aprueba con 10)")
    print("="*60)
    print("1. Generar datos y entrenar sistema")
    print("2. Mostrar estadísticas generales")
    print("3. Mostrar reglas de asociación (Apriori)")
    print("4. Mostrar árbol de decisión")
    print("5. Predecir estudiante individual")
    print("6. Mostrar estudiantes en riesgo (TOP 10)")
    print("7. Salir")
    print("="*60)

def mostrar_estudiante_detalle(estudiante, sistema):
    """Muestra detalles de un estudiante y su predicción"""
    print("\n" + "-"*40)
    print(f"ESTUDIANTE ID: {estudiante.id}")
    print("-"*40)
    print(f"📊 Promedio primer semestre: {estudiante.promedio_primer_semestre}/20")
    print(f"📚 Materias reprobadas: {estudiante.materias_reprobadas}")
    print(f"📅 Asistencia: {estudiante.asistencia_promedio}%")
    print(f"💼 Trabaja: {'Sí' if estudiante.trabaja else 'No'} ({estudiante.horas_trabajo}h)" if estudiante.trabaja else "💼 No trabaja")
    print(f"👨‍👩‍👧 Hijos: {'Sí' if estudiante.hijos else 'No'}")
    print(f"📐 Reprobó Matemáticas I: {'Sí' if estudiante.reprobo_matematicas_I else 'No'}")
    print(f"🧪 Reprobó Química I: {'Sí' if estudiante.reprobo_quimica_I else 'No'}")
    print(f"🎓 Asistió a tutorías: {'Sí' if estudiante.tutorias_asistio else 'No'}")
    print(f"📖 Realidad: {'DESERTÓ' if estudiante.deserto else 'NO DESERTÓ'}")
    
    # Predicción
    prediccion = sistema.predecir(estudiante)
    print(f"\n🔮 PREDICCIÓN DEL SISTEMA:")
    if prediccion['deserta']:
        print(f"   ⚠️ RIESGO ALTO DE DESERCIÓN")
    else:
        print(f"   ✅ RIESGO BAJO DE DESERCIÓN")
    
    # Alerta con recomendaciones
    alerta = sistema.generar_alerta(estudiante)
    if alerta:
        print(f"\n📋 RECOMENDACIONES:")
        for rec in alerta['recomendaciones']:
            print(f"   {rec}")

def main():
    sistema = None
    estudiantes = None
    generador = GeneradorDatos(seed=42)
    
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            print("\n🔄 Generando datos sintéticos...")
            estudiantes = generador.generar_dataset(n=500)
            print(f"✅ Generados {len(estudiantes)} estudiantes")
            
            sistema = SistemaPrediccionDesercion()
            sistema.entrenar(estudiantes)
            
        elif opcion == "2":
            if sistema is None or estudiantes is None:
                print("\n⚠️ Primero debe entrenar el sistema (opción 1)")
            else:
                sistema.mostrar_estadisticas(estudiantes)
                
        elif opcion == "3":
            if sistema is None:
                print("\n⚠️ Primero debe entrenar el sistema (opción 1)")
            else:
                sistema.mostrar_reglas(max_reglas=10)
                
        elif opcion == "4":
            if sistema is None:
                print("\n⚠️ Primero debe entrenar el sistema (opción 1)")
            else:
                sistema.mostrar_arbol()
                
        elif opcion == "5":
            if sistema is None or estudiantes is None:
                print("\n⚠️ Primero debe entrenar el sistema (opción 1)")
            else:
                print("\n" + "="*60)
                print("PREDICCIÓN DE ESTUDIANTE INDIVIDUAL")
                print("="*60)
                
                print("\nEstudiantes disponibles:")
                for i, e in enumerate(estudiantes[:10]):
                    print(f"  {i+1}. ID: {e.id} | Promedio: {e.promedio_primer_semestre}/20 | {'Desertó' if e.deserto else 'Activo'}")
                
                try:
                    idx = int(input("\nSeleccione número de estudiante (1-10): ")) - 1
                    if 0 <= idx < len(estudiantes):
                        mostrar_estudiante_detalle(estudiantes[idx], sistema)
                    else:
                        print("Opción inválida")
                except ValueError:
                    print("Ingrese un número válido")
                    
        elif opcion == "6":
            if sistema is None or estudiantes is None:
                print("\n⚠️ Primero debe entrenar el sistema (opción 1)")
            else:
                print("\n" + "="*60)
                print("ESTUDIANTES EN RIESGO (TOP 10)")
                print("ESCALA DE NOTAS: 0 a 20")
                print("="*60)
                
                alertas = sistema.generar_reporte(estudiantes, top_n=10)
                
                for i, alerta in enumerate(alertas):
                    print(f"\n{i+1}. Estudiante ID: {alerta['estudiante_id']}")
                    print(f"   🔴 Riesgo: {alerta['riesgo']}")
                    print(f"   📊 Nota promedio: {alerta['nota_promedio']}/20")
                    print(f"   📋 Factores: {', '.join(alerta['factores'][:3])}")
                    if alerta['recomendaciones']:
                        print(f"   💡 Recomendación: {alerta['recomendaciones'][0]}")
                        
        elif opcion == "7":
            print("\n👋 Saliendo del sistema...")
            break
            
        else:
            print("\n⚠️ Opción no válida. Intente de nuevo.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()