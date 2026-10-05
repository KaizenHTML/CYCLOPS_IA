from core.skill_base.base_skill import BaseSkill

class NLPCleanerSkill(BaseSkill):
    def execute(self, text: str) -> dict:
        char_count = len(text)
        word_count = len(text.split())
        url_count = text.count("http://") + text.count("https://")
        
        return {
            "cleaned_text": text.lower().strip(),
            "raw_metrics": {
                "char_count": char_count,
                "word_count": word_count,
                "url_count": url_count
            }
        }