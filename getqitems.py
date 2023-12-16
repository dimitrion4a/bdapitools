#!/usr/bin/python3

import base64
import requests
import json
from datetime import datetime,timedelta

#parameters
# -dt <minutes>  - specify number of minutes before current time as interval for searching for quarantined items
# -host <hostname> - specify hostname or IP of BD console server
# -k <apikey>    - specify API key to connect to BD console server
# -h <help> - show short instructions
# -ca <collector account>
# -cp <collector pass>
# -ch <collector host>

#https://YOUR-HOSTNAME/api/v1.0/jsonrpc/quarantine/exchange

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-dt", "--deltatime",type=int,
                    help="specify number of minutes before current time as interval for searching for quarantined items")
parser.add_argument("-host", "--hostname", help="specify hostname or IP of BD console server")
parser.add_argument("-k", "--apikey", help="specify API key to connect to BD console server")
parser.add_argument("-ca", "--collectoraccount", help="specify collector account - email address")
parser.add_argument("-cp", "--collectorpassword",help="specify collector password")
parser.add_argument("-ch", "--collectorhostname",help="specify collector hostname mailbox server")
args = parser.parse_args()


apiKey = args.apikey
loginString = apiKey + ":"
encodedBytes = base64.b64encode(loginString.encode())
encodedUserPassSequence = str(encodedBytes,'utf-8')
authorizationHeader = "Basic " + encodedUserPassSequence
endDate = datetime.datetime.now().isoformat()
parsed_date=datetime.strptime("datetime.datetime.now().isoformat(), "%Y-%m-%dT%H:%M:%S")
startDate= parsed_date+ timedelta(minutes=-args.deltatime)

apiEndpoint_Url = "https://" + args.hostname + "/api/v1.0/jsonrpc/quarantine/exchange"

request = '''     {
         "params": {
             "page": 1,
             "perPage": 100,
             "filters": {
#                 "actionStatus": 1,
                 "startDate": startDate,
                 "endDate": endDate,
             }
         },
         "jsonrpc": "2.0",
         "method": "getQuarantineItemsList",
         "id": "5399c9b5-0b46-45e4-81aa-889952433d86"
     } 
'''
result = requests.post(apiEndpoint_Url,data=request,verify=False,headers= {"Content-Type":"application/json","Authorization":authorizationHeader})

print(result.json())



