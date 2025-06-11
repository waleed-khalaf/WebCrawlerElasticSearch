# Find a way to scrape website recursively until a link takes you out of the specified domain. 
# Then parse the results into mappings that are able to be embedded into a vector store for RAG.  
# Find a way to view the robots.txt file and scrape legally through websites 
# Figure out if there's a need to do extra parsing outside of bs4
# How do I integrate with with langChain to form a complete pipeline from website to Embeddings ? 
import requests
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
