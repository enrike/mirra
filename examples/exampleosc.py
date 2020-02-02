#!/usr/bin/env python
from __future__ import print_function
from mirra import graphics
from mirra import main
from mirra import utilities

from mirra import osc

""" Mirra : 2D graphic engine in OpenGL by www.ixi-software.net
    Version alpha 0.2 -> May 05.
    Check out readme.txt and documentation.txt files
"""


class MirraApp(main.App):
    """ main appplication class, handles window contains events and graphics manager.
        Subclasses main.App and extends its public methods
    """
    def setUp(self):
        """ set here the main window properties and characteristics
        """
        self.caption = "mirra OSC example" # window name
        self.size = 640, 480 #window size
        self.pos = 100,100 # window top left location
        self.fullScreen = 0 # if fullScreen is on it will overwrite your pos and size to match the display's resolution
        self.frameRate = 15 # set refresh framerate

    def start(self):
        """ First thing to happen after the instance has been initalisiated
            good place to instanciate classes and init stuff
        """
        osc.init()
        osc.listen("127.0.0.1", 9001) # this will listen to localhost on port 9001

        osc.bind(self.squSize, "/squ") # bind function to tag
        osc.bind(self.squRot, "/amp") # bind function to tag

        graphics.Text("simple OSC example, click and check the Python terminal", 100, 20)

        self.squ = graphics.Rect(200, 200, 1, 200, 250, (0.5, 0.5, 1))


    # other general app methods defined below
    # If no object trap this events then this methods are called
    def mouseDown(self, x,y):
        """ send simple msg with mouseloc on mousedown to localhost on port 9000
        """
        osc.sendMsg("/mouseloc", (x,y)) # default sends to localhost ip '127.0.0.1' and port 9000
##        osc.sendMsg("/mouseloc", (x,y), "81.23.103.123", 67243)
        print("trying to send osc to localhost on port 9000")



    def squSize(self, *msg):
        """deals with "/print" tagged OSC addresses because it has been
            binded in the addressmanager to that particular tag
        """
        print("printing in the squSize function ", msg)
        print("the oscaddress is ", msg[0][0])
        print("the value is ", msg[0][2])

        if msg[0][2] > 0 : # if positive
            self.squ.width = msg[0][2] # change squ size to match incomming value

    def squRot(self, *msg):
        """ deals with '/amp' tagged OSC messages
            basically will range from 0 to 300 coz received amplitude will be between 0 to 1
        """
        amplitude = msg[0][2]
        self.squ.rotation = amplitude * 300



MirraApp() # init always your main app class that extends main.App




































