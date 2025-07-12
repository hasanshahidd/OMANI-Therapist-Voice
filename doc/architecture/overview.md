<!-- File: docs/architecture/overview.html -->

<h1 align="center">🏛️ Architecture Overview — OMANI‑Therapist‑Voice</h1>

<hr>

<h2>🧠 System Design</h2>
<p>
  OMANI‑Therapist‑Voice is a Flask‑based web application engineered to deliver culturally sensitive mental health support in Omani Arabic.<br>
  It processes user audio through a modular, multi‑stage pipeline:
</p>
<ol>
  <li>🎤 Speech‑to‑Text (STT)</li>
  <li>🛡 Safety Assessment</li>
  <li>😔 Emotion Detection</li>
  <li>💬 Therapy Generation</li>
  <li>🔊 Text‑to‑Speech (TTS)</li>
</ol>
<p>
  Designed for maintainability and scalability, the architecture separates logic into distinct folders (<code>agents</code>, <code>api</code>, <code>utils</code>) with full logging and real‑time performance monitoring.<br>
  The app runs at <a href="http://127.0.0.1:5000">http://127.0.0.1:5000</a> or offline via script. Docker provides deployment flexibility.
</p>

<hr>

<h2>🔑 Key Components</h2>

<h3>🖥 Web Interface</h3>
<ul>
  <li><strong>File:</strong> <code>src/ui/app.py</code></li>
  <li><strong>Role:</strong> Serves <code>index.html</code>, accepts audio via POST, converts WebM to WAV using <code>pydub</code>, invokes all pipeline stages.</li>
  <li><strong>Notes:</strong> Streams final audio with <code>send_file</code>. Supports <code>lang=ar</code> / <code>lang=en</code>.</li>
  <li><strong>Logging:</strong> Integrated via <code>src/utils/logger.py</code>, with 500‑error handling.</li>
</ul>

<h3>🎧 Speech‑to‑Text (STT)</h3>
<ul>
  <li><strong>File:</strong> <code>src/api/stt/stt.py</code></li>
  <li><strong>Role:</strong> Azure Speech SDK transcribes <code>src/utils/output.wav</code>.</li>
  <li><strong>Mocking:</strong> Includes <code>mock_transcript.txt</code> for tests.</li>
  <li><strong>Config:</strong> Credentials from <code>src/api/config/azure_config.json</code>.</li>
  <li><strong>Settings:</strong> 16 kHz mono WAV, optimized for Arabic.</li>
  <li><strong>Log Ref.:</strong> “Lahola lahola ولا قوة؟” @ 12:31:09,823</li>
</ul>

<h3>🛡 Safety Assessment</h3>
<ul>
  <li><strong>File:</strong> <code>src/agents/safety/safety_agent.py</code></li>
  <li><strong>Role:</strong> Flags harmful/crisis content via <code>normalize_arabic_text()</code>.</li>
  <li><strong>Preproc.:</strong> <code>src/utils/text_normalization.py</code> handles Arabic variants.</li>
  <li><strong>Log Ref.:</strong> 12:31:10,252</li>
</ul>

<h3>😔 Emotion Detection</h3>
<ul>
  <li><strong>File:</strong> <code>src/agents/emotion/emotion_agent.py</code></li>
  <li><strong>Models:</strong>
    <ul>
      <li>Base HF model → <code>models/arabic_emotion_model/</code></li>
      <li>Fine‑tuned Omani → <code>models/emotion_finetuned/</code></li>
    </ul>
  </li>
  <li><strong>Data:</strong> <code>data/mental_health_phrases.csv</code></li>
  <li><strong>Detection:</strong> Chooses highest‑confidence emotion (“sadness” @ 0.99 @ 12:31:14,769)</li>
  <li><strong>Script:</strong> <code>fine_tune_emotion.py</code></li>
  <li><strong>Tests:</strong> <code>tests/unit/test_emotion_agent.py</code></li>
</ul>

