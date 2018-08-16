import requests
import json
import math
import re


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
        '''Logs in a user and stores the acquired session token in this Session object.

        Args:
        username -- username for a registered molgenis user
        password -- password for the user
        '''
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

    def get_id_attr(self, entityType):
        meta = self.get_entity_meta_data(entityType)
        return meta['idAttribute']

    def wipe_table(self, entityType):
        id = self.get_id_attr(entityType)
        data = self.get(entityType, num=1000)
        ids = [item[id] for item in data]

        if len(ids) > 0:
            self.delete_list(entityType, ids)

        if self.get_total(entityType) > 0:
            self.wipe_table(entityType)

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

    def get_total(self, entity, q=None):
        response = self.session.get(self.url + "v2/" + entity,
                                    headers=self._get_token_header())
        if response.status_code == 200:
            return response.json()["total"]
        response.raise_for_status()
        return response

    @staticmethod
    def _merge_two_dicts(x, y):
        '''Given two dicts, merge them into a new dict as a shallow copy.'''
        z = x.copy()
        z.update(y)
        return z


def prepare_target(target, table_name):
    target.wipe_table(table_name)

def generate_public_table(molgenis, consensus_table, public_table):
    molgenis.token = '${molgenisToken}'
    prepare_target(molgenis, public_table)
    total = molgenis.get_total(consensus_table)
    times = math.ceil(total / 1000)
    for time in range(times):
        if time != 0:
            start = time * 1000
            consensus = molgenis.get(consensus_table, num=1000, start=start)
            populate_public_table(consensus, molgenis, public_table)
        else:
            consensus = molgenis.get(consensus_table, num=1000)
            populate_public_table(consensus, molgenis, public_table)


def populate_public_table(consensus, target, table_name):
    content = process_consensus(consensus)
    target.add_all(table_name, content)


def is_public_variant(variant):
    classification_type = variant['consensus_classification']
    no_consensus = 'No consensus'
    opposite = 'Opposite classification'
    return classification_type != no_consensus and classification_type != opposite


def process_consensus(consensus):
    public_variants = []
    for variant in consensus:
        if is_public_variant(variant):
            processed_variant = prepare_to_publish(variant)
            public_variants.append(processed_variant)
    return public_variants


def create_label(variant):
    return '{}:{}-{} {} {}>{}'.format(variant['chromosome'], variant['POS'], variant['stop'], variant['gene'],
                                      variant['REF'], variant['ALT'])


def get_classification(variant):
    molgenis_classification = ''
    if variant['consensus_classification'] == 'Classified by one lab':
        if 'erasmus' in variant:
            molgenis_classification = variant['erasmus']
        elif 'umcg' in variant:
            molgenis_classification = variant['umcg']
        elif 'umcu' in variant:
            molgenis_classification = variant['umcu']
        elif 'vumc' in variant:
            molgenis_classification = variant['vumc']
        elif 'radboud' in variant:
            molgenis_classification = variant['radboud']
        elif 'amc' in variant:
            molgenis_classification = variant['amc']
        elif 'nki' in variant:
            molgenis_classification = variant['nki']
        elif 'lumc' in variant:
            molgenis_classification = variant['lumc']
    else:
        molgenis_classification = variant['consensus_classification']

    if 'enign' in molgenis_classification:
        return 'LB'
    elif 'athogenic' in molgenis_classification:
        return 'LP'
    else:
        return 'VUS'


def get_support(variant):
    if variant['consensus_classification'] == 'Classified by one lab':
        return '1 lab'
    else:
        return '{} labs'.format(re.findall(r'\d', variant['consensus_classification'])[0])



def prepare_to_publish(variant):
    output = {
        'ID': variant['id'],
        'label': create_label(variant),
        'chromosome': variant['chromosome'],
        'start': variant['POS'],
        'stop': variant['stop'],
        'ref': variant['REF'],
        'alt': variant['ALT'],
        'gene': variant['gene'],
        'classification': get_classification(variant),
        'support': get_support(variant)
    }

    if 'protein' in variant:
        output['p_notation'] = variant['protein']

    if 'cDNA' in variant:
        output['c_notation'] = variant['cDNA']

    return output


def run():
    molgenis = Molgenis('${url}')
    consensus_table = '${consensus_table}'
    public_table = '${public_consensus_table}'
    generate_public_table(molgenis=molgenis, consensus_table=consensus_table, public_table=public_table)


run()
