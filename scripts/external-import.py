#!/usr/bin/env python3

from model import Spreadsheet, RawRead
from pfchecks import print_pf_checks

print_pf_checks(Spreadsheet("hello", [RawRead(forward_read='PAIR1_1.fastq.gz', reverse_read='PAIR1_2.fastq.gz',
                                              sample_name='SAMPLE1', taxon_id="1280", library_name='LIB1'),
                                      RawRead(forward_read='PAIR2_1.fastq.gz', reverse_read='PAIR2_2.fastq.gz',
                                              sample_name='SAMPLE2', taxon_id="1280", library_name='LIB2')]))

# TODO Create args (spreadsheet, rt number, whether sheet is part of an internal sequencing study), load the sheet
# Todo validate it
# print the pf command
# TODO Save the spreadsheet as external_XXXX.xls where XXXX is the RT ticket number
