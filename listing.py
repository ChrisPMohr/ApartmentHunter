"""Contains a class representing an apartment listing and functions to extract
   each feature."""

from bs4 import BeautifulSoup
import re

class Listing(object):

    """Represents an apartment listing and contains all html about it"""

    def __init__(self, listing_url, link_html, page_html,
                 unhidden_page_html):
        self.features = dict()
        self.features['url'] = listing_url
        self.extract_features(link_html, page_html, unhidden_page_html)

    def set_feature_if_not_none(self, feature, value):
        if value:
            self.features[feature] = value

    def extract_features(self, link_html, page_html, unhidden_page_html):
        """Calls each extractor on the listing"""
        price = extract_price(
            link_html, page_html, unhidden_page_html)
        self.set_feature_if_not_none('price', price)

        date = extract_available_month(
            link_html, page_html, unhidden_page_html)
        self.set_feature_if_not_none('available month', date)

        telephone = extract_telephone_numbers(
            link_html, page_html, unhidden_page_html)
        self.set_feature_if_not_none('telephone', telephone)

        address = extract_address(
            link_html, page_html, unhidden_page_html)
        self.set_feature_if_not_none('address', address)

        number_bedrooms = extract_number_bedrooms(
            link_html, page_html, unhidden_page_html)
        self.set_feature_if_not_none('bedrooms', number_bedrooms)


def extract_price(link_html, page_html, unhidden_page_html):
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


def extract_available_month(link_html, page_html, unhidden_page_html):
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
        return long_month_list.index(match.group(0).lower()) + 1
    
    match = re.search(short_month_regex, listing_text, re.IGNORECASE)
    if match:
        return short_month_list.index(match.group(0).lower()) + 1

    # Look for dates in month/day/year format
    date_regex = '([0-9]{1,2}).[0-9]{1,2}.[0-9]{2,4}'
    match = re.search(date_regex, listing_text)
    if match:
        month = int(match.group(1))
        if month >= 1 and month <= 12:
            return month


def extract_telephone_numbers(link_html, page_html, unhidden_page_html):
    """Tries to extract strings that look like a telephone number"""
    telephone_regex = '\(?([0-9]{3})\)?.([0-9]{3}).([0-9]{4})'
    if unhidden_page_html:
        matches = re.findall(telephone_regex, unhidden_page_html.text)
    else:
        matches = re.findall(telephone_regex, page_html.text)

    telephone_numbers = list()
    for match in matches:
        telephone_number = ''.join(match)
        if len(telephone_number) == 10:
            telephone_numbers.append(telephone_number)
    if telephone_numbers:
    	# remove duplicates
    	telephone_numbers = list(set(telephone_numbers))
        return telephone_numbers


def extract_address(link_html, page_html, unhidden_page_html):
    """Tries to extract address"""
    # Finding addresses in text is challenging, so we just look for
    # the address field that shows up on some listings
    address_tag = page_html.find('div', class_='mapaddress')
    if address_tag:
        return address_tag.string


def extract_number_bedrooms(link_html, page_html, unhidden_page_html):
	"""Tries to extract number of bedrooms"""
	# This usually shows up in the link to the listing
	bedroom_tag = link_html.find('span', class_='l2')
	if bedroom_tag:
		match = re.search('([0-9])br', bedroom_tag.text)
		if match:
			return int(match.group(1))
