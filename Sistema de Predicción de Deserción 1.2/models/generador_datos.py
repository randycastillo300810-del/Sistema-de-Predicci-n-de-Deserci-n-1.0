# models/generador_datos.py
# VERSIÓN CORREGIDA - ESCALA 0-20

import random

class GeneradorDatos:
    def __init__(self, seed=42):
        random.seed(seed)
    
    def generar_estudiante(self, id):
        # Generar nota DIRECTAMENTE en escala 0-20
        # NOTA: entre 0 y 20, media 12
        promedio = random.uniform(0, 20)
        
        # Decidir si deserta basado en la nota
        # NOTA: mientras más baja la nota, más probable que deserte
        if promedio < 8:
            deserto = True  # Nota muy baja, seguro deserta
        elif promedio < 10:
            deserto = random.random() < 0.8  # 80% deserta
        elif promedio < 12:
            deserto = random.random() < 0.5  # 50% deserta
        elif promedio < 14:
            deserto = random.random() < 0.2  # 20% deserta
        else:
            deserto = random.random() < 0.05  # 5% deserta
        
        # Materias reprobadas (reprobar = nota < 10)
        if promedio < 8:
            materias_reprobadas = random.randint(3, 5)
        elif promedio < 10:
            materias_reprobadas = random.randint(1, 3)
        elif promedio < 12:
            materias_reprobadas = random.randint(0, 1)
        else:
            materias_reprobadas = 0
        
        # Materias críticas
        reprobo_mate = promedio < 10 and random.random() < 0.5
        reprobo_quimica = promedio < 10 and random.random() < 0.4
        
        # Asistencia (relacionada con la nota)
        asistencia = min(100, max(0, promedio * 5 + random.gauss(0, 10)))
        
        # Trabajo (más común en notas bajas)
        trabaja = random.random() < (0.4 if promedio < 10 else 0.15)
        horas_trabajo = random.choice([0, 15, 20, 30]) if trabaja else 0
        
        datos = {
            'edad': random.randint(17, 30),
            'genero': random.choice(['M', 'F']),
            'estrato': random.randint(1, 6),
            'foraneo': random.random() < 0.3,
            'trabaja': trabaja,
            'horas_trabajo': horas_trabajo,
            'hijos': random.random() < 0.05,
            'educacion_padres': random.randint(0, 2),
            'promedio_primer_semestre': round(promedio, 1),
            'promedio_acumulado': round(promedio, 1),
            'materias_reprobadas': materias_reprobadas,
            'materias_retiradas': random.randint(0, 1) if promedio < 10 else 0,
            'reprobo_matematicas_I': reprobo_mate,
            'reprobo_quimica_I': reprobo_quimica,
            'asistencia_promedio': round(asistencia, 1),
            'tutorias_asistio': reprobo_mate or reprobo_quimica,
            'deserto': deserto
        }
        
        from models.estudiante import Estudiante
        return Estudiante(id, datos)
    
    def generar_dataset(self, n=500):
        estudiantes = []
        for i in range(n):
            estudiantes.append(self.generar_estudiante(i))
        return estudiantes