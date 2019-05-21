import xlrd

from importer.model import Spreadsheet, RawRead


class SpreadsheetLoader:

    def __init__(self, file, part_of_internally_sequenced_study=False):
        self._file = file
        self._workbook = xlrd.open_workbook(self._file)
        self._sheet = self._workbook.sheet_by_index(0)
        self.part_of_internally_sequenced_study = part_of_internally_sequenced_study

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
            sample_name = self.__extract_text_value(i, sample_name_column)
            library_name = self.__extract_text_value(i, library_name_column)
            if library_name is None:
                library_name = sample_name
            reads.append(RawRead(
                self.__extract_text_value(i, filename_column),
                self.__extract_text_value(i, mate_filename_column),
                sample_name,
                self.__extract_float_value(i, taxon_id_column),
                library_name))

        return Spreadsheet(study, reads, self.part_of_internally_sequenced_study)

    def __extract_text_value(self, row, column):
        new_data = self._sheet.cell_value(row, column).strip()
        return None if new_data == '' else new_data

    def __extract_float_value(self, row, column):
        if self._sheet.cell_type(row, column) != xlrd.XL_CELL_NUMBER:
            return self.__extract_text_value(row, column)
        return str(int(self._sheet.cell_value(row, column)))
