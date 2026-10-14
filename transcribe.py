from dotenv import load_dotenv
from openai import OpenAI



load_dotenv()
client = OpenAI()

with open("bot_testing.m4a", "rb") as audio_file:
    result = client.audio.transcriptions.create(
        model = "whisper-1",
        file = audio_file
    )


    print(result.text)