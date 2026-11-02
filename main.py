
import os
import requests
import pygame

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FISH_API_KEY")
VOICE_ID = os.getenv("FISH_VOICE_ID")

API_URL = "https://api.fish.audio/v1/tts"


def speak(text):

    print("\nWheatley is speaking...")

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

    try:
        response = requests.post(
            "https://api.fish.audio/v1/tts",
            headers=headers,
            json=data,
            timeout=120
        )

        print("HTTP:", response.status_code)

        if response.status_code != 200:
            print("Fish Audio сообщает:", response.text)
            return

        with open("wheatley.mp3", "wb") as file:
            file.write(response.content)

        pygame.mixer.init()
        pygame.mixer.music.load("wheatley.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(20)

        pygame.mixer.quit()

        print("Wheatley voice works!")

    except Exception as error:
        print("Ошибка:", error)


if __name__ == "__main__":

    speak("Привет! Я Уитли! Рад тебя слышать!")

    speak("Hello! I'm Wheatley! Nice to meet you!")
