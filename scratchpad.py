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
