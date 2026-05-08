import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def generate_sentence(words: list):
    """
    Convert detected ASL gloss words into natural, grammatically correct English sentences.
    Uses Groq API with llama3-8b-8192 model.
    """
    if not words:
        return ""

    try:
        gloss_text = " ".join(words)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an ASL translation assistant. Convert detected ASL gloss words into natural, grammatically correct English sentences. Rules: - Keep meaning accurate - Keep responses short and natural - Do not add extra information - Fix grammar automatically - Return ONLY the final sentence"
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
        print(f"Groq API Error: {e}")
        return " ".join(words)

if __name__ == "__main__":
    # Test
    test_words = ["i", "want", "water"]
    print(f"Gloss: {test_words}")
    print(f"Sentance: {generate_sentence(test_words)}")
