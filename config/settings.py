import os

# Try importing streamlit (for cloud secrets)
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False


class Settings:
    """
    Central configuration for the application.
    Supports:
    - Local (.env)
    - AWS EC2
    - Streamlit Cloud (secrets)
    """

    # 🔑 API KEYS
    if STREAMLIT_AVAILABLE:
        GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
        OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY"))
    else:
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    # 🤖 MODEL CONFIG
    GEMINI_MODEL = "gemini-2.0-flash"

    # ⚙️ APP CONFIG
    APP_NAME = "AI Career Advisor Chatbot"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # 📝 LOGGING
    LOG_DIR = "logs"
    LOG_FILE = os.path.join(LOG_DIR, "app.log")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # 🚨 VALIDATION
    @staticmethod
    def validate():
        missing = []

        if not Settings.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")

        # OpenRouter is optional (fallback)
        # if not Settings.OPENROUTER_API_KEY:
        #     missing.append("OPENROUTER_API_KEY")

        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")
