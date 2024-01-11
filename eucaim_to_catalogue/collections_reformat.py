import pandas as pd
import general_reformat as reformat


def get_collections(path, biobank_ids):
    collections = pd.read_csv(path + 'EUCAIM_collections.csv')

    # reformat columns
    collections['resource'] = collections['Biobank_col'].apply(get_biobank_ids, biobank_ids=biobank_ids)
    collections['regions'] = collections['Country'].apply(reformat.reformat_regions)
    collections['countries'] = collections['Country'].apply(reformat.reformat_countries)

    # rename columns
    collections.rename(columns={'Collection name': 'name',
                                'contact': 'contact email',
                                'size': 'number of participants',
                                'categories': 'keywords'}, inplace=True)

    collections = reformat.float_to_int(collections)

    # select columns
    collections = collections[['resource', 'name', 'contact email', 'countries',
                               'networks', 'number of participants', 'description']]  # 'population disease'

    return collections


def get_biobank_ids(name, biobank_ids):
    biobank_id = biobank_ids.get(name)

    return biobank_id
