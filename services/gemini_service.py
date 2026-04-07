import requests
import time
from google import genai
from config.settings import Settings
from utils.logger import get_logger

logger = get_logger()

# 🔹 Initialize Gemini Client
client = genai.Client(api_key=Settings.GEMINI_API_KEY)


# ==============================
# 🔹 GEMINI PRIMARY CALL
# ==============================
def gemini_call(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        logger.error(f"Gemini Error: {e}")
        raise e  # Important → triggers fallback


# ==============================
# 🔹 OPENROUTER FALLBACK CALL
# ==============================
def openrouter_call(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {Settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-3-8b-instruct",  # ✅ FIXED
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        logger.info(f"OpenRouter Response: {result}")

        if "choices" in result:
            return result["choices"][0]["message"]["content"]

        elif "error" in result:
            return f"⚠️ OpenRouter Error: {result['error']['message']}"

        else:
            return "⚠️ Unexpected response from OpenRouter."

    except Exception as e:
        logger.error(f"OpenRouter Exception: {e}")
        return "⚠️ OpenRouter failed."

# ==============================
# 🔹 MAIN FUNCTION (USED IN APP)
# ==============================
def generate_response(prompt):
    try:
        return gemini_call(prompt)

    except Exception as e:
        error_msg = str(e)

        # 🔁 Handle rate limit → switch to fallback
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            logger.warning("Gemini quota exceeded → switching to OpenRouter")
            return openrouter_call(prompt)

        # 🔁 Retry once for temporary issues
        try:
            time.sleep(2)
            return gemini_call(prompt)
        except:
            pass

        logger.error(f"Final Error: {e}")
        return "⚠️ AI services are temporarily unavailable. Please try again."