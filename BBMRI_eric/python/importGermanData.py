import requests
import json

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (bytes, bytearray)):
            return obj.decode("ASCII")  # <- or any other encoding of your choice
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class Molgenis():
    '''Representation of a session with the MOLGENIS REST API.'''

    def __init__(self, url="https://molgenis01.gcc.rug.nl:443/api/"):
        '''Constructs a new Session.'''
        self.url = url

        self.session = requests.Session()

    def login(self, username, password):
        '''Logs in a user and stores the acquired session token in this Session object.'''
        self.session.cookies.clear()
        response = self.session.post(self.url + "v1/login",
                                     data=json.dumps({"username": username, "password": password}),
                                     headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            self.token = response.json()["token"]
        response.raise_for_status()
        return response

    def logout(self):
        '''Logs out the current session token.'''
        response = self.session.post(self.url + "v1/logout",
                                     headers=self._get_token_header())
        if response.status_code == 200:
            self.token = None
        response.raise_for_status()
        return response

    def get(self, entity, q=None, attributes=None, expand=None, num=100, start=0, sortColumn=None, sortOrder=None):
        '''Retrieves entity rows from an entity repository.'''
        if q:
            response = self.session.post(self.url + "v2/" + entity,
                                         headers=self._get_token_header_with_content_type(),
                                         params={"_method": "GET"},
                                         data=json.dumps(
                                             {"q": q, "attributes": attributes, "expand": expand, "num": num,
                                              "start": start,
                                              "sortColumn": sortColumn, "sortOrder": sortOrder}))
        else:
            response = self.session.get(self.url + "v2/" + entity,
                                        headers=self._get_token_header(),
                                        params={"attributes": attributes, "expand": expand, "num": num, "start": start,
                                                "sortColumn": sortColumn, "sortOrder":
                                                    sortOrder})

        if response.status_code == 200:
            return response.json()["items"]
        response.raise_for_status()
        return response

    def add_all(self, entity, entities):
        '''Adds multiple entity rows to an entity repository.'''
        response = self.session.post(self.url + "v2/" + entity,
                                     headers=self._get_token_header_with_content_type(),
                                     data=json.dumps({"entities": entities}))
        print(response)
        if response.status_code == 201:
            return [resource["href"].split("/")[-1] for resource in response.json()["resources"]]
        else:
            errors = json.loads(response.content.decode("utf-8"))['errors'][0]['message']
            print(errors)
        response.raise_for_status()
        return response

    def delete_list(self, entity, entities):
        '''Deletes multiple entity rows to an entity repository, given a list of id's.'''
        headers = self._get_token_header_with_content_type()
        response = self.session.delete(self.url + "v2/" + entity,
                                       headers=headers,
                                       data=json.dumps({"entityIds": entities}))
        response.raise_for_status()
        return response

    def get_entity_meta_data(self, entity):
        '''Retrieves the metadata for an entity repository.'''
        response = self.session.get(self.url + "v1/" + entity + "/meta?expand=attributes", headers=
        self._get_token_header())
        response.raise_for_status()
        return response.json()

    def get_molgenis_upload_format(self, entityType):
        data = self.get(entityType, num=10000)
        one_to_manys = self._get_one_to_manys(entityType)
        upload_format = []
        for i, item in enumerate(data):
            new_item = item
            del new_item['_href']
            for one_to_many in one_to_manys:
                del new_item[one_to_many]
            for key in new_item:
                if type(new_item[key]) is dict:
                    ref = new_item[key]['id']
                    new_item[key] = ref
                elif type(new_item[key]) is list:
                    if len(new_item[key]) > 0:
                        # get id for each new_item in list
                        mref = [l['id'] for l in new_item[key]]
                        new_item[key] = mref
            upload_format.append(new_item)
        return upload_format

    def wipe_table(self, entityType):
        data = self.get(entityType, num=10000)
        ids = [item['id'] for item in data]
        if len(ids) > 0:
            self.delete_list(entityType, ids)

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

    def _get_one_to_manys(self, entity):
        '''Retrieves one-to-many's in table'''
        meta = self.get_entity_meta_data(entity)['attributes']
        one_to_manys = [attr for attr in meta if meta[attr]['fieldType'] == "ONE_TO_MANY"]
        return one_to_manys

    @staticmethod
    def _merge_two_dicts(x, y):
        '''Given two dicts, merge them into a new dict as a shallow copy.'''
        z = x.copy()
        z.update(y)
        return z


def replace_chars(id):
    invalid_chars = ['!', '$', '%', '^', '&', '*', '(', ')', '+', '|', '~', '=', '`', '{', '}', '[', ']',
                     '"', ';', '#', "'", '<', '>', '?', ',', '\\', '/', ' ']
    charList = ['_' if char in invalid_chars else char for char in id]
    if id != ''.join(charList):
        print("Invalid characters in: ", id)
    return ''.join(charList)

def syncEricWithTMF(tables, sourceUrl, targetUrl, token):
    germanMolgenis = Molgenis(sourceUrl)
    ericMolgenis = Molgenis(targetUrl)
    ericMolgenis.token=token
    #wipe everything before upload because this works the other way around as updating
    for table in reversed(tables):
        ericMolgenis.wipe_table(table)
    for table in tables:
        german = germanMolgenis.get_molgenis_upload_format(table)
        if len(german) > 0:
            ericMolgenis.add_all(table, german)


def importGermanData():
    source = "https://molgenis93.gcc.rug.nl/api/"
    target = "https://molgenis129.gcc.rug.nl/api/"
    token = '${molgenisToken}'
    syncEricWithTMF(["eu_bbmri_eric_DE_persons", "eu_bbmri_eric_DE_networks", "eu_bbmri_eric_DE_biobanks", "eu_bbmri_eric_DE_collections"], source, target, token)

importGermanData()