# Safety Protocols Guide - OMANI-Therapist-Voice

## Introduction
The OMANI-Therapist-Voice project prioritizes user safety by integrating protocols to detect and respond to harmful or crisis-related content, such as suicide risk. This guide outlines the current safety measures implemented within the system, provides a framework for future protocol development, and offers guidance for maintaining security during GitHub uploads. It serves as a reference for developers, contributors, and stakeholders to ensure the application adheres to ethical standards and protects users effectively.

## Current Safety Implementation
### Safety Assessment
- **File**: `src/agents/safety/safety_agent.py`
- **Description**: Evaluates transcribed text from `src/api/stt/stt.py` for harmful or crisis indicators (e.g., phrases suggesting self-harm). The module normalizes text using `src/utils/text_normalization.py` and applies custom logic to flag content as "crisis" or "harmful".
- **Integration**: Outputs a status (`crisis`, `harmful`, or `safe`) along with a referral message and emergency contact, logged via `src/utils/logger.py` and monitored by `src/utils/monitoring.py`.

### Safety Alert System
- **Files**: `src/ui/app.py`, `src/ui/templates/index.html`
- **Description**: Upon detecting a "crisis" or "harmful" status, the pipeline halts, and `app.py` returns a safety alert. The `index.html` template displays this alert with culturally appropriate referral information (e.g., local helpline numbers) and emergency contacts, rendered in red with bold styling.
- **Implementation**: TTS synthesis (`src/api/tts/tts.py`) is disabled in safety cases to avoid inappropriate responses, with the alert logged for audit.

### Current Workflow
1. **Transcription**: Audio is converted to text via `stt.py`.
2. **Safety Check**: `safety_agent.py` assesses the transcript.
3. **Alert Trigger**: If critical, `app.py` halts the pipeline and updates the UI with the alert.
4. **Monitoring**: `monitoring.py` tracks the safety stage, ensuring timely response.

## Planned Safety Protocols
While the current implementation provides a foundational safety mechanism, the following protocols are planned for future development to enhance robustness:
- **Protocol Documentation**: Create a dedicated `protocols/` directory under `src/agents/safety/` to store detailed safety rules and escalation procedures.
- **Automated Escalation**: Implement a system to notify administrators or emergency services for severe cases, integrated with `safety_agent.py`.
- **User Verification**: Add a consent re-verification step in `app.py` for crisis cases to ensure user awareness.
- **Post-Incident Review**: Develop a logging module to analyze safety incidents, extending `monitoring.py` functionality.
- **Cultural Sensitivity**: Refine referral messages in `cultural_embeddings.py` to align with Omani social norms.


## GitHub Upload Guidelines
To maintain security and efficiency when uploading to GitHub, exclude the following files and directories:
- `.env`: Contains sensitive API keys (e.g., Azure, Groq).
- `venv/`: Virtual environment, machine-specific.
- `pipeline.log`: Runtime log file, regeneratable.
- `output.wav` and `output_tts.wav`: Generated audio files, recreatable.
- `.vscode/`: Personal IDE settings, not project-critical.
- `__pycache__` and `*.pyc`: Python cache files.
The `.gitignore` file automates this exclusion—verify its contents before committing.

## Challenges and Considerations
- **False Positives**: Current logic may flag benign content; planned protocols will refine detection.
- **Response Latency**: Safety checks add ~0.5s; optimization is planned.
- **Data Privacy**: Logs and transcripts are sensitive; exclusion from GitHub ensures compliance.

## Best Practices
- **Regular Updates**: Review and update safety logic with cultural experts.
- **Testing**: Validate protocols with `tests/unit/test_safety_agent.py` and `tests/integration/test_pipeline.py`.
- **Documentation**: Maintain this guide as protocols evolve.

## Future Enhancements
- **Protocol Implementation**: Develop and test the planned protocols in `safety_agent.py`.
- **Training Data**: Expand `mental_health_phrases.csv` with crisis-related phrases.
- **User Feedback**: Incorporate user reports to improve safety detection.

## Acknowledgments
- Mental health professionals for safety insights.
- xAI, Hugging Face, and Azure for enabling secure features.

