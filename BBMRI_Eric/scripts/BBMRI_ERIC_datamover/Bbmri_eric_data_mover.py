import os
from Bbmri_eric_model_uploader import BbmriEricModelUploader
from Bbmri_eric_quality_checker.configParser import ConfigParser
from Bbmri_eric_data_uploader import BbmriEricDataUploader

class BbmriEricDataMover():
    def __init__(self):
        self.config = ConfigParser().config
        print("Retrieving data from {} to {}".format(self.config['url'], self.config['target_server']))
        print("Uploading model")
        self.upload_model()
        print("Uploading data")
        self.upload_data()
        print("DONE!")

    def upload_model(self):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        os.chdir(ROOT_DIR)
        uploader = BbmriEricModelUploader(self.config)
        uploader.upload_all()

    def upload_data(self):
        BbmriEricDataUploader(self.config)

def main():
    BbmriEricDataMover()

if __name__ == "__main__":
    main()