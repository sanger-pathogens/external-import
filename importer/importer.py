class DataImporter:

    @staticmethod
    def new_instance(base: str, ticket: int, database: str):
        destination = "%s/%d" % (base, ticket)
        return DataImporter(destination, '%s/external_%d.xls' % (destination, ticket), database)

    def __init__(self, destination: str, spreadsheet_file: str, database: str):
        self.destination = destination
        self.spreadsheet_file = spreadsheet_file
        self.spreadsheet_file = spreadsheet_file
        self.database = database

    def load(self):
        print("""
        Execute the below to import:

cd /software/pathogen/projects/update_pipeline
bsub -o ~/external.log -e ~/external.err -M2000 -R "select[mem>2000] rusage[mem=2000]" './bin/update_pipeline_from_spreadsheet.pl \\
  -d %s \\
  -f %s \\
  -p /lustre/scratch118/infgen/pathogen/pathpipe/%s/seq-pipelines \\
  %s'
  
Then following the external data import SOP to register the study
        """ % (self.database, self.destination, self.database, self.spreadsheet_file))
