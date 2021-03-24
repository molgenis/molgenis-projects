This script can be used to compare attributes in directories that have staging areas that map to a 
common database, such as the BBMRI_ERIC directory.

Inside the script fill out the Molgenis entityTypes that you would like to compare in the dictionaries "main_area" and 
"staging areas". Define the attributes that you want to compare in "comparison_list".

Run the script in cmd:
attribute_checks.py -url https://myserver.org -pw myPassword

Output are a txt file per 'main_area' entityType describing the differences in the specified attribute characteristics in the 'staging area' entityTypes.