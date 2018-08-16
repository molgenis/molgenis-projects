import pprint, sys

from Bbmri_eric_quality_checker.qualityChecker import QualityChecker
from Bbmri_eric_quality_checker.configParser import ConfigParser
from molgenis.molgenisConnector import MolgenisConnector

class BbmriEricDataUploader():
    def __init__(self, config):
        self.diseaseCorrections = ""
        self.filter_rows = ""
        self.collections = ""
        self.biobanks = ""
        self.networks = ""
        self.persons = ""
        self.server = config['target_server']
        self.username = config['target_account']
        self.password = config['target_password']
        url = config['url']
        molgenis_connector = MolgenisConnector(url, config['account'], config['password'])
        self.retrieve_data(molgenis_connector)
        self.retrieve_country_data(config, molgenis_connector)

    def chunks(self,l):
        """Yield successive n-sized chunks from l.
        https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks"""
        n = 1000
        chunk_list = []
        for i in range(0, len(l), n):
            chunk_list.append(l[i:i + n])
        return chunk_list

    def retrieve_country_data(self, config, molgenis_connector):
        countries = config['countries'].split(',')
        if "FALSE" not in countries:
            for country in countries:
                # filter out rows with invalid disease type/network
                collections = self.convert_refs(
                    molgenis_connector.session.get("eu_bbmri_eric_{}_collections".format(country), num=10000))
                biobanks = self.convert_refs(
                    molgenis_connector.session.get("eu_bbmri_eric_{}_biobanks".format(country), num=10000))
                persons = self.convert_refs(
                    molgenis_connector.session.get("eu_bbmri_eric_{}_persons".format(country), num=10000))
                networks = self.convert_refs(
                    molgenis_connector.session.get("eu_bbmri_eric_{}_networks".format(country), num=10000))
                if len(persons) > 0:
                    try:
                        self.upload_data("eu_bbmri_eric_{}_persons".format(country), persons, self.server, self.username,
                                         self.password)
                    except:
                        print("Uploading {} failed, is it already uploaded?".format(
                            "eu_bbmri_eric_{}_persons".format(country)))
                if len(networks) > 0:
                    try:
                        self.upload_data("eu_bbmri_eric_{}_networks".format(country), networks, self.server, self.username,
                                     self.password)
                    except:
                        print("Uploading {} failed, is it already uploaded?".format(
                            "eu_bbmri_eric_{}_networks".format(country)))
                if len(biobanks) > 0:
                    try:
                        self.upload_data("eu_bbmri_eric_{}_biobanks".format(country), biobanks, self.server, self.username,
                                     self.password)
                    except:
                        print("Uploading {} failed, is it already uploaded?".format(
                            "eu_bbmri_eric_{}_biobanks".format(country)))
                if len(collections) > 0:
                    try:
                        self.upload_data("eu_bbmri_eric_{}_collections".format(country), collections, self.server,
                                     self.username, self.password)
                    except:
                        print(collections)
                        print("Uploading {} failed, is it already uploaded?".format(
                            "eu_bbmri_eric_{}_collections".format(country)))

    def retrieve_data(self, molgenis_connector):
        qc = QualityChecker(molgenis_connector)
        self.diseaseCorrections = qc.diseaseCorrections
        qc.check_collection_data()
        qc.check_biobank_data()
        qc.check_network_data()
        qc.check_person_data()
        qc.logs.close()
        self.filter_rows = qc.breaking_errors
        self.collections = self.convert_refs(qc.collection_data)
        self.biobanks = self.convert_refs(qc.biobank_data)
        self.networks = self.convert_refs(qc.network_data)
        self.persons = self.convert_refs(qc.person_data)
        # order: persons, networks, biobanks, collections
        try:
            personList = self.chunks(self.persons)
            for persons in personList:
                self.upload_data("eu_bbmri_eric_persons", persons, self.server, self.username, self.password)
        except:
            print("Uploading {} failed, is it already uploaded?".format("eu_bbmri_eric_persons"))
        try:
            networkList = self.chunks(self.networks)
            for networks in networkList:
                self.upload_data("eu_bbmri_eric_networks", networks, self.server, self.username, self.password)
        except:
            print("Uploading {} failed, is it already uploaded?".format("eu_bbmri_eric_networks"))
        try:
            biobankList = self.chunks(self.biobanks)
            for biobanks in biobankList:
                self.upload_data("eu_bbmri_eric_biobanks", biobanks, self.server, self.username, self.password)
        except:
            print("Uploading {} failed, is it already uploaded?".format("eu_bbmri_eric_biobanks"))
        try:
            collectionList = self.chunks(self.collections)
            for collections in collectionList:
                self.upload_data("eu_bbmri_eric_collections", collections, self.server, self.username, self.password)
        except:
            print("Uploading {} failed, is it already uploaded?".format("eu_bbmri_eric_collections"))

    def upload_data(self, entity, entities, url, user, pwd):
        new_server = MolgenisConnector(url, user, pwd)
        print('Uploading {}...'.format(entity))
        status = new_server.session.add_all(entity, entities)

    def convert_refs(self, data):
        new_data = []
        for i, item in enumerate(data):
            new_item = item
            del new_item['_href']
            for key in new_item:
                if key == 'diagnosis_available':
                    correctCodes = []
                    codes = new_item[key]
                    for codeObj in codes:
                        code = codeObj['id']
                        if code in self.diseaseCorrections:
                            if self.diseaseCorrections[code] != 'Delete':
                                # Only get unique values
                                correctCodes = list(set(correctCodes + self.diseaseCorrections[code]))
                        else:
                            correctCodes.append(code)
                    new_item[key] = correctCodes
                elif type(new_item[key]) is dict:
                    ref = new_item[key]['id']
                    if key == 'biobank':
                        new_item[key] = ref
                    elif key == "parent_collection":
                        new_item[key] = ref
                    else:
                        new_item[key] = ref
                elif key == 'contact':
                    mref = [l['id'] for l in new_item[key]]
                    new_item[key] = mref[0]
                elif type(new_item[key]) is list:
                    if len(new_item[key]) > 0:
                        # get id for each new_item in list
                        mref = [l['id'] for l in new_item[key]]
                        new_item[key] = mref
            new_data.append(new_item)
        return new_data

def main():
    config = ConfigParser().config
    data_uploader = BbmriEricDataUploader(config)


if __name__ == '__main__':
    main()
