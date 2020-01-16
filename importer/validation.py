import re
from collections import defaultdict
from typing import List

from importer.model import Spreadsheet, RawRead


def validate_spreadsheet(spreadsheet: Spreadsheet, part_of_internal_study: bool, download_reads_from_ena: bool):
    results = []
    validators = [validate_study_name,
                  validate_mandatory_read_fields,
                  validate_uniqueness_of_reads,
                  validate_no_path_in_filename
                  ]
    if download_reads_from_ena:
        validators.append(check_second_column_is_empty)
    if not download_reads_from_ena:
        validators.append(validate_files_are_compressed, validate_pair_naming_convention)
    if part_of_internal_study:
        validators.append(validate_external_data_part_of_internal_sequencing_study_name)
    for validator in validators:
        results += validator(spreadsheet)
    return results


def validate_study_name(spreadsheet: Spreadsheet) -> List[str]:
    invalid_chars = re.findall("[^\\w_\\d]", spreadsheet.name)
    return ["Invalid chars %s found in study name" % x for x in invalid_chars]


def validate_external_data_part_of_internal_sequencing_study_name(spreadsheet: Spreadsheet) -> List[str]:
    name = re.findall("^\\d+_external$", spreadsheet.name)
    if spreadsheet.name in name:
        return []
    return ["Data part of internal sequencing study should have the suffix '_external' in the name: %s"
            % spreadsheet.name]


def validate_mandatory_read_fields(spreadsheet):
    read_errors = [__validate_mandatory_read_fields_for_read(read) for read in spreadsheet.reads]
    return [item for sublist in read_errors for item in sublist]


def __validate_mandatory_read_fields_for_read(read: RawRead) -> List[str]:
    result = []
    if read.forward_read is None:
        result.append("Missing forward_read for %s" % str(read))
    if read.sample_name is None:
        result.append("Missing sample name for %s" % str(read))
    if read.taxon_id is None:
        result.append("Missing taxon id for %s" % str(read))
    if read.library_name is None:
        result.append("Missing library name for %s" % str(read))
    return result


def validate_files_are_compressed(spreadsheet: Spreadsheet) -> List[str]:
    read_errors = [__validate_files_are_compressed_for_read(read) for read in spreadsheet.reads]
    return [item for sublist in read_errors for item in sublist]


def __validate_files_are_compressed_for_read(read: RawRead) -> List[str]:
    result = []
    if not read.forward_read.endswith("_1.fastq.gz"):
        result.append("Forward read file is not correctly formatted for %s" % str(read))
    if read.reverse_read is not None and not read.reverse_read.endswith("_2.fastq.gz"):
        result.append("Reverse read file is not correctly formatted for %s" % str(read))
    return result


def validate_pair_naming_convention(spreadsheet: Spreadsheet) -> List[str]:
    read_errors = [__validate_pair_naming_convention_for_read(read) for read in spreadsheet.reads]
    return [item for sublist in read_errors for item in sublist]


def __validate_pair_naming_convention_for_read(read: RawRead) -> List[str]:
    result = []
    if read.reverse_read is not None and read.reverse_read.replace("_2.", "_1.") != read.forward_read:
        result.append("Inconsistent naming convention of forward and reverse reads for %s" % str(read))
    return result

def check_second_column_is_empty(spreadsheet: Spreadsheet) -> List[str]:
    for reverse_read in spreadsheet.reads.reverse_read:
        if reverse_read is not None:
            print(re.search('[a-zA-Z]', reverse_read))


def validate_uniqueness_of_reads(spreadsheet: Spreadsheet) -> List[str]:
    forward_read = defaultdict(int)
    reverse_read = defaultdict(int)
    sample_name = defaultdict(int)
    library_name = defaultdict(int)
    for read in spreadsheet.reads:
        forward_read[read.forward_read] += 1
        if read.reverse_read is not None or read.reverse_read is not ( ):
            reverse_read[read.reverse_read] += 1
        sample_name[read.sample_name] += 1
        library_name[read.library_name] += 1

    invalid_forward_read = ["Forward read is not unique: %s" % k for k, v in forward_read.items() if v > 1]
    invalid_reverse_read = ["Reverse read is not unique: %s" % k for k, v in reverse_read.items() if v > 1]
    invalid_sample_name = ["Sample name is not unique: %s" % k for k, v in sample_name.items() if v > 1]
    invalid_library_name = ["Library name is not unique: %s" % k for k, v in library_name.items() if v > 1]

    return invalid_forward_read + invalid_reverse_read + invalid_sample_name + invalid_library_name;


def validate_no_path_in_filename(spreadsheet: Spreadsheet) -> List[str]:
    read_errors = [__validate_no_path_in_filename_for_read(read) for read in spreadsheet.reads]
    return [item for sublist in read_errors for item in sublist]


def __validate_no_path_in_filename_for_read(read: RawRead) -> List[str]:
    result = []
    if "/" in read.forward_read:
        result.append("Path present in filename: %s" % str(read.forward_read))
    if read.reverse_read is not None and "/" in read.reverse_read:
        result.append("Path present in filename: %s" % str(read.reverse_read))
    return result
