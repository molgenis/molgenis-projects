import pandas as pd

excel_file = 'bbmri-eric.xls'

# load collections
collections = pd.read_excel(excel_file, sheet_name='eu_bbmri_eric_collections')
print(collections.columns)


# rename columns to new model
collections.rename(columns={"id": "Identifier", 
                            "name": "Name",
                            "acronym":"Acronym",
                            "url":"Website",
                            "type":"Type",
                            "biobank":"Organisation",
                            "description":"Aim",
                            "network":"Collaborations",
                            "contact":"Contacts",
                            "size":"NoParticipants",
                            "timestamp":"LastUpdated",
                            "also_known":"AlternativeIdentifiers"
                            #todo Investigators, startYear, followUp, EndYear,AccessConditions,MarkerPaper,QualityStandards,Logo
                             },inplace=True)

# remove the columns not yet mapped
collections.drop(columns=[
       #move to population?
       'country','age_low', 'age_high', 'age_unit','sex','diagnosis_available',
       #move to collection event?
       'data_categories',
       'body_part_examined', 'imaging_modality', 'image_dataset_type',
       'materials', 'storage_temperatures', 'image_access_uri',
       # todo: move to use conditions
       'collaboration_commercial', 'collaboration_non_for_profit','sample_access_fee',
       'sample_access_joint_project', 'sample_access_description',
       'sample_access_uri', 'data_access_fee', 'data_access_joint_project',
       'data_access_description', 'data_access_uri', 'image_access_fee',
       'image_joint_projects', 'image_access_description', 
       # todo: move to quality indicators
       'sample_processing_sop', 'sample_transport_sop', 'sample_storage_sop',
       'data_processing_sop', 'data_transport_sop', 'data_storage_sop',
       'quality','standards',
       # removed for other reasons or undecided
       'bioresource_reference',
        'order_of_magnitude', 
       'number_of_donors', 'order_of_magnitude_donors', 'parent_collection',
       'sub_collections', 'id_card', 'head_title_before_name',
       'head_firstname', 'head_lastname', 'head_title_after_name', 'head_role',
       'contact_priority', 'latitude', 'longitude',
        'biobank_label'],inplace=True)

print(collections.head(5))


# load organisations

organisations = pd.read_excel(excel_file, sheet_name='eu_bbmri_eric_biobanks')
print(organisations.columns)


# rename columns to new model

organisations.rename(columns={"id": "Identifier", 
                              "name": "Name",
                              "juridical_person":"LegalEntity",
                              "acronym":"Acronym",
                              "url":"Website",
                              "capabilities":"Capabilities",
                              "contact":"Contact",
                              "description":"Description",
                              "country":"Country",
                              "capabilities":"Capabilities",
                              "network":"Collaborations",
                              "also_known":"AlternativeIdentifiers"
                              "longitude":"Longitude",
                              "latitude":"Latitude"
                             },inplace=True)

#drop columns not yet mapped
#charter signed should probably registered in seperate table
#check if contact is okay
organisations.drop(columns=[
                            #move to capabilities
                            'it_support_available', 
                            'it_staff_size', 
                            'collaboration_commercial', 
                            'collaboration_non_for_profit',
                            'operational_standards',
                            'other_standards',
                            'is_available',
                            'his_available',
                            #supppose remove
                            'collections',
                            'head_firstname',
                            'partner_charter_signed',
                            'head_lastname',
                            'head_title_after_name',
                            'head_title_before_name',
                            'head_role',
                            'contact_priority',
                              'quality'
                             ],inplace=True)

print(organisations.head(5))




