from django.test import TestCase

import utils


class UtilsTest(TestCase):

    def test_format_street_name_numbered(self):
        """
        Tests format_street_name() with a numbered street name.
        """
        self.assertEqual(utils.format_street_name('20TH'), '20th')

    def test_format_street_name_string(self):
        """
        Tests format_street_name() with a string street name.
        """
        self.assertEqual(utils.format_street_name('PINE'), 'Pine')

    def test_fix_address_numbered(self):
        address = '1999 10TH ST'
        self.assertEqual(utils.fix_address(address), '1999 10th St')

    def test_fix_address_string(self):
        address = '104 MAIN ST'
        self.assertEqual(utils.fix_address(address), '104 Main St')
