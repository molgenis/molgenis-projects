import argparse
import molgenis.client as client

from biobanks_reformat import get_biobanks, get_biobank_networks
from collections_reformat import get_collections

# define command line arguments
parser = argparse.ArgumentParser(description="command line args")
parser.add_argument("-pw", type=str, dest="password", required=True, help="Password for server access")

args = parser.parse_args()


def main():
    session = connect_to_server("https://directory.bbmri-eric.eu", args.password)
    biobanks = get_biobanks(session)
    biobank_ids = dict(zip(biobanks.old_id, biobanks.id))

    collections = get_collections(session, biobank_ids)
    collections_networks = collections[['resource', 'networks']]
    biobanks = get_biobank_networks(biobanks, collections_networks)

    # print csv's
    biobanks.to_csv("C:/Users/brend/projects/EOSC4cancer/bbmri/Cohorts.csv", index=None)
    collections.to_csv("C:/Users/brend/projects/EOSC4cancer/bbmri/Subcohorts.csv", index=None)


def connect_to_server(server_url, pw, username="admin"):
    session = client.Session(server_url + "api/")
    session.login(username, pw)

    return session


if __name__ == "__main__":
    main()
