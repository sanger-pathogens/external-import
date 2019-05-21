from shutil import copyfile

import xlwt


# Experimental => no test.  Needs rewrite
def save(spreadsheet, spreadsheet_name):
    wb = xlwt.Workbook()  # create empty workbook object
    newsheet = wb.add_sheet('Sheet1')
    not_applicable(newsheet, 0, 'Supplier Name')
    not_applicable(newsheet, 1, 'Supplier Organisation')
    not_applicable(newsheet, 2, 'Sanger Contact Name')
    not_applicable(newsheet, 3, 'Sequencing Technology')
    write_string(newsheet, 4, 'Study Name', spreadsheet.name)
    not_applicable(newsheet, 5, 'Study Accession number')
    not_applicable(newsheet, 6, 'Total size of files in GBytes')
    not_applicable(newsheet, 7, 'Data to be kept until')
    index = 0
    for header in ['Filename', 'Mate File', 'Sample Name', 'Sample Accession number', 'Taxon ID', 'Library Name',
                   'Fragment Size', 'Read Count', 'Base Count', 'Comments']:
        newsheet.write(9, index, header)
        index += 1
    row = 10
    for read in spreadsheet.reads:
        newsheet.write(row, 0, read.forward_read)
        if read.reverse_read is not None:
            newsheet.write(row, 1, read.reverse_read)
        newsheet.write(row, 2, read.sample_name)
        newsheet.write(row, 4, read.taxon_id)
        newsheet.write(row, 5, read.library_name)
        row += 1
    wb.save(spreadsheet_name)


def spreadsheet_name(destination, ticket):
    return '%s/external_%d.xls' % (destination, ticket)


def import_cmd(database, destination, spreadsheet_path):
    print(
        """
        Execute the below to import:
        
        cd /software/pathogen/projects/update_pipeline
        bsub -o ~/external.log -e ~/external.err -M2000 -R "select[mem>2000] rusage[mem=2000]" './bin/update_pipeline_from_spreadsheet.pl \\
          -d %s \\
          -f %s \\
          -p /lustre/scratch118/infgen/pathogen/pathpipe/%s/seq-pipelines \\
          %s'
          
        Then following the external data import SOP to register the study
        """ % (database, destination, database, spreadsheet_path))


def copy_files(spreadsheet, source, destination):
    for read in spreadsheet.reads:
        copyfile("%s/%s" % (source, read.forward_read), "%s/%s" % (destination, read.forward_read))
        if read.reverse_read is not None:
            copyfile("%s/%s" % (source, read.reverse_read), "%s/%s" % (destination, read.reverse_read))


def output_dir(base, rt):
    output = "%s/%d" % (base, rt)
    return output


def not_applicable(sheet, row, title):
    write_string(sheet, row, title, 'Unused field')


def write_string(sheet, row, title, value):
    sheet.write(row, 0, title)
    sheet.write(row, 1, value)
