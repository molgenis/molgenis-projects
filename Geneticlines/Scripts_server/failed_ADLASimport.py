#////////////////////////////////////////////////////////////////////////////
# FILE: failed_ADLASimport.py
# AUTHOR: Fernanda De Andrade
# CREATED: 24 November 2021
# MODIFIED:N/A
# PURPOSE: Monitor failed curl scripts from ADLAS import.
# STATUS: waiting on curl ADLAS
# COMMENTS: curl-commands that did not reach molgenis are NOT monitored
#////////////////////////////////////////////////////////////////////////////
import pprint
import molgenis.client as molgenis
from datetime import datetime, timedelta

# Save variables used through the entire script (not all are here,needs cleaning):
arguments = {"entityType1": "sys_ImportRun",
             "url": "http://localhost:8080/api/",
             "sort1": "startDate"
             }
# server session, token
session = molgenis.Session(arguments["url"], token="${molgenisToken}")

#get list import
importlist = session.get(arguments["entityType1"], batch_size=1000, sort_column=arguments["sort1"])
print("\nEntityType: {}".format(arguments["entityType1"]))

vandaag =  str(datetime.today())
eergisteren= str(datetime.today() - timedelta(days=2))

for x in importlist:
    x['startDate']= datetime.strptime(x['startDate'],'%Y-%m-%dT%H:%M:%SZ').strftime("%Y-%m-%d")

for x in importlist:
    if x['username'] == 'adlasuploader':
        if x['status'] == 'FAILED':
            if x['startDate'] > eergisteren and x['startDate'] <vandaag:
                2 +'2'
