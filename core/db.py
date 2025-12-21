from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    raise ValueError("❌ MONGO_URL not found in environment variables.")

client = MongoClient(MONGO_URL)
try:
    client.admin.command('ping')
    print("✅ Connected to MongoDB successfully")
except Exception as e:
    raise ConnectionError(f"❌ Could not connect to MongoDB: {e}")

db = client["job_tracker"]
col = db["jobCollection"]  # Use the single collection

def load_previous_jobs(source):
    try:
        doc = col.find_one({"_id": "latest"})
        if not doc:
            print(f"🆕 First time running any scraper. No document found.")
            return []

        if "jobs" not in doc or source not in doc["jobs"]:
            print(f"🆕 First time running scraper for '{source}'. No jobs found for this source.")
            return []

        return doc["jobs"][source]
    except Exception as e:
        print(f"❌ Error loading previous jobs for {source}: {e}")
        return []


def save_jobs(source, jobs):
    # Update just the part of 'jobs' belonging to this source
    col.update_one(
        {"_id": "latest"},
        {
            "$set": {
                f"jobs.{source}": jobs,
                f"last_updated.{source}": datetime.utcnow().isoformat()
            }
        },
        upsert=True
    )
