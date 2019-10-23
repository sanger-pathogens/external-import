import unittest
from unittest.mock import patch, call
import os
import xlrd
from importer.model import Spreadsheet, RawRead
from importer.writer import Preparation, OutputSpreadsheetGenerator

AN_OUTPUT = "AN_OUTPUT"
A_TICKET = 123
AN_INSTANCE = 2
A_NEXT_INSTANCE = AN_INSTANCE + 1
A_BREAKPOINT = 1
A_POSITION = 1

class TestFileCopy(unittest.TestCase):

    @patch('importer.writer.copyfile')
    def test_copy_files(self, copyfile_patch):
        under_test = Preparation.new_instance(Spreadsheet.new_instance("MyStudy", [
            RawRead(forward_read='PAIR1_1.fastq.gz', reverse_read='PAIR1_2.fastq.gz', sample_name='SAMPLE1',
                    taxon_id='1280', library_name='LIB1', sample_accession=None),
            RawRead(forward_read='PAIR2_1.fastq.gz', reverse_read='PAIR2_2.fastq.gz', sample_name='SAMPLE2',
                    taxon_id='1280', library_name='LIB2', sample_accession=None)]), 'destination', 0, 0)
        under_test.copy_files('source')
        self.assertEquals(copyfile_patch.call_args_list,
                          [call('source/PAIR1_1.fastq.gz', 'destination/0/PAIR1_1.fastq.gz'),
                           call('source/PAIR1_2.fastq.gz', 'destination/0/PAIR1_2.fastq.gz'),
                           call('source/PAIR2_1.fastq.gz', 'destination/0/PAIR2_1.fastq.gz'),
                           call('source/PAIR2_2.fastq.gz', 'destination/0/PAIR2_2.fastq.gz')])

    @patch('importer.writer.copyfile')
    def test_copy_files_single_strand(self, copyfile_patch):
        under_test = Preparation.new_instance(Spreadsheet.new_instance("MyStudy", [
            RawRead(forward_read='PAIR1_1.fastq.gz', reverse_read='PAIR1_2.fastq.gz', sample_name='SAMPLE1',
                    taxon_id='1280', library_name='LIB1', sample_accession=None),
            RawRead(forward_read='SINGLE.fastq.gz', reverse_read=None, sample_name='SAMPLE2',
                    taxon_id='1280', library_name='LIB2', sample_accession=None)]), 'destination', 0, 0)
        under_test.copy_files('source')
        self.assertEquals(copyfile_patch.call_args_list,
                          [call('source/PAIR1_1.fastq.gz', 'destination/0/PAIR1_1.fastq.gz'),
                           call('source/PAIR1_2.fastq.gz', 'destination/0/PAIR1_2.fastq.gz'),
                           call('source/SINGLE.fastq.gz', 'destination/0/SINGLE.fastq.gz')])


class TestXlsGeneration(unittest.TestCase):

    def test_of_OutputSpreadsheetGenerator(self):
        sheet = self.make_spreadsheet_for_test()
        self.run_tested_function(sheet)
        self.run_workbook_assertions()
        os.remove('workbook.xls')

    def run_workbook_assertions(self):
        WORKBOOK_UNDER_TEST = xlrd.open_workbook('workbook.xls')
        SHEET_UNDER_TEST = WORKBOOK_UNDER_TEST.sheet_by_index(0)
        BREAKPOINT_SPREADSHEET = xlrd.open_workbook('test_breakpoint_functionality.xls')
        BREAKPOINT_FIRSTSHEET = BREAKPOINT_SPREADSHEET.sheet_by_index(0)
        for row in range(10):
            for col in range(10):
                if BREAKPOINT_FIRSTSHEET.cell_value(row, 0) == 'Data to be kept until' and isinstance(
                        BREAKPOINT_FIRSTSHEET.cell_value(row, col),
                        float) == True:
                    year, month, day, *rest = xlrd.xldate_as_tuple(BREAKPOINT_FIRSTSHEET.cell_value(row, 1),
                                                                   BREAKPOINT_SPREADSHEET.datemode)
                    if day < 10:
                        day = '0' + str(day)
                    if month < 10:
                        month = '0' + str(month)
                    self.assertEqual(SHEET_UNDER_TEST.cell_value(row, col), f'{day}/{month}/{year}')
                else:
                    self.assertEqual(SHEET_UNDER_TEST.cell_value(row, col),
                                     BREAKPOINT_FIRSTSHEET.cell_value(row, col))

    def run_tested_function(self, sheet):
        generator = OutputSpreadsheetGenerator(sheet, A_POSITION)
        workbook, file_ended, current_position = generator.build(A_BREAKPOINT)
        workbook.save('workbook.xls')
        self.assertEqual((current_position, file_ended), (2, True))
        return current_position, file_ended

    def make_spreadsheet_for_test(self):
        sheet = Spreadsheet()
        sheet.supplier, sheet.organisation, sheet.contact, sheet.technology, sheet.name, sheet.accession, sheet.size, \
        sheet.limit = ('Supplier', 'Org', 'Contact', 'Illumina', 'AStudyName1', None, 1.90, '01/01/2025')
        sheet.reads = [RawRead(forward_read='PAIR1_1.fastq.gz', reverse_read='PAIR1_2.fastq.gz', sample_name='SAMPLE1',
                               taxon_id='1280', library_name='LIB1', sample_accession=None),
                       RawRead(forward_read='SECONDLINE.fastq.gz', reverse_read=None, sample_name='SAMPLE2',
                               taxon_id='1280', library_name='LIB2', sample_accession=None)]
        return sheet

    def test_of_preparation_initialization(self):
        spreadsheet = Spreadsheet()
        preparation = Preparation.new_instance(spreadsheet, AN_OUTPUT, A_TICKET, AN_INSTANCE)
        self.assert_preparation(preparation, spreadsheet)


    def assert_preparation(self, preparation, spreadsheet):
        self.assertEqual(preparation.destination, AN_OUTPUT + '/' + str(A_TICKET))
        self.assertEqual(preparation.spreadsheet, spreadsheet)
        self.assertEqual(preparation.spreadsheet_file, (AN_OUTPUT + '/'+ str(A_TICKET) +'/external_' + str(A_TICKET) + '_' + str(AN_INSTANCE) + '.xls'))
