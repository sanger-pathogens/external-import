from collections import namedtuple

RawRead = namedtuple('RawRead', 'forward_read, reverse_read, sample_name, taxon_id, library_name')


class Spreadsheet:

    @staticmethod
    def new_instance(name, reads=[]):
        result = Spreadsheet()
        result.name = name
        result.reads = reads
        return result
