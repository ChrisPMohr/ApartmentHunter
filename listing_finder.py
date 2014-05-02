import requests
from bs4 import BeautifulSoup
from time import sleep

from listing import Listing

def get_listings(base_url, path):
    response = requests.get(base_url + path)
    listing_html = BeautifulSoup(response.text)
    
    for link_tag in listing_html.find_all('p', class_="row"):
        page_html = get_page_html(base_url, link_tag)
        listing = Listing(link_tag, page_html)
        print(listing.features)

def get_page_html(base_url, link_tag):
    link = link_tag.find('a')
    if link:
        link_url = link.get('href')
        if link_url:
            response = requests.get(base_url + link_url)
            # Simple rate limiting to prevent too many requests
            sleep(5)
            return BeautifulSoup(response.text)

if __name__ == "__main__":
    craigslist_base_url = "http://pittsburgh.craiglist.org/"
    craigslist_path = "apa/"
    get_listings(craigslist_base_url, craigslist_path)