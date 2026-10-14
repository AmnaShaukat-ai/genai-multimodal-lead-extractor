from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages = [{"role": "user",
                "content": "Say Hello to MoinSystems in one Sentence"}]
)


print(response.choices[0].message.content)