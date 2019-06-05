# external import
A python3 library to parse external import spreadsheets
<!--
[![Build Status](https://travis-ci.org/sanger-pathogens/external-import.svg?branch=master)](https://travis-ci.org/sanger-pathogens/external-import)   
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-brightgreen.svg)](https://github.com/sanger-pathogens/external-import/blob/master/LICENSE)   
[![status](https://img.shields.io/badge/MGEN-10.1099%2Fmgen.0.000056-brightgreen.svg)](http://mgen.microbiologyresearch.org/content/journal/mgen/10.1099/mgen.0.000186)   
[![status](https://img.shields.io/badge/Bioinformatics-10.1093-brightgreen.svg)](https://doi.org/10.1093/bioinformatics/btw022)  
[![status](https://img.shields.io/badge/GenomeBiology-10.1186-brightgreen.svg)](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-015-0849-0)   
[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg)](http://bioconda.github.io/recipes/seroba/README.html)  
[![Container ready](https://img.shields.io/badge/container-ready-brightgreen.svg)](https://quay.io/repository/biocontainers/seroba)  
[![Docker Build Status](https://img.shields.io/docker/build/sangerpathogens/seroba.svg)](https://hub.docker.com/r/sangerpathogens/seroba)  
[![Docker Pulls](https://img.shields.io/docker/pulls/sangerpathogens/seroba.svg)](https://hub.docker.com/r/sangerpathogens/seroba)  
[![codecov](https://codecov.io/gh/sanger-pathogens/external-import/branch/master/graph/badge.svg)](https://codecov.io/gh/sanger-pathogens/external-import) 
-->
# WIP
<!--
## Contents (edit as fit)
  * [Introduction](#introduction)
  * [Installation](#installation)
    * [Required dependencies](#required-dependencies)
    * [Optional dependencies](#optional-dependencies)
    * [Linux specific instructions (Debian, Ubuntu, RedHat etc\.)](#linux-specific-instructions-debian-ubuntu-redhat-etc)
    * [Mac OS](#mac-os)
    * [Bioconda](#bioconda)
    * [Homebrew/Linuxbrew](#homebrewlinuxbrew)
    * [Docker](#docker)
    * [Virtual Machine](#virtual-machine)
    * [Galaxy](#galaxy)
    * [From Source](#from-source)
    * [Running the tests](#running-the-tests)
  * [Usage](#usage)
  * [License](#license)
  * [Feedback/Issues](#feedbackissues)
  * [Citation](#citation)
  * [Further Information](#further-information)

## Introduction
Provide a more in-depth overview and description of the software. A single paragraph should be sufficient.
-->
## Installation
```
virtualenv --system-site-packages external_import
source external_import/bin/activate
git clone https://github.com/sanger-pathogens/external-import
cd external-import
pip install .
```


## Uninstallation
```
source external_import/bin/activate
pip uninstall external-import
```

### Running the tests
Instructions on how to run the tests and check that the software has installed correctly.

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
usage: external-import validate [-h] -s SPREADSHEET [-i] -o OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  -s SPREADSHEET, --spreadsheet SPREADSHEET
                        Spreadsheet to validate
  -i, --internal        External data part of an internally sequenced study
  -o OUTPUT, --output OUTPUT
                        Output director for generated lane and sample files
                        for pf
```

### Preparation
```
external-import.py prepare --help
usage: external-import prepare [-h] -s SPREADSHEET -t TICKET -i INPUT -o
                               OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  -s SPREADSHEET, --spreadsheet SPREADSHEET
                        Spreadsheet to validate
  -t TICKET, --ticket TICKET
                        RT Ticket number
  -i INPUT, --input INPUT
                        Directory containing the read files
  -o OUTPUT, --output OUTPUT
                        Base directory for import data
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
usage: external-import load [-h] -d DATABASE -t TICKET -o OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  -d DATABASE, --database DATABASE
                        The tracking database to import into
  -t TICKET, --ticket TICKET
                        RT Ticket number
  -o OUTPUT, --output OUTPUT
                        Base directory for import data
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
