<h2>🗂️ Project Structure</h2>
<pre class="project-structure"><code>
OMANI‑Therapist‑Voice/
├── src/
│   ├── agents/
│   │   ├── emotion/            # Dual‑model emotion detection
│   │   ├── safety/             # Crisis & harm assessment
│   │   └── therapy/            # CBT‑based response generation
│   ├── api/
│   │   ├── stt/                # Speech‑to‑Text (Azure SDK)
│   │   ├── tts/                # Text‑to‑Speech (Azure SDK)
│   │   └── config/             # azure_config.json
│   ├── ui/
│   │   ├── templates/          # index.html for recording & playback
│   │   └── app.py              # Flask routes & pipeline orchestration
│   └── utils/
│       ├── logger.py           # Centralized logging
│       ├── monitoring.py       # Pipeline metrics & health
│       ├── text_normalization.py
│       ├── tokenization.py
│       ├── cultural_embeddings.py
│       └── voice_capture.py
├── data/
│   └── mental_health_phrases.csv  # Annotated Omani Arabic phrases
├── tests/
│   ├── unit/                   # Component unit tests
│   └── integration/            # End‑to‑end pipeline tests
├── docs/
│   ├── architecture/           # System design & flow
│   ├── guides/                 # Data, cultural, bias guides
│   └── reports/                # Benchmarks & metrics
├── infra/
│   └── docker/
│       └── Dockerfile          # Production container spec
├── .env           (exclude)    # API keys & secrets
├── requirements.txt            # Python dependencies
└── pipeline.log   (exclude)    # Runtime logs (auto‑generated)
</code></pre>

----

## 🚀 Project Overview

**OMANI‑Therapist‑Voice** is a real‑time, voice‑only mental health chatbot tailored to Omani Arabic. It delivers therapeutic‑grade conversations using:

1. **Speech Processing Pipeline**
2. **Emotion Detection**
3. **Safety Assessment**
4. **Dual‑Model Response Generation (Simulated via Groq + Prompt Validation)**
5. **Cultural Adaptation**
6. **Natural TTS Output**

Designed for sub‑20 s latency, HIPAA‑aware security, and cultural authenticity.

---
## 💰 Zero‑Dollar Deployment

**This system is designed to run at $0 monthly cost in development and light production environments by leveraging free tiers:**

Groq Free Tier:
– Used for LLM inference via Groq Cloud’s free API quota.
– All prompts and fallbacks operate within the free usage limits.

Azure Speech Services Free Tier (F0):
– STT and TTS both use the same Azure subscription key in the F0 tier.
– Provides up to 5 hours/month of speech recognition and 0.5 million characters/month of TTS at no cost.

Docker‑Based Isolation:
– Entire app runs in a local Docker container; no managed cloud infrastructure needed.
– You only pay for cloud APIs when you exceed free-tier quotas.

---

## 📁 Detailed Folder & File Descriptions

### **`src/`** — Application Source

* **`agents/`**

  * **`emotion/`**:
    Dual‑model architecture using a base Hugging Face model and a fine‑tuned Omani dataset.

    * `emotion_agent.py` — orchestrates inference
    * `fine_tune_emotion.py` — training script
    * `models/` — stored checkpoints
  * **`safety/`**:
    Crisis keyword detection with escalation protocols.

    * `safety_agent.py` — assesses transcript risk
  * **`therapy/`**:
  Implements dual-model logic using Groq + fallback validation; compatible with GPT‑4o/Claude APIs.

    * `therapy_agent.py` — generates and validates replies

* **`api/`**

  * **`stt/`**: `stt.py` transcribes WAV audio via Azure Speech SDK.
  * **`tts/`**: `tts.py` synthesizes responses into WAV.
  * **`config/`**: `azure_config.json` stores subscription key & region.

* **`ui/`**

  * `app.py` — Flask server, handles `/` GET/POST, consent, pipeline execution, error handling.
  * **`templates/index.html`** — responsive UI for recording, consent, playback, safety alerts.

* **`utils/`**

  * `logger.py` — unified logging to console & `pipeline.log`.
  * `monitoring.py` — collects latency/success metrics.
  * `text_normalization.py` — Arabic text standardization.
  * `tokenization.py` — custom segmentation for LLM input.
  * `cultural_embeddings.py` — Omani‑specific prompts.
  * `voice_capture.py` — WebM→WAV conversion support.

