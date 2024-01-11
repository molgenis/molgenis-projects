import pandas as pd
import general_reformat as reformat


def get_biobanks(path, network_ids):
    biobanks = pd.read_csv(path + 'EUCAIM_biobanks.csv')

    # reformat columns
    biobanks['type'] = 'Biobank'
    # TODO: get type from 'collection method' in collections
    biobanks['regions'] = biobanks['country'].apply(reformat.reformat_regions)
    biobanks['country'] = biobanks['country'].apply(reformat.reformat_countries)
    biobanks['website'] = biobanks['url'].apply(reformat.get_hyperlink)
    biobanks['networks'] = biobanks['network'].apply(get_network_ids, network_ids=network_ids)
    biobanks['networks'] = biobanks['networks'].apply(add_network)

    # rename columns
    biobanks.rename(columns={'Id': 'id',
                             'Acronym': 'acronym',
                             'Name': 'name',
                             'Description': 'description',
                             'country': 'countries',
                             'contact': 'contact email'}, inplace=True)

    biobanks = reformat.float_to_int(biobanks)
    biobanks.to_csv('C:/Users/brend/projects/EOSC4cancer/bbmri/biobanks.csv')

    # select columns
    biobanks = biobanks[['id', 'name', 'acronym', 'type', 'contact email', 'countries', 'regions',
                         'description', 'website', 'networks']]

    return biobanks


def get_network_ids(name, network_ids):
    network_id = network_ids.get(name)

    return network_id


def add_network(network):
    networks = network + ',EOSC4Cancer'

    return networks
