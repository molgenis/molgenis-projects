Running in mapper

1. Setup/Active a virtual environment (see python setup below)
2. Install dependencies in the virtual environment ( if not installed)

   `pip install -r requirements.txt`
3. run the following scripts sequentially using a batch file:

    `python remodel_lc_vars.py`
    `python remodel_source_vars.py -pw <pw for server>`
    `python remodel_mappings.py -pw <pw for server>`

4. mapped data can been seen in /output folder

Upload data:

1. In table VariableValues: duplicate keys: [ALSPAC,1.0.0,core,g591,2, ALSPAC,1.0.0,core,g650,2],
Change duplicate value for both variables to -2 for label 'No partner'
2. In table VariableMappings: delete many trailing spaces at MOBA mapping to 'prepreg_ed
     ' and MOBA mapping to 'preg_ed                     ' (duplicates in old LifeCycle variables) 
3. rezip all files in output folder
4. Upload output.zip to a new emx2 schema.


## Python setup

Create a new environment

`python -m venv venv` 

Activate the environment

`source venv/bin/activate`

Install deps

`pip install [name-of-dep]`

List packages in active env 

`pip list`

Create requirements.txt file from current active setup

`pip freeze > requirements.txt`

Install dependencies from requirements.txt file

`pip install -r requirements.txt`

Deactivate currently active environment

`deactivate`

More info see: 

mac: https://www.youtube.com/watch?v=Kg1Yvry_Ydk 

window: https://www.youtube.com/watch?v=APOPm01BVrk