import os
import unittest

from importer.loader import SpreadsheetLoader
from importer.model import Spreadsheet, RawRead


class TestLoader(unittest.TestCase):
    data_dir = os.path.dirname(os.path.abspath(__file__))

    def test_header_initialization(self):
        loader = SpreadsheetLoader(os.path.join(self.data_dir, 'test_upload.xls'))

        expected = Spreadsheet.new_instance("MyStudy", [
            self._raw_read('PAIR1_1.fastq.gz', 'PAIR1_2.fastq.gz', 'SAMPLE1', 'LIB1', 'ACCESSION1'),
            self._raw_read('PAIR2_1.fastq.gz', 'PAIR2_2.fastq.gz', 'SAMPLE2', 'LIB2', 'ACCESSION2')],
                                            contact="Some Name", organisation="ENA", supplier='ENA',
                                            technology='Illumina', size=123456.0, accession='accession',
                                            limit='30/09/2020')
        actual = loader.load()
        self.assertSpreadsheet(expected, actual)

    def test_header_initialization_no_reverse_read(self):
        loader = SpreadsheetLoader(os.path.join(self.data_dir, 'test_upload_no_pair.xls'))

        expected = Spreadsheet.new_instance("MyStudy", [
            self._raw_read('PAIR1_1.fastq.gz', None, 'SAMPLE1', 'LIB1', 'ACCESSION1'),
            self._raw_read('PAIR2_1.fastq.gz', None, 'SAMPLE2', 'LIB2', 'ACCESSION2')],
                                            contact="Some Name", organisation="ENA", supplier='ENA',
                                            technology='Illumina', size=123456.0, accession='accession',
                                            limit='30/09/2020')
        actual = loader.load()
        self.assertSpreadsheet(expected, actual)

    def test_header_initialization_no_library_name(self):
        loader = SpreadsheetLoader(os.path.join(self.data_dir, 'test_upload_no_pair_no_lib.xls'))

        expected = Spreadsheet.new_instance("MyStudy", [
            self._raw_read('PAIR1_1.fastq.gz', None, 'SAMPLE1', 'SAMPLE1', 'ACCESSION1'),
            self._raw_read('PAIR2_1.fastq.gz', None, 'SAMPLE2', 'SAMPLE2', 'ACCESSION2')],
                                            contact="Some Name", organisation="ENA", supplier='ENA',
                                            technology='Illumina', size=123456.0, accession='accession',
                                            limit='30/09/2020')
        actual = loader.load()
        self.assertSpreadsheet(expected, actual)

    def test_header_initialization_no_accession(self):
        loader = SpreadsheetLoader(os.path.join(self.data_dir, 'test_upload_no_pair_no_lib_no_accession.xls'))

        expected = Spreadsheet.new_instance("MyStudy", [
            self._raw_read('PAIR1_1.fastq.gz', None, 'SAMPLE1', 'LIB1', None),
            self._raw_read('PAIR2_1.fastq.gz', None, 'SAMPLE2', 'LIB2', None)],
                                            contact="Some Name", organisation="ENA", supplier='ENA',
                                            technology='Illumina', size=123456.0, accession=None,
                                            limit='30/09/2020')
        actual = loader.load()
        self.assertSpreadsheet(expected, actual)

    def assertSpreadsheet(self, expected, actual):
        self.maxDiff = None
        self.assertEqual(expected.__dict__, actual.__dict__)

    def _raw_read(self, forward_read, reverse_read, sample_name, library_name, accession):
        return RawRead(forward_read=forward_read, reverse_read=reverse_read, sample_name=sample_name,
                       sample_accession=accession, taxon_id='1280', library_name=library_name)
