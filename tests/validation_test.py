import unittest
from unittest.mock import patch

from importer.pfchecks import output_directory_for_lanes_and_samples_exists, print_pf_checks
from importer.model import Spreadsheet, RawRead
from importer.validation import validate_study_name, validate_mandatory_read_fields, \
    validate_files_are_compressed, validate_pair_naming_convention, validate_uniqueness_of_reads, \
    validate_no_path_in_filename, validate_external_data_part_of_internal_sequencing_study_name, check_double_ended_column_is_T_or_F, \
    validate_no_abnormal_characters_in_supplier_name, validate_no_hyphen_in_filename, validate_no_hyphen_in_descriptive_names


class TestStudyNameContent(unittest.TestCase):

    def test_study_name_with_valid_char_should_pass_validation(self):
        self.assertEqual([], validate_study_name(Spreadsheet.new_instance("ValidName12345__")))

    def test_study_name_with_invalid_char_should_fail_validation(self):
        self.assertEqual(34,
                         len(validate_study_name(Spreadsheet.new_instance("!\"£$%^&*()+={}[]:@~;'#?/>.<,|\\`¬ \t"))))

class TestSupplierNameContent(unittest.TestCase):

    def test_supplier_name_with_valid_char_should_pass_validation(self):
        self.assertEqual([], validate_no_abnormal_characters_in_supplier_name(Spreadsheet.new_instance("name",supplier="This should work")))

    def test_supplier_name_with_invalid_char_should_fail_validation(self):
        self.assertEqual(33, len(validate_no_abnormal_characters_in_supplier_name(Spreadsheet.new_instance("name",supplier="!\"£$%^&*()+={}[]:@~;'#?/>.<,|\\`¬\t"))))

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

    def test_hyphen_in_sample_name_is_invalid(self):
        self.assertEqual(["Hyphen present in sample name: SAMPLE1-1", ],
                         validate_no_hyphen_in_descriptive_names(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None,
                                                               forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read='PAIR1_2.fastq.gz',
                                                               sample_name='SAMPLE1-1', taxon_id="1280",
                                                               library_name='LIB1')])))

    def test_hyphen_in_library_name_is_invalid(self):
        self.assertEqual(["Hyphen present in library name: LIB-1", ],
                         validate_no_hyphen_in_descriptive_names(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None,
                                                               forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read='PAIR1_2.fastq.gz',
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB-1')])))

class TestValidateNoHyphenInFilename(unittest.TestCase):

    def test_no_hyphen_in_filename(self):
        self.assertEqual([],
                         validate_no_hyphen_in_filename(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read='PAIR1_2.fastq.gz',
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1')])))

    def test_no_hyphen_in_filename_single_read(self):
        self.assertEqual([],
                         validate_no_hyphen_in_filename(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read=None,
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1')])))

    def test_hyphen_in_filename_is_invalid(self):
        self.assertEqual(['Hyphen present in filename: PAIR-1_1.fastq.gz',
                          'Hyphen present in filename: PAIR-1_2.fastq.gz'],
                         validate_no_hyphen_in_filename(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None,
                                                               forward_read='PAIR-1_1.fastq.gz',
                                                               reverse_read='PAIR-1_2.fastq.gz',
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

    def test_uniqueness_of_files_sample_and_library_ENA_download(self):
        self.assertEqual([],
                         validate_uniqueness_of_reads(
                            Spreadsheet.new_instance("1234567890123456",
                                                     [RawRead(sample_accession=None, forward_read='PAIR1',
                                                              reverse_read='T',
                                                              sample_name='SAMPLE1', taxon_id="1280",
                                                              library_name='LIB1'),
                                                      RawRead(sample_accession=None, forward_read='PAIR2',
                                                              reverse_read='F',
                                                              sample_name='SAMPLE2', taxon_id="1280",
                                                              library_name='LIB2')])
        ))


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


class TestCheckDoubleEndedColumnIsTOrF(unittest.TestCase):
    def test_T_or_F_is_valid(self):
        self.assertEqual([],
                         check_double_ended_column_is_T_or_F(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read='T',
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1'),
                                                       RawRead(sample_accession=None, forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read='F',
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1')
                                                       ])))

    def test_none_is_not_valid(self):
        self.assertEqual(["Double-ended is incorrectly formatted, must be T or F"],
                         check_double_ended_column_is_T_or_F(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_1.fastq.gz',
                                                               reverse_read=None,
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1')])))

class TestReadsAreCompressed(unittest.TestCase):

    def test_reads_are_not_compressed(self):
        self.assertEqual(["Forward read file is not correctly formatted for RawRead(forward_read='PAIR1_1.fastq', "
                          "reverse_read='PAIR1_2.fastq', sample_name='SAMPLE1', sample_accession=None, "
                          "taxon_id='1280', library_name='LIB1')",
                          "Reverse read file is not correctly formatted for RawRead(forward_read='PAIR1_1.fastq', "
                          "reverse_read='PAIR1_2.fastq', sample_name='SAMPLE1', sample_accession=None, "
                          "taxon_id='1280', library_name='LIB1')"],
                         validate_files_are_compressed(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_1.fastq',
                                                               reverse_read='PAIR1_2.fastq',
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1')])))

    def test_reads_are_not_fastq(self):
        self.assertEqual(["Forward read file is not correctly formatted for RawRead(forward_read='PAIR1_1.gz', "
                          "reverse_read='PAIR1_2.gz', sample_name='SAMPLE1', sample_accession=None, "
                          "taxon_id='1280', library_name='LIB1')",
                          "Reverse read file is not correctly formatted for RawRead(forward_read='PAIR1_1.gz', "
                          "reverse_read='PAIR1_2.gz', sample_name='SAMPLE1', sample_accession=None, "
                          "taxon_id='1280', library_name='LIB1')"],
                         validate_files_are_compressed(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_1.gz',
                                                               reverse_read='PAIR1_2.gz',
                                                               sample_name='SAMPLE1', taxon_id="1280",
                                                               library_name='LIB1')])))

    def test_reads_are_incorrectly_ended(self):
        self.assertEqual(["Forward read file is not correctly formatted for RawRead(forward_read='PAIR1_INCORRECT.fastq.gz', "
                          "reverse_read='PAIR1.fastq.gz', sample_name='SAMPLE1', sample_accession=None, "
                          "taxon_id='1280', library_name='LIB1')",
                          "Reverse read file is not correctly formatted for RawRead(forward_read='PAIR1_INCORRECT.fastq.gz', "
                          "reverse_read='PAIR1.fastq.gz', sample_name='SAMPLE1', sample_accession=None, "
                          "taxon_id='1280', library_name='LIB1')"],
                         validate_files_are_compressed(
                             Spreadsheet.new_instance("1234567890123456",
                                                      [RawRead(sample_accession=None, forward_read='PAIR1_INCORRECT.fastq.gz',
                                                               reverse_read='PAIR1.fastq.gz',
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

class TestDirectoryCallForPF(unittest.TestCase):
    def test_output_directory_present(self):
        with patch('os.path.isdir', return_value=True) as path_search:
            with patch('os.mkdir') as mocked_dir:
                output_directory_for_lanes_and_samples_exists('dir/')

                path_search.assert_called_once_with('dir/')
                mocked_dir.assert_not_called()


    def test_output_directory_generated(self):
        with patch('os.path.isdir', return_value=False) as path_search:
            with patch('os.mkdir') as mocked_dir:
                output_directory_for_lanes_and_samples_exists('dir/')

                path_search.assert_called_once_with('dir/')
                mocked_dir.assert_called_once_with('dir/')