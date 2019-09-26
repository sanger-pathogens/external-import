import unittest
import os
from importer import file_splitter as fs

class file_split_tester(unittest.TestCase):

    def setUp(self):
        self.datasheet1 = fs.Spreadsheet_Splitter('breakpoint_testing', 12345, 1)
        self.datasheet2 = fs.Spreadsheet_Splitter('breakpoint_testing', 23456, 3)

    def tearDown(self):
        if os.path.isfile('breakpoint_testing/12345/external_12345_0.xls') == True:
            os.remove('breakpoint_testing/12345/external_12345_0.xls')
        if os.path.isfile('breakpoint_testing/12345/external_12345_1.xls') == True:
            os.remove('breakpoint_testing/12345/external_12345_1.xls')
        if os.path.isfile('breakpoint_testing/23456/external_23456_0.xls') == True:
            os.remove('breakpoint_testing/23456/external_23456_0.xls')
        if os.path.isfile('breakpoint_testing/23456/external_23456_1.xls') == True:
            os.remove('breakpoint_testing/23456/external_23456_1.xls')

    def test_header(self):
        test = open('./breakpoint_testing/header_test_1.txt')
        test_data = test.read()
        self.assertEqual(self.datasheet1.header, test_data)
        test.close()

        test = open('./breakpoint_testing/header_test_2.txt')
        test_data = test.read()
        self.assertEqual(self.datasheet2.header, test_data)
        test.close()

    def test_file_sequences(self):
        test_list_1 = ['DRR117952_1.fastq.gz\tDRR117952_2.fastq.gz\tDRS058467\tDRS058467\t482.0\t\t\t\t\t\t\n',
                       'DRR117953_1.fastq.gz\tDRR117953_2.fastq.gz\tDRS058468\tDRS058468\t482.0\t\t\t\t\t\t\n']
        test_list_2 = ['DRR117952_1.fastq.gz\tDRR117952_2.fastq.gz\tDRS058467\tDRS058467\t482.0\t\t\t\t\ttesting comment\t\nDRR117953_1.fastq.gz\tDRR117953_2.fastq.gz\tDRS058468\tDRS058468\t482.0\t\t\t\t\t\t\nDRR117954_1.fastq.gz\tDRR117954_2.fastq.gz\tDRS058469\tDRS058469\t482.0\t\t\t\t\tanother testing comment\t\n', 'DRR117955_1.fastq.gz\tDRR117955_2.fastq.gz\tDRS058470\tDRS058470\t482.0\t\t\t\t\t\t\nDRR117956_1.fastq.gz\tDRR117956_2.fastq.gz\tDRS058471\tDRS058471\t482.0\t\t\t\t\t\t\n']
        self.assertListEqual(self.datasheet1.split_sequences, test_list_1)
        self.assertListEqual(self.datasheet2.split_sequences, test_list_2)

    def test_built_sequence(self):
    # runs through presence and contents checks for each file, then deletes the presence checked file to ensure validation
        if os.path.isfile('./breakpoint_testing/12345/external_12345_0.xls') == True:
            tester_file = open('./breakpoint_testing/test_external_12345_0.xls')
            forged_file = open('./breakpoint_testing/12345/external_12345_0.xls')
            self.assertEqual(forged_file.read(),
                             tester_file.read())
            forged_file.close()
            tester_file.close()
        else:
            self.assertTrue(os.path.isfile('./breakpoint_testing/12345/external_12345_0.xls'))

        if os.path.isfile('./breakpoint_testing/12345/external_12345_1.xls') == True:
            tester_file = open('./breakpoint_testing/test_external_12345_1.xls')
            forged_file = open('./breakpoint_testing/12345/external_12345_1.xls')
            self.assertEqual(forged_file.read(),
                             tester_file.read())
            forged_file.close()
            tester_file.close()
        else:
            self.assertTrue(os.path.isfile('./breakpoint_testing/12345/external_12345_1.xls'))

        if os.path.isfile('./breakpoint_testing/23456/external_23456_0.xls') == True:
            tester_file = open('./breakpoint_testing/test_external_23456_0.xls')
            forged_file = open('./breakpoint_testing/23456/external_23456_0.xls')
            self.assertEqual(forged_file.read(),
                             tester_file.read())
            forged_file.close()
            tester_file.close()
        else:
            self.assertTrue(os.path.isfile('./breakpoint_testing/23456/external_23456_0.xls'))

        if os.path.isfile('./breakpoint_testing/23456/external_23456_1.xls') == True:
            tester_file = open('./breakpoint_testing/test_external_23456_1.xls')
            forged_file = open('./breakpoint_testing/23456/external_23456_1.xls')
            self.assertEqual(forged_file.read(),
                             tester_file.read())
            forged_file.close()
            tester_file.close()
        else:
            self.assertTrue(os.path.isfile('./breakpoint_testing/23456/external_23456_1.xls'))





if __name__ == '__main__':
    file_split_tester()