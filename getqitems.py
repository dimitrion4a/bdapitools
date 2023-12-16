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
                    help="specify number of minutes before current time as interval for searching for quarantined items",required=True)
parser.add_argument("-host", "--hostname", help="specify hostname or IP of BD console server",required=True)
parser.add_argument("-k", "--apikey", help="specify API key to connect to BD console server",required=True)
parser.add_argument("-ca", "--collectoraccount", help="specify collector account - email address",required=True)
parser.add_argument("-cp", "--collectorpassword",help="specify collector password",required=True)
parser.add_argument("-ch", "--collectorhostname",help="specify collector hostname mailbox server",required=True)
args = parser.parse_args()


apiKey = args.apikey
loginString = apiKey + ":"
encodedBytes = base64.b64encode(loginString.encode())
encodedUserPassSequence = str(encodedBytes,'utf-8')
authorizationHeader = "Basic " + encodedUserPassSequence
datetimenow=datetime.now()
endDate = datetimenow.isoformat()
datetimestart=datetimenow - timedelta(minutes=args.deltatime)
startDate= datetimestart.isoformat()

apiEndpoint_Url = "https://" + args.hostname + "/api/v1.0/jsonrpc/quarantine/exchange"

request = '''     {
         "params": {
             "page": 1,
             "perPage": 100,
             "filters": {
#                 "actionStatus": 1,
                 "startDate": '''+startDate+''',
                 "endDate": '''+endDate+''',
             }
         },
         "jsonrpc": "2.0",
         "method": "getQuarantineItemsList",
         "id": "5399c9b5-0b46-45e4-81aa-889952433d86"
     } 
'''
result = requests.post(apiEndpoint_Url,data=request,verify=False,headers= {"Content-Type":"application/json","Authorization":authorizationHeader})

#print(result.json())

#for testing:
jsonsample = '''
{
         "id":"5399c9b5-0b46-45e4-81aa-889952433d86",
         "jsonrpc":"2.0",
         "result": {
              "page": "2",
              "pagesCount": "10",
              "perPage": "1",
              "total": "10",
              "items":[{
                   "id": "5b7d219bb1a43d170b7b23ee",
                   "quarantinedOn": "2019-08-01T07:15:20",
                   "actionStatus": 1,
                   "endpointId": "5d36c255f23f730fa91944e2",
                   "endpointName": "Computer 1",
                   "endpointIP": "57.238.160.118",
                   "endpointAvailable": true,
                   "threatName": "Virus 0",
                   "companyId": "55896b87b7894d0f367b23c6",
                   "details": {
                       "threatStatus": 4,
                       "itemType" : 0,
                       "detectionPoint": 1,
                       "email": { 
                           "senderIP": "185.36.136.238",
                           "senderEmail": "[email protected]",
                           "subject":
                         "Test subject_5b7d2128b1a43da20c7b23c6",
                           "recipients": [
                              "emailprotected", "email protected"
                           ],
                           "realRecipients": [
                              "emailprotected", "email protected"
                          ]
                       }
                   }
               }]
          }
     }  
     '''

#json_q_items = json.load(result.json())
json_q_items = json.loads(jsonsample)
print(type(json_q_items))
quarantineItemsIds=[]
for item in json_q_items["result"]["items"]:
    for itemprop in item:
        print(itemprop + ":" + json_q_items[itemprop])
        quarantineItemsIds.append(json_q_items[id])

#response sample
# {
#          "id":"5399c9b5-0b46-45e4-81aa-889952433d86",
#          "jsonrpc":"2.0",
#          "result": {
#               page: 2,
#               pagesCount: 10,
#               perPage: 1,
#               total: 10
#               items[{
#                    "id": "5b7d219bb1a43d170b7b23ee",
#                    "quarantinedOn": "2019-08-01T07:15:20",
#                    "actionStatus": 1,
#                    "endpointId": "5d36c255f23f730fa91944e2",
#                    "endpointName": "Computer 1",
#                    "endpointIP": "57.238.160.118",
#                    "endpointAvailable": true,
#                    "threatName": "Virus 0",
#                    "companyId": "55896b87b7894d0f367b23c6",
#                    "details": {
#                        "threatStatus": 4,
#                        "itemType" : 0,
#                        "detectionPoint": 1,
#                        "email": { 
#                            "senderIP": "185.36.136.238",
#                            "senderEmail": "[email protected]",
#                            "subject":
#                          "Test subject_5b7d2128b1a43da20c7b23c6",
#                            "recipients": [
#                               "[email protected]", "
#                               [email protected]",
#                            ]
#                            "realRecipients": [
#                               "[email protected]", "
#                               [email protected]"
#                           ]
#                        }
#                    }
#                }]
#           }
#      }  

# de interes:
# id
# quarantinedOn
# actionStatus
# senderIP



#create array of quarantineItemsIds
#call createRestoreQuarantineExchangeItemTask
#https://YOUR-HOSTNAME/api/v1.0/jsonrpc/quarantine/exchange
# Request:

#   {
#        "params": {
#            "quarantineItemsIds": [
#                "63896b87b7894d0f367b23c6",
#                "65896b87b7894d0f367b23c6"
#            ],
#            "username": "user@domain",
#            "password": "userPassword",
#             "email":   "wfwe@wsf.rr"
#        },
#        "jsonrpc": "2.0",
#        "method": "createRestoreQuarantineExchangeItemTask",
#        "id": "5399c9b5-0b46-45e4-81aa-889952433d86"
#   }   
# Response:

#   {
#       "id": "5399c9b5-0b46-45e4-81aa-889952433d86",
#       "jsonrpc":"2.0",
#       "result": True
#   }   


#connect to email server to download elements