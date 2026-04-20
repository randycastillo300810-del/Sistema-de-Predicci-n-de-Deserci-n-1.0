Programas que se tiene que ejecutar para el uso de el programa:
main.py: main.py
¿Qué hace?
Proporciona un menú interactivo en consola para que el usuario use el programa. Ofrece opciones como: entrenar sistema, ver estadísticas, predecir un estudiante, ver reglas, etc.

interfaz_1.py y interfaz_2.py
Es lo mismo que main pero con una interfaz gráfica (ventanas, botones, cajas de texto) para el mismo sistema que al ejercutarse genera dos pestañas una con la interfaz y otra con una terminal.

Mini resumen de los 7 módulos del proyecto
1. estudiante.py
¿Qué hace?
Define la estructura de datos de un estudiante. Es como un molde que guarda toda la información relevante: edad, notas, materias reprobadas, si trabaja, si desertó, etc.

Para qué sirve:
Para que el resto del programa pueda crear, almacenar y manejar estudiantes de forma uniforme.

2. generador_datos.py
¿Qué hace?
Crea estudiantes falsos pero realistas para poder probar el sistema sin necesidad de tener datos reales de la universidad. Genera automáticamente 500 estudiantes con notas entre 0 y 20, y decide si desertan o no según su rendimiento y factores de riesgo.

Para qué sirve:
Permite entrenar y demostrar el sistema aunque no tengas acceso a una base de datos real.

3. preprocesador.py
¿Qué hace?
Prepara los datos para que los algoritmos los entiendan. Convierte números en categorías (ej: promedio 9.2 → "bajo", asistencia 85% → "alta"). También transforma a cada estudiante en una lista de condiciones para el algoritmo Apriori.

Para qué sirve:
Los algoritmos de machine learning trabajan mejor con categorías y con transacciones de condiciones, no con números sueltos.

4. arbol_decision.py
¿Qué hace?
Implementa el Árbol de Decisión ID3 desde cero. Construye un árbol de preguntas (¿promedio bajo? ¿reprobó matemáticas?) que clasifica a los estudiantes en riesgo alto o riesgo bajo de deserción.

Para qué sirve:
Es el corazón de la predicción. Aprende de los datos históricos y luego puede predecir el riesgo de un nuevo estudiante.

5. apriori.py
¿Qué hace?
Implementa el algoritmo Apriori para encontrar reglas de asociación. Descubre patrones como:

"SI promedio bajo Y reprobó matemáticas ENTONCES deserto" (con 85% de confianza)

Para qué sirve:
Explica por qué un estudiante está en riesgo y permite generar recomendaciones específicas (ej: "asignar tutoría de matemáticas").

6. sistema.py
¿Qué hace?
Es el director de orquesta. Integra el árbol de decisión y el Apriori, entrena ambos con los datos, predice estudiantes individuales, genera alertas y muestra estadísticas.

Para qué sirve:
Unifica toda la funcionalidad en una sola clase fácil de usar. Sin este módulo tendrías que usar cada algoritmo por separado.


