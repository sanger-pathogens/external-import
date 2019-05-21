import argparse


class ArgumentParser:

    def __init__(self, validate=None):
        self.validation_function = validate
        pass

    def parse(self, args):
        parser = argparse.ArgumentParser(prog='external-import')
        subparsers = parser.add_subparsers(help='sub-command help')
        validation_parser = subparsers.add_parser('validate', help='Validates the spreadsheet to import')
        validation_parser.add_argument('-s', '--spreadsheet', required=True, help='Spreadsheet to validate')
        validation_parser.add_argument('-i', '--internal', dest='part_of_internal_study', action="store_true",
                                       default=False, help='External data part of an internally sequenced study')
        validation_parser.set_defaults(execute=self.validation_function)

        try:
            return parser.parse_args(args)
        except SystemExit:
            return None
