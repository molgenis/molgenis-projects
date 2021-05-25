import argparse
import molgenis.client as molgenis
import pandas as pd
import os
import shutil
import re

# define command line arguments
parser = argparse.ArgumentParser(description="command line args")
parser.add_argument("-pw", type=str, dest="password", required=True, help="Password for server access")

args = parser.parse_args()

server_url = "https://lifecycle.molgeniscloud.org/"

# define path to cohort source variable entityTypes
cohorts = {"ABCD": "LifeCycle_ABCD_SourceVariables",
           "ALSPAC": "LifeCycle_ALSPAC_SourceVariables",
           "BIB": "LifeCycle_BIB_SourceVariables",
           "CHOP": "LifeCycle_CHOP_SourceVariables",
           "DNBC": "LifeCycle_DNBC_SourceVariables",
           "EDEN": "LifeCycle_EDEN_SourceVariables",
           "ELFE": "LifeCycle_ELFE_SourceVariables",
           "GECKO": "LifeCycle_GECKO_SourceVariables",
           "GenR": "LifeCycle_GenR_SourceVariables",
           "HBCS": "LifeCycle_HBCS_SourceVariables",
           "INMA": "LifeCycle_INMA_SourceVariables",
           ##           "KANC": "LifeCycle_KANC_SourceVariables", #no data
           "MoBa": "LifeCycle_MoBa_SourceVariables",
           "NFBC66": "LifeCycle_NFBC66_SourceVariables",
           "NFBC86": "LifeCycle_NFBC86_SourceVariables",
           "NINFEA": "LifeCycle_NINFEA_SourceVariables",
           ##           "RAINE": "LifeCycle_RAINE_SourceVariables",#source vars not entered appropriately
           "RHEA": "LifeCycle_RHEA_SourceVariables",
           "SWS": "LifeCycle_SWS_SourceVariables"}


def main():
    session = connect_to_server(server_url, args.password)

    # iterate over cohorts
    for key in cohorts:
        source_variables = session.get(cohorts[key])
        source_variables = pd.DataFrame.from_dict(source_variables)

        remodeled_source_vars = remodel_variables(source_variables, key)

        # write to file
        remodeled_source_vars.to_csv("./output/Variables.csv", mode="a", index=False, header=False)

    # Get ALSPAC data
    source_alspac = session.get(cohorts['ALSPAC'])
    alspac_data = pd.DataFrame.from_dict(source_alspac)
    remodeled_vals_alspac = remodel_values_alspac(alspac_data, 'ALSPAC')
    # Write to file
    remodeled_vals_alspac.to_csv("./output/Values.csv", mode="a", index=False, header=True)

    # Get NINFEA data
    # source_ninfea = session.get(cohorts['NINFEA'])
    # ninfea_data = pd.DataFrame.from_dict(source_ninfea)
    # remodeled_vals_ninfea = remodel_values_ninfea(ninfea_data, 'NINFEA')
    # Write to file
    # remodeled_vals_ninfea.to_csv("./output/Values.csv", mode="a", index=False, header=False)

    # if output.zip already exists in ./output, delete it
    if os.path.exists('./output/output.zip'):
        os.remove('./output/output.zip')
    # zip output
    shutil.make_archive('output', 'zip', './output/')
    # move output.zip to folder ouptut
    shutil.move('output.zip', './output')

    session.logout()


def connect_to_server(server_url, pw, username="admin"):
    session = molgenis.Session(server_url + "api/")
    session.login(username, pw)

    return session


def remodel_variables(source_variables, key):
    remodeled_variables = pd.read_csv('./target/Variables.csv', nrows=0)
    remodeled_variables['name'] = source_variables['variable']
    remodeled_variables['label'] = source_variables['label']
    remodeled_variables['format'] = source_variables['datatype'].apply(get_id)
    remodeled_variables['release.resource'] = key
    remodeled_variables['release.version'] = "1.0.0"
    ##    remodeled_variables['unit'] = source_variables['unit'] #some cohorts do not contain unit as column
    remodeled_variables['table'] = "core"
    remodeled_variables['description'] = source_variables['description']
    return remodeled_variables


def remodel_values_alspac(alspac_data, cohort):
    alspac_data['splitted_values'] = alspac_data['values'].str.split(';')
    
    remodeled_values_alspac = alspac_data.explode('splitted_values')
    
    remodeled_values_alspac['variable.name'] = alspac_data['variable']
    remodeled_values_alspac['release.resource'] = cohort
    remodeled_values_alspac['release.version'] = "1.0.0"
    remodeled_values_alspac['variable.table'] = "core"
    remodeled_values_alspac[['value', 'label']] = remodeled_values_alspac['splitted_values'].str.extract(r"(\d+)\s*[=.]\s*\"?([^\"]*)\"?")

    remodeled_values_alspac.drop(['_href', 'variable', 'datatype', 'values', 'unit', 'collectionType', 'description', 'dateOfUpdate', 'splitted_values',], axis='columns', inplace=True)
    
    return remodeled_values_alspac


# def remodel_values_ninfea(ninfea_data, cohort):
#     ninfea_data['splitted_values'] = ninfea_data['values'].str.split(';')
#     #
#     remodeled_values_ninfea = ninfea_data.explode('splitted_values')
#     #
#     remodeled_values_ninfea['variable.name'] = ninfea_data['variable']
#     remodeled_values_ninfea['release.resource'] = cohort
#     remodeled_values_ninfea['release.version'] = "1.0.0"
#     remodeled_values_ninfea['variable.table'] = "core"
#     remodeled_values_ninfea[['value', 'label']] = remodeled_values_ninfea['splitted_values'].str.extract(
#         r"(\d+)\s*[=.]\s*\"?([^\"]*)\"?")
#
#     remodeled_values_ninfea.drop(
#         ['_href', 'variable', 'datatype', 'values', 'unit', 'collectionType', 'description', 'dateOfUpdate',
#          'splitted_values', ], axis='columns', inplace=True)




def get_id(x):
    """ (dict) -> str
    Retrieves value for key "id" from dictionary x.
    """
    value = x['id']

    return value


if __name__ == "__main__":
    main()
