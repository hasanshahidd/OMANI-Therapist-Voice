import json
import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig, ResultReason
from src.utils.logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

def transcribe_audio(audio_file="output.wav"):
    try:
        logger.info("Starting STT transcription...")
        audio_path = os.path.join("src", "utils", audio_file)
        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        logger.info(f"Using audio file: {audio_path}")

        # Load config
        with open("src/api/config/azure_config.json", "r", encoding="utf-8") as f:
            config_data = json.load(f)

        stt_config = config_data.get("stt", {})
        speech_config = SpeechConfig(
            subscription=stt_config.get("subscription_key"),
            region=stt_config.get("region")
        )
        speech_config.speech_recognition_language = "ar-OM"  # Omani Arabic

        audio_config = AudioConfig(filename=audio_path)
        recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        result = recognizer.recognize_once()

        if result.reason == ResultReason.NoMatch:
            logger.error("No speech could be recognized")
            raise ValueError("No speech recognized")
        if result.reason == ResultReason.Canceled:
            logger.error(f"Recognition canceled: {result.cancellation_details}")
            raise RuntimeError(f"Recognition canceled: {result.cancellation_details}")

        transcript = result.text
        logger.info(f"Transcription: {transcript}")
        return transcript

    except Exception as e:
        logger.error(f"STT failed: {str(e)}")
        raise

if __name__ == "__main__":
    transcribe_audio()
