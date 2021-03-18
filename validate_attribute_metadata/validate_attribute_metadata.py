import argparse
import molgenis.client as molgenis
import pandas as pd


#define command line arguments
parser=argparse.ArgumentParser(description="command line args")
parser.add_argument("-url", type=str, dest="server_url", required=True, help="Molgenis server url")
##parser.add_argument("-u", type=str, dest="username", required=False, help="Username for server access")
parser.add_argument("-pw", type=str, dest="password", required=True, help="Password for server access")
##parser.add_argument("-out", type=str, dest="output", required=True, help="Define output filename")

args=parser.parse_args()


#define entityTypes of main/registry area
main_area = {"biobanks": "eu_bbmri_eric_biobanks",
             "collections": "eu_bbmri_eric_collections",
             "networks": "eu_bbmri_eric_networks",
             "persons": "eu_bbmri_eric_persons"}

#define entityTypes of staging areas
staging_areas = {"biobanks": ["eu_bbmri_eric_AT_biobanks", "eu_bbmri_eric_BE_biobanks",
                     "eu_bbmri_eric_BG_biobanks", "eu_bbmri_eric_CH_biobanks",
                     "eu_bbmri_eric_CY_biobanks", "eu_bbmri_eric_CZ_biobanks",
                     "eu_bbmri_eric_DE_biobanks", "eu_bbmri_eric_EE_biobanks",
                     "eu_bbmri_eric_EU_biobanks", "eu_bbmri_eric_EXT_biobanks",
                     "eu_bbmri_eric_FI_biobanks", "eu_bbmri_eric_FR_biobanks",
                     "eu_bbmri_eric_GR_biobanks", "eu_bbmri_eric_IT_biobanks",
                     "eu_bbmri_eric_LT_biobanks", "eu_bbmri_eric_LV_biobanks",
                     "eu_bbmri_eric_MT_biobanks", "eu_bbmri_eric_NL_biobanks",
                     "eu_bbmri_eric_NO_biobanks", "eu_bbmri_eric_PL_biobanks",
                     "eu_bbmri_eric_SE_biobanks", "eu_bbmri_eric_UK_biobanks"],
                 "collections": ["eu_bbmri_eric_AT_collections", "eu_bbmri_eric_BE_collections",
                     "eu_bbmri_eric_BG_collections", "eu_bbmri_eric_CH_collections",
                     "eu_bbmri_eric_CY_collections", "eu_bbmri_eric_CZ_collections",
                     "eu_bbmri_eric_DE_collections", "eu_bbmri_eric_EE_collections",
                     "eu_bbmri_eric_EU_collections", "eu_bbmri_eric_EXT_collections",
                     "eu_bbmri_eric_FI_collections", "eu_bbmri_eric_FR_collections",
                     "eu_bbmri_eric_GR_collections", "eu_bbmri_eric_IT_collections",
                     "eu_bbmri_eric_LT_collections", "eu_bbmri_eric_LV_collections",
                     "eu_bbmri_eric_MT_collections", "eu_bbmri_eric_NL_collections",
                     "eu_bbmri_eric_NO_collections", "eu_bbmri_eric_PL_collections",
                     "eu_bbmri_eric_SE_collections", "eu_bbmri_eric_UK_collections"],
                 "networks": ["eu_bbmri_eric_AT_networks", "eu_bbmri_eric_BE_networks",
                     "eu_bbmri_eric_BG_networks", "eu_bbmri_eric_CH_networks",
                     "eu_bbmri_eric_CY_networks", "eu_bbmri_eric_CZ_networks",
                     "eu_bbmri_eric_DE_networks", "eu_bbmri_eric_EE_networks",
                     "eu_bbmri_eric_EU_networks", "eu_bbmri_eric_EXT_networks",
                     "eu_bbmri_eric_FI_networks", "eu_bbmri_eric_FR_networks",
                     "eu_bbmri_eric_GR_networks", "eu_bbmri_eric_IT_networks",
                     "eu_bbmri_eric_LT_networks", "eu_bbmri_eric_LV_networks",
                     "eu_bbmri_eric_MT_networks", "eu_bbmri_eric_NL_networks",
                     "eu_bbmri_eric_NO_networks", "eu_bbmri_eric_PL_networks",
                     "eu_bbmri_eric_SE_networks", "eu_bbmri_eric_UK_networks"],
                 "persons": ["eu_bbmri_eric_AT_persons", "eu_bbmri_eric_BE_persons",
                     "eu_bbmri_eric_BG_persons", "eu_bbmri_eric_CH_persons",
                     "eu_bbmri_eric_CY_persons", "eu_bbmri_eric_CZ_persons",
                     "eu_bbmri_eric_DE_persons", "eu_bbmri_eric_EE_persons",
                     "eu_bbmri_eric_EU_persons", "eu_bbmri_eric_EXT_persons",
                     "eu_bbmri_eric_FI_persons", "eu_bbmri_eric_FR_persons",
                     "eu_bbmri_eric_GR_persons", "eu_bbmri_eric_IT_persons",
                     "eu_bbmri_eric_LT_persons", "eu_bbmri_eric_LV_persons",
                     "eu_bbmri_eric_MT_persons", "eu_bbmri_eric_NL_persons",
                     "eu_bbmri_eric_NO_persons", "eu_bbmri_eric_PL_persons",
                     "eu_bbmri_eric_SE_persons", "eu_bbmri_eric_UK_persons"]}

