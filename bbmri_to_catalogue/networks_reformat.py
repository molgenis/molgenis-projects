import pandas as pd
import general_reformat as reformat


def get_networks(session):
    data = session.get("eu_bbmri_eric_networks")
    networks = pd.DataFrame.from_dict(data)

    # reformat columns
    networks['country'] = networks['country'].apply(reformat.get_from_dict, key='name')
    networks['country'] = networks['country'].apply(reformat.reformat_countries)
    networks['contact'] = networks['contact'].apply(reformat.get_from_dict, key='email')
    # TODO: reformat id
    # TODO: get old_id to external identifier

    # old_id to external identifier
    external_identifiers = pd.DataFrame(columns=['resource', 'identifier', 'external identifier type other'])
    external_identifiers.resource = networks.id
    external_identifiers.identifier = networks.old_id
    external_identifiers['external identifier type other'] = 'BBMRI id'
    external_identifiers.to_csv('C:/Users/brend/projects/EOSC4cancer/bbmri/External identifiers.csv', index=None)

    # rename columns
    networks.rename(columns={'country': 'countries',
                             'contact': 'contact email'}, inplace=True)

    networks = reformat.float_to_int(networks)
    networks = networks[['id', 'old_id', 'description', 'country', 'contact']]

    return networks
