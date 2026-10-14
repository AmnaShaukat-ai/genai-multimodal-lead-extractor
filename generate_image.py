import base64
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
client = OpenAI()

prompt = (
    "A clean, modern flat-style poster for an AI chatbot company. "
    "A friendly blue robot assistant on the left, a laptop showing a chat window "
    "on the right, white background, plenty of empty space at the top for a title. "
    "No text in the image.")


result = client.images.generate(
    model = "gpt-image-2",
    prompt = prompt, 
    size = "1024x1024"
)

image_bytes = base64.b64decode(result.data[0].b64_json)

with open("ali_poster.png", "wb") as f:
    f.write(image_bytes)

print("Saved ali_poster.png")