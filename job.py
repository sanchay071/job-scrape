
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pprint
from playwright.sync_api import sync_playwright
# This script is designed to scrape job listings from Glassdoor for Business Analyst positions in the United States.

def extract():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.glassdoor.com/Job/united-states-business-analyst-jobs-SRCH_IL.0,13_IN1_KO14,30.htm?sortBy=date_desc")
        html = page.content()
        browser.close()
        return html

if __name__ == "__main__":
    html = extract()
    print(html[:1000])
    
    
    

def transform():
    
    pass

def load():
    
    pass