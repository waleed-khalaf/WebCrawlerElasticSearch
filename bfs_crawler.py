import time
from urllib.parse import urlparse, urldefrag, urlunparse, urljoin
from collections import deque
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# TODO Move to config file when done
HANG_PATTERNS = ["/_layouts/", "/login.apsx", "/singin/", "/authenticate"]

def clean_url(url_to_clean, root_url=None):
   
    # defrag the url
    defragged_url = urldefrag(url_to_clean).url
    # split the url into its parts
    parsed_url = urlparse(defragged_url)
    root_netloc = urlparse(root_url).netloc

    # validations
    # TODO check if same domain

    # TODO check if its just relative path and join
    if parsed_url.netloc == "":
        cleaned_url = urljoin(root_url, parsed_url.path)
    # TODO remove if 'hanging' path eg _layout, authentication etc.
    # TODO continue if hang pattern 
    elif parsed_url.path in HANG_PATTERNS:
        pass
    else:
        cleaned_url = urlunparse(parsed_url)

    if root_netloc == urlparse(cleaned_url).netloc:
        return cleaned_url
    else:
        return None



def bfs_crawler(start_url):

    # Selenium 
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(30)

    # Parsing url
    url_domain = urlparse(start_url).netloc
    print(url_domain)

    # BFS 
    url_queue = deque()
    url_queue += [start_url]
    visited_urls = set()
    visited_urls.add(start_url)

    while url_queue:
        url = url_queue.popleft()
        print(f"Visiting: {url}")

        try:
            # Connecting to url and then waiting until 
            driver.get(url)
            WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

            # iterate over all the a tags to get hrefs, include paths 
            for a_tag in driver.find_elements(By.TAG_NAME, "a"):
                href = a_tag.get_attribute("href")
                cleaned_url = clean_url(href, start_url)
                url_to_check = urlparse(cleaned_url).netloc
                if url_to_check != None and cleaned_url not in visited_urls:
                    url_queue += [cleaned_url]
                    visited_urls.add(cleaned_url)
                # parsed_url = parse_url(href, start_url)
                # if url_domain in parsed_url and parsed_url not in visited_urls:
                #     url_queue += [parsed_url]
                #     visited_urls.add(parsed_url)

            time.sleep(1.0)
            print(len(url_queue))
                
        except Exception as err:
            print(f"{err}\tFailed to visit site {url}")
            continue
        except TimeoutException as err:
            print()
            continue
    print(len(visited_urls))
    return visited_urls


bfs_crawler("https://www.burgan.com/")