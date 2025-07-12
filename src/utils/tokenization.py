from src.utils.logger import setup_logging
import logging
import re

setup_logging()
logger = logging.getLogger(__name__)

def tokenize_text(text):
    try:
        logger.info(f"Tokenizing text: {text}")
        # Normalize Arabic diacritics
        text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)
        # Segment Arabic and English
        tokens = []
        current_token = ""
        is_arabic = lambda c: '\u0600' <= c <= '\u06FF'
        is_english = lambda c: c.isalpha() and not is_arabic(c)
        for char in text:
            if is_arabic(char) or is_english(char):
                current_token += char
            else:
                if current_token:
                    tokens.append(current_token)
                tokens.append(char)
                current_token = ""
        if current_token:
            tokens.append(current_token)
        # Normalize spaces and punctuation
        tokens = [t.strip() for t in tokens if t.strip()]
        logger.info(f"Tokenized output: {tokens}")
        return tokens
    except Exception as e:
        logger.error(f"Tokenization failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_texts = [
        "I’m feeling stressed وما أقدر أتحمل",
        "أشعر بالقلق الشديد بسبب عملي",
        "الحمد لله، الأمور تحسنت"
    ]
    for text in test_texts:
        tokens = tokenize_text(text)
        print(f"Input: {text}")
        print(f"Tokens: {tokens}")
