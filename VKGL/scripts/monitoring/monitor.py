import json
import requests


class Molgenis():
  '''Representation of a session with the MOLGENIS REST API.'''

  def __init__(self, url="https://molgenis72.gcc.rug.nl/api/"):
    '''Constructs a new Session.'''
    self.url = url

    self.session = requests.Session()

  def get(self, entity, q=None, attributes=None, expand=None, num=100, start=0,
      sortColumn=None, sortOrder=None):
    '''Retrieves entity rows from an entity repository.'''
    if q:
      response = self.session.post(self.url + "v2/" + entity,
                                   headers=self._get_token_header_with_content_type(),
                                   params={"_method": "GET"},
                                   data=json.dumps(
                                       {"q": q, "attributes": attributes,
                                        "expand": expand, "num": num,
                                        "start": start,
                                        "sortColumn": sortColumn,
                                        "sortOrder": sortOrder}))
    else:
      response = self.session.get(self.url + "v2/" + entity,
                                  headers=self._get_token_header(),
                                  params={"attributes": attributes,
                                          "expand": expand, "num": num,
                                          "start": start,
                                          "sortColumn": sortColumn, "sortOrder":
                                            sortOrder})

    if response.status_code == 200:
      return response.json()["items"]
    response.raise_for_status()
    return response

  def _get_token_header(self):
    '''Creates an 'x-molgenis-token' header for the current session.'''
    try:
      return {"x-molgenis-token": self.token}
    except AttributeError:
      return {}

  def _get_token_header_with_content_type(self):
    '''Creates an 'x-molgenis-token' header for the current session and a 'Content-Type: application/json' header'''
    headers = self._get_token_header()
    headers.update({"Content-Type": "application/json"})
    return headers


molgenis = Molgenis()
molgenis.token = '${molgenisToken}'
molgenis.get('AMC_okt2018')
molgenis.get('ERASMUS_okt2018')
molgenis.get('LUMC_okt2018')
molgenis.get('RADBOUD_okt2018')
molgenis.get('VUMC_okt2018')
molgenis.get('UMCG_okt2018')
molgenis.get('UMCU_okt2018')
molgenis.get('comments_okt2018')
molgenis.get('VKGL_comments')
