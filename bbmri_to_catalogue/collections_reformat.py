import pandas as pd
import general_reformat as reformat


def get_collections(session, biobank_ids):
    data = session.get("eu_bbmri_eric_collections")
    collections = pd.DataFrame.from_dict(data)
    # print(collections.head(n=20))

    collections['country'] = collections['country'].apply(reformat.get_from_dict, key='name')
    collections['country'] = collections['country'].apply(reformat.reformat_countries)
    collections['contact'] = collections['contact'].apply(reformat.get_from_dict, key='email')

    # reference to BBMRI-ERIC or EOSC4Cancer and BBMRI-ERIC networks
    collections['cancerYN'] = ''
    collections['cancerYN'] = collections['categories'].apply(get_cancer_category)
    collections['networks'] = ''
    collections['networks'] = collections['cancerYN'].apply(get_network)
    collections['categories'] = collections['categories'].apply(reformat.get_from_list_of_dict, key='label')

    # reformat reference to biobank/cohort
    collections['biobank'] = collections['biobank'].apply(reformat.get_from_dict, key='id')
    collections['resource'] = collections['biobank'].apply(get_biobank_id, biobank_ids=biobank_ids)
    collections = collections.dropna(subset='resource')

    # reformat diseases
    # collections['diagnosis_available'] = collections['diagnosis_available'].apply(reformat.get_diagnoses)
    # collections['diagnosis_available'] = collections['diagnosis_available'].apply(reformat.reformat_diseases)

    # number duplicate names
    collections = number_duplicate_names(collections)

    # drop columns
    collections = collections.drop(columns=['sub_collections', 'name'])

    # rename columns
    collections.rename(columns={'num_name': 'name',
                                'country': 'countries',
                                'contact': 'contact email',
                                'size': 'number of participants',
                                # 'diagnosis_available': 'population disease',
                                'categories': 'keywords'}, inplace=True)

    # remove entries that are already in the catalogue
    collections = collections[collections.name != 'Northern Finland Birth Cohort 1986']

    collections = reformat.float_to_int(collections)
    # collections.to_csv('C:/Users/brend/projects/EOSC4cancer/bbmri/collections.csv')
    # select columns
    collections = collections[['resource', 'id', 'name', 'acronym', 'contact email', 'countries', 'keywords',
                               'networks', 'number of participants', 'cancerYN', 'description']]  # 'population disease'

    return collections


def get_biobank_id(old_id, biobank_ids):
    biobank_id = biobank_ids.get(old_id)

    return biobank_id


def get_cancer_category(categories_list):
    for d in categories_list:
        if d.get('label') == 'Cancer':
            return True

    return False


def get_network(cancer_yn):
    if cancer_yn:
        return 'EOSC4Cancer, BBMRI-ERIC'
    else:
        return 'BBMRI-ERIC'


def number_duplicate_names(df):
    df = df.sort_values('name')
    df = df.reset_index()
    df['num_name'] = ''

    previous_name = ''
    num = 1
    for i in range(0, len(df)):
        if df.name[i] == previous_name:
            num += 1
            df.loc[i, 'num_name'] = df.loc[i, 'name'] + "_" + str(num)
        else:
            df.loc[i, 'num_name'] = df.loc[i, 'name']
            num = 1
        previous_name = df.loc[i, 'name']

    return df
