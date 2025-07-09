     # Project Architecture Overview
     The Omani-Therapist-Voice is a voice-only mental health chatbot designed for Omani Arabic users, built for Elile AI's technical assessment.

     ## Components
     - **Speech Pipeline**: Voice capture (sounddevice), STT (Google Cloud free tier), TTS (Azure free tier).
     - **Multi-Agent System**: Emotion, Therapy, Safety agents for sentiment analysis, CBT responses, and crisis detection.
     - **Cultural Sensitivity**: Omani Arabic embeddings and culturally tailored prompts.
     - **Safety**: HIPAA-compliant logging and crisis protocols.

     ## Status
     - Day 1: Initialized folder structure, voice capture, unit tests, and documentation for long-term runnability.