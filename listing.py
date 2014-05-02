"""Contains a class representing an apartment listing and functions to extract
   each feature."""

from bs4 import BeautifulSoup
import re

class Listing(object):

    """Represents a Listing"""

    def __init__(self, listing_url, link_html, page_html):
        self.features = dict()
        self.features['url'] = listing_url
        self.extract_features(link_html, page_html)

    def set_feature_if_not_none(self, feature, value):
        if value:
            self.features[feature] = value

    def extract_features(self, link_html, page_html):
        """Calls each extractor on the listing"""
        price = extract_price(link_html, page_html)
        self.set_feature_if_not_none('price', price)


def extract_price(link_html, page_html):
    """Extracts the price from the link or page"""
    price_string = None

    # First check for a price tag on the link
    price_tag = link_html.find('span', class_='price')
    if price_tag:
        price_string = price_tag.string
    else:
        # Check for a dollar sign followed by numbers in the link text
        match = re.search("\$[0-9]*", link_html.text)
        if match:
            price_string = match.group(0)

    # String dollar sign and convert price to an integer
    if price_string:
        if price_string[0] == '$':
            price_string = price_string[1:]
        try:
            return int(price_string)
        except ValueError:
            pass
