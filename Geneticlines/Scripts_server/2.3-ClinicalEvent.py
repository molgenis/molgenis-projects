#////////////////////////////////////////////////////////////////////////////
# FILE: 2.3-ClinicalEvent.py
# AUTHOR: Fernanda De Andrade
# CREATED: 20 september 2021
# MODIFIED: 27 september 2021(add more items,add EPIC data)
# MODIFIED: 23 november 2021 (added print)
# PURPOSE: Add pseudonimized clinical Event data to geneticlines. Sources; ADLAS and EPIC.
# STATUS: in production
# COMMENTS: vertaling optie, 1 testcode per aanvraag, adviesvraag met meerdere UMCG en EPIC aanvragen koppelen aan aanvraag. Check alleen mogelijk met echte inclusie.
#////////////////////////////////////////////////////////////////////////////
import molgenis.client as molgenis
from datetime import datetime
from deep_translator import GoogleTranslator #need to be installed on server, makes script SLOW
import pprint

# Save variables used through the entire script (not all are here,needs cleaning):
arguments = {"entityType1": "adlasportal_adlasData",
             "entityType2": "epicportal_patients",
             "entityType3": 'geneticlines_moleculardiagngene',
             "entityType4": "geneticlines_counselingType",
             "entityType5": "geneticlines_diseaseGroup",
             "entityType6": "geneticlines_diagnosisGroup",
             "entityType7": "geneticlines_outcome",
             "entityType8":"geneticlines_clinicalEvent",
             "url": "http://localhost:8080/api/",
             "sort1": "UMCGNR",
             "sort2": "MRN",
             }
# server session
session = molgenis.Session(arguments["url"],token="${molgenisToken}")

# Get a list with all adalasportaldata en tests
adlas = session.get(arguments["entityType1"], batch_size=1000, sort_column=arguments["sort1"])
print("\nEntityType: {}".format(arguments["entityType1"]))
epic = session.get(arguments["entityType2"], batch_size=1000 , sort_column=arguments["sort2"])
print("\nEntityType: {}".format(arguments["entityType2"]))
genes = session.get(arguments["entityType3"], batch_size=1000 )
print("\nEntityType: {}".format(arguments["entityType3"]))
counseling = session.get(arguments["entityType4"], batch_size=1000)
print("\nEntityType: {}".format(arguments["entityType4"]))
diseaseGroup = session.get(arguments["entityType5"], batch_size=1000)
print("\nEntityType: {}".format(arguments["entityType5"]))
diagnosisGroup = session.get(arguments["entityType6"], batch_size=1000)
print("\nEntityType: {}".format(arguments["entityType6"]))
outcome =session.get(arguments["entityType7"], batch_size=1000)
print("\nEntityType: {}".format(arguments["entityType7"]))

#'molecular_diagnosis_gene': samengesteld met alle GA_GEN voor 1 adviesID en UMCGnr
#get collection genes...
list_of_genes = {}
for i in adlas:
    aanvraag = i['ADVIESVRAAGNUMMER']
    if aanvraag not in list_of_genes:
        list_of_genes[aanvraag] = set()
    list_of_genes[aanvraag].add(i.get('GA_GEN', None))

for i in adlas:
    if 'GA_GEN' in i:
        aanvraag = i['ADVIESVRAAGNUMMER']
        i['molecular_diagnosis_gene'] = list(list_of_genes[aanvraag])

#list only genes present in genes
for x in adlas:
    for k, v in x.items():
        if(isinstance(v, list)):
            a= []
            for l in v:
                for y in genes:
                    if l== y['value']:
                        a.append(y['value'])
            x['molecular_diagnosis_gene'] = a
#not present in HGNC
for x in adlas:
    if 'GA_GEN' in x:
        if not any(y['value'] == x['GA_GEN'] for y in genes):
            x['notHGNC'] = x['GA_GEN']
