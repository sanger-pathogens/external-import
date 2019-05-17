#!/usr/bin/env python3

from model import Spreadsheet, RawRead
from pfchecks import print_pf_checks

print_pf_checks(Spreadsheet("hello", [RawRead(forward_read='PAIR1_1.fastq.gz', reverse_read='PAIR1_2.fastq.gz',
                                              sample_name='SAMPLE1', taxon_id="1280", library_name='LIB1'),
                                      RawRead(forward_read='PAIR2_1.fastq.gz', reverse_read='PAIR2_2.fastq.gz',
                                              sample_name='SAMPLE2', taxon_id="1280", library_name='LIB2')]))
