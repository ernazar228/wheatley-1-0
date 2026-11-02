
import time
import asyncio
import tempfile
import os

import numpy as np
import sounddevice as sd
import pygame
import ollama
import edge_tts

from faster_whisper import WhisperModel


# ==========================================
# WHEATLEY AI 2.0 — CONFIGURATION
# ==========================================

MODEL = "qwen3:1.7b"

WHISPER_MODEL = "tiny"

SAMPLE_RATE = 16000
CHANNELS = 1

SILENCE_LIMIT = 1.2
MAX_RECORD_TIME = 12

VOICE = "ru-RU-DmitryNeural"

SYSTEM_PROMPT = """
Ты — Уитли, искусственный интеллект из Portal 2.

Ты общаешься на русском языке.
У тебя характер немного нервного, смешного,
болтливого и иногда неуверенного робота.

Ты дружелюбный, любопытный и эмоциональный.
Иногда шутишь и можешь немного паниковать.

Отвечай естественно, как живой собеседник.
Не используй длинные ответы без необходимости.
Не описывай свои действия в скобках.
Ты — Уитли, а не ChatGPT.
"""


# ==========================================
# INITIALIZATION
# ==========================================

print("Загрузка Wheatley AI...")

pygame.mixer.init()

print("Загрузка Whisper...")

whisper = WhisperModel(
    WHISPER_MODEL,
    device="cpu",
    compute_type="int8"
)

print("Проверка Ollama...")

ollama.list()

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

print("Wheatley готов!")


# ==========================================
# MICROPHONE
# ==========================================

def listen():

    print("\n[WHEATLEY] Слушаю...")

    frames = []
    recording = False
    silence_time = 0
    elapsed = 0

    chunk_duration = 0.2
    chunk_size = int(SAMPLE_RATE * chunk_duration)

    threshold = 0.015

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="float32",
            blocksize=chunk_size
        ) as stream:

            while True:

                audio, overflowed = stream.read(chunk_size)

                volume = np.sqrt(np.mean(audio ** 2))

                if volume > threshold:

                    recording = True
                    silence_time = 0

                if recording:

                    frames.append(audio.copy())
                    elapsed += chunk_duration

                    if volume < threshold:
                        silence_time += chunk_duration
                    else:
                        silence_time = 0

                    if silence_time >= SILENCE_LIMIT:
                        break

                    if elapsed >= MAX_RECORD_TIME:
                        break

    except Exception as error:
        print("Ошибка микрофона:", error)
        return None

    if not frames:
        return None

    audio_data = np.concatenate(frames).flatten()

    print("[WHEATLEY] Распознаю речь...")

    segments, info = whisper.transcribe(
        audio_data,
        language="ru",
        beam_size=1,
        vad_filter=True
    )

    text = " ".join(
        segment.text.strip()
        for segment in segments
    ).strip()

    return text if text else None


# ==========================================
# AI BRAIN
# ==========================================

def think(user_text):

    print("\nТы:", user_text)
    print("[WHEATLEY] Думаю...")

    messages.append({
        "role": "user",
        "content": user_text
    })

    try:

        response = ollama.chat(
            model=MODEL,
            messages=messages,
            options={
                "temperature": 0.8,
                "num_predict": 150
            }
        )

        answer = response["message"]["content"]

        messages.append({
            "role": "assistant",
            "content": answer
        })

        # Ограничиваем историю диалога
        if len(messages) > 13:
            messages.pop(1)
            messages.pop(1)

        return answer

    except Exception as error:

        print("Ошибка Ollama:", error)

        return "Ой! Кажется, у меня небольшая техническая проблема."


# ==========================================
# SPEECH OUTPUT
# ==========================================

async def generate_voice(text, filename):

    communicator = edge_tts.Communicate(
        text,
        VOICE
    )

    await communicator.save(filename)


def speak(text):

    print("\nWheatley:", text)

    filename = tempfile.mktemp(suffix=".mp3")

    try:

        asyncio.run(generate_voice(text, filename))

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()

    except Exception as error:

        print("Ошибка озвучивания:", error)

    finally:

        if os.path.exists(filename):
            os.remove(filename)


# ==========================================
# MAIN LOOP
# ==========================================

def main():

    print("\n================================")
    print("       WHEATLEY AI 2.0")
    print("================================")
    print("Голосовое управление активно.")
    print("Скажи что-нибудь!")
    print("Для выхода нажми CTRL+C.")
    
    try:

        while True:

            user_text = listen()

            if not user_text:
                continue

            if user_text.lower() in [
                "выход",
                "пока уитли",
                "отключись"
            ]:

                speak("Ладно, увидимся! Надеюсь, ничего не взорвётся.")
                break

            answer = think(user_text)

            speak(answer)

    except KeyboardInterrupt:

        print("\nWheatley выключается...")

    finally:

        pygame.mixer.quit()


if __name__ == "__main__":
    main()
