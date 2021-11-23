#////////////////////////////////////////////////////////////////////////////
# FILE: 2.4-Labresults.py
# AUTHOR: Fernanda De Andrade
# CREATED: 21 september 2021
# MODIFIED: 23 november 2021 (added print)
# PURPOSE: Add pseudonimized test information to geneticlines, sources; ADLAS and EPIC.
# STATUS: in production
# COMMENTS: N/A
#////////////////////////////////////////////////////////////////////////////
import molgenis.client as molgenis
from datetime import datetime
from deep_translator import GoogleTranslator #need to be installed on server. Makes script SLOW
import pprint

# Save variables used through the entire script (not all are here,needs cleaning):
arguments = {"entityType1": "adlasportal_adlasData",
             "entityType2": "geneticlines_testResult",
             "url": "http://localhost:8080/api/",
             "sort1": "UMCGNR"
             }
# server session
session = molgenis.Session(arguments["url"],token="${molgenisToken}")

# Get a list with all adalasportaldata en tests
adlas = session.get(arguments["entityType1"], batch_size=1000, sort_column=arguments["sort1"])
print("\nEntityType: {}".format(arguments["entityType1"]))

for x in adlas:
    x['clinical_identifier'] = x['GEN_numr'] + '_' + x['ADVIESVRAAGNUMMER']
    x['genetic_testcode'] = x.get('TESTCODE')
    x['date_last_updated'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    if 'GA_GEN' in x:
        x['test_description'] = x['ADVIESVRAAGNUMMER'] + '_' + x['genetic_testcode']
        x['gene'] = x.get('GA_GEN')
        x['mutation'] = x.get('GA_MUTATIE')
        x['NM_numr'] = x.get('GA_NM_NUMMER')
        x['allele_frequency'] = x.get('GA_ALLELFREQUENTIE')
        x['inheritance'] = x.get('GA_OVERERVING')
    elif 'SGA_CYTOBAND' in x:
        x['test_description'] = x['ADVIESVRAAGNUMMER'] + '_' + x['genetic_testcode']
        x['type_test'] = '2'
        x['chromosome_region'] = x.get('SGA_CHROMOSOME_REGION')
        x['cytoband'] = x.get('SGA_CYTOBAND')
        x['DGV'] = x.get('SGA_DGV_SIMILARITY')
        x['CNV_event'] = x.get('SGA_EVENT')
        x['evidence_score'] = x.get('SGA_EVIDENCE_SCORE')
        x['CNV_lenght'] = x.get('SGA_LENGTH')
        x['no_of_probes'] = x.get('SGA_NO_OF_PROBES')
        x['OMIM_morbid_map_count'] = x.get('SGA_OMIM_MORBIDMAP_COUNT')
        x['probe_median'] = x.get('SGA_PROBE_MEDIAN')
        x['refseq_coding_genes_count'] = x.get('SGA_REFSEQ_CODING_GENES_COUNT')
        x['notes'] = x.get('SGA_NOTES')
        x['decipher_syndromes'] = x.get('SGA_DECIPHER_SYNDROMES')
        x['HM_related_gene'] = x.get('SGA_HMRELATED_GENES')
        x['HM_related_gene_count'] = x.get('SGA_HMRELATED_GENES_COUNT')
        x['mosaic_percentage'] = x.get('SGA_MOSAIC_PERCENTAGE')
        x['mosaic'] = x.get('SGA_MOSAIC')
        x['CNV_inheritance'] = x.get('SGA_OVERERVING')
        x['UMCG_NL_CNV_count'] = x.get('SGA_REGIONS_UMCG_CNV_NL_COUNT')
        x['similiar_cases'] = x.get('SGA_SIMILAR_PREVIOUS_CASES')
    else:
        x['testResult_id'] = x['clinical_identifier']
        x['type_test'] = 'other'
for x in adlas:
    if 'genetic_testcode' in x:
        if "NGS" in x['genetic_testcode']:
            x['type_test'] = '1'
        elif "NX" in x['genetic_testcode']:
            x['type_test'] = '1'
        elif "SVP" in x['genetic_testcode']:
            x['type_test'] = '1'
        elif "MLPA" in x['TESTOMSCHRIJVING']:
            x['type_test'] = '3'
        elif "Mutatie analyse" in x['TESTOMSCHRIJVING']:
            x['type_test'] = '4'
        else:
            x['type_test'] = '5'
#delete all None data
for x in adlas:
    filtered = {k: v for k, v in x.items() if v is not None}
    x.clear()
    x.update(filtered)
#translations
for x in adlas:
    if 'mutation' in x:
        x['mutation'] = GoogleTranslator(source='auto', target='en').translate(x['GA_MUTATIE'])
    if 'notes' in x:
        x['notes'] = GoogleTranslator(source='auto', target='en').translate(x['SGA_NOTES'])
#pprint.pprint(adlas)
# import all to geneticlines_testResult
for i in range(0, len(adlas), 1000):
    session.add_all(arguments["entityType2"], adlas[i:i+1000])
print("Total of geneticlines test:", len(adlas))
