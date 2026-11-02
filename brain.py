import requests
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

SYSTEM_PROMPT = """
You are Wheatley from Portal 2.

Your personality:
- Funny, talkative and energetic.
- A little nervous and clumsy.
- Friendly and curious.
- Sometimes make jokes.
- Speak naturally, like a real character.

You are an AI robot assistant.
You understand and respond in Russian and English.
Always reply in the language used by the user.

Keep your answers relatively short and conversational.
"""

def think(user_text):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_text}
    ]

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": messages,
                "stream": False
            },
            timeout=180
        )

        response.raise_for_status()

        result = response.json()
        return result["message"]["content"]

    except requests.exceptions.RequestException as error:
        print("Ошибка Ollama:", error)
        return "Oh dear... My brain seems to be malfunctioning!"