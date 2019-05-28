import unittest

from importer.model import Spreadsheet, RawRead
from importer.validation import validate_study_name, validate_study_name_length, validate_mandatory_read_fields, \
    validate_files_are_compressed, validate_pair_naming_convention, validate_uniqueness_of_reads, \
    validate_no_path_in_filename, validate_external_data_part_of_internal_sequencing_study_name


class TestStudyNameContent(unittest.TestCase):

    def test_study_name_with_valid_char_should_pass_validation(self):
        self.assertEqual([], validate_study_name(Spreadsheet.new_instance("ValidName12345__")))

    def test_study_name_with_invalid_char_should_fail_validation(self):
        self.assertEqual(34,
                         len(validate_study_name(Spreadsheet.new_instance("!\"£$%^&*()+={}[]:@~;'#?/>.<,|\\`¬ \t"))))


class TestStudyNameLength(unittest.TestCase):
    def test_study_name_of_15_chars_or_less_are_valid(self):
        self.assertEqual([], validate_study_name_length(Spreadsheet.new_instance("123456789012345")))

    def test_study_name_of_15_chars_or_less_without_external_suffix_are_valid(self):
        self.assertEqual([], validate_study_name_length(Spreadsheet.new_instance("123456789012345_external")))

    def test_study_name_longer_than_15_characters_should_fail(self):
        self.assertEqual(["Spreadsheet name is longer than 15 chars"],
                         validate_study_name_length(Spreadsheet.new_instance("1234567890123456")))

    def test_study_name_longer_than_15_without_external_suffix_are_valid(self):
        self.assertEqual(["Spreadsheet name excluding '_external' suffix is longer than 15 chars"],
                         validate_study_name_length(Spreadsheet.new_instance("1234567890123456_external")))


class TestStudyNameWhenPartOfInternalSequencing(unittest.TestCase):

    def test_invalid_name_for_external_data_part_of_internal_study(self):
        self.assertEqual(["Data part of internal sequencing study should have the suffix '_external' in the name: "
                          "ValidName12345__"],
                         validate_external_data_part_of_internal_sequencing_study_name(
                             Spreadsheet.new_instance("ValidName12345__", [])))

    def test_valid_name_for_external_data_part_of_internal_study(self):
        self.assertEqual([], validate_external_data_part_of_internal_sequencing_study_name(
            Spreadsheet.new_instance("345_external", [])))


class TestValidateNoPathInFilename(unittest.TestCase):

    def test_no_path_in_filename(self):
        self.assertEqual([],
                         validate_no_path_in_filename(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read='PAIR1_2.fastq.gz',
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1')])))

    def test_no_path_in_filename_single_read(self):
        self.assertEqual([],
                         validate_no_path_in_filename(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read=None,
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1')])))

    def test_path_in_filename_is_invalid(self):
        self.assertEqual(["Path present in filename: /some/path/PAIR1_1.fastq.gz",
                          "Path present in filename: /some/path/PAIR1_2.fastq.gz", ],
                         validate_no_path_in_filename(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None,
                                                               forward_read='/some/path/PAIR1_1.fastq.gz',
                                                               reverse_read='/some/path/PAIR1_2.fastq.gz',
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1')])))


class TestValidateUniquenessOfReads(unittest.TestCase):
    def test_uniqueness_of_files_sample_and_library(self):
        self.assertEqual([],
                         validate_uniqueness_of_reads(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read='PAIR1_2.fastq.gz',
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1'),
                                                       RawRead(sample_accession=None, forward_read='PAIR2_1.fastq.gz',
                                                               reverse_read='PAIR2_2.fastq.gz',
                                                               sample_name='SAMPLE2', taxon_id="1280",
                                                               library_name='LIB2')])))

    def test_library_name_not_unique(self):
        self.assertEqual(["Library name is not unique: LIB1"],
                         validate_uniqueness_of_reads(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read='PAIR1_2.fastq.gz',
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1'),
                                                       RawRead(sample_accession=None, forward_read='PAIR2_1.fastq.gz',
                                                               reverse_read='PAIR2_2.fastq.gz',
                                                               sample_name='SAMPLE2', taxon_id="1280",
                                                               library_name='LIB1')])))

    def test_sample_name_not_unique(self):
        self.assertEqual(["Sample name is not unique: SAMPLE1"],
                         validate_uniqueness_of_reads(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read='PAIR1_2.fastq.gz',
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1'),
                                                       RawRead(sample_accession=None, forward_read='PAIR2_1.fastq.gz',
                                                               reverse_read='PAIR2_2.fastq.gz',
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB2')])))

    def test_reverse_read_not_unique(self):
        self.assertEqual(["Reverse read is not unique: PAIR1_2.fastq.gz"],
                         validate_uniqueness_of_reads(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read='PAIR1_2.fastq.gz',
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1'),
                                                       RawRead(sample_accession=None, forward_read='PAIR2_1.fastq.gz',
                                                               reverse_read='PAIR1_2.fastq.gz',
                                                               sample_name='SAMPLE2', taxon_id="1280",
                                                               library_name='LIB2')])))

    def test_forward_read_not_unique(self):
        self.assertEqual(["Forward read is not unique: PAIR1_1.fastq.gz"],
                         validate_uniqueness_of_reads(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read='PAIR1_2.fastq.gz',
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1'),
                                                       RawRead(sample_accession=None, forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read='PAIR2_2.fastq.gz',
                                                               sample_name='SAMPLE2', taxon_id="1280",
                                                               library_name='LIB2')])))

    def test_uniqueness_of_files_sample_and_library_single_read(self):
        self.assertEqual([],
                         validate_uniqueness_of_reads(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read=None,
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1'),
                                                       RawRead(sample_accession=None, forward_read='PAIR2_1.fastq.gz',
                                                               reverse_read=None,
                                                               sample_name='SAMPLE2', taxon_id="1280",
                                                               library_name='LIB2')])))


