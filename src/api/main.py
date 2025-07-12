import os
from src.api.stt.stt import transcribe_audio
from src.agents.safety.safety_agent import assess_safety
from src.agents.emotion.emotion_agent import analyze_intent
from src.agents.therapy.therapy_agent import generate_therapy_response
from src.api.tts.tts import synthesize_speech
from src.utils.monitoring import monitor
from src.utils.logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_AUDIO_PATH = os.path.join(BASE_DIR, "src", "utils", "output.wav")

def run_pipeline(audio_file=DEFAULT_AUDIO_PATH):
    monitor.start_pipeline()
    try:
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")

        transcript = transcribe_audio(audio_file)
        monitor.log_stage("stt", input_data=audio_file, output_data=transcript)

        status, referral, emergency = assess_safety(transcript)
        monitor.log_stage("safety", input_data=transcript, output_data=status)

        if status in ["crisis", "harmful"]:
            response = referral
        else:
            emotion, score = analyze_intent(transcript)
            monitor.log_stage("emotion", input_data=transcript, output_data=emotion)

            response = generate_therapy_response(transcript, emotion)
            monitor.log_stage("therapy", input_data=transcript, output_data=response)

        output_file = synthesize_speech(response)
        monitor.log_stage("tts", input_data=response, output_data=output_file)

        monitor.log_metrics()
        return output_file, response

    except Exception as e:
        monitor.log_stage("pipeline", error=e)
        monitor.log_metrics()
        raise

if __name__ == "__main__":
    run_pipeline()
