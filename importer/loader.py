import xlrd

from importer.model import Spreadsheet, RawRead


class SpreadsheetLoader:

    def __init__(self, file):
        self._file = file
        self._workbook = xlrd.open_workbook(self._file)
        self._sheet = self._workbook.sheet_by_index(0)

    def load(self):
        data_row = 0
        header_row = 0
        study = ""
        for i in range(self._sheet.nrows):
            if self._sheet.cell_value(i, 0) == 'Study Name':
                study = self._sheet.cell_value(i, 1)
            if self._sheet.cell_value(i, 0) == 'Filename':
                data_row = i + 1
                header_row = i
                break

        for i in range(self._sheet.ncols):
            if self._sheet.cell_value(header_row, i) == 'Filename':
                filename_column = i
            if self._sheet.cell_value(header_row, i) == 'Mate File':
                mate_filename_column = i
            if self._sheet.cell_value(header_row, i) == 'Sample Name':
                sample_name_column = i
            if self._sheet.cell_value(header_row, i) == 'Taxon ID':
                taxon_id_column = i
            if self._sheet.cell_value(header_row, i) == 'Library Name':
                library_name_column = i
        reads = []
        for i in range(data_row, self._sheet.nrows):
            sample_name = self.__convert_empty_to_none(self._sheet.cell_value(i, sample_name_column))
            library_name = self.__convert_empty_to_none(self._sheet.cell_value(i, library_name_column))
            if library_name is None:
                library_name = sample_name
            reads.append(RawRead(
                self.__convert_empty_to_none(self._sheet.cell_value(i, filename_column)),
                self.__convert_empty_to_none(self._sheet.cell_value(i, mate_filename_column)),
                sample_name,
                self.__convert_empty_to_none(self._sheet.cell_value(i, taxon_id_column)),
                library_name))

        return Spreadsheet(study, reads)

    def __convert_empty_to_none(self, data):
        return None if data == '' else data
