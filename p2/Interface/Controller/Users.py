"""
 File: Users.py
 Authors: Leah Hadeed
          Nazariy Gunko

 Description:
 This script is in charge of user account manipulation on the SecureBox
 client server. The functions defined allow a user to register themselves
 with the system, search for another user, delete an ID, and get the public
 key of a user based on their ID.
"""

# Python Libraries
import json
import os
import sys

# Cryptographic Libraries
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Created Libraries
from .API.Relay import Relay
from .Colours import Colours

# This class is responsible for the manipulation of user related functions
class User:
    # Endings for the server URL. These can be changed as needed.
    Colours = None
    register     = 'register'
    searchId     = 'search'
    publickey = 'getPublicKey'
    delete       = 'delete'

    # Base URL for the user manipulation functions
    url = ''
    # Authorization for access to the server
    authorization = ''

    # Constructor for class
    def __init__(self, server, authorization):
        self.url = server + 'users/'
        self.authorization = authorization
        self.Colours = Colours()

    # Print ok stylized
    def print_ok(self, string):
        print(self.Colours.cyan('->') + string + self.Colours.green('OK'))


    # Creates a new identity (based on public and private key pairing) for a
    # given user with associated name and email (and in cases alias) and registers
    # the user to the SecureBox system to be found by other users
    def create_user(self, name, email, alias=None):

        # Generates key with size 2048bits
        key = RSA.generate(2048)

        # Creation of public key
        pKey = key.publickey().exportKey()
        # Creation of private key
        private_key = key.exportKey()

        # Creation of PEM file to store the private certificate
        file_out = open("private.pem", "wb")
        file_out.write(private_key)
        file_out.close()

        # Data setup for request (JSON)
        data = {
            'nombre' : name,
            'email' : email,
            'publicKey' : pKey.decode('ascii'),
            'alias' : alias
        }

        # Determines the final url of the request
        finalUrl = self.url + self.register

        # Creates the request communicator
        request = Relay(data, finalUrl, self.authorization, False)

        # Calls function from REST API that communicates with the server.
        return request.securebox_send()


    # Finds a user whose name or email contains the given search query on the
    # SecureBox Identity Repository and returns the ID of that user.
    def search_id(self, cadena):

        # Data setup for request (JSON)
        args = {'data_search': cadena}
        # Calls function from REST API that communicates with the server.

        # Determines the final url of the request
        finalUrl = self.url + self.searchId

        # Creates the request communicator
        request = Relay(args, finalUrl, self.authorization, False)

        # Calls function from REST API that communicates with the server.
        return request.securebox_send()


    # This method receives a User ID and searches for the corresponding
    # Public Key of that user. If none can be found, it returns error.
    def getPublicKey(self, uid):

        # Sets the arguments for the HTTP request
        args = {'userID': uid}

        # Determines the final url of the request
        finalUrl = self.url + self.publickey

        # Creates the request communicator
        request = Relay(args, finalUrl, self.authorization, False)

        # Calls function from REST API that communicates with the server.
        response = request.securebox_send()

        # If operation succeeds
        if response.status_code == 200:
            # This print is done here to allow for intermediate process check
            self.print_ok(' Recovering public key of ID #' + self.Colours.magenta(uid) + '...')
        # Case: request failure
        else:
            # Print error to terminal
            print('Error Code: ' + self.Colours.red(response.json()['error_code']) + ' Description: ' + response.json()['description'])

        # Returns the response to the main terminal
        return response


    # Deletes the identity with the given ID registered in the system.
    # Only IDs created by the user calling this function can be deleted.
    def delete_id(self, uid):

        # Sets the arguments for the HTTP request
        args = {'userID': uid}

        # Determines the final url of the request
        finalUrl = self.url + self.delete

        # Create the request communicator
        request = Relay(args, finalUrl, self.authorization, False)

        # Calls function from REST API that communicates with the server.
        return request.securebox_send()
