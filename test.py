import os
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()  # <- this reads your .env file

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = "meta-llama/llama-3.3-70b-instruct:free"

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found! Make sure it is set in your .env file.")

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": "Hello"}]
    }
)

print(response.json())
