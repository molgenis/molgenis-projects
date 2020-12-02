import csv
import json
from typing import List

f_name = 'rdconnectfinder.json'
output_f = 'registries.csv'

#Read JSON file
def read_json(filename: str) -> dict:
    with open(filename) as f:
        return json.load(f)['allData']

#Write dictionary with registry info to csv
def write_csv(rows: List[dict], output_filename: str = 'output.csv'):
    with open(output_filename, 'w') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys(), quotechar='"', quoting=csv.QUOTE_ALL)
        w.writeheader()
        for row in rows:
            w.writerow(row)

#Parse JSON file and write extracted registry data to dictionary
def map_orgs(orgs_json: dict) -> List[dict]:
    orgs = list()
    for org in orgs_json:
        mapped_org = dict()

        # General info
        mapped_org['organizationId'] = org['OrganizationID']
        mapped_org['name'] = org['name']
        mapped_org['acronym'] = org['core']['acronym']
        mapped_org['Description'] = org['core']['Description']
        # TODO url
        mapped_org['type'] = org['type']
        mapped_org['nameOfHostInstitution'] = org['address']['name of host institution']
        mapped_org['Type_of_host_institution'] = org['core']['Type_of_host_institution']
        mapped_org['Host_institution_is_a'] = org['core']['Host_institution_is_a']
        mapped_org['year_of_establishment'] = org['core']['year_of_establishment']
        mapped_org['countryCode'] = org['core']['countryCode']
        mapped_org['Source_of_funding'] = org['core']['Source_of_funding']
        mapped_org['date_of_inclusion'] = org['date of inclusion']
        mapped_org['last_activities'] = org['last activities']

        #core
        mapped_org['Associated_data_available'] = org['core']['Associated_data_available']
        mapped_org['Additional_Associated_data_available'] = org['core']['Additional_Associated_data_available']
        mapped_org['Ontologies'] = org['core']['Ontologies']
        mapped_org['Additional_Ontologies'] = org['core']['Additional_Ontologies']
        mapped_org['Imaging_available'] = org['core']['Imaging_available']
        mapped_org['Additional_Imaging_available'] = org['core']['Additional_Imaging_available']
        mapped_org['The_registry_biobanks_is_listed_in_other_inventories_networks'] = org['core']['The_registry_biobanks_is_listed_in_other_inventories_networks']
        mapped_org['Additional_networks_inventories'] = org['core']['Additional_networks_inventories']
        mapped_org['Text5085'] = org['core']['Text5085']

        # Address
        mapped_org['street_1'] = org['address']['street1']
        mapped_org['street_2'] = org['address']['street2']
        mapped_org['zip'] = org['address']['zip']
        mapped_org['city'] = org['address']['city']
        mapped_org['country'] = org['address']['country']

        # Registry quality
        mapped_org['If_yes__specify'] = org['reg_quality']['If_yes__specify']
        # _reg added to attribute name because bb has same info
        mapped_org['Accreditation_certification_program_reg'] = org['reg_quality']['Accreditation_certification_program']
        mapped_org['Training_program_for_the_registering_activities'] = org['reg_quality']['Training_program_for_the_registering_activities']
        mapped_org['Quality_control_external_audits'] = org['reg_quality']['Quality_control_external_audits']
        mapped_org['If_yes__frequency_of_audits'] = org['reg_quality']['If_yes__frequency_of_audits']
        mapped_org['Standardized_Operating_Procedures__SOPs__available_for_data_management'] = org['reg_quality']['Standardized_Operating_Procedures__SOPs__available_for_data_management']
        # _reg added to attribute name because bb has same info
        mapped_org['Standardized_Operating_Procedures__SOPs_available_for_data_management_reg'] = org['reg_quality']['Standardized_Operating_Procedures__SOPs__available_for_data_management']
        # _reg added to attribute name because bb has same info
        mapped_org['If_yes__specify__ISO_standards_reg'] = org['reg_quality']['If_yes__specify__ISO_standards___']
        mapped_org['Standardized_case_inclusion_and_exclusion_criteria'] = org['reg_quality']['Standardized_case-inclusion_and-exclusion_criteria']

        # bb_quality
        # Check if org has bb_quality; not all orgs have this information:
        if 'bb_quality' in org.keys():
            #_bb added to attribute name because reg has same info
            mapped_org['Accreditation_certification_program_bb'] = org['bb_quality']['Accreditation_certification_program']
            mapped_org['Catalogue_of_collections'] = org['bb_quality']['Catalogue_of_collections']
            mapped_org['Is_the_collection_database_exportable'] = org['bb_quality']['Is_the_collection_database_exportable']
            mapped_org['Training_program_for_the_registering_activities'] = org['bb_quality']['Training_program_for_the_registering_activities']
            mapped_org['If_yes_frequency_of_audits'] = org['bb_quality']['If_yes__frequency_of_audits']
            mapped_org['Standardized_case_inclusion_and_exclusion_criteria'] = org['bb_quality']['Standardized_case-inclusion_and-exclusion_criteria']
            mapped_org['Does_sample_management_system_contain_a_data_identification_system'] = org['bb_quality']['Does_sample_management_system_contain_a_data_identification_system']
            mapped_org['Number_of_IT_Staff'] = org['bb_quality']['Number_of_IT_Staff']
            mapped_org['If_yes_online_available_please_specify_URL'] = org['bb_quality']['If_yes__online_available_please_specify_URL_']
            mapped_org['Maintain_of_an_updated_database'] = org['bb_quality']['Maintain_of_an_updated_database']
            mapped_org['Quality_control_external_audits'] = org['bb_quality']['Quality_control_external_audits']
            mapped_org['Software'] = org['bb_quality']['Software']
            # _bb added to attribute name because reg has same info
            mapped_org['Standardized_Operating_Procedures_SOPs_available_for_data_management_bb'] = org['bb_quality']['Standardized_Operating_Procedures__SOPs__available_for_data_management']
            mapped_org['Level_of_Sample_Description_Catalogue'] = org['bb_quality']['Level_of_Sample_Description__Catalogue_']
            # _bb added to attribute name because reg has same info
            mapped_org['If_yes_specify_ISO_standards_bb'] = org['bb_quality']['If_yes__specify__ISO_standards___']
            mapped_org['Molecular_test_performed_to_ensure_sample_integrity'] = org['bb_quality']['Molecular_test_performed_to_ensure_sample_integrity']
        else:
            mapped_org['Accreditation_certification_program_bb'] = ''
            mapped_org['Catalogue_of_collections'] = ''
            mapped_org['Is_the_collection_database_exportable'] = ''
            mapped_org['Training_program_for_the_registering_activities'] = ''
            mapped_org['If_yes_frequency_of_audits'] = ''
            mapped_org['Standardized_case_inclusion_and_exclusion_criteria'] = ''
            mapped_org['Does_sample_management_system_contain_a_data_identification_system'] = ''
            mapped_org['Number_of_IT_Staff'] = ''
            mapped_org['If_yes_online_available_please_specify_URL'] = ''
            mapped_org['Maintain_of_an_updated_database'] = ''
            mapped_org['Quality_control_external_audits'] = ''
            mapped_org['Software'] = ''
            # _bb added to attribute name because reg has same info
            mapped_org['Standardized_Operating_Procedures_SOPs_available_for_data_management_bb'] = ''
            mapped_org['Level_of_Sample_Description_Catalogue'] = ''
            # _bb added to attribute name because reg has same info
            mapped_org['If_yes_specify_ISO_standards_bb'] = ''
            mapped_org['Molecular_test_performed_to_ensure_sample_integrity'] = ''



        # Registry accessibility
        mapped_org['Other1'] = org['reg_accessibility']['Other1']
        mapped_org['Available_Data'] = org['reg_accessibility']['Available_Data']
        mapped_org['Has_the_registry_a_Data_Access_Committee'] = org['reg_accessibility']['Has_the_registry_a_Data_Access_Committee_']
        mapped_org['If_yes__please_provide_the_Data_Access_Committee_webpage'] = org['reg_accessibility']['If_yes__please_provide_the_Data_Access_Committee_webpage']
        mapped_org['Select9246'] = org['reg_accessibility']['Select9246']
        mapped_org['Personal_Data_Collected'] = org['reg_accessibility']['Personal_Data_Collected']
        mapped_org['Data_Access_Agreement'] = org['reg_accessibility']['Data_Access_Agreement']
        mapped_org['Is_an_ethics_board_decision_already_available_for_the_use_of_the_samples_in_research'] = org['reg_accessibility']['Is_an_ethics_board_decision_already_available_for_the_use_of_the_samples_in_research']
        mapped_org['Do_you_use_a_Data_Access_Agreement'] = org['reg_accessibility']['Do_you_use_a_Data_Access_Agreement_']
        mapped_org['Type_of_consent_is_obtained_from_the_patients'] = org['reg_accessibility']['Type_of_consent_is_obtained_from_the_patients']
        mapped_org['Specific_procedure_for_access_to_raw_data'] = org['reg_accessibility']['Specific_procedure_for_access_to_raw_data']
        mapped_org['Other4838'] = org['reg_accessibility']['Other4838']

        # TODO contacts
        # Main contact
        # This part give error but not sure why
        # mapped_org['last_name'] = org['main contact']['last name']
        # mapped_org['first_name'] = org['main contact']['first name']
        # mapped_org['email'] = org['main contact']['email']

        # TODO bb_core (?)
        # TODO bb_accessibility
        # TODO publications
        # TODO bb_contribution
        # TODO Scientific publications
        # TODO: Diseases
        # TODO Disease Areas (ICD20) (?)

        orgs.append(mapped_org)

    print(orgs)
    return orgs


organisations = read_json(f_name)
mapped_orgs = map_orgs(organisations)
write_csv(mapped_orgs, output_f)