#define attribute metadata to compare, "name" is always compared
comparison_list = ["label", "fieldType"]

#all items that can be compared:
##["href", "fieldType", "name", "label", "description", \
##"attributes", "enumOptions", "maxLength", "auto", \
##"nillable", "readOnly", "labelAttribute", "unique", \
##"visible", "lookupAttribute", "isAggregatable"]


def main():
    session = connect_to_server(args.server_url, args.password)

    #iterate over entityTypes of main_area
    for key in main_area:
        main_entity_type = main_area[key]
        file_name = main_entity_type + ".txt"
        file = open(file_name, "w")
        file.close()
        main_entity = Entity(session, main_entity_type, comparison_list)

        #store attribute metadata in df
        main_attributes = main_entity.get_attributes()

        for staging_entity_type in staging_areas[key]:
            staging_entity = Entity(session, staging_entity_type, \
                                    comparison_list)
            
            staging_attributes = staging_entity.get_attributes()

            compare_metadata(main_attributes, staging_attributes, file_name, \
                             staging_entity_type, comparison_list)


class Entity:

    def __init__(self, session, entity_type, comparison_list):
        """
        Creates object Entity that extracts common metadata specified in comparison_list for attributes \
        of the specified entityTypes in main_area and staging_areas.
        :param self.session: class molgenis.client.Session provides access to specified server
        :param self.entity_type: string refering to one of the entityTypes specified in main_area or staging_areas
        :param self.comparison_list: list of attribute metadata to compare
        """
        self.session = session
        self.entity_type = entity_type
        self.comparison_list = comparison_list

    def get_attributes(self):
        """
        Gets attributes in pd.DataFrame.
        """

        self.metadata = self.session.get_entity_meta_data(self.entity_type)
        attributes = self.metadata.get("attributes")

        #store in pandas.DataFrame
        df = pd.DataFrame.from_dict(attributes, orient="index")
        #select metadata items to compare
        df = df[self.comparison_list]  
                
        return df


def connect_to_server(server_url, pw, username="admin"):
    session = molgenis.Session(server_url + "api/")
    session.login(username, pw)

    return session


def compare_metadata(df1, df2, file_name, entity_type, comparison_list):
    #find names missing in staging entityTypes
    missing_names = [idx for idx in df1.index if idx not in df2.index]

    #find names that are not in main entityType
    wrong_names = [idx for idx in df2.index if idx not in df1.index]
    
    #find differences in metadata attributes
    other_metadata = ""   
    for item in comparison_list:
        for idx, value in df1[item].iteritems():
            if idx in df2.index and not value == df2[item][idx]:
                    other_metadata += "Attribute with name: '{}' has a different " \
                                              "'{}': '{}' vs. '{}'".format(idx, item, value, \
                                                                           df2[item][idx])
                    
    write_to_file(file_name, entity_type, missing_names, wrong_names, other_metadata)
    

def write_to_file(file_name, entity_type, missing_names, wrong_names, other_metadata):
    file = open(file_name, "a")
    file.write("entityType: '{}'\n\n".format(entity_type))

    if missing_names:
        missing_names_str = "Missing attribute name(s): \n\t" + "\n\t".join(missing_names)
        file.write(missing_names_str)
        file.write("\n\n")

    if wrong_names:
        wrong_names_str = "Wrong attribute name(s): \n\t" + "\n\t".join(wrong_names)
        file.write(wrong_names_str)
        file.write("\n\n")
    
    if not other_metadata == "":
        file.write(other_metadata)
        file.write("\n\n")
    
    file.close()


if __name__ == "__main__":
    main()
