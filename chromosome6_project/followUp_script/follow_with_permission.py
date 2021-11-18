import molgenis.client as molgenis
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

import pprint

#11-11-2021 Import questionnaire to follow-up table if it is 3 year after submittion

# Save variables used through the entire script (not all are here,needs cleaning):
arguments = {"entityType1": "c6_questionnaire",
             "entityType2": "f1_questionnaire",
             "entityType3": "f2_questionnaire",
             "urlTest": "https://fernanda2.molgeniscloud.org/",
             "url": "http://localhost:8080/api/",
             "username": "admin",
             "password": "xxxxxxx",
             "sort1": "submitDate",
             "sort2": "submitDate",
             "token" : '${molgenisToken}'
             }
f1_list=[]
#RUN test server
# #testserver session
# session = molgenis.Session(arguments["urlTest"])
#
# # testserver Login
# session.login(arguments["username"], arguments["password"])
# print("\nYou are logged in as: {}".format(arguments["username"]))

#RUN with scripts on MOLGENIS
# server session
session = molgenis.Session(arguments["url"],arguments["token"])

#threeyears ago
three_yrs_time = datetime.now() - relativedelta(years=3)
three_yrs_ago = three_yrs_time.strftime("%Y-%m-%d")
print(three_yrs_ago)

# Get all questionnaire info c6
questionnaires = session.get(arguments["entityType1"], batch_size=1000, sort_column=arguments["sort1"])
print("\nEntityType: {}".format(arguments["entityType1"]))
#Get all questionnaire info follow-up1
followUp1 = session.get(arguments["entityType2"], batch_size=1000, sort_column=arguments["sort2"])
print("\nEntityType: {}".format(arguments["entityType2"]))

#change submitdate to other format
for x in questionnaires:
    if 'submitDate' in x:
        if "T" in x['submitDate']:
            x['submitDate'] = (x['submitDate']).replace ("T00:00:00Z","")

#get all questionnaires "submitted" and older teh 3 years old
for questionnaire in questionnaires:
    if questionnaire['status'] == 'SUBMITTED':
        if questionnaire['submitDate'] < three_yrs_ago:
            print('Questionnaire', questionnaire['id'], 'need follow-up')
            f1_list.append(questionnaire)
        else:
            print('Questionnaire', questionnaire['id'], 'not yet ready for follow-up, date submitted', questionnaire['submitDate'])
    else: print('Questionnaire', questionnaire['id'], 'not yet completed')

#make subselection of questionnaire not yet added to follow-up1 table
for questionnaire in f1_list:
    for followup in followUp1:
        if questionnaire['id'] == followup['id']:
            questionnaire['notneeded'] = True
    if 'notneeded' not in questionnaire:
        questionnaire['notneeded'] = False
        questionnaire['status'] = 'OPEN'
        questionnaire['submitDate'] = ''
# to delete questionnaire already present in follow-up1 table
f1_list = [i for i in f1_list if not (i['notneeded'] == True)]

#make all xref and categoricals ready for import
for questionnaire in f1_list:
    for key,value in questionnaire.items():
        if isinstance(value, dict) :
            if "HPO" in value :
                questionnaire[key] = value['HPO']
                #print(key)
            elif 'id' in value:
                questionnaire[key] = value['id']
                #print(value['id'])
        if isinstance(value, list):
            for item in value:
                if "HPO" in item:
                    #print(value)
                    i =[]
                    for y in value:
                        #print(y['label'])
                        i.append(y['HPO'])
                    questionnaire[key] = i
                elif "id" in item:
                    #print(value)
                    d =[]
                    for y in value:
                        #print(y['label'])
                        d.append(y['id'])
                    questionnaire[key] = d
pprint.pprint(f1_list)
# add all to follow-up
if len(f1_list) > 0:
    session.add_all('f1_questionnaire', f1_list)
else:
    print("no updates")
#testserver
# #add users to role f1_VIWER
# for questionnaire in f1_list:
#     response = requests.post(arguments["urlTest"] + 'api/identities/group/f1/member',
#                               headers = {'Accept': 'application/json','Content-Type': 'application/json', "x-molgenis-token": arguments["token"]},
#                               data= json.dumps({'username': questionnaire['owner'], "roleName": "f1_VIEWER" }))
#
# #make user owner
# for questionnaire in f1_list:
#     response = requests.patch(arguments["urlTest"] + 'api/permissions/entity-f1_questionnaire/' + questionnaire['id'],
#                           headers = {'Accept': 'application/json','Content-Type': 'application/json', "x-molgenis-token": arguments["token"]},
#                           data= json.dumps({'ownedByUser': questionnaire['owner'] }))
#
# #give user permission on questionnaire
# for questionnaire in f1_list:
#     response = requests.post(arguments["urlTest"] + 'api/permissions/entity-f1_questionnaire/' + questionnaire['id'],
#                          headers = {'Accept': 'application/json','Content-Type': 'application/json', "x-molgenis-token": arguments["token"]},
#                          data= json.dumps({'permissions': [{'user': questionnaire['owner'], 'permission': 'WRITE'}] }))
#Run by script on MOLGENIS
#add users to role f1_VIWER
for questionnaire in f1_list:
    response = requests.post(arguments["url"] + 'identities/group/f1/member',
                             headers = {'Accept': 'application/json','Content-Type': 'application/json', "x-molgenis-token": arguments["token"]},
                             data= json.dumps({'username': questionnaire['owner'], "roleName": "f1_VIEWER" }))

#make user owner
for questionnaire in f1_list:
    response = requests.patch(arguments["url"] + 'permissions/entity-f1_questionnaire/' + questionnaire['id'],
                              headers = {'Accept': 'application/json','Content-Type': 'application/json', "x-molgenis-token": arguments["token"]},
                              data= json.dumps({'ownedByUser': questionnaire['owner'] }))

#give user permission on questionnaire
for questionnaire in f1_list:
    response = requests.post(arguments["url"] + 'permissions/entity-f1_questionnaire/' + questionnaire['id'],
                             headers = {'Accept': 'application/json','Content-Type': 'application/json', "x-molgenis-token": arguments["token"]},
                             data= json.dumps({'permissions': [{'user': questionnaire['owner'], 'permission': 'WRITE'}] }))
