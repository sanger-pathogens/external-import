import re


def validate_study_name(spreadsheet):
    invalid_chars = re.findall("[^\\w_\\d]", spreadsheet.name)
    return ["Invalid chars %s found in study name" % x for x in invalid_chars]


def validate_study_name_length(spreadsheet):
    return [] if len(spreadsheet.name) <= 15 else ["Spreadsheet name longer than 15 chars"]

#the study title does not have any odd characters and is reasonably short as this will be used with the pf scripts (i.e. don't use a full paper title)
# the study title is not the the same as an internal study (you can check this with pf data -t study -i "STUDY NAME"). If it is, add the word "external" to the end (e.g. 1234_external)
# the columns marked as green are filled in (except _Base Count_ and _Fragment Size_).

#If the Library Name column is not completed then copy over the values from the Sample Name column.

#     the fastq files are named _1 and _2 and are gzipped. If they are not, either tell the user to fix this or rename them yourself.
#    NOTE: The file names (up until _1) will become the lane_ids. Check that they are unique in the database (you can check this with pf data -t lane -i "FILE NAME").
# the sample names and library names are named uniquely within the spreadsheet
# the sample names and library names are unique within the database (you can check this with pf data -t sample -i SAMPLE_NAME)
# the user has not included the complete file path in the spreadsheet. If so, either ask the user to remove the paths and just leave the file names, or do it yourself.
# to add a 'Data to be kept until' date (e.g. 01/01/2022) and a 'Total size of files in GBytes' value (e.g. use du -ch ./*.gz | grep total)
# If the data is to be included as part of an internal sequencing study, it should still be imported into an external database and the study name should be the same as the internal study name with word 'external' at the end of the study name
# Save the spreadsheet as external_XXXX.xls where XXXX is the RT ticket number

