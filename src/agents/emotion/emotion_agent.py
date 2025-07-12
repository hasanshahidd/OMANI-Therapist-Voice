from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from src.utils.logger import setup_logging
from src.utils.tokenization import tokenize_text  # Added for custom tokenization
from src.utils.text_normalization import normalize_arabic_text
import logging, os

setup_logging()
logger = logging.getLogger(__name__)

# Define model paths
BASE_MODEL_ID = "hatemnoaman/bert-base-arabic-finetuned-emotion"
BASE_MODEL_DIR = os.path.join(os.path.dirname(__file__), "models/arabic_emotion_model")
FINETUNED_MODEL_DIR = os.path.join(os.path.dirname(__file__), "models/emotion_finetuned")

# Define model label mapping (assuming consistent with both models)
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

def initialize_models():
    models = {}
    
    # Initialize base model
    if not os.path.isdir(BASE_MODEL_DIR):
        logger.info(f"Downloading and saving base Arabic emotion model to {BASE_MODEL_DIR}...")
        os.makedirs(BASE_MODEL_DIR, exist_ok=True)
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID)
        model = AutoModelForSequenceClassification.from_pretrained(BASE_MODEL_ID)
        tokenizer.save_pretrained(BASE_MODEL_DIR)
        model.save_pretrained(BASE_MODEL_DIR)
    logger.info(f"Loading base model from {BASE_MODEL_DIR}...")
    models['base'] = pipeline(
        "sentiment-analysis",
        model=BASE_MODEL_DIR,
        tokenizer=BASE_MODEL_DIR,
        return_all_scores=True
    )

    # Initialize fine-tuned Omani model
    if os.path.isdir(FINETUNED_MODEL_DIR):
        logger.info(f"Loading fine-tuned Omani model from {FINETUNED_MODEL_DIR}...")
        models['finetuned'] = pipeline(
            "sentiment-analysis",
            model=FINETUNED_MODEL_DIR,
            tokenizer=FINETUNED_MODEL_DIR,
            return_all_scores=True
        )
    else:
        logger.warning(f"Fine-tuned model not found at {FINETUNED_MODEL_DIR}, using base model only.")

    return models

def analyze_intent(text):
    logger.info("Starting emotion analysis...")
    # Normalize text first
    text = normalize_arabic_text(text)
    # Tokenize text using custom tokenizer
    tokens = tokenize_text(text)
    # Join tokens back into a string for model compatibility (since pipeline expects string input)
    processed_text = " ".join(tokens)
    
    models = initialize_models()
    
    best_emotion = None
    best_score = 0.0
    best_model = None

    for model_name, classifier in models.items():
        scores = classifier(processed_text)[0]
        best = max(scores, key=lambda x: x['score'])
        raw_label = best["label"]
        readable_label = label_map.get(raw_label, raw_label)
        score = best["score"]
        logger.info(f"{model_name} model detected emotion: {readable_label} (confidence {score:.2f})")
        
        if score > best_score:
            best_score = score
            best_emotion = readable_label
            best_model = model_name

    logger.info(f"Selected {best_model} model with emotion: {best_emotion} (confidence {best_score:.2f})")
    return best_emotion, best_score

if __name__ == "__main__":
    test_cases = [
        "أحتاج إلى المساعدة، وأريد أن أعيش معك",
        "أشعر بالقلق الشديد بسبب عملي",
        "أواجه مشاكل مع أهلي بسبب توقعاتهم",
        "العمل يرهقني نفسيًا",
        "أشعر أنني لا أستطيع الاستمرار هكذا",
        "I’m feeling stressed وما أقدر أتحمل"
    ]

    print("Emotion Detection Demo")
    print("-" * 40)
    for text in test_cases: 
        label, score = analyze_intent(text)
        print(f"Input: {text}")
        print(f"Detected Emotion: {label} (Confidence: {score:.2f})")
        print("-" * 40)
