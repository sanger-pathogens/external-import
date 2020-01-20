import xlrd

from importer.model import Spreadsheet, RawRead


class SpreadsheetLoader:

    def __init__(self, file):
        self._file = file
        self._workbook = xlrd.open_workbook(self._file)
        self._sheet = self._workbook.sheet_by_index(0)

    def load(self):
        result = Spreadsheet()
        data_row = 0
        header_row = 0
        for i in range(self._sheet.nrows):
            if self._sheet.cell_value(i, 0) == 'Study Name':
                result.name = self._sheet.cell_value(i, 1)
            if self._sheet.cell_value(i, 0) == 'Supplier Name':
                result.supplier = self._sheet.cell_value(i, 1)
            if self._sheet.cell_value(i, 0) == 'Supplier Organisation':
                result.organisation = self._sheet.cell_value(i, 1)
            if self._sheet.cell_value(i, 0) == 'Sanger Contact Name':
                result.contact = self._sheet.cell_value(i, 1)
            if self._sheet.cell_value(i, 0) == 'Sequencing Technology':
                result.technology = self._sheet.cell_value(i, 1)
            if self._sheet.cell_value(i, 0) == 'Study Accession number':
                result.accession = self.__extract_text_value(i, 1)
            if self._sheet.cell_value(i, 0) == 'Total size of files in GBytes':
                result.size = self._sheet.cell_value(i, 1)
            if self._sheet.cell_value(i, 0) == 'Data to be kept until':
                year, month, day, hour, minute, second = xlrd.xldate_as_tuple(self._sheet.cell_value(i, 1),
                                                                              self._workbook.datemode)
                result.limit = "%02d/%02d/%04d" % (day, month, year)
            if self._sheet.cell_value(i, 0) == 'Filename' or self._sheet.cell_value(i, 0) == 'Run Accession':
                data_row = i + 1
                header_row = i
                break
        filename_column = None
        run_accession_column = None
        for i in range(self._sheet.ncols):
            if self._sheet.cell_value(header_row, i) == 'Filename':
                filename_column = i
            if self._sheet.cell_value(header_row, i) == 'Run Accession':
                run_accession_column = i
            if filename_column is not None:
                if self._sheet.cell_value(header_row, i) == 'Mate File':
                    mate_filename_column = i
            if run_accession_column is not None:
                if self._sheet.cell_value(header_row, i) == 'Double-ended Reads':
                    double_ended_reads_column = i
            if self._sheet.cell_value(header_row, i) == 'Sample Name':
                sample_name_column = i
            if self._sheet.cell_value(header_row, i) == 'Sample Accession number':
                sample_accession_column = i
            if self._sheet.cell_value(header_row, i) == 'Taxon ID':
                taxon_id_column = i
            if self._sheet.cell_value(header_row, i) == 'Library Name':
                library_name_column = i
        reads = []
        for i in range(data_row, self._sheet.nrows):
            sample_name = self.__extract_float_value(i, sample_name_column)
            library_name = self.__extract_float_value(i, library_name_column)
            if library_name is None:
                library_name = sample_name
            if filename_column is not None:
                reads.append(RawRead(
                    self.__extract_text_value(i, filename_column),
                    self.__extract_text_value(i, mate_filename_column),
                    sample_name,
                    self.__extract_text_value(i, sample_accession_column),
                    self.__extract_float_value(i, taxon_id_column),
                    library_name))
            if run_accession_column is not None:
                reads.append(RawRead(
                    (self.__extract_text_value(i, run_accession_column)),
                    self.__extract_text_value(i, double_ended_reads_column),
                    sample_name,
                    self.__extract_text_value(i, sample_accession_column),
                    self.__extract_float_value(i, taxon_id_column),
                    library_name))
        result.reads = reads
        return result

    def __extract_text_value(self, row, column):
        print(self._sheet.cell_value(row, column))
        new_data = self._sheet.cell_value(row, column).strip()
        return None if new_data == '' else new_data

    def __extract_float_value(self, row, column):
        if self._sheet.cell_type(row, column) != xlrd.XL_CELL_NUMBER:
            return self.__extract_text_value(row, column)
        return str(int(self._sheet.cell_value(row, column)))
