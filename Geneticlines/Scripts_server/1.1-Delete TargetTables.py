#////////////////////////////////////////////////////////////////////////////
# FILE: 1.1-Delete TargetTables.py
# AUTHOR: Fernanda De Andrade
# CREATED: 17 october 2021
# MODIFIED: 22 october 2021 (xref en mref personal give trouble when deleting with more then 1000 patients)
# MODIFIED: 22 november 2021 (now empty tables are OK, check on storage if empty)
# PURPOSE: delete all data from geneticlines tables to be restored with new data uploaded every night. And store manually adjusted consent information in temporay storage.
# STATUS: in production
# COMMENTS: needs update personal delete if more then 1000 patients are included, testcode commented below
#////////////////////////////////////////////////////////////////////////////
import pprint
import molgenis.client as molgenis

# Save variables used through the entire script (not all are here,needs cleaning):
arguments = {"entityType1": "geneticlines_personal",
             "entityType2": "geneticlines_individualconsent",
             "entityType3": "geneticlines_clinicalEvent",
             "entityType4": "geneticlines_testResult",
             "entityType5": "epicportal_consent",
             "url": "http://localhost:8080/api/",
             "sort1": "GEN_numr",
             "sort2": "individual_consent_id",
             "sort3": "clinical_identifier",
             "sort4": "testResult_id"
             }
# server session, token
session = molgenis.Session(arguments["url"], token="${molgenisToken}")

# Get a list with all data from geneticlines
personal = session.get(arguments["entityType1"], batch_size=1000, sort_column=arguments["sort1"])
print("\nEntityType: {}".format(arguments["entityType1"]))
consent = session.get(arguments["entityType2"], batch_size=1000, sort_column=arguments["sort2"])
print("\nEntityType: {}".format(arguments["entityType2"]))
clinicalEvent = session.get(arguments["entityType3"], batch_size=1000, sort_column=arguments["sort3"])
print("\nEntityType: {}".format(arguments["entityType3"]))
testResult = session.get(arguments["entityType4"], batch_size=1000, sort_column=arguments["sort3"])
print("\nEntityType: {}".format(arguments["entityType4"]))
storage = session.get(arguments["entityType5"], batch_size=1000, sort_column=arguments["sort2"])
print("\nEntityType: {}".format(arguments["entityType5"]))

## 1. Store Consent Information manually adjusted to temporary storage within server
#push geneticlines consent data to epicportal to store manual added information geneticlines code= 201800295
genconsent = [i for i in consent if (i['study_code'] == '201800295')]
print("Number of geneticlines consent that need to be temporarily stored : ", len(genconsent))

#change person_consenting and consent_level to string
for x in genconsent:
    x['person_consenting'] = ((x['person_consenting'])['GEN_numr'])
for x in genconsent:
    i=[]
    for y in x['consent_level']:
        i.append(y['id'])
    x['consent_level'] = i

#Check if epicportal_consent is empty, if NOT empty; delete table information
if len(storage) > 0:
    ids=[]
    for x in storage:
        ids.append(x['individual_consent_id'])
    for i in range(0, len(ids), 1000):
        session.delete_list(arguments["entityType5"], ids[i:i+1000])
        print("Temporary storge NOT empty, deleted: ", ids)

#store information in epicportal_consent
if len(genconsent) > 0:
    for i in range(0, len(genconsent), 1000):
        session.add_all(arguments["entityType5"], genconsent[i:i+1000])
    print("Number of geneticlines consent that is stored: ", len(genconsent))

## 2. Delete all data from geneticlines tables to be restored with new data uploaded every night
ids4=[]
for d in testResult:
    ids4.append(d['testResult_id'])
for i in range(0, len(ids4), 1000):
    session.delete_list(arguments["entityType4"], ids4[i:i+1000])
print("Deleted Lab results: ", len(ids4))

ids3=[]
for d in clinicalEvent:
    ids3.append(d['clinical_identifier'])
for i in range(0, len(ids3), 1000):
    session.delete_list(arguments["entityType3"], ids3[i:i+1000])
print("Deleted Clinical Events: ", len(ids3))

ids2=[]
for d in consent:
    ids2.append(d['individual_consent_id'])
for i in range(0, len(ids2), 1000):
    session.delete_list(arguments["entityType2"], ids2[i:i+1000])
print("Deleted Individual Consent: ", len(ids2))
##NEEDS update linked fam, paternal and maternal, when more then 1000 patienst are included!!
#Need to change paternal, maternal and familyIDs to last Gen_numr(give problem with more then 1000 patient)
#this solution does not work with 15778 patients and a lot of linked families
# sortpersonal = sorted(personal, key=lambda d: d['GEN_numr'])
# fakeLinkedID=[d['GEN_numr'] for d in sortpersonal]
# for x in sortpersonal:
#     if 'maternal_id' in x:
#         session.update_one("geneticlines_personal", x['GEN_numr'], "maternal_id", fakeLinkedID[-1])
#     if 'paternal_id' in x:
#         session.update_one("geneticlines_personal", x['GEN_numr'], "paternal_id", fakeLinkedID[-1])
#     if 'linked_family_ids' in x:
#         session.update_one("geneticlines_personal", x['GEN_numr'], "linked_family_ids", fakeLinkedID[-1])
#delete data from personal
ids=[]
for d in personal:
    ids.append(d['GEN_numr'])
for i in range(0, len(ids), 1000):
    session.delete_list(arguments["entityType1"], ids[i:i+1000])
print("Deleted Personal: ", len(ids))

