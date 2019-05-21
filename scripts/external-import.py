#!/usr/bin/env python3

from os import mkdir
from sys import argv

from importer.argument_parser import ArgumentParser
from importer.loader import SpreadsheetLoader
from importer.pfchecks import print_pf_checks
from importer.validation import validate_spreadsheet
from importer.writer import save, output_dir, copy_files, spreadsheet_name, import_cmd


# Experimental => needs rewriting

def validate(arguments):
    loader = SpreadsheetLoader(arguments.spreadsheet, arguments.part_of_internal_study)
    sheet = loader.load()
    result = validate_spreadsheet(sheet)
    if result:
        print(result)
    else:
        print_pf_checks(sheet, arguments.output)


def prepare(arguments):
    loader = SpreadsheetLoader(arguments.spreadsheet)
    sheet = loader.load()
    destination = output_dir(arguments.output, arguments.ticket)
    mkdir(destination)
    sheet_name = spreadsheet_name(destination, arguments.ticket)
    save(sheet, sheet_name)
    copy_files(sheet, arguments.input, destination)


def import_(arguments):
    destination = output_dir(arguments.output, arguments.ticket)
    sheet_name = spreadsheet_name(destination, arguments.ticket)
    import_cmd(args.database, destination, sheet_name)


parser = ArgumentParser(validate, prepare, import_)
args = parser.parse(argv[1:])
if args.execute is not None:
    args.execute(args)

# TODO: validate preparation on real life example
# TODO: rewrite experimental code
# TODO: check it is running as the desired user.
# TODO: move part_of_internal_study out of the loader, it's a pure validation issue
# TODO: revisit the design of validation (either object or function composition)
