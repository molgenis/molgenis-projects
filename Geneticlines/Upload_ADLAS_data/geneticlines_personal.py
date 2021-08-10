from datetime import date,datetime
import molgenis.client as molgenis

# Define molgenis.session
gen_session = molgenis.Session('https://geneticlines.molgeniscloud.org/api/', token='${molgenisToken}')

# Get a list with all adalasportaldata
adlasportal = gen_session.get('adlasportal_patients', batch_size=1000, sort_column='UMCGNR')

# Get a list with all IDs
keylist = gen_session.get('keylist_ids', batch_size=1000, sort_column='umcg_numr')

#get unique entries per gen_numr
unique_adlas = list({v['UMCGNR']:v for v in adlasportal}.values())

#add GEN_nr to adalasportaldata based on keylist >> to do escape when UMCGnr not present in keylist
for x in unique_adlas:
    for y in keylist:
        if x['UMCGNR'] == y['umcg_numr']:
            x['GEN_numr'] = y['GEN_numr']
#handle missing keys with except
#add maternal_id based on keylist
for x in unique_adlas:
    for y in keylist:
        try:
            if x['UCMGNR_MOEDER'] == y['umcg_numr']:
                x['maternal_id'] = y['GEN_numr']
        except KeyError:
            x['maternal_id'] = None

#add paternal_id based on keylist
for x in unique_adlas:
    for y in keylist:
        try:
            if x['UCMGNR_VADER'] == y['umcg_numr']:
                x['paternal_id'] = y['GEN_numr']
        except KeyError:
            x['paternal_id'] = None
#remove None key:value
for x in unique_adlas:
    if x['paternal_id'] == None :
        del x['paternal_id']
    if x['maternal_id'] == None :
        del x['maternal_id']
# add familynr:
# if 'Familieleden' in unique_adlas:
#     d['linked_family_ids'] = d.pop('Familieleden').replace(' ', '')

#determine year of birth instead of date
def year(born):
    born = datetime.strptime(born, "%d/%m/%Y %H:%M").date()
    return born.year
#determine age of death
def age(born,death):
    born = datetime.strptime(born, "%d/%m/%Y %H:%M").date()
    death= datetime.strptime(death, "%d/%m/%Y %H:%M").date()
    return death.year - born.year - ((death.month,
                                      death.day) < (born.month,
                                                    born.day))
#print(age('01/01/1950 00:00','01/01/2000 00:00'))

#make new headers for update (d['clinical_event'] = d['GEN_numr'] + '_' + d['ADVIESVRAAGNUMMER']<<mag niet one-to-many)
for d in unique_adlas:
    d['GEN_numr'] = d.pop('GEN_numr')
    d['year_birth'] = year(d['GEBOORTEDATUM'])
    d['is_deceased'] = 'true' #werkt niet, misschien true false??
    d['patient_status'] = 'C28554'
   ### #not always filled fields
    try:
        d['age_at_death'] = age(d['GEBOORTEDATUM'],d['DATUM_OVERLEDEN'])
        d['date_deceased'] = d.pop('DATUM_OVERLEDEN')
    except KeyError:
        d['age_at_death'] = None
        d['date_deceased'] = None
    # 'consanguinity': komt dit uit ADLAS?
    # 'twin_status': komt dit uit ADLAS?
for d in unique_adlas:
    if d['date_deceased'] == None:
        d['is_deceased'] = 'false'
        d['patient_status'] = 'C37987'
        del d['date_deceased']
        del d['age_at_death']
print(unique_adlas)

#test= [{'GEN_numr': 'GEN_003' , 'family_numr': 'FAM001','maternal_id': 'GEN_004'},{'GEN_numr': 'GEN_004' , 'family_numr': 'FAM001','dob':'2020-02-03'}]
#gen_session.delete_list('geneticlines_personal', ['GEN_003','GEN_004'])
gen_session.add_all('geneticlines_personal', unique_adlas)

# need to add procced in adalasportaldata in true
