import unittest
import os
from importer.importer import DataImporter
from unittest.mock import patch

COMMAND_FILE_NAME = '.'
COMMAND_1 = DataImporter('base/123', 123, 0, 'database')
COMMAND_2 = DataImporter('base/123', 123, 1, 'database')
COMMANDS = [COMMAND_1, COMMAND_2]

class importerTesting(unittest.TestCase):

    def test_importer_setup(self):
        #TODO return glob as 2 item list -- compare the returned list to the initiated list -- assert glob called correctly
        #with patch(importer.importer.glob.) as
        # @staticmethod
        # def new_instance(base: str, ticket: int, database: str):
        #     loader_list = []
        #     destination = "%s/%d" % (base, ticket)
        #     for index, file in enumerate(glob.glob(
        #             f"/lustre/scratch118/infgen/pathogen/pathpipe/external_seq_data/{ticket}/external_{ticket}_*.xls",
        #             recursive=False)):
        #         command = DataImporter(destination, ticket, index, database)
        #         loader_list.append(command)
        #     return loader_list
        #
        # def __init__(self, destination: str, ticket: int, index: int, database: str):
        #     self.destination = destination
        #     self.ticket = ticket
        #     self.index = index
        #     self.database = database
        pass

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