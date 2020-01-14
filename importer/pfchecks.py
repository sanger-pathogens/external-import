import re
import os


def print_pf_checks(spreadsheet, outputdir, download_reads_from_ENA: bool):
    print("Congratulations, the validation was successful, you now need to perform the below manual checks...:")
    __study_name_should_not_exists(spreadsheet)
    output_directory_for_lanes_and_samples_exists(outputdir)
    __sample_names_should_be_unique_across_the_database(spreadsheet, outputdir)
    __lane_names_should_be_unique_across_the_database(spreadsheet, outputdir, download_reads_from_ENA)


def __study_name_should_not_exists(spreadsheet):
    cmd = f"pf data -t study -i {spreadsheet.name}"
    print(f"""
Check for presence of the study; run the following command:
{cmd}

If this command returns data check with the requestor if they want to append
to the existing study - if not, the name needs to be changed
""" )


def output_directory_for_lanes_and_samples_exists(outputdir):
    if not os.path.isdir(outputdir):
        os.mkdir(outputdir)
        print(f"""
        WARNING: Output directory not found. A directory for lanes and samples has been created at '{outputdir}'
""")


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


def __lane_names_should_be_unique_across_the_database(spreadsheet, outputdir, download_reads_from_ENA: bool):
    names = []
    for read in spreadsheet.reads:
        print(read.forward_read)
        #if download_reads_from_ENA:
            #names += re.findall("^*$", read.forward_read)
        elif read.reverse_read is None:
            names += re.findall("^([^.]+)\\..*$", read.forward_read)
        else:
            names += re.findall("^(.+)_1\\..*$", read.forward_read)
    print(names)
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
