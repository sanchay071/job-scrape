
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pprint
from playwright.sync_api import sync_playwright #From the sync_api module inside the playwright library, import the sync_playwright function
# This script is designed to scrape job listings from Glassdoor for Business Analyst positions in the United States.

def extract():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) #p is the instance of playwright, p.chromium is browser type, p.chromium.launch() launches the browser in headless mode
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        page = context.new_page() # Create a new page in the browser context
        page.goto("https://www.glassdoor.com/Job/united-states-business-analyst-jobs-SRCH_IL.0,13_IN1_KO14,30.htm?sortBy=date_desc")
    
        # Wait for the specific element to load
        page.wait_for_selector("div.jobCard")
        
        
        html = page.content()
        browser.close()
        return html

# if __name__ == "__main__":
#     html = extract()
#     print(html[:1000])   

def transform(html):
    soup = BeautifulSoup(html, "html.parser")
    job_list = soup.find_all("div", {"class" : "jobCard"}) # Find all divs with class jobContainer
    # pprint.pprint(job_list)
    # print(html[:1000])
    return job_list
    
html = extract()
transform(html)
    
html = extract()
job_list = transform(html)

job_listings = []

for job in job_list:
    job_posting = {}
    
    try:
        job_posting['company'] = job.find("span", {"class": "EmployerProfile_compactEmployerName__9MGcV"}).text.strip()
    except:
        job_posting['company'] = None
    try:
        job_title_element = job.find("a", {"class": "JobCard_jobTitle__GLyJ1"})
        job_posting['title'] = job_title_element.text.strip()
        job_posting['link'] = job_title_element['href']  # Extract the href attribute
    except:
        job_posting['title'] = None
        job_posting['link'] = None
    try:
        job_posting['location'] = job.find("div", {"JobCard_location__Ds1fM"}).text.strip()
    except:
        job_posting['location'] = None
    
    job_listings.append(job_posting)
    
pprint.pprint(job_listings)


def load():
    
    pass