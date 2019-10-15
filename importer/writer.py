from os import mkdir, path
from shutil import copyfile

import xlwt

from importer.model import Spreadsheet


class Preparation:


    @staticmethod
    def new_instance(spreadsheet: Spreadsheet, base: str, ticket: int, instance: int):
        destination = "%s/%d" % (base, ticket)
        base_instance = instance
        instance += 1
        return Preparation(spreadsheet, destination, '%s/external_%d_%d.xls' % (destination, ticket, base_instance)), instance

    def __init__(self, spreadsheet: Spreadsheet, destination: str, spreadsheet_file: str):
        self.spreadsheet = spreadsheet
        self.destination = destination
        self.spreadsheet_file = spreadsheet_file

    def copy_files(self, source: str):
        for read in self.spreadsheet._sheet.reads:
            copyfile("%s/%s" % (source, read.forward_read), "%s/%s" % (self.destination, read.forward_read))
            if read.reverse_read is not None:
                copyfile("%s/%s" % (source, read.reverse_read), "%s/%s" % (self.destination, read.reverse_read))

    def save_workbook(self, workbook):
        workbook.save(self.spreadsheet_file)

    def create_destination_directory(self):
        if path.isdir(self.destination) == False:
            mkdir(self.destination)


class OutputSpreadsheetGenerator:

    def __init__(self, spreadsheet: Spreadsheet, current_position: int):
        self.spreadsheet = spreadsheet
        self.row = current_position
        self.status_closed = False
        self.workbook = xlwt.Workbook()
        self.sheet = self.workbook.add_sheet('Sheet1')

    def build(self, breakpoint: int):
        self.build_import_info()
        self.build_read_headers()
        self.build_read_data(breakpoint)
        return self.workbook, self.status_closed, self.row

    def build_import_info(self):

        self.write_string(0, 'Supplier Name', self.spreadsheet.supplier)
        self.write_string(1, 'Supplier Organisation', self.spreadsheet.organisation)
        self.write_string(2, 'Sanger Contact Name', self.spreadsheet.contact)
        self.write_string(3, 'Sequencing Technology', self.spreadsheet.technology)
        self.write_string(4, 'Study Name', self.spreadsheet.name)
        self.write_string(5, 'Study Accession number', self.spreadsheet.accession)
        self.write_string(6, 'Total size of files in GBytes', self.spreadsheet.size)
        self.write_string(7, 'Data to be kept until', self.spreadsheet.limit)

    def build_read_data(self, breakpoint: int):
        for read in range(breakpoint):
            position = read + 10
            if self.row == len(self.spreadsheet.reads):
                self.status_closed = True
                break
            self.sheet.write(position, 0, self.spreadsheet.reads[self.row].forward_read)
            if self.spreadsheet.reads[self.row].reverse_read is not None:
                self.sheet.write(position, 1, self.spreadsheet.reads[self.row].reverse_read)
            self.sheet.write(position, 2, self.spreadsheet.reads[self.row].sample_name)
            self.sheet.write(position, 4, self.spreadsheet.reads[self.row].taxon_id)
            self.sheet.write(position, 5, self.spreadsheet.reads[self.row].library_name)
            self.row += 1
        if self.row == len(self.spreadsheet.reads):
            self.status_closed = True

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
