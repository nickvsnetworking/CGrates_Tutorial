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
            "ID": "Charger_API_Default",
            "RunID": "*Charger_API_Default_RunID",  #Arbitrary Sting
            'FilterIDs': [],
            'AttributeIDs': ['*none'],
            'Weight': 999,
        }
    ]   }   ))  

#Add a balance to the account with type *generic with 10 units of balance
Create_Generic_Balance_JSON = {
    "method": "ApierV1.SetBalance",
    "params": [
        {
            "Tenant": "cgrates.org",
            "Account": "Nick_Test_123",
            "BalanceType": "*generic",
            "Categories": "*any",
            "Balance": {
                "ID": "100_units_generic_balance",
                "Value": "100",
                "Weight": 25,
                "Blocker": "true",       #This stops the Monetary Balance from being used
            }
        }
    ]
}
print(CGRateS_Obj.SendData(Create_Generic_Balance_JSON))


now = datetime.datetime.now()
OriginID = str(uuid.uuid4())
call_event = {
                "RequestType": "*prepaid",
                "ToR": "*generic",
                "Tenant": "cgrates.org",
                "Account": "Nick_Test_123",
                "AnswerTime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "SetupTime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "OriginID": str(uuid.uuid1()),
                "OriginHost": "ScratchPad",
            }

while input("Enter to continue or q to quit") != "q":
    call_event['Usage'] = str(input("Usage: "))
    result = CGRateS_Obj.SendData(
        {"method": "SessionSv1.UpdateSession", "params": [
            {
                "GetAttributes": False,
                "UpdateSession": True,
                "Subsystem" : "sessions",
                "Tenant": "cgrates.org",
                "ID": OriginID,
                "Context": None,
                "Time": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "Event":
                    call_event}
        ]})
    pprint.pprint(result)
print("Quit")
