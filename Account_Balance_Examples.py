import cgrateshttpapi
import pprint
import sys
import json
import datetime
import uuid
now = datetime.datetime.now()
global CGRateS_Obj
CGRateS_Obj = cgrateshttpapi.CGRateS("localhost", 2080)


#Create the Account object inside CGrateS 
Create_Account_JSON = {
    "method": "ApierV2.SetAccount",
    "params": [
        {
            "Tenant": "cgrates.org",
            "Account": "Nick_Test_123"
        }
    ]
}
print(CGRateS_Obj.SendData(Create_Account_JSON))

# Get Account Info (We'll see the Account we just created, but no balances)
pprint.pprint(CGRateS_Obj.SendData({"method": "ApierV2.GetAccount", "params": [
              {"Tenant": "cgrates.org", "Account": "Nick_Test_123"}]}))







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

# Get Account Info Again (This time we'll see only 150 seconds of the 300 seconds we just allocated, as we just used 150 seconds with the last call)
pprint.pprint(CGRateS_Obj.SendData({"method": "ApierV2.GetAccount", "params": [
              {"Tenant": "cgrates.org", "Account": "Nick_Test_123"}]}))










#Create the Destinations we use to filter by dialled number
CGRateS_Obj.SendData({'method':'ApierV2.SetTPDestination','params':[{"TPid":"cgrates.org","ID":"Dest_AU_Fixed","Prefixes":["612", "613", "617", "618"]}]})
CGRateS_Obj.SendData({'method':'ApierV2.SetTPDestination','params':[{"TPid":"cgrates.org","ID":"Dest_AU_Mobile","Prefixes":["614"]}]})

#Load destinations we just defined from StorDB to DataDB
print(CGRateS_Obj.SendData({"method":"APIerSv1.LoadTariffPlanFromStorDb","params":[{"TPid":"cgrates.org","DryRun":False,"Validate":True,"APIOpts":None,"Caching":None}],"id":0}))



#Add a balance to the account with type *voice with 100 minutes of talk time to Local / National Destinations expiring at the end of the month
Create_Local_National_Voice_Balance_JSON = {
    "method": "ApierV1.SetBalance",
    "params": [
        {
            "Tenant": "cgrates.org",
            "Account": "Nick_Test_123",
            "BalanceType": "*voice",
            "Categories": "*any",
            "Balance": {
                "ID": "Local_National_100_minutes_voice_balance",
                "Value": "100m",
                "ExpiryTime": "*month_end",
                "Weight": 60,
                "DestinationIDs": "Dest_AU_Fixed",
            }
        }
    ]
}
print(CGRateS_Obj.SendData(Create_Local_National_Voice_Balance_JSON))

#Add a balance to the account with type *voice with 40 minutes of talk time to Mobile Destinations expiring in 24 hours
Create_Mobile_Voice_Balance_JSON = {
    "method": "ApierV1.SetBalance",
    "params": [
        {
            "Tenant": "cgrates.org",
            "Account": "Nick_Test_123",
            "BalanceType": "*voice",
            "Categories": "*any",
            "Balance": {
                "ID": "Mobile_40_minutes_voice_balance",
                "Value": "40m",
                "ExpiryTime": "*daily",
                "Weight": 60,
                "DestinationIDs": "Dest_AU_Mobile",
            }
        }
    ]
}
print(CGRateS_Obj.SendData(Create_Mobile_Voice_Balance_JSON))

# Get Account Info Again to see the new balances we just created 
pprint.pprint(CGRateS_Obj.SendData({"method": "ApierV2.GetAccount", "params": [
              {"Tenant": "cgrates.org", "Account": "Nick_Test_123"}]}))






#Generate a new call event for a 2.5 minute (150 second) call to a mobile number (Will deduct from Mobile_40_minutes_voice_balance)
Process_External_CDR_JSON = {
    "method": "CDRsV2.ProcessExternalCDR",
    "params": [
        {
            "OriginID": str(uuid.uuid1()),
            "ToR": "*voice",
            "RequestType": "*pseudoprepaid",
            "AnswerTime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "SetupTime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "Subject": "61412341234",
            "Destination": "61412341234",
            "Tenant": "cgrates.org",
            "Account": "Nick_Test_123",
            "Usage": "30s",
        }
    ]
}
print(CGRateS_Obj.SendData(Process_External_CDR_JSON))

#Generate a new call event for a 2.5 minute (150 second) call to a fixed line local/national number (Will deduct from Local_National_100_minutes_voice_balance)
Process_External_CDR_JSON = {
    "method": "CDRsV2.ProcessExternalCDR",
    "params": [
        {
            "OriginID": str(uuid.uuid1()),
            "ToR": "*voice",
            "RequestType": "*pseudoprepaid",
            "AnswerTime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "SetupTime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "Subject": "61212341234",
            "Destination": "61212341234",
            "Tenant": "cgrates.org",
            "Account": "Nick_Test_123",
            "Usage": "30s",
        }
    ]
}
print(CGRateS_Obj.SendData(Process_External_CDR_JSON))

# Get Account Info Again to show the balances being deducted
pprint.pprint(CGRateS_Obj.SendData({"method": "ApierV2.GetAccount", "params": [
              {"Tenant": "cgrates.org", "Account": "Nick_Test_123"}]}))










#Generate a new call event for a 42 minute call to a mobile to use all of our Mobile_40_minutes_voice_balance and start consuming 5_minute_voice_balance
Process_External_CDR_JSON = {
    "method": "CDRsV2.ProcessExternalCDR",
    "params": [
        {
            "OriginID": str(uuid.uuid1()),
            "ToR": "*voice",
            "RequestType": "*pseudoprepaid",
            "AnswerTime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "SetupTime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "Subject": "61412341234",
            "Destination": "61412341234",
            "Tenant": "cgrates.org",
            "Account": "Nick_Test_123",
            "Usage": "2450s",
        }
    ]
}
print(CGRateS_Obj.SendData(Process_External_CDR_JSON))

# Get Account Info Again
pprint.pprint(CGRateS_Obj.SendData({"method": "ApierV2.GetAccount", "params": [
              {"Tenant": "cgrates.org", "Account": "Nick_Test_123"}]}))