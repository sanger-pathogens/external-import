from os import mkdir
from shutil import copyfile

import xlwt

from importer.model import Spreadsheet


class Preparation:

    @staticmethod
    def new_instance(spreadsheet: Spreadsheet, base: str, ticket: int):
        destination = "%s/%d" % (base, ticket)
        return Preparation(spreadsheet, destination, '%s/external_%d.xls' % (destination, ticket))

    def __init__(self, spreadsheet: Spreadsheet, destination: str, spreadsheet_file: str):
        self.spreadsheet = spreadsheet
        self.destination = destination
        self.spreadsheet_file = spreadsheet_file

    def copy_files(self, source: str):
        for read in self.spreadsheet.reads:
            copyfile("%s/%s" % (source, read.forward_read), "%s/%s" % (self.destination, read.forward_read))
            if read.reverse_read is not None:
                copyfile("%s/%s" % (source, read.reverse_read), "%s/%s" % (self.destination, read.reverse_read))

    def save_workbook(self, workbook):
        workbook.save(self.spreadsheet_file)

    def create_destination_directory(self):
        mkdir(self.destination)


class OutputSpreadsheetGenerator:

    def __init__(self, spreadsheet: Spreadsheet):
        self.spreadsheet = spreadsheet
        self.workbook = xlwt.Workbook()
        self.sheet = self.workbook.add_sheet('Sheet1')

    def build(self):
        self.build_import_info()
        self.build_read_headers()
        self.build_read_data()
        return self.workbook

    def build_import_info(self):
        self.not_applicable(0, 'Supplier Name')
        self.not_applicable(1, 'Supplier Organisation')
        self.not_applicable(2, 'Sanger Contact Name')
        self.not_applicable(3, 'Sequencing Technology')
        self.write_string(4, 'Study Name', self.spreadsheet.name)
        self.not_applicable(5, 'Study Accession number')
        self.not_applicable(6, 'Total size of files in GBytes')
        self.not_applicable(7, 'Data to be kept until')

    def build_read_data(self):
        row = 10
        for read in self.spreadsheet.reads:
            self.sheet.write(row, 0, read.forward_read)
            if read.reverse_read is not None:
                self.sheet.write(row, 1, read.reverse_read)
            self.sheet.write(row, 2, read.sample_name)
            self.sheet.write(row, 4, read.taxon_id)
            self.sheet.write(row, 5, read.library_name)
            row += 1

    def build_read_headers(self):
        index = 0
        for header in ['Filename', 'Mate File', 'Sample Name', 'Sample Accession number', 'Taxon ID', 'Library Name',
                       'Fragment Size', 'Read Count', 'Base Count', 'Comments']:
            self.sheet.write(9, index, header)
            index += 1

    def not_applicable(self, row, title):
        self.write_string(row, title, 'Unused field')

    def write_string(self, row, title, value):
        self.sheet.write(row, 0, title)
        self.sheet.write(row, 1, value)
