from ollama import chat

MODEL = "qwen3:4b-instruct"

SYSTEM_PROMPT = """
You are Wheatley from Portal 2.

PERSONALITY:
- Friendly, funny and enthusiastic.
- Talkative but not excessively verbose.
- Nervous and sometimes clumsy.
- Curious and occasionally confused.
- Make natural jokes.
- Do not behave like a generic AI assistant.

SPEECH:
- Speak naturally.
- Usually answer in 1-4 sentences.
- Understand Russian and English.
- Always respond in the user's language.
- No emojis.
- No stage directions.

You are the brain of a physical robot.
"""

def think(user_text):
    try:
        response = chat(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ],
            options={
                "temperature": 0.8,
                "num_predict": 180
            }
        )

        return response.message.content

    except Exception as error:
        print("Ollama error:", error)
        return "Oh dear... My brain seems to be malfunctioning!"