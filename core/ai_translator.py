"""
Module: ai_translator.py
Purpose: Converts detected ASL gloss words into natural English via Groq API.
"""
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# FIX: Do NOT initialize Groq client at module level — it raises an AuthenticationError
# if GROQ_API_KEY is missing/placeholder. Build it lazily inside the function.
_client = None

def _get_client():
    """Lazily create the Groq client so missing keys don't crash at import time."""
    global _client
    if _client is None:
        api_key = os.environ.get("GROQ_API_KEY", "")
        if not api_key or api_key == "YOUR_GROQ_API_KEY":
            return None
        try:
            from groq import Groq
            _client = Groq(api_key=api_key)
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            return None
    return _client


def generate_sentence(words: list) -> str:
    """
    Convert detected ASL gloss words into natural, grammatically correct English.
    Falls back to joining words with spaces if Groq is unavailable.
    """
    if not words:
        return ""

    # If the input is already a sentence (from chat), return as-is
    if len(words) == 1 and len(words[0].split()) > 3:
        return words[0]

    gloss_text = " ".join(str(w) for w in words)

    client = _get_client()
    if client is None:
        logger.warning("Groq client unavailable — returning raw gloss text.")
        return gloss_text

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an ASL translation assistant. Convert detected ASL gloss words "
                        "into natural, grammatically correct English sentences. "
                        "Rules: Keep meaning accurate. Keep responses short and natural. "
                        "Do not add extra information. Fix grammar automatically. "
                        "Return ONLY the final sentence."
                    )
                },
                {
                    "role": "user",
                    "content": f"Detected words: {gloss_text}\nConvert into a natural English sentence."
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Groq API Error: {e}")
        return gloss_text


if __name__ == "__main__":
    test_words = ["i", "want", "water"]
    print(f"Gloss: {test_words}")
    print(f"Sentence: {generate_sentence(test_words)}")
