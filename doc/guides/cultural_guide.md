# 🌍 Cultural Guide — OMANI‑Therapist‑Voice

## 📘 Introduction
OMANI‑Therapist‑Voice is a culturally-aware mental health chatbot built specifically for Omani Arabic speakers. This guide documents how linguistic, religious, and emotional nuances from Omani society have been embedded into the application to ensure psychological safety, relatability, and therapeutic effectiveness.

The project’s goal is to bridge the gap between modern AI therapy and Omani cultural expectations, using Islamic values, dialect-specific language processing, and safety-driven logic.

---

## 🕌 Cultural Context

Mental health tools must resonate with local beliefs, language, and norms. In Oman, culture is deeply rooted in Islamic principles, Arabic traditions, and strong community ethics. To respect and reflect this:

- Responses are emotionally aligned with Omani values.
- Islamic idioms and cultural references are prioritized.
- Crisis detection is handled with social and religious sensitivity.

Example:  
> _"الصبر مفتاح الفرج"_ ("Patience is the key to relief")

This reflects both a cognitive-behavioral and Islamic therapeutic approach.

---

## 🧠 Key Cultural Features

### 🗣️ Linguistic Nuance
- **Dialect**: Recognizes Omani Arabic, distinct from Modern Standard Arabic (MSA).
- **Preprocessing**: Normalization via `src/utils/text_normalization.py`.
- **Custom Tokenization**: Future-ready via `src/utils/tokenization.py` to handle Omani idioms, spelling variants, and diacritics.

### 🕌 Islamic Values
- Embeds positive religious phrases.
- Avoids content that contradicts conservative values.
- Reinforces hope, resilience, and faith.

### 🫂 Emotional Intelligence
- Fine-tuned emotion model (`models/emotion_finetuned/`) includes phrases derived from Omani user scenarios.
- Culturally appropriate emotional labels (e.g., grief, shame, guilt) are considered.

---

## 🛠 Implementation Details

### 📜 Cultural Embeddings
- **File**: `src/utils/cultural_embeddings.py`
- **Purpose**: Injects localized therapy examples like _"أنا هنا بدعم عماني"_ ("I'm here with Omani support").
- **Integration**: Used in `therapy_agent.py` to generate LLM-guided CBT responses.

### 😔 Emotion Detection
- **File**: `src/agents/emotion/emotion_agent.py`
- **Models**:
  - Base: `models/arabic_emotion_model/`
  - Fine-Tuned: `models/emotion_finetuned/`
- **Training Data**: `data/mental_health_phrases.csv`
- **Tokenization**: Future pipeline with dialect-specific token handling.
- **Validation**: `tests/unit/test_emotion_agent.py`

### 🚨 Safety Alerts
- **Files**:
  - `src/agents/safety/safety_agent.py`
  - `src/ui/app.py`
  - `src/ui/templates/index.html`
- **Logic**: Halts response if suicidal/self-harm patterns detected.
- **Cultural Sensitivity**: Returns crisis-safe message and local support referral.
- **Monitoring**: Integrated into `monitoring.py` for audit logs.

### 💬 Therapy Generation
- **File**: `src/agents/therapy/therapy_agent.py`
- **LLM**: Groq with cultural reinforcement.
- **Fallback**: Skips response when safety alert triggers.
- **Validation**: Reviewed for cultural fit before logging output.

---

## 🧪 User Journey

- **Access**: Available at `http://127.0.0.1:5000`
- **Language Toggle**: `lang=ar` activates Omani Arabic responses.
- **Voice Flow**:
  1. Record → STT
  2. Analyze → Emotion/Safety
  3. Respond → Cultural CBT or Alert
  4. TTS → WAV Output

---
---

## 🚫 GitHub Upload Guidelines

To protect privacy and keep the repo clean:

| Exclude File/Folder      | Reason                          |
|--------------------------|----------------------------------|
| `.env`                   | Contains API keys               |
| `venv/`                  | Machine-specific env            |
| `pipeline.log`           | Regeneratable runtime logs      |
| `output.wav`, `output_tts.wav` | Temp audio files          |
| `.vscode/`               | Personal IDE settings           |
| `__pycache__` / `*.pyc`  | Python bytecode/cache           |

✅ Confirm `.gitignore` contains all above.

---

## 🛠 Cultural Challenges & Fixes

| Challenge                         | Solution                                               |
|----------------------------------|--------------------------------------------------------|
| Dialect mismatch in emotion detection | Fine-tuned model + token normalization              |
| Cultural irrelevance in LLM output | Injected `cultural_embeddings.py` with local phrases |
| Western bias in crisis flags     | Custom logic to reflect Omani social structure        |

---

## ✅ Best Practices

- Consult native Omani speakers for phrase review.
- Run `tests/unit/test_*.py` on all cultural modules.
- Avoid hardcoded Western content in prompts.
- Validate emotion labels using real-world dialect samples.

---

## 🚀 Future Enhancements

- Expand emotion dataset with region-specific mental health conversations.
- Build automated dialect classifier.
- Add cultural feedback collection form (opt-in from users).
- Collaborate with local psychologists on fine-tuning prompts.

---

## 🙏 Acknowledgments

- **xAI** for access to Groq models.
- **Azure** for STT/TTS pipelines.
- **Hugging Face** for pretrained Arabic emotion models.
- **Omani Counselors & Linguists** for feedback and cultural alignment.

---

## 🕓 Version History

| Date         | Update Summary                                                |
|--------------|---------------------------------------------------------------|
| July 11, 2025 | Introduced safety alerts and cultural phrase logic           |
| July 12, 2025 | Added GitHub upload rules, tokenization, emotional mapping   |

---

## 📌 Summary

This guide encapsulates the OMANI‑Therapist‑Voice project’s commitment to cultural relevance, safety, and accessibility. By blending dialectal NLP with local emotional intelligence, it serves as a respectful and impactful therapeutic assistant rooted in Omani society.
