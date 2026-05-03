# models/estudiante.py

class Estudiante:

    #Clasificación del estudiante basada en sus atributos
    
    def __init__(self, id, datos):
        self.id = id
        
        # DATOS DEMOGRÁFICOS
        self.edad = datos.get('edad', 18)
        self.genero = datos.get('genero', 'M')
        self.estrato = datos.get('estrato', 3)
        self.foraneo = datos.get('foraneo', False)
        self.trabaja = datos.get('trabaja', False)
        self.horas_trabajo = datos.get('horas_trabajo', 0)
        self.hijos = datos.get('hijos', False)
        self.educacion_padres = datos.get('educacion_padres', 1)
        
        # RENDIMIENTO ACADÉMICO
        self.promedio_primer_semestre = datos.get('promedio_primer_semestre', 3.0)
        self.promedio_acumulado = datos.get('promedio_acumulado', 3.0)
        self.materias_reprobadas = datos.get('materias_reprobadas', 0)
        self.materias_retiradas = datos.get('materias_retiradas', 0)
        
        # MATERIAS CRÍTICAS
        self.reprobo_matematicas_I = datos.get('reprobo_matematicas_I', False)
        self.reprobo_quimica_I = datos.get('reprobo_quimica_I', False)
        
        # COMPROMISO
        self.asistencia_promedio = datos.get('asistencia_promedio', 85.0)
        self.tutorias_asistio = datos.get('tutorias_asistio', False)
        
        # FACTORES DE RIESGO COMPUESTOS
        self.carga_alta = (self.trabaja and self.horas_trabajo > 20) or self.hijos
        self.rezago_academico = self.materias_reprobadas > 2
        self.bajo_rendimiento_inicial = self.promedio_primer_semestre < 3.0
        self.baja_asistencia = self.asistencia_promedio < 70
        
        # VARIABLE OBJETIVO
        self.deserto = datos.get('deserto', False)
        
        # VARIABLES DISCRETIZADAS (se llenan después)
        self.promedio_categoria = None
        self.asistencia_categoria = None
        self.materias_categoria = None
    
    def __repr__(self):
        estado = "DESERTÓ" if self.deserto else "ACTIVO"
        return f"Estudiante {self.id} | Promedio: {self.promedio_primer_semestre} | {estado}"