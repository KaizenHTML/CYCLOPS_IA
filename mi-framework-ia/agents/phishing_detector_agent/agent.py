from core.agent_base.base_agent import BaseAgent

class PhishingDetectorAgent(BaseAgent):
    def __init__(self, nlp_skill, scaler_skill, model):
        self.nlp_skill = nlp_skill
        self.scaler_skill = scaler_skill
        self.model = model

    def evaluate_email(self, raw_text: str):
        cleaned_data = self.nlp_skill.execute(raw_text)
        scaled_features = self.scaler_skill.execute(cleaned_data["raw_metrics"])
        
        confidence = self.model.predict_proba(scaled_features)
        
        if confidence >= 0.90:
            action = "AUTO_MITIGATED_QUARANTINE"
        elif 0.50 <= confidence < 0.90:
            action = "ROUTED_TO_SOC_CONSOLE"
        else:
            action = "MARKED_AS_SAFE"
            
        return {
            "confidence_score": confidence,
            "classification": "PHISHING" if confidence >= 0.50 else "LEGITIMATE",
            "action_taken": action
        }