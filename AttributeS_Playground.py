import cgrateshttpapi
import pprint

CGRateS_Obj = cgrateshttpapi.CGRateS('localhost', 2080)


#Define a basic Key-Value attribute to account 1234
SetAttributeProfile = {
    "method": "APIerSv2.SetAttributeProfile",
    "params": [{
        "Tenant": "cgrates.org",
        "ID": "ATTR_Nick_Key_Value_Example",
        "Contexts": ["*any"],
        "FilterIDs": [
            "*string:~*req.Account:1234"
        ],
        "Attributes": [
            {
            "FilterIDs": [],
            "Path": "*req.ExampleKey",
            "Type": "*constant",
            "Value": "ExampleValue"
            }
        ],
        "Blocker": False,
        "Weight": 10
    }],
}
result = CGRateS_Obj.SendData(SetAttributeProfile)
pprint.pprint(result)

#Get the Attribute by calling ProcessEvent
result = CGRateS_Obj.SendData({"method":"AttributeSv1.ProcessEvent",
                               "params":[
                                   {"Tenant":"cgrates.org",
                                    "Event":{"Account":"1234"},
                                    #"APIOpts":{"*processRuns":2,"*profileRuns":1,"*subsys":"*sessions"}
                                    }]})
pprint.pprint(result)


#Create a new Attribute for storing the SIP password
SetAttributeProfile = {
    "method": "APIerSv2.SetAttributeProfile",
    "params": [{
        "Tenant": "cgrates.org",
        "ID": "ATTR_Nick_Password_Example",
        "Contexts": ["*any"],
        "FilterIDs": [
            "*string:~*req.Account:1234"
        ],
        "Attributes": [
            {
            "FilterIDs": [],
            "Path": "*req.SIP_password",
            "Type": "*constant",
            "Value": "sosecretiputitonthewebsite"
            }
        ],
        "Blocker": False,
        "Weight": 10
    }],
}
result = CGRateS_Obj.SendData(SetAttributeProfile)
pprint.pprint(result)

#Check the result again
result = CGRateS_Obj.SendData({"method":"AttributeSv1.ProcessEvent",
                               "params":[
                                   {"Tenant":"cgrates.org",
                                    "Event":{"Account":"1234"},
                                    }]})
pprint.pprint(result)
input("Enter to continue")

#Add 3 DIDs to account NickTest1234 that will get transformed to the Account
Account = 'Nick_Test_123'
for DID in ['12340001', '12340002', '12340003']:
    AttributeProfile = {
                "method": "APIerSv2.SetAttributeProfile",
                "params": [{
                    "Tenant": "cgrates.org",
                    "ID": "ATTR_Calling_" + str(Account) + "_" + str(DID),
                    "Contexts": [
                        "*any"
                    ],
                    "FilterIDs": [
                        '*string:~*req.Account:' + str(DID),
                    ],
                    "Attributes": [{
                            "Path": "*req.Account",
                            "Type": "*constant",
                            "Value": str(Account)
                        }
                    ],
                    "Weight": 0
                }],
                "id": 2
            }
    result = CGRateS_Obj.SendData(AttributeProfile)
    pprint.pprint(result)


#Define default Charger
print(CGRateS_Obj.SendData({"method":"APIerSv1.SetChargerProfile","params":[{"Tenant":"cgrates.org","ID":"DEFAULT","FilterIDs":[],"AttributeIDs":["*none"],"Weight":0}]}))

#Add an SMS Balance
print(CGRateS_Obj.SendData({"method":"ApierV1.SetBalance","params":[{"Tenant":"cgrates.org","Account":"Nick_Test_123","BalanceType":"*sms","Categories":"*any","Balance":{"ID":"SMS_Balance_1","Value":"100","Weight":25}}],"id":13}))

