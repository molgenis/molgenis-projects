# MOLGENIS Projects table of contents

1. [Molgenis default](#molgenis-default)
  [How to](#how-to)
  a. [Websites](#websites)
  b. [Publications](#publications)
2. [1000IBD](#1000ibd)
  a. [Websites](#websites-1)
  b. [Publications](#publications-1)
3. [BBRMI-ERIC](#bbrmi-eric)
  a. [Websites](#websites-2)
  b. [Publications](#publications-2)
4. [VKGL](#vkgl)
  [How to](#how-to)
  a. [Websites](#websites-2)
5. [Chromosome6 project](#chromosome6-project)
  a. [Websites](#websites)
  b. [Publications](#publications)
6. [Theming workflow](#theming-workflow)

## Molgenis default

> MOLGENIS: Flexible software for scientific data

### Online resources
#### Websites
http://molgenis.github.io/

#### Publications
*The MOLGENIS toolkit: rapid prototyping of biosoftware at the push of a button.* - Swertz et al.
https://www.ncbi.nlm.nih.gov/pubmed/21210979
*Beyond standardization: dynamic software infrastructures for systems biology.* - Swertz & Jansen
https://www.ncbi.nlm.nih.gov/pubmed/17297480

## 1000IBD
> The 1000IDB project describes patients and samples with inflammatory bowel disease.

### Online resources
#### Websites
A public MOLGENIS data server can be found [here](https://1000ibd.com).
It contains an overview of data and research results.

#### Publications
TODO: add papers + url's

## BBRMI-ERIC
> BBMRI-ERIC aims to establish, operate and develop a pan-European distributed research infrastructure of biobanks and biomolecular resources in order to facilitate the access to resources as well as facilities and to support high quality biomolecular and medical research.

### Online resources
#### Websites
A public MOLGENIS data server can be found [here](https://directory.bbmri-eric.eu).
It contains the BBMRI-ERIC Directory containing biobanks and sample collection metadata form organizations all over Europe.

You can read more about the BBMRI-ERIC groups and projects at http://www.bbmri-eric.eu/

#### Publications
*Biopreservation and Biobanking* - Holub Petr, Swertz Morris, Reihs Robert, van Enckevort David, Müller Heimo, and Litton Jan-Eric
http://online.liebertpub.com/doi/10.1089/bio.2016.0088

### How to

#### Data mover
This script downloads data from one server of BBMRI eric and uploads it to a specified target server. The datamodel is altered.
This new model is specified in the data_model folder. This new model will be uploaded.
The old data retrieved from the specified server will be converted to the new model.
Invalid rows will be filtered out and written to logfiles. The valid data will be uploaded in the models

##### Run
Add a config.txt file in the format of config_example.txt, in the same directory.
Config.txt:

```
url=http(s)://source-server/api/
account=username
password=password
countries=AT,BE,CZ,DE,EE,FI,FR,GR,IT,MT,NL,NO,PL,SE,UK,LV
target_server=http(s)://target-server/api/
target_account=username
target_password=password
```
To upload without countries, set the "countries" parameter to "FALSE" in the config file.

Run the script:
```
python3 Bbmri_data_mover.py
```

##### Model
Model for countries will be created in /datamodel/countries.
Model for general directory is already in /datamodel and will be zipped as: meta_data.zip

##### Data
Data will be retrieved from one server, converted to new model and put in the new server. Invalid rows are filtered out.

##### Logs of invalid data
Logs will be created in /Bbrmi_eric_quality_checker. Two logs will be written:

| Logfile           | Description                                                                                 |
|-------------------|---------------------------------------------------------------------------------------------|
| logs.txt          | Contains all rows with invalid data                                                         |
| breaking_rows.txt | Contains data invalid rows that are not uploaded in the new model on the target server      |

## VKGL
> Association of Clinical Lab Diagnostics (Vereniging Klinische Lab Diagnostiek)

### How to
#### Consensus
This script generates the consensus table for the VKGL project
To run: incude a config.txt in the directory of this project. The file should look like: config_example.txt.
Make sure you have loaded tables with the metadata of the VKGL project on your molgenis server.
Now run VKGL_consensus_table_generator.py

#### Clinvar export
Work in progress

### Online resources
#### Websites
http://www.vkgl.nl/nl/
http://molgenis.org/vkgl

## Chromosome6 project
> The chromosome 6 project aims to compare alterations in chromosome 6 (the genotype) with the effect they have on the appearance features and other clinical features of individuals with chromosome 6 abberations.

### Online resources
#### Websites
https://chromosome6.org

#### Publications
*The phenotypic spectrum of proximal 6q deletions based on a large cohort derived from social media and literature reports* - Engwerda et al.
https://www.nature.com/articles/s41431-018-0172-9

## Theming workflow

Molgenis themes are managed from [Molgenis-theme](https://github.com/molgenis/molgenis-theme).
Checkout its docs or ask one of the frontend devs, on how to create a new project theme.
Fixes to the base theme are propagated to all [checked-in](https://github.com/molgenis/molgenis-theme/tree/master/theme) themes. New versions are automatically published to [npm](http://npmjs.com/@molgenis/molgenis-theme) and served from [unpkg](https://unpkg.com/browse/@molgenis/molgenis-theme@latest/css/).

> Some projects may still have their Bootstrap CSS checked in to this repository.
In such case; please create a new theme in the molgenis-theme project, based on
the old theme variables and remove the old CSS from this project.
