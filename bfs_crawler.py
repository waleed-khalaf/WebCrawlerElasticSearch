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

HANG_PATTERNS = ["layouts", "login.aspx", "signin", "authenticate", "{}"]

def clean_url(url_to_clean: str, root_url: str) -> str | None:
    """
    Normalize and filter a candidate URL.
    
    - Remove fragments
    - Resolve relative URLs against root_url
    - Only allow http(s) URLs on the same domain as root_url
    - Strip query strings
    - Drop URLs whose path contains any HANG_PATTERNS
    """
    if not url_to_clean:
        return None

    # 1) Remove fragment identifier
    defragged, _ = urldefrag(url_to_clean)
    parsed = urlparse(defragged)

    # 2) Resolve relative URLs
    if not parsed.netloc:
        # e.g. "/about" → "https://root.com/about"
        cleaned = urljoin(root_url, parsed.path)
    else:
        cleaned = defragged

    parsed = urlparse(cleaned)

    # 3) Only http(s)
    if parsed.scheme not in ("http", "https"):
        return None

    # 4) Same-domain check
    root_netloc = urlparse(root_url).netloc
    if parsed.netloc.lower() != root_netloc:
        return None

    # 5) Strip query & params, keep only scheme://netloc/path
    normalized = urlunparse((parsed.scheme,
                             parsed.netloc,
                             parsed.path.rstrip("/"),  # optional: drop trailing slash
                             "",  # params
                             "",  # query
                             "")) # fragment

    # 6) Drop any path containing a "hang" term
    path_lower = parsed.path.lower()
    if any(pat in path_lower for pat in HANG_PATTERNS):
        return None

    return normalized

    


def bfs_crawler(root_url):

    # Selenium 
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(30)

    # Parsing url
    url_domain = urlparse(root_url).netloc
    print(url_domain)

    # BFS 
    url_queue = deque()
    url_queue += [root_url]
    visited_urls = set()
    visited_urls.add(root_url)

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
                cleaned_url = clean_url(href, root_url)
                if cleaned_url != None and cleaned_url not in visited_urls:
                    url_queue += [cleaned_url]
                    visited_urls.add(cleaned_url)

            time.sleep(1.0)
                
        except Exception as err:
            print(f"{err}\tFailed to visit site {url}")
            visited_urls.remove(url)
            continue
        except TimeoutException as err:
            print()
            continue
    print(len(visited_urls))
    return visited_urls

bfs_crawler("https://www.burgan.com/")
# TODO output to file that bs4 can use an input to scrape
