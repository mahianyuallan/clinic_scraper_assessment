import argparse
from scraper import scrape_maps
from classifier import filter_private_clinics
from normalizer import normalize_leads

def main():
    parser = argparse.ArgumentParser(
        description="Clinic Scraper Microservice"
    )
    parser.add_argument(
        "--query",
        required=True,
        help="Search query, e.g. 'Dentist in Maadi'"
    )

    args = parser.parse_args()

    print(f"[INFO] Starting scraper for query: {args.query}")

    raw_results = scrape_maps(args.query)
    print(f"[INFO] Scraped {len(raw_results)} raw results")

    filtered_results = filter_private_clinics(raw_results)
    print(f"[INFO] {len(filtered_results)} results after AI filtering")

    final_leads = normalize_leads(filtered_results)
    print(f"[SUCCESS] Saved {len(final_leads)} leads to data/leads.csv")

if __name__ == "__main__":
    main()
