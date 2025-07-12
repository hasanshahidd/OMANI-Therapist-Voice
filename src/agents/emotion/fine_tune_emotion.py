from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from src.utils.logger import setup_logging
import logging
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
import os
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

setup_logging()
logger = logging.getLogger(__name__)

MODEL_DIR = r"C:\Users\Admin\Desktop\OMANI-Therapist-Voice\src\agents\emotion\models\arabic_emotion_model"   #put you data path
FINETUNED_DIR = r"C:\Users\Admin\Desktop\OMANI-Therapist-Voice\src\agents\emotion\models\emotion_finetuned"   #put you data path
DATA_PATH = r"C:\Users\Admin\Desktop\OMANI-Therapist-Voice\data\mental_health_phrases_300.xlsx"   #put you data path


def load_data():
    try:
        logger.info("Loading dataset...")
        if not os.path.exists(DATA_PATH):
            logger.error(f"Dataset file not found: {DATA_PATH}")
            raise FileNotFoundError(f"Dataset file not found: {DATA_PATH}")
        
        df = pd.read_excel(DATA_PATH, engine="openpyxl")
        
        if df.empty or "text" not in df.columns or "emotion" not in df.columns:
            logger.error("Dataset is empty or missing required columns: 'text', 'emotion'")
            raise ValueError("Dataset is empty or missing required columns: 'text', 'emotion'")
        
        return df["text"].tolist(), df["emotion"].tolist()
    except Exception as e:
        logger.error(f"Data loading failed: {str(e)}")
        raise

def evaluate_model(trainer, val_dataset, label_map):
    logger.info("Evaluating the model...")
    preds_output = trainer.predict(val_dataset)
    preds = np.argmax(preds_output.predictions, axis=1)
    true_labels = preds_output.label_ids
    inv_label_map = {v: k for k, v in label_map.items()}
    pred_labels = [inv_label_map[p] if p in inv_label_map else "unknown" for p in preds]
    true_labels_text = [inv_label_map[t] for t in true_labels]
    print("\nClassification Report:")
    print(classification_report(true_labels_text, pred_labels))
    print("Confusion Matrix:")
    print(confusion_matrix(true_labels_text, pred_labels))

def fine_tune_model():
    try:
        logger.info("Starting fine-tuning...")
        texts, labels = load_data()
        label_map = {
    "anger": 0,
    "disgust": 1,
    "joy": 2,
    "sadness": 3,
    "surprise": 4,
    "love": 5,
    "neutral": 6,
    "fear": 7
}

        labels = [label_map[label] for label in labels]
        train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=0.2)

        tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR, num_labels=8)

        train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
        val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=128)

        class Dataset(torch.utils.data.Dataset):
            def __init__(self, encodings, labels):
                self.encodings = encodings
                self.labels = labels
            def __getitem__(self, idx):
                item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
                item["labels"] = torch.tensor(self.labels[idx])
                return item
            def __len__(self):
                return len(self.labels)

        train_dataset = Dataset(train_encodings, train_labels)
        val_dataset = Dataset(val_encodings, val_labels)

        training_args = TrainingArguments(
            output_dir=FINETUNED_DIR,
            num_train_epochs=3,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            warmup_steps=10,
            weight_decay=0.01,
            logging_dir="logs",
            logging_steps=10,
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
        )

        trainer.train()
        evaluate_model(trainer, val_dataset, label_map)
        model.save_pretrained(FINETUNED_DIR)
        tokenizer.save_pretrained(FINETUNED_DIR)
        logger.info(f"Fine-tuned model saved to {FINETUNED_DIR}")
    except Exception as e:
        logger.error(f"Fine-tuning failed: {str(e)}")
        raise

if __name__ == "__main__":
    fine_tune_model()
