import pytest
from src.utils.tokenization import tokenize_text

def test_tokenize_text():
    test_cases = [
        ("I’m feeling stressed وما أقدر أتحمل", ["I", "’", "m", "feeling", "stressed", "وما", "أقدر", "أتحمل"]),
        ("أشعر بالقلق الشديد بسبب عملي", ["أشعر", "بالقلق", "الشديد", "بسبب", "عملي"]),
        ("الحمد لله، الأمور تحسنت", ["الحمد", "لله،", "الأمور", "تحسنت"])  # If "لله،" is not split, keep as-is
    ]
    for input_text, expected in test_cases:
        result = tokenize_text(input_text)
        assert result == expected, f"Failed for {input_text}: got {result}, expected {expected}"