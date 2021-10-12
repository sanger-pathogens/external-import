import glob
import os

class DataImporter:

    BASE_DATA_PATH = "/lustre/scratch118/infgen/pathogen/pathpipe/external_seq_data"

    @staticmethod
    def new_instance(base: str, ticket: int, database: str):
        loader_list = []
        destination = "%s/%d" % (base, ticket)
        for index, file in enumerate(glob.glob(f"{DataImporter.BASE_DATA_PATH}/{ticket}/external_{ticket}_*.xlsx",
                                               recursive=False)):
            command = DataImporter(destination, ticket, index, database)
            loader_list.append(command)
        return loader_list
    
    @staticmethod
    def get_complete_manifest_for_ticket(ticket: int):
        return f"{DataImporter.BASE_DATA_PATH}/{ticket}/complete_external_{ticket}.xlsx"

    def __init__(self, destination: str, ticket: int, index: int, database: str):
        self.destination = destination
        self.ticket = ticket
        self.index = index
        self.database = database


    @staticmethod
    def load(commands, command_file_name):
        command_file = open(f'{command_file_name}/command_file.sh','w')
        command_file.write("""#!/bin/bash

    # Execute the below to import:
""")
        command = commands[0]
        command_file.write(f"""
bsub -o {command.destination}/external_{command.ticket}_{command.index}.log -e {command.destination}/external_{command.ticket}_{command.index}.err -M2000 \\
  -J external_{command.ticket}_{command.index} -q long \\
  -R "select[mem>2000] rusage[mem=2000]" update_pipeline_from_spreadsheet.pl \\
  -d {command.database} \\
  -f {command.destination} \\
  -p /lustre/scratch118/infgen/pathogen/pathpipe/{command.database}/seq-pipelines \\
  {command.destination}/external_{command.ticket}_{command.index}.xlsx

""")
        dependency = f"external_{command.ticket}_{command.index}"
        length = len(commands) - 1
        if length >= 1:
            command_file.write(f"""
bsub -o {command.destination}/external_{command.ticket}.%J.%I.o -e {command.destination}/external_{command.ticket}.%J.%I.e -M2000 \\
  -w 'ended("{dependency}")' \\
  -J external_{command.ticket}[1-{length}]%5 -q long \\
  -R "select[mem>2000] rusage[mem=2000]" update_pipeline_from_spreadsheet.pl \\
  -d {command.database} \\
  -f {command.destination} \\
  -p /lustre/scratch118/infgen/pathogen/pathpipe/{command.database}/seq-pipelines \\
  {command.destination}/external_{command.ticket}_\$LSB_JOBINDEX.xlsx

""")
        command_file.write("""
# Then following the external data import SOP to register the study
""")

        command_file.close()
        os.chmod(f'{command_file_name}/command_file.sh', 0o755)