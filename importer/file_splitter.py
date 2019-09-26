import xlrd

class Spreadsheet_Splitter:

    def __init__(self, output, ticket, read_length=150):
        ''' Runs full script for separating the spreadsheet to correct sizes '''
        spreadsheet = f'{output}/{ticket}/external_{ticket}.xls'
        self.header = Spreadsheet_Splitter.header_getter(self, spreadsheet)
        self.split_sequences = Spreadsheet_Splitter.part_builder(self, spreadsheet, read_length)
        Spreadsheet_Splitter.build_sequences(self, ticket, output)

    def header_getter(self, spreadsheet):
        '''Takes the header from the spreadsheet given and stores it'''
        head_set = xlrd.open_workbook(spreadsheet, 'r')
        sheet = head_set.sheet_by_index(0)
        header = ''
        for i in range(10):
            for col in range(sheet.ncols):
                if sheet.cell_type(i, col) not in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
                    if sheet.cell_value(i, 0) == 'Data to be kept until':
                        year, month, day, *rest = xlrd.xldate_as_tuple(sheet.cell_value(i, 1), head_set.datemode)
                        header = header + str(sheet.cell_value(i, 0)) + '\t' + (f'{day}/{month}/{year}\t')
                        i += 1
                    else:
                        header = header + str(sheet.cell_value(i, col)) + '\t'
            header = header + ' \n'
        return header

    def part_builder(self, spreadsheet, read_length):
        ''' Takes the rows of gene data and generates a list from sets of them '''
        head_set = xlrd.open_workbook(spreadsheet, 'r')
        sheet = head_set.sheet_by_index(0)
        init = 10
        reads = []
        read_body = ''
        while init != sheet.nrows:
            for i in range(read_length):
                if init == sheet.nrows:
                    break
                for col in range(sheet.ncols):
                    read_body = read_body + str(sheet.cell_value(init, col)) + '\t'
                init += 1
                read_body = read_body + '\n'
            reads.append(read_body)
            read_body = ''
        return reads


    def build_sequences(self, ticket, directory):
        ''' Uses header and list to build new files '''
        for seq_strip in range(len(self.split_sequences)):
            log = self.header + self.split_sequences[seq_strip]
            written_file = open('{}/{}/external_{}_{}.xls'.format(directory, ticket, ticket, seq_strip), 'w')
            written_file.write(log)
            written_file.close()