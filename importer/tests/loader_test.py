import unittest
from importer.loader import SpreadsheetLoader
from importer.model import Spreadsheet, RawRead


class TestDocument(unittest.TestCase):

    def test_header_initialization(self):
        loader = SpreadsheetLoader("test_upload.xls")

        expected = Spreadsheet("MyStudy", [
            RawRead(forward_read='PAIR1_1.fastq.gz', reverse_read='PAIR1_2.fastq.gz', sample_name='SAMPLE1', taxon_id=1280.0, library_name='LIB1'),
            RawRead(forward_read='PAIR2_1.fastq.gz', reverse_read='PAIR2_2.fastq.gz', sample_name='SAMPLE2', taxon_id=1280.0, library_name='LIB2')])
        actual = loader.load()
        self.assertSpreadsheet(expected, actual)

    def assertSpreadsheet(self, expected, actual):
        self.maxDiff = None
        self.assertEquals(expected.__dict__, actual.__dict__)
