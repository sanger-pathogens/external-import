import xlrd


class SpreadsheetLoader:

    def __init__(self, file):
        self._file = file
        self._workbook = xlrd.open_workbook(self._file)
        self._sheet = self._workbook.sheet_by_index(0)

    def load(self):
        return self._sheet.nrows
