"""Contains a class that retrieves listings from craigslist and extracts
   features, saving them in a database"""

import requests
import pymongo
from bs4 import BeautifulSoup
from time import sleep

from listing import Listing

class ListingFinder(object):
    def __init__(self, city_name, base_url, path):
        client = pymongo.MongoClient()
        self.collection = client.apartments[city_name]
        self.base_url = base_url
        self.path = path

    def get_listings(self, max_to_retrieve):
        response = requests.get(self.base_url + self.path)
        listing_html = BeautifulSoup(response.text)

        currently_retrieved = 0

        for link_tag in listing_html.find_all('p', class_="row"):
            # Check if link in DB already. If not, load page and collect data
            link_url = self.base_url + get_link_url(link_tag)
            listing_record = self.collection.find_one({'url': link_url})
            if not listing_record:
                page_html = get_page_html(link_url)
                contact_info_url = get_contact_info_url(page_html)
                if contact_info_url:
                    full_contact_info_url = self.base_url + contact_info_url
                    unhidden_page_html = get_page_html(full_contact_info_url)
                else:
                    unhidden_page_html = None
                listing = Listing(link_url, link_tag, page_html,
                                  unhidden_page_html)
                print(listing.features)
                self.collection.insert(listing.features)
                currently_retrieved += 1
                if currently_retrieved >= max_to_retrieve:
                    break


def get_link_url(link_tag):
    link = link_tag.find('a')
    if link:
        return link.get('href')


def get_page_html(link_url):
    response = requests.get(link_url)
    # Simple rate limiting to prevent too many requests
    sleep(5)
    return BeautifulSoup(response.text)


def get_contact_info_url(page_html):
    show_contact_link = page_html.find('a', class_='showcontact')
    if show_contact_link:
        return show_contact_link.get('href')
        

if __name__ == "__main__":
    city_name = 'Pittsburgh'
    craigslist_base_url = "http://pittsburgh.craigslist.org"
    craigslist_path = "/apa/"

    listing_finder = ListingFinder(city_name, craigslist_base_url,
                                   craigslist_path)
    listing_finder.get_listings(2)
