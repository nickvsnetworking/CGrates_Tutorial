##CGrateS Python Library
import requests
import json
import pprint
from collections import OrderedDict
import logging
#https://pkg.go.dev/github.com/cgrates/cgrates@v0.10.2/apier/v2

class CGRateS:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        print("Initializing with host " + str(self.host) + " on port " + str(self.port))
        self.SendData({'method':'ApierV2.Ping','params':[{'Tenant':'cgrates.org'}]})

    
    def SendData(self, json):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        print("Sending Request with Body:")
        print(json)
        r = requests.post("http://" + str(self.host) + ":" + str(self.port) + "/jsonrpc", json=json, headers=headers)
        if r.status_code != 200:
            print("Got error code " + str(r.status_code) + " back")
            raise
        try:
            json_out = r.json(object_pairs_hook=OrderedDict)
            return json_out
        except:
            print("Could not decode JSON out of " + str(r.raw))
            raise ValueError("Could not decode JSON output")
