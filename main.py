import requests
from bs4 import BeautifulSoup
import json
import os
import smtplib
import traceback
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv() 

# === Configuration ===
URL = "https://www.angelone.in/careers"  # Replace with the actual URL
STORED_FILE = "job_titles.json"

# Email config (read from environment variables on Render)
EMAIL_FROM = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")  # You can set this to your own email
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def fetch_job_titles():
    response = requests.get(URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        position_div = soup.find('div', class_='position-listing')
        if position_div:
            return [p.get_text(strip=True) for p in position_div.find_all('p', class_='job-title')]
    return []


def load_previous_titles():
    if os.path.exists(STORED_FILE):
        try:
            with open(STORED_FILE, 'r') as f:
                content = f.read().strip()
                if not content:
                    print("📂 job_titles.json is empty. Assuming first run.")
                    return []
                return json.loads(content)
        except json.JSONDecodeError:
            print("❌ Corrupted JSON detected. Starting fresh.")
            return []
    else:
        print("📂 No previous data file found. Assuming first run.")
        return []



def save_titles(titles):
    with open(STORED_FILE, 'w') as f:
        json.dump(titles, f)


def send_email(new_titles):
    body = "⚠️ New job listing(s) detected:\n\n" + "\n".join(new_titles)
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
        traceback.print_exc()  # ← Logs the full stack trace



def main():
    print("📡 Checking job listings...")
    current_titles = fetch_job_titles()
    if not current_titles:
        print("⚠️ No job titles found or page failed to load.")
        return

    # for a in current_titles:
    #     print(a + ",");
    previous_titles = load_previous_titles()
    new_listings = [title for title in current_titles if title not in previous_titles]

    if new_listings:
        print(f"🔔 Detected {len(new_listings)} new job title(s). Sending email...")
        send_email(new_listings)
        save_titles(current_titles)
    else:
        print("✅ No changes detected. No email sent.")


if __name__ == "__main__":
    main()