import uuid
import datetime
now = datetime.datetime.now()
#Generate a test CDR
result = CGRateS_Obj.SendData({
    "method": "CDRsV2.ProcessExternalCDR",
    "params": [
        {
            "OriginID": str(uuid.uuid1()),
            "ToR": "*sms",
            "RequestType": "*pseudoprepaid",
            "AnswerTime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "SetupTime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "Tenant": "cgrates.org",
            #This is going to be transformed to Nick_Test_123 by Attributes
            "Account": "12340003",
            "Usage": "1",
        }
    ]
})
pprint.pprint(result)
input("Enter to continue")



#Create a new Attribute for translating 0NSN and NSN from 612 to E164
SetAttributeProfile = {
    "method": "APIerSv2.SetAttributeProfile",
    "params": [{
        "Tenant": "cgrates.org",
        "ID": "ATTR_0NSN_to_E164_02_Area_Code",
        "Contexts": ["*any"],
        "FilterIDs": [
            "*string:~*req.Account:NickTest7"
        ],
        "Attributes": [
            {
            "FilterIDs": [],
            "Path": "*req.Subject",
            "Type": "*variable",
            "Value": "~*req.Subject:s/^0(\d{1})(\d{8})$/61${1}${2}/"
            },
            {
            "FilterIDs": [],
            "Path": "*req.Subject",
            "Type": "*variable",
            "Value": "~*req.Subject:s/^(\d{8})$/612${1}/"
            },
        ],
        "Blocker": False,
        "Weight": 10
    }],
}
result = CGRateS_Obj.SendData(SetAttributeProfile)
pprint.pprint(result)

#This is in 0NSN format, so it should be translated to E164
result = CGRateS_Obj.SendData({"method":"AttributeSv1.ProcessEvent",
                               "params":[
                                   {"Tenant":"cgrates.org",
                                    "Event":{"Account":"NickTest7", "Subject" : "0312341234"},
                                    "APIOpts":{"*processRuns":5,"*profileRuns":5,"*subsys":"*sessions"}
                                    }]})
pprint.pprint(result)

#This is in NSN format, which we want to translate to E164
result = CGRateS_Obj.SendData({"method":"AttributeSv1.ProcessEvent",
                               "params":[
                                   {"Tenant":"cgrates.org",
                                    "Event":{"Account":"NickTest7", "Subject" : "12341234"},
                                    "APIOpts":{"*processRuns":5,"*profileRuns":5,"*subsys":"*sessions"}
                                    }]})
pprint.pprint(result)



#Now let's imagine that 61212341234 has the Destination set to DST_Operator1 from our Destinations table
#But we know it's been ported to Operator2, so we rewrite the Destination to DST_Operator2
#Create a new Attribute for translating 0NSN and NSN from 612 to E164
SetAttributeProfile = {
    "method": "APIerSv2.SetAttributeProfile",
    "params": [{
        "Tenant": "cgrates.org",
        "ID": "ATTR_Ported_61212341234",
        "Contexts": ["*any"],
        "FilterIDs": [
            #"*string:~*req.Account:NickTest7",
            "*string:~*req.Subject:61212341234",
            #"*string:~*req.Destination:DST_Operator1"
            #"*prefix:~*req.Subject:612123412",
        ],
        "Attributes": [
            {
            "FilterIDs": [],
            "Path": "*req.Destination",
            "Type": "*constant",
            "Value": "DST_Operator2"
            },
        ],
        "Blocker": False,
        "Weight": 5
    }],
}
result = CGRateS_Obj.SendData(SetAttributeProfile)
pprint.pprint(result)

#This is in NSN format, which we want to translate to E164
result = CGRateS_Obj.SendData({"method":"AttributeSv1.ProcessEvent",
                               "params":[
                                   {"Tenant":"cgrates.org",
                                    "Event":{"Account":"NickTest7", "Subject" : "12341234"},
                                    "APIOpts":{"*processRuns":5,"*profileRuns":5,"*subsys":"*sessions"}
                                    }]})
pprint.pprint(result)
