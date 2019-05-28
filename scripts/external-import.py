#!/usr/bin/env python3

import argparse
from sys import argv

from importer.argument_parser import ArgumentParser
from importer.importer import DataImporter
from importer.loader import SpreadsheetLoader
from importer.pfchecks import print_pf_checks
from importer.validation import validate_spreadsheet
from importer.writer import Preparation, \
    OutputSpreadsheetGenerator


def validate(arguments: argparse.Namespace):
    loader = SpreadsheetLoader(arguments.spreadsheet)
    sheet = loader.load()
    result = validate_spreadsheet(sheet, arguments.part_of_internal_study)
    if result:
        print(result)
    else:
        print_pf_checks(sheet, arguments.output)


def prepare(arguments: argparse.Namespace):
    loader = SpreadsheetLoader(arguments.spreadsheet)
    sheet = loader.load()
    generator = OutputSpreadsheetGenerator(sheet)
    workbook = generator.build()
    preparation = Preparation.new_instance(sheet, arguments.output, arguments.ticket)
    preparation.create_destination_directory()
    preparation.copy_files(arguments.input)
    preparation.save_workbook(workbook)


def load(arguments: argparse.Namespace):
    importer = DataImporter.new_instance(arguments.output, arguments.ticket, arguments.database)
    importer.load()


parser = ArgumentParser(validate, prepare, load)
args = parser.parse(argv[1:])
if args is not None and args.execute is not None:
    args.execute(args)

# TODO: check it is running as the desired user.
# TODO: revisit the design of validation (either object or function composition)
# TODO: Add validation for unused fields in header (Supplier Name, etc....)
