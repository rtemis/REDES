# practica3

This is the third and final project for the practical course: REDES II.  The idea behind this project was the relay of multimedia between two entities through the use of sockets. The basic outline of the project is described in the diagram below:

### Project Diagram
![Diagram](https://moodle.uam.es/pluginfile.php/1951839/mod_book/chapter/3829/Diagrama_practica3%20-%20Page%201.png)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Before deployment, you need to install the software:
* [Python 3](https://www.python.org/download/releases/3.0/)

It is also necessary to execute the following commands:
```
sudo apt install python-opencv

pip3 install opencv-python

sudo apt install python3-pil.imagetk python3-tk python3-numpy python-imaging-tk
```

*Note: The installation instructions for the aforementioned software is located in the link provided.*

### Installing

The actual application need not be installed because it is compiled in the moment of execution.

*Note: Assure that there is an __init__.py file in each folder.*


### Deployment

In the event of changing servers, the only modification needed for the application to function correctly is to replace the server variable in the Interface class located in Interface.py (as seen below):

```
# Main VideoClient application class
class VideoClient(object):
	# User variables
	nickname = ""
	password = ""
	port = 5000             # Change this 
	recPort = 6000          # Change this 
	ip = "172.17.60.60"     # Change this
	version = "V0"
```

## Use

This program is run directly through the terminal using the command: 
```
python3 video_client.py
```

*More instructions on use are available in the [Use](https://vega.ii.uam.es/2311-10-19/practica3/wikis/use) section of the Wiki*

## Authors

* **Leah Hadeed** - *leah.hadeed@estudiante.uam.es*
* **Nazary Gunko** - *nazariy.gunko@estudiante.uam.es*

## Acknowledgments

* **Subject Professors:** Carlos Garcia, Oscar Delgado

* **Resources:**
 - [Python Request Documentation](http://docs.python-requests.org/en/master/)
 - [OpenCV](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html)