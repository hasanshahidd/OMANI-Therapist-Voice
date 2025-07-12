import logging
import os
import sys

def setup_logging():
    # Ensure console uses UTF-8 encoding for Arabic
    if sys.platform.startswith('win'):
        sys.stdout.reconfigure(encoding='utf-8')
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(
                r"C:\Users\Admin\Desktop\OMANI-Therapist-Voice\pipeline.log", 
                encoding='utf-8'
            ),
            logging.StreamHandler(sys.stdout)
        ],
        force=True
    )
