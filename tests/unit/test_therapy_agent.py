import pytest
from src.agents.therapy.therapy_agent import generate_therapy_response

def test_generate_therapy_response():
    transcript = "أحتاج إلى المساعدة، وأريد أن أعيش معك"
    emotion = "sadness"
    response = generate_therapy_response(transcript, emotion)
    assert isinstance(response, str)
    assert len(response) > 0
    assert "حزن" in response  # Check for context relevance
