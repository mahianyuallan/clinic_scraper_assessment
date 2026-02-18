import os
import json
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=GEMINI_API_KEY)

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

def classify_clinic(name: str) -> dict:
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[
                SYSTEM_PROMPT,
                f"Business name: {name}"
            ],
            generation_config={
                "temperature": 0,
                "max_output_tokens": 150
            }
        )

        text = response.text.strip()

        # Defensive JSON parsing
        return json.loads(text)

    except Exception as e:
        print(f"[WARN] LLM failed for '{name}': {e}")
        return {
            "keep": False,
            "doctor_name": None,
            "confidence": "Low"
        }


def filter_private_clinics(leads):
    filtered = []

    for lead in leads:
        name = lead.get("name", "")
        result = classify_clinic(name)

        if result.get("keep"):
            lead["doctor_name"] = result.get("doctor_name")
            lead["confidence"] = result.get("confidence")
            filtered.append(lead)

    return filtered