class TestValidatePairReadsFileNamingConvention(unittest.TestCase):
    def test_pair_naming_convention_is_valid(self):
        self.assertEqual([],
                         validate_pair_naming_convention(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read='PAIR1_2.fastq.gz',
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1')])))

    def test_invalid_pair_naming_convention(self):
        self.assertEqual(["Inconsistent naming convention of forward and reverse reads for RawRead("
                          "forward_read='PAIR1xxx_1.fastq.gz', reverse_read='PAIR1_2.fastq.gz', "
                          "sample_name='SAMPLE1', sample_accession=None, taxon_id='1280', library_name='LIB1')"],
                         validate_pair_naming_convention(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None,
                                                               forward_read='PAIR1xxx_1.fastq.gz',
                                                               reverse_read='PAIR1_2.fastq.gz',
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1')])))

    def test_pair_naming_convention_is_valid_for_single_read(self):
        self.assertEqual([],
                         validate_pair_naming_convention(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read=None,
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1')])))


class TestReadsAreCompressed(unittest.TestCase):

    def test_reads_are_not_compressed(self):
        self.assertEqual(["Forward read is not compressed with gz for RawRead(forward_read='PAIR1_1.fastq', "
                          "reverse_read='PAIR1_2.fastq', sample_name='SAMPLE1', sample_accession=None, "
                          "taxon_id='1280', library_name='LIB1')",
                          "Reverse read is not compressed with gz for RawRead(forward_read='PAIR1_1.fastq', "
                          "reverse_read='PAIR1_2.fastq', sample_name='SAMPLE1', sample_accession=None, "
                          "taxon_id='1280', library_name='LIB1')"],
                         validate_files_are_compressed(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_1.fastq',
                                                               reverse_read='PAIR1_2.fastq',
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1')])))

    def test_reads_are_compressed(self):
        self.assertEqual([],
                         validate_files_are_compressed(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read='PAIR1_2.fastq.gz',
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1')])))

    def test_single_read_is_compressed(self):
        self.assertEqual([],
                         validate_files_are_compressed(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read=None,
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1')])))


class TestMandatoryFieldsForReads(unittest.TestCase):
    def test_mandatory_fields_for_reads_are_populated(self):
        self.assertEqual([],
                         validate_mandatory_read_fields(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read='PAIR1_2.fastq.gz',
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1')])))

    def test_mandatory_fields_for_reads_are_populated_single_read(self):
        self.assertEqual([],
                         validate_mandatory_read_fields(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='READ.fastq.gz',
                                                               reverse_read=None,
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1')])))

    def test_forward_read_not_populated(self):
        self.assertEqual(["Missing forward_read for RawRead(forward_read=None, reverse_read=None, "
                          "sample_name='SAMPLE1', sample_accession=None, taxon_id='1280', library_name='LIB1')"],
                         validate_mandatory_read_fields(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read=None,
                                                               reverse_read=None,
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1')])))

    def test_sample_name_not_populated(self):
        self.assertEqual(["Missing sample name for RawRead(forward_read='READ.fastq.gz', reverse_read=None, "
                          "sample_name=None, sample_accession=None, taxon_id='1280', library_name='LIB1')"],
                         validate_mandatory_read_fields(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='READ.fastq.gz',
                                                               reverse_read=None,
                                                               sample_name=None, taxon_id="1280",
                                                               library_name='LIB1')])))

    def test_taxon_id_not_populated(self):
        self.assertEqual(["Missing taxon id for RawRead(forward_read='READ.fastq.gz', reverse_read=None, "
                          "sample_name='SAMPLE1', sample_accession=None, taxon_id=None, library_name='LIB1')"],
                         validate_mandatory_read_fields(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='READ.fastq.gz',
                                                               reverse_read=None,
                                                               sample_name='SAMPLE1', taxon_id=None,
                                                               library_name='LIB1')])))

    def test_library_name_not_populated(self):
        self.assertEqual(["Missing library name for RawRead(forward_read='READ.fastq.gz', reverse_read=None, "
                          "sample_name='SAMPLE1', sample_accession=None, taxon_id='1280', library_name=None)"],
                         validate_mandatory_read_fields(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='READ.fastq.gz',
                                                               reverse_read=None,
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name=None)])))
