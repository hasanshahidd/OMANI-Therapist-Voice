# src/utils/cultural_embedding.py
from src.utils.logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

class CulturalEmbeddings:
    def __init__(self):
        self.embeddings = {
            "ar": {
                "sadness": "الصبر مفتاح الفرج، هل تريد مشاركة ما يزعجك؟",
                "anxiety": "وفقك الله، هل يمكنني مساعدتك بالهدوء؟",
                "default": "أنا هنا بدعم عماني، كيف أساعدك؟"
            },
            "en": {
                "sadness": "Patience is key in our culture, want to share more?",
                "anxiety": "May peace guide you, can I help you calm down?",
                "default": "I’m here with Omani warmth, how can I assist?"
            }
        }

    def get_prompt(self, emotion, lang="ar"):
        prompt = self.embeddings.get(lang, self.embeddings["ar"]).get(emotion, self.embeddings[lang]["default"])
        logger.info(f"Retrieved cultural prompt for {emotion} in {lang}: {prompt}")
        return prompt

cultural_embeddings = CulturalEmbeddings()
