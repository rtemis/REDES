"""
File: controller.py
Authors: Leah Hadeed Sanguinette
         Nazariy Gunko

This class is responsible for socket server communications.

The commands recognized by the server are:
    - REGISTER
    - QUERY
    - LIST_USERS
    - QUIT
"""

# Python Libraries
import socket

# This class controls client/server communications
class Controller:
    # IP for server https://vega.ii.uam.es/
    serverName = '150.244.59.230'
    serverPort = 8000
    client_socket = None

    # Constructor
    def __init__(self):
        # Create socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect socket to server through given port
        self.client_socket.connect((self.serverName,self.serverPort))


    # Method responsible for sending to and receiving messages from server
    def interact(self, sentence):
        # Sends request to server
        self.client_socket.send(bytearray(sentence, 'utf-8'))

        # Receives response from server
        response = self.client_socket.recv(8192).decode('utf-8')

        modifiedSentence = ""
        # Socket read loop
        while response != None:
            # Concatenate the response to the return variable
            modifiedSentence += response
            # Test size of sent data
            if len(response.encode('utf-8')) < 4096:
                # Leave loop if data transmission finished
                response = None
                break
            else:
                # Collect new response
                response = self.client_socket.recv(4096).decode('utf-8')

        # Case: list users has extra data in response that needs to be taken out
        if 'LIST_USERS' in sentence:
            # Returns the parsed version of user information
            return modifiedSentence.split('#')
        # Returns the string parsed with spaces
        return modifiedSentence.split(' ')

    # Method responsible for registering the user with the server database
    def register(self, nickname, ip, port, password, protocol):
        # Create the 'HTTP Request' structure
        sentence = "REGISTER " + nickname + " " + ip + " " + port + " " + password + " " + protocol
        # Calls server with the command sentence
        split = self.interact(sentence)

        # Case: Server response is OK
        if split[0] == 'OK':
            # Creates a dictionary with user information
            _dict = {
                'response'  : split[0],
                'command'   : split[1],
                'user'      : split[2],
                'ts'        : split[3]
            }
        # Case: Error server response
        else:
            # Creates a dictionary with error information
            _dict = {
                'response': split[0],
                'error'   : split[1]
            }
        # Returns dictionary to main function
        return _dict

    # Method responsible for collecting the information of a specific user through their username
    def query(self, name):
        if name is None:
            return
        # Creates the 'HTTP Request' structure
        sentence = "QUERY " + name
        # Calls server with the command sentence
        split = self.interact(sentence)

        # Case: Server response is OK
        if split[0] == 'OK':
            # Creates a dictionary with user information
            _dict = {
                'response'  : split[0],
                'command'   : split[1],
                'user'      : split[2],
                'ip'        : split[3],
                'port'      : split[4],
                'version'   : split[5]
            }
        # Case: Error server response
        else:
            # Creates a dictionary with the error information
            _dict = {
                'response': split[0],
                'error'   : split[1]
            }
        # Returns dictionary to main function
        return _dict

    # Method responsible for listing all available users in server database
    def list_users(self):
        # Creates the 'HTTP Request' structure
        sentence = "LIST_USERS"
        # Calls server with the command sentence
        split = self.interact(sentence)
        # Case: Server response OK
        if 'OK' in split[0]:
            # Creates dictionary with user information
            users = []
            x = split[0].split()
            _dict = {
                'user'      : x[3],
                'ip'        : x[4],
                'port'      : x[5],
                'timestamp' : x[6]
            }

            # Adds first user to dictionary
            users.append(_dict)

            # Creates separate dictionaries for each user
            for user in split[1:-1]:
                x = user.split(' ')
                if len(x) == 4:
                    _dict = {
                        'user'      : x[0],
                        'ip'        : x[1],
                        'port'      : x[2],
                        'timestamp' : x[3]
                    }
                    # Appends user dictionary to user list
                    users.append(_dict)
            # Return list of users
            return users
        # Case: Server error response
        else:
            # Creates dictionary with error information
            _dict = {
                'response': split[0],
                'error'   : split[1]
            }
        # Return error dictionary
        return _dict

    # Method responsible for closing the connection with server
    def quit(self):
        # Creates the 'HTTP Request' structure
        sentence = "QUIT"
        # Calls the server with the command sentence
        resp = self.interact(sentence)
        # Closes socket
        self.client_socket.close()
        # Returns server response
        return resp
