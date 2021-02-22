###
# 2020-05-06 Dieuwke Roelofs-Prins
# Script which updates the COVID19 attributes in eu_bbmri_eric_biobanks and
# eu_bbmri_eric_collections with information from eu_bbmri_eric_CentralBioCovid
# and eu_bbmri_eric_CentralColCovid


import requests
import json
from urllib.parse import quote_plus, urlparse, parse_qs

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (bytes, bytearray)):
            return obj.decode("ASCII")  # <- or any other encoding of your choice
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

class Session():
    '''Representation of a session with the MOLGENIS REST API.'''
    '''Depending on the Molgenis Version different REST API's are available'''

    def __init__(self, url="http://localhost:80/api/", debug=False):
        '''Constructs a new Session.'''
        self.url = url

        self.debug = debug

        self.session = requests.Session()

        response = self.session.get(self.url + 'v2/version',
                                     headers=self._get_token_header())
        molgenisVersion=json.loads(response.text)['molgenisVersion']

        if molgenisVersion < '8':
            self.rest_api='v2'
        else:
            self.rest_api='data'

        print('Molgenis Version of {0} is {1}, used REST API is {2}'.format(self.url, molgenisVersion, self.rest_api))
               
    def get(self, entity, q=None, attributes=None, num=None, batch_size=10000, start=0, sortColumn=None, sortOrder=None, raw=False,
            expand=None):
        """Retrieves all entity rows from an entity repository.
        Args:
        entity -- fully qualified name of the entity
        q -- query in rsql format, see our RSQL documentation for details
            (https://molgenis.gitbooks.io/molgenis/content/developer_documentation/ref-RSQL.html)
        attributes -- The list of attributes to retrieve
        expand -- the attributes to expand
        num -- the maximum amount of entity rows to retrieve
        batch_size - the amount of entity rows to retrieve per time (max. 10.000)
        start -- the index of the first row to retrieve (zero indexed)
        sortColumn -- the attribute to sort on
        sortOrder -- the order to sort in
        raw -- when true, the complete REST response will be returned, rather than the data items alone
        Examples:
        >>> session = Session('http://localhost:80/api/')
        >>> session.get('Person')
        >>> session.get(entity='Person', q='name=="Henk"', attributes=['name', 'age'])
        >>> session.get(entity='Person', sort_column='age', sort_order='desc')
        >>> session.get('Person', raw=True)
        """

        if not sortColumn:  # Ensure correct ordering for batched retrieval for old Molgenis instances
            for items in self.get_entity_meta_data(entity)['items']:
                if items['data']['idAttribute']:
                    sortColumn=items['data']['name']

        if not attributes:
            filter=attributes
        else:
            filter=','.join(attributes)

        batch_start = start
        items = []

        while not num or len(items) < num:  # Keep pulling in batches
            response = self.session.get(self.url + self.rest_api + '/' + entity,
                                        headers=self._get_token_header(),
                                        params={"q":q, "filter": filter, "expand": expand, "num": batch_size, "start": batch_start,
                                                  "sortColumn": sortColumn, "sortOrder":sortOrder})
            
            if raw:
                return response  # Simply return the first batch response JSON
            else:
                if response.status_code == 200:
                    #return response.json()["items"]
                    items.extend(response.json()["items"])
                else:
                    errors = json.loads(response.content.decode("utf-8"))['errors'][0]['message']
                    print('get error', response.status_code, errors)

            if 'nextHref' in response.json():  # There is more to fetch
                decomposed_url = urlparse(response.json()['nextHref'])
                query_part_url = parse_qs(decomposed_url.query)
                batch_start = query_part_url['start'][0]
            else:
                break  # We caught them all

        if num:  # Truncate items
            items = items[:num]

        print('\nTotal number of entities retrieved from entity', entity, 'is', len(items))
        if self.debug: print('\nSELECTED items', items)
        return items

    def update_per_id(self, entity, id_, attribute_values):
        """Updates all given attributes of a given entity in a table"""
        if self.debug: print('update URL is', self.url + self.rest_api + "/" + quote_plus(entity) + "/" + id_)
        if self.debug: print('attribute_values', attribute_values)
        response = self.session.patch(self.url + self.rest_api + "/" + quote_plus(entity) + "/" + id_,
                                     headers=self._get_token_header_with_content_type(),
                                     data=json.dumps(attribute_values))
        if response.status_code != 204:
            print('Update per ID error for id', id_, 'and attribute values', attribute_values, 'ERROR', response.text)
        #try:
        #    response.raise_for_status()
        #except requests.RequestException as ex:
        #    self._raise_exception(ex)

        return response        

   
    def get_entity_meta_data(self, entity):
        '''Retrieves the metadata for an entity repository.'''
        response = self.session.get(self.url + 'metadata/' + entity + '/attributes'
                                    , headers=
        self._get_token_header())
        response.raise_for_status()
        return response.json()

    def get_molgenis_upload_format(self, entityType, n_entities, condition, attributes):
        data = self.get(entityType, num=n_entities, q=condition, attributes=attributes)
        one_to_manys = self._get_attribute_types(entityType, ['onetomany'])
        if self.debug: print('ONE TO MANYS', one_to_manys)
        xrefs = self._get_attribute_types(entityType, ['categorical', 'xref'])
        if self.debug: print('XREFS', xrefs)
        mrefs = self._get_attribute_types(entityType, ['mref', 'categoricalmref'])
        if self.debug: print('MREFS', mrefs)
        upload_format = []
        for item in data:
            new_item = item['data']
            for one_to_many in one_to_manys:
                try:
                    del new_item[one_to_many]
                except:
                    if self.debug:
                        print('one to many attribute {0} not in the selected attributes {1}'.format(one_to_many, attributes))
            for xref in xrefs:
                try:                  
                    url=new_item[xref]['links']['self'].replace(new_item[xref]['links']['self'].split('/')[2], self.url.split('/')[2])
                    new_item[xref]=self.session.get(url,
                                                    headers=self._get_token_header()).json()['data']['id']
                except:
                    if self.debug :
                        print('xref attribute {0} not in the selected attributes {1}'.format(xref, attributes))         
            for mref in mrefs:
                try:
                    mref_ids=[]                    
                    # For localhost url return contains molgenis:8080 in stead of localhost:80
                    url=new_item[mref]['links']['self'].replace(new_item[mref]['links']['self'].split('/')[2], self.url.split('/')[2])
                    mref_items=self.session.get(url,
                                                headers=self._get_token_header()).json()
                    for items in mref_items['items'] :
                        mref_ids.append(items['data']['id'])
                    new_item[mref]=mref_ids
                except:
                    if self.debug :
                        print('mref attribute {0} not in the selected attributes {1}'.format(mref, attributes))
           
            upload_format.append(new_item)
        return upload_format

    def _get_token_header(self):
        '''Creates an 'x-molgenis-token' header for the current session.'''
       # print('STAP 3: _get_token_header')
        try:
       #     print('STAP 3: self.token', self.token)
            return {"x-molgenis-token": self.token}
        except AttributeError:
       #     print('STAP 3: Attribute error')
            return {}

    def _get_token_header_with_content_type(self):
        '''Creates an 'x-molgenis-token' header for the current session and a 'Content-Type: application/json' header'''
        headers = self._get_token_header()
        headers.update({"Content-Type": "application/json"})
        return headers

    def _get_attribute_types(self, entity, data_types):
        '''Retrieves all attributes with the give data_types'''
        attributes=[]
        for item in self.get_entity_meta_data(entity)['items']:
            for data_type in data_types:
                if item['data']['type'] == data_type :
                    attributes.append(item['data']['name'])
        return attributes

