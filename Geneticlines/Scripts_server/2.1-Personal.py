#////////////////////////////////////////////////////////////////////////////
# FILE: 2.1-Personal.py
# AUTHOR: Fernanda De Andrade
# CREATED: 20 september 2021
# MODIFIED: 21 october(make use of combine table and linked family needed adjustment)
# MODIFIED: 23 november 2021 (added print)
# PURPOSE: Add pseudonimized personal information to geneticlines, sources; ADLAS and EPIC.
# STATUS: in production
# COMMENTS: more then 1000 geneticlines participants give trouble with maternal, paternal and linked familyids. Geslacht en geboortedatum moeten altijd gevuld,anders krijg je error(dit is wat afgesproken is met ADLAS team)
#////////////////////////////////////////////////////////////////////////////
import molgenis.client as molgenis
from datetime import datetime
import pprint

# Save variables used through the entire script:
arguments = {"entityType1": "adlasportal_adlasData",
             "entityType2": "epicportal_patients",
             "entityType3": "geneticlines_personal",
             "url": "http://localhost:8080/api/",
             "sort1":"GEN_numr",
             "sort2": "MRN"
             }
# server session
session = molgenis.Session(arguments["url"],token="${molgenisToken}")

# Get a list with all adalasportaldata en tests
adlaspatients = session.get(arguments["entityType1"], batch_size=1000, sort_column=arguments["sort1"])
print("\nEntityType: {}".format(arguments["entityType1"]))
epic = session.get(arguments["entityType2"], batch_size=1000 , sort_column=arguments["sort2"])
print("\nEntityType: {}".format(arguments["entityType2"]))

#functions used in this script
#determine year of birth instead of date
def year(born):
    born = datetime.strptime(born, "%Y-%m-%dT%H:%M").date()
    return born.year
#determine age of death
def age(born,death):
    born = datetime.strptime(born, "%Y-%m-%dT%H:%M").date()
    death= datetime.strptime(death, "%Y-%m-%dT%H:%M").date()
    return death.year - born.year - ((death.month,
                                      death.day) < (born.month,
                                                    born.day))

#get unique entries per gen_numr
personal = list({v['GEN_numr']:v for v in adlaspatients}.values())

#add items to personal
for d in personal:
    d['is_deceased'] = 'true'
    d['patient_status'] = 'C28554'
    d['date_last_updated'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    d['year_birth'] = year(d['GEBOORTEDATUM'])##need geboortedatum, if not filled ==>ERROR
    d['biological_sex'] = d['GESLACHT'] ##need Geslacht, if not filled ==>ERROR
    d['biological_sex'] = d['biological_sex'].replace('Vrouw','383')
    d['biological_sex'] = d['biological_sex'].replace('Man','384')
    #not always filled fields
    try:
        d['age_at_death'] = age(d['GEBOORTEDATUM'],d['DATUM_OVERLEDEN'])
        d['date_deceased'] = d.pop('DATUM_OVERLEDEN')
    except KeyError:
        d['age_at_death'] = None
        d['date_deceased'] = None
    # 'twin_status': komt dit uit EPIC
for d in personal:
    if d['date_deceased'] == None:
        d['is_deceased'] = 'false'
        d['patient_status'] = 'C37987'
        del d['date_deceased']
        del d['age_at_death']

#'///////////////////////////////////ADDING CONTENT from EPICportal//////////////////////////////////////////
#add EPIC firt consultdate
for x in personal:
    for y in epic:
        if "UMCGNR" in x:
            if x['UMCGNR'] == y['MRN']:
                x['date_first_consult'] = y['Firstconsultdate']

#change dateformat
for x in personal:
    if 'date_first_consult' in x:
        if "T" in x['date_first_consult']:
            x['date_first_consult'] = (x['date_first_consult']).replace ("T00:00","")
        elif x['date_first_consult'] == "NULL":
            x['date_first_consult'] = None
        else:
            #print(type(x['date_first_consult']))
            x['date_first_consult'] = datetime.strptime((x['date_first_consult']),"%m/%d/%Y").strftime("%Y-%m-%d")
#///////////////////////////////////IMPORT PERSONALinfo/////////////////////////////////////////
#add items to personal (if more then 1000, it is possible)
sortpersonal = sorted(personal, key=lambda d: d['UMCGNR'])

for i in range(0, len(sortpersonal), 1000):
    session.add_all(arguments["entityType3"], sortpersonal[i:i+1000])
print("Total of geneticlines participants: ", len(sortpersonal))
#///////////////////////////////////IMPORT linked personaldata/////////////////////////////////////////
#session.update_one("geneticlines_personal", "id", "paternal_id", "newValue")
#add paternal and maternalids, since 1000 add give problems, need to add referring personalIDs on later stage
for x in personal:
    if 'mama' in x:
        session.update_one(arguments["entityType3"], x['GEN_numr'], "maternal_id", x['mama'])
        print("maternalid:",x['mama'])
    if 'papa' in x:
        session.update_one(arguments["entityType3"], x['GEN_numr'], "paternal_id", x['papa'])
        print("maternalid:",x['papa'])
    if 'FAMILIELEDEN' in x:
        session.update_one(arguments["entityType3"], x['GEN_numr'], "linked_family_ids", x['FAMILIELEDEN'])
        print("linked family:",x['FAMILIELEDEN'])
