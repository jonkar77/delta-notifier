import requests 
from bs4 import BeautifulSoup

URL = "https://boards-api.greenhouse.io/v1/boards/razorpaysoftwareprivatelimited/jobs?content=true"

def scrape():
    response = requests.get(URL)
    if response.status_code != 200:
        return Exception("❌ Failed to fetch jobs from Razorpay")
    data = response.json()
    # print(data)
    job_data = []   

    for job in data["jobs"]:
        job_data.append({
           'title': job['title'],
           'link': job['absolute_url']
        })

    return job_data

# return job_data

