import cgrateshttpapi
import pprint
import sys
import uuid
#Create an Object to send the Requests to (You'll need to update this IP to point to your CGrateS instance)
CGRateS_Obj = cgrateshttpapi.CGRateS('172.16.41.134', 2080)


#Define Destinations
CGRateS_Obj.SendData({'method':'ApierV2.SetTPDestination','params':[{"TPid":"cgrates.org","ID":"Dest_AU_Fixed","Prefixes":["612", "613", "617", "618"]}]})
CGRateS_Obj.SendData({'method':'ApierV2.SetTPDestination','params':[{"TPid":"cgrates.org","ID":"Dest_AU_Mobile","Prefixes":["614"]}]})
CGRateS_Obj.SendData({'method':'ApierV2.SetTPDestination','params':[{"TPid":"cgrates.org","ID":"Dest_AU_TollFree","Prefixes":["6113", "6118"]}]})
#Get the Destinations
destinations = CGRateS_Obj.SendData({'method':'ApierV1.GetTPDestinationIDs','params':[{"TPid":"cgrates.org"}]})['result']
print("Destinations: ")
for destination in destinations:
    #Iterate through all the Destinations and print the specific data for each and pretty print them
    destination = CGRateS_Obj.SendData({'method':'ApierV1.GetTPDestination','params':[{"TPid":"cgrates.org", "ID" : str(destination)}]})['result']
    pprint.pprint(destination)
print("\n\n\n")


#Define Rates
CGRateS_Obj.SendData({"method":"ApierV1.SetTPRate","params":[{"ID":"Rate_Data_1024_1","TPid":"cgrates.org","RateSlots":[{"ConnectFee":0,"Rate":1,"RateUnit":"1024","RateIncrement":"1024","GroupIntervalStart":"0s"}]}],"id":1})
CGRateS_Obj.SendData({"method":"ApierV1.SetTPRate","params":[{"ID":"Rate_AU_Mobile_Rate_1","TPid":"cgrates.org","RateSlots":[{"ConnectFee":0,"Rate":22,"RateUnit":"60s","RateIncrement":"60s","GroupIntervalStart":"0s"}]}],"id":1})
CGRateS_Obj.SendData({"method":"ApierV1.SetTPRate","params":[{"ID":"Rate_AU_Fixed_Rate_1","TPid":"cgrates.org","RateSlots":[{"ConnectFee":0,"Rate":14,"RateUnit":"60s","RateIncrement":"60s","GroupIntervalStart":"0s"}]}],"id":1})
CGRateS_Obj.SendData({"method":"ApierV1.SetTPRate","params":[{"ID":"Rate_AU_Toll_Free_Rate_1","TPid":"cgrates.org","RateSlots":[{"ConnectFee":25,"Rate":0,"RateUnit":"60s","RateIncrement":"60s","GroupIntervalStart":"0s"}]}],"id":1})
#Get the Rates
TPRateIds = CGRateS_Obj.SendData({"method":"ApierV1.GetTPRateIds","params":[{"TPid":"cgrates.org"}]})['result']
print("Rates: ")
for TPRateId in TPRateIds:
    #Iterate through all the rates and pretty print them
    print(TPRateId)
print("\n\n\n")


#Define DestinationRate for Voice
CGRateS_Obj.SendData({"method": "ApierV1.SetTPDestinationRate", "params": [
        {"ID": "DestinationRate_AU", "TPid": "cgrates.org", "DestinationRates": [ \
            {"DestinationId": "Dest_AU_Fixed", "RateId": "Rate_AU_Fixed_Rate_1", "Rate": None, "RoundingMethod": "*up", "RoundingDecimals": 4, "MaxCost": 0, "MaxCostStrategy": ""},\
            {"DestinationId": "Dest_AU_Mobile", "RateId": "Rate_AU_Mobile_Rate_1", "Rate": None, "RoundingMethod": "*up", "RoundingDecimals": 4, "MaxCost": 0, "MaxCostStrategy": ""}, \
            {"DestinationId": "Dest_AU_TollFree", "RateId": "Rate_AU_Toll_Free_Rate_1", "Rate": None, "RoundingMethod": "*up", "RoundingDecimals": 4, "MaxCost": 0, "MaxCostStrategy": ""}\
     ]},
    ]})
#Define DestinationRate for Data
CGRateS_Obj.SendData({"method": "ApierV1.SetTPDestinationRate", "params": [
        {"ID": "DestinationRate_DataServices", "TPid": "cgrates.org", "DestinationRates": [ \
                        {"DestinationId": "*any", "RateId": "Rate_Data_1024_1", "Rate": None, "RoundingMethod": "*up", "RoundingDecimals": 4, "MaxCost": 0, "MaxCostStrategy": ""}\
        ]},
    ]})

#Get the DestinationRate we just created
print("DestinationRate: ")
TPDestinationRate = CGRateS_Obj.SendData({"jsonrpc":"2.0","method":"ApierV1.GetTPDestinationRate","params":[{"ID":"DestinationRate_AU","TPid":"cgrates.org"}],"id":1})
pprint.pprint(TPDestinationRate)
print("\n\n\n")


