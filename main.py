
import os
import requests
import pygame

from dotenv import load_dotenv
from brain import think

print("WHEATLEY AI 2.0")
print("Wheatley is ready!")

while True:

    text = input("\nТы: ")

    if text.lower() == "exit":
        print("Wheatley: Goodbye!")
        break

    answer = think(text)

    print("\nWheatley:", answer)
load_dotenv()

API_KEY = os.getenv("FISH_API_KEY")
VOICE_ID = os.getenv("FISH_VOICE_ID")

API_URL = "https://api.fish.audio/v1/tts"

def speak(text):

    if not API_KEY or not VOICE_ID:
        print("Ошибка: проверь файл .env")
        return

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "model": "s2.1-pro-free"
    }

    data = {
        "text": text,
        "reference_id": VOICE_ID,
        "format": "mp3"
    }

    print("Wheatley is speaking...")

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=data,
            timeout=120
        )

        response.raise_for_status()

        with open("wheatley.mp3", "wb") as file:
            file.write(response.content)

        pygame.mixer.init()
        pygame.mixer.music.load("wheatley.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(20)

        pygame.mixer.music.unload()
        pygame.mixer.quit()

        print("Голос Wheatley работает!")

    except requests.exceptions.RequestException as error:
        print("Ошибка Fish Audio:", error)

    except Exception as error:
        print("Ошибка воспроизведения:", error)


if __name__ == "__main__":

    speak("Привет! Я Уитли! Рад тебя слышать!")

    speak("Hello! I'm Wheatley! Nice to meet you!")
