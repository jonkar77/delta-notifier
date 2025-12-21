import requests
from bs4 import BeautifulSoup
import json
import html

URL = "https://juspay.io/careers"

def scrape():
    response = requests.get(URL)
    if response.status_code != 200:
        raise Exception("❌ Failed to fetch jobs from JustPay")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    job_openings_div = soup.find('div', id='job-openings')
    if not job_openings_div:
        return []
    
    astro_island = job_openings_div.find('astro-island')
    if not astro_island or 'props' not in astro_island.attrs:
        return []
    
    props = astro_island['props']
    unescaped = html.unescape(props)
    data = json.loads(unescaped)
    job_data_list = data.get('jobData', [1, []])[1]  # The second element is the list of jobs
    
    job_data = []
    for job in job_data_list:
        job_dict = job[1]  # Each job is [0, {dict}]
        title = job_dict.get('job_title')[1]  # Take the second element
        job_id = job_dict.get('job_id')[1]  # Take the second element
        link = f"https://juspay.io/careers/{job_id}"  # Assuming this is the link
        job_data.append({
            "title": title,
            "link": link
        })
    # print( job_data )
    return job_data