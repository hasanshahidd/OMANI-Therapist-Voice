import sounddevice as sd
import scipy.io.wavfile as wavfile
import logging
import os

# Set absolute path for pipeline.log
LOG_FILE = os.path.join(r"C:\Users\Admin\Desktop\OMANI-Therapist-Voice", "pipeline.log")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ],
    force=True
)

def record_audio(duration=5, sample_rate=16000):
    try:
        logging.info("Starting audio recording...")
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()
        logging.info("Recording stopped.")
        output_file = "output.wav"
        wavfile.write(output_file, sample_rate, audio)
        logging.info(f"Saved audio to {output_file}")
        return output_file
    except Exception as e:
        logging.error(f"Recording failed: {str(e)}")
        raise

if __name__ == "__main__":
    record_audio()
