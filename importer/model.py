from collections import namedtuple

RawRead = namedtuple('RawRead', 'forward_read, reverse_read, sample_name, taxon_id, library_name')

class Spreadsheet:

    def __init__(self, name, reads=[]):
        self.name = name
        self.reads = reads

