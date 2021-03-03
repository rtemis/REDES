"""
Author: Leah Hadeed

This script allows you to send an options header through to the server socket.
"""

import socket
import os
 
dirpath = os.getcwd()
print("current directory is : " + dirpath)
foldername = os.path.basename(dirpath)
print("Directory name is : " + foldername)

f = open(dirpath + '/server.conf', 'r')

scriptDir = ""
serverPort = 0

for line in f:
    if 'server_root' in line:
        scriptDir = '/' + (line.split("server_root = "))[1]
        scriptDir = scriptDir.split(' \n')[0] + '/'
        print(scriptDir) 
    if 'listen_port' in line:
        serverPort = int(line.split("listen_port = ")[1].split(' \n')[0])
        print(serverPort)

f.close()

serverName = '127.0.0.1'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((serverName,serverPort))
    
client_socket.send("OPTIONS /index.html HTTP/1.1")
modifiedSentence = client_socket.recv(1024)
print('Desde el servidor:\n')
print(modifiedSentence)

client_socket.close()

