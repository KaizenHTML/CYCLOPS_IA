# 📋 Historias de Usuario y Flujo de Interacción - CYCLOPS

Este documento mapea los Requerimientos Funcionales y la secuencia operativa entre los tres actores principales del sistema: el Empleado, el Agente de Inteligencia Artificial y el Analista SOC.

---

## 1. Diagrama de Historias de Usuario

Describe la ruta de procesamiento condicional basada en el nivel de confianza arrojado por el modelo de clasificación.

💡
* **Diagrama de Historias de Usuario:** [Ver Diagrama en PDF](assets/user_stories.pdf)

---

## 2. Detalle de Historias de Usuario por Rol

### Rol: Usuario Final - Empleado
* **HU01:** Ingestar correos sospechosos sin alterar la estructura original de los encabezados.
* **HU02:** Obtener retroalimentación en tiempo real sobre la resolución o el estado de triaje de su reporte.

### Rol: Agente de Inteligencia Artificial CYCLOPS
* **HU03:** Preprocesar texto mediante tokenización, lematización y enmascaramiento de direcciones IP.
* **HU04:** Transformar variables cuantitativas usando RobustScaler para evitar la influencia de valores extremos.
* **HU05:** Calcular el score probabilístico y evaluar si supera el umbral de automatización.
* **HU06:** Ejecutar la cuarentena inmediata y notificar al remitente si la confianza es superior al noventa por ciento.
* **HU07:** Escalar el ticket a la consola humana cuando la evaluación presente ambigüedad.

### Rol: Analista de Seguridad SOC
* **HU08:** Inspeccionar incidentes priorizados según métricas de severidad.
* **HU09:** Confirmar la acción recomendada por el agente de Inteligencia Artificial.
* **HU10:** Cerrar el caso y enviar la actualización definitiva al empleado reportante.