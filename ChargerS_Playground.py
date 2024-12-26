import cgrateshttpapi
import pprint
import sys
import json
import datetime
import uuid
now = datetime.datetime.now()
global CGRateS_Obj
CGRateS_Obj = cgrateshttpapi.CGRateS("localhost", 2080)

#Define default Charger
print(CGRateS_Obj.SendData({
    "method": "APIerSv1.SetChargerProfile",
    "params": [
        {
            "Tenant": "cgrates.org",
            "ID": "DEFAULT",
            'FilterIDs': [],
            'AttributeIDs' : ['*none'],
            'RunID' : 'default',
            'Weight': 0,
        }
    ]   }   ))   

#Define another Charger
print(CGRateS_Obj.SendData({
    "method": "APIerSv1.SetChargerProfile",
    "params": [
        {
            "ID": "CHARGER_Retail",
            "FilterIDs": [],
            'AttributeIDs' : ['*constant:*req.Category:RetailCharge'],
            'RunID' : 'charger_retail',
            'Weight': 0,
        }
    ]   }))

#Add a balance to the account with type *voice with 5 minutes of Talk Time
Create_Voice_Balance_JSON = {
    "method": "ApierV1.SetBalance",
    "params": [
        {
            "Tenant": "cgrates.org",
            "Account": "Nick_Test_123",
            "BalanceType": "*voice",
            "Categories": "*any",
            "Balance": {
                "ID": "5_minute_voice_balance",
                "Value": "5m",
                "Weight": 25
            }
        }
    ]
}
print(CGRateS_Obj.SendData(Create_Voice_Balance_JSON))


# Get Account Info (We'll see the new balance we just created)
pprint.pprint(CGRateS_Obj.SendData({"method": "ApierV2.GetAccount", "params": [
              {"Tenant": "cgrates.org", "Account": "Nick_Test_123"}]}))






#Generate a new call event for a 2.5 minute (150 second) call
Process_External_CDR_JSON = {
    "method": "CDRsV2.ProcessExternalCDR",
    "params": [
        {
            "OriginID": str(uuid.uuid1()),
            "ToR": "*voice",
            "RequestType": "*pseudoprepaid",
            "AnswerTime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "SetupTime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "Tenant": "cgrates.org",
            "Account": "Nick_Test_123",
            "Usage": "150s",
        }
    ]
}
print(CGRateS_Obj.SendData(Process_External_CDR_JSON))
