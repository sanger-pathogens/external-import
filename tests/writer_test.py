import unittest
from unittest.mock import patch, call
import os
import xlrd
from importer.model import Spreadsheet, RawRead
from importer.writer import Preparation, OutputSpreadsheetGenerator, create_commands, submit_commands
import pandas as pd
from testfixtures import TempDirectory

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

class TestFileDownload(unittest.TestCase):

    def setUp(self):
        self.tempdir = TempDirectory()
        self.tempdir.write('1/Accession1.fastq.gz', b'the text')
        self.tempdir.write('2/Accession1_1.fastq.gz', b'the text')
        self.tempdir.write('2/Accession1_2.fastq.gz',b'the text')
        self.tempdir_path = self.tempdir.path
        print('temp',self.tempdir_path)
        self.under_test1 = Preparation.new_instance(Spreadsheet.new_instance("MyStudy", [
            RawRead(forward_read='Accession1', reverse_read='T', sample_name='SAMPLE1',
                    taxon_id='1280', library_name='LIB1', sample_accession=None),
            RawRead(forward_read='Accession2', reverse_read='T', sample_name='SAMPLE2',
                    taxon_id='1280', library_name='LIB2', sample_accession=None)]), self.tempdir_path, 0, 0)
        self.under_test2 = Preparation.new_instance(Spreadsheet.new_instance("MyStudy", [
            RawRead(forward_read='Accession1', reverse_read='T', sample_name='SAMPLE1',
                    taxon_id='1280', library_name='LIB1', sample_accession=None),
            RawRead(forward_read='Accession2', reverse_read='T', sample_name='SAMPLE2',
                    taxon_id='1280', library_name='LIB2', sample_accession=None)]), self.tempdir_path, 1, 0)
        self.under_test3 = Preparation.new_instance(Spreadsheet.new_instance("MyStudy", [
            RawRead(forward_read='Accession1', reverse_read='T', sample_name='SAMPLE1',
                    taxon_id='1280', library_name='LIB1', sample_accession=None),
            RawRead(forward_read='Accession2', reverse_read='T', sample_name='SAMPLE2',
                    taxon_id='1280', library_name='LIB2', sample_accession=None)]), self.tempdir_path, 2, 0)

    def tearDown(self):
        self.tempdir.cleanup()
        pass

    def test_ENA_download_calls_create_commands_correctly(self):
        connections=1
        with patch("importer.writer.Preparation.create_dataframe_from_list", return_value = 'df') as mock_create_dataframe_from_list:
            with patch("importer.writer.Preparation.check_if_file_downloaded", return_value =False) as mock_check_if_file_downloaded:
                with patch("importer.writer.create_commands", return_value='df') as mock_create_commands:
                    with patch("importer.writer.submit_commands") as mock_submit_commands:
                       self.under_test1.download_files_from_ena(connections)
        mock_create_dataframe_from_list.assert_called_once_with(['Accession1','Accession2'])
        mock_create_commands.assert_called_once_with('df', 1, self.tempdir_path+'/0')
        mock_submit_commands.assert_called_once_with('df')

    def test_create_dataframe_from_list(self):
        reads = ['Accession1','Accession2']
        actual=self.under_test1.create_dataframe_from_list(reads)
        expected = pd.DataFrame(([read, 'import_%s' % read] for read in reads),
                          columns=('Read accession', 'Job_name'))
        pd.testing.assert_frame_equal(actual,expected)

    def test_check_if_file_downloaded_no_files(self):
        actual=self.under_test1.check_if_file_downloaded('Accession1')
        self.assertEqual(actual,False)

    def test_check_if_file_downloaded_single_ended_exists(self):
        actual=self.under_test2.check_if_file_downloaded('Accession1')
        self.assertEqual(actual,True)

    def test_check_if_file_downloaded_double_ended_exists(self):
        actual=self.under_test3.check_if_file_downloaded('Accession1')
        self.assertEqual(actual,True)


