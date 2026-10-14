import base64
from datetime import date
from typing import Literal, Optional
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel 


load_dotenv()
client = OpenAI()


class Lead(BaseModel):
    intent : Literal["inquiry", "support", "complaint", "other"]
    name : Optional[str]
    phone : Optional[str]
    budget : Optional[float]
    currency : Optional[str]
    urgency : Literal["low", "medium", "high"]


SYSTEM_PROMPT = """ You are a Lead Extraction Assistant for MoinSystems, an AI and Software Company.
Rules: 
- If a detail is not present in a message use NULL, never guess.
- intent : "inquiry" = want information or want to buy/build something
new(even if a thing is a "support chatbot", a new project is an inquiry), 
"compalint" = unhappy about something that has already happened,
"support" = ONLY if they already use a MoinSystems product and need help with it, 
"other" = anything else.

-If the customer is unhappy about something, use "complaint" even if they also ask for fix.
- budget: use a number only if the message gives an exact or approximate amount.
If budget is described only in words like "low", "high", or "flexible" use null.
- urgency: count the days from today to the deadline.
"high" = 3 or less, or the message says urgent/quickly/immediately.
"medium" = 4 to 30 days, "low" = more than 30 days or no deadline or no rush.
 """



def image_to_data_url(path):
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def extract_lead_from_image(path):
    prompt = SYSTEM_PROMPT + f"\nToday's date is {date.today()}."
    response = client.chat.completions.parse(
        model = "gpt-4o",
        temperature = 0, 
        messages = [
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract the lead from this image."},
                    {"type": "image_url", "image_url": {"url": image_to_data_url(path)}},
                ],
            },
        ],
        response_format= Lead,
    )
    return response.choices[0].message.parsed


lead = extract_lead_from_image("inquiry.png")
print(lead.model_dump_json(indent = 2))
