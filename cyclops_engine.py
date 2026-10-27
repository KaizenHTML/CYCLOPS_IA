from typing import Any
import re
import uuid
import datetime
import numpy as np
from sklearn.preprocessing import RobustScaler
from sklearn.linear_model import LogisticRegression

class EmailMetadata:
    def __init__(self, raw_text):
        self.id = str(uuid.uuid4())[:8]
        self.raw_text = raw_text
        self.char_count = 0
        self.word_count = 0
        self.url_count = 0
        self.has_url = 0
        self.urgency_score = 0.0
        self.scaled_urgency_score = 0.0
        self.url_density = 0.0
        self.urgency_density = 0.0
        self.is_threat = False
        self.anonymized_sender = "usuario.corporativo@empresa.com"
        self.extract_features()

    def extract_features(self):
        text = self.raw_text or ""
        self.char_count = len(text)
        words = text.split()
        self.word_count = len(words)
        
        urls = re.findall(r"https?://\S+|www\.\S+|\b[A-Za-z0-9.-]+\.[a-z]{2,}\b/\S*", text, re.IGNORECASE)
        self.url_count = len(urls)
        self.has_url = 1 if self.url_count > 0 else 0

        urgency_terms = [
            "urgente", "urgencia", "inmediato", "inmediatamente", "suspension",
            "suspendida", "suspender", "bloqueada", "bloqueo", "cuenta", "banco",
            "bancaria", "seguridad", "verificar", "verificacion", "actualizar",
            "credenciales", "clave", "contraseña", "password", "24 horas", "48 horas",
            "expira", "vencimiento", "multa", "penalizacion", "confirmar",
            "acceso", "restringido", "alerta", "critica", "haga clic", "clic aqui"
        ]
        
        text_lower = text.lower()
        matched_score = 0.0
        for term in urgency_terms:
            if term in text_lower:
                matched_score += 1.5

        if self.url_count > 0 and matched_score > 0:
            matched_score += 2.0

        self.urgency_score = min(round(matched_score, 2), 10.0)

        effective_words = max(self.word_count, 1)
        self.url_density = round((self.url_count / effective_words) * 100.0, 2)
        self.urgency_density = round((self.urgency_score / effective_words) * 100.0, 2)

    def to_dict(self):
        return {
            "id": self.id,
            "char_count": int(self.char_count),
            "word_count": int(self.word_count),
            "url_count": int(self.url_count),
            "has_url": int(self.has_url),
            "urgency_score": float(self.urgency_score),
            "scaled_urgency_score": float(self.scaled_urgency_score),
            "url_density": float(self.url_density),
            "urgency_density": float(self.urgency_density),
            "is_threat": bool(self.is_threat),
            "anonymized_sender": self.anonymized_sender
        }

class RobustScalerService:
    def __init__(self):
        self.model_path = "models/robust_scaler.joblib"
        self.scaler = RobustScaler()
        baseline_samples = np.array([
            [80.0, 15.0, 0.0, 0.0, 0.0, 0.0],
            [150.0, 25.0, 0.0, 0.5, 0.0, 1.2],
            [220.0, 35.0, 0.0, 0.0, 0.0, 0.0],
            [350.0, 50.0, 1.0, 1.0, 1.5, 2.0],
            [450.0, 65.0, 0.0, 0.0, 0.0, 0.0],
            [280.0, 42.0, 2.0, 6.0, 4.5, 12.0],
            [190.0, 30.0, 1.0, 8.5, 3.2, 22.0],
            [520.0, 75.0, 3.0, 9.0, 3.8, 11.5]
        ])
        self.scaler.fit(baseline_samples)

    def transform(self, features_list):
        arr = np.array([features_list], dtype=float)
        scaled = self.scaler.transform(arr)
        return scaled[0].tolist()

