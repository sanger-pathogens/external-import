import unittest
from unittest.mock import patch, call

from importer.model import Spreadsheet, RawRead
from importer.writer import Preparation


class TestFileCopy(unittest.TestCase):

    @patch('importer.writer.copyfile')
    def test_copy_files(self, copyfile_patch):
        under_test = Preparation.new_instance(Spreadsheet.new_instance("MyStudy", [
            RawRead(forward_read='PAIR1_1.fastq.gz', reverse_read='PAIR1_2.fastq.gz', sample_name='SAMPLE1',
                    taxon_id='1280', library_name='LIB1', sample_accession=None),
            RawRead(forward_read='PAIR2_1.fastq.gz', reverse_read='PAIR2_2.fastq.gz', sample_name='SAMPLE2',
                    taxon_id='1280', library_name='LIB2', sample_accession=None)]), 'destination', 0)
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
                    taxon_id='1280', library_name='LIB2', sample_accession=None)]), 'destination', 0)
        under_test.copy_files('source')
        self.assertEquals(copyfile_patch.call_args_list,
                          [call('source/PAIR1_1.fastq.gz', 'destination/0/PAIR1_1.fastq.gz'),
                           call('source/PAIR1_2.fastq.gz', 'destination/0/PAIR1_2.fastq.gz'),
                           call('source/SINGLE.fastq.gz', 'destination/0/SINGLE.fastq.gz')])
