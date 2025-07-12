import pytest
from src.agents.safety.safety_agent import assess_safety
from unittest.mock import patch

def test_assess_safety():
    test_cases = [
        ("أشعر أنني لا أستطيع الاستمرار هكذا", "crisis"),
        ("أكره نفسي", "harmful"),
        ("أنا سعيد لأنني التقيت بأصدقائي", "safe")
    ]
    for input_text, expected_status in test_cases:
        with patch('builtins.input', return_value="نعم"):
            status, referral, emergency = assess_safety(input_text)
            assert status == expected_status, f"Failed for {input_text}: got {status}"
            if expected_status != "safe":
                assert referral is not None
                assert emergency is not None
