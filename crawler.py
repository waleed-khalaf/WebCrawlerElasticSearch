import re
from collections import deque
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException


options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Firefox(options=options)
driver.get("https://www.burgan.com")
WebDriverWait(driver, 30).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
    )

# BRUTE FORCE
links_to_filter = driver.find_elements(By.TAG_NAME, "a")
pattern = re.compile(r"^https://(?:www\.)?burgan\.com(?:$|/).*")


all_href = [link.get_attribute("href") for link in links_to_filter]
urls_to_scrape = [href for href in all_href if href != "" and re.search(pattern, href)]


print(len(urls_to_scrape))
for url in urls_to_scrape:
    print(url)
print("End of basic crawl")

#TODO: (BFS) to find all the webpages on the site then compare with the brute force number, expecting it to be higher than BF number:w

def get_domain_links(start_url):
    url_queue = deque()
    url_queue += [start_url]
    visited_urls = set()
    base_domain = urlparse(start_url).netloc

    while url_queue:
        url = url_queue.popleft()
        print(f"Visting: {url}\n")
        try:
            driver.get(url)
        except Exception as err:
            print(f"Failed to load {url}: {err}")
            continue

        if url not in visited_urls:
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
                   (By.TAG_NAME,"a"))
                   )
            for a_tag in driver.find_elements(By.TAG_NAME, "a"):
                href = a_tag.get_attribute("href")
                print(href)
                if not href:
                    continue
                   
                parts = urlparse(href)
                if parts.netloc != base_domain:
                    continue
                normalized = f"{parts.scheme}://{parts.netloc}{parts.path}"
                if normalized not in visited_urls:
                    url_queue += [normalized]
                    visited_urls.add(normalized)
       
    return visited_urls



print("\nStarting BFS Crawl")

scraped_domains = get_domain_links("https://www.burgan.com")
print(f"Amount of Domains: {len(scraped_domains)}")
print()

driver.quit()


#TODO: Use bs4 access to parse the html 

#TODO: Normalize data to be ingested by ElasticSearch 

#TODO: Upload data to ElasticSearch