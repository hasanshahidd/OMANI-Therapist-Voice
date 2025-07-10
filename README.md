# Omani-Therapist-Voice
A voice-only mental health chatbot in Omani Arabic for Elile AI's technical assessment.

## Features
- STT/TTS pipeline with Azure Speech Services (Omani Arabic, >90% accuracy, <20s latency).
- Emotion detection with hatemnoaman/bert-base-arabic-finetuned-emotion (models/arabic_emotion_model/).
- CBT-based therapy responses (therapy_agent.py).
- Text normalization for Arabic diacritics.
- Omani cultural considerations (see cultural_guide.md).

## Setup
1. Install Python 3.10+ from [python.org](https://www.python.org/).
2. Create a virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run voice capture: `python src\utils\voice_capture.py`
6. Run STT: `python src\api\stt\stt.py`
7. Run TTS: `python src\api\tts\tts.py`
8. Run emotion analysis: `python src\agents\emotion\emotion_agent.py`
9. Run therapy response: `python src\agents\therapy\therapy_agent.py`
10. Run pipeline test: `pytest tests\integration\test_pipeline.py`

## Notes
- Sample audio: `src\utils\output.wav` ("أحتاج إلى المساعدة، وأريد أن أعيش معك"), `src\utils\output_tts.wav`
- Reference transcript: `src\api\stt\mock_transcript.txt` ("أحتاج إلى المساعدة، وأريد أن أعيش معك.")
- Logs: `pipeline.log`
- API setup in `docs/deployment.md`
- Pipeline architecture in `docs/architecture/pipeline_architecture.md`
- Designed for long-term local runnability with stable libraries.
