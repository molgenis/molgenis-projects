#////////////////////////////////////////////////////////////////////////////
# FILE: 2.2-Individual Consent.py
# AUTHOR: Fernanda De Andrade
# CREATED: 22 september 2021
# MODIFIED: 22 october 2021 (remove geneticlines consent already present in database(add only new consentTypes))
# MODIFIED: 23 november 2021 (added print, check if storage present when deleting, studiecode update)
# PURPOSE: Add new consent information and already stored in storage table. And deleting storage data, for next night.
# STATUS: in production
# COMMENTS:N/A
#////////////////////////////////////////////////////////////////////////////
import molgenis.client as molgenis
from datetime import datetime
import pprint

# Save variables used through the entire script (not all are here,needs cleaning):
arguments = {"entityType1": "adlasportal_adlasData",
             "entityType2": "epicportal_patients",
             "entityType3": 'epicportal_consent',
             "entityType4": "geneticlines_individualconsent",
             "url": "http://localhost:8080/api/",
             "sort1": "UMCGNR",
             "sort2": "MRN"
             }
# server session
session = molgenis.Session(arguments["url"],token="${molgenisToken}")

# Get a list with all adalasportaldata en tests
adlas = session.get(arguments["entityType1"], batch_size=1000, sort_column=arguments["sort1"])
print("\nEntityType: {}".format(arguments["entityType1"]))
epic = session.get(arguments["entityType2"], batch_size=1000 , sort_column=arguments["sort2"])
print("\nEntityType: {}".format(arguments["entityType2"]))
storage = session.get(arguments["entityType3"], batch_size=1000)
print("\nEntityType: {}".format(arguments["entityType3"]))

#get unique entries per gen_numr
personal = list({v['GEN_numr']:v for v in adlas}.values())
# add none to 'antwoord_consent'
for x in personal:
    x['antwoord_consent'] = None
#add consentinfo from epic
for x in personal:
    for y in epic:
        if 'UMCGNR' in x:
            if x['UMCGNR'] == y['MRN']:
                if "Consent" in y['vraag']:
                    x['antwoord_consent'] = y['antwoord']
                    x['person_consenting'] = x['GEN_numr']
                    x['individual_consent_label'] = (x['antwoord_consent']).replace (" ","") + '_' + x['person_consenting']

#remove all dicts without consentInfo (antwoord_consent= None)
personal = [i for i in personal if not (i['antwoord_consent'] == None)]

#split antwoord_consent over multiple fields
for x in personal:
    if 'antwoord_consent' in x:
        x['antwoord_consent'] = x['antwoord_consent'].split(' - ')
        x['study_code'] = x['antwoord_consent'][0]
        x['status_study'] = x['antwoord_consent'][1]
        x['enrolment_status'] = x['antwoord_consent'][2]
        x['enrolment_date'] = datetime.strptime((x['antwoord_consent'][3]),"%d-%m-%Y").strftime("%Y-%m-%d")

#flag existing geneticlines consent present in storage
for x in storage:
    for y in personal:
        if 'study_code' in y:
            if y['study_code'] == '201800295' and x['person_consenting'] == y['person_consenting']:
                y['flag'] = True
for x in personal:
    if not 'flag' in x:
        x['flag'] = False
#delete items that are already in storage
withoutstorage = [i for i in personal if not (i['flag'] == True)]

#when geneticlines studiecode is NEWly present zet bool op true
for x in withoutstorage:
    if x['study_code'] == '201800295':
        x['consent_bool'] = 'true'
        x['consent_form_version'] = 'Version 06, 2021'
        x['leaflet_version'] = 'Version 07, 2021'
    else:
        x['consent_bool'] = 'false'

#change person_consenting to string and consent_level to list of ids
for x in storage:
    i=[]
    for y in x['consent_level']:
        i.append(y['id'])
    x['consent_level'] = i
# pprint.pprint(storage)
#add to consent from storage and new from nightly upload
for i in range(0, len(storage), 1000):
    session.add_all(arguments["entityType4"], storage[i:i+1000])
print("Number of consent from storage:", len(storage))
for i in range(0, len(withoutstorage), 1000):
    session.add_all(arguments["entityType4"], withoutstorage[i:i+1000])
print("Number of new consent:", len(withoutstorage))

#delete consent from storage
if len(storage) > 0:
    ids=[]
    for d in storage:
        ids.append(d['individual_consent_label'])
    for i in range(0, len(ids), 1000):
        session.delete_list(arguments["entityType3"], ids[i:i+1000])
print("Deleted from storage:",len(storage))
