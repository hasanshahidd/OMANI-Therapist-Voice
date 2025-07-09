     Omani-Therapist-Voice
     A voice-only mental health chatbot in Omani Arabic for Elile AI's technical assessment.

     Setup
     1. Install Python 3.10+ from [python.org](https://www.python.org/).
     2. Create a virtual environment: `python -m venv venv`
     3. Activate: `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
     4. Install dependencies: `pip install -r requirements.txt`
     5. Run voice capture test: `python src/utils/voice_capture.py`
     6. Run unit tests: `pytest tests/unit/test_voice_capture.py`

     Notes
     - Sample audio: `src/utils/output.wav`
     - Logs: `pipeline.log`
     - STT/TTS setup (Google Cloud, Azure free tiers) instructions in `docs/deployment.md` (Day 2).
     - Designed for long-term local runnability with stable libraries.

