from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from src.utils.logger import setup_logging
import logging, os
from src.utils.text_normalization import normalize_arabic_text  # Updated correct path

setup_logging()
logger = logging.getLogger(__name__)

MODEL_ID = "hatemnoaman/bert-base-arabic-finetuned-emotion"
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models/arabic_emotion_model")

# Define model label mapping
label_map = {
    "LABEL_0": "anger",
    "LABEL_1": "disgust",
    "LABEL_2": "joy",
    "LABEL_3": "sadness",
    "LABEL_4": "surprise",
    "LABEL_5": "love",
    "LABEL_6": "neutral",
    "LABEL_7": "fear"
}

def initialize_model():
    if not os.path.isdir(MODEL_DIR):
        logger.info(f"Downloading and saving Arabic emotion model to {MODEL_DIR}...")
        os.makedirs(MODEL_DIR, exist_ok=True)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)
        tokenizer.save_pretrained(MODEL_DIR)
        model.save_pretrained(MODEL_DIR)
    else:
        logger.info(f"Loading model from {MODEL_DIR}...")

    return pipeline(
        "sentiment-analysis",
        model=MODEL_DIR,
        tokenizer=MODEL_DIR,
        return_all_scores=True
    )

def analyze_emotion(text):
    logger.info("Starting emotion analysis...")
    text = normalize_arabic_text(text)
    classifier = initialize_model()
    scores = classifier(text)[0]
    best = max(scores, key=lambda x: x['score'])
    raw_label = best["label"]
    readable_label = label_map.get(raw_label, raw_label)
    score = best["score"]
    logger.info(f"Detected emotion: {readable_label} (confidence {score:.2f})")
    return readable_label, score

if __name__ == "__main__":
    test_cases = [
        "أنا حزين جدًا.",
        "أشعر بسعادة غامرة!",
        "لا بأس، الأمور تمشي.",
        "أشعر بالخوف والقلق.",
        "أنا غاضب جدًا مما حدث!",
        "هذا أمر مقزز للغاية.",
        "لقد وقعت في الحب!",
        "لم أكن أتوقع هذا أبداً!",
    ]

    print("Arabic Emotion Detection Demo")
    print("-" * 40)
    for text in test_cases:
        label, score = analyze_emotion(text)
        print(f"Input: {text}")
        print(f"Detected Emotion: {label} (Confidence: {score:.2f})")
        print("-" * 40)
