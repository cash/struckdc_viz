import unittest
from extract import AddressExtractor, Tokens

class ExtractTestCase(unittest.TestCase):

    def setUp(self):
        self.extractor = AddressExtractor()

    def testMapForNumberStreets(self):
        self.assertEqual(Tokens.NAME, self.extractor.map('13th'))
