import molgenis.client as molgenis
import pandas as pd
import tempfile
from os.path import abspath
import csv
import numpy as np
from datetime import date,datetime

#uncomment when deployed and fill password
host = 'https://geneticlines.molgeniscloud.org/'
username = "admin"
password ="XXXXXXXXXXXXXX"

class Molgenis(molgenis.Session):
  def __init__(self, *args, **kwargs):
    super(Molgenis, self).__init__(*args, **kwargs)
    self.fileImportApi = f"{self._root_url}plugin/importwizard/importFile"
    # self.host = self._api_url.replace('/api/','')
    # self.fileImportApi = f"{self.host}/plugin/importwizard/importFile"


  def to_csv(self, path, df):
    """To CSV
    Write pandas dataframe as CSV file

    @param path location to save the file
    @param df pandas data.frame
    """
    data = df.replace({np.nan: None})
    data.to_csv(path, index=False, quoting=csv.QUOTE_ALL)

  def importPandasAsCsv(self, pkg_entity, data):
    with tempfile.TemporaryDirectory() as tmpdir:
      filepath=f"{tmpdir}/{pkg_entity}.csv"
      self.to_csv(filepath, data)
      with open(abspath(filepath),'r') as file:
        response = self._session.post(
          url=self.fileImportApi,
          headers = self._headers.token_header,
          files={'file': file},
          params = {'action': 'add_update_existing', 'metadataAction': 'ignore'}
        )

        if (response.status_code // 100) != 2:
          print('Failed to import data into', pkg_entity,'(',response.status_code,')')
        else:
          print('Imported data into', pkg_entity)
      return response

#####################
db = Molgenis(url=host)
db.login(username=username, password=password)
##########################
datefolder= '20221031'#fill correct folder
file= '/Users/andradefm/Documents/Project/GeneticLinesBiobank/import_BIMS/' + datefolder +'/spss_data/Biomateriaal sample informatie (BIO_SAMPLE).sav'
file2='/Users/andradefm/Documents/Project/GeneticLinesBiobank/import_BIMS/' + datefolder +'/spss_data/Biomateriaal (BIMS_BIOMAT).sav'
df= pd.read_spss(file)
df2= pd.read_spss(file2)
db.importPandasAsCsv(pkg_entity="epicportal_BIOSAMPLE", data=df)
db.importPandasAsCsv(pkg_entity="epicportal_BIOMAT", data=df2)
