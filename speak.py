from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI()

text = "Hello, Amna! Thankyou for contacting MoinSystems AI. Our support team will call you with two working days"

speech_file = Path("reply.mp3")

with client.audio.speech.with_streaming_response.create(
    model = "gpt-4o-mini-tts", 
    voice = "coral",
    input = text,
    instructions = "Speak in a warm, Professional tone.",
) as response:
    response.stream_to_file(speech_file)


print("Saved reply mp3.")