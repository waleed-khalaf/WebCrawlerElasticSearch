from bs4 import BeautifulSoup as bs
import requests
from time import sleep
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


URL = "https://www.burgan.com/Pages/Home.aspx"

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Firefox(options=options)
driver.set_page_load_timeout(30)



driver.get(URL)
WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
html = driver.page_source
soup = bs(html, "html.parser")
print(soup.text)