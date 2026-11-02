import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FISH_API_KEY")
VOICE_ID = os.getenv("FISH_TEST_VOICE_ID")

if not API_KEY or not VOICE_ID:
    raise ValueError("Проверь FISH_API_KEY и FISH_TEST_VOICE_ID в .env")

url = "https://api.fish.audio/v1/tts"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "model": "s2.1-pro-free"
}

data = {
    "text": "Hello! I am Wheatley. Testing my new voice!",
    "reference_id": VOICE_ID,
    "format": "mp3"
}

print("Wheatley is generating speech...")

response = requests.post(
    url,
    headers=headers,
    json=data,
    timeout=120
)

if response.status_code == 200:
    with open("test_fish.mp3", "wb") as file:
        file.write(response.content)

    print("Audio successfully saved!")
else:
    print("HTTP Error:", response.status_code)
    print("Details:", response.text)