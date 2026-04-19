# models/preprocesador.py

class Preprocesador:
    """
    Prepara los datos para los algoritmos
    NOTAS: escala 0-20
    """
    
    def __init__(self):
        self.cortes = {}
    
    def discretizar(self, valor, nombre, cortes):
        """Discretiza un valor según cortes predefinidos"""
        if valor is None:
            return 'medio'
        
        if nombre not in self.cortes:
            return 'medio'
        
        cortes_var = self.cortes[nombre]
        
        if valor < cortes_var[0]:
            return 'bajo'
        elif valor < cortes_var[1]:
            return 'medio'
        else:
            return 'alto'
    
    def calcular_cortes(self, estudiantes, nombre, valores):
        """Calcula cortes de percentiles para una variable"""
        if not valores:
            # Valores por defecto para escala 0-20
            if nombre == 'promedio':
                self.cortes[nombre] = [10, 14]  # bajo: <10, medio: 10-14, alto: >14
            elif nombre == 'asistencia':
                self.cortes[nombre] = [70, 85]
            elif nombre == 'materias':
                self.cortes[nombre] = [1, 3]
            return
        
        valores_ordenados = sorted(valores)
        n = len(valores_ordenados)
        
        # Percentiles 33 y 66
        p33 = valores_ordenados[int(n * 0.33)]
        p66 = valores_ordenados[int(n * 0.66)]
        
        self.cortes[nombre] = [p33, p66]
    
    def preparar_para_arbol(self, estudiantes):
        """
        Prepara estudiantes para el árbol de decisión
        """
        # Recolectar valores
        promedios = [e.promedio_primer_semestre for e in estudiantes]
        asistencias = [e.asistencia_promedio for e in estudiantes]
        materias = [e.materias_reprobadas for e in estudiantes]
        
        # Calcular cortes
        self.calcular_cortes(estudiantes, 'promedio', promedios)
        self.calcular_cortes(estudiantes, 'asistencia', asistencias)
        self.calcular_cortes(estudiantes, 'materias', materias)
        
        # Discretizar cada estudiante
        for e in estudiantes:
            e.promedio_categoria = self.discretizar(e.promedio_primer_semestre, 'promedio', self.cortes.get('promedio', [10, 14]))
            e.asistencia_categoria = self.discretizar(e.asistencia_promedio, 'asistencia', self.cortes.get('asistencia', [70, 85]))
            e.materias_categoria = self.discretizar(e.materias_reprobadas, 'materias', self.cortes.get('materias', [1, 3]))
        
        return estudiantes
    
    def preparar_para_apriori(self, estudiantes):
        """
        Prepara estudiantes para Apriori
        """
        transacciones = []
        
        for e in estudiantes:
            transaccion = set()
            
            # Variables discretizadas
            transaccion.add(f"promedio_{e.promedio_categoria}")
            transaccion.add(f"asistencia_{e.asistencia_categoria}")
            transaccion.add(f"materias_{e.materias_categoria}")
            
            # Variables categóricas
            transaccion.add(f"estrato_{e.estrato}")
            
            # Variables booleanas
            if e.trabaja:
                transaccion.add(f"trabaja_{e.horas_trabajo}h")
            if e.reprobo_matematicas_I:
                transaccion.add("reprobo_matematicas")
            if e.reprobo_quimica_I:
                transaccion.add("reprobo_quimica")
            if e.bajo_rendimiento_inicial:
                transaccion.add("bajo_rendimiento")  # promedio < 10
            if e.rezago_academico:
                transaccion.add("rezago_academico")
            if e.carga_alta:
                transaccion.add("carga_alta")
            if e.tutorias_asistio:
                transaccion.add("tutorias")
            
            # Variable objetivo
            if e.deserto:
                transaccion.add("deserto")
            else:
                transaccion.add("no_deserto")
            
            transacciones.append(transaccion)
        
        return transacciones