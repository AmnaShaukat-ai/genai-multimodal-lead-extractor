from typing import Literal, Optional
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from datetime import date

load_dotenv()
client = OpenAI()


class Lead(BaseModel):
    intent: Literal["inquiry", "complaint", "support", "other"]
    name: Optional[str]
    budget: Optional[float]
    currency: Optional[str]
    phone: Optional[str]
    urgency: Literal["low", "medium", "high"]


SYSTEM_PROMPT = """You are a lead extraction assistant for MoinSystems, an AI and Software Company.
Read the customer message and extract the fields.
Rules:
- If a detail is not in the message, use null. Never guess.
- intent: "inquiry" = wants information OR wants to buy/build something new
  (even if the thing is a "support chatbot", a new project is an inquiry),
  "complaint" = unhappy about something that already happened,
  "support" = ONLY if they already use a MoinSystems product and need help with it,
  "other" = anything else.
- If the customer is unhappy about something, use "complaint" even if they also ask for a fix.
- budget: use a number only if the message gives an exact or approximate amount.
  If budget is described only in words like "low", "high" or "flexible", use null.
- urgency: count the days from today to the deadline.
  "high" = 3 days or less, or the message says urgent/immediately/quickly,
  "medium" = 4 to 30 days, "low" = more than 30 days or no deadline or no rush.
"""


def extract_lead(message):
    prompt = SYSTEM_PROMPT + f"\nToday's date is {date.today()}."
    response = client.chat.completions.parse(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": message},
        ],
        response_format=Lead,
    )
    return response.choices[0].message.parsed

messages = [
    "Hi, I am Ahmad. I need a customer support chatbot for my company website. Budget is around 10000 AED and we want to launch it till the end of the month.",
    "Your chatbot replied wrong to my customer yesterday and he is unhappy now. So please fix the chatbot quickly.",
    "Hi, I am Fatima from Logistic Company. I want to know about services of your company. No hurry.",
    "Hello, I want a voice assistant for my boutique. My budget is low and I want it within 15 working days.",
     ]

for message in messages:
    lead = extract_lead(message)
    print(lead.model_dump_json(indent=2))