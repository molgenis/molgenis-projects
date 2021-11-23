#////////////////////////////////////////////////////////////////////////////
# FILE: 0.1-Delete rawTables.py
# AUTHOR: Fernanda De Andrade
# CREATED: 24 october 2021
# MODIFIED: 22 november 2021 (add print and decsriptions)
# PURPOSE: deleting staging areas in order to import new data (ADLAS 3:00 cURL)
# STATUS: (partly) in production (only ADLAS part in production working)
# COMMENTS: EPIC data is going to be larger..we are waiting on file containing sample information.
#////////////////////////////////////////////////////////////////////////////
import molgenis.client as molgenis

# Save variables used through the entire script (not all are here,needs cleaning):
arguments = {"entityType1": "adlasportal_patients",
             "entityType2": "adlasportal_tests",
             "entityType3": "epicportal_patients",
             "url": "http://localhost:8080/api/",
             "sort1":"UMCG_NUMMER",
             "sort2": "UMCGNR",
             "sort3": "MRN"
             }
# server session
session = molgenis.Session(arguments["url"], token="${molgenisToken}")

# Get all data from portaltables
adlaspatient = session.get(arguments["entityType1"], batch_size=1000, sort_column=arguments["sort1"])
print("\nEntityType: {}".format(arguments["entityType1"]))
adlastest = session.get(arguments["entityType2"], batch_size=1000, sort_column=arguments["sort2"])
print("\nEntityType: {}".format(arguments["entityType2"]))
epicpatient = session.get(arguments["entityType3"], batch_size=1000, sort_column=arguments["sort3"])
print("\nEntityType: {}".format(arguments["entityType3"]))

#delete all data from ADLASportal
ids=[]
for d in adlaspatient:
    ids.append(d['id'])
for i in range(0, len(ids), 1000):
    session.delete_list(arguments["entityType1"], ids[i:i+1000])
print("Deleted adlaspatients: ", len(ids))

ids2=[]
for d in adlastest:
    ids2.append(d['id'])
for i in range(0, len(ids2), 1000):
    session.delete_list(arguments["entityType2"], ids2[i:i+1000])
print("Deleted adlastests: ", len(ids2))

#Not yet in operation, need EPIC decisions for automated upload
#delete all data from EPICportal
# ids3=[]
# for d in epicpatient:
#     ids3.append(d['id'])
# for i in range(0, len(ids3), 1000):
#     session.delete_list(arguments["entityType3"], ids3[i:i+1000])
#print("Deleted EPICdata: ", len(ids3))
