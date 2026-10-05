# Product Requirements Document - CYCLOPS

Este documento especifica la visión, el alcance, las reglas de negocio, los requerimientos funcionales y no funcionales, así como los casos de uso principales para la plataforma de ciberseguridad **CYCLOPS**.

---

## 1. Visión y Alcance del Producto

### Visión
Ofrecer una plataforma Enterprise B2B de detección de phishing y respuesta a incidentes que reduzca drásticamente los tiempos de exposición ante amenazas por correo electrónico, automatizando la mitigación de casos de alta certeza y optimizando la carga operativa del equipo SOC.

### Alcance
El sistema comprende la ingesta de correos sospechosos reportados por empleados, la extracción y limpieza de datos mediante NLP, la transformación de métricas cuantitativas con RobustScaler, la clasificación por modelo de Machine Learning en Scikit-Learn y la orquestación en FastAPI con base de datos PostgreSQL. La plataforma maneja una respuesta de dos niveles de confianza y expone una consola de triaje priorizada para el Analista SOC.

---

## 2. Casos de Uso Principales

### CU01: Reporte de Correo Sospechoso por Empleado
* **Actor Principal:** Empleado - Usuario Final.
* **Precondición:** El empleado recibe un correo sospechoso en su cliente de correo.
* **Flujo Principal:**
  1. El empleado ingresa el texto o cuerpo del mensaje en la interfaz de usuario.
  2. El sistema recibe el reporte, genera un identificador de incidente y responde de forma asíncrona en milisegundos.
  3. El sistema notifica al usuario el resultado de la evaluación inmediata o el estado de revisión.

### CU02: Evaluación y Mitigación Automática por Agente de IA
* **Actor Principal:** Agente de Inteligencia Artificial CYCLOPS.
* **Precondición:** Incidente registrado en estado pendiente de análisis.
* **Flujo Principal:**
  1. El agente invoca la skill de limpieza NLP para anonimizar texto y extraer métricas numéricas.
  2. El agente invoca la skill de escalado para transformar variables numéricas con el modelo entrenado de RobustScaler.
  3. El agente evalúa la probabilidad de amenaza devuelta por Scikit-Learn.
  4. Si la confianza es mayor o igual al noventa por ciento, el sistema aplica cuarentena automática, marca el incidente como automitigado y notifica al empleado.
  5. Si la confianza está entre cincuenta y ochenta y nueve por ciento, el sistema enruta el ticket a la consola del Analista SOC.

### CU03: Triaje Manual y Resolución por Analista SOC
* **Actor Principal:** Analista de Seguridad SOC.
* **Precondición:** Existencia de incidentes en estado de revisión manual por ambigüedad.
* **Flujo Principal:**
  1. El analista visualiza la lista de alertas priorizadas en su consola React.
  2. Inspecciona el resumen técnico, las métricas escaladas y la recomendación del modelo.
  3. Selecciona la acción definitiva con un clic confirmando phishing o falsa alarma.
  4. El sistema actualiza el registro en PostgreSQL y envía la notificación final al empleado reportante.

---

## 3. Requerimientos Funcionales

* **RF01 - Ingesta de Reportes:** La API debe permitir la recepción de solicitudes HTTP POST con el texto del correo y los datos del remitente.
* **RF02 - Preprocesamiento NLP:** El backend debe limpiar el texto eliminando caracteres innecesarios y anonimizando direcciones IP.
* **RF03 - Escalado Robusto:** Las métricas de conteo de caracteres, palabras y URLs deben ser transformadas utilizando el modelo preentrenado de RobustScaler para evitar distorsión por valores extremos.
* **RF04 - Clasificación de Riesgo:** El sistema debe calcular la probabilidad probabilística de phishing utilizando un modelo supervisado de Scikit-Learn.
* **RF05 - Motor de Decisión Híbrido:** El sistema debe bifurcar la respuesta operativamente: automatización inmediata si la confianza es igual o superior al noventa por ciento, y derivación a consola SOC para valores entre cincuenta y ochenta y nueve por ciento.
* **RF06 - Persistencia Relacional:** PostgreSQL debe registrar el historial completo de cada incidente, sus metadatos extraídos, la evaluación del modelo y la acción de mitigación aplicada.
* **RF07 - Consola de Triaje:** La interfaz debe proveer al analista SOC un panel para filtrar, ordenar y resolver incidentes pendientes.

---

## 4. Requerimientos No Funcionales

* **RNF01 - Rendimiento y Latencia:** La API de ingesta en FastAPI debe responder la confirmación de recepción en menos de doscientos milisegundos.
* **RNF02 - Escalabilidad:** El backend debe utilizar procesamiento asíncrono para manejar ráfagas de reportes sin bloquear el hilo principal.
* **RNF03 - Seguridad por Diseño:** No se deben almacenar datos sensibles sin anonimizar, y todas las conexiones a PostgreSQL deben manejar autenticación segura.
* **RNF04 - Mantenibilidad y Clean Architecture:** El código debe estructurarse respetando la separación en capas, desacoplando la lógica de agente, skills, persistencia e interfaces.
* **RNF05 - Disponibilidad de la Interfaz:** La consola en React con Tailwind CSS debe ser completamente adaptativa y responder a estándares de diseño oscuro optimizado para operaciones de SOC.