<h3>💬 Therapy Generation</h3>
<ul>
  <li><strong>File:</strong> <code>src/agents/therapy/therapy_agent.py</code></li>
  <li><strong>LLM Backend:</strong> Uses <code>Groq-hosted Mixtral</code> for generating culturally appropriate CBT-style responses.</li>
  <li><strong>Prompt Logic:</strong> Dynamically injects Omani Arabic idioms from <code>src/utils/cultural_embeddings.py</code> (e.g., “الصبر مفتاح الفرج”) to ensure relevance and trust-building.</li>
  <li><strong>Dual-Model Strategy:</strong> Prompt chaining and response validation emulate GPT-4o + Claude Opus 4 behavior under API constraints.</li>
  <li><strong>Validation:</strong> Ensures responses align with Islamic values, therapeutic tone, and dialect sensitivity.</li>
  <li><strong>Log Reference:</strong> 12:31:14,882</li>
</ul>


<h3>🔊 Text‑to‑Speech (TTS)</h3>
<ul>
  <li><strong>File:</strong> <code>src/api/tts/tts.py</code></li>
  <li><strong>Role:</strong> Azure TTS converts therapy text to <code>src/utils/output_tts.wav</code>.</li>
  <li><strong>Voices:</strong> Omani Arabic; disabled in crisis cases.</li>
  <li><strong>Log Ref.:</strong> 12:31:15,637</li>
</ul>

<h3>⚙️ Utilities</h3>
<ul>
  <li><strong>Logger:</strong> <code>src/utils/logger.py</code> → unified logs (<code>pipeline.log</code>).</li>
  <li><strong>Monitoring:</strong> <code>src/utils/monitoring.py</code> → stage latency & success rates.</li>
  <li><strong>Voice Capture:</strong> <code>src/utils/voice_capture.py</code> → WebM→WAV.</li>
  <li><strong>Normalization:</strong> <code>src/utils/text_normalization.py</code>.</li>
  <li><strong>Tokenization:</strong> <code>src/utils/tokenization.py</code>.</li>
</ul>

<hr>

<h2>📦 Deployment</h2>
<pre><code>docker build -t omani-therapist-voice infra/docker/Dockerfile .
docker run -p 5000:5000 omani-therapist-voice
</code></pre>

<hr>

<h2>⚙️ Technical Specifications</h2>
<ul>
  <li>Python 3.9+</li>
  <li>Flask, transformers, langchain‑groq, pydub, azure‑cognitiveservices‑speech</li>
  <li>Models: HF BERT (Arabic), Groq LLM</li>
  <li>Latency < 20 s (monitored)</li>
</ul>

<hr>

<h2>🗂️ Project Structure</h2>
<pre class="project-structure"><code>
OMANI‑Therapist‑Voice/
├── src/
│   ├── agents/
│   ├── api/
│   ├── ui/
│   └── utils/
├── data/
├── tests/
├── docs/
│   └── architecture/overview.html
├── infra/
│   └── docker/
├── .env           (exclude)
├── requirements.txt
└── pipeline.log   (exclude)
</code></pre>

<hr>

<h2>🛠 Challenges & Fixes</h2>
<ul>
  <li><strong>Model Loading Lag:</strong> Preloaded models in <code>emotion_agent.py</code>.</li>
  <li><strong>TTS Cutoffs:</strong> Debug logs + Azure SDK fix; disabled in crisis.</li>
  <li><strong>Consent Flow:</strong> Checkbox + 400 error if missing.</li>
</ul>

<hr>

<h2>🚀 Future Considerations</h2>
<ul>
  <li>Load balancing for scale.</li>
  <li>Expand emotion dataset.</li>
  <li>Implement bias mitigation per <code>bias_mitigation.md</code>.</li>
</ul>

<hr>

<h2>🙏 Acknowledgments</h2>
<ul>
  <li>Hugging Face</li>
  <li>Azure Cognitive Services</li>
  <li>Groq</li>
</ul>

<hr>

<h2>📜 Version History</h2>
<ul>
  <li><strong>July 11, 2025:</strong> Safety alerts, tokenization, consent flow added.</li>
  <li><strong>July 12, 2025:</strong> GitHub guidelines, refined overview.</li>
</ul>

<p class="footer-note">
  <strong>Exclude from GitHub:</strong> <code>.env</code>, <code>venv/</code>, <code>pipeline.log</code>, audio outputs, <code>__pycache__</code>.
</p>