class TestCreateCommands(unittest.TestCase):

    def setUp(self):
        self.ena_command_path='enaDataGet'
        self.memory= "-M2000 -R 'select[mem>2000] rusage[mem=2000]'"
        self.mv_accession1_command = 'mv destination/Accession1/* destination  && rm -rf destination/Accession1'
        self.mv_accession2_command = 'mv destination/Accession2/* destination  && rm -rf destination/Accession2'
        self.job_name1 = 'import_Accession1'
        self.job_name2 = 'import_Accession2'
        self.reads = ['Accession1', 'Accession2']
        self.df = pd.DataFrame(([read, 'import_%s' % read] for read in self.reads),
                                columns=('Read accession', 'Job_name'))

    def test_dataframe_commands_entered_correctly_connection1(self):
        actual_df=create_commands(self.df,1,'destination')
        d={'Read accession': self.reads, 'Job_name': [self.job_name1,self.job_name2],
              'enaDataGet_command':[self.ena_command_path+' -f fastq -d destination Accession1',self.ena_command_path+' -f fastq -d destination Accession2'],
              'extract_data_command':[self.mv_accession1_command,self.mv_accession2_command],
              'Command':['bsub -o destination/Accession1.o -e destination/Accession1.e '+self.memory+'  -J import_Accession1 "'+self.ena_command_path+' -f fastq -d destination Accession1 && '+self.mv_accession1_command+'"',
                         'bsub -o destination/Accession2.o -e destination/Accession2.e '+self.memory+'  -J import_Accession2 -w import_Accession1 "'+self.ena_command_path+' -f fastq -d destination Accession2 && '+self.mv_accession2_command+'"'],
              'Job_to_depend_on':[None,'import_Accession1']}
        expected_df = pd.DataFrame(data=d)
        pd.testing.assert_frame_equal(actual_df,expected_df)

    def test_dataframe_commands_entered_correctly_connections3(self):
        actual_df = create_commands(self.df,3,'destination')

        d = {'Read accession': self.reads, 'Job_name': [self.job_name1, self.job_name2],
             'enaDataGet_command': [self.ena_command_path + ' -f fastq -d destination Accession1',
                                    self.ena_command_path + ' -f fastq -d destination Accession2'],
             'extract_data_command': [self.mv_accession1_command, self.mv_accession2_command],
             'Command': [
                 'bsub -o destination/Accession1.o -e destination/Accession1.e ' + self.memory + '  -J import_Accession1 "' + self.ena_command_path + ' -f fastq -d destination Accession1 && ' + self.mv_accession1_command + '"',
                 'bsub -o destination/Accession2.o -e destination/Accession2.e ' + self.memory + '  -J import_Accession2 "' + self.ena_command_path + ' -f fastq -d destination Accession2 && ' + self.mv_accession2_command + '"'],
             }
        expected_df = pd.DataFrame(data=d)
        pd.testing.assert_frame_equal(actual_df, expected_df)

class TestSubmitCommands(unittest.TestCase):

    def setUp(self):
        self.ena_command_path='enaDataGet'
        self.memory= "-M2000 -R 'select[mem>2000] rusage[mem=2000]'"
        self.mv_accession1_command = 'mv destination/Accession1/* destination  && rm -rf destination/Accession1'
        self.mv_accession2_command = 'mv destination/Accession2/* destination  && rm -rf destination/Accession2'
        self.job_name1 = 'import_Accession1'
        self.job_name2 = 'import_Accession2'
        self.reads = ['Accession1', 'Accession2']
        self.df = pd.DataFrame(([read, 'import_%s' % read] for read in self.reads),
                                columns=('Read accession', 'Job_name'))

    @patch('importer.writer.runrealcmd')
    def test_submit_commands_no_job_dependency(self,runrealcmd_patch):
        d = {'Read accession': self.reads, 'Job_name': [self.job_name1, self.job_name2],
             'enaDataGet_command': [self.ena_command_path + ' -f fastq -d destination Accession1',
                                    self.ena_command_path + ' -f fastq -d destination Accession2'],
             'extract_data_command': [self.mv_accession1_command, self.mv_accession2_command],
             'Command': [
                 'bsub -o destination/Accession1.o -e destination/Accession1.e ' + self.memory + '  -J import_Accession1 "' + self.ena_command_path + ' -f fastq -d destination Accession1 && ' + self.mv_accession1_command + '"',
                 'bsub -o destination/Accession2.o -e destination/Accession2.e ' + self.memory + '  -J import_Accession2 "' + self.ena_command_path + ' -f fastq -d destination Accession2 && ' + self.mv_accession2_command + '"'],
             }
        df = pd.DataFrame(data=d)
        submit_commands(df)
        self.assertEqual(runrealcmd_patch.call_args_list,
                        [call('bsub -o destination/Accession1.o -e destination/Accession1.e -M2000 -R \'select[mem>2000] rusage[mem=2000]\'  -J import_Accession1 "enaDataGet -f fastq -d destination Accession1 && mv destination/Accession1/* destination  && rm -rf destination/Accession1"'),
                         call('bsub -o destination/Accession2.o -e destination/Accession2.e -M2000 -R \'select[mem>2000] rusage[mem=2000]\'  -J import_Accession2 "enaDataGet -f fastq -d destination Accession2 && mv destination/Accession2/* destination  && rm -rf destination/Accession2"')])

    @patch('importer.writer.runrealcmd')
    def test_submit_commands_with_job_dependency(self,runrealcmd_patch):
        d = {'Read accession': self.reads, 'Job_name': [self.job_name1, self.job_name2],
             'enaDataGet_command': [self.ena_command_path + ' -f fastq -d destination Accession1',
                                    self.ena_command_path + ' -f fastq -d destination Accession2'],
             'extract_data_command': [self.mv_accession1_command, self.mv_accession2_command],
             'Command': [
                 'bsub -o destination/Accession1.o -e destination/Accession1.e ' + self.memory + '  -J import_Accession1 "' + self.ena_command_path + ' -f fastq -d destination Accession1 && ' + self.mv_accession1_command + '"',
                 'bsub -o destination/Accession2.o -e destination/Accession2.e ' + self.memory + '  -J import_Accession2 -w import_Accession1 "' + self.ena_command_path + ' -f fastq -d destination Accession2 && ' + self.mv_accession2_command + '"'],
             }
        df = pd.DataFrame(data=d)
        submit_commands(df)
        self.assertEqual(runrealcmd_patch.call_args_list,
                         [call('bsub -o destination/Accession1.o -e destination/Accession1.e -M2000 -R \'select[mem>2000] rusage[mem=2000]\'  -J import_Accession1 "enaDataGet -f fastq -d destination Accession1 && mv destination/Accession1/* destination  && rm -rf destination/Accession1"'),
                          call('bsub -o destination/Accession2.o -e destination/Accession2.e -M2000 -R \'select[mem>2000] rusage[mem=2000]\'  -J import_Accession2 -w import_Accession1 "enaDataGet -f fastq -d destination Accession2 && mv destination/Accession2/* destination  && rm -rf destination/Accession2"')])

    @patch('importer.writer.runrealcmd')
    def test_submit_commands_on_df_with_no_commands(self,runrealcmd_patch):
        df = pd.DataFrame([] ,columns=('Read accession', 'Job_name'))
        submit_commands(df)
        runrealcmd_patch.assert_not_called()