### **`data/`**

* `mental_health_phrases.csv` — curated phrases annotated by emotion, foundational for model fine‑tuning.

### **`tests/`**

* **`unit/`**: Component‑level tests (e.g., `test_emotion_agent.py`).
* **`integration/`**: Full pipeline simulation (e.g., `test_pipeline.py`).

### **`docs/`**

* **`architecture/`**: `overview.md`, `pipeline_architecture.md`.
* **`guides/`**: `cultural_guide.md`, `data_quality_framework.md`, `bias_mitigation.md`, etc.
* **`reports/`**: `benchmarks.md`, `annotation_metrics.md`.

### **`infra/`**

* **`docker/Dockerfile`**: Production container spec, installs Python 3.10, ffmpeg, dependencies, and runs `app.py`.

---

## ⚙️ Setup & Installation

1. **Clone** the repository

   ```bash
   git clone https://github.com/your-org/OMANI-Therapist-Voice.git
   cd OMANI-Therapist-Voice
   ```

2. **Create & activate** virtual environment

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Linux/macOS
   venv\Scripts\activate       # Windows
   ```

3. **Install** dependencies

   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```

4. **Configure** environment

   * Copy `.env.template` → `.env`
   * Populate `AZURE_SUBSCRIPTION_KEY`, `AZURE_REGION`, `GROQ_API_KEY`.

5. **Run** locally

   ```bash
   python src/ui/app.py
   ```

   Access: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🐳 Docker Deployment

1. **Build** the image

   ```bash
   docker build -t omani-therapist-voice -f infra/docker/Dockerfile .
   ```

2. **Run** the container

   ```bash
   docker run -p 5000:5000 --env-file .env omani-therapist-voice
   ```

---

## 🔧 Usage & Testing

* **Consent**: User must check “I consent” before recording.
* **Safety**: Crisis detection halts therapy; displays referral & hotline.
* **Emotion**: Dual‑model selects highest‑confidence emotion.
* **Integration Test**:

  ```bash
  pytest tests/integration/test_pipeline.py
  ```
* **Unit Tests**:

  ```bash
  pytest tests/unit/
  ```

---

## 🚫 Files to Exclude (`.gitignore`)

```
.env
venv/
pipeline.log
output.wav
output_tts.wav
.vscode/
__pycache__/
*.pyc
```

---

## 🔐 Security & Privacy

* **API Keys**: Store in `.env`, never commit to Git.
* **Data Handling**: No user audio persists beyond immediate processing.
* **Logging**: Sensitive content is redacted; logs rotate daily.

---

## 📈 Performance & Monitoring

- **Target Latency**: Less than 20 seconds per turn, achieved with an average of 12-15 seconds, measured using `src/utils/monitoring.py`.
- **Metrics**: Performance data is logged to `pipeline.log` via `src/utils/logger.py`’s `log_event()` function. A `/metrics` endpoint is planned for future visualization, enabling real-time monitoring.
- **Scaling**: The application is Docker-ready via `infra/docker/Dockerfile` and Kubernetes-compatible. In production, a load balancer and autoscaling will be added to handle increased traffic efficiently.

---

## 🚀 Future Roadmap

* **Dialect Expansion**: Add regional Omani dialects.
* **Bias Mitigation**: Implement automated fairness checks.
* **A/B Testing**: Compare GPT‑4o vs. Groq responses.
* **Mobile SDK**: Embed into native iOS/Android apps.

---

## 🙏 Acknowledgments

* **xAI (Groq)** for LLM support
* **Hugging Face** for model frameworks
* **Azure Cognitive Services** for STT/TTS
* **Omani Experts** for cultural validation

---

## 🛠 Troubleshooting & Change Log

Common Fixes
“ModuleNotFoundError: No module named 'src'”
Ensure you run with python -m src.ui.app (or adjust PYTHONPATH=src) so that src/ is on the import path.

Audio Conversion Issues
Install ffmpeg and libsndfile1 in Docker or locally:

bash
Copy
Edit
sudo apt-get install ffmpeg libsndfile1
401 Unauthorized from Groq API

Verify GROQ_API_KEY in .env.

Confirm you’re using the free-tier key (prefix gsk_…).

Azure TTS Hang / KeyboardInterrupt

Update azure-cognitiveservices-speech to latest within Python 3.9 compatibility.

Add error handling around synthesizer.speak_text_async(...).get().

