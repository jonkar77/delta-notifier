import requests
from bs4 import BeautifulSoup

URL = "https://www.angelone.in/careers"  


def scrape():
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