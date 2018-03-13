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

## Molgenis default
> MOLGENIS: Flexible software for scientific data

### How to
Css minified in molgenis repository using: https://cssminifier.com/

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
Requirements before running:  
- Incude a config.txt in the directory of this project. The file should look like: config_example.txt.  
- Include omim.txt, which is a biomart export with unique rows containing the columns: Gene_stable_ID, MIM_disease_accession, HGNC_symbol  
- Make sure you have loaded tables with the metadata of the VKGL project on your molgenis server.  
  
Run: 
```
python3 VKGL_consensus_table_generator.py
```

#### Clinvar export
This script generates the ClinVar export per lab. Variants exported to ClinVar meet the following rules:
- Variant has consensus classification  
- Only one OMIM code is selected for the variant in the consensus table  

Requirements before running:  
- Incude a config.txt in the directory of this project. The file should look like: config_example.txt.  

```
python3 ConsensusTableParser.py
```

### Online resources
#### Websites
http://www.vkgl.nl/nl/  
http://molgenis.org/vkgl