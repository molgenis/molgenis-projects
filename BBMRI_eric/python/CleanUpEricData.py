"""
 202010 Dieuwke Roelofs-Prins
 With this script:
 - Entries which are in BBMRI ERIC persons, networks, biobanks and
   collections which do not exist in het National Node data will be
   deleted.
"""

# Import module(s)
import molgenis.client as molgenis

# Define variable(s)
bb_qualities={}
check_list=['collections', 'biobanks', 'networks', 'persons']
debug=False
col_qualities={}
eric_session = molgenis.Session('https://molgenis104.gcc.rug.nl/api/', token='${molgenisToken}')
nn_ids=[]
nn_packages=[]

### Get a list with all eu_bbmri_eric packages
eric_packages=eric_session.get('sys_md_Package', attributes='id', batch_size=1000, sort_column='id', q='id=like="eu_bbmri_eric"')
if len(eric_packages) == 0:
    raise SystemExit('No ERIC packages found?!?')
else: print('Number ERIC packages is', len(eric_packages))

# Store the packages in a list
for package in eric_packages:
    if package['id'] != 'eu_bbmri_eric':
        nn_packages.append(package['id'])

print('Number of National Node packages is', len(nn_packages))

# Select the biobank and collection quality information
quality_data=eric_session.get('eu_bbmri_eric_bio_qual_info', attributes='id,biobank', batch_size=1000, sort_column='id')
if len(quality_data) == 0:
    raise SystemExit('No biobank quality data found?!?')
else: print('Number of BBMRI-ERIC biobank qualities is', len(quality_data))

for item in quality_data:
    bb_qualities[item['biobank']['id']]=item['id']

quality_data=eric_session.get('eu_bbmri_eric_col_qual_info', attributes='id,collection', batch_size=1000, sort_column='id')
if len(quality_data) == 0:
    raise SystemExit('No collection quality data found?!?')
else: print('Number of BBMRI-ERIC collection qualities is', len(quality_data))

for item in quality_data:
    col_qualities[item['collection']['id']]=item['id']

### Loop through the list with entities to be checked
for entity in check_list:
    print('\n')
    nn_ids=[]
    n_exist = 0
    ### Get National Node data of the entity
    for nn_package in nn_packages:
        nn_data=eric_session.get(nn_package+'_'+entity, attributes='id', batch_size=1000, sort_column='id')
        if len(nn_data) == 0:
            print('No data found for', nn_package+'_'+entity, '?!?')
            #raise SystemExit('No data found for '+nn_package+'_'+entity+'?!?')
        elif debug: print('Number of', nn_package+'_'+entity, 'is', len(nn_data))
        for item in nn_data:
            nn_ids.append(item['id'])
            
    print('Number of unique', entity,'of all NN''s is', len(set(nn_ids)))
                          
    ### Get ERIC data of the entity
    eric_data=eric_session.get('eu_bbmri_eric_'+entity, attributes='id', batch_size=1000, sort_column='id')
    if len(eric_data) == 0:
        raise SystemExit('No ERIC data found for '+entity+'?!?')
    else: print('Number of ERIC', entity, 'is', len(eric_data))

    ### Check if all ERIC ids are still in the NN ids list

    for item in eric_data:
        if item['id'] not in nn_ids:
            # Check if the id exists in biobank of collection qualities
            # Remove it also from there
            if item['id'] in bb_qualities.keys():
                print(item['id'], 'has a biobank quality')
                eric_session.delete('eu_bbmri_eric_bio_qual_info', id_=bb_qualities[item['id']])
            if item['id'] in col_qualities.keys():
                print(item['id'], 'has a collection quality')
                eric_session.delete('eu_bbmri_eric_col_qual_info', id_=col_qualities[item['id']])
            # Delete this entry from the ERIC entity
            print('Delete', item['id'], 'in', entity)
            eric_session.delete('eu_bbmri_eric_'+entity, id_=item['id'])
        else: n_exist+=1 #print(item['id'], 'still exists in', entity)
    print('Number of ERIC ids that exist in the National Nodes is', n_exist)

print('FINISHED')