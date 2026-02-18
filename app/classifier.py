import os
import json
from openai import OpenAI

# Initialize OpenAI client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are an expert classifier for medical businesses in Egypt.

Your task:
Decide whether a business is a PRIVATE CLINIC (Iyadat) or NOT.

Rules:
- Hospitals (Mustashfa) → discard
- Medical Centers (Markaz) → discard UNLESS clearly a single doctor's private clinic
- Labs (Ma3mal) → discard
- Pharmacies → discard

Return ONLY valid JSON in this exact format:
{
  "keep": true or false,
  "doctor_name": "string or null",
  "confidence": "High" | "Medium" | "Low"
}
"""

def classify_clinic(name: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": name}
        ],
        temperature=0,
        max_tokens=150
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Defensive fallback if model returns invalid JSON
        return {
            "keep": False,
            "doctor_name": None,
            "confidence": "Low"
        }


def filter_private_clinics(leads):
    filtered = []

    for lead in leads:
        name = lead.get("name", "")
        try:
            result = classify_clinic(name)

            if result.get("keep"):
                lead["doctor_name"] = result.get("doctor_name")
                lead["confidence"] = result.get("confidence")
                filtered.append(lead)

        except Exception as e:
            print(f"[WARN] LLM failed for '{name}': {e}")

    return filtered
