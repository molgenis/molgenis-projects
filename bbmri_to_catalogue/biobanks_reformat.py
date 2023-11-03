import pandas as pd
import general_reformat as reformat


def get_biobank_networks(biobanks, collections_networks):
    biobanks['networks'] = biobanks['id'].apply(get_network, collection_networks=collections_networks)

    return biobanks


def get_network(biobank_id, collection_networks):
    # select all collections belonging to a biobank
    biobanks_networks = collection_networks.loc[collection_networks['resource'] == biobank_id]

    # select collections that are associated with EOSC4Cancer network
    cancer_networks = biobanks_networks[biobanks_networks["networks"].map(lambda networks: "EOSC4Cancer" in networks)]
    if len(cancer_networks) != 0:
        return 'EOSC4Cancer,BBMRI-ERIC'

    return 'BBMRI-ERIC'


def get_biobanks(session):
    data = session.get("eu_bbmri_eric_biobanks")
    biobanks = pd.DataFrame.from_dict(data)

    # id to place holder 'old_id', acronym to id
    biobanks['old_id'] = biobanks.id
    biobanks.id = biobanks.acronym
    # fill empty id's and id == '-' with biobank name
    biobanks.id = biobanks.acronym.fillna(biobanks.name)
    biobanks.loc[biobanks['id'].eq('-'), 'id'] = biobanks.loc[biobanks['id'].eq('-'), 'name']

    # change specific duplicate id's, or drop duplicates:
    biobanks.loc[54, 'id'] = biobanks.loc[54, 'name']
    biobanks.loc[286, 'id'] = 'Biobanca Bruno Boerci'
    biobanks.loc[122, 'id'] = 'CC BBMRI-ERIC'
    biobanks = biobanks.drop(index=[326, 585, 636])

    # old_id to external identifier
    external_identifiers = pd.DataFrame(columns=['resource', 'identifier', 'external identifier type other'])
    external_identifiers.resource = biobanks.id
    external_identifiers.identifier = biobanks.old_id
    external_identifiers['external identifier type other'] = 'BBMRI id'
    external_identifiers.to_csv("C:/Users/brend/projects/EOSC4cancer/bbmri/External identifiers.csv", index=None)

    biobanks['networks'] = 'EOSC4Cancer, BBMRI-ERIC'
    # TODO: get network into Networks table, get cancer networks from subcohorts
    biobanks['type'] = 'Biobank'

    # reformat columns
    biobanks['country'] = biobanks['country'].apply(reformat.get_from_dict, key='name')
    biobanks['country'] = biobanks['country'].apply(reformat.reformat_countries)
    biobanks['contact'] = biobanks['contact'].apply(reformat.get_from_dict, key='email')
    biobanks['url'] = biobanks['url'].apply(reformat.get_hyperlink)

    # rename columns
    biobanks.rename(columns={'url': 'website',
                             'country': 'countries',
                             'contact': 'contact email'}, inplace=True)
    # TODO: get diseases from subcohorts, get keywords from subcohorts

    biobanks = reformat.float_to_int(biobanks)
    biobanks.to_csv('C:/Users/brend/projects/EOSC4cancer/bbmri/biobanks.csv')

    # select columns
    biobanks = biobanks[['id', 'pid', 'name', 'acronym', 'type', 'contact email', 'countries',
                         'description', 'website', 'networks', 'old_id']]

    return biobanks
