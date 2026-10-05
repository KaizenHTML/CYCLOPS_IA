from core.skill_base.base_skill import BaseSkill
import joblib

class RobustScalerSkill(BaseSkill):
    def __init__(self, scaler_path: str):
        self.scaler = joblib.load(scaler_path)

    def execute(self, metrics: dict) -> list:
        features = [[
            metrics["char_count"],
            metrics["word_count"],
            metrics["url_count"]
        ]]
        scaled_features = self.scaler.transform(features)
        return scaled_features.tolist()