#Define RatingPlan
TPRatingPlans = CGRateS_Obj.SendData({
    "id": 3,
    "method": "APIerSv1.SetTPRatingPlan",
    "params": [
        {
            "TPid": "cgrates.org",
            "ID": "RatingPlan_VoiceCalls",
            "RatingPlanBindings": [
                {
                    "DestinationRatesId": "DestinationRate_AU",
                    "TimingId": "*any",
                    "Weight": 10
                }
            ]
        },
        {
            "TPid": "cgrates.org",
            "ID": "RatingPlan_DataCalls",
            "RatingPlanBindings": [
                {
                    "DestinationRatesId": "DestinationRate_DataServices",
                    "TimingId": "*any",
                    "Weight": 10
                }
            ]
        }
    ]
})
#Get the RatingPlans
RatingPlan_VoiceCalls = CGRateS_Obj.SendData(
    {"jsonrpc": "2.0", "method": "ApierV1.GetTPRatingPlanIds", "params": [{"TPid": "cgrates.org"}]})
print("RatingPlan_VoiceCalls: ")
pprint.pprint(RatingPlan_VoiceCalls)
print("\n\n\n")


#Load TariffPlan we just defiend from StorDB to DataDB
print(CGRateS_Obj.SendData({"method":"APIerSv1.LoadTariffPlanFromStorDb","params":[{"TPid":"cgrates.org","DryRun":False,"Validate":True,"APIOpts":None,"Caching":None}],"id":0}))


#Create RatingProfile
print(CGRateS_Obj.SendData({
    "method": "APIerSv1.SetRatingProfile",
    "params": [
{
            "TPid": "RatingProfile_VoiceCalls",
            "Overwrite": True,
            "LoadId" : "APItest",
            "Tenant": "cgrates.org",
            "Category": "call",
            "Subject": "*any",
            "RatingPlanActivations": [
                {
                    "ActivationTime": "2014-01-14T00:00:00Z",
                    "RatingPlanId": "RatingPlan_VoiceCalls",
                    "FallbackSubjects": ""
                }
            ]
        },
        {
            "TPid": "RatingProfile_Data",
            "Overwrite": True,
            "LoadId" : "APItest",
            "Tenant": "cgrates.org",
            "Category": "data",
            "Subject": "*any",
            "RatingPlanActivations": [
                {
                    "ActivationTime": "2014-01-14T00:00:00Z",
                    "RatingPlanId": "RatingPlan_DataCalls",
                    "FallbackSubjects": ""
                }
            ]         
        }
    ]
}))

#Get the Rating Profiles
print("GetTPRatingProfileIds: ")
TPRatingProfileIds = CGRateS_Obj.SendData({"jsonrpc": "2.0", "method": "ApierV1.GetRatingProfileIDs", "params": [{"TPid": "cgrates.org"}]})
print("TPRatingProfileIds: ")
pprint.pprint(TPRatingProfileIds)

#Define Charger
print(CGRateS_Obj.SendData({
    "method": "APIerSv1.SetChargerProfile",
    "params": [
        {
            "Tenant": "cgrates.org",
            "ID": "DEFAULT",
            'FilterIDs': [],
            'AttributeIDs' : ['*none'],
            'Weight': 0,
        }
    ]   }   ))   
#Set Charger
print("GetChargerProfile: ")
GetChargerProfile = CGRateS_Obj.SendData({"jsonrpc": "2.0", "method": "ApierV1.GetChargerProfile", "params": [{"TPid": "cgrates.org", "ID" : "DEFAULT"}]})
print("GetChargerProfile: ")
pprint.pprint(GetChargerProfile)

#Rate a test call
print("Testing call..")
cdr = CGRateS_Obj.SendData({"method": "APIerSv1.GetCost", "params": [ { \
    "Tenant": "cgrates.org", \
    "Category": "call", \
    "Subject": "1001", \
    "AnswerTime": "2025-08-04T13:00:00Z", \
    "Destination": "6140000", \
    "Usage": "123s", \
    "APIOpts": {}
    }], "id": 0})
pprint.pprint(cdr)

#Add a CDR
print("Testing call..")
cdr = CGRateS_Obj.SendData({"method": "CDRsV1.ProcessExternalCDR", "params": [ { \
"Direction": "*out",
    "Category": "call",
    "RequestType": "*raw",
    "ToR": "*monetary",
    "Tenant": "cgrates.org",
    "Account": "1002",
    "Subject": "1002",
    "Destination": "6141111124211",
    "AnswerTime": "2022-02-15 13:07:39",
    "SetupTime": "2022-02-15 13:07:30",
    "Usage": "181s",
    "OriginID": "API Function Example"
    }], "id": 0})
pprint.pprint(cdr)

#Get CDRs
cdrs = CGRateS_Obj.SendData({"method": "ApierV1.GetCDRs", "params": [ { \
"Direction": "*out",
   "Tenants": ["cgrates.org"],
   "Accounts": ["1002"],
    "TimeStart": "2022-02-14 13:07:39",
    "TimeEnd": "2022-02-16 13:07:39",
    "Limit": 100
    }], "id": 0})
pprint.pprint(cdrs)
