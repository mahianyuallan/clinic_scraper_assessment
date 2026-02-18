import os
import json
import httpx
import asyncio

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

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

async def classify_clinic(name: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": name}
                ],
                "temperature": 0
            },
            timeout=20
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return json.loads(content)

def filter_private_clinics(leads):
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set")

    filtered = []

    for lead in leads:
        name = lead.get("name", "")
        try:
            result = asyncio.run(classify_clinic(name))
            if result.get("keep"):
                lead["doctor_name"] = result.get("doctor_name")
                lead["confidence"] = result.get("confidence")
                filtered.append(lead)
        except Exception as e:
            print(f"[WARN] LLM failed for '{name}': {e}")

    return filtered
