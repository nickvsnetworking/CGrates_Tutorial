import cgrateshttpapi
import pprint
import sys
#Create an Object to send the Requests to (You'll need to update this IP to point to your CGrateS instance)
CGRateS_Obj = cgrateshttpapi.CGRateS('172.16.41.133', 2080)


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


#Define DestinationRate
CGRateS_Obj.SendData({"method": "ApierV1.SetTPDestinationRate", "params": [
        {"ID": "DestinationRate_AU", "TPid": "cgrates.org", "DestinationRates": [ \
            {"DestinationId": "Dest_AU_Fixed", "RateId": "Rate_AU_Fixed_Rate_1", "Rate": None, "RoundingMethod": "*up", "RoundingDecimals": 4, "MaxCost": 0, "MaxCostStrategy": ""},\
            {"DestinationId": "Dest_AU_Mobile", "RateId": "Rate_AU_Mobile_Rate_1", "Rate": None, "RoundingMethod": "*up", "RoundingDecimals": 4, "MaxCost": 0, "MaxCostStrategy": ""}, \
            {"DestinationId": "Dest_AU_TollFree", "RateId": "Rate_AU_Toll_Free_Rate_1", "Rate": None, "RoundingMethod": "*up", "RoundingDecimals": 4, "MaxCost": 0, "MaxCostStrategy": ""}\
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
        }
    ]
}))
#Get the Rating Profiles
print("GetTPRatingProfileIds: ")
TPRatingProfileIds = CGRateS_Obj.SendData({"jsonrpc": "2.0", "method": "ApierV1.GetRatingProfileIDs", "params": [{"TPid": "cgrates.org"}]})
print("TPRatingProfileIds: ")
pprint.pprint(TPRatingProfileIds)



#Make a test call
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
