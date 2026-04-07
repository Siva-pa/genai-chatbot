import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """
    Central configuration class for the chatbot application.
    Handles all environment variables securely.
    """

    # 🔑 API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    # 🤖 Model Config
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    # ⚙️ App Config
    APP_NAME = "AI Career Advisor Chatbot"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # 📝 Logging
    LOG_FILE = "logs/app.log"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # 🚨 Validation (optional but professional)
    @staticmethod
    def validate():
        missing = []

        if not Settings.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")

        if not Settings.OPENROUTER_API_KEY:
            missing.append("OPENROUTER_API_KEY")

        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")