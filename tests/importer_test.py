import unittest
import os
from importer.importer import DataImporter
from unittest.mock import patch

OUTPUT = 'base'
TICKET = 123
DATABASE = 'database'
COMMAND_FILE_NAME = '/tmp'
COMMAND_1 = DataImporter('base/123', 123, 0, 'database')
COMMAND_2 = DataImporter('base/123', 123, 1, 'database')
COMMAND_3 = DataImporter('base/123', 123, 2, 'database')
COMMANDS = [COMMAND_1, COMMAND_2, COMMAND_3]

def glob_replacer(ticket_string, recursive):
    if ticket_string != f'/lustre/scratch118/infgen/pathogen/pathpipe/external_seq_data/{TICKET}/external_{TICKET}_*.xls':
        raise Exception('Ticket lost in transfer.')
    elif recursive != False:
        raise Exception('Recursive not set to false.')
    else:
        GLOB_LIST = ['one', 'two', 'three']
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
        TESTER_LINES = ['#!/bin/bash\n',
            '\n',
            '    # Execute the below to import:\n',
            '\n',
            f'bsub -o {OUTPUT}/{TICKET}/external_{TICKET}_0.log -e {OUTPUT}/{TICKET}/external_{TICKET}_0.err -M2000 \\\n',
            f'  -J external_{TICKET}_0 -q long \\\n',
            '''  -R "select[mem>2000] rusage[mem=2000]" 'update_pipeline_from_spreadsheet.pl \\\n''',
            f'  -d {DATABASE} \\\n',
            f'  -f {OUTPUT}/{TICKET} \\\n',
            f'  -p /lustre/scratch118/infgen/pathogen/pathpipe/{DATABASE}/seq-pipelines \\\n',
            f"  {OUTPUT}/{TICKET}/external_{TICKET}_0.xls'\n",
            '\n',
            '\n',
            f'bsub -o {OUTPUT}/{TICKET}/external_{TICKET}.%J.%I.o -e {OUTPUT}/{TICKET}/external_{TICKET}.%J.%I.e -M2000 \\\n',
            f'  -w ended(external_{TICKET}_0) \\\n',
            f'  -J external_{TICKET}[1-2]%5 -q long \\\n',
            '''  -R "select[mem>2000] rusage[mem=2000]" 'update_pipeline_from_spreadsheet.pl \\\n''',
            f'  -d {DATABASE} \\\n',
            f'  -f {OUTPUT}/{TICKET} \\\n',
            f'  -p /lustre/scratch118/infgen/pathogen/pathpipe/{DATABASE}/seq-pipelines \\\n',
            f"  {OUTPUT}/{TICKET}/external_{TICKET}_\$LSB_JOBINDEX.xls'\n",
            '\n',
            '\n',
            '# Then following the external data import SOP to register the study\n',
            '\n']

        DataImporter.load(COMMANDS, COMMAND_FILE_NAME)

        if os.path.isfile(f'/tmp/command_file.sh'):
            TESTED_FILE = open(f'{COMMAND_FILE_NAME}/command_file.sh')
            for index, LINE in enumerate(TESTED_FILE):
                self.assertEqual(LINE, TESTER_LINES[index])
        else:
            self.fail('The command_file.sh was not properly created in /tmp.')

    def test_importer_printout_2_jobs(self):
        TESTER_LINES = ['#!/bin/bash\n',
            '\n',
            '    # Execute the below to import:\n',
            '\n',
            f'bsub -o {OUTPUT}/{TICKET}/external_{TICKET}_0.log -e {OUTPUT}/{TICKET}/external_{TICKET}_0.err -M2000 \\\n',
            f'  -J external_{TICKET}_0 -q long \\\n',
            '''  -R "select[mem>2000] rusage[mem=2000]" 'update_pipeline_from_spreadsheet.pl \\\n''',
            f'  -d {DATABASE} \\\n',
            f'  -f {OUTPUT}/{TICKET} \\\n',
            f'  -p /lustre/scratch118/infgen/pathogen/pathpipe/{DATABASE}/seq-pipelines \\\n',
            f"  {OUTPUT}/{TICKET}/external_{TICKET}_0.xls'\n",
            '\n',
            '\n',
            f'bsub -o {OUTPUT}/{TICKET}/external_{TICKET}.%J.%I.o -e {OUTPUT}/{TICKET}/external_{TICKET}.%J.%I.e -M2000 \\\n',
            f'  -w ended(external_{TICKET}_0) \\\n',
            f'  -J external_{TICKET}[1-1]%5 -q long \\\n',
            '''  -R "select[mem>2000] rusage[mem=2000]" 'update_pipeline_from_spreadsheet.pl \\\n''',
            f'  -d {DATABASE} \\\n',
            f'  -f {OUTPUT}/{TICKET} \\\n',
            f'  -p /lustre/scratch118/infgen/pathogen/pathpipe/{DATABASE}/seq-pipelines \\\n',
            f"  {OUTPUT}/{TICKET}/external_{TICKET}_\$LSB_JOBINDEX.xls'\n",
            '\n',
            '\n',
            '# Then following the external data import SOP to register the study\n',
            '\n']

        DataImporter.load([COMMAND_1, COMMAND_2], COMMAND_FILE_NAME)

        if os.path.isfile(f'/tmp/command_file.sh'):
            TESTED_FILE = open(f'{COMMAND_FILE_NAME}/command_file.sh')
            for index, LINE in enumerate(TESTED_FILE):
                self.assertEqual(LINE, TESTER_LINES[index])
        else:
            self.fail('The command_file.sh was not properly created in /tmp.')

    def test_importer_printout_single_job(self):
        TESTER_LINES = ['#!/bin/bash\n',
            '\n',
            '    # Execute the below to import:\n',
            '\n',
            f'bsub -o {OUTPUT}/{TICKET}/external_{TICKET}_0.log -e {OUTPUT}/{TICKET}/external_{TICKET}_0.err -M2000 \\\n',
            f'  -J external_{TICKET}_0 -q long \\\n',
            '''  -R "select[mem>2000] rusage[mem=2000]" 'update_pipeline_from_spreadsheet.pl \\\n''',
            f'  -d {DATABASE} \\\n',
            f'  -f {OUTPUT}/{TICKET} \\\n',
            f'  -p /lustre/scratch118/infgen/pathogen/pathpipe/{DATABASE}/seq-pipelines \\\n',
            f"  {OUTPUT}/{TICKET}/external_{TICKET}_0.xls'\n",
            '\n',
            '\n',
            '# Then following the external data import SOP to register the study\n',
            '\n']

        DataImporter.load([COMMAND_1], COMMAND_FILE_NAME)

        if os.path.isfile(f'/tmp/command_file.sh'):
            TESTED_FILE = open(f'{COMMAND_FILE_NAME}/command_file.sh')
            for index, LINE in enumerate(TESTED_FILE):
                self.assertEqual(LINE, TESTER_LINES[index])
        else:
            self.fail('The command_file.sh was not properly created in /tmp.')