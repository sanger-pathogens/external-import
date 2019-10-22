import unittest
import os
import glob
from importer.importer import DataImporter
from unittest.mock import Mock, patch

OUTPUT = 'base'
TICKET = 123
DATABASE = 'database'
COMMAND_FILE_NAME = '.'
COMMAND_1 = DataImporter('base/123', 123, 0, 'database')
COMMAND_2 = DataImporter('base/123', 123, 1, 'database')
COMMANDS = [COMMAND_1, COMMAND_2]

def glob_replacer(ticket_string, recursive):
    if ticket_string != f'/lustre/scratch118/infgen/pathogen/pathpipe/external_seq_data/{TICKET}/external_{TICKET}_*.xls':
        raise Exception('Ticket lost in transfer.')
    elif recursive != False:
        raise Exception('Recursive not set to false.')
    else:
        GLOB_LIST = ['one', 'two']
        return GLOB_LIST

class importerTesting(unittest.TestCase):

    def test_importer_setup(self):
        with patch('glob.glob', side_effect=glob_replacer) as glob_mock:
            RECEIVED_LIST = DataImporter.new_instance(OUTPUT, TICKET, DATABASE)
            for MATCHING_COMMAND, CREATED_COMMAND in enumerate(RECEIVED_LIST):
                self.assertEqual(CREATED_COMMAND.destination, COMMANDS[MATCHING_COMMAND].destination)
                self.assertEqual(CREATED_COMMAND.database, COMMANDS[MATCHING_COMMAND].database)
                self.assertEqual(CREATED_COMMAND.ticket, COMMANDS[MATCHING_COMMAND].ticket)
                self.assertEqual(CREATED_COMMAND.index, COMMANDS[MATCHING_COMMAND].index)
            glob_mock.assert_called_once_with('/lustre/scratch118/infgen/pathogen/pathpipe/external_seq_data/123/external_123_*.xls', recursive=False)


    def test_importer_printout(self):
        TESTER_LINES = ['\n',
                        '        Execute the below to import:\n',
                        '\n',
                        'cd /software/pathogen/projects/update_pipeline\n',
                        '\n',
                        'bsub -o base/123/external_123_0.log -e base/123/external_123_0.err -M2000 \\\n',
                        '''  -R "select[mem>2000] rusage[mem=2000]" './bin/update_pipeline_from_spreadsheet.pl \\\n''',
                        '  -d database \\\n',
                        '  -f base/123 \\\n',
                        '  -p /lustre/scratch118/infgen/pathogen/pathpipe/database/seq-pipelines \\\n',
                        "  base/123/external_123_0.xls'\n",
                        '\n',
                        '\n',
                        'bsub -o base/123/external_123_1.log -e base/123/external_123_1.err -M2000 \\\n',
                        '''  -R "select[mem>2000] rusage[mem=2000]" './bin/update_pipeline_from_spreadsheet.pl \\\n''',
                        '  -d database \\\n',
                        '  -f base/123 \\\n',
                        '  -p /lustre/scratch118/infgen/pathogen/pathpipe/database/seq-pipelines \\\n',
                        "  base/123/external_123_1.xls'\n",
                        '\n',
                        '\n',
                        'Then following the external data import SOP to register the study\n',
                        '\n']

        DataImporter.load(COMMANDS, COMMAND_FILE_NAME)

        if os.path.isfile(f'{COMMAND_FILE_NAME}/command_file.txt'):
            TESTED_FILE = open(f'{COMMAND_FILE_NAME}/command_file.txt','r')
            for index, LINE in enumerate(TESTED_FILE):
                self.assertEqual(LINE, TESTER_LINES[index])
            os.remove(f'{COMMAND_FILE_NAME}/command_file.txt')
        else:
            No_File = 'The command_file.txt was not properly created (Does not exist).'
            raise Exception(No_File)