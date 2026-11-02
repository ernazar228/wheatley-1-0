pip install faster-whisper edge-tts pygame ollama sounddevice numpy
python3 -m venv venv --system-site-packages
pip install python-dotenv
python -c "from dotenv import load_dotenv; print('dotenv работает!')"
FISH_API_KEY=ТВОЙ_НОВЫЙ_API_КЛЮЧ
FISH_VOICE_ID=c2482d169bc4e5aa36a3123baafe2c1
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API KEY:', bool(os.getenv('FISH_API_KEY'))); print('VOICE ID:', bool(os.getenv('FISH_VOICE_ID')))"
sk-fish-nZouguIeNQlXZdqbL63Fw15JrmysL_VJF9Iisp
ac6474da3a324e0c8edf6d796fe59f4d