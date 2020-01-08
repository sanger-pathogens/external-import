import argparse


class ArgumentParser:

    def __init__(self, validate=None, prepare=None, load=None):
        self.validation_function = validate
        self.preparation_function = prepare
        self.load_function = load
        self.parser = self._build_parser()
        pass

    def parse(self, args):
        try:
            return self.parser.parse_args(args)
        except SystemExit:
            return None

    def _build_parser(self):
        parser = argparse.ArgumentParser(prog='external-import')
        subparsers = parser.add_subparsers(help='sub-command help')
        self._build_validation_sub_parser(subparsers.add_parser('validate', help='Validates the spreadsheet to import'))
        self._build_preparation_parser(subparsers.add_parser('prepare', help='Prepare the import'))
        self._build_load_parser(subparsers.add_parser('load', help='Print the command to import the external data'))
        return parser

    def _build_load_parser(self, load_parser):
        load_parser.add_argument('-d', '--database', required=True, help='The tracking database to import into')
        load_parser.add_argument('-t', '--ticket', type=int, required=True, help='RT Ticket number')
        load_parser.add_argument('-o', '--output', required=True, help='Base directory for import data')
        load_parser.add_argument('-c', '--commands', required=True, help='Directory for command file')
        load_parser.set_defaults(execute=self.load_function)

    def _build_preparation_parser(self, preparation_parser):
        preparation_parser.add_argument('-s', '--spreadsheet', required=True, help='Spreadsheet to validate')
        preparation_parser.add_argument('-t', '--ticket', type=int, required=True, help='RT Ticket number')
        group = preparation_parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-i', '--input', help='Directory containing the read files to be copied.')
        group.add_argument('-dl', '--download', help='Use this flag to download the fastq files from ENA', action='store_true')
        group2 = parser.add_mutually_exclusive_group(required=True)
        group2.add_argument('--single-ended', help='Use this flag for single-ended reads', action='store_true')
        group2.add_argument('--double-ended', help='Use this flag for double-ended reads')
        preparation_parser.add_argument('-c', '--connections', type=int, choices=range(1,100), default=10, metavar='range[1,1000]',
                                        help='Number of connections to ENA to be made at a time if files are to be downloaded. Default is 10.')
        preparation_parser.add_argument('-o', '--output', required=True, help='Base directory for import datas')
        preparation_parser.add_argument('-b', '--breakpoint', type=int, required=False, default=0,
                                        help='Breakpoint to split spreadsheet, default is no breaking')
        preparation_parser.set_defaults(execute=self.preparation_function)

    def _build_validation_sub_parser(self, validation_parser):
        validation_parser.add_argument('-s', '--spreadsheet', required=True, help='Spreadsheet to validate')
        validation_parser.add_argument('-i', '--internal', dest='part_of_internal_study', action="store_true",
                                       default=False, help='External data part of an internally sequenced study')
        validation_parser.add_argument('-o', '--output', required=True,
                                       help='Output director for generated lane and sample files for pf')
        group = preparation_parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-cp', '--input', help='Spreadsheet is prepared to copy reads from existing files.')
        group.add_argument('-dl', '--download', help='Spreadsheet is prepared to download reads from ENA',
                           action='store_true')
        validation_parser.set_defaults(execute=self.validation_function)