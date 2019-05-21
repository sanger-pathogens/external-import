#!/usr/bin/env python3

from sys import argv

from importer.argument_parser import ArgumentParser
from importer.loader import SpreadsheetLoader
from importer.pfchecks import print_pf_checks
from importer.validation import validate_spreadsheet


def validate(args):
    loader = SpreadsheetLoader(args.spreadsheet, args.part_of_internal_study)
    sheet = loader.load()
    result = validate_spreadsheet(sheet)
    if result:
        print(result)
    else:
        print_pf_checks(sheet)


parser = ArgumentParser(validate)
args = parser.parse(argv[1:])
args.execute(args)


# TODO Save the spreadsheet as external_XXXX.xls where XXXX is the RT ticket number
