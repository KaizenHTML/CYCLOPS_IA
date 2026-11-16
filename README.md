# CYCLOPS SENTINEL

Plataforma inteligente y autónoma para la detección proactiva de amenazas de phishing, análisis de correos sospechosos y protección en tiempo real para usuarios finales mediante Machine Learning.

<br>

---
<br>

## Descripción del Proyecto

**CYCLOPS SENTINEL** es una solución tecnológica avanzada diseñada para mitigar el riesgo de fraude digital por ingeniería social, phishing y vectores de ataque transmitidos a través del correo electrónico. 

El sistema está concebido con un **enfoque cien por ciento centrado en el usuario final**. Permite que cualquier usuario ingrese o reporte un mensaje sospechoso en la interfaz web interactiva, activando un pipeline de inferencia en tiempo real que ejecuta limpieza de texto, anonimización de datos sensibles, extracción de métricas estructurales y acondicionamiento estadístico mediante **RobustScaler**. 

A través de un modelo supervisado de aprendizaje automático de alta precisión y explicabilidad, el sistema genera de forma autónoma e instantánea un veredicto definitivo: **Phishing Confirmado**, **Phishing Sospechoso** o **Mensaje Legítimo**, indicando el nivel de riesgo, la probabilidad matemática y una serie de recomendaciones preventivas claras para salvaguardar la seguridad del usuario sin depender de intermediarios ni de analistas externos.

<br>

---
<br>

## Integrantes del Proyecto

* **Cristian Díaz** - Ingeniero de Software e Investigador Principal
  
<br>

---
<br>

## Stack Tecnológico Principal

### Presentación e Interfaz de Usuario
* **Interfaz Web Interactiva:** HTML5 Semántico, CSS3 Moderno con arquitectura responsive y JavaScript asíncrono Fetch API
* **Estilo Visual:** Dashboard corporativo de ciberseguridad en tema oscuro, indicadores de riesgo en tiempo real y paneles de explicabilidad

### Backend y Servicios de Inferencia
* **Lenguaje:** Python 3.10+
* **Framework Web y API REST:** Flask y FastAPI
* **Servicios de Inferencia:** Arquitectura desacoplada en memoria RAM para latencias de respuesta inferiores a doscientos milisegundos

### Inteligencia Artificial y Machine Learning
* **Librería de Analítica y Modelado:** Scikit-Learn y NumPy
* **Acondicionamiento Numérico:** RobustScaler para mitigar el impacto de valores atípicos severos en conteos de enlaces y longitudes de texto
* **Módulo de Aprendizaje Supervisado:** Clasificador por Árbol de Decisión para diagnóstico transparente, determinístico y de máxima explicabilidad
* **Módulo de Aprendizaje No Supervisado:** Agrupamiento K-Means para la identificación de familias y perfiles de ataque
* **Procesamiento de Lenguaje Natural:** Pipeline NLP para normalización léxica, detección de términos de urgencia coercitiva y enmascaramiento de direcciones IP y correos

### Almacenamiento, Persistencia y Auditoría
* **Base de Datos Relacional:** PostgreSQL
* **Capa de Abstracción de Datos:** SQLAlchemy para el registro del historial de consultas, trazabilidad de análisis y auditoría del sistema
  
<br>

---
<br>

## Arquitectura del Pipeline y Funcionamiento del Sistema

El flujo de procesamiento del sistema se estructura en dos fases complementarias:

### 1. Fase de Entrenamiento y Acondicionamiento de Datos
1. **Ingesta Heterogénea:** Consolidación de tres conjuntos de datos representativos: correos corporativos legítimos, correos confirmados de phishing y mensajes de texto spam.
2. **Anonimización y Limpieza:** Enmascaramiento de direcciones IP públicas y cuentas de correo para proteger la privacidad de la información.
3. **Ingeniería de Características:** Extracción de variables cuantificables clave: conteo de caracteres, total de palabras, conteo de hipervínculos, presencia de enlaces, indicador de direcciones IP, puntaje de urgencia heurístico y densidades sintéticas.
4. **Escalado Robusto:** Acondicionamiento de variables numéricas utilizando la mediana y el rango intercuartílico mediante RobustScaler, previniendo la fuga de datos mediante una estricta partición ochenta a veinte entre entrenamiento y prueba.
5. **Modelado Híbrido:** Entrenamiento del clasificador supervisado y estructuración de centroides con K-Means para perfilamiento de amenazas.
6. **Serialización:** Congelamiento de transformadores y modelos en disco para consumo en producción.

### 2. Fase de Inferencia y Diagnóstico en Tiempo Real
Cuando un usuario consulta un correo sospechoso en la plataforma, el sistema ejecuta una secuencia lógica estructurada en cuatro niveles:
* **Nivel 1 - Ingesta y Preprocesamiento NLP:** Normalización del mensaje ingresado y extracción dinámica de métricas cuantitativas.
* **Nivel 2 - Extracción de Métricas y Escalado Robusto:** Transformación del vector numérico empleando el artefacto preentrenado de RobustScaler para aislar valores atípicos.
* **Nivel 3 - Inferencia Probabilística:** Evaluación matemática de patrones sospechosos mediante el modelo clasificador.
* **Nivel 4 - Diagnóstico Directo y Recomendaciones:** Entrega del veredicto final categorizado por nivel de riesgo, junto con recomendaciones preventivas inmediatas para el usuario.
  
