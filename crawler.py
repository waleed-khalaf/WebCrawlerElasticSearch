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

#TODO: (BFS) to find all the webpages on the site then compare with the brute force number, expecting it to be higher than BF number:w

url_dict = dict()

def search_url(root_url):
    url_queue = deque()
    search_queue += url_dict[root_url]
    visited_urls = set()
    while search_queue:
        url = search_queue.popleft()
        if url not in visited_urls:
            if url:
                pass
            else:
                # selenium to scrape the page for links (to create dict entry for url_dict[new_url])
                new_url = ""
                search_queue += url_dict[new_url]
                visited_urls.add()




# def search(name):
#     search_queue = deque()
#     search_queue += graph[name]
#     searched = []
#     while search_queue:
#         person = search_queue.popleft()
#         if not person in searched:
#             if person_is_seller(person):
#                 print(person + " is a mango seller!")
#                 return True
#             else:
#                 search_queue += graph[person]
#                 searched.append(person)
#     return False

# search("you")

#TODO: Save links to some sort of data structure 

driver.quit()


#TODO: Use bs4 access to parse the html 

#TODO: Normalize data to be ingested by ElasticSearch 

#TODO: Upload data to ElasticSearch