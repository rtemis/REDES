""" 
 File: Relay.py
 Authors: Leah Hadeed
          Nazariy Gunko

 Description:

 This script is in charge of communications between the server and the 
 command line interface. The class 'Relay' creates the appropriate headers
 for the HTTP Request and sends the data through POST to the SecureBox 
 Server for processing. It then returns the response in JSON format.
"""

# Python Libraries
import requests
import os
import json 

# This class is in charge of relaying the information to the server 
class Relay:
    data = None 
    url = ''
    authorization = ''
    uflag = False

    def __init__(self, data, url, authorization, uflag):
        self.data = data
        self.url = url 
        self.authorization = authorization
        self.uflag = uflag 

    # This method communicates with the SecureBox server
    def securebox_send(self):
        
        # Case: Upload True 
        if self.uflag == True:
             # Set headers for HTTP request
            headers = {
                'authorization' : 'Bearer ' + self.authorization
            }
            # For Upload, which requires files instead of json arguments
            r = requests.post(self.url, headers=headers, files=self.data)

        # Case: Upload False 
        else: 
            # Send request to server
            if self.data ==  None:
                # Header setup for request (JSON)
                headers = {
                    'authorization' : 'Bearer ' + self.authorization
                }
                # For commands that don't require JSON data transfer
                r = requests.post(self.url, headers=headers)
            else: 
                # Header setup for request (JSON)
                headers = {
                    'content-type' : 'application/json',
                    'content-length' : str(len(str(self.data))),
                    'authorization' : 'Bearer ' + self.authorization
                }
                # For commands that require supplementary arguments
                r = requests.post(self.url, headers=headers, json=self.data)
                #Send response to user interface
        return r 