def UpdateCOVID19(tables, bbmriEricUrl, UpdateToken, debug):
    EricSession = Session(bbmriEricUrl, debug)
    EricSession.token=UpdateToken


    for table_name in tables:
        # Number of entities in the end not really relevant, necessary to start the iteration
        # to be sure to get everything set is to a really high number
        n_entities=10000000

        # Define which attributes to select under which selection criteria 
        if table_name == 'eu_bbmri_eric_CentralBioCovid':
            attributes=None
            condition=None
            eric_table='eu_bbmri_eric_biobanks'
            eric_upd_attributes=['network', 'covid19biobank', 'collaboration_commercial', 'collaboration_non_for_profit']
            collaboration_commercial = ['3_commercial', '5_academic_inst_PL_for_commercial']
            collaboration_non_for_profit = ['1_non_for_profit', '2_academic', '4_non-for_profit_with_commercial_inst']
        elif table_name == 'eu_bbmri_eric_CentralColCovid':
            attributes=None
            condition=None
            eric_table='eu_bbmri_eric_collections'
            eric_upd_attributes=['network', 'diagnosis_available', 'number_of_donors', 'order_of_magnitude', 'materials', 'data_categories', 'data_access_description', 'data_access_fee', 'data_access_joint_project', 'sample_access_description', 'sample_access_fee', 'sample_access_joint_project', 'sample_processing_sop']
            # attributes that are available but not ingested are:
            # end_date, end_responsibiliby, experimental_data, funding, informed_consent,
            # institutes, link_and_enrich, multi_or_mono, organisation, principal_investigators,
            # publications, sample_access, start_date, study_type, subjects, umcg, umcg_single_site,
            # visibility_bbmri, way_collecting, website, wmo
        else:
            attributes=None
            condition=None
            eric_table='Unknown'


        print('\nGet data from table', table_name)
