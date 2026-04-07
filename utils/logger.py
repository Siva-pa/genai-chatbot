import logging
import os

def get_logger():
    # ✅ Ensure logs folder exists
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("chatbot")
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers (important for Streamlit reruns)
    if not logger.handlers:
        handler = logging.FileHandler("logs/app.log")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
