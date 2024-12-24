import cgrateshttpapi
import pprint
import sys
import uuid
#Create an Object to send the Requests to (You'll need to update this IP to point to your CGrateS instance)
CGRateS_Obj = cgrateshttpapi.CGRateS('localhost', 2080)
import time
tpid = "NickTest_" + str(int(time.time()))

print("Creating TPID: " + tpid)

#Define Destinations
CGRateS_Obj.SendData({'method':'ApierV2.SetTPDestination','params':[{"TPid": tpid,"ID":"Dest_GY_Fixed","Prefixes":["5922", "5923", "5927", "5928"]}]})
CGRateS_Obj.SendData({'method':'ApierV2.SetTPDestination','params':[{"TPid": tpid,"ID":"Dest_GY_Mobile","Prefixes":["5924"]}]})
CGRateS_Obj.SendData({'method':'ApierV2.SetTPDestination','params':[{"TPid": tpid,"ID":"Dest_GY_TollFree","Prefixes":["59213", "59218"]}]})
#Get the Destinations
destinations = CGRateS_Obj.SendData({'method':'ApierV1.GetTPDestinationIDs','params':[{"TPid": tpid}]})['result']
print("Destinations: ")
for destination in destinations:
    #Iterate through all the Destinations and print the specific data for each and pretty print them
    destination = CGRateS_Obj.SendData({'method':'ApierV1.GetTPDestination','params':[{"TPid": tpid, "ID" : str(destination)}]})['result']
    pprint.pprint(destination)
print("\n\n\n")


#Define Rates
CGRateS_Obj.SendData({"method":"ApierV1.SetTPRate","params":[{"ID":"Rate_Data_1024_1","TPid": tpid,"RateSlots":[{"ConnectFee":0,"Rate":1,"RateUnit":"1024","RateIncrement":"1024","GroupIntervalStart":"0s"}]}],"id":1})
CGRateS_Obj.SendData({"method":"ApierV1.SetTPRate","params":[{"ID":"Rate_GY_Mobile_Rate_1","TPid": tpid,"RateSlots":[{"ConnectFee":0,"Rate":22,"RateUnit":"60s","RateIncrement":"60s","GroupIntervalStart":"0s"}]}],"id":1})
CGRateS_Obj.SendData({"method":"ApierV1.SetTPRate","params":[{"ID":"Rate_GY_Fixed_Rate_1","TPid": tpid,"RateSlots":[{"ConnectFee":0,"Rate":14,"RateUnit":"60s","RateIncrement":"60s","GroupIntervalStart":"0s"}]}],"id":1})
CGRateS_Obj.SendData({"method":"ApierV1.SetTPRate","params":[{"ID":"Rate_GY_Toll_Free_Rate_1","TPid": tpid,"RateSlots":[{"ConnectFee":25,"Rate":0,"RateUnit":"60s","RateIncrement":"60s","GroupIntervalStart":"0s"}]}],"id":1})
#Get the Rates
TPRateIds = CGRateS_Obj.SendData({"method":"ApierV1.GetTPRateIds","params":[{"TPid": tpid}]})['result']
print("Rates: ")
for TPRateId in TPRateIds:
    #Iterate through all the rates and pretty print them
    print(TPRateId)
print("\n\n\n")


#Define DestinationRate for Voice
CGRateS_Obj.SendData({"method": "ApierV1.SetTPDestinationRate", "params": [
        {"ID": "DestinationRate_GY", "TPid": tpid, "DestinationRates": [ \
            {"DestinationId": "Dest_GY_Fixed", "RateId": "Rate_GY_Fixed_Rate_1", "Rate": None, "RoundingMethod": "*up", "RoundingDecimals": 4, "MaxCost": 0, "MaxCostStrategy": ""},\
            {"DestinationId": "Dest_GY_Mobile", "RateId": "Rate_GY_Mobile_Rate_1", "Rate": None, "RoundingMethod": "*up", "RoundingDecimals": 4, "MaxCost": 0, "MaxCostStrategy": ""}, \
            {"DestinationId": "Dest_GY_TollFree", "RateId": "Rate_GY_Toll_Free_Rate_1", "Rate": None, "RoundingMethod": "*up", "RoundingDecimals": 4, "MaxCost": 0, "MaxCostStrategy": ""}\
     ]},
    ]})


