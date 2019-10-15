import unittest
from unittest.mock import patch, call
import os
import filecmp
import xlrd
from importer.model import Spreadsheet, RawRead
from importer.writer import Preparation
from importer.writer import OutputSpreadsheetGenerator


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
        sheet = Spreadsheet()
        sheet.supplier, sheet.organisation, sheet.contact, sheet.technology, sheet.name, sheet.accession, sheet.size,\
        sheet.limit = ('Supplier', 'Org', 'Contact', 'Illumina', 'AStudyName1', None, 1.90, '01/01/2025')
        sheet.reads = [RawRead(forward_read='PAIR1_1.fastq.gz', reverse_read='PAIR1_2.fastq.gz', sample_name='SAMPLE1',
                              taxon_id='1280', library_name='LIB1', sample_accession=None),
                       RawRead(forward_read='SECONDLINE.fastq.gz', reverse_read=None, sample_name='SAMPLE2',
                              taxon_id='1280', library_name='LIB2', sample_accession=None)]
        current_position = 1
        breakpoint = 1
        generator = OutputSpreadsheetGenerator(sheet, current_position)
        workbook, file_ended, current_position = generator.build(breakpoint)
        workbook.save('workbook.xls')
        self.assertEqual((current_position, file_ended), (2, True))
        please = xlrd.open_workbook('workbook.xls')
        work = please.sheet_by_index(0)
        ineed = xlrd.open_workbook('test_breakpoint_functionality.xls')
        abreak = ineed.sheet_by_index(0)
        for row in range(10):
            for col in range(10):
                if abreak.cell_value(row, 0) == 'Data to be kept until' and isinstance(abreak.cell_value(row, col), float) == True :
                    year, month, day, *rest = xlrd.xldate_as_tuple(abreak.cell_value(row, 1), ineed.datemode)
                    if day < 10:
                        day = '0'+str(day)
                    if month < 10:
                        month = '0'+str(month)
                    self.assertEqual(work.cell_value(row,col), f'{day}/{month}/{year}')
                else:
                    self.assertEqual(work.cell_value(row,col), abreak.cell_value(row,col))
        os.remove('workbook.xls')

    def test_of_preparation_initialization(self):
        spreadsheet = Spreadsheet()
        output = 'output'
        ticket = 123
        instance = 2
        preparation, instance = Preparation.new_instance(spreadsheet, output, ticket, instance)
        self.assertEqual(preparation.destination, 'output/123')
        self.assertEqual(preparation.spreadsheet, spreadsheet)
        self.assertEqual(preparation.spreadsheet_file, 'output/123/external_123_2.xls')
        self.assertEqual(instance, 3)
