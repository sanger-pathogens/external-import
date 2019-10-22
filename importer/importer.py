import glob

class DataImporter:

    @staticmethod
    def new_instance(base: str, ticket: int, database: str):
        loader_list = []
        destination = "%s/%d" % (base, ticket)
        for index, file in enumerate(glob.glob(f"/lustre/scratch118/infgen/pathogen/pathpipe/external_seq_data/{ticket}/external_{ticket}_*.xls",
                                               recursive=False)):
            command = DataImporter(destination, ticket, index, database)
            loader_list.append(command)
        return loader_list

    def __init__(self, destination: str, ticket: int, index: int, database: str):
        self.destination = destination
        self.ticket = ticket
        self.index = index
        self.database = database


    @staticmethod
    def load(commands, command_file_name):
        command_file = open(f'{command_file_name}/command_file.txt','w')
        command_file.write("""
        Execute the below to import:

cd /software/pathogen/projects/update_pipeline
""")

        for command in commands:
            command_file.write(f"""
bsub -o {command.destination}/external_{command.ticket}_{command.index}.log -e {command.destination}/external_{command.ticket}_{command.index}.err -M2000 \\
  -R "select[mem>2000] rusage[mem=2000]" './bin/update_pipeline_from_spreadsheet.pl \\
  -d {command.database} \\
  -f {command.destination} \\
  -p /lustre/scratch118/infgen/pathogen/pathpipe/{command.database}/seq-pipelines \\
  {command.destination}/external_{command.ticket}_{command.index}.xls'

""")
        command_file.write("""
Then following the external data import SOP to register the study
""")

        command_file.close()
