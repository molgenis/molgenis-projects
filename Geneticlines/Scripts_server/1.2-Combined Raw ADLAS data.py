#////////////////////////////////////////////////////////////////////////////
# FILE: 1.2-Combined Raw ADLAS data.py
# AUTHOR: Fernanda De Andrade
# CREATED: 21 October 2021
# MODIFIED: 23 november 2021 (added print, check if table empty)
# PURPOSE: new table to get all ADLAS data from geneticlines participants in one table, to make other scripts faster
# STATUS: in production
# COMMENTS: Does not work if patients are included but NOT present with test(s).
#////////////////////////////////////////////////////////////////////////////
import molgenis.client as molgenis
import pprint

# Save variables used through the entire script:
arguments = {"entityType1": "adlasportal_patients",
             "entityType2": "adlasportal_tests",
             "entityType3": "keylist_ids",
             "entityType4": "adlasportal_adlasData",
             "url": "http://localhost:8080/api/",
             "sort1":"UMCG_NUMMER",
             "sort2": "UMCGNR",
             "sort3": "OriginalId"
             }
# server session
session = molgenis.Session(arguments["url"],token="${molgenisToken}")

# Get a list with all adalasportaldata en tests
adlaspatients = session.get(arguments["entityType1"], batch_size=1000, sort_column=arguments["sort1"])
print("\nEntityType: {}".format(arguments["entityType1"]))
adlastest = session.get(arguments["entityType2"], batch_size=1000, sort_column=arguments["sort2"])
print("\nEntityType: {}".format(arguments["entityType2"]))
keylist = session.get(arguments["entityType3"], batch_size=1000, sort_column=arguments["sort3"])
print("\nEntityType: {}".format(arguments["entityType3"]))
combine = session.get(arguments["entityType4"], batch_size=1000, sort_column=arguments["sort2"])
print("\nEntityType: {}".format(arguments["entityType4"]))
#///////////////////////////////////ADDING keys from keylist//////////////////////
#add GEN_nr to adlastest based on keylist
print("Number of patients present in ADLAS test table: ", len(adlastest))
for x in adlastest:
    for y in keylist:
        if 'UMCGNR' in x:
            if x['UMCGNR'] == y['OriginalId']:
                x['GEN_numr'] = y['id']
                x['start_date'] = y['create_date']
            else:
                x['geenGennumr'] = x['UMCGNR']
        else:
            x['GEN_numr'] = None
#add None to UMCGnr not present in keylist
for x in adlastest:
    for y in keylist:
        if 'geenGennumr' in x:
            if x['geenGennumr'] == y['OriginalId']:
                del x['geenGennumr']
for x in adlastest:
    if 'geenGennumr' in x:
        x['geenGennumr']= None
        x['GEN_numr']= x.pop('geenGennumr')
# to delete patients without matching Gen_numr, values are "None" in dictionary
adlastest = [i for i in adlastest if not (i['GEN_numr'] == None)]
# #add maternal_id and paternal_id based on keylist
for x in adlaspatients:
    for y in keylist:
        if 'UMCG_MOEDER' in x:
            if x['UMCG_MOEDER'] == y['OriginalId']:
                x['mama'] = y['id']
        if 'UMCG_VADER' in x:
            if x['UMCG_VADER'] == y['OriginalId']:
                x['papa'] = y['id']
#add familymembers:
for x in adlaspatients:
    if 'FAMILIELEDEN' in x:
        x['FAMILIELEDEN'] = x['FAMILIELEDEN'].split(", ")
#replace familyIDs with exsiting GENnrs (if family not present with GENnr, ids will be removed)
for x in adlaspatients:
    for k, v in x.items():
        if(isinstance(v, list)):
            a= []
            for l in v:
                for y in keylist:
                    if l == y['OriginalId']:
                        a.append(y['id'])
            x['FAMILIELEDEN']= ",".join(a)
print("Number of patients present in ADLAS patient table: ", len(adlaspatients))
#///////////////////////////////////ADDING CONTENT from patients to test//////////////////////////////////////////
# #add geboortedatum,sex,linked fam,maternalid and paternalid to adlastest
for x in adlastest:
    for y in adlaspatients:
        if 'UMCGNR' in x:
            if x['UMCGNR'] == y['UMCG_NUMMER']:
                x['GEBOORTEDATUM'] = y['GEBOORTEDATUM']
                x['GESLACHT'] = y.get('GESLACHT')
                x['mama'] = y.get('mama')
                x['papa'] = y.get('papa')
                x['FAMILIELEDEN'] = y.get('FAMILIELEDEN')
                x['DATUM_OVERLEDEN'] = y.get('OVERLIJDENSDATUM')
#delete all None data
for x in adlastest:
    filtered = {k: v for k, v in x.items() if v is not None}
    x.clear()
    x.update(filtered)
#///////////////////////////////////Add combined data to one table//////////////////////////////////////////
#check if combine table is EMPTY, if NOT remove content to make space for new data
if len(combine) > 0:
    ids=[]
    for x in combine:
        ids.append(x['id'])
    for i in range(0, len(ids), 1000):
        session.delete_list(arguments["entityType4"], ids[i:i+1000])
        print("ADLAS combine table NOT empty, deleted: ", ids)

#Add all data from both ADLAS tables (collected in adlastest) in one table
for i in range(0, len(adlastest), 1000):
    session.add_all(arguments["entityType4"], adlastest[i:i+1000])
print("Total of geneticlines tests: ", len(adlastest))