#        CentralCOVID19 = EricSession.get(table_name, num=n_entities, q=condition, attributes=attributes)
        CentralCOVID19 = EricSession.get_molgenis_upload_format(table_name, n_entities, condition=condition, attributes=attributes)

        # Empty the update status columns
        for entity_row in CentralCOVID19 :
            empty_status=EricSession.update_per_id(table_name, entity_row['id'], {'added' : '', 'up_to_date' : '', 'update_failed' : '' })
            if empty_status.status_code != 204:
                print('Clear the update column(s) for {0} did not go OK'.format(entity_row['label']))
                exit()
        
        for entity_row in CentralCOVID19:           
            #print(entity_row)
            print('Add data to', eric_table)
            # Ideally the batch API should be used to add the data, but this is not available yet
            # Furthermore the api/v2/entity/attribute option to update values of particular rows
            # does not work for attributes having xref/mref data types
            # Therefore for the time being do it in this way (assuming the amount of data is not that much)
            # !! WARNING, this causes overhead (indexing on machine) which in case of large amount
            # of data can give problems.

            # First check if value already exists if equal to value to add then
            # the attribute is not updated.

            print(entity_row['label'])
            condition='id=='+entity_row['label']
            current=EricSession.get_molgenis_upload_format(eric_table, n_entities, condition=condition, attributes=eric_upd_attributes)
            added = []
            up_to_date = []
            update_failed = []
            upd_entity=False

            if table_name == 'eu_bbmri_eric_CentralBioCovid' :
                if not 'covid19' in entity_row['covid19biobank'] : entity_row['covid19biobank'].append('covid19')
                entity_row['collaboration_commercial'] = False
                entity_row['collaboration_non_for_profit'] = False
                if len(set(entity_row['collaboration']).intersection(set(collaboration_commercial))) > 0:
                    entity_row['collaboration_commercial'] = True
                if len(set(entity_row['collaboration']).intersection(set(collaboration_non_for_profit))) > 0:
                    entity_row['collaboration_non_for_profit'] = True
            if table_name == 'eu_bbmri_eric_CentralColCovid' :
                entity_row['data_access_description'] = None
                entity_row['data_access_fee'] = False
                entity_row['data_access_joint_project'] = False
                entity_row['sample_access_description'] = None
                entity_row['sample_access_fee'] = False
                entity_row['sample_access_joint_project'] = False
                if 'access' in entity_row:
                    if entity_row['access'] == 'Joint project' :
                        entity_row['data_access_joint_project'] = True
                        entity_row['sample_access_joint_project'] = True
                    if entity_row['access'] == 'Fee for access' :
                        entity_row['data_access_fee'] = True
                        entity_row['sample_access_fee'] = True
                    if entity_row['access'] == 'Other':
                        entity_row['data_access_description'] = entity_row['access_description']
                        entity_row['sample_access_description'] = entity_row['access_description']                        

                
            if len(current) == 1 :
                upd_data={}
                for attribute in eric_upd_attributes:
                    if attribute in current[0] :
                        if debug: print('current', attribute, 'is', current[0][attribute], 'new is', entity_row[attribute])
                        upd_data[attribute] = current[0][attribute]
                        n_added = 0
                        if type(entity_row[attribute]) is list :
                            for value in entity_row[attribute] :
                                if value not in current[0][attribute] :
                                    upd_data[attribute].append(value)
                                    upd_entity = True
                                    n_added += 1
                            if n_added == 0 :
                                del upd_data[attribute]
                                up_to_date.append(attribute)
                        elif current[0][attribute] == entity_row[attribute] :
                            if debug: print('is gelijk', attribute)
                            del upd_data[attribute]
                            up_to_date.append(attribute)
                        elif current[0][attribute] != entity_row[attribute] :
                            if debug: print('is niet gelijk', attribute)
                            upd_data[attribute]=entity_row[attribute]
                            upd_entity = True
                    else :
                        if entity_row[attribute] != None:
                            upd_data[attribute] = entity_row[attribute]
                            upd_entity = True
                        
            else :
                print('More than one record ({0}) for id {1} of entity {2} retrieved'.format(len(current), entity_row['label'], eric_table))
                update_failed = eric_upd_attributes

            if upd_entity :
                if debug: print('update entity', eric_table, entity_row['label'], upd_data)
                update=EricSession.update_per_id(eric_table, entity_row['label'], upd_data)
                if update.status_code == 204:
                    for attribute in upd_data:
                        added.append(attribute)
                else :
                    for attribute in upd_data :
                        update_failed.append(attribute)
            
            upd=EricSession.update_per_id(table_name, entity_row['id'], {'added' : ', '.join(added), 'up_to_date': ', '.join(up_to_date), 'update_failed' : ', '.join(update_failed)})
            if debug: print('updating update status columns exit code is', upd)
 

def UpdateCOVID19Info():
    EricUrl= "https://molgenis104.gcc.rug.nl/api/"
    EricToken = '${molgenisToken}'
    debug = False
    UpdateCOVID19(["eu_bbmri_eric_CentralBioCovid", "eu_bbmri_eric_CentralColCovid"], EricUrl, EricToken, debug) 


UpdateCOVID19Info()