import sys, os, zipfile

sys.path.append('../molgenis')
from Bbmri_eric_country_model_maker import BbmriEricCountryModelMaker
from molgenis.molgenisConnector import MolgenisConnector


class BbmriEricModelUploader():
    def __init__(self, config):
        self.cwd = os.getcwd()
        self.countries = config['countries'].split(',')
        self.session = MolgenisConnector(config['target_server'], config['target_account'],
                                         config['target_password']).session
        if "FALSE" not in self.countries:
            model_maker = BbmriEricCountryModelMaker(self.countries, self.cwd)
            os.chdir('data_model/countries')
            model_maker.create_country_directories()
            model_maker.create_meta_data_for_countries()

    def upload_all_countries(self):
        for country in self.countries:
            self.upload_country(country)

    def upload_country(self, country):
        response = self.session.upload_zip('{}/{}.zip'.format(country, country))
        self.check_import_run(response, country)

    def check_import_run(self, response, name):
        response = response.split('/')
        runEntityType = response[-2]
        runId = response[-1]
        statusInfo = self.session.getById(runEntityType, runId)
        count = 1
        print("\r{} uploading{}".format(name, count * "."), end='')
        while statusInfo['status'] == 'RUNNING':
            count += 1
            print("\r{} uploading{}".format(name, count * "."), end='')
            statusInfo = self.session.getById(runEntityType, runId)
            if statusInfo["status"] == "FINISHED":
                print("{} uploaded".format(name))
                return "FINISHED"
            if statusInfo["status"] == "FAILED":
                print(statusInfo)
                print("Failed: ", statusInfo['message'])
                return "FAILED"

    def upload_all(self):
        zipFileName = self.cwd + '/data_model/meta_data.zip'
        meta_data = zipfile.ZipFile(zipFileName, 'w')
        packages = self.cwd + '/data_model/packages.csv'
        attributes = self.cwd + '/data_model/attributes.csv'
        entities = self.cwd + '/data_model/entities.csv'
        meta_data.write(self.cwd + '/data_model/eu_bbmri_eric_age_units.csv')
        meta_data.write(self.cwd + '/data_model/eu_bbmri_eric_biobank_size.csv')
        meta_data.write(self.cwd + '/data_model/eu_bbmri_eric_body_parts.csv')
        meta_data.write(self.cwd + '/data_model/eu_bbmri_eric_capabilities.csv')
        meta_data.write(self.cwd + '/data_model/eu_bbmri_eric_countries.csv')
        meta_data.write(self.cwd + '/data_model/eu_bbmri_eric_collection_types.csv')
        meta_data.write(self.cwd + '/data_model/eu_bbmri_eric_data_types.csv')
        meta_data.write(self.cwd + '/data_model/eu_bbmri_eric_disease_types.csv')
        meta_data.write(self.cwd + '/data_model/eu_bbmri_eric_image_data_types.csv')
        meta_data.write(self.cwd + '/data_model/eu_bbmri_eric_imaging_modality.csv')
        meta_data.write(self.cwd + '/data_model/eu_bbmri_eric_lab_standards.csv')
        meta_data.write(self.cwd + '/data_model/eu_bbmri_eric_material_types.csv')
        meta_data.write(self.cwd + '/data_model/eu_bbmri_eric_ops_standards.csv')
        meta_data.write(self.cwd + '/data_model/eu_bbmri_eric_sex_types.csv')
        meta_data.write(self.cwd + '/data_model/eu_bbmri_eric_temp_types.csv')
        meta_data.write(packages)
        meta_data.write(attributes)
        meta_data.write(entities)
        meta_data.close()
        response = self.session.upload_zip(zipFileName)
        status = self.check_import_run(response, "general meta data")
        if status == "FINISHED" and "FALSE" not in self.countries:
            self.upload_all_countries()

