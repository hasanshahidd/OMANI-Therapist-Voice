<h1 align="center">🏛️ Architecture Overview — OMANI‑Therapist‑Voice</h1>



---

## 🧠 System Design

OMANI-Therapist-Voice is a Flask-based web application engineered to deliver culturally sensitive mental health support in Omani Arabic.  
It processes user audio through a modular, multi-stage pipeline:

1. 🎤 Speech-to-Text (STT)  
2. 🛡 Safety Assessment  
3. 😔 Emotion Detection  
4. 💬 Therapy Generation  
5. 🔊 Text-to-Speech (TTS)

Designed for maintainability and scalability, the architecture separates logic into distinct folders (`agents`, `api`, `utils`) with full logging and real-time performance monitoring. The app runs via `http://127.0.0.1:5000` or offline via script. Docker is used for deployment flexibility.

---

## 🔑 Key Components

### 🖥 Web Interface

- **File**: `src/ui/app.py`  
- **Role**: Serves `index.html`, accepts audio via POST, converts WebM to WAV using `pydub`, calls all pipeline stages.  
- **Notes**: Streams final audio with `send_file`. Supports `lang=ar` / `lang=en`.  
- **Logging**: Integrated via `src/utils/logger.py`. 500 error handling included.

---

### 🎧 Speech-to-Text (STT)

- **File**: `src/api/stt/stt.py`  
- **Role**: Uses Azure Speech SDK to transcribe `src/utils/output.wav`.  
- **Mocking**: Includes `mock_transcript.txt` for testing.  
- **Config**: Reads credentials from `src/api/config/azure_config.json`.  
- **Settings**: Input is 16kHz mono WAV, optimized for Arabic.  
- **Log Reference**: "Lahola lahola ولا قوة؟" (12:31:09,823)

---

### 🛡 Safety Assessment

- **File**: `src/agents/safety/safety_agent.py`  
- **Role**: Analyzes transcripts for harmful or crisis-related content.  
- **Preprocessing**: Uses `src/utils/text_normalization.py` to handle Arabic variants.  
- **Logic**: Uses keyword/contextual rules to flag high-risk messages.  
- **Log Reference**: 12:31:10,252

---

### 😔 Emotion Detection

- **File**: `src/agents/emotion/emotion_agent.py`  
- **Models**: 
  - Base HuggingFace model → `models/arabic_emotion_model/`  
  - Fine-tuned Omani model → `models/emotion_finetuned/`  
- **Training Data**: `data/mental_health_phrases.csv`  
- **Detection**: Chooses emotion with highest confidence.  
- **Log Reference**: "sadness" at 0.99 confidence (12:31:14,769)  
- **Training Script**: `fine_tune_emotion.py`  
- **Unit Tests**: `tests/unit/test_emotion_agent.py`

---

### 💬 Therapy Generation

- **File**: `src/agents/therapy/therapy_agent.py`  
- **LLM**: Uses Groq LLM to generate CBT-style responses.  
- **Prompt Injection**: Pulls Omani phrases from `src/utils/cultural_embeddings.py`  
- **Example Phrase**: "الصبر مفتاح الفرج"  
- **Validation**: Ensures cultural alignment.  
- **Log Reference**: 12:31:14,882

---

### 🔊 Text-to-Speech (TTS)

- **File**: `src/api/tts/tts.py`  
- **Role**: Converts therapy output to audio using Azure SDK.  
- **Output**: Saves to `src/utils/output_tts.wav`  
- **Voices**: Supports Omani Arabic  
- **Log Reference**: 12:31:15,637

---

### ⚙️ Utilities

- **Logger**: `src/utils/logger.py`  
  - Unified logs with timestamp, level (INFO/ERROR) → `pipeline.log`
- **Monitoring**: `src/utils/monitoring.py`  
  - Tracks stage latency & success rates; embedded in `app.py`
- **Voice Capture**: `src/utils/voice_capture.py`  
  - Converts WebM → WAV
- **Normalization**: `src/utils/text_normalization.py`  
  - Standardizes Arabic characters and punctuation
- **Tokenization**: `src/utils/tokenization.py`  
  - Placeholder for future preprocessing logic

---

## 📦 Deployment

- **Dockerfile**: `infra/docker/Dockerfile`  
- **Command**:  
  ```bash
  docker build -t omani-therapist-voice .
  docker run -p 5000:5000 omani-therapist-voice
  ```

---

## ⚙️ Technical Specifications

- **Language**: Python 3.9+  
- **Core Libraries**:  
  - `Flask`, `transformers`, `langchain-groq`, `pydub`, `azure-cognitiveservices-speech`  
- **Models**:  
  - Hugging Face BERT (Arabic)  
  - Groq LLM  
- **Target Performance**:  
  - < 20s latency (end-to-end), tracked via monitoring

---

## 🗂️ Project Structure

```text
OMANI-Therapist-Voice/
├── src/
│   ├── agents/       # Emotion, therapy, safety agents
│   ├── api/          # STT, TTS, main scripts
│   ├── ui/           # Web interface
│   └── utils/        # Utilities
├── data/             # Data files
├── tests/            # Unit and integration tests
├── docs/             # Documentation
├── infra/            # Docker configuration
├── .env              # Environment vars
├── requirements.txt  # Dependencies
└── pipeline.log      # Logs
```

---

## 🧪 Implementation Details

- **Integration Testing**:  
  `tests/integration/test_pipeline.py` with `mock_transcript.txt`  
- **Unit Testing**:  
  `tests/unit/test_therapy_agent.py`, `test_emotion_agent.py`, etc.  
- **Data Source**:  
  `data/mental_health_phrases.csv`

---

## 🛠 Challenges & Fixes

- **Model Loading Lag**  
  → Solved with early preloading in `emotion_agent.py`
- **TTS Audio Cutoffs**  
  → Resolved via debug logging and Azure SDK fix

---

## 🚀 Future Considerations

- Add load balancing for multi-user scaling  
- Retrain `emotion_finetuned` with larger Omani dataset  
- Implement `tokenization.py` for smarter preprocessing

---

## 🙏 Acknowledgments

- 🧠 Hugging Face for transformer-based models  
- 🔊 Azure Cognitive Services (STT/TTS APIs)  
- 🤖 Groq for culturally responsive therapy LLM