#Get the DestinationRate we just created
print("DestinationRate: ")
TPDestinationRate = CGRateS_Obj.SendData({"jsonrpc":"2.0","method":"ApierV1.GetTPDestinationRate","params":[{"ID":"DestinationRate_GY","TPid": tpid}],"id":1})
pprint.pprint(TPDestinationRate)
print("\n\n\n")


print(CGRateS_Obj.SendData({"method":"ApierV2.SetTPTiming","params":[{"TPid":tpid,"ID":"Timing_Monday","Years":"*any","Months":"*any","MonthDays":"*any","WeekDays":"1","Time":"00:00:00"}]}))
print(CGRateS_Obj.SendData({"method":"ApierV2.SetTPTiming","params":[{"TPid":tpid,"ID":"Timing_Tuesday","Years":"*any","Months":"*any","MonthDays":"*any","WeekDays":"2","Time":"00:00:00"}]}))
print(CGRateS_Obj.SendData({"method":"ApierV2.SetTPTiming","params":[{"TPid":tpid,"ID":"Timing_Wednesday","Years":"*any","Months":"*any","MonthDays":"*any","WeekDays":"3","Time":"00:00:00;23:59:59"}]}))
print(CGRateS_Obj.SendData({"method":"ApierV2.SetTPTiming","params":[{"TPid":tpid,"ID":"Timing_Thursday","Years":"*any","Months":"*any","MonthDays":"*any","WeekDays":"4","Time":"00:00:00;23:59:59"}]}))
print(CGRateS_Obj.SendData({"method":"ApierV2.SetTPTiming","params":[{"TPid":tpid,"ID":"Timing_Friday","Years":"*any","Months":"*any","MonthDays":"*any","WeekDays":"5","Time":"00:00:00;23:59:59"}]}))
print(CGRateS_Obj.SendData({"method":"ApierV2.SetTPTiming","params":[{"TPid":tpid,"ID":"Timing_Saturday","Years":"*any","Months":"*any","MonthDays":"*any","WeekDays":"6","Time":"00:00:00;23:59:59"}]}))
print(CGRateS_Obj.SendData({"method":"ApierV2.SetTPTiming","params":[{"TPid":tpid,"ID":"Timing_Sunday","Years":"*any","Months":"*any","MonthDays":"*any","WeekDays":"7","Time":"00:00:00;23:59:59"}]}))
print(CGRateS_Obj.SendData({"method":"ApierV2.SetTPTiming","params":[{"TPid":tpid,"ID":"TM_MORNING","Years":"*any","Months":"*any","MonthDays":"*any","WeekDays":"1,2,3,4,5","Time":"08:00:00;23:59:59"}]}))


#Define RatingPlan
TPRatingPlans = CGRateS_Obj.SendData({
    "id": 3,
    "method": "APIerSv1.SetTPRatingPlan",
    "params": [
        {
            "TPid": tpid,
            "ID": "RatingPlan_VoiceCalls",
            "RatingPlanBindings": [
                {
                    "DestinationRatesId": "DestinationRate_GY",
                    "TimingId": "*any",
                    "Weight": 10
                }
            ]
        },
    ]
})
#Get the RatingPlans
RatingPlan_VoiceCalls = CGRateS_Obj.SendData(
    {"jsonrpc": "2.0", "method": "ApierV1.GetTPRatingPlanIds", "params": [{"TPid": tpid}]})
print("RatingPlan_VoiceCalls: ")
pprint.pprint(RatingPlan_VoiceCalls)
print("\n\n\n")


#Load TariffPlan we just defiend from StorDB to DataDB
print(CGRateS_Obj.SendData({"method":"APIerSv1.LoadTariffPlanFromStorDb","params":[{"TPid": tpid,"DryRun":False,"Validate":True,"APIOpts":None,"Caching":None}],"id":0}))


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
    ]
}))

