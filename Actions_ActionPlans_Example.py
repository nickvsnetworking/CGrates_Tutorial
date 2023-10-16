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


# Create the Account object inside CGrateS and apply the ActionPlan "ActionPlan_Signup_Bonus"
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

# Get Account Info (Check for the new Balance we just created)
pprint.pprint(CGRateS_Obj.SendData({'method': 'ApierV2.GetAccount', 'params': [
              {"Tenant": "cgrates.org", "Account": str(Account)}]}))