"""
 File: Parser.py
 Authors: Leah Hadeed
          Nazariy Gunko

 Description:
 This script is in charge of parsing the command line arguments
 and returning the arguments to the main interface function.

"""

# Python Libraries
import argparse

from Interface import Interface

# This class has no arguments because it is used solely to parse terminal arguments
class securebox_client:
    parser = None
    args = None
    interface = None

    def __init__(self, authorization):
        # Initialization of interface
        self.interface = Interface(authorization)

        # Definition / Initialization of argument parser
        self.parser = argparse.ArgumentParser(description='Connection to SecureBox Server.')

        # Command for creation of new IDs
        self.parser.add_argument(
            '--create_id',
            metavar=('Name'),
            nargs='+',
            help='Creation of new user.'
        )

        # Command for searching database based on a specific string set
        self.parser.add_argument(
            '--search_id',
            nargs=1,
            metavar='String',
            help='Search for a user based on a given string.'
        )

        # Command for deletion of a given ID
        self.parser.add_argument(
            '--delete_id',
            nargs=1,
            metavar='User ID',
            help='Delete the user associated with the given ID.'
        )

        # Command for uploading a file to server
        self.parser.add_argument(
            '--upload',
            metavar='FILE',
            nargs=1,
            help='Upload a file to the server.'
        )

        # Command for including file destination on server
        self.parser.add_argument(
            '--dest_id',
            metavar='User ID',
            nargs=1,
            help='Choose the destination of file on server.'
        )

        # Command for including file origin on server
        self.parser.add_argument(
            '--source_id',
            metavar='User ID',
            nargs=1,
            help='Choose the location of file on server.'
        )

        # Command for download of file from server
        self.parser.add_argument(
            '--download',
            nargs=1,
            metavar='File ID',
            help='Download the file associated with the given ID.'
        )

        # Command for listing of all files available to current user
        self.parser.add_argument(
            '--list_files',
            action='store_true',
            help='Lists all the files available to the current user.'
        )

        # Command for delete file from server
        self.parser.add_argument(
            '--delete_file',
            nargs=1,
            metavar='File ID',
            help='Delete the file associated with the given ID.'
        )

        # Return the parsed arguments to the main interface
        self.args = self.parser.parse_args()

        # Begin interface
        self.interface.start_interface(self.args)

#p = securebox_client('AcfE6259eb7F40B8')
p = securebox_client('1F6CBe9a2fc3ADdE')
