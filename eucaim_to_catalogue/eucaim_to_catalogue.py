import argparse
import molgenis.client as client

from biobanks_reformat import get_biobanks
from collections_reformat import get_collections
from networks_reformat import get_networks

PATH = 'C:/Users/brend/projects/EOSC4cancer/eucaim/'


def main():
    networks = get_networks(PATH)
    network_ids = dict(zip(networks.name, networks.id))
    biobanks = get_biobanks(PATH, network_ids)
    biobank_ids = dict(zip(biobanks.name, biobanks.id))
    collections = get_collections(PATH, biobank_ids)

    # print csv's
    biobanks.to_csv("C:/Users/brend/projects/EOSC4cancer/eucaim/Cohorts.csv", index=None)
    collections.to_csv("C:/Users/brend/projects/EOSC4cancer/eucaim/Subcohorts.csv", index=None)
    networks.to_csv("C:/Users/brend/projects/EOSC4cancer/eucaim/Networks.csv", index=None)


if __name__ == "__main__":
    main()
