# external import
A python3 library to parse external import spreadsheets

[![Build Status](https://travis-ci.org/sanger-pathogens/external-import.svg?branch=master)](https://travis-ci.org/sanger-pathogens/external-import)   
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-brightgreen.svg)](https://github.com/sanger-pathogens/external-import/blob/master/LICENSE)   
[![codecov](https://codecov.io/gh/sanger-pathogens/external-import/branch/master/graph/badge.svg)](https://codecov.io/gh/sanger-pathogens/external-import)   
[![Docker Build Status](https://img.shields.io/docker/cloud/build/sangerpathogens/external-import.svg)](https://hub.docker.com/r/sangerpathogens/external-import)  
[![Docker Pulls](https://img.shields.io/docker/pulls/sangerpathogens/external-import.svg)](https://hub.docker.com/r/sangerpathogens/external-import)  

# WIP
## Contents
  * [Introduction](#introduction)
  * [Installation](#installation)
    * [Required dependencies](#required-dependencies)
    * [From Source](#installing from source)
    * [Docker](#installing with docker)
  * [Uninstallation](#from-source)
  * [Usage](#usage)
  * [License](#license)
  * [Feedback/Issues](#feedbackissues)


##Introduction
This software can be used to prepare data to be imported into the pathogen's pipelines. There are three steps to this process. 
Validation is used to check over the manifest supplied by the user and check that the lanes have not already been imported. 
The prepare step converts the spreadsheet supplied into the correct format. It can also split this spreadsheet if there are 
too many lanes to be imported in one go. This step can also be run in two modes, to either copy the files to a set location 
from a users directory, or to download the files from the ENA. The last step is to load the commands needed to import the data 
into a bash script.  

## Installation
There are a number of ways to install external-import and details are provided below. If you encounter an issue when installing <software name> please contact your local system administrator.
### Required Dependencies 
    * Python 3.6.9
    * enaBrowserTools 1.5.4

### From Source
```
python3 -m venv external_import
source external_import/bin/activate
git clone https://github.com/sanger-pathogens/external-import
```
Run the tests 
```
python3 setup.py test
```
If all of the tests pass, then install 
```
cd external-import
pip install .
```

### Docker
The external import can be run in a Docker container. First install Docker 
and then install external-import:

    docker pull sangerpathogens/external-import

To use external-import use a command like this, replacing /local/data with where your files are stored:

    docker run --rm -it -v /local/data:/data sangerpathogens/external-import external-import.py --help

When calling external-import (as above) you will need to add /data before any file you pass in.

## Uninstallation
```
source external_import/bin/activate
pip uninstall external-import
```

## Usage
```
external-import.py --help
usage: external-import [-h] {validate,prepare,load} ...

positional arguments:
  {validate,prepare,load}
                        sub-command help
    validate            Validates the spreadsheet to import
    prepare             Prepare the import
    load                Print the command to import the external data

optional arguments:
  -h, --help            show this help message and exit
```

### Validation
```
external-import.py validate --help
usage: external-import validate [-h] -s SPREADSHEET [-i] -o OUTPUT (-cp | -dl)

optional arguments:
  -h, --help            show this help message and exit
  -s SPREADSHEET, --spreadsheet SPREADSHEET
                        Spreadsheet to validate
  -i, --internal        External data part of an internally sequenced study
  -o OUTPUT, --output OUTPUT
                        Output director for generated lane and sample files
                        for pf
  -cp, --copy           Spreadsheet is prepared to copy reads from existing
                        files.
  -dl, --download       Spreadsheet is prepared to download reads from ENA
```

### Preparation
```
external-import.py prepare --help
usage: external-import prepare [-h] -s SPREADSHEET -t TICKET (-i INPUT | -dl)
                               [-c range[1,1000]] -o OUTPUT [-b BREAKPOINT]

optional arguments:
  -h, --help            show this help message and exit
  -s SPREADSHEET, --spreadsheet SPREADSHEET
                        Spreadsheet to validate
  -t TICKET, --ticket TICKET
                        RT Ticket number
  -i INPUT, --input INPUT
                        Directory containing the read files to be copied.
  -dl, --download       Use this flag to download the fastq files from ENA
  -c range[1,1000], --connections range[1,1000]
                        Number of connections to ENA to be made at a time if
                        files are to be downloaded. Default is 10.
  -o OUTPUT, --output OUTPUT
                        Base directory for import datas
  -b BREAKPOINT, --breakpoint BREAKPOINT
                        Breakpoint to split spreadsheet, default is no
                        breaking

```
Base directory for import data is ```/lustre/scratch118/infgen/pathogen/pathpipe/external_seq_data```

Should be run using bsub to avoid timeout:
```
bsub -o prepare.o -e prepare.e -M2000 -R "select[mem>2000] rusage[mem=2000]" external-import.py prepare \
   -o /lustre/scratch118/infgen/pathogen/pathpipe/external_seq_data \
   -s spreadsheet.xls \
   -i inputdir \
   -t 123456 
```

### Loading
The script doesn't load the data, but rather prints the instructions to load the data.
```
external-import.py load --help
usage: external-import load [-h] -d DATABASE -t TICKET -o OUTPUT -c COMMANDS

optional arguments:
  -h, --help            show this help message and exit
  -d DATABASE, --database DATABASE
                        The tracking database to import into
  -t TICKET, --ticket TICKET
                        RT Ticket number
  -o OUTPUT, --output OUTPUT
                        Base directory for import data
  -c COMMANDS, --commands COMMANDS
                        Directory for command file
```
<!--
## License
<software name> is free software, licensed under [<license>](link_to_license_file_on_github).

## Feedback/Issues
Please report any issues to the [issues page](link_to_github_issues_page) or email path-help@sanger.ac.uk <or appropriate tool email list e.g. iva@sanger.ac.uk>.

## Citation
If you use this software please cite:
<Insert citation (journal publication, bioarxiv, JOSS or github repo)>

Also include any additional references that should be cited.

## Further Information (optional)
For more information on this software see:
* [Software Web page](link_to_web_page)
* [Jupyter notebook tutorial](https://github.com/sanger-pathogens/pathogen-informatics-training)
-->
