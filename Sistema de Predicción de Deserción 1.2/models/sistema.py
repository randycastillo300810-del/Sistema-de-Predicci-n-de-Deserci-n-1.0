# models/sistema.py
# Versión corregida y completa (sin errores de indentación)

from models.arbol_decision import ArbolDecisionID3
from models.apriori import Apriori
from models.preprocesador import Preprocesador

class SistemaPrediccionDesercion:
    """
    Sistema completo de predicción de deserción
    NOTAS: escala 0-20
    """
    
    def __init__(self):
        self.arbol = ArbolDecisionID3()
        self.apriori = Apriori(soporte_minimo=0.03, confianza_minima=0.5)
        self.preprocesador = Preprocesador()
    
    def entrenar(self, estudiantes):
        """Entrena el sistema con datos de estudiantes"""
        print("\n" + "="*60)
        print("ENTRENANDO SISTEMA DE PREDICCIÓN")
        print("ESCALA DE NOTAS: 0 a 20 (aprueba con 10)")
        print("="*60)
        
        print("1. Preprocesando datos...")
        estudiantes_proc = self.preprocesador.preparar_para_arbol(estudiantes)
        
        atributos = [
            'estrato', 'promedio_categoria', 'asistencia_categoria',
            'materias_categoria', 'reprobo_matematicas_I', 'reprobo_quimica_I',
            'trabaja', 'carga_alta', 'bajo_rendimiento_inicial'
        ]
        
        print("2. Entrenando árbol de decisión ID3...")
        self.arbol.entrenar(estudiantes_proc, atributos, max_profundidad=5)
        
        print("3. Preparando transacciones para Apriori...")
        transacciones = self.preprocesador.preparar_para_apriori(estudiantes_proc)
        
        print("4. Generando reglas de asociación con Apriori...")
        self.apriori.generar_reglas(transacciones)
        
        print("\n✅ SISTEMA ENTRENADO CORRECTAMENTE")
        print(f"   Árbol de decisión: {self._contar_nodos(self.arbol.raiz)} nodos")
        print(f"   Reglas Apriori: {len(self.apriori.reglas)} reglas encontradas")
        print(f"   Reglas de deserción: {len(self.apriori.obtener_reglas_desercion())}")
    
    def _contar_nodos(self, nodo):
        if nodo is None:
            return 0
        if nodo.es_hoja():
            return 1
        total = 1
        for hijo in nodo.hijos.values():
            total += self._contar_nodos(hijo)
        return total
    
    def predecir(self, estudiante):
        """Predice riesgo para un estudiante"""
        if estudiante.promedio_categoria is None:
            estudiante.promedio_categoria = self.preprocesador.discretizar(
                estudiante.promedio_primer_semestre, 'promedio',
                self.preprocesador.cortes.get('promedio', [10, 14]))
        if estudiante.asistencia_categoria is None:
            estudiante.asistencia_categoria = self.preprocesador.discretizar(
                estudiante.asistencia_promedio, 'asistencia',
                self.preprocesador.cortes.get('asistencia', [70, 85]))
        if estudiante.materias_categoria is None:
            estudiante.materias_categoria = self.preprocesador.discretizar(
                estudiante.materias_reprobadas, 'materias',
                self.preprocesador.cortes.get('materias', [1, 3]))
        
        deserta = self.arbol.predecir(estudiante)
        return {'deserta': deserta, 'riesgo': 'ALTO' if deserta else 'BAJO'}
    
    def generar_alerta(self, estudiante):
        """Genera alerta completa con recomendaciones (solo si riesgo alto)"""
        prediccion = self.predecir(estudiante)
        if not prediccion['deserta']:
            return None
        #CODIGO DE RANDY CASTILLO 30727559
        recomendaciones = []
        if estudiante.reprobo_matematicas_I:
            recomendaciones.append("📐 Asignar tutoría de matemáticas")
        if estudiante.reprobo_quimica_I:
            recomendaciones.append("🧪 Asignar tutoría de química")
        if estudiante.bajo_rendimiento_inicial:
            recomendaciones.append(f"📚 Inscribir en curso de nivelación (promedio: {estudiante.promedio_primer_semestre}/20)")
        if estudiante.trabaja and estudiante.horas_trabajo > 20:
            recomendaciones.append("💼 Evaluar opciones de beca o reducción de carga laboral")
        if estudiante.asistencia_promedio < 70:
            recomendaciones.append(f"📅 Programar seguimiento de asistencia ({estudiante.asistencia_promedio}%)")
        if not estudiante.tutorias_asistio:
            recomendaciones.append("🎓 Invitar a sesiones de tutoría")
        if estudiante.rezago_academico:
            recomendaciones.append(f"📖 Reducir carga académica ({estudiante.materias_reprobadas} materias reprobadas)")
        if estudiante.carga_alta:
            recomendaciones.append("⚖️ Evaluar apoyo para conciliar estudio y trabajo/familia")
        
        return {
            'estudiante_id': estudiante.id,
            'riesgo': prediccion['riesgo'],
            'nota_promedio': estudiante.promedio_primer_semestre,
            'factores': self._identificar_factores(estudiante),
            'recomendaciones': recomendaciones
        }
    
    def _identificar_factores(self, estudiante):
        """Identifica factores de riesgo del estudiante (versión mejorada)"""
        factores = []
        
        # Rendimiento
        if estudiante.bajo_rendimiento_inicial:
            factores.append(f"Bajo rendimiento inicial (nota {estudiante.promedio_primer_semestre}/20)")
        elif estudiante.promedio_primer_semestre < 12:
            factores.append(f"Nota moderada ({estudiante.promedio_primer_semestre}/20) - requiere seguimiento")
        
        if estudiante.reprobo_matematicas_I:
            factores.append("Reprobó Matemáticas I")
        if estudiante.reprobo_quimica_I:
            factores.append("Reprobó Química I")
        if estudiante.rezago_academico:
            factores.append(f"Rezago académico ({estudiante.materias_reprobadas} materias reprobadas)")
        
        # Asistencia
        if estudiante.baja_asistencia:
            factores.append(f"Baja asistencia ({estudiante.asistencia_promedio}%)")
        elif estudiante.asistencia_promedio < 85:
            factores.append(f"Asistencia moderada ({estudiante.asistencia_promedio}%) - puede mejorar")
        
        # Carga personal
        if estudiante.carga_alta:
            motivos = []
            if estudiante.trabaja and estudiante.horas_trabajo > 20:
                motivos.append(f"trabaja {estudiante.horas_trabajo}h")
            if estudiante.hijos:
                motivos.append("tiene hijos")
            factores.append(f"Carga alta ({', '.join(motivos)})")
        elif estudiante.trabaja and estudiante.horas_trabajo > 0:
            factores.append(f"Trabaja {estudiante.horas_trabajo}h (carga moderada)")
        
        # Tutorías no utilizadas
        if not estudiante.tutorias_asistio and (estudiante.reprobo_matematicas_I or estudiante.reprobo_quimica_I or estudiante.promedio_primer_semestre < 12):
            factores.append("No ha utilizado las tutorías disponibles")
        
        # Categorías discretizadas (para depurar)
        if estudiante.promedio_categoria is None:
            estudiante.promedio_categoria = self.preprocesador.discretizar(
                estudiante.promedio_primer_semestre, 'promedio',
                self.preprocesador.cortes.get('promedio', [10, 14]))
        if estudiante.asistencia_categoria is None:
            estudiante.asistencia_categoria = self.preprocesador.discretizar(
                estudiante.asistencia_promedio, 'asistencia',
                self.preprocesador.cortes.get('asistencia', [70, 85]))
        
        if estudiante.asistencia_categoria == 'baja' and "Baja asistencia" not in str(factores):
            factores.append(f"Asistencia en categoría baja ({estudiante.asistencia_promedio}%)")
        if estudiante.promedio_categoria == 'bajo':
            factores.append(f"Promedio bajo ({estudiante.promedio_primer_semestre}/20) - categoría baja")
        elif estudiante.promedio_categoria == 'medio' and estudiante.asistencia_categoria == 'baja':
            factores.append(f"Combinación: nota media ({estudiante.promedio_primer_semestre}/20) con baja asistencia")
        
        if not factores:
            factores.append("Factores no específicos, pero el árbol de decisión detectó riesgo")
        
        return factores
    
    def generar_reporte(self, estudiantes, top_n=None):
        """Genera reporte de estudiantes en riesgo. top_n=None devuelve todos."""
        alertas = []
        for e in estudiantes:
            alerta = self.generar_alerta(e)
            if alerta:
                alertas.append(alerta)
        alertas.sort(key=lambda x: x.get('nota_promedio', 20))
        return alertas if top_n is None else alertas[:top_n]
    
    def mostrar_estadisticas(self, estudiantes):
        """Muestra estadísticas generales (modo consola)"""
        total = len(estudiantes)
        desertores = sum(1 for e in estudiantes if e.deserto)
        print("\n" + "="*60)
        print("ESTADÍSTICAS GENERALES (Escala 0-20)")
        print("="*60)
        print(f"Total estudiantes: {total}")
        print(f"Desertores: {desertores} ({desertores/total*100:.1f}%)")
        notas = [e.promedio_primer_semestre for e in estudiantes]
        print(f"Promedio general: {sum(notas)/len(notas):.1f}/20")
        print(f"Mínima: {min(notas):.1f} | Máxima: {max(notas):.1f}")
    
    def mostrar_reglas(self, max_reglas=10):
        reglas = self.apriori.obtener_reglas_desercion()
        print("\n" + "="*60)
        print("REGLAS DE ASOCIACIÓN - DESERCIÓN")
        print("="*60)
        if not reglas:
            print("No se encontraron reglas.")
            return
        for i, r in enumerate(reglas[:max_reglas], 1):
            ant = " Y ".join(sorted(r['antecedente']))
            print(f"{i}. SI [{ant}] → deserto (confianza {r['confianza']*100:.1f}%)")
    
    def mostrar_arbol(self):
        print("\n" + "="*60)
        print("ÁRBOL DE DECISIÓN (ID3)")
        print("Escala: bajo=<10, medio=10-14, alto=>14")
        print("="*60)
        self.arbol.imprimir()
    
    def diagnosticar_estudiante(self, estudiante):
        """Diagnóstico detallado para depuración"""
        if estudiante.promedio_categoria is None:
            estudiante.promedio_categoria = self.preprocesador.discretizar(
                estudiante.promedio_primer_semestre, 'promedio',
                self.preprocesador.cortes.get('promedio', [10, 14]))
        if estudiante.asistencia_categoria is None:
            estudiante.asistencia_categoria = self.preprocesador.discretizar(
                estudiante.asistencia_promedio, 'asistencia',
                self.preprocesador.cortes.get('asistencia', [70, 85]))
        if estudiante.materias_categoria is None:
            estudiante.materias_categoria = self.preprocesador.discretizar(
                estudiante.materias_reprobadas, 'materias',
                self.preprocesador.cortes.get('materias', [1, 3]))
        
        deserta = self.arbol.predecir(estudiante)
        factores = self._identificar_factores(estudiante)
        
        return {
            'id': estudiante.id,
            'nota_real': estudiante.promedio_primer_semestre,
            'nota_categoria': estudiante.promedio_categoria,
            'asistencia_categoria': estudiante.asistencia_categoria,
            'materias_categoria': estudiante.materias_categoria,
            'reprobo_mate': estudiante.reprobo_matematicas_I,
            'reprobo_quimica': estudiante.reprobo_quimica_I,
            'trabaja': estudiante.trabaja,
            'horas_trabajo': estudiante.horas_trabajo,
            'carga_alta': estudiante.carga_alta,
            'bajo_rendimiento': estudiante.bajo_rendimiento_inicial,
            'rezago_academico': estudiante.rezago_academico,
            'baja_asistencia': estudiante.baja_asistencia,
            'factores': factores,
            'prediccion': 'ALTO' if deserta else 'BAJO'
        }