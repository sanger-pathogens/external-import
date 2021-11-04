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
    result = validate_spreadsheet(sheet, arguments.part_of_internal_study, arguments.download)
    if result:
        print(result)
    else:
        print_pf_checks(sheet, arguments.output,arguments.download)


def prepare(arguments: argparse.Namespace):
    loader = SpreadsheetLoader(arguments.spreadsheet)
    sheet = loader.load()

    generator = OutputSpreadsheetGenerator(sheet, 0)
    workbook, file_ended, current_position = generator.build(0, arguments.download)
    preparation = Preparation.new_instance_complete(sheet, arguments.output, arguments.ticket)
    preparation.create_destination_directory()
    preparation.save_workbook(workbook)
    if arguments.download:
        preparation.download_files_from_ena(connections=arguments.connections)

    else:
        preparation.copy_files(arguments.input)

def split_spreadsheet_by_breakpoint(sheet,arguments):
    file_ended = False
    instance = 0
    current_position = 0
    while file_ended == False:
        generator = OutputSpreadsheetGenerator(sheet, current_position)
        workbook, file_ended, current_position = generator.build(arguments.breakpoint, False)
        preparation = Preparation.new_instance(sheet, arguments.output, arguments.ticket, instance)
        preparation.create_destination_directory()
        preparation.save_workbook(workbook)
        instance += 1

def load(arguments: argparse.Namespace):
    # Split complete spreadsheet by breakpoint
    complete_spreadsheet = DataImporter.get_complete_manifest_for_ticket(arguments.ticket, arguments.output)
    loader = SpreadsheetLoader(complete_spreadsheet)
    sheet = loader.load()
    split_spreadsheet_by_breakpoint(sheet, arguments)

    # Do load
    importer = DataImporter.new_instance(arguments.output, arguments.ticket, arguments.database)
    DataImporter.load(importer, arguments.commands)


parser = ArgumentParser(validate, prepare, load)
args = parser.parse(argv[1:])
if args is not None and args.execute is not None:
    args.execute(args)

# TODO: check it is running as the desired user.
# TODO: revisit the design of validation (either object or function composition)
# TODO: Add validation for unused fields in header (Supplier Name, etc....)
# TODO: fix copy file tests in writer test module
# TODO: alter importer test to use temporary files