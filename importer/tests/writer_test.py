import unittest
from unittest.mock import patch, call

from importer.model import Spreadsheet, RawRead
from importer.writer import Preparation


class TestFileCopy(unittest.TestCase):

    @patch('importer.writer.copyfile')
    def test_copy_files(self, copyfile_patch):
        under_test = Preparation(Spreadsheet("MyStudy", [
            RawRead(forward_read='PAIR1_1.fastq.gz', reverse_read='PAIR1_2.fastq.gz', sample_name='SAMPLE1',
                    taxon_id='1280', library_name='LIB1'),
            RawRead(forward_read='PAIR2_1.fastq.gz', reverse_read='PAIR2_2.fastq.gz', sample_name='SAMPLE2',
                    taxon_id='1280', library_name='LIB2')]), 'destination')
        under_test.copy_files('source')
        self.assertEquals(copyfile_patch.call_args_list,
                          [call('source/PAIR1_1.fastq.gz', 'destination/PAIR1_1.fastq.gz'),
                           call('source/PAIR1_2.fastq.gz', 'destination/PAIR1_2.fastq.gz'),
                           call('source/PAIR2_1.fastq.gz', 'destination/PAIR2_1.fastq.gz'),
                           call('source/PAIR2_2.fastq.gz', 'destination/PAIR2_2.fastq.gz')])

    @patch('importer.writer.copyfile')
    def test_copy_files_single_strand(self, copyfile_patch):
        under_test = Preparation(Spreadsheet("MyStudy", [
            RawRead(forward_read='PAIR1_1.fastq.gz', reverse_read='PAIR1_2.fastq.gz', sample_name='SAMPLE1',
                    taxon_id='1280', library_name='LIB1'),
            RawRead(forward_read='SINGLE.fastq.gz', reverse_read=None, sample_name='SAMPLE2',
                    taxon_id='1280', library_name='LIB2')]), 'destination')
        under_test.copy_files('source')
        self.assertEquals(copyfile_patch.call_args_list,
                          [call('source/PAIR1_1.fastq.gz', 'destination/PAIR1_1.fastq.gz'),
                           call('source/PAIR1_2.fastq.gz', 'destination/PAIR1_2.fastq.gz'),
                           call('source/SINGLE.fastq.gz', 'destination/SINGLE.fastq.gz')])
