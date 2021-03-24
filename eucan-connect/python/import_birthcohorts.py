"""
 202011 Dieuwke Roelofs-Prins
 Script to import birthcohort data (using JSON API from birthcohorts.net)
 and add the data to the EUCAN model.
"""

# Import module(s)
import molgenis.client as molgenis
import random
import re
import requests
import string
import argparse
import logging as log

class molgenisExtra(molgenis.Session):
    # deze klasse bevat alle functionaliteit die ook in de normale client.Session zit
    # + de extra functionaliteit die je zelf toevoegt:

    def update_all(self, entity, entities):
        """Updates multiple entity rows in an entity repository."""
        response = self._session.put(self._url + "v2/" + quote_plus(entity),
                                      headers=self._get_token_header_with_content_type(),
                                      data=json.dumps({"entities": entities}))

        try:
            response.raise_for_status()
        except requests.RequestException as ex:
            self._raise_exception(ex)

        return [resource["href"].split("/")[-1] for resource in response.json()["resources"]]

# Define function(s)

# Generate a random string with selected number of characters (both alphanumeric as well as numeric). 
def random_string(n_chars):
    random_string = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(n_chars)]) 
  
    # Print the random string of length n_chars
    return (random_string)

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', dest='username', default='admin', help='Username for the MOLGENIS server')
parser.add_argument('-p', '--password', dest='password', help='Password to login to the MOLGENIS server')
parser.add_argument('-s', '--server', dest='server', default='https://catalogue.eucanconnect.eu/api/', help='URL of the API end-point of the MOLGENIS server.')
parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='Provide debug logging.')

args = parser.parse_args()

if args.username is None or args.password is None or args.server is None:
    log.error('Must specify username, password and server.')
    raise SystemExit('Must specify username, password and server.')

# Define variable(s)

# Constant variables
birthCohortsUrl='www.birthcohorts.net/wp-content/themes/x-child/rss.cohorts.php?'
call_limit=10

eucan_session = molgenisExtra(args.server)
eucan_session.login(args.username, args.password)

nRetrievedCohorts = 0
user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
header={"User-Agent" : user_agent}


# Dictionaries
countryIDs={}
existing_contacts={}

# List variables
cohort_keys=['identification', 'description', 'questionnaire', 'comments']
eucan_events=[]
eucan_persons=[]
eucan_populations=[]
eucan_studies=[]
eucan_delete_events=[]
eucan_delete_persons=[]
eucan_delete_populations=[]
eucan_delete_studies=[]
events = []
persons = []
populations = []
study_names=[]
title_list=['Prof.', 'Professor', 'Prof', 'Dr.', 'dr.', 'Dr']

######## Get the total number of cohorts from birthcohorts.net ######
BirthCohorts=requests.get(url='http://' + birthCohortsUrl + 'limit=0&json', headers=header)

if len(BirthCohorts.json()) == 0:
    raise SystemExit('No data from birthcohorts.net found?!?')

n_birthcohorts=135
# The API returns 159, but we can only fetch 135
# n_birthcohorts= BirthCohorts.json()['@attributes']['count']
log.info('Total number of birth cohorts is', BirthCohorts.json()['@attributes']['count'])

# Get the list with countries from EUCAN
countries=eucan_session.get('eucan_country', batch_size=1000)

if len(countries) == 0:
    raise SystemExit('No countries found?!?')

for country in countries:
    # In the birth cohorts data no distinguish is made between first_name and last_name only the full name is available
    countryIDs[country['label']]=country['id']

# Get the current list with persons/contacts from EUCAN
persons=eucan_session.get('eucan_persons', batch_size=1000)

if len(persons) == 0:
    #raise SystemExit('No persons found?!?')
    log.error('No persons found in EUCAN')

for person in persons:
    # In birthcohorts no distinguish is made between first_name and last_name only the full name is available
    existing_contacts[person['last_name']]=person['id']

# Get the current list of birth cohort studies from EUCAN
studies=eucan_session.get('eucan_study', attributes='study_name', q='source_catalogue=="https://birthcohorts.net"', batch_size=1000)

