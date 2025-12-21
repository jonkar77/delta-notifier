import requests 
from bs4 import BeautifulSoup
import json
import re

URL = "https://careers.cred.club/openings"


def scrape():
    response = requests.get(URL)
    if response.status_code != 200:
        return Exception("❌ Failed to fetch jobs from CRED")
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', id='__NEXT_DATA__')

        if not script_tag:
            return Exception("❌ Failed to find script tag with id '__NEXT_DATA__'")
        data = script_tag.string
        if not data:
            return Exception("❌ Script tag '__NEXT_DATA__' is empty")
        
        json_data = json.loads(data)
        jobs = json_data['props']['pageProps']['data']['data']
        job_list = []
        for job in jobs:
            job_list.append({
                "title": job['text'],
                "link":  job['urls']['show']
            })
        # print(job_list)
        return job_list
    return []
    