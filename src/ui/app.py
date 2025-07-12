from flask import Flask, request, render_template, send_file
from src.utils.logger import setup_logging
from src.api.stt.stt import transcribe_audio
from src.agents.emotion.emotion_agent import analyze_intent
from src.agents.safety.safety_agent import assess_safety
from src.agents.therapy.therapy_agent import generate_therapy_response
from src.api.tts.tts import synthesize_speech
from pydub import AudioSegment
from src.utils.monitoring import monitor  

import logging
import os
import io

app = Flask(__name__)
setup_logging()
logger = logging.getLogger(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    lang = request.args.get("lang", "ar")

    if request.method == "POST":
        try:
            monitor.start_pipeline()  # Start monitoring the pipeline
            audio_file = request.files["audio"]
            audio_bytes = audio_file.read()
            consent = request.form.get("consent")
            if consent != "yes":
                logger.warning("Consent not granted by user.")
                return render_template("index.html", summary="Consent is required to proceed.", lang=lang), 400

            input_io = io.BytesIO(audio_bytes)
            audio = AudioSegment.from_file(input_io, format="webm")
            audio_path = os.path.join("src", "utils", "output.wav")
            audio.export(audio_path, format="wav")
            logger.info("Audio converted to WAV using PyDub")
            monitor.log_stage("audio_conversion", output_data=audio_path)

            transcript = transcribe_audio("output.wav")
            monitor.log_stage("stt", output_data=transcript)
            safety_result = assess_safety(transcript)
            status = safety_result["status"]
            referral = safety_result["referral"]
            emergency = safety_result["emergency"]

            monitor.log_stage("safety", output_data=status)

            if status in ["crisis", "harmful"]:
                summary = f"Alert: {referral}. For immediate help, contact: {emergency}."
                logger.info(f"Crisis detected: {summary}")
                monitor.log_stage("pipeline", output_data="halted_due_to_crisis")
                monitor.log_metrics()
                return render_template("index.html", summary=summary, lang=lang), 200

            # Optional: defensive check for unexpected status
            if status not in ["safe", "neutral", "positive"]:
                logger.warning(f"Unexpected status passed through: {status}")
                return render_template("index.html", summary="Unexpected issue occurred. Please try again later.", lang=lang), 500

            emotion, score = analyze_intent(transcript)
            monitor.log_stage("emotion", output_data=emotion)
            response = generate_therapy_response(transcript, emotion)
            monitor.log_stage("therapy", output_data=response)

            output_file = synthesize_speech(response)
            full_path = os.path.abspath(os.path.join("src", "utils", output_file))
            monitor.log_stage("tts", output_data=full_path)
            monitor.log_metrics()
            logger.info(f"Pipeline completed: {transcript} | {response} | {full_path}")

            return send_file(full_path, mimetype="audio/wav")

        except Exception as e:
            monitor.log_stage("pipeline", error=e)
            monitor.log_metrics()
            logger.error(f"Pipeline failed: {str(e)}")
            return {"error": str(e)}, 500

    return render_template("index.html", summary=summary, lang=lang)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
