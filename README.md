# Clinic Scraper Microservice

This project is a production-ready microservice that scrapes Google Maps to discover **private medical clinics in Egypt**, filters out hospitals and medical centers using an LLM, and outputs clean, structured leads.

It was built as part of Sofindex's Junior AI Automation Engineer technical assessment.

---

## Features

- Google Maps scraping via SerpAPI
- Automatic retries and timeout handling
- LLM-based filtering for Egyptian medical business types
- Phone number normalization (mobile + landline)
- Clean CSV output
- Fully containerized with Docker

---

## Requirements

You need API keys for:

- **SerpAPI** — Google Maps scraping
- **OpenAI** — LLM filtering 

---

## Setup

Create a `.env` file in the project root:

```env
SERP_API_KEY=your_serpapi_key_here
OPENAI_API_KEY=your_groq_api_key_here

```

---

## Run the Service

Run everything with one command:

```bash
docker-compose up --build
```

The scraper will run with the default query:

```
Dentist in Maadi
```

You can change the query in `docker-compose.yml`, or run manually:

```bash
docker run --env-file .env clinic-scraper \
  python app/main.py --query "Dermatologist in Maadi"
```

---

## Output

The final results are saved to:

```
data/leads.csv
```

### CSV Schema

| Column | Description |
|---|---|
| `clinic_name` | Name of the clinic |
| `doctor_name` | Doctor's name (if available) |
| `phone_number` | Normalized phone number |
| `address` | Clinic address |
| `Maps_link` | Google Maps link |
| `confidence_score` | LLM confidence score |

### Sample Output

| clinic_name | phone_number | address | confidence_score |
|---|---|---|---|
| Dr Ahmed Clinic | +201012345678 | Maadi | High |

---

## Notes

- Hospitals, labs, pharmacies, and corporate medical centers are discarded.
- Ambiguous names are resolved using strict LLM prompting.
- If the LLM fails, the service logs the error and continues processing without crashing.
