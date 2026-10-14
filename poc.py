import base64
from datetime import date
from pathlib import Path
from typing import Literal, Optional
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()
client = OpenAI()


class Lead(BaseModel):
    intent: Literal["inquiry", "support", "complaint", "other"]
    name: Optional[str]
    phone: Optional[str]
    budget: Optional[float]
    currency: Optional[str]
    urgency: Literal["low", "medium", "high"]


SYSTEM_PROMPT = """You are a Lead Extraction Assistant for MoinSystems, an AI and Software Company.
Rules:
- If a detail is not present in the message, use null. Never guess.
- intent: "inquiry" = wants information OR wants to buy/build something new
  (even if the thing is a "support chatbot", a new project is an inquiry),
  "complaint" = unhappy about something that has already happened,
  "support" = ONLY if they already use a MoinSystems product and need help with it,
  "other" = anything else.
- If the customer is unhappy about something, use "complaint" even if they also ask for a fix.
- budget: use a number only if the message gives an exact or approximate amount.
  If budget is described only in words like "low", "high" or "flexible", use null.
- urgency: count the days from today to the deadline.
  "high" = 3 days or less, or the message says urgent/quickly/immediately,
  "medium" = 4 to 30 days, "low" = more than 30 days or no deadline or no rush.
- currency: always use the 3-letter ISO code (for example AED, PKR, USD), never the word "Dirham" or "Rupees".
"""


def transcribe(path):
    with open(path, "rb") as f:
        result = client.audio.transcriptions.create(model="whisper-1", file=f)
    return result.text


def image_to_data_url(path):
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def extract_lead(content):
    prompt = SYSTEM_PROMPT + f"\nToday's date is {date.today()}."
    response = client.chat.completions.parse(
        model="gpt-4o",
        temperature=0,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content},
        ],
        response_format=Lead,
    )
    return response.choices[0].message.parsed


def build_reply(lead):
    name = lead.name or "there"
    if lead.intent == "complaint":
        return f"Hello {name}, we are sorry about your experience. Our team will contact you as soon as possible to fix this."
    when = "today" if lead.urgency == "high" else "within one working day"
    return f"Hello {name}, thank you for contacting MoinSystems. Our team will call you {when} to discuss your request."


def speak(text, out_file):
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=text,
        instructions="Speak in a warm, professional tone.",
    ) as response:
        response.stream_to_file(Path(out_file))


# ---- Main flow ----
INPUT_FILE = "bot_testing.m4a"   # change to "inquiry.png" for the image test

suffix = Path(INPUT_FILE).suffix.lower()

if suffix in [".m4a", ".mp3", ".wav"]:
    text = transcribe(INPUT_FILE)
    print("Transcript:", text)
    lead = extract_lead(text)
elif suffix == ".png":
    content = [
        {"type": "text", "text": "Extract the lead from this image."},
        {"type": "image_url", "image_url": {"url": image_to_data_url(INPUT_FILE)}},
    ]
    lead = extract_lead(content)
else:
    raise ValueError("Use an audio file (.m4a/.mp3/.wav) or a .png image")

print(lead.model_dump_json(indent=2))

reply = build_reply(lead)
print("Reply:", reply)
speak(reply, "reply.mp3")
print("Saved reply.mp3")