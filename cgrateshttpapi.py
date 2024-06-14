import requests
import json
from collections import OrderedDict

class CGRateS:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.session = requests.Session()
        self.session.headers.update({'Content-type': 'application/json', 'Accept': 'text/plain'})
        print("Initializing with host " + str(self.host) + " on port " + str(self.port))
        self.SendData({'method': 'ApierV2.Ping', 'params': [{'Tenant': 'cgrates.org'}]})

    def SendData(self, data):
        url = "http://" + str(self.host) + ":" + str(self.port) + "/jsonrpc"
        print("Sending Request with Body:")
        print(data)
        response = self.session.post(url, json=data)
        
        if response.status_code != 200:
            print("Got error code " + str(response.status_code) + " back")
            raise requests.exceptions.HTTPError(response.status_code, response.text)

        try:
            json_out = json.loads(response.text)
            return json_out
        except json.JSONDecodeError:
            print("Could not decode JSON out of " + str(response.content))
            raise ValueError("Could not decode JSON output")
