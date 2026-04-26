# Sistema de Predicción de Deserción 1.0 🎓📊

## 📝 Descripción
El programa es una herramienta de apoyo académico que utiliza inteligencia artificial (algoritmos ID3 y Apriori) para identificar estudiantes con riesgo de abandonar la universidad y generar alertas tempranas con recomendaciones personalizadas.

## ✨ Características Principales
* **Clasificación de Riesgo:** Utiliza árboles de decisión (algoritmo ID3) para clasificar el nivel de riesgo de deserción de un estudiante en base a su historial académico.
* **Descubrimiento de Patrones:** Implementa reglas de asociación (algoritmo Apriori) para encontrar patrones subyacentes y correlaciones entre materias reprobadas, asistencia y otros factores de riesgo.
* **Alertas Tempranas:** Genera notificaciones accionables para permitir intervenciones a tiempo por parte de la institución.

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3.x
* **Análisis de Datos:** pandas, numpy
* **Machine Learning:** scikit-learn (para árboles de decisión), mlxtend (para la implementación de Apriori)

## 📁 Estructura del Proyecto
```text
Sistema-de-Predicci-n-de-Deserci-n-1.0/
│
├── data/               # Datasets históricos y procesados
├── models/             # Lógica de los algoritmos (id3_classifier.py, apriori_rules.py)
├── utils/              # Scripts de preprocesamiento y limpieza de datos
├── main.py             # Archivo principal de ejecución
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación del proyecto
