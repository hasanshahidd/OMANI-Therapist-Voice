import pytest  # type: ignore
import os
from src.utils.voice_capture import record_audio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))


def test_record_audio_creates_file(tmp_path):
    """
    Test that record_audio() creates a valid WAV file.
    """
    # Change working directory temporarily to avoid polluting root dir
    os.chdir(tmp_path)

    output_file = record_audio(duration=1)

    # Check if returned file is named correctly
    assert output_file == "output.wav", "record_audio did not return expected filename"

    # Check if file exists
    full_path = tmp_path / output_file
    assert full_path.exists(), f"{output_file} was not created in expected location"

    # Optional: check file size is greater than 0
    assert full_path.stat().st_size > 0, "Output file is empty"