class TestXlsGeneration(unittest.TestCase):
    data_dir = os.path.dirname(os.path.abspath(__file__))

    def test_of_OutputSpreadsheetGenerator_for_copy(self):
        sheet = self.make_spreadsheet_for_copy()
        self.run_function(sheet)
        self.run_workbook_assertions()
        os.remove('workbook.xls')

    def test_of_OutputSpreadsheetGenerator_for_download(self):
        sheet = self.make_spreadsheet_for_ena_download()
        self.run_function(sheet)
        self.run_workbook_assertions()
        os.remove('workbook.xls')

    def run_workbook_assertions(self):
        WORKBOOK_UNDER_TEST = xlrd.open_workbook('workbook.xls')
        SHEET_UNDER_TEST = WORKBOOK_UNDER_TEST.sheet_by_index(0)
        BREAKPOINT_SPREADSHEET = xlrd.open_workbook(os.path.join(self.data_dir, 'test_breakpoint_functionality.xls'))
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

    def run_function(self, sheet):
        generator = OutputSpreadsheetGenerator(sheet, A_POSITION)
        workbook, file_ended, current_position = generator.build(A_BREAKPOINT, False)
        workbook.save('workbook.xls')
        self.assertEqual((current_position, file_ended), (2, True))
        return current_position, file_ended

    def make_spreadsheet_for_copy(self):
        sheet = Spreadsheet()
        sheet.supplier, sheet.organisation, sheet.contact, sheet.technology, sheet.name, sheet.accession, sheet.size, \
        sheet.limit = ('Supplier', 'Org', 'Contact', 'Illumina', 'AStudyName1', None, 1.90, '01/01/2025')
        sheet.reads = [RawRead(forward_read='PAIR1_1.fastq.gz', reverse_read='PAIR1_2.fastq.gz', sample_name='SAMPLE1',
                               taxon_id='1280', library_name='LIB1', sample_accession=None),
                       RawRead(forward_read='SECONDLINE.fastq.gz', reverse_read=None, sample_name='SAMPLE2',
                               taxon_id='1280', library_name='LIB2', sample_accession=None)]
        return sheet

    def make_spreadsheet_for_ena_download(self):
        sheet = Spreadsheet()
        sheet.supplier, sheet.organisation, sheet.contact, sheet.technology, sheet.name, sheet.accession, sheet.size, \
        sheet.limit = ('Supplier', 'Org', 'Contact', 'Illumina', 'AStudyName1', None, 1.90, '01/01/2025')
        sheet.reads = [RawRead(forward_read='PAIR1', reverse_read='T', sample_name='SAMPLE1',
                               taxon_id='1280', library_name='LIB1', sample_accession=None),
                       RawRead(forward_read='Pair2.fastq.gz', reverse_read='F', sample_name='SAMPLE2',
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
