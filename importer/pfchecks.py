import re


def print_pf_checks(spreadsheet):
    __study_name_should_not_exists(spreadsheet)
    __sample_names_should_be_unique_across_the_database(spreadsheet)
    __lane_names_should_be_unique_across_the_database(spreadsheet)


def __study_name_should_not_exists(spreadsheet):
    cmd = "pf data -N -t study -i %s" % spreadsheet.name
    print("""
Check that the study name doesn't already exist, the following command should return no data:
%s
If it does, rename the study to %s
Make sure it is still less than 15 characters long
""" % (cmd, spreadsheet.name + "_external"))


def __sample_names_should_be_unique_across_the_database(spreadsheet):
    samples = set()
    for read in spreadsheet.reads:
        samples.add(read.sample_name)
        samples.add(read.library_name)
    message = "Check that the sample and library names are unique in the database," \
              " the following commands should return no data:\n"
    for sample in samples:
        message += "pf data -N -t sample -i %s\n" % sample
    print(message)


def __lane_names_should_be_unique_across_the_database(spreadsheet):
    names = []
    for read in spreadsheet.reads:
        if read.reverse_read is None:
            names += re.findall("^([^.]+)\..*$", read.forward_read)
        else:
            names += re.findall("^(.+)_1\..*$", read.forward_read)
    message = "Check that the lanes are unique in the database, the following commands should return no data:\n"
    for name in names:
        message += "pf data -N -t lane -i %s\n" % name
    print(message)
