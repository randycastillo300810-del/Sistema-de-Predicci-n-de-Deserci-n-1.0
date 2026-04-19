# models/sistema.py

from models.arbol_decision import ArbolDecisionID3
from models.apriori import Apriori
from models.preprocesador import Preprocesador

class SistemaPrediccionDesercion:
    """
    Sistema completo de predicción de deserción
    """
    
    def __init__(self):
        self.arbol = ArbolDecisionID3()
        self.apriori = Apriori(soporte_minimo=0.05, confianza_minima=0.6)
        self.preprocesador = Preprocesador()
    
    def entrenar(self, estudiantes):
        """Entrena el sistema con datos de estudiantes"""
        print("\n" + "="*60)
        print("ENTRENANDO SISTEMA DE PREDICCIÓN")
        print("="*60)
        
        # Preprocesar
        print("1. Preprocesando datos...")
        estudiantes_proc = self.preprocesador.preparar_para_arbol(estudiantes)
        
        # Atributos para el árbol
        atributos = [
            'estrato', 'promedio_categoria', 'asistencia_categoria',
            'materias_categoria', 'reprobo_matematicas_I', 'reprobo_quimica_I',
            'trabaja', 'carga_alta', 'bajo_rendimiento_inicial'
        ]
        
        # Entrenar árbol
        print("2. Entrenando árbol de decisión ID3...")
        self.arbol.entrenar(estudiantes_proc, atributos, max_profundidad=5)
        
        # Preparar para Apriori
        print("3. Preparando transacciones para Apriori...")
        transacciones = self.preprocesador.preparar_para_apriori(estudiantes_proc)
        
        # Entrenar Apriori
        print("4. Generando reglas de asociación con Apriori...")
        self.apriori.generar_reglas(transacciones)
        
        print("\n✅ SISTEMA ENTRENADO CORRECTAMENTE")
        print(f"   Árbol de decisión: {self._contar_nodos(self.arbol.raiz)} nodos")
        print(f"   Reglas Apriori: {len(self.apriori.reglas)} reglas encontradas")
        print(f"   Reglas de deserción: {len(self.apriori.obtener_reglas_desercion())}")
    
    def _contar_nodos(self, nodo):
        """Cuenta nodos del árbol"""
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
        # Discretizar variables
        estudiante.promedio_categoria = self.preprocesador.discretizar(
            estudiante.promedio_primer_semestre, 'promedio', 
            self.preprocesador.cortes.get('promedio', [3.0, 4.0]))
        estudiante.asistencia_categoria = self.preprocesador.discretizar(
            estudiante.asistencia_promedio, 'asistencia',
            self.preprocesador.cortes.get('asistencia', [70, 85]))
        estudiante.materias_categoria = self.preprocesador.discretizar(
            estudiante.materias_reprobadas, 'materias',
            self.preprocesador.cortes.get('materias', [1, 3]))
        
        deserta = self.arbol.predecir(estudiante)
        
        return {
            'deserta': deserta,
            'riesgo': 'ALTO' if deserta else 'BAJO'
        }
    
    def generar_alerta(self, estudiante):
        """Genera alerta completa con recomendaciones"""
        prediccion = self.predecir(estudiante)
        
        if not prediccion['deserta']:
            return None
        
        # Generar recomendaciones basadas en factores
        recomendaciones = []
        
        if estudiante.reprobo_matematicas_I:
            recomendaciones.append("📐 Asignar tutoría de matemáticas")
        if estudiante.reprobo_quimica_I:
            recomendaciones.append("🧪 Asignar tutoría de química")
        if estudiante.bajo_rendimiento_inicial:
            recomendaciones.append("📚 Inscribir en curso de nivelación académica")
        if estudiante.trabaja and estudiante.horas_trabajo > 20:
            recomendaciones.append("💼 Evaluar opciones de beca o reducción de carga laboral")
        if estudiante.asistencia_promedio < 70:
            recomendaciones.append("📅 Programar seguimiento de asistencia semanal")
        if not estudiante.tutorias_asistio:
            recomendaciones.append("🎓 Invitar a sesiones de tutoría")
        if estudiante.rezago_academico:
            recomendaciones.append("📖 Reducir carga académica temporalmente")
        
        return {
            'estudiante_id': estudiante.id,
            'riesgo': prediccion['riesgo'],
            'factores': self._identificar_factores(estudiante),
            'recomendaciones': recomendaciones
        }
    
    def _identificar_factores(self, estudiante):
        """Identifica factores de riesgo del estudiante"""
        factores = []
        if estudiante.bajo_rendimiento_inicial:
            factores.append("Bajo rendimiento en primer semestre")
        if estudiante.reprobo_matematicas_I:
            factores.append("Reprobó Matemáticas I")
        if estudiante.reprobo_quimica_I:
            factores.append("Reprobó Química I")
        if estudiante.rezago_academico:
            factores.append("Rezago académico (más de 2 materias reprobadas)")
        if estudiante.carga_alta:
            factores.append("Carga alta (trabaja >20h o tiene hijos)")
        if estudiante.baja_asistencia:
            factores.append(f"Baja asistencia ({estudiante.asistencia_promedio}%)")
        return factores
    
    def generar_reporte(self, estudiantes, top_n=10):
        """Genera reporte completo con estudiantes en riesgo"""
        alertas = []
        for e in estudiantes:
            alerta = self.generar_alerta(e)
            if alerta:
                alertas.append(alerta)
        
        # Ordenar por riesgo (los de riesgo alto primero)
        alertas.sort(key=lambda x: 0 if x['riesgo'] == 'ALTO' else 1)
        
        return alertas[:top_n]
    
    def mostrar_estadisticas(self, estudiantes):
        """Muestra estadísticas generales"""
        total = len(estudiantes)
        desertores = sum(1 for e in estudiantes if e.deserto)
        
        print("\n" + "="*60)
        print("ESTADÍSTICAS GENERALES")
        print("="*60)
        print(f"Total estudiantes: {total}")
        print(f"Desertores: {desertores} ({desertores/total*100:.1f}%)")
        print(f"No desertores: {total - desertores}")
        
        # Por estrato
        print("\n📊 Deserción por estrato:")
        for estrato in range(1, 7):
            grupo = [e for e in estudiantes if e.estrato == estrato]
            if grupo:
                des = sum(1 for e in grupo if e.deserto)
                print(f"  Estrato {estrato}: {des}/{len(grupo)} ({des/len(grupo)*100:.1f}%)")
        
        # Por materias críticas
        print("\n📚 Impacto de materias críticas:")
        reprobados_mate = [e for e in estudiantes if e.reprobo_matematicas_I]
        if reprobados_mate:
            des_mate = sum(1 for e in reprobados_mate if e.deserto)
            print(f"  Reprobar Matemáticas I: {des_mate}/{len(reprobados_mate)} ({des_mate/len(reprobados_mate)*100:.1f}% desertan)")
        
        reprobados_quimica = [e for e in estudiantes if e.reprobo_quimica_I]
        if reprobados_quimica:
            des_quimica = sum(1 for e in reprobados_quimica if e.deserto)
            print(f"  Reprobar Química I: {des_quimica}/{len(reprobados_quimica)} ({des_quimica/len(reprobados_quimica)*100:.1f}% desertan)")
        
        # Por carga
        carga_alta = [e for e in estudiantes if e.carga_alta]
        if carga_alta:
            des_carga = sum(1 for e in carga_alta if e.deserto)
            print(f"  Carga alta (trabaja >20h o hijos): {des_carga}/{len(carga_alta)} ({des_carga/len(carga_alta)*100:.1f}% desertan)")
    
    def mostrar_reglas(self, max_reglas=10):
        """Muestra las mejores reglas de asociación"""
        reglas_desercion = self.apriori.obtener_reglas_desercion()
        
        print("\n" + "="*60)
        print("REGLAS DE ASOCIACIÓN - PREDICCIÓN DE DESERCIÓN")
        print("="*60)
        
        for i, regla in enumerate(reglas_desercion[:max_reglas]):
            ant = " Y ".join(sorted(regla['antecedente']))
            con = " Y ".join(sorted(regla['consecuente']))
            
            print(f"\nRegla {i+1}:")
            print(f"  SI [{ant}]")
            print(f"  ENTONCES [{con}]")
            print(f"  Soporte: {regla['soporte']*100:.1f}% | Confianza: {regla['confianza']*100:.1f}%")
    
    def mostrar_arbol(self):
        """Muestra la estructura del árbol de decisión"""
        print("\n" + "="*60)
        print("ÁRBOL DE DECISIÓN (ID3)")
        print("="*60)
        self.arbol.imprimir()