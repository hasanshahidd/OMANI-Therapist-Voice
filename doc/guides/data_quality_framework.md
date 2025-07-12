
`markdown
<h1 align="center">📊 Data Quality Framework — OMANI‑Therapist‑Voice</h1>

---

## 📥 Introduction

The **OMANI-Therapist-Voice** project depends on a carefully curated and culturally sensitive dataset to ensure reliable emotion detection, safe interaction, and therapeutic accuracy in Omani Arabic. This framework documents how data is sourced, preprocessed, validated, and expanded — with integrated quality gates, monitoring, and GitHub upload hygiene.

---

## 📂 Data Overview

### 🧾 Primary Dataset

- **File**: `data/mental_health_phrases.csv`  
- **Use**: Core training data for the `emotion_finetuned` model  
- **Content**: Annotated Omani phrases tagged with emotions like sadness, anger, and fear  
- **Scope**: Culturally aligned but currently limited to central dialects (expansion in progress)

---

## 🧹 Quality Assurance

### 🧼 Preprocessing

| Step              | Script                                | Description                                       |
|-------------------|----------------------------------------|---------------------------------------------------|
| Normalization     | `src/utils/text_normalization.py`     | Unifies Arabic variants, removes diacritics       |
| Tokenization      | `src/utils/tokenization.py`           | Custom Arabic-aware segmenter for LLM inputs      |
| Logging & Metrics | `src/utils/logger.py`, `monitoring.py`| Logs token counts, latency, and text deltas       |

### ✅ Validation

- **Annotation Accuracy**: Reviewed by native Omani speakers  
- **Model Evaluation**: Accuracy improvements tracked in `test_emotion_agent.py`  
- **Safety Sync**: Dataset aligned with `safety_agent.py` for suicide/harm trigger words  

---

## 📊 Quality Metrics

| Metric      | Source                         | Result                          |
|-------------|--------------------------------|---------------------------------|
| Emotion Accuracy | `docs/reports/annotation_metrics.md` | +15% vs. base model            |
| Text Consistency | `pipeline.log`             | Verified via preprocessing logs |
| Coverage     | Manual Audit                  | Missing regional dialects       |

---

## 🧩 Data Pipeline Flow

1. **Input**: Audio captured → STT → `transcript`  
2. **Process**: Transcript normalized & tokenized  
3. **Usage**:
   - Passed to `emotion_agent.py` and `safety_agent.py`
   - Informs response generation via `therapy_agent.py`
4. **Output**: Emotion-tagged, culturally adapted audio or crisis alert

---

## 🧠 Monitoring & Logging

- **Tool**: `src/utils/monitoring.py`  
- **Logs**: Stage latency, token count, success/failure  
- **Visibility**: All logs written to `pipeline.log` (excluded from GitHub)  
- **UI Hook**: Displayed in Flask app via `/logs` route for debugging (optional)

---

## 📁 Project Structure (Partial)

```text
OMANI-Therapist-Voice/
├── data/
│   └── mental_health_phrases.csv
├── src/
│   ├── agents/
│   │   └── emotion/
│   │       └── emotion_agent.py
│   └── utils/
│       ├── text_normalization.py
│       ├── tokenization.py
│       └── monitoring.py
└── tests/
    └── unit/
        └── test_emotion_agent.py
````

---

## 🚫 GitHub Upload Guidelines

To protect privacy and keep the repo clean:

| Exclude File/Folder            | Reason                     |
| ------------------------------ | -------------------------- |
| `.env`                         | Contains API keys          |
| `venv/`                        | Machine-specific env       |
| `pipeline.log`                 | Regeneratable runtime logs |
| `output.wav`, `output_tts.wav` | Temp audio files           |
| `.vscode/`                     | Personal IDE settings      |
| `__pycache__` / `*.pyc`        | Python bytecode/cache      |

✅ Confirm `.gitignore` contains all above.

---

## 🛠 Challenges & Fixes

| Challenge                   | Solution                                              |
| --------------------------- | ----------------------------------------------------- |
| Dialect scarcity in dataset | Expansion plan with region-specific samples           |
| Mislabels in emotional tags | Manual audits + unit tests in `test_emotion_agent.py` |
| Model inconsistencies       | Added custom tokenization + text normalization        |

---

## ✅ Best Practices

* Use dialectal examples from real Omani therapy sessions
* Re-run validation tests after each dataset update
* Back up `mental_health_phrases.csv` with each Git commit
* Collaborate with cultural experts when labeling ambiguous phrases

---

## 🚀 Future Enhancements

* Add emotion labels for compound expressions (e.g., shame + guilt)
* Expand with child/adolescent mental health phrases
* Integrate dialect detection to route phrases to region-specific LLM prompts
* Automate cultural bias scans using `docs/guides/bias_mitigation.md`

---

## 🙏 Acknowledgments

* **Hugging Face**: Arabic BERT architecture
* **xAI**: LLM therapy generation (Groq)
* **Azure**: Voice I/O and TTS processing
* **Omani Reviewers**: Phrase validation & dialect guidance

---
## 📌 Summary

This document outlines how **OMANI-Therapist-Voice** achieves trustworthy, culturally respectful, and accurate emotion detection by managing its most critical asset — the **data**. Through normalization, annotation, and quality metrics, it lays the foundation for an emotionally intelligent and safe digital therapist.
