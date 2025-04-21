import smtplib
from email.mime.text import MIMEText
import os
import traceback

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(source, new_jobs):
    if not new_jobs:
        return
    body = f"⚠️ New job listings from {source}:\n\n" + "\n".join(
        f"{job['title']} - {job['link']}" for job in new_jobs
    )
    msg = MIMEText(body)
    msg["Subject"] = f"🚀 {source} Job Listings Updated!"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = os.getenv("EMAIL_TO")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_USER"), os.   getenv("EMAIL_PASS"))
            server.send_message(msg)
    except Exception as e:
        print("❌ Failed to send email:", e)
        traceback.print_exc()
