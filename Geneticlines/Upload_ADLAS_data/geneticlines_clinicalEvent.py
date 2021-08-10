from datetime import date,datetime
import molgenis.client as molgenis
from deep_translator import GoogleTranslator #need to be installed on server if desired action translating dutch tekst to english

# Define molgenis.session
gen_session = molgenis.Session('https://geneticlines.molgeniscloud.org/api/', token='${molgenisToken}')

# Get a list with all adalasportaldata
adlasportal = gen_session.get('adlasportal_patients', batch_size=1000, sort_column='UMCGNR')

# Get a list with all IDs
keylist = gen_session.get('keylist_ids', batch_size=1000, sort_column='umcg_numr')

#add GEN_nr to adalasportaldata based on keylist
for x in adlasportal:
    for y in keylist:
        if x['UMCGNR'] == y['umcg_numr']:
            x['GEN_numr'] = y['GEN_numr']

#make new headers for update
for d in adlasportal:
    d['clinical_identifier'] = d['GEN_numr'] + '_' + d['ADVIESVRAAGNUMMER']
    d['belongs_to_person'] = d.pop('GEN_numr')
    d['application_date'] = (d['ADVIESVRAAG_DATUM']).replace (" 00:00","")
    d['genetic_testcode'] = d.pop('TESTCODE') #<<niet alle codes aanwezig<als 1 testcode per aanvraag dan deze oplossing
    d['testcode_decription'] = GoogleTranslator(source='auto', target='en').translate(d['TESTOMSCHRIJVING'])
    d['outcome'] = GoogleTranslator(source='auto', target='en').translate(d['EINDUITSLAG'])
    d['outcome_text'] = GoogleTranslator(source='auto', target='en').translate(d['EINDUITSLAGTEKST'])
    d['outcome_date']  = (d['EINDUITSLAG_DATUM']).replace (" 00:00","")
    d['date_last_updated'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

#change date format
for d in adlasportal:
    d['application_date'] = datetime.strptime((d['application_date']),"%d/%m/%Y").strftime("%Y-%m-%d")
    d['outcome_date']  = datetime.strptime((d['outcome_date']),"%d/%m/%Y").strftime("%Y-%m-%d")

#'molecular_diagnosis_gene' : samengesteld met alle GA_GEN voor 1 adviesID en UMCG d.get('GA_GEN')
#get collection genes...
list_of_genes = {}
for i in adlasportal:
    aanvraag = i['ADVIESVRAAGNUMMER']
    if aanvraag not in list_of_genes:
        list_of_genes[aanvraag] = set()
    list_of_genes[aanvraag].add(i.get('GA_GEN', None))

for i in adlasportal:
    if 'GA_GEN' in i:
        aanvraag = i['ADVIESVRAAGNUMMER']
        i['molecular_diagnosis_gene'] = list(list_of_genes[aanvraag]) #resut>>['ABCC6', 'AFF4', 'GPR143', 'ARHGAP31', 'COL4A3', 'RAF1', 'MYO7A', None]
        i['molecular_diagnosis_gene'] = ' '.join(map(str, i['molecular_diagnosis_gene'] )).replace(' ', ',')
# result is ['gen01','gen02', None, 'gen03'] needs to change to gen01,gen02,gen03>>if GL result are not imported no problem

#get unique entries per adviesvraagnr ?need to extend if UMCGnr has same adviesvraagnr?<<straks aanpassen, meerdere UMCGnr aan 1 adviesvraag
unique_adlas = list({v['ADVIESVRAAGNUMMER']:v for v in adlasportal}.values())
#print(unique_adlas)
#import all to clinicalevent
gen_session.add_all('geneticlines_clinicalEvent', unique_adlas)


