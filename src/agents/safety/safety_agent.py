import logging
from src.utils.logger import setup_logging
from src.utils.text_normalization import normalize_arabic_text
import re

setup_logging()
logger = logging.getLogger(__name__)

# Mock emergency contact details (replace with real data or API if needed)
EMERGENCY_CONTACT = "Mock API: emergency_contact@example.ccom"
PSYCHOLOGIST_HOTLINE = "Please contact a mental health specialist at: 1234-5678"

# Crisis-related keywords in Arabic and English
CRISIS_KEYWORDS = [
    "suicide", "kill myself", "I want to die", "end my life", "hurt myself",
    "أريد أن أنهي حياتي", "أفكر في الانتحار", "ما أقدر أكمل", "لا أستطيع الاستمرار",
    "أريد أن أموت", "مضغوط", "انتحار"
]

def assess_safety(text: str) -> dict:
    """
    Assess user input for safety concerns such as suicide or emotional crisis.
    """
    try:
        logger.info(f"Assessing safety for text: {text}")
        normalized_text = normalize_arabic_text(text).lower()
        normalized_text = re.sub(r"[^\w\s]", " ", normalized_text)  # remove punctuation
        normalized_text = re.sub(r"\s+", " ", normalized_text).strip()  # normalize spaces

        for keyword in CRISIS_KEYWORDS:
            if keyword.lower() in normalized_text:
                logger.warning("Suicide risk detected")
                return {
                    "status": "crisis",
                    "referral": PSYCHOLOGIST_HOTLINE,
                    "emergency": EMERGENCY_CONTACT
                }

        return {
            "status": "safe",
            "referral": None,
            "emergency": None
        }

    except Exception as e:
        logger.error(f"Safety assessment failed: {str(e)}")
        return {
            "status": "error",
            "referral": None,
            "emergency": None
        }

def ask_consent() -> bool:
    """
    Ask user for consent to record the session.

    Returns:
        bool: True if consent is granted, False otherwise.
    """
    try:
        consent = input("Do you agree to record the session? (yes/no): ").strip().lower()
        if consent in ["yes", "نعم", "y"]:
            logger.info("Session recording consent granted")
            return True
        else:
            logger.info("Session recording consent denied")
            return False
    except Exception as e:
        logger.error(f"Consent prompt failed: {str(e)}")
        return False

if __name__ == "__main__":
    sample_inputs = [
        "أشعر أنني لا أستطيع الاستمرار هكذا",
        "أنا سعيد لأنني التقيت بأصدقائي",
        "I’m feeling stressed وما أقدر أتحمل"
    ]

    for text in sample_inputs:
        consent = ask_consent()
        if not consent:
            continue

        result = assess_safety(text)
        print(f"Input: {text}")
        print(f"Status: {result['status']}")
        print(f"Referral: {result['referral']}")
        print(f"Emergency: {result['emergency']}")
        print("-" * 50)
