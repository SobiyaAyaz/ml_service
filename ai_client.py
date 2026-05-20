import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def call_ai(prompt: str) -> dict:
    response = model.generate_content(prompt)
    raw = response.text.strip()
    # Strip markdown code blocks if Gemini wraps in ```json
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)