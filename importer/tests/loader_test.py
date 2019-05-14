import unittest
from importer.loader import SpreadsheetLoader


class TestDocument(unittest.TestCase):

    def test_header_initialization(self):
        loader = SpreadsheetLoader("auguet_2016_PRJEB11177.samples.xls")

        self.assertEqual(loader.load(), 752)