if len(studies) == 0:
    #raise SystemExit('No studies found?!?')
    log.error('No birth cohort studies found in EUCAN')
else: log.info('Number of birth cohort studies in EUCAN', len(studies))

for study in studies:
    log.info(study)
    study_names.append(study['study_name'])

# Get the current list of events from EUCAN
data_events=eucan_session.get('eucan_events', attributes='name', batch_size=1000)

if len(data_events) == 0:
    #raise SystemExit('No data events found?!?')
    log.error('No Data Events found in EUCAN')

for data_event in data_events:
    events.append(data_event['name'])

# Get the current list of populations from EUCAN
populations_eucan=eucan_session.get('eucan_population', attributes='id', batch_size=1000)

if len(populations_eucan) == 0:
    #raise SystemExit('No populations found?!?')
    log.error('No populations found in EUCAN')

for population in populations_eucan:
    populations.append(population['id'])      

######## Get the birth cohorts data from birthcohorts.net ######

pageNr=1
while pageNr < int(n_birthcohorts) + call_limit:
    BirthCohorts=requests.get(url='http://' + birthCohortsUrl + 'limit=' + str(call_limit) + '&page=' + str(pageNr) + '&json', headers=header)
    log.debug(BirthCohorts.json()['@attributes'])
    pageNr=pageNr+call_limit

    for key in BirthCohorts.json().keys():
        if key not in ['@attributes', 'cohort']:
            log.error('There is another dictionary key ('+key+') found than cohort and @attributes!')
            raise SystemExit('There is another dictionary key ('+key+') found than cohort and @attributes!')

    if 'cohort' not in BirthCohorts.json().keys():
        if n_birthcohorts != nRetrievedCohorts:
            log.error('No more cohorts anymore?!? Number of cohorts retreived is '+str(nRetrievedCohorts)+' expected number is '+str(n_birthcohorts))
            raise SystemExit('No more cohorts anymore?!? Number of cohorts retreived is '+str(nRetrievedCohorts)+' expected number is '+str(n_birthcohorts))
        else: 
            log.info('All birth cohorts are retrieved')
            break # All cohorts are retrieved add/update the data

    for birth_cohort in BirthCohorts.json()['cohort']:
        log.info(birth_cohort['identification']['id'], birth_cohort['identification']['name'])

    for birth_cohort in BirthCohorts.json()['cohort']:
        nRetrievedCohorts += 1
        # Empty the variables
        contactIDs=[]
        eucan_event={}
        eucan_pop_children={}
        eucan_pop_mothers={}
        eucan_pop_fathers={}
        eucan_pop_grandparents={}
        eucan_pop_fam_members={}
        eucan_study={}
        investigatorIDs=[]
        study_acronym=''
        titles=[]
        
        for key in birth_cohort.keys():
            if key not in cohort_keys:
                raise SystemExit(key+' is a new item in the birth_cohort dictionary!')
            if key=='identification':
                # Derivation/Definition of some variables (and mising values)
                if type(birth_cohort['identification']['contact']['name']) is dict and len(birth_cohort['identification']['contact']['name']) == 0:
                    contacts="Unknown"
                else: contacts=birth_cohort['identification']['contact']['name']
                if type(birth_cohort['identification']['investigator']['name']) is dict and len(birth_cohort['identification']['investigator']['name']) == 0:
                    investigators="Unknown"
                else: investigators = birth_cohort['identification']['investigator']['name']
                if type(birth_cohort['identification']['contact']['email']) is dict and len(birth_cohort['identification']['contact']['email']) == 0:
                    contact_emails=None
                else: contact_emails = birth_cohort['identification']['contact']['email']
                if type(birth_cohort['identification']['investigator']['email']) is dict and len(birth_cohort['identification']['investigator']['email']) == 0:
                    investigator_emails=None
                else: investigator_emails = birth_cohort['identification']['investigator']['email']
                if type(birth_cohort['identification']['website']) is not dict:
                        if len(birth_cohort['identification']['website'].split()) > 1:
                            print('More than one website available for study '+birth_cohort['identification']['name']+' '+birth_cohort['identification']['website'])
                            # If more than one website is available, the first one is stored
                            website=birth_cohort['identification']['website'].split()[0].strip()
                        else: website=birth_cohort['identification']['website'].strip()
                else: website=None

                # Get the right country ID
                country = None
                if type(birth_cohort['identification']['country']) is dict and len(birth_cohort['identification']['country']) == 0:
                    country=None
                else:
                    for country_name in countryIDs.keys():
                        if country_name in birth_cohort['identification']['country']:
                            country=countryIDs[country_name]
                            break
                    if country == None: country=birth_cohort['identification']['country']

                if type(birth_cohort['identification']['abbreviation']) is dict and len(birth_cohort['identification']['abbreviation']) == 0:
                    if len(birth_cohort['identification']['name'].split()) == 1:
                        study_acronym = birth_cohort['identification']['name']
                        # print('Eigen acronym Een woord', birth_cohort['identification']['name'], study_acronym)
                    else: 
                        for word in birth_cohort['identification']['name'].split():
                            study_acronym = study_acronym + word[0].upper()
                        # print('Eigen acronym Meerdere woorden', birth_cohort['identification']['name'], study_acronym)
                else:
                    study_acronym = birth_cohort['identification']['abbreviation'].replace(',',' and')
                    # print('Bestaand acronym', birth_cohort['identification']['name'], study_acronym)

                # Check if the contact/investigator already exist, if yes get the right ID(s)
                for i, contact_name in enumerate(re.split(', |; ', contacts), start=1):
                    if len(contact_name) > 0:
                        for title in title_list:
                            if title in contact_name:
                                titles.append(title)
                                contact_name=contact_name.replace(title, '')
                        contact_name=contact_name.strip()        
                        if contact_name in existing_contacts.keys():
                            contactIDs.append(existing_contacts[contact_name])
                        else:
                            if args.debug: log.debug('Contact', contact_name, 'not yet in EUCAN contacts')
                            contactID='birthcohorts:'+random_string(n_chars=10)
                            existing_contacts[contact_name]=contactID
                            contactIDs.append(contactID)
                            if contact_emails != None:
                                if i <= len(re.split(', |; ', contact_emails)):
                                    contact_email = re.split(', |; ', contact_emails)[i-1].strip()
                                else: contact_email = re.split(', |; ', contact_emails)[len(re.split(', |; ', contact_emails))-1].strip()
                                if '@' not in contact_email:
                                    print('Email adress', contact_email, 'is not valid')
                                    contact_email=None
                            else: contact_email = None
                            eucan_persons.append({'id': contactID,
                                                  'title': ' '.join(titles),
                                                'country': country,
                                               'first_name': contact_name,
                                               'last_name': contact_name,
                                               'email': contact_email})

                # Investigators
                for i, contact_name in enumerate(re.split(', |; ', investigators), start=1):
                    for title in title_list:
                        if title in contact_name:
                            titles.append(title)
                            contact_name=contact_name.replace(title, '')
                    contact_name=contact_name.strip()
                    if contact_name in existing_contacts.keys():
                        investigatorIDs.append(existing_contacts[contact_name])
                    else:
                        if args.debug: log.debug('Investigator', contact_name, 'not yet in EUCAN contacts')
                        contactID='birthcohorts:'+random_string(n_chars=10)
                        existing_contacts[contact_name]=contactID
                        investigatorIDs.append(contactID)
                        if investigator_emails != None:
                            if i <= len(re.split(', |; ', investigator_emails)):
                                contact_email = re.split(', |; ', investigator_emails)[i-1].strip()
                            else: contact_email = re.split(', |; ', investigator_emails)[len(re.split(', |; ', investigator_emails))-1].strip()
                        else: contact_email = None
                        eucan_persons.append({'id': contactID,
                                    'country': country,
                                    'title': ' '.join(titles),
                                   'first_name': contact_name,
                                   'last_name': contact_name,                              
                                   'email': contact_email})

                eucan_study={'id': 'birthcohorts:'+birth_cohort['identification']['id'],
                             'study_name': birth_cohort['identification']['name'].strip(),
                             'acronym': study_acronym,
                             'start_year': birth_cohort['identification']['date'][0:4].replace('0000',''),
                             'website': website,
                             'principle_investigators': investigatorIDs,
                             'contacts': contactIDs,
                             'source_catalogue':'https://www.birthcohorts.net/birthcohorts/birthcohort/?id='+birth_cohort['identification']['id'],
                             'populations': []}
            

            elif key == 'description':
                if len(birth_cohort['description']['enrollment']['followup']) > 0:
                    name = birth_cohort['description']['enrollment']['followup'].replace('\t', '')
                    name = name.replace('\n','')
                    name = name.replace("/",'_')
                    name = name.replace(' ', '')
                    name = name.strip()
                    eucan_study['data_collection_events'] = name
                # Definition of some variables (and mising values)
                    if type(birth_cohort['description']['enrollment']['period']['start']) is not dict \
                       and len(birth_cohort['description']['enrollment']['period']['start']) != 0 \
                       and type(birth_cohort['description']['enrollment']['period']['end']) is not dict \
                       and len(birth_cohort['description']['enrollment']['period']['end']) != 0:
                        start_end_year=birth_cohort['description']['enrollment']['period']['start'][0:4]+'-'+birth_cohort['description']['enrollment']['period']['end'][0:4]
                        start_end_month=birth_cohort['description']['enrollment']['period']['start'][5:7]+'-'+birth_cohort['description']['enrollment']['period']['end'][5:7]
                    else:
                        start_end_year=None
                        start_end_month=None

                    event_id = 'birthcohorts:'+random_string(8)
                    eucan_event={'id': event_id,
                                 'name': study_acronym+'_'+name,
                                 'description': birth_cohort['description']['enrollment']['followup'],
                                 'start_end_year': start_end_year,
                                 'start_end_month': start_end_month}

                    eucan_study['data_collection_events'] = event_id

                # Population information
                if type(birth_cohort['description']['enrollment']['criteria_exclusion']) is dict:
                    selection_criteria_supplement = None
                else:
                    selection_criteria_supplement = birth_cohort['description']['enrollment']['criteria_exclusion']
                    selection_criteria_supplement = selection_criteria_supplement.replace('\n','')
                  
                if int(birth_cohort['description']['recruited']['children']) > 0:
                    eucan_pop_children={'id': 'birthcohorts:'+random_string(8),
                                     'name': study_acronym+' - Children',
                                     'number_of_participants': birth_cohort['description']['recruited']['children'],
                                     'selection_criteria_supplement': selection_criteria_supplement}
                    eucan_study['populations'].append(eucan_pop_children['id'])
                if int(birth_cohort['description']['recruited']['mothers']) > 0:
                    eucan_pop_mothers={'id': 'birthcohorts:'+random_string(8),
                                     'name': study_acronym+' - Mothers',
                                     'number_of_participants': birth_cohort['description']['recruited']['mothers'],
                                     'selection_criteria_supplement': selection_criteria_supplement}
                    eucan_study['populations'].append(eucan_pop_mothers['id'])
                if int(birth_cohort['description']['recruited']['fathers']) > 0:
                    eucan_pop_fathers={'id': 'birthcohorts:'+random_string(8),
                                     'name': study_acronym+' - Fathers',
                                     'number_of_participants': birth_cohort['description']['recruited']['fathers'],
                                     'selection_criteria_supplement': selection_criteria_supplement}
                    eucan_study['populations'].append(eucan_pop_fathers['id'])
                if int(birth_cohort['description']['recruited']['grandparents']) > 0:
                    eucan_pop_grandparents={'id': 'birthcohorts:'+random_string(8),
                                     'name': study_acronym+' - Grandparents',
                                     'number_of_participants': birth_cohort['description']['recruited']['grandparents'],
                                     'selection_criteria_supplement': selection_criteria_supplement}
                    eucan_study['populations'].append(eucan_pop_grandparents['id'])
                if int(birth_cohort['description']['recruited']['familymembers']) > 0:
                    eucan_pop_fam_members={'id': 'birthcohorts:'+random_string(8),
                                     'name': study_acronym+' - FamilyMembers',
                                     'number_of_participants': birth_cohort['description']['recruited']['familymembers'],
                                     'selection_criteria_supplement': selection_criteria_supplement}
                    eucan_study['populations'].append(eucan_pop_fam_members['id'])
                if type(birth_cohort['description']['aim']) is not dict and len(birth_cohort['description']['aim']) > 0:
                    eucan_study['objectives']= birth_cohort['description']['aim']

        # If a study, person, event or population already exists these will be deleted first
        # Add the data to the lists to be uploaded
        if len(eucan_event) > 0:
            if eucan_event['name'] in events:
                eucan_delete_events.append(eucan_event['name'])
            eucan_events.append(eucan_event)
        if len(eucan_pop_children) > 0:
            if eucan_pop_children['id'] in populations:
                eucan_delete_populations.append(eucan_pop_children['id'])
            eucan_populations.append(eucan_pop_children)
        if len(eucan_pop_mothers) > 0:
            if eucan_pop_mothers['id'] in populations:
                eucan_delete_populations.append(eucan_pop_mothers['id'])
            eucan_populations.append(eucan_pop_mothers)
        if len(eucan_pop_fathers) > 0:
            if eucan_pop_fathers['id'] in populations:
                eucan_delete_populations.append(eucan_pop_fathers['id'])
            eucan_populations.append(eucan_pop_fathers)
        if len(eucan_pop_grandparents) > 0:
            if eucan_pop_grandparents['id'] in populations:
                eucan_delete_populations.append(eucan_pop_grandparents['id'])
            eucan_populations.append(eucan_pop_grandparents)
        if len(eucan_pop_fam_members) > 0:
            if eucan_pop_fam_members['id'] in populations:
                eucan_delete_populations.append(eucan_pop_fam_members['id'])
            eucan_populations.append(eucan_pop_fam_members)
        if len(eucan_study) > 0:
            if eucan_study['study_name'] in study_names:
                eucan_delete_studies.append(eucan_study['study_name'])
            eucan_studies.append(eucan_study)


