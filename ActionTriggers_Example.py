import cgrateshttpapi
import pprint
import sys
import json
global CGRateS_Obj
CGRateS_Obj = cgrateshttpapi.CGRateS('localhost', 2080)

Account = "Nick_Test_123"

# Add a Signup Bonus of $99 to the account with type *monetary expiring a month after it's added
Action_Signup_Bonus = {
    "id": "0",
    "method": "ApierV1.SetActions",
    "params": [
        {
          "ActionsId": "Action_Add_Signup_Bonus",
          "Actions": [
              {
                  "Identifier": "*topup_reset",
                  "BalanceId": "Balance_Signup_Bonus",
                  "BalanceType": "*monetary",
                  "Units": 99,
                  "ExpiryTime": "*month",
                  "BalanceWeight": 1200,
                  "Weight": 90
              },
              {
                  "Identifier": "*cdrlog",
                  "BalanceId": "",
                  "BalanceUuid": "",
                  "BalanceType": "*monetary",
                  "Directions": "*out",
                  "Units": 0,
                  "ExpiryTime": "",
                  "Filter": "",
                  "TimingTags": "",
                  "DestinationIds": "",
                  "RatingSubject": "",
                  "Categories": "",
                  "SharedGroups": "",
                  "BalanceWeight": 0,
                  "ExtraParameters": "{\"Category\":\"^activation\",\"Destination\":\"Your sign up Bonus\"}",
                  "BalanceBlocker": "false",
                  "BalanceDisabled": "false",
                  "Weight": 80
              },
              {
                  "Identifier": "*http_post_async",
                  "ExtraParameters": "http://10.177.2.135/signup_bonus",
                  "ExpiryTime": "*unlimited",
                  "Weight": 70
              },
              {
                  "Identifier": "*log",
                  "Weight": 60
              }
          ]}]}
pprint.pprint(CGRateS_Obj.SendData(Action_Signup_Bonus))


# Create ActionPlan using SetActionPlan to trigger the Action_Signup_Bonus ASAP
SetActionPlan_Signup_Bonus_JSON = {
    "method": "ApierV1.SetActionPlan",
    "params": [{
        "Id": "ActionPlan_Signup_Bonus",
        "ActionPlan": [{
            "ActionsId": "Action_Add_Signup_Bonus",
            "Years": "*any",
            "Months": "*any",
            "MonthDays": "*any",
            "WeekDays": "*any",
            "Time": "*asap",
            "Weight": 10
        }],
        "Overwrite": True,
        "ReloadScheduler": True
    }]
}
pprint.pprint(CGRateS_Obj.SendData(SetActionPlan_Signup_Bonus_JSON))


# View the Actions we've got defined
Get_Actions_JSON = {
    "method": "APIerSv2.GetActions",
    "params": [
        {
            "Tenant": "cgrates.com"
        }

    ],
}
pprint.pprint(CGRateS_Obj.SendData(Get_Actions_JSON))



# Create the Account object inside CGrateS
Create_Account_JSON = {
    "method": "ApierV2.SetAccount",
    "params": [
        {
            "Tenant": "cgrates.org",
            "Account": str(Account),
            "ActionPlanIds": ["ActionPlan_Signup_Bonus"],
            "ActionPlansOverwrite": True,
  		    "ReloadScheduler":True
        }
    ]
}
print(CGRateS_Obj.SendData(Create_Account_JSON))

import time
#Give it a second to apply the ActionPlan
time.sleep(1)

# Get Account Info
pprint.pprint(CGRateS_Obj.SendData({'method': 'ApierV2.GetAccount', 'params': [
              {"Tenant": "cgrates.org", "Account": str(Account)}]}))






# Action to add a Monthly charge of $6
Action_Monthly_Charge = {
    "id": "0",
    "method": "ApierV1.SetActions",
    "params": [
        {
          "ActionsId": "Action_Monthly_Charge",
          "Actions": [
              {
                'Identifier': '*debit',
                'BalanceType': '*monetary',
               'Units': 6,
               'Id': 'Action_Monthly_Charge_Debit',
               'Weight': 70},
              {
                  "Identifier": "*log",
                  "Weight": 60,
                  'Id' : "Action_Monthly_Charge_Log"
              },
              {
                  "Identifier": "*cdrlog",
                  "BalanceId": "",
                  "BalanceUuid": "",
                  "BalanceType": "*monetary",
                  "Directions": "*out",
                  "Units": 0,
                  "ExpiryTime": "",
                  "Filter": "",
                  "TimingTags": "",
                  "DestinationIds": "",
                  "RatingSubject": "",
                  "Categories": "",
                  "SharedGroups": "",
                  "BalanceWeight": 0,
                  "ExtraParameters": "{\"Category\":\"^activation\",\"Destination\":\"Recurring Charge\"}",
                  "BalanceBlocker": "false",
                  "BalanceDisabled": "false",
                  "Weight": 80
              },
          ]}]}
pprint.pprint(CGRateS_Obj.SendData(Action_Monthly_Charge))