#Get the Rating Profiles
print("GetTPRatingProfileIds: ")
TPRatingProfileIds = CGRateS_Obj.SendData({"jsonrpc": "2.0", "method": "ApierV1.GetRatingProfileIDs", "params": [{"TPid": tpid}]})
print("TPRatingProfileIds: ")
pprint.pprint(TPRatingProfileIds)

# Define Charger
print(CGRateS_Obj.SendData({
    "method": "APIerSv1.SetChargerProfile",
    "params": [
        {
            "Tenant": "cgrates.org",
            "ID": "DEFAULT",
            'FilterIDs': [],
            'AttributeIDs': ['*none'],
            "RunID": "DEFAULT",
            'Weight': 0,
        }
    ]}))
# Set Charger
print("GetChargerProfile: ")
GetChargerProfile = CGRateS_Obj.SendData(
    {"jsonrpc": "2.0", "method": "ApierV1.GetChargerProfile", "params": [{"Tenant": "cgrates.org", "ID": "DEFAULT"}]})
print("GetChargerProfile: ")
pprint.pprint(GetChargerProfile)

#Clear the Cache
pprint.pprint(CGRateS_Obj.SendData({"method":"CacheSv1.Clear","params":[]}))

StatQueueProfile_VoiceStats = {
    "method":"APIerSv1.SetStatQueueProfile",
    "params":[{
        "Tenant":"cgrates.org",
        "ID":"StatQueueProfile_VoiceStats",
        "FilterIDs":["*string:~*req.Account:Nick"],
        "ActivationInterval":None,
        "QueueLength":10000000,
        "TTL":-1,
        "MinItems":0,
        "Metrics":[
            {"FilterIDs":None,"MetricID":"*tcd"},
            {"FilterIDs":None,"MetricID":"*asr"},
            {"FilterIDs":None,"MetricID":"*acd"}
            ],
        "Stored":True,
        "Blocker":False,
        "Weight":0,
        "ThresholdIDs":None,
        }]}
pprint.pprint(CGRateS_Obj.SendData(StatQueueProfile_VoiceStats))

pprint.pprint(CGRateS_Obj.SendData({"method": "ApierV1.SetFilter", "params": [{"Tenant": "cgrates.org", "ID": "Filter_Monday", "Rules": [{"Type": "*timings", "Element": "~*req.AnswerTime", "Values": ["Timing_Monday"]}], "ActivationInterval": {}}]}))
pprint.pprint(CGRateS_Obj.SendData({"method": "ApierV1.SetFilter", "params": [{"Tenant": "cgrates.org", "ID": "Filter_Tuesday", "Rules": [{"Type": "*timings", "Element": "~*req.AnswerTime", "Values": ["Timing_Tuesday"]}], "ActivationInterval": {}}]}))
pprint.pprint(CGRateS_Obj.SendData({"method": "ApierV1.SetFilter", "params": [{"Tenant": "cgrates.org", "ID": "Filter_Wednesday", "Rules": [{"Type": "*timings", "Element": "~*req.AnswerTime", "Values": ["Timing_Wednesday"]}], "ActivationInterval": {}}]}))
pprint.pprint(CGRateS_Obj.SendData({"method": "ApierV1.SetFilter", "params": [{"Tenant": "cgrates.org", "ID": "Filter_Thursday", "Rules": [{"Type": "*timings", "Element": "~*req.AnswerTime", "Values": ["Timing_Thursday"]}], "ActivationInterval": {}}]}))
pprint.pprint(CGRateS_Obj.SendData({"method": "ApierV1.SetFilter", "params": [{"Tenant": "cgrates.org", "ID": "Filter_Friday", "Rules": [{"Type": "*timings", "Element": "~*req.AnswerTime", "Values": ["Timing_Friday"]}], "ActivationInterval": {}}]}))
pprint.pprint(CGRateS_Obj.SendData({"method": "ApierV1.SetFilter", "params": [{"Tenant": "cgrates.org", "ID": "Filter_Saturday", "Rules": [{"Type": "*timings", "Element": "~*req.AnswerTime", "Values": ["Timing_Saturday"]}], "ActivationInterval": {}}]}))
pprint.pprint(CGRateS_Obj.SendData({"method": "ApierV1.SetFilter", "params": [{"Tenant": "cgrates.org", "ID": "Filter_Sunday", "Rules": [{"Type": "*timings", "Element": "~*req.AnswerTime", "Values": ["Timing_Sunday"]}], "ActivationInterval": {}}]}))
pprint.pprint(CGRateS_Obj.SendData({"method": "ApierV1.SetFilter", "params": [{"Tenant": "cgrates.org", "ID": "FLTR_TM_1", "Rules": [{"Type": "*timings", "Element": "~*req.AnswerTime", "Values": ["TM_MORNING"]}], "ActivationInterval": {}}]}))


