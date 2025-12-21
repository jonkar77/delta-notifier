import requests 
from bs4 import BeautifulSoup

URL = "https://careers.cred.club/openings"


def scrape():
    response = requests.get(URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        job_listings = soup.find_all('div', class_='job-listing')
        for job in job_listings:
            title = job.find('h3').text.strip()
            location = job.find('span', class_='location').text.strip()
            print(f"Title: {title}\nLocation: {location}\n")
    else:
        print("Failed to retrieve the webpage.")
