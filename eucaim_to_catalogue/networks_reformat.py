import pandas as pd
import general_reformat as reformat


def get_networks(path):
    networks = pd.read_csv(path + 'EUCAIM_networks.csv')

    # reformat columns
    networks['acronym'] = networks['Name']

    # rename columns
    networks.rename(columns={'Id': 'id',
                             'Name': 'name',
                             'Description': 'description',
                             'URL': 'website',
                             'Contact': 'contact email'}, inplace=True)

    networks = reformat.float_to_int(networks)
    networks = networks[['id', 'name', 'description', 'acronym', 'contact email', 'website']]

    return networks
