# Procedure LifeLines NEXT to TGO NEXT data model.

## Background:

LifeLines (LL) NEXT questionnaire data model was moved from LifeLines databases to Unipark. The data model was made by TGO at the UMCG.
LL NEXT variable names were not kept. Questionnaire questions were entered into the system by hand by multiple people.

## 1. Matching LifeLines NEXT and TGO NEXT codebooks:

llnext_mapping.py -ll_in <LL NEXT codebook> -tgo_in <TGO NEXT codebook> -out <output file name>

Script maps LL NEXT questions to TGO NEXT questions. Needs to be run on each questionnaire codebook pair
separately and give one output file per questionnaire pair (see folder 'codebooks_comparison'). All output files were checked for mapping/matching
errors by hand.

## 2. Transfer/transform LL NEXT data to TGO NEXT model:

llnext_recoding.py -c <comparison codebook> -d <LL NEXT data> -out <output file name>

Script transfers data from LL NEXT data model to TGO NEXT data model using the mappings described
in the comparison codebook. Needs to be run separately for each questionnaire.

check transfer:

llnext_check_data.py -c <comparison codebook> -dtgo <LL NEXT data in TGO model> -dll <LL NEXT data>

Script checks whether data is transfered correctly. Weakness is that it uses the same comparison codebook that is used
to transfer the data. More data checks can be done, such as comparing analyses/basic statistics.

check variables:

check_ll_variables.py -c -c <comparison codebook> -dll <LL NEXT data> 

Run script per comparison codebook and data file per questionnaire. 
Output on screen, overview of variables that are in the codebook but are missing in the data files.


## 3. Model metadata (TGO NEXT codebooks) to EMX:

llnext_emx.py -out <output_filename>

Script uses TGO NEXT codebooks and comparison codebooks to make
EMX datamodel for MOLGENIS

## 4. Model LL NEXT data in TGO NEXT model to fit with EMX: 

llnext_data_emx_ll.py -out <output_filename>

Script uses LL NEXT recoded/transformed data and writes them to match the EMX metadata model.
Takes in all data files that are in the folder where the script is run.
Data files are in possession of the data manager of LL NEXT.

## 5. Model TGO NEXT data in TGO NEXT model to fit with EMX: 

llnext_data_emx_tgo.py -out <output_filename>

Script uses TGO extracts of data from Unipark and writes them to match the EMX metadata model.
Takes in all data files that are in the folder where the script is run.
This script also takes care of the changes that were made in M2_Baby, M6_Baby, M9_Baby, P12, P18, P32 and Father_1.
Some final changes to P18 were done by hand, see the documentation in folder 'Documentation'. 
Data files that were moved to EMX are in possesion of the data manager of LL NEXT.

Resulting EMX for MOLGENIS and data files that are uploaded to MOLGENIS, codebooks and 
comparison codebooks can be obtained through the LL NEXT data manager.
