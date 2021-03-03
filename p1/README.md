# practica1

This is the first project for the practical course: REDES II.  The idea behind this project was the creation of an HTTP web server.
This specific server responds to concurrent requests through the use of a thread pool.  

The functionality is limited to support the commands:
* GET
* POST
* OPTIONS

The server is configured through the [server configuration](https://vega.ii.uam.es/2311-10-19/practica1/server.conf) file located in the project.

The server also gives support to script execution.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Before deployment, you need to install the software:
	 [Libconfuse](https://github.com/martinh/libconfuse)

The installation instructions are located in the [README.md](https://github.com/martinh/libconfuse/blob/master/README.md) file located in the link.

Once downloaded and installed, you must export the code to the current terminal using the following commands:

```
	export LD_LIBRARY_PATH=/usr/local/lib/
	export PATH=$HOME/local/bin:$PATH
```
This allows the open terminal to access the libconfuse library.

### Installing

Before you begin, you must execute the command:
```
make folders
```
This command creates the missing folders:
* - obj/
* - lib/

For direct installation, from the main project folder, use the command:
```
make
```
The actual code behind this command directly executes these commands:
```
all: clean static objects $(EXE) clear
```
Which erases the previous project data, creates the static libraries, creates the objects, creates the executables, and finally clears the object files.

*Note: Static libraries need not be repeatedly recompiled. In the case of recompilation, use the command:*
```
make no-static
```

_Step by step installation_

To install the system, first, compile the static libraries using the command:
```
make static
````
The libraries created by this command are libpicohttpparser.a [see documentation here](https://github.com/h2o/picohttpparser) and librequests.a


Then, to create the .obj files, use the command:
```
make objects
```

The server is now ready to be deployed!


## Deployment

To deploy the system, first configure the [server configuration script](https://vega.ii.uam.es/2311-10-19/practica1/server.conf).

Example:
```
server_root = htmlfiles/www
max_clients = 10
listen_port = 8080
server_signature = Practica1

```
*Note:* The server signature should be free of spaces.
*Note:* The server root should contain a folder 'htmlfiles/www'

Next, execute the command:

```
make run
```

For memory check, execute the following command:
```
make runv
```

To end close the web server, execute the following command: 
```
make rune
```
*Note: This command runs the exit program that terminates the server process.*

## Authors

* **Leah Hadeed** - *leah.hadeed@estudiante.uam.es*
* **Nazary Gunko** - *nazariy.gunko@estudiante.uam.es*

## Acknowledgments

* **Subject Professors:** Carlos Garcia, Oscar Delgado

* **Online Resources:**
* - [HTTP basics](https://www.ntu.edu.sg/home/ehchua/programming/webprogramming/HTTP_Basics.html)
* - [Stevens, W. Richard - Unix Network Programming, ch 30](https://proquest.safaribooksonline.com/book/programming/unix/0131411551/advanced-sockets/ch30#X2ludGVybmFsX0h0bWxWaWV3P3htbGlkPTAtMTMtMTQxMTU1LTElMkZjaDMwJnF1ZXJ5PQ==)
* - [How to create a README.md](https://gist.github.com/PurpleBooth)


* **Libraries Used:**
* - [PicoHTTPParser](https://github.com/h2o/picohttpparser)
* - [Libconfuse](https://github.com/martinh/libconfuse)
