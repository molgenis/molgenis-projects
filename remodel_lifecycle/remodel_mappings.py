import argparse
import molgenis.client as molgenis
import pandas as pd
import os
import shutil


#define command line arguments
parser=argparse.ArgumentParser(description="command line args")
##parser.add_argument("-url", type=str, dest="server_url", required=True, help="Molgenis server url")
parser.add_argument("-pw", type=str, dest="password", required=True, help="Password for server access")

args=parser.parse_args()

server_url = "https://lifecycle.molgeniscloud.org/"

#define path to cohort Harmonization entityTypes
cohorts = {"ABCD": "LifeCycle_ABCD_Harmonizations",
           "ALSPAC": "LifeCycle_ALSPAC_Harmonizations",
           "BIB": "LifeCycle_BIB_Harmonizations",
           "CHOP": "LifeCycle_CHOP_Harmonizations",
           "DNBC": "LifeCycle_DNBC_Harmonizations",
           "EDEN": "LifeCycle_EDEN_Harmonizations",
           "ELFE": "LifeCycle_ELFE_Harmonizations",
           "GECKO": "LifeCycle_GECKO_Harmonizations",
           "GenR": "LifeCycle_GenR_Harmonizations",
           "HBCS": "LifeCycle_HBCS_Harmonizations",
           "INMA": "LifeCycle_INMA_Harmonizations",
##           "KANC": "LifeCycle_KANC_Harmonizations",#no data
           "MoBa": "LifeCycle_MoBa_Harmonizations",
           "NFBC66": "LifeCycle_NFBC66_Harmonizations",
           "NFBC86": "LifeCycle_NFBC86_Harmonizations",
           "NINFEA": "LifeCycle_NINFEA_Harmonizations",
##           "RAINE": "LifeCycle_RAINE_Harmonizations",#corrupt data
           "RHEA": "LifeCycle_RHEA_Harmonizations",
           "SWS": "LifeCycle_SWS_Harmonizations"}


def main():
    session = connect_to_server(server_url, args.password)

    #read mappings emx2 catalogue model
    remodeled_mappings = pd.read_csv("./target/VariableMappings.csv", nrows=0)
    #write model to csv (later append data per cohort)
    remodeled_mappings.to_csv("./output/VariableMappings.csv", index=False)

    #iterate over cohorts 
    for key in cohorts:
        mappings = session.get(cohorts[key])
        mappings = pd.DataFrame.from_dict(mappings)

        remodeled_mappings = remodel_mappings(mappings, key)
   
##    #get mappings from 'mapped' Harmonizations table on LifeCycle server per cohort
##    for i in range(0, 60000, 5000):
##        mappings = session.get("LifeCycle_Harmonizations", start=i, num=5000)
##        mappings = pd.DataFrame.from_dict(mappings)
##
##        #remodel mappings
##        remodeled_mappings = remodel_mappings(mappings) 

        #write (append) to file
        remodeled_mappings.to_csv("./output/VariableMappings.csv", mode="a", index=False, header=False)

    #if output.zip already exists in ./output, delete it
    if os.path.exists('./output/output.zip'):
        os.remove('./output/output.zip')
    #zip output
    shutil.make_archive('output', 'zip', './output/')    
    #move output.zip to folder ouptut
    shutil.move('output.zip', './output')
    
    session.logout()


def connect_to_server(server_url, pw, username="admin"):
    session = molgenis.Session(server_url + "api/")
    session.login(username, pw)

    return session


def remodel_mappings(mappings, key):
##    #drop rows where source variables column is empty
##    mappings = mappings[mappings['sources'].astype(bool)]
    
    remodeled_mappings = pd.read_csv("./target/VariableMappings.csv", nrows=0)

    remodeled_mappings['fromVariable'] = mappings['sources'].apply(get_source_names)
    remodeled_mappings['fromTable'] = "core" #for now table "core"
    remodeled_mappings['fromRelease.resource'] = key
    remodeled_mappings['fromRelease.version'] = "1.0.0"
    
    remodeled_mappings['toRelease.resource'] = "LifeCycle"
    remodeled_mappings['toRelease.version'] = "1.0.0"
    remodeled_mappings['toTable'] = "core"
    remodeled_mappings['toVariable'] = mappings['target'].apply(get_target_name)

    remodeled_mappings['match'] = mappings['status'].apply(get_id)
    remodeled_mappings['description'] = mappings['description']
    remodeled_mappings['syntax'] = mappings['syntax']
##    remodeled_mappings['comments'] = mappings['info'] #empty in table Harmonizations
    
    return remodeled_mappings


def get_target_name(x):
    """ (dict) -> str
    Retrieves value for key "variable" from dictionary x.
    """
    value = x['variable']

    return value


def get_source_names(x):
    """ (list of dict) -> str
    Retrieves all values for key "id" in list of dictionaries x and returns tehm in a
    string, separated by commas.
    """
    values = ""
    for item in x:
        values = values + item['variable'] + ","

    return values[:-1]


def get_id(x):
    """ (dict) -> str
    Retrieves value for key "id" from dictionary x.
    """
    value = x['id']

    return value


if __name__ == "__main__":
    main()
