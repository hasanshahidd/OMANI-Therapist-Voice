# Text Pipeline Guide - OMANI-Therapist-Voice

## Introduction
The OMANI-Therapist-Voice project processes user input through a sophisticated text pipeline, transforming audio transcripts into meaningful therapy responses or safety alerts. This guide details the stages of the text pipeline, from normalization to therapy generation, reflecting recent enhancements such as custom tokenization and the safety alert system. It provides a comprehensive resource for developers, contributors, and stakeholders to understand, maintain, and optimize the pipeline, while including guidance for secure GitHub uploads.

## Pipeline Process
### Stages
1. **Text Normalization**
   - **File**: `src/utils/text_normalization.py`
   - **Description**: Standardizes Arabic text by removing diacritics and normalizing variations, ensuring consistency for subsequent processing.
   - **Implementation**: Applied to transcripts from `src/api/stt/stt.py`, logged via `src/utils/logger.py`.

2. **Tokenization**
   - **File**: `src/utils/tokenization.py`
   - **Description**: Performs custom segmentation of text to prepare it for emotion detection models in `src/agents/emotion/emotion_agent.py`, enhancing input quality.
   - **Implementation**: Integrated into the pipeline, with outputs monitored by `src/utils/monitoring.py`.

3. **Emotion Analysis**
   - **File**: `src/agents/emotion/emotion_agent.py`
   - **Description**: Uses dual Hugging Face models (`models/arabic_emotion_model` and `models/emotion_finetuned`) to detect emotions (e.g., "sadness" with 1.00 confidence), selecting the highest-confidence result.
   - **Implementation**: Trained on `data/mental_health_phrases.csv`, validated by `tests/unit/test_emotion_agent.py`.

4. **Safety Assessment**
   - **File**: `src/agents/safety/safety_agent.py`
   - **Description**: Evaluates text for crisis or harmful content, triggering a halt if detected, with alerts managed by `src/ui/app.py`.
   - **Implementation**: Uses normalized text to flag issues, logged for review.

5. **Therapy Generation**
   - **File**: `src/agents/therapy/therapy_agent.py`
   - **Description**: Generates CBT-based responses using a Groq LLM, enriched with cultural prompts from `src/utils/cultural_embeddings.py`, skipped in safety cases.
   - **Implementation**: Outputs are synthesized by `src/api/tts/tts.py` when safe.

## Implementation Details
### Input and Output
- **Input**: Raw transcript from `src/api/stt/stt.py`.
- **Output**: Either a therapy response (as audio via `output_tts.wav`) or a safety alert displayed in `src/ui/templates/index.html`.

### Monitoring and Logging
- **File**: `src/utils/monitoring.py`
- **Description**: Tracks each pipeline stage (e.g., normalization, tokenization) and logs metrics (e.g., latency) to `pipeline.log`, excluded from GitHub for privacy.
- **Implementation**: Integrated into `src/ui/app.py` for real-time insights.


## GitHub Upload Guidelines
To maintain security and efficiency when uploading to GitHub, exclude the following files and directories:
- `.env`: Contains sensitive API keys (e.g., Azure, Groq).
- `venv/`: Virtual environment, machine-specific.
- `pipeline.log`: Runtime log file, regeneratable.
- `output.wav` and `output_tts.wav`: Generated audio files, recreatable.
- `.vscode/`: Personal IDE settings, not project-critical.
- `__pycache__` and `*.pyc`: Python cache files.
The `.gitignore` file automates this exclusion—verify its contents before committing.

## Optimization Tips
- **Batch Processing**: Consider batching tokenization for large inputs to reduce latency.
- **Model Efficiency**: Adjust model parameters in `emotion_agent.py` for performance.
- **Safety Tuning**: Refine `safety_agent.py` logic to minimize false positives.

## Testing
- **File**: `tests/integration/test_pipeline.py`
- **Description**: Validates the end-to-end text pipeline using `mock_transcript.txt`, ensuring reliability across stages.

## Challenges and Solutions
- **Tokenization Overhead**: Addressed by optimizing `tokenization.py` for speed.
- **Safety Delays**: Mitigated by prioritizing safety checks early in the pipeline.
- **Response Accuracy**: Improved by fine-tuning `emotion_finetuned` with diverse data.

## Best Practices
- **Pipeline Monitoring**: Regularly review `monitoring.py` logs for bottlenecks.
- **Data Updates**: Update `mental_health_phrases.csv` to reflect new emotional contexts.
- **Validation**: Use `tests/unit/` to verify each stage.

## Future Enhancements
- **Parallel Processing**: Implement multi-threaded tokenization.
- **Advanced Safety**: Enhance `safety_agent.py` with machine learning for better detection.
- **Cultural Refinement**: Integrate more Omani phrases into the pipeline.

## Acknowledgments
- xAI for Groq LLM support.
- Hugging Face for model frameworks.
- Azure for STT/TTS services.

