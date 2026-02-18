import os
import requests
from tenacity import retry, stop_after_attempt, wait_fixed

SERP_API_KEY = os.getenv("SERP_API_KEY")

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def scrape_maps(query: str):
    if not SERP_API_KEY:
        raise RuntimeError("SERP_API_KEY is not set")

    params = {
        "engine": "google_maps",
        "q": query,
        "type": "search",
        "api_key": SERP_API_KEY
    }

    print("[INFO] Querying Google Maps via SerpAPI")

    response = requests.get(
        "https://serpapi.com/search",
        params=params,
        timeout=15
    )
    response.raise_for_status()

    data = response.json()
    results = []

    for place in data.get("local_results", []):
        results.append({
            "name": place.get("title"),
            "phone": place.get("phone"),
            "address": place.get("address"),
            "link": place.get("link")
        })

    return results
