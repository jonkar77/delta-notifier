import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os
import smtplib
import traceback
from email.mime.text import MIMEText
from dotenv import load_dotenv
from datetime import datetime
load_dotenv() 

# === Configuration ===
URL = "https://www.angelone.in/careers"  

# Connect to MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["job_tracker"]
col = db["jobCollection"]

# Email config (read from environment variables on Render)
EMAIL_FROM = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")  # You can set this to your own email
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# previous_titles_memory = []

def fetch_job_titles():
    response = requests.get(URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        position_div = soup.find('div', class_='position-listing')

        if position_div:
            job_data = []
            # Loop through each job block (assuming titles and links are wrapped in <a>)
            for a_tag in position_div.find_all('a', href=True):
                title_tag = a_tag.find('p', class_='job-title')
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    link = a_tag['href']
                    job_data.append({
                        "title": title,
                        "link": link
                    })
            return job_data

    return []


def load_previous_titles():
    doc = col.find_one({"_id": "latest"})
    if doc:
        print("📥 Loaded previous job data from MongoDB.")
        return doc.get("jobs", [])  # Contains list of {"title", "link"}
    print("🆕 No previous job data found in MongoDB.")
    return []


def save_titles(titles_with_links):
    col.update_one(
        {"_id": "latest"},
        {
            "$set": {
                "jobs": titles_with_links,
                "last_updated": datetime.utcnow().isoformat()
            }
        },
        upsert=True
    )
    print("💾 Saved current job titles + links to MongoDB.")
    

def send_email(new_titles):
    body = "⚠️ New job listing(s) detected:\n\n" + "\n".join(
        f"{title['title']} - {title['link']}" for title in new_titles
    )
    msg = MIMEText(body)
    msg['Subject'] = '🚀 Job Listings Updated!'
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASS)
            server.send_message(msg)
            print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)
        traceback.print_exc()




def main():
    print("📡 Checking job listings...")
    current_titles = fetch_job_titles()
   
    if not current_titles:
        print("⚠️ No job titles found or page failed to load.")
        return

    previous_titles = load_previous_titles()
    
    if not previous_titles:
        print("🆕 First run. Saving titles in-memory.")
        save_titles(current_titles)
        return
    
    new_listings = [title for title in current_titles if title not in previous_titles]

    if new_listings:
        print(f"🔔 Detected {len(new_listings)} new job title(s). Sending email...")
        print(f"🔔 Detected {new_listings} new job(s).")
        send_email(new_listings)
        save_titles(current_titles)
    else:
        print("✅ No changes detected. No email sent.")


if __name__ == "__main__":
    main()