#add items for clinicalEvent upload
for x in adlas:
    x['genetic_testcode'] = x.get('TESTCODE') #<<niet alle codes aanwezig<als 1 testcode per aanvraag dan deze oplossing
    x['testcode_decription'] = x['TESTOMSCHRIJVING']
    x['outcome_text'] = x.get('EINDUITSLAGTEKST')
    x['date_last_updated'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    x['clinical_identifier'] = x['GEN_numr'] + '_' + x['ADVIESVRAAGNUMMER']
    x['belongs_to_person'] = x['GEN_numr']
    x['application_date'] = x.get('ADVIESVRAAG_DATUM')
    x['outcome_date']  = x.get('EINDUITSLAG_DATUM')
    if 'molecular_diagnosis_gene' in x:
        x['molecular_diagnosis_gene'] = ",".join(x['molecular_diagnosis_gene'])

#remove None values
for x in adlas:
    filtered = {k: v for k, v in x.items() if v is not None}
    x.clear()
    x.update(filtered)

#get unique entries per adviesvraagnr ?need to extend if UMCGnr has same adviesvraagnr?<<straks aanpassen, meerdere UMCGnr aan 1 adviesvraag
unique_adlas = list({v['ADVIESVRAAGNUMMER']:v for v in adlas}.values())

#ADD EPIC DATA
for x in unique_adlas:
    for y in epic:
        if 'UMCGNR' in x:
            if x['UMCGNR'] == y['MRN']:
                if "GENONDERWERP" in y['vraag']:
                    x['diagnosis_group'] = y['antwoord']
                if "TYPE COUNSELING" in y['vraag']:
                    x['counseling_type'] = y['antwoord']
                if "DATUMSLUITENDOSSIERGENETICA" in y['vraag']:
                    x['diagnosis_date'] = y['antwoord']
                if "Problem" in y['vraag']:
                    x['problem'] = y['antwoord']
                if "DIAGNOSE IMMUNOLOGISCH" in y['vraag']:
                    x['disease2'] = y['antwoord']
                elif "DIAGNOSE ANDERE AANGEBOREN AFWIJKIGEN" in y['vraag']:
                    x['disease2'] = y['antwoord']
                elif "DIAGNOSE OVERIGE NIET PASSEND" in y['vraag']:
                    x['disease2'] = y['antwoord']
                elif "DIAGNOSEBINDWEEFSEL" in y['vraag']:
                    x['disease2'] = y['antwoord']
                elif "DIAGNOSECHROMOSOOMAFWIJKING" in y['vraag']:
                    x['disease2'] = y['antwoord']
                elif "DIAGNOSEEPILEPSIE" in y['vraag']:
                    x['disease2'] = y['antwoord']
                elif "DIAGNOSEGENODERMATOSEN" in y['vraag']:
                    x['disease2'] = y['antwoord']
                elif "DIAGNOSEGENONCOHM" in y['vraag']:
                    x['disease2'] = y['antwoord']
                elif "DIAGNOSENEUROGENETICA" in y['vraag']:
                    x['disease2'] = y['antwoord']
                elif "DIAGNOSENIERAANDOENING" in y['vraag']:
                    x['disease2'] = y['antwoord']
                elif "DIAGNOSEONCOGENNZ" in y['vraag']:
                    x['disease2'] = y['antwoord']
                elif "DIAGNOSEONGENA-G" in y['vraag']:
                    x['disease2'] = y['antwoord']
                elif "DIAGNOSEONTWIKKELINGSACHTERSTAND" in y['vraag']:
                    x['disease2'] = y['antwoord']
                elif "DIAGNOSEOOGAFWIJKINGEN" in y['vraag']:
                    x['disease2'] = y['antwoord']
                elif "DIAGNOSESKELET" in y['vraag']:
                    x['disease2'] = y['antwoord']
                elif "GENDIAGNOSELIJSTCARDIO" in y['vraag']:
                    x['disease2'] = y['antwoord']
                elif "GENDIAGNOSELIJSTONCO" in y['vraag']:
                    x['disease2'] = y['antwoord']
                elif "DIAGNOSESLECHTHORENHEID" in y['vraag']:
                    x['disease2'] = y['antwoord']
                elif "ANDERSDIAGNOSE" in y['vraag']:
                    x['other_diagnosis']= y['antwoord']
#Adding internal lookup values
#adding outcomecodes based on internal lookup
for x in unique_adlas:
    for y in outcome:
        if 'EINDUITSLAG' in x:
            if x['EINDUITSLAG'] == y['labelNL']:
                x['outcome'] = y['id']
for x in unique_adlas:
    for y in diagnosisGroup:
        if 'diagnosis_group' in x:
            if x['diagnosis_group'] == y['labelNL']:
                x['diagnosis_group'] = y['id']
for x in unique_adlas:
    for y in counseling:
        if 'counseling_type' in x:
            if x['counseling_type'] == y['labelNL']:
                x['counseling_type'] = y['id']
for x in unique_adlas:
    for y in diseaseGroup:
        if 'disease2' in x:
            if x['disease2'] == y['labelNL']:
                x['disease_group'] = y['id']
            else:
                x['other_diagnosis'] =x['disease2']
for x in unique_adlas:
    for y in diseaseGroup:
        if 'other_diagnosis' in x:
            if x['other_diagnosis'] == y['labelNL']:
                del x['other_diagnosis']
#add probleminfo, need to split string
for x in unique_adlas:
    if 'problem' in x:
        x['problem'] = x['problem'].split(' - ')
        x['disease'] = x['problem'][0]
        x['problem_start_date'] = datetime.strptime((x['problem'][1]),"%d-%m-%Y").strftime("%Y-%m-%d")
        x['problem_end_date'] = datetime.strptime((x['problem'][2]),"%d-%m-%Y").strftime("%Y-%m-%d")
#changing dateformats
for x in unique_adlas:
    if 'diagnosis_date' in x:
        if "T" in x['diagnosis_date']:
            x['diagnosis_date'] = (x['diagnosis_date']).replace ("T00:00","")
        else:
            x['diagnosis_date'] = datetime.strptime((x['diagnosis_date']),"%m/%d/%Y").strftime("%Y-%m-%d")
    if 'application_date' in x:
        x['application_date'] = (x['application_date']).replace ("T00:00","")
    if 'outcome_date' in x:
        x['outcome_date']  = (x['outcome_date']).replace ("T00:00","")
#adding translations
for x in unique_adlas:
    if 'testcode_decription' in x:
        x['testcode_decription'] = GoogleTranslator(source='auto', target='en').translate(x['testcode_decription'])
    if 'outcome_text' in x:
        x['outcome_text'] = GoogleTranslator(source='auto', target='en').translate(x['outcome_text'])
#pprint.pprint(unique_adlas)
#import all to clinicalevent
for i in range(0, len(unique_adlas), 1000):
    session.add_all(arguments["entityType8"], unique_adlas[i:i+1000])
print("Total of geneticlines clinicalEvents:", len(unique_adlas))
