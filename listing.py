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

        date = extract_available_month(link_html, page_html)
        self.set_feature_if_not_none('available month', date)


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

def extract_available_month(link_html, page_html):
    """Tries to extract move in date from the link or page
       This method may give some false matches as month names, especially
       "may", may appear in listings when not refering to the month"""
    # Search both the title and page for a month
    listing_text = ''.join([link_html.a.text, page_html.text])

    # Look for long or short month names
    short_month_list = ["jan", "feb", "mar", "apr", "may", "jun",
                        "jul", "aug", "sept", "oct", "nov", "dec"]
    long_month_list = ["january", "february", "march", "april", "may",
                       "june", "july", "august", "september", "october",
                       "november", "december"]
    short_month_regex = '(' + '|'.join(short_month_list) + ')\\b'
    long_month_regex = '(' + '|'.join(long_month_list) + ')\\b'

    match = re.search(long_month_regex, listing_text, re.IGNORECASE)
    if match:
        print(listing_text.encode('utf-8'))
        return long_month_list.index(match.group(0).lower()) + 1
    
    match = re.search(short_month_regex, listing_text, re.IGNORECASE)
    if match:
        return short_month_list.index(match.group(0).lower()) + 1

    # Look for dates in month/day/year format
    date_regex = '([0-9]{1,2})/[0-9]{1,2}/[0-9]{2,4}'
    match = re.search(date_regex, listing_text)
    if match:
        return int(match.group(1))
