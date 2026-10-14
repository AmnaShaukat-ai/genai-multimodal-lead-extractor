# Voice and Image Lead Extractor (Multimodal AI PoC)

A small proof of concept built in Round 7 (Generative AI) of my AI Engineer internship.

It takes a customer voice note or a screenshot of an inquiry, extracts a structured lead, and replies with a spoken message.

## How it works
1. Audio goes to Whisper (speech-to-text). Images go straight to GPT-4o (vision).
2. GPT-4o returns a validated lead as JSON (intent, name, phone, budget, currency, urgency) using Pydantic.
3. Python builds a short reply.
4. gpt-4o-mini-tts turns the reply into `reply.mp3`.

## Run it
1. `pip install -r requirements.txt`
2. Create a `.env` file with `OPENAI_API_KEY=your-key`
3. In `poc.py`, set `INPUT_FILE` to an audio file or `inquiry.png`
4. `python poc.py`

## Limitations
Tested on a small sample (4 emails, 1 voice note, 1 screenshot). Results are indicative, not final.