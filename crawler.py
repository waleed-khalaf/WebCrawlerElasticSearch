import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException

# TODO: Create list of urls to begin scraping at
# TODO: Use traversal algorithm to find all the links on the site
# TODO: Scrape the information from those sites
# TODO: Normalise data for elasticsearch
# TODO: Upload to elasticsearch

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get("https://www.burgan.com")
WebDriverWait(driver, 30).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
    )

# BRUTE FORCE
links_to_filter = driver.find_elements(By.TAG_NAME, "a")
print(f"Found {len(links_to_filter)} links to filter through") 
print()

pattern = re.compile(r"^https://(?:www\.)?burgan\.com(?:$|/).*")


all_href = [link.get_attribute("href") for link in links_to_filter]
urls_to_scrape = [href for href in all_href if href != "" and re.search(pattern, href)]


for link in urls_to_scrape:
    print(link)

# Some sort of graph algorithm (BFS) to find all the webpages on the site

# Save links to some sort of data structure 

driver.quit()


# Use bs4 access to parse the html 

# Normalize data to be ingested by ElasticSearch 

# Upload data to ElasticSearch