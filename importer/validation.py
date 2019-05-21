import re
from collections import defaultdict
from typing import List

from importer.model import Spreadsheet, RawRead


def validate_spreadsheet(spreadsheet: Spreadsheet):
    results = []
    for v in [validate_study_name_length,
              validate_study_name,
              validate_external_data_part_of_internal_sequencing_study_name,
              validate_mandatory_read_fields,
              validate_files_are_compressed,
              validate_pair_naming_convention,
              validate_uniqueness_of_reads,
              validate_no_path_in_filename,
              ]:
        results += v(spreadsheet)
    return results


def validate_study_name(spreadsheet: Spreadsheet) -> List[str]:
    invalid_chars = re.findall("[^\\w_\\d]", spreadsheet.name)
    return ["Invalid chars %s found in study name" % x for x in invalid_chars]


def validate_external_data_part_of_internal_sequencing_study_name(spreadsheet: Spreadsheet) -> List[str]:
    if not spreadsheet.part_of_internal_sequencing_study:
        return []
    name = re.findall("^\\d+_external$", spreadsheet.name)
    if spreadsheet.name in name:
        return []
    return ["Invalid name for data part of internal sequencing study %s" % spreadsheet.name]


def validate_study_name_length(spreadsheet: Spreadsheet) -> List[str]:
    if spreadsheet.name.endswith('_external'):
        validate = spreadsheet.name.replace('_external', '')
        return [] if len(validate) <= 15 else ["Spreadsheet name excluding '_external' suffix is longer than 15 chars"]
    return [] if len(spreadsheet.name) <= 15 else ["Spreadsheet name is longer than 15 chars"]


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
    if not read.forward_read.endswith(".gz"):
        result.append("Forward read is not compressed with gz for %s" % str(read))
    if read.reverse_read is not None and not read.reverse_read.endswith(".gz"):
        result.append("Reverse read is not compressed with gz for %s" % str(read))
    return result


def validate_pair_naming_convention(spreadsheet: Spreadsheet) -> List[str]:
    read_errors = [__validate_pair_naming_convention_for_read(read) for read in spreadsheet.reads]
    return [item for sublist in read_errors for item in sublist]


def __validate_pair_naming_convention_for_read(read: RawRead) -> List[str]:
    result = []
    if read.reverse_read is not None and read.reverse_read.replace("_2.", "_1.") != read.forward_read:
        result.append("Inconsistent naming convention of forward and reverse reads for %s" % str(read))
    return result


def validate_uniqueness_of_reads(spreadsheet: Spreadsheet) -> List[str]:
    forward_read = defaultdict(int)
    reverse_read = defaultdict(int)
    sample_name = defaultdict(int)
    library_name = defaultdict(int)
    for read in spreadsheet.reads:
        forward_read[read.forward_read] += 1
        if read.reverse_read is not None:
            reverse_read[read.reverse_read] += 1
        sample_name[read.sample_name] += 1
        library_name[read.library_name] += 1

    invalid_forwad_read = ["Forward read is not unique: %s" % k for k, v in forward_read.items() if v > 1]
    invalid_reverse_read = ["Reverse read is not unique: %s" % k for k, v in reverse_read.items() if v > 1]
    invalid_sample_name = ["Sample name is not unique: %s" % k for k, v in sample_name.items() if v > 1]
    invalid_library_name = ["Library name is not unique: %s" % k for k, v in library_name.items() if v > 1]

    return invalid_forwad_read + invalid_reverse_read + invalid_sample_name + invalid_library_name;


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