StatQueueProfile_VoiceStats_Monday = {
    "method":"APIerSv1.SetStatQueueProfile",
    "params":[{
        "Tenant":"cgrates.org",
        "ID":"StatQueueProfile_VoiceStats_Monday",
        "FilterIDs":[
            #"*string:~*req.Account:Nick",
            "Filter_Monday",
        ],
        "ActivationInterval":None,
        "QueueLength":10000000,
        "TTL":-1,
        "MinItems":0,
        "Metrics":[
            {"FilterIDs":None,"MetricID":"*tcd"},
            ],
        "Stored":True,
        "Blocker":False,
        "Weight":0,
        "ThresholdIDs":None,
        }]}
pprint.pprint(CGRateS_Obj.SendData(StatQueueProfile_VoiceStats_Monday))

import random
import uuid


count = 0
while count < 20:
    count += 1
    #Add a CDR
    print("Testing call..")
    area_codes = ["5922", "5923", "5927", "5928", "5924", "59213", "59218"]
    Subject = random.choice(area_codes) + str(random.randint(10000000, 99999999)).zfill(8)
    Duration = str(random.randint(1, 1000)) + "s"
    start_date = "2025-01-01 00:00:00"
    end_date = "2025-01-28 23:59:59"
    from datetime import datetime, timedelta
    start = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

    # Generate a random timestamp between start and end
    SetupTime = start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

    #Add a random number of seconds to the AnswerTime
    AnswerTime = SetupTime + timedelta(seconds=random.randint(0, 10))

    # Format back to string in the same format
    AnswerTime = AnswerTime.strftime("%Y-%m-%d %H:%M:%S")
    SetupTime = SetupTime.strftime("%Y-%m-%d %H:%M:%S")

    ProcessCDR = {"method": "CDRsV1.ProcessExternalCDR", "params": [ { \
    "Direction": "*out",
        "Category": "call",
        #"RequestType": "*raw",
        #"ToR": "*monetary",
        "Tenant": "cgrates.org",
        "Account": "Nick",
        "Subject": Subject,
        "Destination": Subject,
        "AnswerTime": AnswerTime,
        "SetupTime": SetupTime,
        "Usage": Duration,
        "OriginID": str(uuid.uuid4())
        }], "id": 0}
    pprint.pprint(ProcessCDR)

    cdr = CGRateS_Obj.SendData(ProcessCDR)
    pprint.pprint(cdr)


#Get StatsQueues
GetStatQueues = {
    "method": "APIerSv1.GetStatQueueProfile",
    "Tenant": "cgrates.org",
    "params": [
        {
            "ID": "StatQueueProfile_TalkTime",
        }
    ]
}
pprint.pprint(CGRateS_Obj.SendData(GetStatQueues))

#Get Metrics
GetMetrics = {"method":"StatSv1.GetQueueStringMetrics","params":[{"Tenant":"","ID":"StatQueueProfile_VoiceStats","APIOpts":{}}],"id":11}
pprint.pprint(CGRateS_Obj.SendData(GetMetrics))
GetMetrics = {"method":"StatSv1.GetQueueStringMetrics","params":[{"Tenant":"","ID":"StatQueueProfile_VoiceStats","APIOpts":{}}],"id":11}
pprint.pprint(CGRateS_Obj.SendData(GetMetrics))
