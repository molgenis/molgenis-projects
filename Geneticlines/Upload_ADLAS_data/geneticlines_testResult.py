from datetime import date,datetime
import molgenis.client as molgenis

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
    d['genetic_testcode'] = d.pop('TESTCODE')
    d['lab_result_date'] = (d['LABUITSLAG_DATUM']).replace (" 00:00","")


#'lab_results_id': #based on gene or CNV'samengestelde naam(clinical_id, testresult)
for d in adlasportal:
    if 'GA_GEN' in d:
        d['testResult_id'] = (d['GA_MUTATIE']).replace("." , "").replace(">" , "-").replace(" " , "_").replace('(' , "").replace(")" , "")
        d['testResult_id'] = d['clinical_identifier'] + '_' + d['GA_GEN'] + '_' + d['testResult_id']
        d['type_test'] = 'NGS'
        d['gene'] = d.pop('GA_GEN')
        d['mutation'] = d.pop('GA_MUTATIE')
        d['NM_numr'] = d.pop('GA_NM_NUMMER')
        d['allele_frequency'] = d.pop('GA_ALLELFREQUENTIE')
        d['inheritance'] = d.pop('GA_OVERERVING')
    elif 'SGA_CYTOBAND' in d:
        d['testResult_id'] = d['clinical_identifier'] + '_' + d['SGA_CYTOBAND'].replace(' - ', '_')
        d['type_test'] = 'array'
        d['chromosome_region'] = d.pop('SGA_CHROMOSOME_REGION')
        d['cytoband'] = d.pop('SGA_CYTOBAND')
        d['DGV'] = d.pop('SGA_DGV_SIMILARITY')
        d['CNV_event'] = d.pop('SGA_EVENT')
        d['evidence_score'] = d.pop('SGA_EVIDENCE_SCORE')
        d['HM_related_gene_count'] = d.pop('SGA_HMRELATED_GENES_COUNT')
        d['CNV_lenght'] = d.pop('SGA_LENGTH')
        d['mosaic_percentage'] = d.pop('SGA_MOSAIC_PERCENTAGE')
        d['no_of_probes'] = d.pop('SGA_NO_OF_PROBES')
        d['notes'] = d.pop('SGA_NOTES')
        d['OMIM_morbid_map_count'] = d.pop('SGA_OMIM_MORBIDMAP_COUNT')
        d['probe_median'] = d.pop('SGA_PROBE_MEDIAN')
        d['refseq_coding_genes_count'] = d.pop('SGA_REFSEQ_CODING_GENES_COUNT')
        d['similiar_cases'] = d.pop('SGA_SIMILAR_PREVIOUS_CASES')
    elif 'SGA_DECIPHER_SYNDROMES' in d:
        d['decipher_syndromes'] = d.pop('SGA_DECIPHER_SYNDROMES')
    elif 'SGA_HMRELATED_GENES' in d:
        d['HM_related_gene'] = d.pop('SGA_HMRELATED_GENES')
    elif 'SGA_MOSAIC' in d:
        d['mosaic'] = d.pop('SGA_MOSAIC')
    elif 'SGA_OVERERVING' in d:
        d['CNV_inheritance'] = d.pop('SGA_OVERERVING')
    elif 'SGA_REGIONS_UMCG_CNV_NL_COUNT' in d:
        d['UMCG_NL_CNV_count'] = d.pop('SGA_REGIONS_UMCG_CNV_NL_COUNT')
    else:
        d['testResult_id'] = d['clinical_identifier']
        d['type_test'] = 'other'

#change date format
for d in adlasportal:
    d['lab_result_date'] = datetime.strptime((d['lab_result_date']),"%d/%m/%Y").strftime("%Y-%m-%d")

#import all to geneticlines_testResult
gen_session.add_all('geneticlines_testResult', adlasportal)

# Get a list with all adalasportaldata for archive
adlasarchive = gen_session.get('adlasportal_patients', batch_size=1000, sort_column='UMCGNR')
for d in adlasarchive:
    d['processed'] = 'true' #todo: need to add escapes when not processed>add to adlasportal and then remove?
    d['processes_date'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
#import data to archive
gen_session.add_all('adlasarchive_patients', adlasarchive)

# delete all data that is processed from adlasportal
# processedids=[]
# for d in adlasportal:
#     processedids.append(d['id'])
#     if d['processed'] != True:
#         gen_session.delete_list('adlasportal_patients', processedids)

#todo:
# - when error give warning in log
# - when item can be procesed leave in adlasportal
# - update items met EPIC data
# - delete and update
