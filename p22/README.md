# practica2

This is the second project for the practical course: REDES II.  The idea behind this project was the relay of information with a server through interactions with the terminal.

This application supports the following commands:
* --create_id
* --search_id
* --delete_id
* --upload
* --source_id
* --dest_id
* --download
* --list_files
* --delete_file


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Before deployment, you need to install the software:
* [Python 3](https://www.python.org/download/releases/3.0/)

* [PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/src/installation.html)

* [Python Requests](http://docs.python-requests.org/en/master/user/install/#install)

An alternative to the PyCryptodome link is to execute the following commands:
```
pip3 install PyCryptodome
```

*Note: The installation instructions for the aforementioned software is located in the link provided.*

### Installing

The actual application need not be installed because it is compiled in the moment of execution.

*Note: Assure that there is an __init__.py file in each folder.*


### Deployment

In the event of changing servers, the only modification needed for the application to function correctly is to replace the server variable in the Interface class located in Interface.py (as seen below):
```
# Class in charge of displaying messages to the terminal 
class Interface:
    # Interface variables
    colour = None

    # SecureBox Variables
    server = 'http://vega.ii.uam.es:8080/api/'
```

## Use

This program is run directly through the terminal. 

Each action is prefaced with the command: 
```
python securebox_client.py 
```

The commands available allow for:

* User creation: A name, email, and alias are passed to the program through the command line interface and the program sends the data to the server to save the new user data. *Any new user overwrites the pre-existing user.* 

* User deletion: An ID is passed to the program through the command line interface and the program sends the data to the server and erases the account associated to the ID from the system database. *Only an ID belonging to the current user can be deleted.*

* User search: A character string is passed to the program through the command line interface and the program sends the data to the server and returns any users whose data contains the searched string via terminal. 

* File upload: The filename and destination ID are passed to the program through the command line interface and the program sends the data to the server and returns a confirmation that the file has been signed, encrypted, and uploaded successfully. *The processes of signing and encrypting are done behind the scenes.*

* File download: The file ID and the source ID are passed to the program through the command line interface and the program sends the data to the server and, if successful, download the file and processes it, decrypting it and verifying the signature. *If either process fails, an error is returned.*

* File deletion: The file ID is passed to the program through the command line interface and the program sends the data to the server. Upon completion, the file is moved from the current user's file database 
on the server. *Note, only files owned by the user can be deleted.*

* List files: This command requires no arguments. An HTTP request is sent upon calling this function and returns a list of all the files belonging to the current user. 

### Command Line Arguments

When using the command line, arguments with spaces must be encapsulated by apostrophes. For example:
```
python securebox_client.py --create_id 'John Doe' john_doe@abc.com johnnie
```

Command examples:
* Create ID
```
python securebox_client.py --create_id <full_name> <email> <alias>
```
* Search ID
```
python securebox_client.py --search_id <search_text>
```
* Delete ID 
```
python securebox_client.py --delete_id <user_id>
```
* Upload File
```
python securebox_client.py --upload <filename> --dest_id <user_id>
```
* Download File
```
python securebox_client.py --download <file_id> --source_id <user_id>
```
* Delete File
```
python securebox_client.py --delete_file <file_id>
```

## Authors

* **Leah Hadeed** - *leah.hadeed@estudiante.uam.es*
* **Nazary Gunko** - *nazariy.gunko@estudiante.uam.es*

## Acknowledgments

* **Subject Professors:** Carlos Garcia, Oscar Delgado

* **Resources:**
* - [Python Request Documentation](http://docs.python-requests.org/en/master/)
* - [Project Description](https://moodle.uam.es/mod/book/tool/print/index.php?id=1066001)
* - [Argparse Documentation](https://docs.python.org/3/library/argparse.html)

* **Libraries Used:**
* - [PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/src/installation.html)
* - [Python Requests](http://docs.python-requests.org/en/master/user/install/#install)
