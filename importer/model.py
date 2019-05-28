from collections import namedtuple

RawRead = namedtuple('RawRead', 'forward_read, reverse_read, sample_name, sample_accession, taxon_id, library_name')


class Spreadsheet:

    @staticmethod
    def new_instance(name, reads=[], accession='', contact='', organisation='', size=0, supplier='', technology='',
                     limit=''):
        result = Spreadsheet()
        result.name = name
        result.reads = reads
        result.accession = accession
        result.contact = contact
        result.organisation = organisation
        result.size = size
        result.supplier = supplier
        result.technology = technology
        result.limit = limit
        return result
