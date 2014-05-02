"""Tests for the listing module"""

import unittest
from unittest.mock import Mock

import listing

class ExtractPriceTests(unittest.TestCase):
    def setUp(self):
        self.link_html = Mock()
        self.page_html = None
        self.unhidden_page_html = None

    def test_has_price_tag(self):
        tag_mock = Mock()
        tag_mock.string = "$345"
        self.link_html.find = Mock(return_value=tag_mock)
        price = listing.extract_price(
            self.link_html, self.page_html, self.unhidden_page_html)
        self.assertEqual(price, 345)

    def test_has_price_tag_not_number(self):
        tag_mock = Mock()
        tag_mock.string = "$Test String"
        self.link_html.find = Mock(return_value=tag_mock)
        price = listing.extract_price(
            self.link_html, self.page_html, self.unhidden_page_html)
        self.assertIsNone(price)

    def test_has_price_in_link(self):
        self.link_html.find = Mock(return_value=None)
        self.link_html.text = "Rent is $345 a month"
        price = listing.extract_price(
            self.link_html, self.page_html, self.unhidden_page_html)
        self.assertEqual(price, 345)

    def test_has_no_price(self):
        self.link_html.find = Mock(return_value=None)
        self.link_html.text = "Not a price"
        price = listing.extract_price(
            self.link_html, self.page_html, self.unhidden_page_html)
        self.assertIsNone(price)


class ExtractAvailableMonthTests(unittest.TestCase):
    def setUp(self):
        self.link_html = Mock()
        self.page_html = Mock()
        self.page_html.text = ""
        self.unhidden_page_html = None

    def test_has_long_month(self):
        self.link_html.a.text = "Available August 1"
        available_month = listing.extract_available_month(
            self.link_html, self.page_html, self.unhidden_page_html)
        self.assertEqual(available_month, 8)

    def test_has_short_month(self):
        self.link_html.a.text = "Available Mar 2015"
        available_month = listing.extract_available_month(
            self.link_html, self.page_html, self.unhidden_page_html)
        self.assertEqual(available_month, 3)

    def test_has_formatted_date(self):
        self.link_html.a.text = "Available 6/25/2015"
        available_month = listing.extract_available_month(
            self.link_html, self.page_html, self.unhidden_page_html)
        self.assertEqual(available_month, 6)

    def test_has_no_date(self):
        self.link_html.a.text = "Apartment is available immediately!"
        available_month = listing.extract_available_month(
            self.link_html, self.page_html, self.unhidden_page_html)
        self.assertIsNone(available_month)


class ExtractTelephoneNumbers(unittest.TestCase):
    def setUp(self):
        self.link_html = None
        self.page_html = Mock()
        self.unhidden_page_html = Mock()

    def test_multiple_telephone_numbers(self):
        self.unhidden_page_html.text = "Call at 123-456-7890 or 098-765-4321"
        telephone_numbers = listing.extract_telephone_numbers(
            self.link_html, self.page_html, self.unhidden_page_html)
        self.assertEqual(telephone_numbers, ['1234567890', '0987654321'])

    def test_space_formatted_telephone_number(self):
        self.unhidden_page_html.text = "Call at 123 456 7890"
        telephone_numbers = listing.extract_telephone_numbers(
            self.link_html, self.page_html, self.unhidden_page_html)
        self.assertEqual(telephone_numbers, ['1234567890'])

    def test_formatted_telephone_number(self):
        self.unhidden_page_html.text = "Call at (123) 456-7890"
        telephone_numbers = listing.extract_telephone_numbers(
            self.link_html, self.page_html, self.unhidden_page_html)
        self.assertEqual(telephone_numbers, ['1234567890'])

    def test_no_telephone_numbers(self):
        self.unhidden_page_html.text = "Please contact me on craigslist"
        telephone_numbers = listing.extract_telephone_numbers(
            self.link_html, self.page_html, self.unhidden_page_html)
        self.assertIsNone(telephone_numbers)


if __name__ == '__main__':
    unittest.main()