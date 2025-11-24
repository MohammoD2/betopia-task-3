import os
import requests
import json
from dotenv import load_dotenv

# Load .env file
load_dotenv()  # <- this reads your .env file

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = "meta-llama/llama-3.3-70b-instruct:free"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

class OutreachGenerator:
    def __init__(self, api_key=OPENROUTER_API_KEY, model=OPENROUTER_MODEL):
        self.api_key = api_key
        self.model = model

    # ----------- 1. Build prompt with tone and structured output -----------
    def build_prompt(self, company, persona, product, tone="Formal"):
        return f"""
You are an expert AI Outreach Generator.

### COMPANY PROFILE:
{company}

### PERSONA PROFILE:
{persona}

### PRODUCT DESCRIPTION:
{product}

### REQUIREMENTS:
- Tone: {tone} (Formal / Friendly / Short / Long)
- Highly personalized email
- Include 1 strong CTA
- Explain why the prospect is a strong match in 3 bullet points
- Return output in JSON format:

JSON FORMAT:
{{
  "email": "<personalized outreach email>",
  "why_this_match_works": ["Reason 1", "Reason 2", "Reason 3"]
}}
"""

    # ----------- 2. API Call -----------
    def call_openrouter(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(
            url=OPENROUTER_URL,
            headers=headers,
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            # Attempt to parse JSON if returned correctly
            try:
                return json.loads(content)
            except:
                # fallback: return as text
                return {"email": content, "why_this_match_works": []}
        else:
            return {"email": f"Error: {response.status_code} | {response.text}",
                    "why_this_match_works": []}

    # ----------- 3. Generate Outreach -----------
    def generate_outreach(self, company, persona, product, tone="Formal"):
        prompt = self.build_prompt(company, persona, product, tone)
        return self.call_openrouter(prompt)


# ------------------- USAGE EXAMPLE -------------------
if __name__ == "__main__":
    generator = OutreachGenerator()

    company = """
Company: AcmeHR
Industry: HR Tech
Size: 150 employees
Challenge: Slow hiring process, manual onboarding
Website: acmesolutions.com
"""

    persona = """
Name: Sarah Gomez
Role: HR Director
Responsibilities: Talent acquisition, onboarding, HR automation
Pain points: long hiring cycles, employee dropout
"""

    product = """
Product: AllOfTech AI HR Suite
Features: Automated screening, onboarding workflow, analytics
Value: reduces time-to-hire by 60%
"""

    # You can change tone to "Friendly", "Short", "Long"
    result = generator.generate_outreach(company, persona, product, tone="Friendly")

    print("\n--- Generated Outreach Email ---\n")
    print(result["email"])
    print("\n--- Why This Match Works ---\n")
    for reason in result["why_this_match_works"]:
        print("-", reason)
