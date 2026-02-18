import pandas as pd
import re
from typing import List, Dict

def normalize_phone(phone: str | None):
    if not phone:
        return None

    digits = re.sub(r"\D", "", phone)

    # Mobile numbers (01xxxxxxxxx)
    if digits.startswith("01") and len(digits) == 11:
        return f"+20{digits[1:]}"

    # Already international
    if digits.startswith("201") and len(digits) == 12:
        return f"+{digits}"

    # Landlines (02...) are allowed but kept as-is
    if digits.startswith("02"):
        return digits

    return None


def normalize_leads(leads: List[Dict]):
    rows = []

    for lead in leads:
        rows.append({
            "clinic_name": lead.get("name"),
            "doctor_name": lead.get("doctor_name"),
            "phone_number": normalize_phone(lead.get("phone")),
            "address": lead.get("address"),
            "Maps_link": lead.get("link"),
            "confidence_score": lead.get("confidence", "Medium")
        })

    df = pd.DataFrame(rows)

    # Ensure output directory exists
    df.to_csv("data/leads.csv", index=False)

    return rows
