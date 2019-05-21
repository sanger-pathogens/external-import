import re


def print_pf_checks(spreadsheet, outputdir):
    print("Congratulations, the validation was successful, you now need to perform the below manual checks...:")
    __study_name_should_not_exists(spreadsheet)
    __sample_names_should_be_unique_across_the_database(spreadsheet, outputdir)
    __lane_names_should_be_unique_across_the_database(spreadsheet, outputdir)


def __study_name_should_not_exists(spreadsheet):
    cmd = "pf data -t study -i %s" % spreadsheet.name
    print("""
Check that the study name doesn't already exist, the following command should return no data:
%s
If it does, rename the study to %s
""" % (cmd, spreadsheet.name + "_external"))


def __sample_names_should_be_unique_across_the_database(spreadsheet, outputdir):
    samples = set()
    for read in spreadsheet.reads:
        samples.add(read.sample_name)
        samples.add(read.library_name)
    filename = '%s/samples.txt' % outputdir
    with open(filename, 'w') as file:
        file.writelines(["%s\n" % item for item in samples])
    print("""Check that the sample and library names are unique in the database.
The following commands should return no data:
pf data -t file --file-id-type sample -i %s
""" % filename)


def __lane_names_should_be_unique_across_the_database(spreadsheet, outputdir):
    names = []
    for read in spreadsheet.reads:
        if read.reverse_read is None:
            names += re.findall("^([^.]+)\\..*$", read.forward_read)
        else:
            names += re.findall("^(.+)_1\\..*$", read.forward_read)

    filename = '%s/lanes.txt' % outputdir
    with open(filename, 'w') as file:
        file.writelines(["%s\n" % item for item in names])

    message = "Check that the lanes are unique in the database, the following commands should return no data:\n"
    for name in names:
        message += "pf data -N -t lane -i %s\n" % name
    print("""Check that the lanes are unique in the database.
The following commands should return no data:
pf data -t file --file-id-type lane -i %s
""" % filename)
