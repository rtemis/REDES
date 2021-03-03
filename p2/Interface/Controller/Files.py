"""
 File: Files.py
 Authors: Leah Hadeed
          Nazariy Gunko

 Description:
 This script is in charge of file manipulation within the SecureBox client.
 The functions defined allow a user to upload, download, view and delete
 files.
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
from .Encrypter.Encryption import Encryption

from .Colours import Colours

# This class is responsible for the file manipulation related functions
class Files:
    # Attachments for the server URL. These can be changed as needed.
    uploadURL   = 'upload'
    downloadURL = 'download'
    listFiles   = 'list'
    deleteURL   = 'delete'

    # Base URL for the user manipulation functions
    url = ''
    # Authorization for access to the server
    authorization = ''
    # Encryption code
    encrypt = None
    colour = None

    # Constructor for class
    def __init__(self, server, authorization):
        self.url = server + 'files/'
        self.authorization = authorization
        self.encrypt = Encryption(authorization)
        self.colour = Colours()

    # Print ok stylized
    def print_ok(self, string):
        print(self.colour.cyan('->') + string + self.colour.green('OK'))


    # Sends a file to another user, whose ID is specified by the option --dest_id.
    # The file is uploaded to SecureBox, signed and encrypted with the appropriate
    # keys so that the file can be recovered and verified by the receiver.
    def upload(self, filename, userpk):
        # Sign and Encrypt File
        self.encrypt.sign_encrypt(filename, userpk)

        # Set arguments for the file transfer
        args = { 'ufile' : open(filename, 'rb')}

        # Determines the final url of the request
        finalUrl = self.url + self.uploadURL

        # Creates the request communicator
        request = Relay(args, finalUrl, self.authorization, True)

        # Calls function from REST API that communicates with the server.
        return request.securebox_send()


    # List files on server that belong to a specific user
    def list(self):
        # Determines the final url of the request
        finalUrl = self.url + self.listFiles

        # Creates the request communicator
        request = Relay(None, finalUrl, self.authorization, False)

        # Calls function from REST API that communicates with the server.
        return request.securebox_send()

    # Download a file from server with the ID from the system (generated in upload
    # and communicated to receiver). After download is completed, the signature is
    # verified and the content is decrypted.
    def download(self, fileid):

        args = { 'file_id': fileid }

        # Determines the final url of the request
        finalUrl = self.url + self.downloadURL

        # Creates the request communicator
        request = Relay(args, finalUrl, self.authorization, False)

        # Calls function from REST API that communicates with the server.
        response = request.securebox_send()

        # Case: request success
        if response.status_code == 200:
            # Retrieve filename
            filename = response.headers['Content-Disposition'].split('"')
            
            # Create file to dump text to.
            file = open(filename[1], 'wb+')

            # Dumps response text to file
            file.write(response.content)
            # Alert user that file has been downloaded
            self.print_ok(' File ' + self.colour.yellow(fileid) + ' download...')
            # Returns the response value
            return str(filename[1])
        # Case: FILE2 error
        else:
            # Print error to terminal
            print('Error Code: ' + self.colour.red(response.json()['error_code']) + ' Description: ' + response.json()['description'])
            # Return error
            return None

    # Delete a file from server
    def delete(self, fileid):

        args = { 'file_id': fileid }

        # Determines the final url of the request
        finalUrl = self.url + self.deleteURL

        # Creates the request communicator
        request = Relay(args, finalUrl, self.authorization, False)

        # Calls function from REST API that communicates with the server.
        return request.securebox_send()
