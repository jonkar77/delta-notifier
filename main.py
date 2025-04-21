import importlib
import os
from core.db import load_previous_jobs, save_jobs
from core.emailer import send_email
import traceback

SCRAPERS = [
    "scrapers.angelone",
]

def run_scraper(module_path):
    scraper = importlib.import_module(module_path)
    source = module_path.split('.')[-1]
    print(f"🔍 Checking jobs from {source}...")
    current_jobs = scraper.scrape()
    previous_jobs = load_previous_jobs(source)
    if not previous_jobs:
        print(f"📝 Initial save for {source}.")
        save_jobs(source, current_jobs)
        return

    new_jobs = [job for job in current_jobs if job not in previous_jobs]
    if new_jobs:
        print(f"📬 {len(new_jobs)} new jobs found for {source}")
        # print(f"📬 {new_jobs}")
        send_email(source, new_jobs)
        save_jobs(source, current_jobs)
    else:
        print(f"✅ No new jobs for {source}")

def main():
    for scraper_path in SCRAPERS:
        try:
            run_scraper(scraper_path)
        except Exception as e:
            print(f"❌ Error running scraper {scraper_path}: {e}")
            traceback.print_exc()


if __name__ == "__main__":
    main()