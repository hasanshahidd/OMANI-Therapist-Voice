import json
import os
import logging
import scipy.io.wavfile as wavfile
from azure.cognitiveservices.speech import (
    SpeechConfig,
    SpeechSynthesizer,
    AudioConfig,
    SpeechSynthesisOutputFormat,
    CancellationDetails,
    ResultReason,
)

from src.utils.logger import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

def synthesize_speech(text, output_file="output_tts.wav"):
    try:
        logger.info("Starting TTS synthesis...")

        # Load config for TTS
        with open(r"src\api\config\azure_config.json", "r", encoding="utf-8") as f:
            config_data = json.load(f)
        tts_config = config_data["tts"]

        # Setup SpeechConfig
        speech_config = SpeechConfig(subscription=tts_config["subscription_key"], region=tts_config["region"])
        speech_config.speech_synthesis_voice_name = "ar-EG-SalmaNeural"  # Use supported Arabic voice for eastus
        speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm)

        # Output path
        audio_path = os.path.join("src", "utils", output_file)
        audio_config = AudioConfig(filename=audio_path)

        # Synthesize
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        result = synthesizer.speak_text_async(text).get()

        # Handle result
        if result.reason == ResultReason.SynthesizingAudioCompleted:
            logger.info(f"TTS synthesis completed, saved to {output_file}")
            if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
                sample_rate, _ = wavfile.read(audio_path)
                logger.info(f"Output WAV format: {sample_rate} Hz, mono, 16-bit PCM")
            else:
                logger.error("TTS output file is empty or not created")
                raise RuntimeError("TTS output file is empty or not created")
            return output_file

        elif result.reason == ResultReason.Canceled:
            cancellation = CancellationDetails(result)
            logger.error(f"TTS canceled: {cancellation.reason}, {cancellation.error_details}")
            raise RuntimeError(f"TTS canceled: {cancellation.reason}, {cancellation.error_details}")

    except Exception as e:
        logger.error(f"TTS failed: {str(e)}")
        raise

if __name__ == "__main__":
    synthesize_speech("مرحبًا، كيف يمكنني مساعدتك؟")  # Example Arabic text
