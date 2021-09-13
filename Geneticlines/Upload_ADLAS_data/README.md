#Geneticlines ADLAS-data import

This is first attempt to make a simple scripts to upload data from ADLAS to Geneticllines biobank.

##Step 1.
Import data from ADLAS to entity=adlasportal_patients.
- RFQ requested
- script based on RFQ
- feedback RFQ import
- updated script based on feedback 10-08-2021

####TODO:
- get new RFQ data, more request, more tests (also other test)
- RFC, requested needs to change based on feedback
- Adapt script to process all data properly
- Add warnings and add options to go-on without error (leave item with status 'processed' on 'false')
- Handle items that could not be processed
- Handle data import EPIC
- Get ADLAS data via cURL into adlasportal_patients

##Step 2.
Import keys (all UMCGnr need geneticlines number)

##Step 3
Run script to transform data to be mapped to personal, clinicalEvent and testResults
order of running script:
- Run geneticlines_personal.py
- Run geneticlines_clinicalEvent.py
- Run geneticlines_testResult.py 

In geneticlines_testResult.py 
1. Map data to testResult
2. Move all processed data to adlasarchive_patients with data of processed
3. Remove all processed patients from adlasportal_patients