class AIClassifierService:
    def __init__(self, scaler_service):
        self.model_path = "models/scikit_classifier.joblib"
        self.confidence_threshold = 0.90
        self.scaler_service = scaler_service
        self.classifier = LogisticRegression(random_state=42)
        train_x = np.array([
            [60.0, 10.0, 0.0, 0.0, 0.0, 0.0],
            [120.0, 22.0, 0.0, 0.0, 0.0, 0.0],
            [260.0, 45.0, 0.0, 0.5, 0.0, 1.0],
            [380.0, 60.0, 0.0, 1.0, 0.0, 1.4],
            [140.0, 24.0, 1.0, 4.0, 4.1, 15.0],
            [210.0, 32.0, 2.0, 7.5, 5.8, 20.0],
            [290.0, 40.0, 2.0, 9.0, 4.7, 18.5],
            [180.0, 28.0, 1.0, 8.0, 3.5, 24.0],
            [320.0, 48.0, 3.0, 9.5, 6.0, 17.5]
        ])
        train_y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1])
        train_scaled = self.scaler_service.scaler.transform(train_x)
        self.classifier.fit(train_scaled, train_y)

    def predict(self, metadata):
        raw_vector = [
            float(metadata.char_count),
            float(metadata.word_count),
            float(metadata.url_count),
            float(metadata.urgency_score),
            float(metadata.url_density),
            float(metadata.urgency_density)
        ]
        
        scaled_vector = self.scaler_service.transform(raw_vector)
        metadata.scaled_urgency_score = round(scaled_vector[3], 3)
        
        prob_phishing = self.classifier.predict_proba([scaled_vector])[0][1]

        if metadata.url_count > 0 and metadata.urgency_score >= 5.0:
            prob_phishing = max(prob_phishing, 0.935)
        elif metadata.url_count > 0 and metadata.urgency_score >= 2.0:
            prob_phishing = max(prob_phishing, 0.685)
        elif metadata.url_count == 0 and metadata.urgency_score <= 1.5:
            prob_phishing = min(prob_phishing, 0.125)

        confidence_pct = round(prob_phishing * 100.0, 1)

        if prob_phishing >= 0.90:
            classification = "PHISHING CONFIRMADO"
            risk_level = "CRITICO"
            action = "AUTO_MITIGATED_QUARANTINE"
            metadata.is_threat = True
            action_label = "Cuarentena Automatica Inmediata"
            summary = "Amenaza de phishing detectada con certeza superior al 90%. El mensaje contiene hipervinculos y multiples inductores de urgencia coercitiva. El sistema activo la cuarentena y aislamiento sin intervencion del analista."
        elif prob_phishing >= 0.50:
            classification = "PHISHING SOSPECHOSO"
            risk_level = "MEDIO"
            action = "ROUTED_TO_SOC_CONSOLE"
            metadata.is_threat = True
            action_label = "Derivacion a Consola de Triaje SOC"
            summary = "Puntaje de riesgo intermedio entre 50% y 89%. Presenta indicios de riesgo que ameritan analisis forense L2 en la consola de triaje para confirmacion humana."
        else:
            classification = "LEGITIMO"
            risk_level = "BAJO"
            action = "MARKED_AS_SAFE"
            metadata.is_threat = False
            action_label = "Marcado como Seguro"
            summary = "Mensaje sin presencia significativa de patrones maliciosos ni enlaces de riesgo. Clasificado como legitimo y seguro para el usuario corporativo."

        decision_levels = [
            {
                "level": "Nivel 1 - Ingesta y Preprocesamiento NLP",
                "status": "Completado",
                "details": f"Texto normalizado. Conteo de {metadata.char_count} caracteres, {metadata.word_count} palabras, {metadata.url_count} enlaces detectados y {metadata.urgency_score} puntos de urgencia identificados."
            },
            {
                "level": "Nivel 2 - Extracción de Métricas y Escalado Robusto",
                "status": "Completado",
                "details": f"Métricas transformadas con RobustScaler para aislar valores atipicos. Densidad de enlaces {metadata.url_density}%, densidad de urgencia {metadata.urgency_density}%, score de urgencia escalado {metadata.scaled_urgency_score}."
            },
            {
                "level": "Nivel 3 - Inferencia Probabilística",
                "status": "Completado",
                "details": f"Evaluacion mediante clasificador Scikit-Learn. Probabilidad calculada de amenaza situada en {confidence_pct}%."
            },
            {
                "level": "Nivel 4 - Bifurcacion y Reglas de Decision",
                "status": "Completado",
                "details": f"Umbral evaluado. Resultado asignado a la via operacional {action_label}. Nivel de riesgo catalogado como {risk_level}."
            }
        ]

        return {
            "confidence_score": float(confidence_pct),
            "classification": classification,
            "risk_level": risk_level,
            "action_taken": action,
            "action_label": action_label,
            "summary": summary,
            "decision_levels": decision_levels,
            "scaled_vector": [float(round(v, 3)) for v in scaled_vector],
            "is_high_confidence": bool(prob_phishing >= 0.90)
        }

class Incident:
    metadata: Any = None
    evaluation: Any = None
    mitigation: Any = None

    def __init__(self, raw_text, reporter_id="emp.usr.001", metadata: Any = None, evaluation: Any = None):
        self.id = "INC-" + str(uuid.uuid4())[:6].upper()
        self.reporter_id = reporter_id
        self.raw_text = raw_text
        self.status = "PENDING_ANALYSIS"
        self.alert_level = "BAJO"
        self.reported_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.metadata = metadata
        self.evaluation = evaluation
        self.mitigation = None

    def set_metadata(self, metadata: Any):
        self.metadata = metadata

    def set_evaluation(self, evaluation: Any):
        self.evaluation = evaluation

    def update_status(self, new_status, action_type=None, executed_by="CYCLOPS_AI_AGENT"):
        self.status = new_status
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if action_type:
            self.mitigation = {
                "id": "MIT-" + str(uuid.uuid4())[:6].upper(),
                "action_type": action_type,
                "executed_by": executed_by,
                "executed_at": now_str
            }

    def to_dict(self):
        return {
            "id": self.id,
            "reporter_id": self.reporter_id,
            "raw_text": self.raw_text,
            "status": self.status,
            "alert_level": self.alert_level,
            "reported_at": self.reported_at,
            "metadata": self.metadata.to_dict() if self.metadata else None,
            "evaluation": self.evaluation,
            "mitigation": self.mitigation
        }

class SOCAnalystService:
    def __init__(self):
        self.incidents = []

    def add_incident(self, incident):
        self.incidents.insert(0, incident)

    def get_pending_incidents(self):
        return [inc.to_dict() for inc in self.incidents if inc.status in ["PENDING_SOC_REVIEW", "PENDING_ANALYSIS"]]

    def get_all_incidents(self):
        return [inc.to_dict() for inc in self.incidents]

    def resolve_incident(self, incident_id, action, analyst_name="Analista SOC Tier 2"):
        for inc in self.incidents:
            if inc.id == incident_id:
                if action == "CONFIRMED_THREAT":
                    inc.update_status("RESOLVED_QUARANTINE", "ISOLATE_NETWORK_HOST", analyst_name)
                    inc.alert_level = "CRITICO"
                else:
                    inc.update_status("RESOLVED_FALSE_POSITIVE", "RESTORE_MESSAGE_INBOX", analyst_name)
                    inc.alert_level = "BAJO"
                return inc.to_dict()
        return None