for pop in eucan_populations:
    if 'name' not in pop:
        print('Missing name', pop)

if  len(eucan_studies) != n_birthcohorts:
    raise SystemExit('Number of new birth cohorts and birth cohorts to be updated ('+len(eucan_studies)+') is not equal to total number of birth cohorts ('+n_birthcohorts+')')
    print('Number of new birth cohorts and birth cohorts to be updated (', len(eucan_studies), ') is not equal to total number of birth cohorts (', n_birthcohorts,')')

# Delete existing birth cohort data from EUCAN

if len(eucan_delete_studies) > 0:
    print('\nDelete', len(eucan_delete_studies),'studies')    
    eucan_session.delete_list('eucan_study', eucan_delete_studies)

if len(eucan_delete_populations) > 0:
    print('\nDelete', len(eucan_delete_populations), 'populations')      
    eucan_session.delete_list('eucan_population', eucan_delete_populations)

if len(eucan_delete_events) > 0:
    print('\nDelete', len(eucan_delete_events), 'events')      
    eucan_session.delete_list('eucan_events', eucan_delete_events)

if len(eucan_delete_persons) > 0:
    print('\nDelete', len(eucan_delete_persons), 'persons')      
    eucan_session.delete_list('eucan_persons', eucan_delete_persons)        


# Add new birth cohorts to EUCAN
if len(eucan_persons) > 0:
    print('\nAdd', len(eucan_persons), 'Contacts')
    for person in eucan_persons:
        if len(person['first_name']) == 0: print(person)
    eucan_session.add_all('eucan_persons', eucan_persons)
else: print('\nNo new contacts to be added')
if len(eucan_events) > 0:
    print('\nAdd', len(eucan_events), 'Events')
    eucan_session.add_all('eucan_events', eucan_events)
else: print('\nNo new events to be added')

if len(eucan_populations) > 0:
    print('\nAdd', len(eucan_populations), 'Populations')
    eucan_session.add_all('eucan_population', eucan_populations)
else: print('\nNo new populations to be added')
print('\nAdd', len(eucan_studies), 'Studies')
eucan_session.add_all('eucan_study', eucan_studies)

print('FINISHED')


