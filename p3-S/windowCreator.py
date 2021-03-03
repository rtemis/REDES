"""
Authors: Leah Hadeed
         Nazariy Gunko

This class is responsible with the creation of all pop-up or subwindows used
in this application. To be able to manipulate the base application through 
this class, it was necessary to pass the entire application as an
argument in the constructor.
"""

# Window creator class
class windowCreator:
    app = None
    callWindowName = "Call-Port-"

    # Window Creator Constructor
    def __init__(self, app, register, recPort, call):
        self.app = app
        self.callWindowName += str(recPort)

        # Create a pop-up form
        self.app.startSubWindow("Registrarse", modal=True)
        self.app.setPadding(10,10)
        # Add username and password fields
        self.app.addLabel("userLab", "Username:", 0, 0)
        self.app.addEntry("userEnt", 0, 1)
        self.app.addLabel("passLab", "Password:", 1, 0)
        self.app.addSecretEntry("passEnt", 1, 1)
        # Add buttons to form
        self.app.addButtons( ["Submit", "Cancel"], register, colspan=2)
        # End window definition
        self.app.stopSubWindow()

        # Define call window
        self.app.startSubWindow(self.callWindowName, modal=True)
        # Add image slot for call window
        self.app.addImage("videoRecv", "imgs/webcam.gif")
        # Add buttons to call window
        self.app.addButtons(["PAUSE", "END", "RESUME"], call)
        # Create status bar
        self.app.addStatusbar(fields=4)
        # End call window definition
        self.app.stopSubWindow()

    # Method for creating a user search subwindow
    def userSearch(self, result, search):
        # Begin window definition
        self.app.startSubWindow("User-Search", modal=True)
        self.app.setPadX(10)

        # Case: User search successful
        if 'error' not in result:
            # Add user information to window
            self.app.addLabel("search-success", "Success! User Found:" , row=0,colspan=2)
            self.app.addLabel("search-user", "User: ", 1,0)
            self.app.addLabel("search-results-user", result['user'], 1,1)
            self.app.addLabel("search-ip", "IP: ", 2,0)
            self.app.addLabel("search-results-ip", result['ip'], 2,1)
            self.app.addLabel("search-port", "Port: ", 3,0)
            self.app.addLabel("search-results-port", result['port'], 3, 1)
            self.app.addLabel("search-version", "Versions accepted: ", 4, 0)
            self.app.addLabel("search-results-version", result['version'], 4,1)
            self.app.addButton("OK", self.killSearch, colspan=2)
        # Case: User search unsuccessful
        else:
            self.app.addLabel("search-error", "ERROR", row=0, colspan=2)
            self.app.addLabel("search-error-ex", "No user found with name: " + search, row=1, colspan=2)
            self.app.addButton("OK", self.killSearch, colspan=2)

        # End window definition
        self.app.stopSubWindow()

    # Method for creating an address book subwindow
    def addressBook(self, result):
        # Create new sub-window
        self.app.startSubWindow("Address Book", modal=True)

        # Create a scrollpane to be able to see all the entries
        self.app.startScrollPane("Scroller")

        # Create table headers
        self.app.addLabel("Table-user", "Username", 0,0)
        self.app.setLabelBg("Table-user","Turquoise")
        self.app.addLabel("Table-ip", "IP Address", 0,1)
        self.app.setLabelBg("Table-ip","MediumTurquoise")
        self.app.addLabel("Table-port", "Host Port", 0,2)
        self.app.setLabelBg("Table-port","Turquoise")

        # Create loop for naming objects
        i = 1
        for user in result:
            # Populate address table
            self.app.addLabel("User-" + str(i), user['user'], i, 0)
            self.app.setLabelBg("User-" + str(i),"Azure")
            self.app.addLabel("IP-" + str(i), user['ip'], i, 1)
            self.app.setLabelBg("IP-" + str(i),"MintCream")
            self.app.addLabel("Port-" + str(i), user['port'], i, 2)
            self.app.setLabelBg("Port-" + str(i),"Azure")
            i += 1

        # Close scrollpane encapsulation
        self.app.stopScrollPane()
        self.app.addButton("OK", self.killAddress, colspan=3)
        # Close sub-window encapsulation
        self.app.stopSubWindow()

    # Method for creating a registration process subwindow
    def registerWindow(self, resp):
        # Case: Successful registration
        if 'error' not in resp:
            # Disable register button
            self.app.infoBox("Welcome", "Welcome " + resp['user'] +"!")
            self.app.setToolbarButtonDisabled("REGISTER")
            # Enable other buttons
            self.app.setToolbarButtonEnabled("SEARCH")
            self.app.setToolbarButtonEnabled("ADDRESS-BOOK")
            self.app.setToolbarButtonEnabled("TELEPHONE")
            resp = None
        else:
            self.app.infoBox("Registration Error", "OOPS! Something went wrong with the registration process. Please try again.")

    # Creates infoboxes for call control
    def callWindowControl(self, response, receiveBuffer, paused, busy, close_connections, active=False, caller=False):
        # Test for call pause
        if response == "CALL_HOLD":
            # Pause the call
            self.app.infoBox("Paused","Call Paused")
            # Set call paused true
            paused = True
            # Free receive buffer
            receiveBuffer.clear()

        # Test for call resume
        if response == "CALL_RESUME":
            # Resume the call
            self.app.infoBox("Resumed","Call Resumed")
            # Set call paused false
            paused = False

        # Test for call end
        if response == "CALL_END":
            # End the call
            self.app.infoBox("Ended", "Call Ended")
            # Set caller busy false
            busy = False
            # Free receive buffer
            receiveBuffer.clear()
            
            # If user is main caller
            if caller == True:
                # Set active connection false
                active = False
                # Set caller false
                caller = False
                # Close socket connections
                close_connections()
            self.app.hideSubWindow(self.callWindowName)
        

    # Close search window
    def killSearch(self, btn):
        # When the ok button is pressed, destroy the window
        if btn == "OK":
            self.app.hideSubWindow("User-Search")
            self.app.destroySubWindow("User-Search")

    # Close the addres book window
    def killAddress(self, btn):
        # When the ok button is pressed, destroy the window
        if btn == "OK":
            self.app.hideSubWindow("Address Book")
            self.app.destroySubWindow("Address Book")