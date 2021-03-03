"""
 File: Interface.py
 Authors: Leah Hadeed
          Nazariy Gunko

 Description:
 This script is in charge of communicating directly with the user
 through the terminal. This class collects the information passed
 through the command line and then prints the responses to the screen.

"""

# Python Libraries
import json
import os
import sys

from .Controller.Users import User
from .Controller.Files import Files
from .Controller.Colours import Colours


# Class in charge of displaying messages to the terminal
class Interface:
    # Interface variables
    colour = None

    # SecureBox Variables
    server = 'http://vega.ii.uam.es:8080/api/'
    authorization = ''

    # Object Variables
    users = None
    files = None

    # Constructor
    def __init__(self, authorization):
        self.users = User(self.server, authorization)
        self.files = Files(self.server, authorization)
        self.colour = Colours()

    # Print error stylized
    def print_arg_error(self, string):
        print(self.colour.red('Structure Error: ') + "python3 securebox_client.py " + string)

    # Print ok stylized
    def print_ok(self, string):
        print(self.colour.cyan('->') + string + self.colour.green('OK'))

    # Interface main code
    def start_interface(self, args):

        # Case: Creating a user
        if args.create_id != None:
            # Error control: parameters
            if len(args.create_id) < 2:
                self.print_arg_error(self.colour.magenta('--create_id <name> <email>') + ' OPTIONAL ' + self.colour.magenta('<alias>'))

            else:
                # Case: Alias excluded
                if len(args.create_id) == 2:
                    response = self.users.create_user(args.create_id[0],args.create_id[1])
                # Case: Alias included
                else:
                    response = self.users.create_user(args.create_id[0],args.create_id[1],args.create_id[2])

                # Printing response if no errors found.
                if response.status_code == 200:
                    # Collect JSON response data
                    r = response.json()
                    # Print success
                    self.print_ok(self.colour.green('Success!') + ' User ' + str(r['nombre']) + ' created. timestamp: ' + str(r['ts']) + ' ')
                else:
                    print('Error Code: ' + self.colour.red(r['error_code']) + ' Description: ' + r['description'])

        # Case: Searching for user on server
        elif args.search_id != None:
            # Error control: parameters
            if (len(args.search_id) < 1):
                self.print_arg_error(self.colour.magenta('--search_id <criteria>'))

            else:
                # User feedback
                self.print_ok(' Searching for user named \'' +  self.colour.yellow(str(args.search_id[0])) + '\'...')
                # Search for user
                response = self.users.search_id(args.search_id[0])

                # Printing response to terminal
                if response.status_code == 200:
                    # Collect JSON response data
                    r = response.json()
                    # User feedback
                    print(str(len(r)) + ' users found with criteria: ' + self.colour.magenta(args.search_id[0]))

                    # Loop for printing users
                    i = 1
                    for x in r:
                        print('[' + self.colour.cyan(str(i)) + '] ' + str(x['nombre']) + ', ' + self.colour.yellow(str(x['email'])) + ', ID: ' + self.colour.green(str(x['userID'])))
                        i += 1
                # Case: Error with request
                else:
                    print('Error Code: ' + self.colour.red(r['error_code']) + ' Description: ' + r['description'])

        # Case: Deleting user
        elif args.delete_id != None:
            # Delete user
            response = self.users.delete_id(args.delete_id[0])
            # Test for errors
            if response.status_code == 200:
                # Collect JSON response data
                r = response.json()
                # Print response to terminal
                self.print_ok(' User with ID#' + self.colour.green(r['userID']) + ' deleted correctly.')

        # Case: Uploading file to server
        elif args.upload != None:
            # Case: incomplete arguments
            if args.dest_id == None:
                # Print error to terminal
                self.print_arg_error(self.colour.magenta('--upload <filename> --dest_id <user_id>'))
            # Case: correct arguments
            else:
                # Get public key of user
                response = self.users.getPublicKey(args.dest_id[0])
                # Case: request success
                if response.status_code == 200:
                    # Save public key
                    publicKey = response.json()['publicKey']
                    # Upload file to user repository
                    response = self.files.upload(args.upload[0], publicKey)
                # Case: request error
                else:
                    # Print error to terminal
                    print('Error Code: ' + self.colour.red(response.json()['error_code']) + ' Description: ' + response.json()['description'])

        # Case: Downloading file from server
        elif args.download != None:
            # Case: incomplete arguments
            if args.source_id == None:
                # Print error to terminal
                self.print_arg_error(self.colour.magenta('--download <file> --source_id <userid>'))
            # Case: correct arguments
            else:
                # Download file from user repository
                response = self.files.download(args.download[0])
                # Test for error
                if response != None:
                    res = self.users.getPublicKey(args.source_id[0])
                    if res.status_code == 200:
                        # Save public key
                        publicKey = res.json()['publicKey']
                        # Begnin file decryption
                        self.files.encrypt.decryptFile(response, publicKey, True)
                        # Print success.
                        self.print_ok(' File decryption...')

        # Case: Deleting file from server
        elif args.delete_file != None:
            # Error control: parameters
            if (len(args.delete_file) < 1):
                self.print_arg_error(self.colour.magenta('--delete_file <fileid>'))
            else:
                # Delete file from user repository
                response = self.files.delete(args.delete_file[0])
                # Case: request success
                if response.status_code == 200:
                    # Collect request JSON data
                    r = response.json()
                    # Print response to terminal
                    self.print_ok(' File ' + self.colour.yellow(r['file_id']) + ' deletion...')
                # Case: request failure
                else:
                    # Print error to terminal
                    print('Error Code: ' + self.colour.red(response.json()['error_code']) + ' Description: ' + response.json()['description'])

        # Case: Listing files pertaining to current user
        elif args.list_files != None:
            # List files in user repository
            response = self.files.list()
            # Test for error
            if response.status_code == 200:
                # Collect JSON response data
                r = response.json()

                # Case: no files found for current user
                if r['num_files'] < 1:
                    print('No files found belonging to current user.')
                else:
                    # User feedback
                    print(str(r['num_files']) + ' files found beloning to current user:')

                    # Loop for printing files
                    i = 1
                    for x in r['files_list']:
                        print('[' + self.colour.cyan(str(i)) + '] ' + str(x))
                        i += 1
