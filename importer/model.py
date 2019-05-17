from collections import namedtuple

RawRead = namedtuple('RawRead', 'forward_read, reverse_read, sample_name, taxon_id, library_name')


class Spreadsheet:

    def __init__(self, name, reads=[], part_of_internal_sequencing_study=False):
        self.name = name
        self.reads = reads
        self.part_of_internal_sequencing_study = part_of_internal_sequencing_study
