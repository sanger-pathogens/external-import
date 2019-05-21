import argparse


class ArgumentParser:

    def __init__(self, validate=None, prepare=None, import_=None):
        self.validation_function = validate
        self.preparation_function = prepare
        self.import_function = import_
        pass

    def parse(self, args):
        parser = argparse.ArgumentParser(prog='external-import')
        subparsers = parser.add_subparsers(help='sub-command help')
        validation_parser = subparsers.add_parser('validate', help='Validates the spreadsheet to import')
        validation_parser.add_argument('-s', '--spreadsheet', required=True, help='Spreadsheet to validate')
        validation_parser.add_argument('-i', '--internal', dest='part_of_internal_study', action="store_true",
                                       default=False, help='External data part of an internally sequenced study')
        validation_parser.set_defaults(execute=self.validation_function)

        # Experimental => needs rewriting
        preparation_parser = subparsers.add_parser('prepare', help='Prepare the import')
        preparation_parser.add_argument('-s', '--spreadsheet', required=True, help='Spreadsheet to validate')
        preparation_parser.add_argument('-t', '--ticket', type=int, required=True, help='RT Ticket number')
        preparation_parser.add_argument('-i', '--input', required=True, help='Directory containing the read files')
        preparation_parser.add_argument('-o', '--output', required=True, help='Base directory for import datas')
        preparation_parser.set_defaults(execute=self.preparation_function)
        import_parser = subparsers.add_parser('import', help='Print the command to import the external data')
        import_parser.add_argument('-d', '--database', required=True, help='The tracking database to import into')
        import_parser.add_argument('-t', '--ticket', type=int, required=True, help='RT Ticket number')
        import_parser.add_argument('-o', '--output', required=True, help='Base directory for import datas')
        import_parser.set_defaults(execute=self.import_function)
        # End of Experimental => needs rewriting

        try:
            return parser.parse_args(args)
        except SystemExit:
            return None