<br>

---
<br>

## Documentación del Sistema y Entregables

Toda la definición arquitectónica, estratégica y normativa del proyecto se encuentra centralizada en el directorio documental:

* **Plan de Auditoría Técnica Oficial:** [Ver Plan de Auditoría Markdown](mi-framework-ia/docs/audit_plan.md) | [Descargar Documento Word APA 7](Plan_de_Auditoria_CYCLOPS_APA7.docx)
  * Matriz con diez controles de calidad de datos, prevención de data leakage, rendimiento de modelos y latencia.
* **Documento de Requerimientos de Producto:** [Ver PRD](mi-framework-ia/docs/prd.md)
  * Definición funcional y no funcional del sistema centrado en el usuario final.
* **Arquitectura General del Sistema:** [Ver Arquitectura](mi-framework-ia/docs/architecture.md)
  * Especificación de componentes, clases y persistencia relacional.
* **Historias de Usuario:** [Ver Historias de Usuario](mi-framework-ia/docs/user_stories.md)
  * Flujos de interacción del usuario con el motor de inteligencia artificial.
* **Prompts de Contexto Estratégico:** [Ver Prompts](mi-framework-ia/docs/prompts.md)
  * Directrices de gobernanza técnica y reglas operativas del framework.
* **Diagramas Técnicos en PDF:** [Explorar Carpeta de Assets](mi-framework-ia/docs/assets/)
  * Diagrama de clases, diagrama de componentes, modelo entidad-relación e historias de usuario.
    
<br>

---
<br>

## Estructura del Repositorio

```text
frameworkIa/
├── app.py                                   # Servidor web Flask y API REST de inferencia
├── cyclops_engine.py                        # Motor de IA: extracción, RobustScaler y clasificación
├── verify_no_parens.py                      # Auditoría estática de sintaxis y restricciones de estilo
├── README.md                                # Documentación general del proyecto
├── Plan_de_Auditoria_CYCLOPS_APA7.docx       # Plan de auditoría técnica en formato Word APA 7
├── templates/
│   └── index.html                           # Interfaz interactiva de inferencia e historial
├── static/
│   ├── css/style.css                        # Estilos visuales del dashboard corporativo
│   └── js/app.js                            # Lógica cliente para consumo asíncrono de la API
└── mi-framework-ia/
    ├── .gitignore                           # Exclusiones de control de versiones
    ├── config/
    │   └── agents.yaml                      # Configuración declarativa del agente
    ├── agents/
    │   └── phishing_detector_agent/
    │       ├── agent.py                     # Agente autónomo de detección de amenazas
    │       └── manifest.yaml                # Manifiesto y contratos del agente
    ├── skills/
    │   ├── nlp_cleaner/
    │   │   ├── skill.py                     # Skill de normalización léxica y limpieza NLP
    │   │   └── manifest.yaml                # Manifiesto de la skill NLP
    │   └── robust_scaler_tool/
    │       ├── skill.py                     # Skill de acondicionamiento con RobustScaler
    │       └── manifest.yaml                # Manifiesto de la skill de escalado
    ├── core/
    │   ├── agent_base/                      # Contratos base y registro central de agentes
    │   └── skill_base/                      # Contratos base y registro central de skills
    └── docs/
        ├── audit_plan.md                    # Plan de auditoría técnica en Markdown
        ├── prd.md                           # Documento de requerimientos de producto
        ├── architecture.md                  # Especificación técnica de arquitectura
        ├── user_stories.md                  # Historias de usuario del sistema
        ├── prompts.md                       # Prompts de contexto para los agentes
        └── assets/                          # Diagramas técnicos en formato PDF
```

<br>

---
<br>

## Puesta en Marcha y Ejecución Local

Para ejecutar la plataforma localmente y realizar pruebas interactivas de detección de phishing en tiempo real:

1. **Clonar o situarse en el directorio del proyecto:**
   ```bash
   cd frameworkIa
   ```

2. **Crear y activar un entorno virtual de Python:**
   ```bash
   python -m venv .venv
   # En Windows:
   .venv\Scripts\activate
   # En Linux o macOS:
   source .venv/bin/activate
   ```

3. **Instalar dependencias necesarias:**
   ```bash
   pip install flask scikit-learn numpy python-docx
   ```

4. **Ejecutar el servidor de la aplicación:**
   ```bash
   python app.py
   ```

5. **Acceder a la interfaz web:**
   Abrir un navegador e ingresar a la dirección local:
   ```
   http://127.0.0.1:5000
   ```
   
<br>

---
<br>

## Verificación de Calidad y Restricciones de Formato

El repositorio cuenta con una herramienta de auditoría automatizada para verificar el cumplimiento estricto de las directrices de estilo y la ausencia total de caracteres no permitidos en el código fuente y las interfaces:

```bash
python verify_no_parens.py
```
* **Estado:** Cien por ciento de cumplimiento verificado.
