import openai
from decouple import config

openai.api_key = config('openai_key')

file = open("/Users/zhouyou/PycharmProjects/interview_django/recorded_voice/test_audio.mp3", "rb")
transcription = openai.Audio.transcribe("whisper-1", file)

print(transcription.get("text"))

