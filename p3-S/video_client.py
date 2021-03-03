"""
Authors: Subject Professors
		 		 Leah Hadeed 
         Nazariy Gunko

This class is responsible for displaying the application.
"""

# import libraries
from appJar import gui
from PIL 	import Image, ImageTk

import numpy as np
import cv2
import threading
import socket
import time
import collections

import controller
import windowCreator 

# Main VideoClient application class
class VideoClient(object):
	# User variables
	nickname = ""
	password = ""
	port = 5000
	recPort = 6000
	ip = "127.0.0.1"
	version = "V0"

	# Class variables
	controller = None
	search = None
	windowCreator = None

	# Busy flag
	busy = False
	# paused flag
	paused = False
	# Connected TCP socket
	connection = None
	# Connected UDP socket
	receiveUDP = None
	# TCP server socket
	serverTCP = None
	# TCP client socket
	clientTCP = None
	# UDP server socket
	sendUDP = None

	# Threads
	send_thread = None
	receive_thread = None 
	# Sizes
	recSize = 65536
	comSize = 1024

	# Buffer of received packets
	receiveBuffer = None
	# Pointer to received packets
	recPointer = 0
	# Pointer to reproduced packets
	repPointer = 0

	# Timestamp
	frame_timestamp = 0
	# Timestamp of the last received frame
	last_recv_timestamp = 0
	# Delay between recieved frames
	delay = 0
	# Status bar objects 
	timestamp = 0
	fps = 20
	res = ""
	duration = 0
	startTime = 0

	# Flag to know if the current client started the call
	caller = False
	# Current frame to be sent
	current_frame = None

	# Variables for socket responses
	CALL_BUSY 		= "CALL_BUSY"
	CALL_ACCEPTED = "CALL_ACCEPTED"
	CALL_DENIED 	= "CALL_DENIED"

	# Variables for resolution
	LOW		 = "160x120"
	MEDIUM = "320x240"
	HIGH 	 = "640x480"


	# Constructor for application
	def __init__(self, window_size):
		# Create local GUI variable
		self.app = gui("Redes2 - P2P", window_size)
		self.app.setIcon("imgs/webcam.gif")

		# Set padding for application
		self.app.setGuiPadding(10,10)

		# Add toolbar above image window
		self.app.addToolbar(["EXIT", "REGISTER", "SEARCH", "ADDRESS-BOOK", "TELEPHONE"], self.toolbar, findIcon=True)

		# Set the background colour for the application
		self.app.setBg("SlateGray")
		self.app.setToolbarButtonDisabled("SEARCH")
		self.app.setToolbarButtonDisabled("ADDRESS-BOOK")
		self.app.setToolbarButtonDisabled("TELEPHONE")

		# Prepare interface
		self.app.addLabel("title", "Cliente Multimedia P2P - Redes2 ")
		self.app.addImage("video", "imgs/webcam.gif")

		# Register video capture function
		self.cap = cv2.VideoCapture("imgs/webcam.gif")
		self.app.setPollTime(self.fps)
		self.app.registerEvent(self.capturaVideo)
		self.app.registerEvent(self.videoStatus)

		# Create server communications controller
		self.controller = controller.Controller()
		
		# Window creator initialization
		self.windowCreator = windowCreator.windowCreator(self.app, self.register, self.recPort, self.call)

		# Set up receive buffer for reproduction
		self.receiveBuffer = list()

	# Start application function
	def start(self):
		self.app.go()

	
	# Register method communicates user registration with vega server
	def register(self, btn):
		# If the button pressed was submit
		if btn == "Submit":
			# Add information to local user
			self.nickname = self.app.getEntry("userEnt")
			self.password = self.app.getEntry("passEnt")
			# Call register method in server controller
			resp = self.controller.register(self.nickname, self.ip, str(self.port), self.password, self.version)
			# Create response subwindow
			self.windowCreator.registerWindow(resp)

		# Hide pop-up window
		self.app.hideSubWindow("Registrarse")

	
	# Call control function
	def call(self, btn):
		# If the button pressed was pause
		if btn == "PAUSE":
			# Pause the call
			self.app.infoBox("Paused","Call Paused")
			self.paused = True
			# Free the buffer
			self.receiveBuffer.clear()
			# Pause video sending
			self.clientTCP.send(bytearray("CALL_HOLD " + self.nickname, 'utf-8'))

		# If the button pressed was resume
		if btn == "RESUME":
			# Resume the call
			self.app.infoBox("Resumed","Call Resumed")
			self.paused = False

			# Test for main caller
			if self.caller == True:
				self.clientTCP.send(bytearray("CALL_RESUME " + self.nickname, 'utf-8'))
			else:
				self.connection.send(bytearray("CALL_RESUME " + self.nickname, 'utf-8'))

		# If the button pressed was end
		if btn == "END":
			# End the call
			self.app.infoBox("Ended","Call Ended")
			self.busy = False
			# Free the buffer
			self.receiveBuffer.clear()

			if self.caller == True:
				self.clientTCP.send(bytearray("CALL_END " + self.nickname, 'utf-8'))
				self.caller = False
			else:
				self.connection.send(bytearray("CALL_END " + self.nickname, 'utf-8'))
		# Hide pop-up window
		self.app.hideSubWindow("Call-Port-"+str(self.recPort))


	# Method called by the toolbar buttons
	def toolbar(self, btn):
		# Case: Exit button pressed
		if btn == "EXIT":
			# Quit server connections
			msg = self.controller.quit()
			# Print exit message
			self.app.infoBox("Exit", "Closing server.\n" + msg[0])
			# Stop application
			self.app.stop()
		# Case: Register button pressed
		elif btn == "REGISTER":
			# Open login pop-up window
			self.app.showSubWindow("Registrarse")

		# Case: Search button pressed
		elif btn == "SEARCH":
			# Collect nickname of user to connect to
			search = self.app.textBox("Conexion", "Introduce el nick del usuario a buscar")

			if search != None:
				# Collect response from server search
				result = self.controller.query(search)

				# Creation of search window
				self.windowCreator.userSearch(result, search)

				# Open pop-up with search results
				self.app.showSubWindow("User-Search")

		elif btn == "ADDRESS-BOOK":
			# Call server list users method
			result = self.controller.list_users()

			# Creation of address book
			self.windowCreator.addressBook(result)

			# Show address book window
			self.app.showSubWindow("Address Book")


		elif btn == "TELEPHONE":
			# Collect desired contact user
			nick = self.app.textBox("Call Query", "Which user would you like to call?")
			# Collect server data
			user = self.controller.query(nick)

			# Test for user existence
			if user['response'] == 'OK':
				# Add user to list of connections
				self.app.infoBox("Conexion", "Calling user..." + user['user'])
				address = (user['ip'], int(user['port']))
				# Connect to the users app
				try:
					self.clientTCP.connect(address)
					# Try to start call
					self.clientTCP.send(bytearray("CALLING " + self.nickname + " " + str(self.recPort), 'utf-8'))
					call_thread = threading.Thread(target=self.check_call, name="call_thread")
					call_thread.start()
				except (ConnectionRefusedError, OSError):
					self.app.infoBox("Connection Refused", "We are sorry, the user " + user['user'] + " is not currently available.")

	# Active call maintenance function
	def check_call(self):
		active = True 
		# While call is active 
		while active:
			# Collect answer
			response = self.clientTCP.recv(1024).decode('utf-8').split(' ')

			# Case: accept call
			if response[0] == "CALL_ACCEPTED":
				# Set caller 
				self.caller = True
				# Begin data transfer 
				self.transfer_data(response[1],response[2])
				# Show call window
				self.app.showSubWindow("Call-Port-" + str(self.recPort))

			# Case: deny call
			elif response[0] == "CALL_DENIED":
				# Show call denied 
				self.app.infoBox("Denied","Call Denied")
				# Set not active
				active = False
				# reset sockets
				self.close_connections()

			# Case: user busy
			elif response[0] == "CALL_BUSY":
				# Show caller is busy
				self.app.infoBox("Busy","Caller Busy")
				# Set not active 
				active = False
				# reset sockets
				self.close_connections()

			# Case: in-app button pressed
			else:
				self.windowCreator.callWindowControl(response[0], self.receiveBuffer, self.paused, self.busy, self.close_connections, active, self.caller)


	# Function that prepares the UDP sockets and begins the data transfer
	def transfer_data(self, name, port):
		try:
			self.busy = True
			# Create new socket for UDP receive
			self.receiveUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			# Bind socket to receive data
			self.receiveUDP.bind((self.ip, self.recPort))
			# Create new socket for UDP send
			self.sendUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			# Get the ip of user calling
			ip = self.controller.query(name)['ip']
			# Send data
			self.send_thread = threading.Thread(target=self.sendStream, args=((ip, int(port)),), daemon=True)
			# Receive data
			self.receive_thread = threading.Thread(target=self.receiveStream, daemon=True)

			# Begin threads
			self.receive_thread.start()
			self.send_thread.start()
			# Set start time 
			self.startTime = time.time()
		
		except (OSError):
			self.app.infoBox("Socket Issue", "Socket address already in use.")


	# Function that starts TCP socket connections
	def start_connections(self):
		# Creation of TCP socket
		self.serverTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Creation of TCP socket
		self.clientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Setup socket
		self.serverTCP.bind((self.ip, self.port))
		# Begin listening
		self.serverTCP.listen(1)

		while True:
      # Accept connections
			self.connection, cliaddr = self.serverTCP.accept()

			# Collect response from TCP control socket
			response = self.connection.recv(self.comSize).decode('utf-8').split(' ')

			while response != None:
				# Test for calls
				if response[0] == "CALLING":
					# Test for previously opened connections
					if self.busy == False:
						# Test for call accept
						if self.app.yesNoBox("Incoming Call", "Call from " + response[1] + ". Do you wish to accept?") == True:
							# Accept call through TCP socket
							self.connection.send(bytearray("CALL_ACCEPTED " + self.nickname + " " + str(self.recPort), 'utf-8'))
							# Begin transfer
							self.transfer_data(response[1], response[2])
							# Display caller window
							self.app.showSubWindow("Call-Port-" + str(self.recPort))
						else:
							# Send deny signal and leave connection
							self.connection.send(bytearray("CALL_DENIED " + self.nickname, 'utf-8'))
							self.close_connections()
					else:
						# Send busy signal and leave connection
						self.connection.send(bytearray("CALL_BUSY", 'utf-8'))
						self.close_connections()

				else:
					# Manage active call buttons
					self.windowCreator.callWindowControl(response[0], self.receiveBuffer, self.paused, self.busy, self.close_connections)

				# Collect response from TCP control socket
				response = self.connection.recv(self.comSize).decode('utf-8').split(' ')

	# Function to close UDP sockets
	def close_connections(self):
		self.duration = 0
		self.startTime = 0
		# Catch exceptions
		try:
			# Test for open reception socket
			if self.receiveUDP != None:
				# Send socket shutdown signal 
				self.receiveUDP.shutdown(socket.SHUT_RDWR)
				# Close socket
				self.receiveUDP.close()
				# Garbage collection
				self.receiveUDP = None
				# Join threads
				self.receive_thread.join(10.0)
			# Test for open emission socket 
			if self.sendUDP != None:
				# Send socket shutdown signal
				self.sendUDP.shutdown(socket.SHUT_RDWR)
				# Close socket
				self.sendUDP.close()
				# Garbage collection
				self.sendUDP = None
				# Join threads
				self.send_thread.join(10.0)
			# Test for open client connection
			if self.connection != None:
				# Shutdown connection
				self.connection.shutdown(socket.SHUT_RDWR)
				# Close socket 
				self.connection.close()
				# Garbage collection
				self.connection = None
			# Test for open server connection
			if self.clientTCP != None:
				# Shutdown connection
				self.clientTCP.shutdown(socket.SHUT_RDWR)
				# Detach socket
				self.clientTCP.close()
				# Garbage collection
				self.clientTCP = None
		# Catch OSError
		except (OSError):
			self.app.infoBox("Error", "Connections already closed.")


	# Function to show video in application
	def capturaVideo(self):
		# Capture video frame
		ret, frame = self.cap.read()
		frame = cv2.resize(frame, (640,480))
		cv2_im = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
		img_tk = ImageTk.PhotoImage(Image.fromarray(cv2_im))

		# Show video in GUI
		self.app.setImageData("video", img_tk, fmt = 'PhotoImage')

		# Compresión JPG al 50% de resolución (se puede variar)
		encode_param = [cv2.IMWRITE_JPEG_QUALITY,50]
		result,encimg = cv2.imencode('.jpg',frame,encode_param)
		# Test encoding
		if result == False:
			print('Error al codificar imagen')
		# Convert image to bytes
		self.current_frame = encimg.tobytes()

	# Update status bar 
	def videoStatus(self):
		# If there is a call in process
		if self.busy == True:
			self.duration = time.time() - self.startTime
		# Update status bar variables
		self.app.setStatusbar("FPS: " + str(int(self.fps)), 0)
		self.app.setStatusbar("Timestamp: " + str(self.timestamp), 1)
		self.app.setStatusbar("Resolution: " + self.res, 2)
		self.app.setStatusbar("Duration: %.2d:%.2d:%.2d" % ((self.duration/3600) % 60, (self.duration/60) % 60, self.duration % 60), 3)


	# Method that loads video into separate caller window
	def loadVideo(self, capture):
		# Decompression of video once received
		decimg = cv2.imdecode(np.frombuffer(capture,np.uint8), 1)
		# GUI video format conversion
		cv2_im = cv2.cvtColor(decimg,cv2.COLOR_BGR2RGB)
		img_tk = ImageTk.PhotoImage(Image.fromarray(cv2_im))

		# Return image
		return img_tk


    # Function that sends datagrams to the given ip and port
	def sendStream(self, cliaddr):
		# Order of packets
		num_ord = 0
		# Loop for sending data to connected party
		while self.busy == True:
			self.videoStatus()
			# If call is not paused, send data
			if self.paused == False:
				# Picture resolution
				res = self.HIGH
				# Current video frame
				# Time frame
				actual_frame = time.time()
				dif = actual_frame - self.frame_timestamp
				self.frame_timestamp = actual_frame
				# Frames per second
				fps = 1/dif
				# Package to send
				datagram = bytearray(str(num_ord) + "#" + str(actual_frame) + "#" + res + "#" + str(fps) + "#", 'utf-8') + self.current_frame
				# Send data
				self.sendUDP.sendto(datagram, cliaddr)
				# Increase number of package
				num_ord += 1


	# Function that collects datagrams from receive socket and inserts them into the receive buffer
	def receiveStream(self):
		# Continually receive data
		while self.busy == True:
			# Catch any exceptions launched by sockets
			try:
				# Only reproduce data if video is not paused
				if self.paused == False:
					dat, addr = self.receiveUDP.recvfrom(self.recSize)
					datagram = dat.split(b'#',4)
					num_ord = int(datagram[0])
					recv_timestamp = float(datagram[1])
					self.res = datagram[2].decode('utf-8')
					recv_fps = float(datagram[3])
					frame = datagram[4]
					self.recPointer += 1
					
					if self.recPointer > 1:
						self.delay = recv_timestamp - self.last_recv_timestamp
						# If the delay between packets is greater than 100 ms, we wait for that time, reducing the fps
						if self.delay > 0.1:
							print("Latency is higer than 100ms, reducing fps")
							time.sleep(self.delay)
							self.fps = round(1/self.delay)
						else:
							self.fps = 20

					self.last_recv_timestamp = recv_timestamp

					# Insert into buffer
					self.receiveBuffer.insert(num_ord, frame)
					# Set video quality
					if self.res == "HIGH" or self.res == self.HIGH:
						self.setImageResolution("HIGH")
					elif self.res == "MEDIUM" or self.res == self.MEDIUM:
						self.setImageResolution("MEDIUM")
					else:
						self.setImageResolution("LOW")

					# Buffering control
					if self.recPointer > 50 and self.repPointer <= self.recPointer:
						# Remove next frame from buffer
						current = self.receiveBuffer.pop()
						# Decode frame 
						decoded_frame = self.loadVideo(current)
						# Set image
						self.app.setImageData("videoRecv", decoded_frame, fmt ='PhotoImage')
						# Increment reproduction pointer
						self.repPointer += 1

			# Catch attribute errors
			except (AttributeError):
				self.app.infoBox("Not Available", "User no longer available.")

	# Establece la resolucion de la imagen capturada
	def setImageResolution(self, resolution):
		# Se establece la resolucion de captura de la webcam
		# Puede anadirse algun valor superior si la camara lo permite
		# pero no modificar estos
		if resolution == "LOW":
			self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
			self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
		elif resolution == "MEDIUM":
			self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
			self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
		elif resolution == "HIGH":
			self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
			self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)



if __name__ == '__main__':

	vc = VideoClient("740x620")
	# Crear aqui los threads de lectura, de recepcion y,
	# en general, todo el codigo de inicializacion que sea necesario
	# ...

	controlTCP = threading.Thread(target=vc.start_connections, name="controlTCP", daemon=True)
	controlTCP.start()


	# Lanza el bucle principal del GUI
	# El control ya NO vuelve de esta funcion, por lo que todas las
	# acciones deberan ser gestionadas desde callbacks y threads
	vc.start()
