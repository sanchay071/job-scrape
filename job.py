
import requests
import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd
import pprint
from playwright.sync_api import sync_playwright #From the sync_api module inside the playwright library, import the sync_playwright function
import mysql.connector  # Import the mysql.connector module to connect to MySQL database

# This script is designed to scrape job listings from Glassdoor for Business Analyst positions in the United States.

def extract():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) #p is the instance of playwright, p.chromium is browser type, p.chromium.launch() launches the browser in headless mode
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36") #create a new browser context with a specific user agent to mimic a real browser
        page = context.new_page() # Create a new page in the browser context
        job_location = input("Enter Job Location:") # Prompt user for job location input
        search_term = input("Enter Title:") # Prompt user for job title input
        job_location_hyphenated = job_location.replace(" ", "-")
        search_term_hyphenated = search_term.replace(" ", "-")
    
        job_location_encoded = urllib.parse.quote(job_location_hyphenated)
        search_term_encoded = urllib.parse.quote(search_term_hyphenated)
        
        keyword_start = len(job_location_hyphenated) + 1 #calcuating the Keyword Offset(KO) in glass door URL. This is will fetch the starting index for the search term
        keyword_end = keyword_start + len(search_term_hyphenated) #keyword_end will fetch the end index of the search term in the URL
        # Generate the URL
        final_url = f"https://www.glassdoor.com/Job/{job_location_encoded}-{search_term_encoded}-jobs-SRCH_IL.0,13_IN1_KO{keyword_start},{keyword_end}.htm?sortBy=date_desc"

        # Print the URL to the console
        print("Generated URL:", final_url)
        
        page.goto(final_url)
    
        # Wait for the specific element to load
        page.wait_for_selector("div.jobCard")
        
        html = page.content()
        browser.close()
        return html
#testing code to extract the html content
# if __name__ == "__main__":
#     html = extract()
#     print(html[:1000])   

def transform(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all("div", {"class" : "jobCard"}) # Find all divs with class jobContainer
    
def load(job_list):
    # This function processes the job listings and extracts relevant information.
    # It returns a list of dictionaries containing job details.
    
    # Initialize an empty list to hold job postings

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
        
        # pprint.pprint(job_listings)
        
    df =pd.DataFrame(job_listings, index=None)
    return df

def create_database(df):
    conn = mysql.connector.connect(
        host="localhost",
        user = "root",
        password = "petra",
        database = "joblist") #from mysql library import connector module and connect method
    curr = conn.cursor() #an object to iterate over the rows of a result set
    curr.execute("""CREATE TABLE IF NOT EXISTS scraped_jobs (id INT AUTO_INCREMENT PRIMARY KEY,
                        company VARCHAR(255),
                        title VARCHAR(255),
                        link VARCHAR(255),
                        location VARCHAR(255))""")
    
    for _, row in df.iterrows():
        curr.execute("""INSERT INTO scraped_jobs (company, title, link, location)
                      VALUES (%s, %s, %s, %s)""", 
                      (row['company'], row['title'], row['link'], row['location']))
    
    conn.commit()  # Commit the changes to the database
    print("Data inserted successfully.")
    
    #extract data
    curr.execute("""SELECT * from scraped_jobs ORDER BY id DESC""") #execute the SQL query to select all records from the scraped_jobs table""")
    rows = curr.fetchall()
    
    for row in rows:
        print (row)
    conn.close()  # Close the connection to the database