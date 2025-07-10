import re
from src.utils.logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

def normalize_arabic_text(text):
    try:
        logger.info("Normalizing Arabic text...")
        # Remove diacritics
        text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)
        # Normalize spaces
        text = re.sub(r'\s+', ' ', text).strip()
        logger.info(f"Normalized text: {text}")
        return text
    except Exception as e:
        logger.error(f"Normalization failed: {str(e)}")
        raise