# View the Actions we've got defined
Get_Actions_JSON = {
    "method": "APIerSv2.GetActions",
    "params": [
        {
            "Tenant": "cgrates.com",
            "Id" : "Action_Monthly_Charge"
        }

    ],
}
pprint.pprint(CGRateS_Obj.SendData(Get_Actions_JSON))


# # Create ActionPlan using SetActionPlan to trigger the Action_Monthly_Charge
SetActionPlan_Daily_Action_Monthly_Charge_JSON = {
    "method": "ApierV1.SetActionPlan",
    "params": [{
        "Id": "ActionPlan_Monthly_Charge",
        "ActionPlan": [{
            "ActionsId": "Action_Monthly_Charge",
            "Years": "*any",
            "Months": "*any",
            "MonthDays": "*any",
            "WeekDays": "*any",
                        "Time": "*every_minute",
                        "Weight": 10
        }],
        "Overwrite": True,
        "ReloadScheduler": True
    }]
}
pprint.pprint(CGRateS_Obj.SendData(
    SetActionPlan_Daily_Action_Monthly_Charge_JSON))


# Get the GetActionPlanIDs
Action_Plan_IDs = CGRateS_Obj.SendData(
    {'method': 'ApierV2.GetActionPlanIDs', 'params': []})['result']
for result in Action_Plan_IDs:
    print("Getting info for ActionPlan: " + str(result))
    pprint.pprint(CGRateS_Obj.SendData(
        {'method': 'ApierV2.GetActionPlan', 'params': [{"ID": str(result)}]})['result'])


# Create the Account object inside CGrateS & assign ActionPlan_Signup_Bonus and ActionPlan_Monthly_Charge
Create_Account_JSON = {
    "method": "ApierV2.SetAccount",
    "params": [
        {
            "Tenant": "cgrates.org",
            "Account": str(Account),
            "ActionPlanIds": ["ActionPlan_Signup_Bonus", "ActionPlan_Monthly_Charge"],
            "ActionPlansOverwrite": True,
  		    "ReloadScheduler":True
        }
    ]
}
print(CGRateS_Obj.SendData(Create_Account_JSON))

# Get the GetActionPlanIDs
Action_Plan_IDs = CGRateS_Obj.SendData(
    {'method': 'ApierV2.GetActionPlanIDs', 'params': []})['result']
for result in Action_Plan_IDs:
    print("Getting info for ActionPlan: " + str(result))
    pprint.pprint(CGRateS_Obj.SendData(
        {'method': 'ApierV2.GetActionPlan', 'params': [{"ID": str(result)}]})['result'])


# Get Account Info
pprint.pprint(CGRateS_Obj.SendData({'method': 'ApierV2.GetAccount', 'params': [
              {"Tenant": "cgrates.org", "Account": str(Account)}]}))

#Define a new Action to send an HTTP POST
Action_HTTP_Notify_95 = {
    "id": "0",
    "method": "ApierV1.SetActions",
    "params": [
        {
          "ActionsId": "Action_HTTP_Notify_95",
          "Actions": [
              {
                  "Identifier": "*http_post_async",
                  "ExtraParameters": "http://10.177.2.135/95_remaining",
                  "ExpiryTime": "*unlimited",
                  "Weight": 700
              },
              {
                  "Identifier": "*log",
                  "Weight": 1200
              }
          ]}]}
pprint.pprint(CGRateS_Obj.SendData(Action_HTTP_Notify_95))

#Define ActionTrigger
ActionTrigger_95_Remaining_JSON = {
    "method": "APIerSv1.SetActionTrigger",
    "params": [
        {
            "GroupID" : "ActionTrigger_95_Remaining",
            "ActionTrigger": 
                {
                    "BalanceType": "*monetary",
                    "Balance" : {
                        'BalanceType': '*monetary',
                        'ID' : "*default",
                        'BalanceID' : "*default",
                        'Value' : 95,
                        },
                    "ThresholdType": "*min_balance",
                    "ThresholdValue": 95,
                    "Weight": 10,
                    "ActionsID" : "Action_HTTP_Notify_95",
                },
            "Overwrite": True
        }
    ]
}
pprint.pprint(CGRateS_Obj.SendData(ActionTrigger_95_Remaining_JSON))

#Get ActionTriggers
Get_Action_Triggers_JSON = {
    "method": "APIerSv1.GetActionTriggers",
    "params": [
        {"GroupID" : "ActionTrigger_95_Remaining"}
    ]
}
pprint.pprint(CGRateS_Obj.SendData(Get_Action_Triggers_JSON))


#Add ActionTrigger to Account 
Add_ActionTrigger_to_Account_JSON = {
    "method": "APIerSv1.AddAccountActionTriggers",
    "params": [
        {
            "Tenant": "cgrates.org",
            "Account": str(Account),
            "ActionTriggerIDs": ["ActionTrigger_95_Remaining"],
            "ActionTriggersOverwrite": True
        }
    ]
}
pprint.pprint(CGRateS_Obj.SendData(Add_ActionTrigger_to_Account_JSON))

# Get Account Info
pprint.pprint(CGRateS_Obj.SendData({'method': 'ApierV2.GetAccount', 'params': [
              {"Tenant": "cgrates.org", "Account": str(Account)}]}))
