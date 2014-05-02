"""Tests for the listing module"""

import unittest
from unittest.mock import Mock

import listing

class ExtractPriceTests(unittest.TestCase):
    def setUp(self):
        self.link_html = Mock()
        self.page_html = None

    def test_has_price_tag(self):
        tag_mock = Mock()
        tag_mock.string = "$345"
        self.link_html.find = Mock(return_value=tag_mock)
        price = listing.extract_price(self.link_html, self.page_html)
        self.assertEqual(price, 345)

    def test_has_price_tag_not_number(self):
        tag_mock = Mock()
        tag_mock.string = "$Test String"
        self.link_html.find = Mock(return_value=tag_mock)
        price = listing.extract_price(self.link_html, self.page_html)
        self.assertIsNone(price)

    def test_has_price_in_link(self):
        self.link_html.find = Mock(return_value=None)
        self.link_html.text = "$345 "
        price = listing.extract_price(self.link_html, self.page_html)
        self.assertEqual(price, 345)

if __name__ == '__main__':
    unittest.main()