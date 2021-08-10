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
        actual = loader.load_xls()
        self.assertSpreadsheet(expected, actual)

    def test_header_initialization_no_reverse_read(self):
        loader = SpreadsheetLoader(os.path.join(self.data_dir, 'test_upload_no_pair.xls'))

        expected = Spreadsheet.new_instance("MyStudy", [
            self._raw_read('PAIR1_1.fastq.gz', None, 'SAMPLE1', 'LIB1', 'ACCESSION1'),
            self._raw_read('PAIR2_1.fastq.gz', None, 'SAMPLE2', 'LIB2', 'ACCESSION2')],
                                            contact="Some Name", organisation="ENA", supplier='ENA',
                                            technology='Illumina', size=123456.0, accession='accession',
                                            limit='30/09/2020')
        actual = loader.load_xls()
        self.assertSpreadsheet(expected, actual)

    def test_header_initialization_no_library_name(self):
        loader = SpreadsheetLoader(os.path.join(self.data_dir, 'test_upload_no_pair_no_lib.xls'))

        expected = Spreadsheet.new_instance("MyStudy", [
            self._raw_read('PAIR1_1.fastq.gz', None, 'SAMPLE1', 'SAMPLE1', 'ACCESSION1'),
            self._raw_read('PAIR2_1.fastq.gz', None, 'SAMPLE2', 'SAMPLE2', 'ACCESSION2')],
                                            contact="Some Name", organisation="ENA", supplier='ENA',
                                            technology='Illumina', size=123456.0, accession='accession',
                                            limit='30/09/2020')
        actual = loader.load_xls()
        self.assertSpreadsheet(expected, actual)

    def test_header_initialization_no_accession(self):
        loader = SpreadsheetLoader(os.path.join(self.data_dir, 'test_upload_no_pair_no_lib_no_accession.xls'))

        expected = Spreadsheet.new_instance("MyStudy", [
            self._raw_read('PAIR1_1.fastq.gz', None, 'SAMPLE1', 'LIB1', None),
            self._raw_read('PAIR2_1.fastq.gz', None, 'SAMPLE2', 'LIB2', None)],
                                            contact="Some Name", organisation="ENA", supplier='ENA',
                                            technology='Illumina', size=123456.0, accession=None,
                                            limit='30/09/2020')
        actual = loader.load_xls()
        self.assertSpreadsheet(expected, actual)

    def test_sample_and_library_names_as_integers(self):
        loader = SpreadsheetLoader(os.path.join(self.data_dir, 'test_sample_name_as_int.xls'))

        expected = Spreadsheet.new_instance("AStudyName1", [
            self._raw_read('ERR0000001_1.fastq.gz', 'ERR0000001_2.fastq.gz', '101260', '1000000001', 'ERR0000001',
                           '485'),
            self._raw_read('ERR0000002_1.fastq.gz', 'ERR0000002_2.fastq.gz', '101264', '2000000002', 'ERR0000002',
                           '485')],
                                            contact="Me", organisation="Org", supplier='Supplier',
                                            technology='Illumina', size=1.90, accession=None,
                                            limit='01/01/2025')
        actual = loader.load_xls()
        self.assertSpreadsheet(expected, actual)

    def test_no_filename_only_run_accession(self):
        loader = SpreadsheetLoader(os.path.join(self.data_dir, 'test_run_accession.xls'))

        expected = Spreadsheet.new_instance("MyStudy", [
            self._raw_read('PAIR1', 'T', 'SAMPLE1', 'LIB1', 'ACCESSION1'),
            self._raw_read('PAIR2', 'T', 'SAMPLE2', 'LIB2', 'ACCESSION2'),
            self._raw_read('PAIR3', 'F', 'SAMPLE3', 'LIB3', 'ACCESSION3')],
                                            contact="Some Name", organisation="ENA", supplier='ENA',
                                            technology='Illumina', size=123456.0, accession='accession',
                                            limit='30/09/2020')
        actual = loader.load_xls()
        self.assertSpreadsheet(expected, actual)

    def test_cells_read_xlsx(self):
        loader = SpreadsheetLoader(os.path.join(self.data_dir, 'test_upload.xlsx'))

        expected = Spreadsheet.new_instance("MyStudy", [
            self._raw_read('PAIR1_1.fastq.gz', 'PAIR1_2.fastq.gz', 'SAMPLE1', 'LIB1', 'ACCESSION1'),
            self._raw_read('PAIR2_1.fastq.gz', 'PAIR2_2.fastq.gz', 'SAMPLE2', 'LIB2', 'ACCESSION2')],
                                            contact="Some Name", organisation="ENA", supplier='ENA',
                                            technology='Illumina', size=123456.0, accession='accession',
                                            limit='30/09/2020')
        actual = loader.load_xlsx()
        self.assertSpreadsheet(expected, actual)

    def test_cell_formats_xls(self):
        loader = SpreadsheetLoader(os.path.join(self.data_dir, 'cell_formats.xls'))
        expected = Spreadsheet.new_instance("AStudyName1", [
            self._raw_read('ERR0000001_1.fastq.gz', 'ERR0000001_2.fastq.gz', 'some_name', '1000000001', 'ERR0000001','485'),
            self._raw_read('ERR0000002_1.fastq.gz', 'ERR0000002_2.fastq.gz', '12345', '2000000002', 'ERR0000002','485'),
            self._raw_read('ERR0000003_1.fastq.gz', 'ERR0000003_2.fastq.gz', '6789', '2000000002', 'ERR0000002','485'),
            self._raw_read('ERR0000004_1.fastq.gz', 'ERR0000004_2.fastq.gz', None, '1000000001', 'ERR0000002','485')],
                                            contact="Me", organisation="Org", supplier='Supplier',
                                            technology='Illumina', size=1.90, accession=None,
                                            limit='01/01/2025')
        actual = loader.load_xls()
        self.assertSpreadsheet(expected, actual)

    def test_cell_formats_xlsx(self):
        loader = SpreadsheetLoader(os.path.join(self.data_dir, 'cell_formats.xlsx'))
        expected = Spreadsheet.new_instance("AStudyName1", [
            self._raw_read('ERR0000001_1.fastq.gz', 'ERR0000001_2.fastq.gz', 'some_name', '1000000001', 'ERR0000001','485'),
            self._raw_read('ERR0000002_1.fastq.gz', 'ERR0000002_2.fastq.gz', '12345', '2000000002', 'ERR0000002','485'),
            self._raw_read('ERR0000003_1.fastq.gz', 'ERR0000003_2.fastq.gz', '6789', '2000000002', 'ERR0000002','485'),
            self._raw_read('ERR0000004_1.fastq.gz', 'ERR0000004_2.fastq.gz', None, '1000000001', 'ERR0000002','485')],
                                            contact="Me", organisation="Org", supplier='Supplier',
                                            technology='Illumina', size=1.90, accession=None,
                                            limit='01/01/2025')
        actual = loader.load_xlsx()
        self.assertSpreadsheet(expected, actual)

    def assertSpreadsheet(self, expected, actual):
        self.maxDiff = None
        self.assertEqual(expected.__dict__, actual.__dict__)

    def _raw_read(self, forward_read, reverse_read, sample_name, library_name, accession, taxon_id='1280'):
        return RawRead(forward_read=forward_read, reverse_read=reverse_read, sample_name=sample_name,
                       sample_accession=accession, taxon_id=taxon_id, library_name=library_name)
