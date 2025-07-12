import pytest
from src.api.stt.stt import transcribe_audio
from src.agents.emotion.emotion_agent import analyze_emotion
from src.agents.therapy.therapy_agent import generate_therapy_response
from src.api.tts.tts import synthesize_speech
from src.utils.logger import setup_logging
import logging
import os
import re
import difflib

setup_logging()
logger = logging.getLogger(__name__)

def normalize_text(text):
    """Remove extra spaces and punctuation for comparison."""
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', text)).strip()

def test_pipeline():
    try:
        logger.info("Starting pipeline integration test...")

        # Step 1: STT
        transcript = transcribe_audio()
        assert transcript, "STT transcription is empty"
        assert any(c.isalpha() for c in transcript), "STT transcription contains no valid text"
        logger.info(f"STT passed: {transcript}")

        # Optional accuracy log
        mock_transcript_path = r"src/api/stt/mock_transcript.txt"
        if os.path.exists(mock_transcript_path):
            with open(mock_transcript_path, "r", encoding="utf-8") as f:
                expected = f.read().strip()
            similarity = difflib.SequenceMatcher(None, normalize_text(transcript), normalize_text(expected)).ratio()
            logger.info(f"Transcription accuracy (reference): {similarity*100:.2f}%")

        # Step 2: Emotion
        emotion, score = analyze_emotion(transcript)
        assert emotion in ["sadness", "anger", "joy", "fear", "surprise", "neutral", "love"], "Unexpected emotion detected"
        assert 0 <= score <= 1
        logger.info(f"Emotion analysis passed: {emotion} (confidence: {score:.2f})")

        # Step 3: Therapy
        response = generate_therapy_response(transcript, emotion)
        assert isinstance(response, str)
        assert len(response) > 0
        logger.info(f"Therapy response passed: {response}")

        # Step 4: TTS
        output_file = synthesize_speech(response)

        # ✅ Ensure this matches your actual path
        expected_path = os.path.abspath("src/utils/output_tts.wav")
        assert os.path.exists(expected_path), f"TTS file not found at {expected_path}"
        assert os.path.getsize(expected_path) > 0
        logger.info(f"TTS passed: {expected_path} generated")

    except Exception as e:
        logger.error(f"Pipeline test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_pipeline()
