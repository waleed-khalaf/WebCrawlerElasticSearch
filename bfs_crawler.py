import time
import random
from urllib.parse import urlparse, urldefrag, urlunparse, urljoin
from collections import deque
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

HANG_PATTERNS = ["layouts", "login.aspx", "signin", "authenticate", "{}"]

def is_valid_url(candidate_url: str, root_url: str) -> bool:
    """
    Return True if `candidate` is non-empty http(s) URL on the same domain as the root url
    whose path does NOT contain any hang patterns.
    """
    if not candidate_url:
        return False
    
    defragged, _ = urldefrag(candidate_url)
    parsed = urlparse(defragged)

    root_netloc = urlparse(root_url).netloc.lower()
    if parsed.netloc:
        if parsed.netloc.lower() != root_netloc:
            return False
        
    if parsed.scheme and parsed.scheme not in ("http", "https"):
        return False
    
    path = parsed.path.lower()
    if any(pat in path for pat in HANG_PATTERNS):
        return False
    
    return True

def clean_url(url_to_clean: str, root_url: str) -> str | None:
    """
    Normalize and filter a candidate URL.
    
    - Remove fragments
    - Resolve relative URLs against root_url
    - Only allow http(s) URLs on the same domain as root_url
    - Strip query strings
    - Drop URLs whose path contains any HANG_PATTERNS
    """
    if not is_valid_url(url_to_clean, root_url):
        return None
    
    defragged, _ = urldefrag(url_to_clean)
    parsed = urlparse(defragged)

    if not parsed.netloc:
        resolved = urljoin(root_url, parsed.path)
    else:
        resolved = defragged

    parsed = urlparse(resolved)

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/")

    normalized = urlunparse((scheme, netloc, path, "", "", ""))
    return normalized



# TODO Parse Html loaded from selenium with bs4
def parse_hrefs():
    pass

# TODO add politeness to prevent getting banned 
def bfs_crawler(root_url: str) -> list:

    user_agents = []
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(30)

    # BFS 
    url_queue = deque()
    url_queue += [root_url]
    visited_urls = set()
    discovered_url = set()
    discovered_lower = set()

    while url_queue:
        url = url_queue.popleft()
        print(f"Visiting: {url}")

        try:
            # Connecting to url and then waiting until 
            driver.get(url)
            visited_urls.add(url)
            WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

            # iterate over all the a tags to get hrefs, include paths 
            for a_tag in driver.find_elements(By.TAG_NAME, "a"):
                try:
                    if not a_tag.is_displayed() or a_tag.size == {'height': 0, 'width': 0}:
                        continue
                    href = a_tag.get_attribute("href")
                    # TODO Use beautiful soup to parse html 

                    cleaned_url = clean_url(href, root_url)
                    if cleaned_url and cleaned_url.lower() not in discovered_lower:
                        url_queue += [cleaned_url]
                        discovered_url.add(cleaned_url)
                        discovered_lower.add(cleaned_url.lower())
                except StaleElementReferenceException:
                    print(f"{href} went stale, as the DOM changed.")
                    continue
            print(f"{len(url_queue)} pages in queue")

            time.sleep(1.0 + random.uniform(0,1.0))
                
        except TimeoutException as err:
            print(f"{err}\t{url} took long to load.")
            # TODO retry the url 
            continue
        except Exception as err:
            print(f"{err}:\tFailed to visit site {url}")
            continue
    print(f"Discovered: {len(discovered_url)}")
    print(f"Visited: {len(visited_urls)}")
    return visited_urls 

bfs_crawler("https://www.burgan.com/")
# TODO how to pass data into format that elastic search can index ?