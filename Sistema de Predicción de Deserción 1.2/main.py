# main.py
# Versión con lista completa de riesgo y búsqueda por ID

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
    print("5. Predecir estudiante individual (por ID)")
    print("6. Mostrar TODOS los estudiantes en riesgo (lista completa)")
    print("7. Mostrar TOP 10 estudiantes en riesgo")
    print("8. Salir")
    print("="*60)

def mostrar_estudiante_detalle(estudiante, sistema):
    """Muestra detalles completos de un estudiante y su predicción (similar a diagnóstico)"""
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
    print(f"📖 Realidad histórica: {'DESERTÓ' if estudiante.deserto else 'NO DESERTÓ'}")
    
    # Predicción del sistema
    prediccion = sistema.predecir(estudiante)
    print(f"\n🔮 PREDICCIÓN DEL SISTEMA:")
    if prediccion['deserta']:
        print(f"   ⚠️ RIESGO ALTO DE DESERCIÓN")
    else:
        print(f"   ✅ RIESGO BAJO DE DESERCIÓN")
    
    # Factores de riesgo (usando el método mejorado)
    alerta = sistema.generar_alerta(estudiante)
    if alerta:
        if alerta['factores']:
            print(f"\n📋 Factores de riesgo detectados:")
            for factor in alerta['factores']:
                print(f"   • {factor}")
        if alerta['recomendaciones']:
            print(f"\n💡 Recomendaciones:")
            for rec in alerta['recomendaciones']:
                print(f"   {rec}")

#CODIGO DE RANDY CASTILLO 30727559

def mostrar_lista_completa_riesgo(sistema, estudiantes):
    """Muestra TODOS los estudiantes en riesgo (sin límite)"""
    alertas = sistema.generar_reporte(estudiantes, top_n=None)
    if not alertas:
        print("\n✅ No hay estudiantes en riesgo.")
        return
    print("\n" + "="*60)
    print(f"⚠️ LISTA COMPLETA DE ESTUDIANTES EN RIESGO ({len(alertas)} en total)")
    print("="*60)
    for i, a in enumerate(alertas, 1):
        print(f"{i}. ID: {a['estudiante_id']} | Nota: {a['nota_promedio']}/20 | Riesgo: {a['riesgo']}")
        if a['factores']:
            print(f"   Factores: {', '.join(a['factores'][:3])}")
        else:
            print(f"   Factores: (ninguno específico)")
        if a['recomendaciones']:
            print(f"   💡 {a['recomendaciones'][0]}")
        print("-"*50)

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
                try:
                    id_buscar = int(input("\nIngrese el ID del estudiante a predecir: "))
                    estudiante = next((e for e in estudiantes if e.id == id_buscar), None)
                    if not estudiante:
                        print(f"❌ No existe estudiante con ID {id_buscar}")
                    else:
                        mostrar_estudiante_detalle(estudiante, sistema)
                except ValueError:
                    print("❌ Ingrese un número válido")
                    
        elif opcion == "6":
            if sistema is None or estudiantes is None:
                print("\n⚠️ Primero debe entrenar el sistema (opción 1)")
            else:
                mostrar_lista_completa_riesgo(sistema, estudiantes)
        
        elif opcion == "7":
            if sistema is None or estudiantes is None:
                print("\n⚠️ Primero debe entrenar el sistema (opción 1)")
            else:
                print("\n" + "="*60)
                print("TOP 10 ESTUDIANTES EN RIESGO")
                print("="*60)
                alertas = sistema.generar_reporte(estudiantes, top_n=10)
                if not alertas:
                    print("✅ No hay estudiantes en riesgo.")
                else:
                    for i, a in enumerate(alertas, 1):
                        print(f"{i}. ID: {a['estudiante_id']} | Nota: {a['nota_promedio']}/20 | Riesgo: {a['riesgo']}")
                        if a['factores']:
                            print(f"   Factores: {', '.join(a['factores'][:2])}")
                        if a['recomendaciones']:
                            print(f"   💡 {a['recomendaciones'][0]}")
                        print("-"*40)
                        
        elif opcion == "8":
            print("\n👋 Saliendo del sistema...")
            break
            
        else:
            print("\n⚠️ Opción no válida. Intente de nuevo.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()