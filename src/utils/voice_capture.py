import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import logging
import os

# Set absolute path for logs and output
BASE_DIR = r"C:\Users\Admin\Desktop\OMANI-Therapist-Voice"     
UTILS_DIR = os.path.join(BASE_DIR, "src", "utils")
os.makedirs(UTILS_DIR, exist_ok=True)
LOG_FILE = os.path.join(BASE_DIR, "pipeline.log")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
    force=True
)

def record_audio(duration=10, sample_rate=16000):
    try:
        logging.info("Starting audio recording...")
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()
        logging.info("Recording stopped.")

        # Convert float32 to int16 for 16-bit PCM
        audio_int16 = np.int16(audio * 32767)

        output_path = os.path.join(UTILS_DIR, "output.wav")
        wavfile.write(output_path, sample_rate, audio_int16)
        logging.info(f"Saved audio to {output_path}")
        return output_path
    except Exception as e:
        logging.error(f"Recording failed: {str(e)}")
        raise

if __name__ == "__main__":
    record_audio()
